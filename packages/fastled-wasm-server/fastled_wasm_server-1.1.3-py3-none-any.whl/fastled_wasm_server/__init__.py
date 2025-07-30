"""FastLED WASM Server package."""

from collections.abc import AsyncGenerator, Generator
from pathlib import Path

from fastled_wasm_server.models import (
    CompilerInUseResponse,
    DwarfSourceRequest,
    HealthResponse,
    ServerInfo,
    ServerSettings,
    SessionResponse,
)
from fastled_wasm_server.types import BuildMode

# Default timeout for HTTP requests (in seconds)
_DEFAULT_TIMEOUT = 60.0


class ClientAsync:
    """
    Async API interface for FastLED WASM server operations.

    This class provides an async client interface for all FastLED WASM server operations.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = _DEFAULT_TIMEOUT,
    ):
        """
        Initialize the FastLED WASM API.

        Args:
            base_url: Base URL of the FastLED WASM server
            timeout: Request timeout in seconds
        """
        from .client_async import ClientAsyncImpl

        # Use async client implementation
        self._client = ClientAsyncImpl(
            base_url=base_url,
            timeout=timeout,
        )

    @property
    def base_url(self) -> str:
        """Get the base URL from the implementation."""
        return self._client.base_url

    @property
    def timeout(self) -> float:
        """Get the timeout from the implementation."""
        return self._client.timeout

    # Context manager support for async client
    async def __aenter__(self):
        """Async context manager entry."""
        return await self._client.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        """Close the HTTP client."""
        await self._client.close()

    async def health_check(self) -> HealthResponse:
        """
        Perform a health check on the server.

        Returns:
            HealthResponse: Server health status
        """
        return await self._client.health_check()

    async def get_settings(self) -> ServerSettings:
        """
        Get server settings.

        Returns:
            ServerSettings: Current server settings
        """
        return await self._client.get_settings()

    async def get_info(self) -> ServerInfo:
        """
        Get server information including available examples and statistics.

        Returns:
            ServerInfo: Server information and statistics
        """
        return await self._client.get_info()

    async def is_compiler_in_use(self) -> CompilerInUseResponse:
        """
        Check if the compiler is currently in use.

        Returns:
            CompilerInUseResponse: Compiler usage status
        """
        return await self._client.is_compiler_in_use()

    async def shutdown_server(self) -> dict[str, str]:
        """
        Shutdown the server (if allowed by server configuration).

        Returns:
            Dict[str, str]: Shutdown status
        """
        return await self._client.shutdown_server()

    async def init_project(self, example: str | None = None) -> bytes:
        """
        Initialize a new project with default or specified example.

        Args:
            example: Optional example name. If None, uses default example.

        Returns:
            bytes: ZIP file content of the initialized project
        """
        return await self._client.init_project(example)

    async def get_dwarf_source(self, path: str) -> str:
        """
        Get source file content for debugging.

        Args:
            path: Path to the source file

        Returns:
            str: Source file content
        """
        return await self._client.get_dwarf_source(path)

    async def start_session(self) -> SessionResponse:
        """
        Start a new session and get session ID.

        Returns:
            SessionResponse: Session ID and info
        """
        return await self._client.start_session()

    async def compile_wasm(
        self,
        file_path: str | Path,
        build: BuildMode = BuildMode.QUICK,
        profile: str | None = None,
        strict: bool = False,
        no_platformio: bool | None = None,
        native: bool | None = None,
        session_id: int | None = None,
        allow_libcompile: bool = True,
    ) -> bytes:
        """
        Compile a WASM file.

        Args:
            file_path: Path to the file to compile
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            profile: Profile setting
            strict: Enable strict compilation
            no_platformio: Disable PlatformIO usage
            native: Enable native compilation
            session_id: Session ID for tracking
            allow_libcompile: Allow library compilation

        Returns:
            bytes: Compiled WASM file content
        """
        return await self._client.compile_wasm(
            file_path,
            build,
            profile,
            strict,
            no_platformio,
            native,
            session_id,
            allow_libcompile=allow_libcompile,
        )

    async def compile_wasm_with_file_content(
        self,
        file_content: bytes,
        filename: str,
        build: BuildMode = BuildMode.QUICK,
        profile: str | None = None,
        strict: bool = False,
        no_platformio: bool | None = None,
        native: bool | None = None,
        session_id: int | None = None,
    ) -> bytes:
        """
        Compile WASM from file content (without saving to disk).

        Args:
            file_content: Content of the file to compile
            filename: Name of the file (for server reference)
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            profile: Profile setting
            strict: Enable strict compilation
            no_platformio: Disable PlatformIO usage
            native: Enable native compilation
            session_id: Session ID for tracking

        Returns:
            bytes: Compiled WASM file content
        """
        return await self._client.compile_wasm_with_file_content(
            file_content,
            filename,
            build,
            profile,
            strict,
            no_platformio,
            native,
            session_id,
        )

    async def compile_libfastled(
        self, build: BuildMode = BuildMode.QUICK, dry_run: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Compile libfastled library and stream the compilation output.

        Args:
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            dry_run: If True, performs a dry run without actual compilation

        Returns:
            AsyncGenerator[str, None]: Compilation output lines
        """
        async for line in self._client.compile_libfastled(build, dry_run):
            yield line

    @property
    def client(self):
        """Access to the underlying client implementation."""
        return self._client


