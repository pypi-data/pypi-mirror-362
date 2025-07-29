import asyncio
import atexit
import importlib
import inspect
import multiprocessing
import os
import socket
import re
import tempfile
from argparse import Namespace
from functools import partial
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncIterator, Optional, Set, List, Tuple

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Mount
from typing_extensions import assert_never

import vllm.envs as envs
from vllm.config import ModelConfig, VllmConfig
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.engine.protocol import EngineClient
from vllm.entrypoints.launcher import serve_http
from vllm.entrypoints.logger import RequestLogger
from vllm.entrypoints.openai.cli_args import make_arg_parser
# yapf conflicts with isort for this block
# yapf: disable
from vllm.entrypoints.openai.protocol import (ChatCompletionRequest,
                                              ChatCompletionResponse,
                                              CompletionRequest,
                                              CompletionResponse,
                                              DetokenizeRequest,
                                              DetokenizeResponse,
                                              EmbeddingRequest,
                                              EmbeddingResponse, ErrorResponse,
                                              LoadLoRAAdapterRequest,
                                              TokenizeRequest,
                                              TokenizeResponse,
                                              UnloadLoRAAdapterRequest)
from vllm.engine.multiprocessing.client import MQLLMEngineClient
from vllm.engine.multiprocessing.engine import run_mp_engine
# yapf: enable
from vllm.entrypoints.openai.serving_chat import OpenAIServingChat
from vllm.entrypoints.openai.serving_completion import OpenAIServingCompletion
from vllm.entrypoints.openai.serving_embedding import OpenAIServingEmbedding
from vllm.entrypoints.openai.serving_tokenization import (
    OpenAIServingTokenization)
from vllm.entrypoints.openai.serving_models import OpenAIServingModels
from vllm.entrypoints.openai.serving_models import BaseModelPath
from vllm.logger import init_logger
from vllm.usage.usage_lib import UsageContext
from vllm.transformers_utils.config import (
    maybe_register_config_serialize_by_value)
from vllm.utils import FlexibleArgumentParser, get_open_zmq_ipc_path, is_valid_ipv6_address
from vllm.version import __version__ as VLLM_VERSION

# import for generate api
import json
from typing import AsyncGenerator
from vllm.sampling_params import SamplingParams
from vllm.usage.usage_lib import UsageContext
from vllm.utils import random_uuid

from llm.optimized.inference.interceptor import InterceptorFactory

TIMEOUT_KEEP_ALIVE = 5  # seconds

async_engine_client: EngineClient
engine_args: AsyncEngineArgs
openai_serving_chat: OpenAIServingChat
openai_serving_completion: OpenAIServingCompletion
openai_serving_embedding: OpenAIServingEmbedding
openai_serving_tokenization: OpenAIServingTokenization
prometheus_multiproc_dir: tempfile.TemporaryDirectory

# Cannot use __name__ (https://github.com/vllm-project/vllm/pull/4765)
logger = init_logger('vllm.entrypoints.openai.api_server')

_running_tasks: Set[asyncio.Task] = set()

@asynccontextmanager
async def lifespan(app: FastAPI):

    async def _force_log():
        while True:
            await asyncio.sleep(10)
            await async_engine_client.do_log_stats()

    if not engine_args.disable_log_stats:
        task = asyncio.create_task(_force_log())
        _running_tasks.add(task)
        task.add_done_callback(_running_tasks.remove)

    yield


@asynccontextmanager
async def build_async_engine_client(
        args: Namespace) -> AsyncIterator[Optional[EngineClient]]:

    # Context manager to handle async_engine_client lifecycle
    # Ensures everything is shutdown and cleaned up on error/exit
    global engine_args
    engine_args = AsyncEngineArgs.from_cli_args(args)

    # Backend itself still global for the silly lil' health handler
    global async_engine_client

    async with build_async_engine_client_from_engine_args(
            engine_args, args.disable_frontend_multiprocessing) as engine:

        async_engine_client = engine  # type: ignore[assignment]
        yield engine

