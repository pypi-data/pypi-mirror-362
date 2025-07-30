"""Web compile."""

import asyncio
import hashlib
import io
import json
import os
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from fastled_wasm_server.connection_test import find_good_connection
from fastled_wasm_server.print_filter import PrintFilterDefault
from fastled_wasm_server.types import BuildMode
from fastled_wasm_server.zip_files import zip_files

DEFAULT_HOST = "https://fastled.onrender.com"
ENDPOINT_COMPILED_WASM = "compile/wasm"
_TIMEOUT = 60 * 4  # 2 mins timeout
_AUTH_TOKEN = "oBOT5jbsO4ztgrpNsQwlmFLIKB"
ENABLE_EMBEDDED_DATA = True
SERVER_PORT = 9021


def _find_good_connection_sync(urls: list[str]) -> Any | None:
    """Synchronous wrapper for the async find_good_connection function."""
    try:
        return asyncio.run(find_good_connection(urls))
    except Exception:
        return None


def _sanitize_host(host: str) -> str:
    if host.startswith("http"):
        return host
    is_local_host = "localhost" in host or "127.0.0.1" in host or "0.0.0.0" in host
    use_https = not is_local_host
    if use_https:
        return host if host.startswith("https://") else f"https://{host}"
    return host if host.startswith("http://") else f"http://{host}"


@dataclass
class CompileResult:
    success: bool
    stdout: str
    hash_value: str | None
    zip_bytes: bytes

    def __bool__(self) -> bool:
        return self.success

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()

    def __post_init__(self):
        # Filter the stdout.
        pf = PrintFilterDefault(echo=False)
        self.stdout = pf.print(self.stdout)


def _banner(msg: str) -> str:
    """
    Create a banner for the given message.
    Example:
    msg = "Hello, World!"
    print -> "#################"
             "# Hello, World! #"
             "#################"
    """
    lines = msg.split("\n")
    # Find the width of the widest line
    max_width = max(len(line) for line in lines)
    width = max_width + 4  # Add 4 for "# " and " #"

    # Create the top border
    banner = "\n" + "#" * width + "\n"

    # Add each line with proper padding
    for line in lines:
        padding = max_width - len(line)
        banner += f"# {line}{' ' * padding} #\n"

    # Add the bottom border
    banner += "#" * width + "\n"
    return f"\n{banner}\n"


def _print_banner(msg: str) -> None:
    print(_banner(msg))


def web_compile(
    directory: Path | str,
    host: str | None = None,
    auth_token: str | None = None,
    build_mode: BuildMode | None = None,
    profile: bool = False,
    no_platformio: bool = False,
) -> CompileResult:
    start_time = time.time()
    if isinstance(directory, str):
        directory = Path(directory)
    host = _sanitize_host(host or DEFAULT_HOST)
    build_mode = build_mode or BuildMode.QUICK
    _print_banner(f"Compiling on {host}")
    auth_token = auth_token or _AUTH_TOKEN
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    zip_result = zip_files(directory, build_mode=build_mode)
    if isinstance(zip_result, Exception):
        return CompileResult(
            success=False, stdout=str(zip_result), hash_value=None, zip_bytes=b""
        )
    zip_bytes = zip_result.zip_bytes
    archive_size = len(zip_bytes)
    print(f"Web compiling on {host}...")
    try:
        host = _sanitize_host(host)
        urls = [host]
        domain = host.split("://")[-1]
        if ":" not in domain:
            urls.append(f"{host}:{SERVER_PORT}")

        connection_result = _find_good_connection_sync(urls)
        if connection_result is None:
            _print_banner("Connection failed to all endpoints")
            return CompileResult(
                success=False,
                stdout="Connection failed",
                hash_value=None,
                zip_bytes=b"",
            )

        ipv4_stmt = "IPv4" if connection_result.ipv4 else "IPv6"
        transport = (
            httpx.HTTPTransport(local_address="0.0.0.0")
            if connection_result.ipv4
            else None
        )
        with httpx.Client(
            transport=transport,
            timeout=_TIMEOUT,
        ) as client:
            headers = {
                "accept": "application/json",
                "authorization": auth_token,
                "build": (
                    build_mode.value.lower()
                    if build_mode
                    else BuildMode.QUICK.value.lower()
                ),
                "profile": "true" if profile else "false",
                "no-platformio": "true" if no_platformio else "false",
            }

            url = f"{connection_result.host}/{ENDPOINT_COMPILED_WASM}"
            print(f"Compiling on {url} via {ipv4_stmt}. Zip size: {archive_size} bytes")
            files = {"file": ("wasm.zip", zip_bytes, "application/x-zip-compressed")}
            response = client.post(
                url,
                follow_redirects=True,
                files=files,
                headers=headers,
                timeout=_TIMEOUT,
            )

            if response.status_code != 200:
                json_response = response.json()
                detail = json_response.get("detail", "Could not compile")
                return CompileResult(
                    success=False, stdout=detail, hash_value=None, zip_bytes=b""
                )

            print(f"Response status code: {response}")
            # Create a temporary directory to extract the zip
            with tempfile.TemporaryDirectory() as extract_dir:
                extract_path = Path(extract_dir)

                # Write the response content to a temporary zip file
                temp_zip = extract_path / "response.zip"
                temp_zip.write_bytes(response.content)

                # Extract the zip
                shutil.unpack_archive(temp_zip, extract_path, "zip")

                if zip_result.zip_embedded_bytes:
                    # extract the embedded bytes, which were not sent to the server
                    temp_zip.write_bytes(zip_result.zip_embedded_bytes)
                    shutil.unpack_archive(temp_zip, extract_path, "zip")

                # we don't need the temp zip anymore
                temp_zip.unlink()

                # Read stdout from out.txt if it exists
                stdout_file = extract_path / "out.txt"
                hash_file = extract_path / "hash.txt"
                stdout = (
                    stdout_file.read_text(encoding="utf-8", errors="replace")
                    if stdout_file.exists()
                    else ""
                )
                hash_value = (
                    hash_file.read_text(encoding="utf-8", errors="replace")
                    if hash_file.exists()
                    else None
                )

                # now rezip the extracted files since we added the embedded json files
                out_buffer = io.BytesIO()
                with zipfile.ZipFile(
                    out_buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9
                ) as out_zip:
                    for root, _, _files in os.walk(extract_path):
                        for file in _files:
                            file_path = Path(root) / file
                            relative_path = file_path.relative_to(extract_path)
                            out_zip.write(file_path, relative_path)

                diff_time = time.time() - start_time
                msg = f"Compilation success, took {diff_time:.2f} seconds"
                _print_banner(msg)
                return CompileResult(
                    success=True,
                    stdout=stdout,
                    hash_value=hash_value,
                    zip_bytes=out_buffer.getvalue(),
                )
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        raise
    except httpx.HTTPError as e:
        print(f"Error: {e}")
        return CompileResult(
            success=False, stdout=str(e), hash_value=None, zip_bytes=b""
        )


def hash_file(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _file_info(file_path: Path) -> str:
    hash_txt = hash_file(file_path)
    file_size = file_path.stat().st_size
    json_str = json.dumps({"hash": hash_txt, "size": file_size})
    return json_str
