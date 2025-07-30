import click
import os
import re
import time
import tempfile
import tarfile
import subprocess
from InquirerPy import inquirer
from urllib.parse import urlparse
from typing import List
from sima_cli.utils.env import get_environment_type
from sima_cli.download import download_file_from_url
from sima_cli.utils.config_loader import load_resource_config
from sima_cli.update.remote import push_and_update_remote_board, get_remote_board_info, reboot_remote_board
from sima_cli.update.local import get_local_board_info, push_and_update_local_board
from sima_cli.update.query import list_available_firmware_versions

def _resolve_firmware_url(version_or_url: str, board: str, internal: bool = False) -> str:
    """
    Resolve the final firmware download URL based on board, version, and environment.

    Args:
        version_or_url (str): Either a version string (e.g. 1.6.0_master_B1611) or a full URL.
        board (str): Board type ('davinci' or 'modalix').
        internal (bool): Whether to use internal config for URL construction.

    Returns:
        str: Full download URL.
    """
    # If it's already a full URL, return it as-is
    if re.match(r'^https?://', version_or_url):
        return version_or_url

    # Load internal or public config
    cfg = load_resource_config()

    repo_cfg = cfg.get("internal" if internal else "public", {}).get("download")
    artifactory_cfg = cfg.get("internal" if internal else "public", {}).get("artifactory")
    base_url = artifactory_cfg.get("url", {})
    download_url = repo_cfg.get("download_url")
    url = f"{base_url}/{download_url}"
    if not url:
        raise RuntimeError("⚠️ 'url' is not defined in resource config.")

    # Format full download path, internal for now.
    download_url = url.rstrip("/") + f"/soc-images/{board}/{version_or_url}/artifacts/release.tar.gz"
    return download_url

def _pick_from_available_versions(board: str, version_or_url: str, internal: bool) -> str:
    """
    Presents an interactive menu (with search) for selecting a firmware version.
    """

    if "http" in version_or_url:
        return version_or_url

    available_versions = list_available_firmware_versions(board, version_or_url, internal=True)

    if len(available_versions) > 1:
        click.echo("Multiple firmware versions found matching your input:")

        selected_version = inquirer.fuzzy(
            message="Select a version:",
            choices=available_versions,
            max_height="70%",  # scrollable
            instruction="(Use ↑↓ to navigate, / to search, Enter to select)"
        ).execute()

        if not selected_version:
            click.echo("No selection made. Exiting.", err=True)
            raise SystemExit(1)

        return selected_version

    elif len(available_versions) == 1:
        return available_versions[0]

    else:
        click.echo(
            f"No firmware versions found matching keyword '{version_or_url}' for board '{board}'.",
            err=True
        )
        raise SystemExit(1)

def _sanitize_url_to_filename(url: str) -> str:
    """
    Convert a URL to a safe filename by replacing slashes and removing protocol.

    Args:
        url (str): Original URL.

    Returns:
        str: Safe, descriptive filename (e.g., soc-images__modalix__1.6.0__release.tar.gz)
    """
    parsed = urlparse(url)
    path = parsed.netloc + parsed.path
    safe_name = re.sub(r'[^\w.-]', '__', path)
    return safe_name


def _extract_required_files(tar_path: str, board: str) -> list:
    """
    Extract required files from a .tar.gz or .tar archive into the same folder
    and return the full paths to the extracted files (with subfolder if present).
    Skips files that already exist.

    Args:
        tar_path (str): Path to the downloaded or provided firmware archive.
        board (str): Board type ('davinci' or 'modalix').

    Returns:
        list: List of full paths to extracted files.
    """
    extract_dir = os.path.dirname(tar_path)

    # Define required filenames (not full paths)
    target_filenames = {
        "troot-upgrade-simaai-ev.swu",
        f"simaai-image-palette-upgrade-{board}.swu"
    }

    env_type, _os = get_environment_type()
    if env_type == "host" and _os == "linux":
        target_filenames.add("sima_pcie_host_pkg.sh")

    extracted_paths = []

    try:
        try:
            tar = tarfile.open(tar_path, mode="r:gz")
        except tarfile.ReadError:
            tar = tarfile.open(tar_path, mode="r:")

        with tar:
            for member in tar.getmembers():
                base_name = os.path.basename(member.name)
                if base_name in target_filenames:
                    full_dest_path = os.path.join(extract_dir, member.name)

                    if os.path.exists(full_dest_path):
                        click.echo(f"⚠️  Skipping existing file: {full_dest_path}")
                        extracted_paths.append(full_dest_path)
                        continue

                    # Ensure directory structure exists
                    os.makedirs(os.path.dirname(full_dest_path), exist_ok=True)

                    tar.extract(member, path=extract_dir)
                    extracted_paths.append(full_dest_path)
                    click.echo(f"✅ Extracted: {full_dest_path}")

        if not extracted_paths:
            click.echo("⚠️  No matching files were found or extracted.")

        return extracted_paths

    except Exception as e:
        click.echo(f"❌ Failed to extract files from archive: {e}")
        return []

