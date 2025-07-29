"""
Commands for managing tests in TestZeus CLI.
"""

import asyncio
import click
from pathlib import Path
from rich.console import Console

from testzeus_sdk import TestZeusClient
from testzeus_cli.config import get_client_config
from testzeus_cli.utils.formatters import format_output, print_message
from testzeus_cli.utils.validators import validate_id, parse_key_value_pairs
from testzeus_cli.utils.client import run_client_operation
from testzeus_cli.utils.auth import initialize_client_with_token

console = Console()


@click.group(name="tests")
def tests_group():
    """Manage TestZeus tests"""
    pass


@tests_group.command(name="list")
@click.option(
    "--filters", "-f", multiple=True, help="Filter results (format: key=value)"
)
@click.option("--sort", help="Sort by field")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def list_tests(ctx, filters, sort, expand):
    """List tests with optional filters and sorting"""

    # Parse filters
    filter_dict = parse_key_value_pairs(filters) if filters else {}

    # Define the operation to run with the authenticated client
    async def _list_tests(client: TestZeusClient):
        return await client.tests.get_list(
            expand=expand, sort=sort, filters=filter_dict
        )

    # Run the operation and format the result
    result = run_client_operation(ctx, _list_tests)
    format_output(result, ctx.obj["FORMAT"])


