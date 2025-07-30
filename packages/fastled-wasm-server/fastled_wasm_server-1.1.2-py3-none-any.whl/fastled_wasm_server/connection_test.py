"""
Connection testing utilities for FastLED WASM Server.

This module provides utilities to test HTTP connections and determine
the best transport configuration (IPv4 vs IPv6) for optimal connectivity.
"""

import asyncio
from dataclasses import dataclass

import httpx


@dataclass
class ConnectionResult:
    """Result of connection testing."""

    host: str
    ipv4: bool
    success: bool = True


async def _test_connection(url: str, use_ipv4: bool = True) -> ConnectionResult:
    """
    Test a single connection to determine if it works.

    Args:
        url: URL to test
        use_ipv4: Whether to force IPv4 or IPv6

    Returns:
        ConnectionResult with connection details
    """
    try:
        # Configure transport based on IP version
        transport = None
        if use_ipv4:
            transport = httpx.AsyncHTTPTransport(local_address="0.0.0.0")

        async with httpx.AsyncClient(transport=transport, timeout=5.0) as client:
            # Quick test connection
            response = await client.get(f"{url}/healthz", timeout=2.0)
            response.raise_for_status()
            return ConnectionResult(host=url, ipv4=use_ipv4, success=True)

    except Exception:
        return ConnectionResult(host=url, ipv4=use_ipv4, success=False)


async def find_good_connection(
    urls: list[str], filter_out_bad: bool = True, use_ipv6: bool = True
) -> ConnectionResult | None:
    """
    Test connections to find the best available endpoint and determine IP version.

    Args:
        urls: List of URLs to test
        filter_out_bad: Whether to filter out failed connections
        use_ipv6: Whether to test IPv6 connections

    Returns:
        ConnectionResult with host and IPv4 flag, or None if no connection works
    """
    # Check if any URL contains 0.0.0.0 - if so, force IPv4
    for url in urls:
        if "0.0.0.0" in url:
            return ConnectionResult(
                host=url, ipv4=True, success=False if filter_out_bad else True
            )

    # Create tasks for concurrent connection testing
    tasks = []
    for url in urls:
        # Always test IPv4
        task = asyncio.create_task(_test_connection(url, use_ipv4=True))
        tasks.append(task)

        # Test IPv6 if enabled and not localhost
        if use_ipv6 and "localhost" not in url:
            task_v6 = asyncio.create_task(_test_connection(url, use_ipv4=False))
            tasks.append(task_v6)

    try:
        # Return first successful result
        for coro in asyncio.as_completed(tasks):
            result: ConnectionResult = await coro
            if result.success or not filter_out_bad:
                # Cancel remaining tasks
                for task in tasks:
                    if not task.done():
                        task.cancel()
                return result
    except Exception:
        pass
    finally:
        # Ensure all tasks are cancelled
        for task in tasks:
            if not task.done():
                task.cancel()

        # Wait for all tasks to complete cancellation
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    return None