@asynccontextmanager
async def build_async_engine_client_from_engine_args(
    engine_args: AsyncEngineArgs,
    disable_frontend_multiprocessing: bool = False,
) -> AsyncIterator[Optional[EngineClient]]:
    """
    Create EngineClient, either:
        - in-process using the AsyncLLMEngine Directly
        - multiprocess using AsyncLLMEngine RPC

    Returns the Client or None if the creation failed.
    """

    # If manually triggered or embedding model, use AsyncLLMEngine in process.
    # TODO: support embedding model via RPC.
    usage_context = UsageContext.OPENAI_API_SERVER
    vllm_config = engine_args.create_engine_config(usage_context=usage_context)

    # V1 AsyncLLM.
    if envs.VLLM_USE_V1:
        if disable_frontend_multiprocessing:
            logger.warning(
                "V1 is enabled, but got --disable-frontend-multiprocessing. "
                "To disable frontend multiprocessing, set VLLM_USE_V1=0.")

        from vllm.v1.engine.async_llm import AsyncLLM
        async_llm: Optional[AsyncLLM] = None
        try:
            async_llm = AsyncLLM.from_vllm_config(
                vllm_config=vllm_config,
                usage_context=usage_context,
                disable_log_requests=engine_args.disable_log_requests,
                disable_log_stats=engine_args.disable_log_stats)
            yield async_llm
        finally:
            if async_llm:
                async_llm.shutdown()

    # V0 AsyncLLM.
    elif (MQLLMEngineClient.is_unsupported_config(vllm_config)
          or disable_frontend_multiprocessing):

        engine_client: Optional[EngineClient] = None
        try:
            engine_client = AsyncLLMEngine.from_vllm_config(
                vllm_config=vllm_config,
                usage_context=usage_context,
                disable_log_requests=engine_args.disable_log_requests,
                disable_log_stats=engine_args.disable_log_stats)
            yield engine_client
        finally:
            if engine_client and hasattr(engine_client, "shutdown"):
                engine_client.shutdown()

    # V0MQLLMEngine.
    else:
        if "PROMETHEUS_MULTIPROC_DIR" not in os.environ:
            # Make TemporaryDirectory for prometheus multiprocessing
            # Note: global TemporaryDirectory will be automatically
            #   cleaned up upon exit.
            global prometheus_multiproc_dir
            prometheus_multiproc_dir = tempfile.TemporaryDirectory()
            os.environ[
                "PROMETHEUS_MULTIPROC_DIR"] = prometheus_multiproc_dir.name
        else:
            logger.warning(
                "Found PROMETHEUS_MULTIPROC_DIR was set by user. "
                "This directory must be wiped between vLLM runs or "
                "you will find inaccurate metrics. Unset the variable "
                "and vLLM will properly handle cleanup.")

        # Select random path for IPC.
        ipc_path = get_open_zmq_ipc_path()
        logger.debug("Multiprocessing frontend to use %s for IPC Path.",
                     ipc_path)

        # Start RPCServer in separate process (holds the LLMEngine).
        # the current process might have CUDA context,
        # so we need to spawn a new process
        context = multiprocessing.get_context("spawn")

        # Ensure we can serialize transformer config before spawning
        maybe_register_config_serialize_by_value()

        # The Process can raise an exception during startup, which may
        # not actually result in an exitcode being reported. As a result
        # we use a shared variable to communicate the information.
        engine_alive = multiprocessing.Value('b', True, lock=False)
        engine_process = context.Process(
            target=run_mp_engine,
            args=(vllm_config, UsageContext.OPENAI_API_SERVER, ipc_path,
                  engine_args.disable_log_stats,
                  engine_args.disable_log_requests, engine_alive))
        engine_process.start()
        engine_pid = engine_process.pid
        assert engine_pid is not None, "Engine process failed to start."
        logger.info("Started engine process with PID %d", engine_pid)

        def _cleanup_ipc_path():
            socket_path = ipc_path.replace("ipc://", "")
            if os.path.exists(socket_path):
                os.remove(socket_path)

        # Ensure we clean up the local IPC socket file on exit.
        atexit.register(_cleanup_ipc_path)

        # Build RPCClient, which conforms to EngineClient Protocol.
        build_client = partial(MQLLMEngineClient, ipc_path, vllm_config,
                               engine_pid)
        mq_engine_client = await asyncio.get_running_loop().run_in_executor(
            None, build_client)
        try:
            while True:
                try:
                    await mq_engine_client.setup()
                    break
                except TimeoutError:
                    if (not engine_process.is_alive()
                            or not engine_alive.value):
                        raise RuntimeError(
                            "Engine process failed to start. See stack "
                            "trace for the root cause.") from None

            yield mq_engine_client  # type: ignore[misc]
        finally:
            # Ensure rpc server process was terminated
            engine_process.terminate()

            # Close all open connections to the backend
            mq_engine_client.close()

            # Wait for engine process to join
            engine_process.join(4)
            if engine_process.exitcode is None:
                # Kill if taking longer than 5 seconds to stop
                engine_process.kill()

            # Lazy import for prometheus multiprocessing.
            # We need to set PROMETHEUS_MULTIPROC_DIR environment variable
            # before prometheus_client is imported.
            # See https://prometheus.github.io/client_python/multiprocess/
            from prometheus_client import multiprocess
            multiprocess.mark_process_dead(engine_process.pid)