@tests_group.command(name="get")
@click.argument("test_id")
@click.option("--expand", help="Expand related entities")
@click.pass_context
def get_test(ctx, test_id, expand):
    """Get a single test by ID"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            test = await client.tests.get_one(test_id_validated, expand=expand)
            return test.data

    result = asyncio.run(_run())
    format_output(result, ctx.obj["FORMAT"])


def _read_feature_file(file_path: str) -> str:
    """
    Read feature content from a file as plain text

    Args:
        file_path: Path to the feature file

    Returns:
        The raw text content of the file
    """
    feature_path = Path(file_path)
    if not feature_path.exists():
        raise click.BadParameter(f"Feature file not found: {file_path}")

    try:
        with open(feature_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except Exception as e:
        raise click.BadParameter(f"Failed to read feature file: {str(e)}")

    # Always return the raw text content, regardless of file extension
    return content


@tests_group.command(name="create")
@click.option("--name", required=True, help="Test name")
@click.option("--feature", help="Test feature content as text")
@click.option("--feature-file", help="Path to file containing feature content (text)")
@click.option("--status", default="draft", help="Test status (draft, ready, deleted)")
@click.option("--data", multiple=True, help="Test data IDs")
@click.option("--tags", multiple=True, help="Tag IDs")
@click.option("--environment", help="Environment ID")
@click.option(
    "--execution-mode", default="lenient", help="Execution mode (lenient, strict)"
)
@click.pass_context
def create_test(
    ctx, name, feature, feature_file, status, data, tags, environment, execution_mode
):
    """Create a new test with feature content from text or file"""

    if not feature and not feature_file:
        raise click.UsageError("Either --feature or --feature-file is required")

    if feature and feature_file:
        raise click.UsageError("Cannot use both --feature and --feature-file")

    # Process the feature content (from file or directly)
    feature_content = _read_feature_file(feature_file) if feature_file else feature

    async def _run():
        config, token, stored_tenant_id, stored_user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        # Prepare parameters
        test_data = {
            "name": name,
            "status": status,
            "execution_mode": execution_mode,
            "tenant": stored_tenant_id,
            "modified_by": stored_user_id,
            "metadata": {},
            "test_params": {},
        }

        # Always set feature content as text
        test_data["test_feature"] = feature_content

        if data:
            test_data["test_data"] = list(data)

        if tags:
            test_data["tags"] = list(tags)

        if environment:
            test_data["environment"] = environment

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            if ctx.obj.get("VERBOSE"):
                console.print(
                    f"[blue]Creating test with parameters: {test_data}[/blue]"
                )

            new_test = await client.tests.create(test_data)
            return new_test.data

    result = asyncio.run(_run())
    print_message(f"[green]Test created successfully with ID: {result['id']}[/green]", ctx.obj["FORMAT"])
    format_output(result, ctx.obj["FORMAT"])


@tests_group.command(name="update")
@click.argument("test_id")
@click.option("--name", help="New test name")
@click.option("--feature", help="New test feature content as text")
@click.option(
    "--feature-file", help="Path to file containing new feature content (text)"
)
@click.option("--status", help="New test status (draft, ready, deleted)")
@click.option("--data", multiple=True, help="Test data IDs")
@click.option("--tags", multiple=True, help="Tag IDs")
@click.option("--environment", help="Environment ID")
@click.pass_context
def update_test(
    ctx, test_id, name, feature, feature_file, status, data, tags, environment
):
    """Update an existing test with feature content from text or file"""

    if feature and feature_file:
        raise click.UsageError("Cannot use both --feature and --feature-file")

    # Process the feature content if a file was provided
    feature_content = None
    if feature_file:
        feature_content = _read_feature_file(feature_file)
    elif feature:
        feature_content = feature

    async def _run():
        config, token, stored_tenant_id, stored_user_id = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                # Use the safe initialization method to ensure tenant data is set
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()
            # Start with all existing data to ensure we don't lose anything
            update_data = {"tenant": stored_tenant_id, "modified_by": stored_user_id}

            has_updates = False

            # Add only the fields the user wants to update
            if name:
                update_data["name"] = name
                has_updates = True

            if feature_content is not None:
                # Always set feature content as text
                update_data["test_feature"] = feature_content
                has_updates = True

            if status:
                update_data["status"] = status
                has_updates = True

            if data:
                update_data["test_data"] = list(data)
                has_updates = True

            if tags:
                update_data["tags"] = list(tags)
                has_updates = True

            if environment:
                update_data["environment"] = environment
                has_updates = True

            if not has_updates:
                print_message("[yellow]No updates provided[/yellow]", ctx.obj["FORMAT"])
                return None

            if ctx.obj.get("VERBOSE"):
                console.print(f"[blue]Updating test with: {update_data}[/blue]")

            updated_test = await client.tests.update(test_id_validated, update_data)
            return updated_test.data

    try:
        result = asyncio.run(_run())
        if result:
            print_message(f"[green]Test updated successfully: {result['name']}[/green]", ctx.obj["FORMAT"])
            format_output(result, ctx.obj["FORMAT"])
    except Exception as e:
        if ctx.obj.get("VERBOSE"):
            print_message("[red]Error updating test:[/red]", ctx.obj["FORMAT"])
            import traceback

            print_message(traceback.format_exc(), ctx.obj["FORMAT"])
        else:
            print_message(f"[red]Error updating test:[/red] {str(e)}", ctx.obj["FORMAT"])
        exit(1)


@tests_group.command(name="delete")
@click.argument("test_id")
@click.confirmation_option(prompt="Are you sure you want to delete this test?")
@click.pass_context
def delete_test(ctx, test_id):
    """Delete a test"""

    async def _run():
        config, token, _, _ = get_client_config(
            ctx.obj["PROFILE"], api_url=ctx.obj.get("API_URL")
        )
        client = TestZeusClient(**config)

        test_id_validated = validate_id(test_id, "test")

        async with client:
            # Apply token from config if available
            if token:
                initialize_client_with_token(client, token)
            else:
                await client.ensure_authenticated()

            success = await client.tests.delete(test_id_validated)
            return {"success": success, "id": test_id_validated}

    try:
        result = asyncio.run(_run())
        print_message(f"[green]Test deleted successfully: {result['id']}[/green]", ctx.obj["FORMAT"])
    except Exception as e:
        print_message(f"[red]Error deleting test:[/red] {str(e)}", ctx.obj["FORMAT"])
        exit(1)
