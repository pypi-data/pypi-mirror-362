"""
Tag management commands for TestZeus CLI.
"""

import asyncio
import click
from rich.console import Console
from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output, print_message
from testzeus_cli.utils.auth import initialize_client_with_token
from testzeus_cli.utils.validators import parse_key_value_pairs, validate_id

console = Console()


@click.group()
def tags_group():
    """Manage tags in TestZeus"""
    pass


@tags_group.command()
@click.option("--name", required=True, help="Tag name")
@click.option("--value", required=False, default=None, help="Tag value")
@click.pass_context
def create(ctx, name, value):
    """Create a new tag"""

    async def _run():
        config, token, stored_tenant_id, stored_user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            params = {
                "name": name,
                "value": value,
                "tenant": stored_tenant_id,
                "modified_by": stored_user_id,
            }
            tag = await client.tags.create(params)
            return tag.data

    try:
        result = asyncio.run(_run())
        print_message(f"[green]Tag '{result['name']}' created successfully[/green]", ctx.obj["FORMAT"])
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error creating tag: {str(e)}[/red]", ctx.obj["FORMAT"])
        raise click.Abort()


@tags_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list(ctx, filters, sort, expand):
    """List all tags"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        # Parse filters
        filter_dict = parse_key_value_pairs(filters) if filters else {}

        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            result = await client.tags.get_list(
                expand=expand, sort=sort, filters=filter_dict
            )

            return result

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error listing tags: {str(e)}[/red]", ctx.obj["FORMAT"])
        raise click.Abort()


@tags_group.command(name="get")
@click.argument("tag_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_tags(ctx, tag_id, expand):
    """Get a tag by id"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        tag_id_validated = validate_id(tag_id, "tag")
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            tag = await client.tags.get_one(tag_id_validated, expand=expand)
            return tag.data

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error getting tag: {str(e)}[/red]", ctx.obj["FORMAT"])
        raise click.Abort()


@tags_group.command(name="update")
@click.argument("tags_id")
@click.option("--name", help="New tag name")
@click.option("--value", help="New tag value")
@click.pass_context
def update_tags(ctx, tags_id, name, value):
    """Update a tag"""

    async def _run():
        config, token, tenanat_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        tag_id_validated = validate_id(tags_id, "tag")
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            updates = {"tenant": tenanat_id, "modified_by": user_id}
            has_updates = False

            if name:
                updates["name"] = name
                has_updates = True

            if value:
                updates["value"] = value
                has_updates = True

            if has_updates:
                update_tags = await client.tags.update(tag_id_validated, updates)
                return update_tags.data
            else:
                print_message("[yellow]No updates provided[/yellow]", ctx.obj["FORMAT"])
                return None

    try:
        result = asyncio.run(_run())
        print_message(f"[green]Tag '{result['name']}' updated successfully[/green]", ctx.obj["FORMAT"])
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error updating tag: {str(e)}[/red]", ctx.obj["FORMAT"])
        raise click.Abort()


@tags_group.command(name="delete")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this tag?")
@click.pass_context
def delete(ctx, name):
    """Delete a tag"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            await client.tags.delete(name)
            return {"name": name}

    try:
        result = asyncio.run(_run())
        print_message(f"[green]Tag '{result['name']}' deleted successfully[/green]", ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error deleting tag: {str(e)}[/red]", ctx.obj["FORMAT"])
        raise click.Abort()