def _download_image(version_or_url: str, board: str, internal: bool = False):
    """
    Download or use a firmware image for the specified board and version or file path.

    Args:
        version_or_url (str): Version string, HTTP(S) URL, or local file path.
        board (str): Target board type ('davinci' or 'modalix').
        internal (bool): Whether to use internal Artifactory resources.

    Notes:
        - If a local file is provided, it skips downloading.
        - Downloads the firmware into the system's temporary directory otherwise.
        - Target file name is uniquely derived from the URL or preserved from local path.
    """
    try:
        # Case 1: Local file provided
        if os.path.exists(version_or_url) and os.path.isfile(version_or_url):
            click.echo(f"📁 Using local firmware file: {version_or_url}")
            return _extract_required_files(version_or_url, board)

        # Case 2: Treat as custom full URL
        if version_or_url.startswith("http://") or version_or_url.startswith("https://"):
            image_url = version_or_url
        else:
            # Case 3: Resolve standard version string (Artifactory/AWS)
            image_url = _resolve_firmware_url(version_or_url, board, internal)

        # Determine platform-safe temp directory
        temp_dir = tempfile.gettempdir()
        os.makedirs(temp_dir, exist_ok=True)

        # Build safe filename based on the URL
        safe_filename = _sanitize_url_to_filename(image_url)
        dest_path = os.path.join(temp_dir, safe_filename)

        # Download the file
        click.echo(f"📦 Downloading from {image_url}")
        firmware_path = download_file_from_url(image_url, dest_path, internal=internal)

        click.echo(f"📦 Firmware downloaded to: {firmware_path}")
        return _extract_required_files(firmware_path, board)

    except Exception as e:
        click.echo(f"❌ Host update failed: {e}")

