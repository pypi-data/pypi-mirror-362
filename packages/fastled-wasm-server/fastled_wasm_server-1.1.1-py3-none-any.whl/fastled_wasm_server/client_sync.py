"""
FastLED WASM Server API Client

This module provides both synchronous and asynchronous HTTP clients for interacting
with the FastLED WASM server. The clients handle all available endpoints with proper
typing and error handling.
"""

import asyncio
from collections.abc import Generator
from pathlib import Path

from fastled_wasm_server.models import (
    CompilerInUseResponse,
    HealthResponse,
    ServerInfo,
    ServerSettings,
    SessionResponse,
)
from fastled_wasm_server.types import BuildMode


class ClientSyncImpl:
    """
    Synchronous HTTP client for FastLED WASM server.

    This client provides synchronous methods for all available server endpoints including:
    - Health checks and server info
    - Project initialization
    - WASM compilation
    - Library compilation
    - Debugging support

    This implementation delegates to ClientAsyncImpl and uses asyncio.run to provide
    a synchronous interface.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        """
        Initialize the FastLED WASM client.

        Args:
            base_url: Base URL of the FastLED WASM server
            timeout: Request timeout in seconds
        """
        from fastled_wasm_server.client_async import ClientAsyncImpl

        self._async_client = ClientAsyncImpl(base_url=base_url, timeout=timeout)

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._async_client.base_url

    @property
    def timeout(self) -> float:
        """Get the timeout."""
        return self._async_client.timeout

    @property
    def _client(self):
        """Get the underlying HTTP client for backward compatibility."""
        return self._async_client._client

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        asyncio.run(self._async_client.close())

    def health_check(self) -> HealthResponse:
        """
        Perform a health check on the server.

        Returns:
            HealthResponse: Server health status
        """
        return asyncio.run(self._async_client.health_check())

    def get_settings(self) -> ServerSettings:
        """
        Get server settings.

        Returns:
            ServerSettings: Current server settings
        """
        return asyncio.run(self._async_client.get_settings())

    def get_info(self) -> ServerInfo:
        """
        Get server information including available examples and statistics.

        Returns:
            ServerInfo: Server information and statistics
        """
        return asyncio.run(self._async_client.get_info())

    def is_compiler_in_use(self) -> CompilerInUseResponse:
        """
        Check if the compiler is currently in use.

        Returns:
            CompilerInUseResponse: Compiler usage status
        """
        return asyncio.run(self._async_client.is_compiler_in_use())

    def shutdown_server(self) -> dict[str, str]:
        """
        Shutdown the server (if allowed by server configuration).

        Returns:
            Dict[str, str]: Shutdown status

        Raises:
            httpx.HTTPStatusError: If shutdown is not allowed or fails
        """
        return asyncio.run(self._async_client.shutdown_server())

    def init_project(self, example: str | None = None) -> bytes:
        """
        Initialize a new project with default or specified example.

        Args:
            example: Optional example name. If None, uses default example.

        Returns:
            bytes: ZIP file content of the initialized project
        """
        return asyncio.run(self._async_client.init_project(example))

    def get_dwarf_source(self, path: str) -> str:
        """
        Get source file content for debugging.

        Args:
            path: Path to the source file

        Returns:
            str: Source file content
        """
        return asyncio.run(self._async_client.get_dwarf_source(path))

    def start_session(self) -> SessionResponse:
        """
        Start a new session and get session ID.

        Returns:
            SessionResponse: Session ID and info
        """
        return asyncio.run(self._async_client.start_session())

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

        Returns:
            bytes: Compiled WASM file content
        """
        return asyncio.run(
            self._async_client.compile_wasm(
                file_path=file_path,
                build=build,
                profile=profile,
                strict=strict,
                no_platformio=no_platformio,
                native=native,
                session_id=session_id,
                allow_libcompile=allow_libcompile,
            )
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
        return asyncio.run(
            self._async_client.compile_wasm_with_file_content(
                file_content=file_content,
                filename=filename,
                build=build,
                profile=profile,
                strict=strict,
                no_platformio=no_platformio,
                native=native,
                session_id=session_id,
            )
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

        async def _collect_chunks():
            chunks = []
            async for chunk in self._async_client.compile_libfastled(build, dry_run):
                chunks.append(chunk)
            return chunks

        # Since we can't directly run an async generator with asyncio.run,
        # we collect all chunks and then yield them synchronously
        chunks = asyncio.run(_collect_chunks())
        yield from chunks
