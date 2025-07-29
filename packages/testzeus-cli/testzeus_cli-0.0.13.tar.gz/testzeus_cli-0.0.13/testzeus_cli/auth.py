"""
Authentication utilities for TestZeus CLI.
"""

import asyncio
import click
from getpass import getpass
from rich.console import Console
from typing import Dict, Any, Optional

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import update_config, get_client_config, clear_auth_data
from testzeus_cli.utils.auth import (
    initialize_client_with_token,
)

console = Console()


@click.command(name="login")
@click.option("--email", help="Your TestZeus email")
@click.option("--password", help="Your TestZeus password", hide_input=True)
@click.option("--save", is_flag=True, default=True, help="Save credentials to config")
@click.pass_context
def login_command(
    ctx: click.Context, email: Optional[str], password: Optional[str], save: bool
) -> None:
    """Log in to TestZeus"""
    if not email:
        email = click.prompt("Email")

    if not password:
        password = getpass("Password: ")

    async def _login() -> Dict[str, Any]:
        config, _, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )

        # Create a clean config without email/password to avoid duplicates
        base_config = {"base_url": config.get("base_url")}

        # Create client with explicit email/password
        client = TestZeusClient(email=email, password=password, **base_config)

        async with client:
            # Authenticate and get token
            await client.ensure_authenticated()
            token = client.token

            # Get tenant ID from the authenticated client
            tenant_id = client.get_tenant_id()
            user_id = client.get_user_id()

            if save:
                update_config(
                    ctx.obj["PROFILE"],
                    {
                        "api_url": client.base_url,
                        "email": email,
                        "token": token,
                        "tenant_id": tenant_id,
                        "user_id": user_id,
                    },
                )

            return {
                "email": email,
                "api_url": client.base_url,
                "authenticated": client.is_authenticated(),
                "tenant_id": tenant_id,
                "user_id": user_id,
            }

    try:
        result = asyncio.run(_login())
        console.print("[green]Successfully logged in![/green]")
        console.print(f"Email: {result['email']}")
        console.print(f"API URL: {result['api_url']}")
        console.print(f"Tenant ID: {result['tenant_id']}")
    except Exception as e:
        console.print(f"[red]Login failed:[/red] {str(e)}")
        exit(1)


@click.command(name="logout")
@click.pass_context
def logout_command(ctx: click.Context) -> None:
    """Log out from TestZeus"""
    profile = ctx.obj["PROFILE"]
    clear_auth_data(profile)
    console.print(f"[green]Successfully logged out from profile '{profile}'[/green]")


@click.command(name="whoami")
@click.pass_context
def whoami_command(ctx: click.Context) -> None:
    """Show current user information"""

    async def _whoami() -> Dict[str, Any]:
        config, token, stored_tenant_id, stored_user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )

        client = TestZeusClient(**config)

        try:
            async with client:
                # Apply token from config if available
                if token:
                    initialize_client_with_token(client, token)
                else:
                    await client.ensure_authenticated()
                return {
                    "email": client.email,
                    "api_url": client.base_url,
                    "tenant_id": stored_tenant_id,
                    "user_id": stored_user_id,
                }
        except Exception as e:
            console.print(f"[red]Not authenticated:[/red] {str(e)}")
            console.print("[yellow]Run 'testzeus login' to authenticate[/yellow]")
            exit(1)

    try:
        user_info = asyncio.run(_whoami())
        console.print("[green]Current User Information:[/green]")
        console.print(f"Email: {user_info['email']}")
        console.print(f"API URL: {user_info['api_url']}")
        console.print(f"Tenant ID: {user_info['tenant_id']}")
        console.print(f"User ID: {user_info['user_id']}")
    except Exception as e:
        console.print(f"[red]Failed to get user information:[/red] {str(e)}")
        exit(1)
