"""
TestZeus CLI - Command line interface for TestZeus testing platform.
"""

import sys
import click
from rich.console import Console

from testzeus_cli import __version__
from testzeus_cli.auth import login_command, logout_command, whoami_command
from testzeus_cli.commands.tests import tests_group
from testzeus_cli.commands.test_runs import test_runs_group
from testzeus_cli.commands.test_data import test_data_group
from testzeus_cli.commands.tags import tags_group
from testzeus_cli.commands.environments import environments_group

# New command groups can be imported here when implemented

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="testzeus")
@click.option("--profile", default="default", help="Configuration profile to use")
@click.option("--api-url", help="TestZeus API URL")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table", "yaml"]),
    default="table",
    help="Output format",
)
@click.pass_context
def cli(ctx, profile, api_url, verbose, output_format):
    """TestZeus CLI - Command line interface for TestZeus testing platform"""
    ctx.ensure_object(dict)
    ctx.obj["PROFILE"] = profile
    ctx.obj["API_URL"] = api_url
    ctx.obj["VERBOSE"] = verbose
    ctx.obj["FORMAT"] = output_format


# Add commands
cli.add_command(login_command)
cli.add_command(logout_command)
cli.add_command(whoami_command)
cli.add_command(tests_group)
cli.add_command(test_runs_group)
cli.add_command(test_data_group)
cli.add_command(tags_group)
cli.add_command(environments_group)
# New command groups can be added here when implemented


def main():
    """Main entry point for the CLI"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        if "--verbose" in sys.argv:
            console.print_exception(show_locals=True)
        else:
            console.print("[yellow]Run with --verbose for more details[/yellow]")
        sys.exit(1)


if __name__ == "__main__":
    main()
