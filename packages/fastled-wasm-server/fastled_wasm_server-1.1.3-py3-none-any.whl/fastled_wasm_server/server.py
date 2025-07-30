"""FastLED WASM Server."""

import json
import os
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from disklru import DiskLRUCache
from fastapi import (
    BackgroundTasks,
    Body,
    FastAPI,
    File,
    Header,
    HTTPException,
    UploadFile,
)
from fastapi.responses import (
    FileResponse,
    RedirectResponse,
    StreamingResponse,
)
from fastled_wasm_compiler import Compiler
from fastled_wasm_compiler.dwarf_path_to_file_path import (
    dwarf_path_to_file_path,
)

from fastled_wasm_server.compile_lock import COMPILE_LOCK
from fastled_wasm_server.examples import EXAMPLES
from fastled_wasm_server.models import DwarfSourceRequest
from fastled_wasm_server.paths import (  # The folder where the actual source code is located.; FASTLED_SRC,
    COMPILER_ROOT,
    OUTPUT_DIR,
    SKETCH_CACHE_FILE,
    UPLOAD_DIR,
    VOLUME_MAPPED_SRC,
)
from fastled_wasm_server.server_compile import ServerWasmCompiler
from fastled_wasm_server.server_fetch_example import (
    fetch_example,
)
from fastled_wasm_server.server_misc import start_memory_watchdog
from fastled_wasm_server.session_manager import SessionManager
from fastled_wasm_server.types import BuildMode, CompilerStats
from fastled_wasm_server.upload_size_middleware import UploadSizeMiddleware

_COMPILER_STATS = CompilerStats()
_SESSION_MANAGER = SessionManager()

_TEST = False
_UPLOAD_LIMIT = 10 * 1024 * 1024
_MEMORY_LIMIT_MB = int(os.environ.get("MEMORY_LIMIT_MB", "0"))  # 0 means disabled

_LIVE_GIT_UPDATES_INTERVAL = int(
    os.environ.get("LIVE_GIT_UPDATE_INTERVAL", 60 * 60 * 24)
)  # Update every 24 hours
_ALLOW_SHUTDOWN = os.environ.get("ALLOW_SHUTDOWN", "false").lower() in ["true", "1"]
_NO_SKETCH_CACHE = os.environ.get("NO_SKETCH_CACHE", "false").lower() in ["true", "1"]

# debug is a 20mb payload for the symbol information.
_ONLY_QUICK_BUILDS = os.environ.get("ONLY_QUICK_BUILDS", "false").lower() in [
    "true",
    "1",
]

_ALLOW_CODE_SYNC = False

_LIVE_GIT_UPDATES_ENABLED = False

if _NO_SKETCH_CACHE:
    print("Sketch caching disabled")

UPLOAD_DIR.mkdir(exist_ok=True)
START_TIME = time.time()

OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize disk cache
SKETCH_CACHE_MAX_ENTRIES = 50
SKETCH_CACHE = DiskLRUCache(str(SKETCH_CACHE_FILE), SKETCH_CACHE_MAX_ENTRIES)

# New compiler type that will replace the legacy ones.
_NEW_COMPILER = Compiler(
    volume_mapped_src=VOLUME_MAPPED_SRC,
)