router = APIRouter()


def mount_metrics(app: FastAPI):
    # Lazy import for prometheus multiprocessing.
    # We need to set PROMETHEUS_MULTIPROC_DIR environment variable
    # before prometheus_client is imported.
    # See https://prometheus.github.io/client_python/multiprocess/
    from prometheus_client import (CollectorRegistry, make_asgi_app,
                                   multiprocess)

    prometheus_multiproc_dir_path = os.getenv("PROMETHEUS_MULTIPROC_DIR", None)
    if prometheus_multiproc_dir_path is not None:
        logger.info("vLLM to use %s as PROMETHEUS_MULTIPROC_DIR",
                    prometheus_multiproc_dir_path)
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)

        # Add prometheus asgi middleware to route /metrics requests
        metrics_route = Mount("/metrics", make_asgi_app(registry=registry))
    else:
        # Add prometheus asgi middleware to route /metrics requests
        metrics_route = Mount("/metrics", make_asgi_app())

    # Workaround for 307 Redirect for /metrics
    metrics_route.path_regex = re.compile("^/metrics(?P<path>.*)$")
    app.routes.append(metrics_route)


@router.get("/health")
async def health() -> Response:
    """Health check."""
    await async_engine_client.check_health()
    return Response(status_code=200)


@router.post("/tokenize")
async def tokenize(request: TokenizeRequest):
    generator = await openai_serving_tokenization.create_tokenize(request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    elif isinstance(generator, TokenizeResponse):
        return JSONResponse(content=generator.model_dump())

    assert_never(generator)


@router.post("/detokenize")
async def detokenize(request: DetokenizeRequest):
    generator = await openai_serving_tokenization.create_detokenize(request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    elif isinstance(generator, DetokenizeResponse):
        return JSONResponse(content=generator.model_dump())

    assert_never(generator)


@router.get("/v1/models")
async def show_available_models():
    models = await openai_serving_completion.show_available_models()
    return JSONResponse(content=models.model_dump())


@router.get("/version")
async def show_version():
    ver = {"version": VLLM_VERSION}
    return JSONResponse(content=ver)

@router.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest,
                                 raw_request: Request):

    request = InterceptorFactory.get_interceptor().modify_request(request=request)

    generator = await openai_serving_chat.create_chat_completion(
        request, raw_request)

    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)

    elif isinstance(generator, ChatCompletionResponse):
        return JSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


