"""
FastLED WASM Server API Client

This module provides both synchronous and asynchronous HTTP clients for interacting
with the FastLED WASM server. The clients handle all available endpoints with proper
typing and error handling.
"""

from collections.abc import AsyncGenerator
from pathlib import Path
from urllib.parse import urlparse

import httpx

from fastled_wasm_server.connection_test import find_good_connection
from fastled_wasm_server.models import (
    CompilerInUseResponse,
    DwarfSourceRequest,
    HealthResponse,
    ServerInfo,
    ServerSettings,
    SessionResponse,
)
from fastled_wasm_server.types import BuildMode


class ClientAsyncImpl:
    """
    Asynchronous HTTP client for FastLED WASM server.

    This client provides async methods for all available server endpoints including:
    - Health checks and server info
    - Project initialization
    - WASM compilation
    - Library compilation
    - Debugging support
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
    ):
        """
        Initialize the FastLED WASM async client.

        Args:
            base_url: Base URL of the FastLED WASM server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None
        self._client_initialized = False

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _ensure_client_initialized(self) -> httpx.AsyncClient:
        """Ensure the HTTP client is initialized with connection testing."""
        if not self._client_initialized:
            # Test connection and determine if IPv4 transport is needed
            urls = [self.base_url]
            parsed = urlparse(self.base_url)
            domain = parsed.netloc

            # Add port variant if no port specified
            if ":" not in domain:
                # Extract scheme and add default port
                scheme = parsed.scheme or "http"
                default_port = 80 if scheme == "http" else 443
                urls.append(f"{scheme}://{domain}:{default_port}")

            connection_result = await find_good_connection(urls, filter_out_bad=False)

            # Configure transport based on connection test
            transport = None
            if connection_result and connection_result.ipv4:
                transport = httpx.AsyncHTTPTransport(local_address="0.0.0.0")

            # Create client with appropriate transport
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                transport=transport,
            )
            self._client_initialized = True

        assert self._client is not None, "Client should be initialized"
        return self._client

    async def close(self):
        """Close the HTTP client."""
        if self._client is not None:
            await self._client.aclose()

    async def health_check(self) -> HealthResponse:
        """
        Perform a health check on the server.

        Returns:
            HealthResponse: Server health status
        """
        client = await self._ensure_client_initialized()
        response = await client.get("/healthz")
        response.raise_for_status()
        return HealthResponse(**response.json())

    async def get_settings(self) -> ServerSettings:
        """
        Get server settings.

        Returns:
            ServerSettings: Current server settings
        """
        client = await self._ensure_client_initialized()
        response = await client.get("/settings")
        response.raise_for_status()
        return ServerSettings(**response.json())

    async def get_info(self) -> ServerInfo:
        """
        Get server information including available examples and statistics.

        Returns:
            ServerInfo: Server information and statistics
        """
        client = await self._ensure_client_initialized()
        response = await client.get("/info")
        response.raise_for_status()
        return ServerInfo(**response.json())

    async def is_compiler_in_use(self) -> CompilerInUseResponse:
        """
        Check if the compiler is currently in use.

        Returns:
            CompilerInUseResponse: Compiler usage status
        """
        client = await self._ensure_client_initialized()
        response = await client.get("/compile/wasm/inuse")
        response.raise_for_status()
        return CompilerInUseResponse(**response.json())

    async def shutdown_server(self) -> dict[str, str]:
        """
        Shutdown the server (if allowed by server configuration).

        Returns:
            Dict[str, str]: Shutdown status

        Raises:
            httpx.HTTPStatusError: If shutdown is not allowed or fails
        """
        client = await self._ensure_client_initialized()
        response = await client.get("/shutdown")
        response.raise_for_status()
        return response.json()

    async def init_project(self, example: str | None = None) -> bytes:
        """
        Initialize a new project with default or specified example.

        Args:
            example: Optional example name. If None, uses default example.

        Returns:
            bytes: ZIP file content of the initialized project
        """
        client = await self._ensure_client_initialized()
        if example is None:
            response = await client.get("/project/init")
        else:
            response = await client.post("/project/init", content=example)

        response.raise_for_status()
        return response.content

    async def get_dwarf_source(self, path: str, session_id: int | None = None) -> str:
        """
        Get source file content for debugging.

        Args:
            path: Path to the source file
            session_id: Optional session ID for authentication

        Returns:
            str: Source file content
        """
        await self._ensure_client_initialized()
        request_data = DwarfSourceRequest(path=path)
        headers = {}
        if session_id is not None:
            headers["session_id"] = str(session_id)

        client = await self._ensure_client_initialized()
        response = await client.post(
            "/dwarfsource",
            headers=headers,
            json=request_data.model_dump(),
        )
        response.raise_for_status()
        return response.text

    async def start_session(self) -> SessionResponse:
        """
        Start a new session and get session ID.

        Returns:
            SessionResponse: Session ID and info
        """
        client = await self._ensure_client_initialized()
        response = await client.post("/session/start")
        response.raise_for_status()
        return SessionResponse(**response.json())

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
            session_id: Session ID for tracking (auto-generated if None)
            allow_libcompile: Allow library compilation

        Returns:
            bytes: Compiled WASM file content
        """
        # Auto-generate session ID if not provided
        if session_id is None:
            session_response = await self.start_session()
            session_id = session_response.session_id

        # Prepare headers
        headers = {}

        # Build parameter is always provided now
        headers["build"] = build.value
        if profile is not None:
            headers["profile"] = profile
        if strict:
            headers["strict"] = "true"
        if no_platformio is not None:
            headers["no_platformio"] = "true" if no_platformio else "false"
        if native is not None:
            headers["native"] = "true" if native else "false"
        if session_id is not None:
            headers["session_id"] = str(session_id)
        if allow_libcompile:
            headers["allow_libcompile"] = "true"
        else:
            headers["allow_libcompile"] = "false"

        # Ensure client is initialized before making requests
        client = await self._ensure_client_initialized()

        # Prepare file upload
        file_path = Path(file_path)

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}

            response = await client.post("/compile/wasm", headers=headers, files=files)

        response.raise_for_status()
        return response.content

    async def compile_libfastled(
        self, build: BuildMode = BuildMode.QUICK, dry_run: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Compile libfastled library and stream the compilation output.

        Args:
            build: Build type (BuildMode enum: QUICK, DEBUG, RELEASE)
            dry_run: If True, performs a dry run without actual compilation

        Yields:
            str: Compilation output lines
        """
        headers = {}

        # Build parameter is always provided now
        headers["build"] = build.value
        if dry_run:
            headers["dry_run"] = "true"

        # Ensure client is initialized before making requests
        client = await self._ensure_client_initialized()

        async with client.stream(
            "POST", "/compile/libfastled", headers=headers
        ) as response:
            response.raise_for_status()

            async for chunk in response.aiter_text():
                if chunk:
                    yield chunk

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
        allow_libcompile: bool = True,
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
            session_id: Session ID for tracking (auto-generated if None)

        Returns:
            bytes: Compiled WASM file content
        """
        # Auto-generate session ID if not provided
        if session_id is None:
            session_response = await self.start_session()
            session_id = session_response.session_id

        # Prepare headers
        headers = {}

        # Build parameter is always provided now
        headers["build"] = build.value
        if profile is not None:
            headers["profile"] = profile
        if strict:
            headers["strict"] = "true"
        if no_platformio is not None:
            headers["no_platformio"] = "true" if no_platformio else "false"
        if native is not None:
            headers["native"] = "true" if native else "false"
        if session_id is not None:
            headers["session_id"] = str(session_id)
        if allow_libcompile:
            headers["allow_libcompile"] = "true"
        else:
            headers["allow_libcompile"] = "false"

        # Ensure client is initialized before making requests
        client = await self._ensure_client_initialized()

        # Prepare file upload
        files = {"file": (filename, file_content, "application/octet-stream")}

        response = await client.post("/compile/wasm", headers=headers, files=files)

        response.raise_for_status()
        return response.content