_COMPILER = ServerWasmCompiler(
    compiler_root=COMPILER_ROOT,
    sketch_cache=SKETCH_CACHE,
    compiler=_NEW_COMPILER,
    only_quick_builds=_ONLY_QUICK_BUILDS,
    compiler_lock=COMPILE_LOCK,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting FastLED wasm compiler server...")
    try:
        print(f"Settings: {json.dumps(get_settings(), indent=2)}")
    except Exception as e:
        print(f"Error getting settings: {e}")

    if _MEMORY_LIMIT_MB > 0:
        print(f"Starting memory watchdog (limit: {_MEMORY_LIMIT_MB}MB)")
        start_memory_watchdog(_MEMORY_LIMIT_MB)

    if _ALLOW_CODE_SYNC:
        print("Code sync disabled, skipping code sync")
    else:
        print("Code sync disabled")

    yield  # end startup
    return  # end shutdown


app = FastAPI(lifespan=lifespan)

app.add_middleware(UploadSizeMiddleware, max_upload_size=_UPLOAD_LIMIT)


def try_get_cached_zip(hash: str) -> bytes | None:
    if _NO_SKETCH_CACHE:
        print("Sketch caching disabled, skipping cache get")
        return None
    return SKETCH_CACHE.get_bytes(hash)


def get_settings() -> dict:
    """Get server settings."""
    return {
        "volume_mapped_src": str(VOLUME_MAPPED_SRC),
        "volume_mapped_src_exists": VOLUME_MAPPED_SRC.exists(),
        "output_dir": str(OUTPUT_DIR),
        "only_quick_builds": _ONLY_QUICK_BUILDS,
        "allow_code_sync": _ALLOW_CODE_SYNC,
        "allow_shutdown": _ALLOW_SHUTDOWN,
        "no_sketch_cache": _NO_SKETCH_CACHE,
        "memory_limit_mb": _MEMORY_LIMIT_MB,
        "live_git_updates_enabled": _LIVE_GIT_UPDATES_ENABLED,
        "live_git_updates_interval": _LIVE_GIT_UPDATES_INTERVAL,
        "upload_limit": _UPLOAD_LIMIT,
        "sketch_cache_max_entries": SKETCH_CACHE_MAX_ENTRIES,
        "uptime": time.time() - START_TIME,
    }


@app.get("/", include_in_schema=False)
async def read_root() -> RedirectResponse:
    """Redirect to the /docs endpoint."""

    print("Endpoint accessed: / (root redirect to docs)")
    return RedirectResponse(url="/docs")


@app.get("/healthz")
async def health_check() -> dict:
    """Health check endpoint."""
    print("Endpoint accessed: /healthz")
    return {"status": "ok"}


@app.get("/settings")
async def get_server_settings() -> dict:
    """Get server settings."""
    print("Endpoint accessed: /settings")
    return get_settings()


@app.get("/info")
async def get_info() -> dict:
    """Get server information."""
    print("Endpoint accessed: /info")
    return {
        "examples": EXAMPLES,
        "stats": {
            "compile_count": _COMPILER_STATS.compile_count,
            "compile_failures": _COMPILER_STATS.compile_failures,
            "compile_successes": _COMPILER_STATS.compile_successes,
            "compiler_in_use": COMPILE_LOCK.locked(),
        },
        "settings": get_settings(),
    }


@app.get("/compile/wasm/inuse")
async def is_compiler_in_use() -> dict:
    """Check if compiler is in use."""
    print("Endpoint accessed: /compile/wasm/inuse")
    return {"in_use": COMPILE_LOCK.locked()}


@app.get("/shutdown")
async def shutdown_server(session_id: int | None = Header(None)) -> dict:
    """Shutdown the server."""
    print("Endpoint accessed: /shutdown")
    if not _ALLOW_SHUTDOWN:
        raise HTTPException(status_code=403, detail="Shutdown not allowed")

    if not _TEST and (
        session_id is None or not _SESSION_MANAGER.session_exists(session_id)
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"status": "ok"}


@app.post("/session/start")
async def start_session() -> dict:
    """Start a new session and return session ID."""
    print("Endpoint accessed: /session/start")
    session_id = _SESSION_MANAGER.generate_session_id()
    session_info = _SESSION_MANAGER.get_session_info(session_id)
    return {
        "session_id": session_id,
        "session_info": session_info,
    }


@app.post("/project/init")
def project_init_example(
    background_tasks: BackgroundTasks, example: str = Body(...)
) -> FileResponse:
    """Archive /git/fastled/examples/{example} into a zip file and return it."""
    print(f"Endpoint accessed: /project/init/example with example: {example}")
    out: FileResponse = fetch_example(
        background_tasks=background_tasks, example=example
    )
    return out


@app.post("/dwarfsource")
async def get_dwarf_source(
    request: DwarfSourceRequest, session_id: int | None = Header(None)
) -> str:
    """Get source file content for debugging."""
    print(f"Endpoint accessed: /dwarfsource with path: {request.path}")

    if not _TEST and (
        session_id is None or not _SESSION_MANAGER.session_exists(session_id)
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        file_path = dwarf_path_to_file_path(request.path)
        if file_path is None:
            raise HTTPException(status_code=404, detail="File not found")
        if isinstance(file_path, Exception):
            raise HTTPException(status_code=404, detail=str(file_path))
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compile/wasm")
def compile_wasm(
    file: UploadFile = File(...),
    build: str | None = Header(None),
    profile: str | None = Header(None),
    strict: bool = Header(False),
    allow_libcompile: bool = Header(True),
    no_platformio: bool | None = Header(None),
    native: bool | None = Header(None),
    session_id: int | None = Header(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> FileResponse:
    """Upload a file into a temporary directory."""

    # Handle session management
    if session_id is None:
        session_id = _SESSION_MANAGER.generate_session_id()
    else:
        if not _SESSION_MANAGER.touch_session(session_id):
            session_id = _SESSION_MANAGER.generate_session_id()

    session_info = _SESSION_MANAGER.get_session_info(session_id)

    # Convert build string to BuildMode enum
    try:
        build_type = BuildMode.from_string(build or "quick")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Handle native parameter with environment variable fallback
    if native is None:
        native = os.environ.get("NATIVE", "0") == "1"

    # Handle no_platformio parameter with environment variable fallback
    if no_platformio is None:
        no_platformio = os.environ.get("NO_PLATFORMIO", "0") == "1"

    # If native is True, automatically set no_platformio to True
    if native:
        no_platformio = True

    print(
        f"Endpoint accessed: /compile/wasm with file: {file.filename}, build: {build_type.value}, profile: {profile}, no_platformio: {no_platformio}, native: {native}, session: {session_info}"
    )

    file_response = _COMPILER.compile(
        file=file,
        build=build_type.value,
        profile=profile or "",
        output_dir=OUTPUT_DIR,
        use_sketch_cache=not _NO_SKETCH_CACHE,
        background_tasks=background_tasks,
        strict=strict,
        no_platformio=no_platformio,
        native=native,
        allow_libcompile=allow_libcompile,
    )

    # Add session information to response headers
    file_response.headers["X-Session-Id"] = str(session_id)
    file_response.headers["X-Session-Info"] = session_info
    return file_response


@app.post("/compile/libfastled")
async def compile_libfastled(
    build: str | None = Header(None),
    dry_run: str = Header("false"),
    session_id: int | None = Header(None),
) -> StreamingResponse:
    """Compile libfastled library and stream the compilation output."""

    # Simple session validation - either no session required or valid session
    if (
        not _TEST
        and session_id is not None
        and not _SESSION_MANAGER.session_exists(session_id)
    ):
        raise HTTPException(status_code=401, detail="Invalid session")

    # Convert build string to BuildMode enum
    try:
        build_type = BuildMode.from_string(build or "quick")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Parse dry_run string to boolean
    dry_run_bool = dry_run.lower() in ["true", "1", "yes"]

    print(
        f"Endpoint accessed: /compile/libfastled with build: {build_type.value}, dry_run: {dry_run_bool}"
    )

    async def stream_compilation() -> AsyncGenerator[bytes, None]:
        """Stream the compilation output line by line."""
        try:
            yield f"data: Using BUILD_MODE: {build_type.value.upper()}\n".encode()
            if dry_run_bool:
                yield b"data: DRY RUN MODE: Will skip actual compilation\n"
                yield f"data: Would compile libfastled with BUILD_MODE={build_type.value.upper()}\n".encode()
                yield b"data: COMPILATION_COMPLETE\ndata: EXIT_CODE: 0\ndata: STATUS: SUCCESS\n"
                return

            # For now, return an informative error about the missing functionality
            yield b"data: Starting libfastled compilation...\n"
            yield b"data: ERROR: libfastled compilation requires a properly configured environment\n"
            yield b"data: The FastLED source directory is not available in this environment\n"
            yield f"data: Expected source at: {VOLUME_MAPPED_SRC}\n".encode()
            yield b"data: This endpoint is designed for Docker/container environments\n"
            yield b"data: COMPILATION_FAILED\ndata: EXIT_CODE: 1\ndata: STATUS: FAIL\n"

        except Exception as e:
            yield f"data: ERROR: {str(e)}\n".encode()
            yield b"data: COMPILATION_FAILED\ndata: EXIT_CODE: 1\ndata: STATUS: FAIL\n"

    return StreamingResponse(stream_compilation(), media_type="text/event-stream")