class ClientSync:
    """
    Sync API interface for FastLED WASM server operations.

    This class provides a sync client interface for all FastLED WASM server operations.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = _DEFAULT_TIMEOUT,
    ):
        """
        Initialize the FastLED WASM API.

        Args:
            base_url: Base URL of the FastLED WASM server
            timeout: Request timeout in seconds
        """
        from .client_sync import ClientSyncImpl

        # Use sync client implementation
        self._client = ClientSyncImpl(
            base_url=base_url,
            timeout=timeout,
        )

    @property
    def base_url(self) -> str:
        """Get the base URL from the implementation."""
        return self._client.base_url

    @property
    def timeout(self) -> float:
        """Get the timeout from the implementation."""
        return self._client.timeout

    # Context manager support for sync client
    def __enter__(self):
        """Sync context manager entry."""
        return self._client.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        self._client.__exit__(exc_type, exc_val, exc_tb)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def health_check(self) -> HealthResponse:
        """
        Perform a health check on the server.

        Returns:
            HealthResponse: Server health status
        """
        return self._client.health_check()

    def get_settings(self) -> ServerSettings:
        """
        Get server settings.

        Returns:
            ServerSettings: Current server settings
        """
        return self._client.get_settings()

    def get_info(self) -> ServerInfo:
        """
        Get server information including available examples and statistics.

        Returns:
            ServerInfo: Server information and statistics
        """
        return self._client.get_info()

    def is_compiler_in_use(self) -> CompilerInUseResponse:
        """
        Check if the compiler is currently in use.

        Returns:
            CompilerInUseResponse: Compiler usage status
        """
        return self._client.is_compiler_in_use()

    def shutdown_server(self) -> dict[str, str]:
        """
        Shutdown the server (if allowed by server configuration).

        Returns:
            Dict[str, str]: Shutdown status
        """
        return self._client.shutdown_server()

    def init_project(self, example: str | None = None) -> bytes:
        """
        Initialize a new project with default or specified example.

        Args:
            example: Optional example name. If None, uses default example.

        Returns:
            bytes: ZIP file content of the initialized project
        """
        return self._client.init_project(example)

    def get_dwarf_source(self, path: str) -> str:
        """
        Get source file content for debugging.

        Args:
            path: Path to the source file

        Returns:
            str: Source file content
        """
        return self._client.get_dwarf_source(path)

    def start_session(self) -> SessionResponse:
        """
        Start a new session and get session ID.

        Returns:
            SessionResponse: Session ID and info
        """
        return self._client.start_session()

    def compile_wasm(
        self,
        file_path: str | Path,
        build: BuildMode = BuildMode.QUICK,
        profile: str | None = None,
        strict: bool = False,
        no_platformio: bool | None = None,
        native: bool | None = None,
        session_id: int | None = None,
        allow_libcompile: bool = True,
    ) -> bytes:
        """
        Compile a WASM file.

        Args:
            file_path: Path to the file to compile
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            profile: Profile setting
            strict: Enable strict compilation
            no_platformio: Disable PlatformIO usage
            native: Enable native compilation
            session_id: Session ID for tracking
            allow_libcompile: Allow library compilation

        Returns:
            bytes: Compiled WASM file content
        """
        return self._client.compile_wasm(
            file_path,
            build,
            profile,
            strict,
            no_platformio,
            native,
            session_id,
            allow_libcompile=allow_libcompile,
        )

    def compile_wasm_with_file_content(
        self,
        file_content: bytes,
        filename: str,
        build: BuildMode = BuildMode.QUICK,
        profile: str | None = None,
        strict: bool = False,
        no_platformio: bool | None = None,
        native: bool | None = None,
        session_id: int | None = None,
    ) -> bytes:
        """
        Compile WASM from file content (without saving to disk).

        Args:
            file_content: Content of the file to compile
            filename: Name of the file (for server reference)
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            profile: Profile setting
            strict: Enable strict compilation
            no_platformio: Disable PlatformIO usage
            native: Enable native compilation
            session_id: Session ID for tracking

        Returns:
            bytes: Compiled WASM file content
        """
        return self._client.compile_wasm_with_file_content(
            file_content,
            filename,
            build,
            profile,
            strict,
            no_platformio,
            native,
            session_id,
        )

    def compile_libfastled(
        self, build: BuildMode = BuildMode.QUICK, dry_run: bool = False
    ) -> Generator[str, None, None]:
        """
        Compile libfastled library and stream the compilation output.

        Args:
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            dry_run: If True, performs a dry run without actual compilation

        Returns:
            Generator[str, None, None]: Compilation output lines
        """
        return self._client.compile_libfastled(build, dry_run)

    @property
    def client(self):
        """Access to the underlying client implementation."""
        return self._client


__all__ = [
    "ClientAsync",
    "ClientSync",
    "BuildMode",
    "ServerSettings",
    "ServerInfo",
    "CompilerInUseResponse",
    "HealthResponse",
    "DwarfSourceRequest",
    "SessionResponse",
]
