"""FastLED WASM Server package."""

from pathlib import Path
from typing import AsyncGenerator, Dict, Optional, Union

from .api_client import (
    ClientAsync,
    CompilerInUseResponse,
    DwarfSourceRequest,
    HealthResponse,
    ServerInfo,
    ServerSettings,
)


class FastLEDWasmAPI:
    """
    Async API interface for FastLED WASM server operations.

    This class provides an async client interface for all FastLED WASM server operations.
    """

    def __init__(
        self,
        base_url: str,
        auth_token: Optional[str] = None,
        timeout: float = 30.0,
        **httpx_kwargs,
    ):
        """
        Initialize the FastLED WASM API.

        Args:
            base_url: Base URL of the FastLED WASM server
            auth_token: Optional authorization token for protected endpoints
            timeout: Request timeout in seconds
            **httpx_kwargs: Additional arguments passed to httpx.AsyncClient
        """
        self.base_url = base_url
        self.auth_token = auth_token
        self.timeout = timeout
        self.httpx_kwargs = httpx_kwargs

        # Use async client implementation
        self._client = ClientAsync(
            base_url=base_url,
            auth_token=auth_token,
            timeout=timeout,
            **httpx_kwargs,
        )

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

    async def shutdown_server(self) -> Dict[str, str]:
        """
        Shutdown the server (if allowed by server configuration).

        Returns:
            Dict[str, str]: Shutdown status
        """
        return await self._client.shutdown_server()

    async def init_project(self, example: Optional[str] = None) -> bytes:
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

    async def compile_wasm(
        self,
        file_path: Union[str, Path],
        build: Optional[str] = None,
        profile: Optional[str] = None,
        strict: bool = False,
        no_platformio: Optional[bool] = None,
        native: Optional[bool] = None,
        session_id: Optional[int] = None,
        allow_libcompile: bool = True,
    ) -> bytes:
        """
        Compile a WASM file.

        Args:
            file_path: Path to the file to compile
            build: Build type (quick, debug, release)
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
        build: Optional[str] = None,
        profile: Optional[str] = None,
        strict: bool = False,
        no_platformio: Optional[bool] = None,
        native: Optional[bool] = None,
        session_id: Optional[int] = None,
    ) -> bytes:
        """
        Compile WASM from file content (without saving to disk).

        Args:
            file_content: Content of the file to compile
            filename: Name of the file (for server reference)
            build: Build type (quick, debug, release)
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
        self, build: Optional[str] = None, dry_run: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Compile libfastled library and stream the compilation output.

        Args:
            build: Build type (quick, debug, release)
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


__all__ = [
    "FastLEDWasmAPI",
    "ClientAsync",
    "ServerSettings",
    "ServerInfo",
    "CompilerInUseResponse",
    "HealthResponse",
    "DwarfSourceRequest",
]
