"""
Commands for managing test data in TestZeus CLI.
"""

import asyncio
import click
from rich.console import Console
from pathlib import Path

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output, print_message
from testzeus_cli.utils.validators import validate_id, parse_key_value_pairs
from testzeus_cli.utils.auth import initialize_client_with_token
from pocketbase.client import FileUpload

console = Console()


def _read_data_file(file_path: str) -> str:
    """
    Read data content from a file as plain text
    Args:
        file_path: Path to the data file
    Returns:
        The raw text content of the file
    """
    data_path = Path(file_path)
    if not data_path.exists():
        raise click.BadParameter(f"Data file not found: {file_path}")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        raise click.BadParameter(f"Failed to read data file: {str(e)}")

    # Always return the raw text content
    return content


@click.group(name="test-data")
def test_data_group():
    """Manage TestZeus test data"""
    pass


@test_data_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list_test_data(ctx, filters, sort, expand):
    """List test data with optional filters and sorting"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Parse filters
        filter_dict = parse_key_value_pairs(filters) if filters else {}

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            test_data = await client.test_data.get_list(
                expand=expand, sort=sort, filters=filter_dict
            )
            return test_data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="get")
@click.argument("test_data_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_test_data(ctx, test_data_id, expand):
    """Get a single test data by ID"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            test_data = await client.test_data.get_one(
                test_data_id_validated, expand=expand
            )
            return test_data.data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="create")
@click.option("--name", required=True, help="Test data name")
@click.option("--type", default="test", help="Test data type")
@click.option(
    "--status", default="draft", help="Test data status (draft, ready, deleted)"
)
@click.option("--data", "-d", help="Test data content as text")
@click.option(
    "--data-file",
    "-df",
    type=click.Path(exists=True),
    help="Path to text file with test data",
)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Path to text file with test data",
)
@click.pass_context
def create_test_data(ctx, name, type, status, data, data_file, file):
    """Create new test data"""

    if not data and not data_file:
        raise click.UsageError("Either --data or --data-file is required")

    if data and data_file:
        raise click.UsageError("Cannot use both --data and --data-file")

    # Process the data content (from file or directly)
    data_content = _read_data_file(data_file) if data_file else data

    async def _run():
        config, token, tenant_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Prepare test data
        test_data = {
            "name": name,
            "type": type,
            "status": status,
            "data": data_content,
            "tenant": tenant_id,
            "modified_by": user_id,
            "metadata": {},
        }

        # Add data content if provided directly
        if data:
            test_data["data"] = data

        # Read from file if provided
        if file:
            try:
                test_data["supporting_data_files"] = FileUpload(file, open(file, "rb"))
            except Exception as e:
                print_message(f"[red]Error reading file:[/red] {str(e)}", ctx.obj["FORMAT"])
                exit(1)

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            new_test_data = await client.test_data.create(test_data)
            return new_test_data.data

    result = asyncio.run(_run())
    print_message(
        f"[green]Test data created successfully with ID: {result['id']}[/green]", ctx.obj["FORMAT"]
    )
    format_output(result, ctx.obj["FORMAT"])


@test_data_group.command(name="update")
@click.argument("test_data_id")
@click.option("--name", help="New test data name")
@click.option("--type", help="New test data type")
@click.option("--status", help="New test data status (draft, ready, deleted)")
@click.option("--data", "-d", help="New test data content as text")
@click.option(
    "--data-file",
    "-df",
    type=click.Path(exists=True),
    help="Path to text file with new test data",
)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True),
    help="Path to text file with new test data",
)
@click.pass_context
def update_test_data(ctx, test_data_id, name, type, status, data, data_file, file):
    """Update an existing test data"""

    if data and data_file:
        raise click.UsageError("Cannot use both --data and --data-file")

    # Process the data content (from file or directly)
    data_content = None
    if data_file:
        data_content = _read_data_file(data_file)
    elif data:
        data_content = data

    async def _run():
        config, token, tenant_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            # Prepare updates starting with all existing data
            updates = {"tenant": tenant_id, "modified_by": user_id}
            has_updates = False

            # Update only the fields that were provided
            if name:
                updates["name"] = name
                has_updates = True

            if type:
                updates["type"] = type
                has_updates = True

            if status:
                updates["status"] = status
                has_updates = True

            # Process input data (either from input or file)
            if data_content:
                updates["data"] = data_content
                has_updates = True

            if file:
                try:
                    updates["supporting_data_files+"] = FileUpload(
                        file, open(file, "rb")
                    )
                    has_updates = True
                except Exception as e:
                    print_message(f"[red]Error reading file:[/red] {str(e)}", ctx.obj["FORMAT"])
                    exit(1)

            if has_updates:
                updated_data = await client.test_data.update(
                    test_data_id_validated, updates
                )
                return updated_data.data
            else:
                print_message("[yellow]No updates provided[/yellow]", ctx.obj["FORMAT"])
                return None

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error updating test data:[/red] {str(e)}", ctx.obj["FORMAT"])
        raise click.Abort()


