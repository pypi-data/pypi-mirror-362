import os
import click
from sima_cli.utils.env import get_environment_type
from sima_cli.update.updater import perform_update
from sima_cli.model_zoo.model import list_models, download_model, describe_model
from sima_cli.utils.config_loader import internal_resource_exists
from sima_cli.mla.meminfo import monitor_simaai_mem_chart

# Entry point for the CLI tool using Click's command group decorator
@click.group()
@click.option('-i', '--internal', is_flag=True, help="Use internal Artifactory resources.")
@click.pass_context
def main(ctx, internal):
    """
    sima-cli – SiMa Developer Portal CLI Tool

    Global Options:
      --internal  Use internal Artifactory resources (can also be set via env variable SIMA_CLI_INTERNAL=1)
    """
    ctx.ensure_object(dict)

    # Allow env override if --internal not explicitly passed
    if not internal:
        internal = os.getenv("SIMA_CLI_INTERNAL", "0") in ("1", "true", "yes")

    if internal and not internal_resource_exists():
        click.echo("❌ You have specified -i or --internal argument to access internal resources, but you do not have an internal resource map configured.")        
        click.echo("Refer to the confluence page to find out how to configure internal resource map.")
        exit(0)        

    ctx.obj["internal"] = internal

    env_type, env_subtype = get_environment_type()

    if internal:
        click.echo(f"🔧 Environment: {env_type} ({env_subtype}) | Internal: {internal}")
    else:
        click.echo(f"🔧 Environment: {env_type} ({env_subtype})")

# ----------------------
# Authentication Command
# ----------------------
@main.command()
@click.pass_context
def login(ctx):
    """Authenticate with the SiMa Developer Portal."""

    from sima_cli.auth import login as perform_login

    internal = ctx.obj.get("internal", False)
    perform_login.login("internal" if internal else "external")

# ----------------------
# Download Command
# ----------------------
@main.command(name="download")
@click.argument('url')  # Accept both file and folder URLs
@click.option('-d', '--dest', type=click.Path(), default='.', help="Target download directory")
@click.pass_context
def download(ctx, url, dest):
    """Download a file or a whole folder from a given URL."""
    from sima_cli.download.downloader import download_file_from_url, download_folder_from_url

    internal = ctx.obj.get("internal", False)

    # First, try to download as a file
    try:
        click.echo("🔍 Checking if URL is a direct file...")
        path = download_file_from_url(url, dest, internal)
        click.echo(f"\n✅ File downloaded successfully to: {path}")
        return
    except Exception as e:
        pass

    # If that fails, try to treat as a folder and download all files
    try:
        click.echo("🔍 Attempting folder download...")
        paths = download_folder_from_url(url, dest, internal)
        if not paths:
            raise RuntimeError("No files were downloaded.")
        click.echo(f"\n✅ Folder download completed. {len(paths)} files saved to: {dest}")
    except Exception as e:
        click.echo(f"\n❌ Failed to download as folder: {e}", err=True)

# ----------------------
# Update Command
# ----------------------
@main.command(name="update")
@click.argument('version_or_url')
@click.option('--ip', help="Target device IP address for remote firmware update.")

@click.option(
    '--passwd',
    default='edgeai',
    help="Optional SSH password for remote board (default is 'edgeai')."
)
@click.pass_context
def update(ctx, version_or_url, ip, passwd):
    """
    Run system update across different environments.
    Downloads and applies firmware updates for PCIe host or SiMa board.

    version_or_url: The version string (e.g. '1.5.0') or a direct URL to the firmware package.
    """
    internal = ctx.obj.get("internal", False)
    if not internal:
        click.echo(f"external environment is not supported yet..")
        exit(0)
 
    perform_update(version_or_url, ip, internal, passwd=passwd)

# ----------------------
# Model Zoo Subcommands
# ----------------------
@main.group()
@click.option('--ver', default="1.6.0", show_default=True, help="SDK version, minimum and default is 1.6.0")
@click.pass_context
def modelzoo(ctx, ver):
    """Access models from the Model Zoo."""
    ctx.ensure_object(dict)
    ctx.obj['ver'] = ver
    internal = ctx.obj.get("internal", False)
    if not internal:
        click.echo(f"external environment is not supported yet..")
        exit(0)

    pass

@modelzoo.command("list")
@click.pass_context
def list_models_cmd(ctx):
    """List available models."""
    internal = ctx.obj.get("internal", False)
    version = ctx.obj.get("ver")
    click.echo(f"Listing models for version: {version}")
    list_models(internal, version)

@modelzoo.command("get")
@click.argument('model_name') 
@click.pass_context
def get_model(ctx, model_name):
    """Download a specific model."""
    ver = ctx.obj.get("ver")
    internal = ctx.obj.get("internal", False)
    click.echo(f"Getting model '{model_name}' for version: {ver}")
    download_model(internal, ver, model_name)

@modelzoo.command("describe")
@click.argument('model_name') 
@click.pass_context
def get_model(ctx, model_name):
    """Download a specific model."""
    ver = ctx.obj.get("ver")
    internal = ctx.obj.get("internal", False)
    click.echo(f"Getting model '{model_name}' for version: {ver}")
    describe_model(internal, ver, model_name)

# ----------------------
# Authentication Command
# ----------------------
@main.group()
@click.pass_context
def mla(ctx):
    """Machine Learning Accelerator Utilities."""
    env_type, _ = get_environment_type()
    if env_type != 'board':
        click.echo("❌ This command can only be executed on the SiMa board.")
    pass

@mla.command("meminfo")
@click.pass_context
def show_mla_memory_usage(ctx):
    """Show MLA Memory usage overtime."""
    monitor_simaai_mem_chart()
    pass

# ----------------------
# App Zoo Subcommands
# ----------------------
# @main.group()
# @click.pass_context
# def app_zoo(ctx):
#     """Access apps from the App Zoo."""
#     pass

# @app_zoo.command("list")
# @click.option('--ver', help="SDK version")
# @click.pass_context
# def list_apps(ctx, ver):
#     """List available apps."""
#     # Placeholder: Call API to list apps
#     click.echo(f"Listing apps for version: {ver or 'latest'}")

# @app_zoo.command("get")
# @click.argument('app_name')  # Required: app name
# @click.option('--ver', help="SDK version")
# @click.pass_context
# def get_app(ctx, app_name, ver):
#     """Download a specific app."""
#     # Placeholder: Download and validate app
#     click.echo(f"Getting app '{app_name}' for version: {ver or 'latest'}")

# ----------------------
# Entry point for direct execution
# ----------------------
if __name__ == "__main__":
    main()