@router.post("/v1/completions")
async def create_completion(request: CompletionRequest, raw_request: Request):
    generator = await openai_serving_completion.create_completion(
        request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    elif isinstance(generator, CompletionResponse):
        return JSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


@router.post("/v1/embeddings")
async def create_embedding(request: EmbeddingRequest, raw_request: Request):
    generator = await openai_serving_embedding.create_embedding(
        request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    elif isinstance(generator, EmbeddingResponse):
        return JSONResponse(content=generator.model_dump())

    assert_never(generator)


@router.post("/generate")
async def generate(request: Request) -> Response:
    """Generate completion for the request.

    The request should be a JSON object with the following fields:
    - prompt: the prompt to use for the generation.
    - stream: whether to stream the results or not.
    - other fields: the sampling parameters (See `SamplingParams` for details).
    """
    generate_openai_response = False
    if "generate_openai_response" in request.headers:
        generate_openai_response = request.headers["generate_openai_response"] == "true"
    
    if generate_openai_response:
        request_dict = await request.json()
        prompt = request_dict.pop("prompt")
        stream = request_dict.pop("stream", False)
        sampling_params = SamplingParams(**request_dict)
        request_id = random_uuid()
        # create ChatCompletionRequest object
        # load messages from prompt
        messages = json.loads(prompt)

        chat_request = ChatCompletionRequest(
            model=served_model_names[0],
            messages=messages,
            stream=stream,
            **request_dict
        )

        chat_request = InterceptorFactory.get_interceptor().modify_request(request=chat_request)

        generator = await openai_serving_chat.create_chat_completion(
            chat_request, request)
        logger.info(f"OpenAI response {generator.model_dump()}")
        if isinstance(generator, ErrorResponse):
            return JSONResponse(content=generator.model_dump(),
                                status_code=generator.code)
        if chat_request.stream:
            return StreamingResponse(content=generator,
                                    media_type="text/event-stream")
        else:
            assert isinstance(generator, ChatCompletionResponse)
            response = JSONResponse(content=generator.model_dump())
            return response
    else:
        request_dict = await request.json()
        prompt = request_dict.pop("prompt")
        stream = request_dict.pop("stream", False)
        sampling_params = SamplingParams(**request_dict)
        request_id = random_uuid()
        assert async_engine_client is not None

        results_generator = async_engine_client.generate(prompt=prompt, sampling_params=sampling_params, request_id=request_id)
        # Streaming case
        async def stream_results() -> AsyncGenerator[bytes, None]:
            async for request_output in results_generator:
                prompt = request_output.prompt
                text_outputs = [
                    prompt + output.text for output in request_output.outputs
                ]
                ret = {"text": text_outputs}
                yield (json.dumps(ret) + "\0").encode("utf-8")
        if stream:
            return StreamingResponse(stream_results())
        # Non-streaming case
        final_output = None
        async for request_output in results_generator:
            if await request.is_disconnected():
                # Abort the request if the client disconnects.
                await async_engine_client.abort(request_id)
                return Response(status_code=499)
            final_output = request_output
        assert final_output is not None
        prompt = final_output.prompt
        text_outputs = [prompt + output.text for output in final_output.outputs]
        ret = {"text": text_outputs}
        return JSONResponse(ret)



if envs.VLLM_TORCH_PROFILER_DIR:
    logger.warning(
        "Torch Profiler is enabled in the API server. This should ONLY be "
        "used for local development!")

    @router.post("/start_profile")
    async def start_profile():
        logger.info("Starting profiler...")
        await async_engine_client.start_profile()
        logger.info("Profiler started.")
        return Response(status_code=200)

    @router.post("/stop_profile")
    async def stop_profile():
        logger.info("Stopping profiler...")
        await async_engine_client.stop_profile()
        logger.info("Profiler stopped.")
        return Response(status_code=200)


if envs.VLLM_ALLOW_RUNTIME_LORA_UPDATING:
    logger.warning(
        "Lora dynamic loading & unloading is enabled in the API server. "
        "This should ONLY be used for local development!")

    @router.post("/v1/load_lora_adapter")
    async def load_lora_adapter(request: LoadLoRAAdapterRequest):
        response = await openai_serving_chat.load_lora_adapter(request)
        if isinstance(response, ErrorResponse):
            return JSONResponse(content=response.model_dump(),
                                status_code=response.code)

        response = await openai_serving_completion.load_lora_adapter(request)
        if isinstance(response, ErrorResponse):
            return JSONResponse(content=response.model_dump(),
                                status_code=response.code)

        return Response(status_code=200, content=response)

    @router.post("/v1/unload_lora_adapter")
    async def unload_lora_adapter(request: UnloadLoRAAdapterRequest):
        response = await openai_serving_chat.unload_lora_adapter(request)
        if isinstance(response, ErrorResponse):
            return JSONResponse(content=response.model_dump(),
                                status_code=response.code)

        response = await openai_serving_completion.unload_lora_adapter(request)
        if isinstance(response, ErrorResponse):
            return JSONResponse(content=response.model_dump(),
                                status_code=response.code)

        return Response(status_code=200, content=response)


def build_app(args: Namespace) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    app.root_path = args.root_path

    mount_metrics(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=args.allowed_origins,
        allow_credentials=args.allow_credentials,
        allow_methods=args.allowed_methods,
        allow_headers=args.allowed_headers,
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_, exc):
        err = openai_serving_chat.create_error_response(message=str(exc))
        return JSONResponse(err.model_dump(),
                            status_code=HTTPStatus.BAD_REQUEST)

    if token := envs.VLLM_API_KEY or args.api_key:

        @app.middleware("http")
        async def authentication(request: Request, call_next):
            root_path = "" if args.root_path is None else args.root_path
            if request.method == "OPTIONS":
                return await call_next(request)
            if not request.url.path.startswith(f"{root_path}/v1"):
                return await call_next(request)
            if request.headers.get("Authorization") != "Bearer " + token:
                return JSONResponse(content={"error": "Unauthorized"},
                                    status_code=401)
            return await call_next(request)

    for middleware in args.middleware:
        module_path, object_name = middleware.rsplit(".", 1)
        imported = getattr(importlib.import_module(module_path), object_name)
        if inspect.isclass(imported):
            app.add_middleware(imported)
        elif inspect.iscoroutinefunction(imported):
            app.middleware("http")(imported)
        else:
            raise ValueError(f"Invalid middleware {middleware}. "
                             f"Must be a function or a class.")

    return app

def _get_base_model_paths(served_model_names : List[str]):
    base_model_path : List[BaseModelPath] = []
    for model_name in served_model_names:
        model_path = BaseModelPath(model_name, model_name)
        base_model_path.append(model_path)
    return base_model_path

def create_server_socket(addr: Tuple[str, int]) -> socket.socket:
    family = socket.AF_INET
    if is_valid_ipv6_address(addr[0]):
        family = socket.AF_INET6

    sock = socket.socket(family=family, type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(addr)

    return sock

async def init_app(
    async_engine_client: EngineClient,
    args: Namespace,
) -> FastAPI:
    app = build_app(args)

    if args.served_model_name is not None:
        served_model_names = args.served_model_name
    else:
        served_model_names = [args.model]

    model_config = await async_engine_client.get_model_config()

    if args.disable_log_requests:
        request_logger = None
    else:
        request_logger = RequestLogger(max_log_len=args.max_log_len)

    global openai_serving_chat
    global openai_serving_completion
    global openai_serving_embedding
    global openai_serving_tokenization

    base_model_paths = _get_base_model_paths(served_model_names)
    openai_serving_models = OpenAIServingModels(
        engine_client=async_engine_client,
        model_config=model_config,
        base_model_paths=base_model_paths,
        lora_modules=args.lora_modules,
        prompt_adapters=args.prompt_adapters,
    )

    openai_serving_chat = OpenAIServingChat(
        async_engine_client,
        model_config,
        openai_serving_models,
        args.response_role,
        request_logger=request_logger,
        chat_template=args.chat_template,
        chat_template_content_format=args.chat_template_content_format,
        return_tokens_as_token_ids=args.return_tokens_as_token_ids,
        enable_auto_tools=args.enable_auto_tool_choice,
        tool_parser=args.tool_call_parser,
        enable_prompt_tokens_details=args.enable_prompt_tokens_details)
    openai_serving_completion = OpenAIServingCompletion(
        async_engine_client,
        model_config,
        openai_serving_models,
        request_logger=request_logger,
        return_tokens_as_token_ids=args.return_tokens_as_token_ids,
    )
    openai_serving_embedding = OpenAIServingEmbedding(
        async_engine_client,
        model_config,
        openai_serving_models,
        request_logger=request_logger,
        chat_template=args.chat_template,
        chat_template_content_format=args.chat_template_content_format
    )
    openai_serving_tokenization = OpenAIServingTokenization(
        async_engine_client,
        model_config,
        openai_serving_models,
        request_logger=request_logger,
        chat_template=args.chat_template,
        chat_template_content_format=args.chat_template_content_format
    )
    app.root_path = args.root_path

    #Fix AttributeError: 'State' object has no attribute 'engine_client'
    app.state.engine_client = async_engine_client

    return app


async def run_server(args, **uvicorn_kwargs) -> None:
    logger.info("vLLM API server version %s", VLLM_VERSION)
    logger.info("args: %s", args)

    async with build_async_engine_client(args) as async_engine_client:
        # If None, creation of the client failed and we exit.
        if async_engine_client is None:
            return

        app = await init_app(async_engine_client, args)
        sock_addr = (args.host or "", args.port)
        sock = create_server_socket(sock_addr)

        shutdown_task = await serve_http(
            app,
            sock=sock,
            host=args.host,
            port=args.port,
            log_level=args.uvicorn_log_level,
            timeout_keep_alive=TIMEOUT_KEEP_ALIVE,
            ssl_keyfile=args.ssl_keyfile,
            ssl_certfile=args.ssl_certfile,
            ssl_ca_certs=args.ssl_ca_certs,
            ssl_cert_reqs=args.ssl_cert_reqs,
            **uvicorn_kwargs,
        )

    # NB: Await server shutdown only after the backend context is exited
    await shutdown_task


if __name__ == "__main__":
    # NOTE(simon):
    # This section should be in sync with vllm/scripts.py for CLI entrypoints.
    parser = FlexibleArgumentParser(
        description="vLLM OpenAI-Compatible RESTful API server.")
    parser = make_arg_parser(parser)
    args = parser.parse_args()
    if args.served_model_name is not None:
        served_model_names = args.served_model_name
    else:
        served_model_names = [args.model]

    asyncio.run(run_server(args))
