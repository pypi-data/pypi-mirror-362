"""
Client utility functions for TestZeus CLI.
"""

import asyncio
from typing import Any, Optional, Callable, TypeVar, Awaitable, Dict

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.auth import initialize_client_with_token

T = TypeVar("T")


async def with_authenticated_client(
    profile: str,
    api_url: Optional[str],
    operation: Callable[[TestZeusClient], Awaitable[T]],
) -> T:
    """
    Execute an operation with an authenticated client

    Args:
        profile: Configuration profile to use
        api_url: Optional API URL to override profile setting
        operation: Async function that takes a TestZeusClient and returns a value

    Returns:
        The result of the operation
    """
    config, token, _, _ = get_client_config(profile, api_url)
    client = TestZeusClient(**config)

    async with client:
        # Apply token from config if available
        if token:
            initialize_client_with_token(client, token)
        else:
            await client.ensure_authenticated()

        return await operation(client)


def run_client_operation(
    ctx: Dict[str, Any], operation: Callable[[TestZeusClient], Awaitable[T]]
) -> T:
    """
    Run an operation with a client using the context configuration

    Args:
        ctx: Click context object with configuration
        operation: Async function that takes a TestZeusClient and returns a value

    Returns:
        The result of the operation
    """
    profile = ctx.obj["PROFILE"]
    api_url = ctx.obj.get("API_URL")

    return asyncio.run(with_authenticated_client(profile, api_url, operation))