@test_data_group.command(name="delete")
@click.argument("test_data_id")
@click.confirmation_option(prompt="Are you sure you want to delete this test data?")
@click.pass_context
def delete_test_data(ctx, test_data_id):
    """Delete test data"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)

            # Optionally get the test data before deletion for confirmation
            test_data = await client.test_data.get_one(test_data_id_validated)
            await client.test_data.delete(test_data_id_validated)
            return test_data.data

    try:
        result = asyncio.run(_run())
        print_message(
            f"[green]Test data '{result['name']}' deleted successfully[/green]", ctx.obj["FORMAT"]
        )
    except Exception as e:
        print_message(f"[red]Failed to delete test data:[/red] {str(e)}", ctx.obj["FORMAT"])
        exit(1)


@test_data_group.command(
    name="upload-file", help="Upload a file to a test data using ID and file path"
)
@click.argument("test_data_id")
@click.argument("file_path")
@click.pass_context
def upload_file(ctx, test_data_id, file_path):
    """Upload a file to a test data"""

    async def _run():
        config, token, tenant_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            file_path_validated = Path(file_path)
            if not file_path_validated.exists():
                print_message(f"[red]File not found:[/red] {file_path}", ctx.obj["FORMAT"])
                exit(1)
            params = {
                "supporting_data_files+": FileUpload(file_path, open(file_path, "rb")),
                "tenant": tenant_id,
                "modified_by": user_id,
            }
            upload_file = await client.test_data.update(test_data_id_validated, params)
            return upload_file.data

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error uploading file:[/red] {str(e)}", ctx.obj["FORMAT"])
        raise click.Abort()


@test_data_group.command(
    name="delete-all-files", help="Delete all files from a test data using ID"
)
@click.argument("test_data_id")
@click.pass_context
def delete_all_files(ctx, test_data_id):
    """Delete all files from a test data"""

    async def _run():
        config, token, tenant_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_data_id_validated = validate_id(test_data_id, "test data")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            params = {
                "supporting_data_files": None,
                "tenant": tenant_id,
                "modified_by": user_id,
            }
            update_test_data = await client.test_data.update(
                test_data_id_validated, params
            )
            return update_test_data.data

    try:
        result = asyncio.run(_run())
        format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error deleting all files:[/red] {str(e)}", ctx.obj["FORMAT"])
        raise click.Abort()


@test_data_group.command(
    name="remove-file", help="Remove a file from a test data using ID and file path"
)
@click.argument("test_data_id")
@click.argument("file_path")
@click.pass_context
def remove_file(ctx, test_data_id, file_path):
    """Remove a file from a test data"""

    async def _run():
        config, token, tenant_id, user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)
        async with client:
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            test_data_data = await client.test_data.get_one(test_data_id)
            file_name = None
            if test_data_data.supporting_data_files:
                for file in test_data_data.supporting_data_files:
                    if (
                        file_path.split("/")[-1].split(".")[0].lower()
                        == file.split("_")[0].lower()
                    ):
                        file_name = file
                        break
            params = {
                "supporting_data_files-": [file_name],
                "tenant": tenant_id,
                "modified_by": user_id,
            }
            await client.test_data.update(test_data_id, params)
            return {"id": test_data_id}

    try:
        result = asyncio.run(_run())
        print_message(f"[green]File removed from test data {result['id']}[/green]", ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error removing file:[/red] {str(e)}", ctx.obj["FORMAT"])
        raise click.Abort()
