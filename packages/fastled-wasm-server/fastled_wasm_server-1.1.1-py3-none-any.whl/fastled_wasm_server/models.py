"""
FastLED WASM Server API Client

This module provides both synchronous and asynchronous HTTP clients for interacting
with the FastLED WASM server. The clients handle all available endpoints with proper
typing and error handling.
"""

from pydantic import BaseModel


class DwarfSourceRequest(BaseModel):
    """Request model for dwarf source file retrieval."""

    path: str


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str


class ServerSettings(BaseModel):
    """Server settings response model."""

    volume_mapped_src: str
    volume_mapped_src_exists: bool
    output_dir: str
    only_quick_builds: bool
    allow_code_sync: bool
    allow_shutdown: bool
    no_sketch_cache: bool
    memory_limit_mb: int
    live_git_updates_enabled: bool
    live_git_updates_interval: int
    upload_limit: int
    sketch_cache_max_entries: int
    uptime: float


class ServerInfo(BaseModel):
    """Server information response model."""

    examples: list[str]
    stats: dict
    settings: ServerSettings


class CompilerInUseResponse(BaseModel):
    """Compiler in use response model."""

    in_use: bool


class SessionResponse(BaseModel):
    """Session start response model."""

    session_id: int
    session_info: str