def _update_host(script_path: str, board: str, boardip: str, passwd: str):
    """
    Perform PCIe host update by running the sima_pcie_host_pkg.sh script.

    Args:
        script_path (str): Full path of the extracted host package script
        board (str): Board type (e.g., 'davinci' or 'modalix').
    """
    try:
        if not script_path or not os.path.isfile(script_path):
            click.echo("❌ sima_pcie_host_pkg.sh not found in extracted files.")
            return

        click.echo(f"🚀 Running PCIe host install script: {script_path}")

        # Start subprocess with live output streaming
        process = subprocess.Popen(
            ["sudo", "bash", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        # Stream output line by line
        for line in process.stdout:
            click.echo(f"📄 {line.strip()}")

        process.stdout.close()
        returncode = process.wait()

        if returncode != 0:
            click.echo(f"❌ Host driver install script exited with code {returncode}.")
            return

        click.echo("✅ PCIe host update completed successfully.")

        # Ask for reboot
        if click.confirm("🔄 Do you want to reboot your system now?", default=True):
            click.echo("♻️ Rebooting system...")
            # This workaround reboots the PCIe card before we reboot the system
            reboot_remote_board(boardip, passwd)
            time.sleep(2)
            subprocess.run(["sudo", "reboot"])
        else:
            click.echo("🕒 Reboot skipped. Please powercycle to apply changes.")

    except Exception as e:
        click.echo(f"❌ Host update failed: {e}")


def _update_sdk(version_or_url: str, board: str):
    click.echo(f"⚙️  Simulated SDK firmware update logic for board '{board}' (not implemented).")
    # TODO: Implement update via SDK-based communication or tools

def _update_board(extracted_paths: List[str], board: str, passwd: str):
    """
    Perform local firmware update using extracted files.

    Args:
        extracted_paths (List[str]): Paths to the extracted .swu files.
        board (str): Board type expected (e.g. 'davinci', 'modalix').
    """
    click.echo(f"⚙️  Starting local firmware update for board '{board}'...")

    # Locate the needed files
    troot_path = next((p for p in extracted_paths if "troot-upgrade" in os.path.basename(p)), None)
    palette_path = next((p for p in extracted_paths if f"palette-upgrade-{board}" in os.path.basename(p)), None)

    if not troot_path or not palette_path:
        click.echo("❌ Required firmware files not found in extracted paths.")
        return

    # Optionally verify the board type
    board_type, _ = get_local_board_info()
    if board_type.lower() != board.lower():
        click.echo(f"❌ Board mismatch: expected '{board}', but found '{board_type}'")
        return

    click.echo("✅ Board verified. Starting update...")
    push_and_update_local_board(troot_path, palette_path, passwd)

def _update_remote(extracted_paths: List[str], ip: str, board: str, passwd: str, reboot_and_wait: bool = True):
    """
    Perform remote firmware update to the specified board via SSH.

    Args:
        extracted_paths (List[str]): Paths to the extracted .swu files.
        ip (str): IP of the remote board.
        board (str): Expected board type ('davinci' or 'modalix').
        passwd (str): password to access the board, if it's not default
    """
    click.echo(f"⚙️  Starting remote update on '{ip}' for board type '{board}'...")

    # Locate files
    troot_path = next((p for p in extracted_paths if "troot-upgrade" in os.path.basename(p)), None)
    palette_path = next((p for p in extracted_paths if f"palette-upgrade-{board}" in os.path.basename(p)), None)
    script_path = next((p for p in extracted_paths if p.endswith("sima_pcie_host_pkg.sh")), None)

    if not troot_path or not palette_path:
        click.echo("❌ Required firmware files not found in extracted paths.")
        return

    # Get remote board info
    click.echo("🔍 Checking remote board type and version...")
    remote_board, remote_version = get_remote_board_info(ip, passwd)

    if not remote_board:
        click.echo("❌ Could not determine remote board type.")
        return

    click.echo(f"🔍 Remote board: {remote_board} | Version: {remote_version}")

    if remote_board.lower() != board.lower():
        click.echo(f"❌ Board mismatch: expected '{board}', but got '{remote_board}' on device.")
        return

    # Proceed with update
    click.echo("✅ Board type verified. Proceeding with firmware update...")
    push_and_update_remote_board(ip, troot_path, palette_path, passwd=passwd, reboot_and_wait=reboot_and_wait)

    return script_path


def perform_update(version_or_url: str, ip: str = None, internal: bool = False, passwd: str = "edgeai"):
    r"""
    Update the system based on environment and input.

    - On PCIe host: updates host driver and/or downloads firmware.
    - On SiMa board: applies firmware update.
    - In SDK: allows simulated or direct board update.
    - Unknown env: requires --ip to specify remote device.

    Args:
        version_or_url (str): Version string or direct URL.
        ip (str): Optional remote target IP.
        board (str): Board type, must be 'davinci' or 'modalix'.
        passwd : non-default password in case user has changed the password of the board user `sima`
    """
    try:
        board = ''
        env_type, env_subtype = get_environment_type()
        click.echo(f"🔄 Running update for environment: {env_type} ({env_subtype})")
        click.echo(f"🔧 Requested version or URL: {version_or_url}")

        if env_type == 'board':
            board, version = get_local_board_info()
        else:
            board, version = get_remote_board_info(ip, passwd)

        if board in ['davinci', 'modalix']:
            click.echo(f"🔧 Target board: {board}, board currently running: {version}")
                        
            if 'http' not in version_or_url:
                version_or_url = _pick_from_available_versions(board, version_or_url, internal)

            extracted_paths = _download_image(version_or_url, board, internal)
            click.echo("⚠️  DO NOT INTERRUPT THE UPDATE PROCESS...")

            if len(extracted_paths) > 0:
                if env_type == "host" and env_subtype == 'linux':
                    # Always update the remote device first then update the host driver, otherwise the host would 
                    # not be able to connect to the board
                    click.echo("👉 Updating PCIe host driver and downloading firmware...")        
                    script_path = _update_remote(extracted_paths, ip, board, passwd, reboot_and_wait = False)
                    _update_host(script_path, board, ip, passwd)
                elif env_type == "board":
                    _update_board(extracted_paths, board, passwd)
                elif env_type == "sdk":
                    click.echo("👉 Updating firmware from within the Palette SDK...: Not implemented yet")
                elif ip:
                    click.echo(f"👉 Updating firmware on remote board at {ip}...")
                    _update_remote(extracted_paths, ip, board, passwd, reboot_and_wait = True)
                else:
                    click.echo("❌ Unknown environment. Use --ip to specify target device.")
        else:
            click.echo("❌ Unable to retrieve target board information")

    except Exception as e:
        click.echo(f"❌ Update failed {e}")

