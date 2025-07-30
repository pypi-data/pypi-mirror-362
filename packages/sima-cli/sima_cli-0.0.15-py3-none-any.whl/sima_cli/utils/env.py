import os
import subprocess
import platform
from typing import Tuple

# Utility functions to determine the environment:
# - Whether we are running on a SiMa board
# - Or from a PCIe host (e.g., a developer workstation)

def is_sima_board() -> bool:
    """
    Detect if running on a SiMa board.

    This is done by checking for the existence of a known build info file
    located at /etc/build and looking for specific identifiers like 
    SIMA_BUILD_VERSION and MACHINE.

    Returns:
        bool: True if running on a SiMa board, False otherwise.
    """
    build_file_path = "/etc/build"
    if not os.path.exists(build_file_path):
        return False

    try:
        with open(build_file_path, "r") as f:
            content = f.read()
            return "SIMA_BUILD_VERSION" in content and "MACHINE" in content
    except Exception:
        return False

def is_pcie_host() -> bool:
    """
    Detect if running from a PCIe host (typically a Linux or macOS dev machine).

    This assumes a PCIe host is not a SiMa board and is running on a standard
    Unix-based OS like Linux or macOS (Darwin).

    Returns:
        bool: True if likely a PCIe host, False otherwise.
    """
    import platform
    return not is_sima_board() and platform.system() in ["Linux", "Darwin"]

def get_sima_board_type() -> str:
    """
    If running on a SiMa board, extract the board type from the MACHINE field in /etc/build.

    Returns:
        str: The board type (e.g., "modalix", "davinci"), or an empty string if not found or not a SiMa board.
    """
    build_file_path = "/etc/build"
    if not os.path.exists(build_file_path):
        return ""

    try:
        with open(build_file_path, "r") as f:
            for line in f:
                if line.startswith("MACHINE"):
                    # Format: MACHINE = modalix
                    parts = line.split("=")
                    if len(parts) == 2:
                        return parts[1].strip()
    except Exception:
        pass

    return ""

def is_palette_sdk() -> bool:
    """
    Check if the environment is running inside the Palette SDK container.

    This is detected by checking for the /etc/sdk-release file and verifying
    it contains the string 'Palette_SDK'.

    Returns:
        bool: True if running in Palette SDK, False otherwise.
    """
    sdk_release_path = "/etc/sdk-release"
    if not os.path.exists(sdk_release_path):
        return False

    try:
        with open(sdk_release_path, "r") as f:
            content = f.read()
            return "Palette_SDK" in content
    except Exception:
        return False

def get_environment_type() -> Tuple[str, str]:
    """
    Return the environment type and subtype as a tuple.

    Returns:
        tuple:
            - env_type (str): "board", "sdk", or "host"
            - env_subtype (str): board type (e.g., "modalix"), "palette", or host OS (e.g., "mac", "linux", "windows")
    """
    if is_palette_sdk():
        return "sdk", "palette"

    if is_sima_board():
        board_type = get_sima_board_type()
        return "board", board_type or "unknown"

    import platform
    system = platform.system().lower()
    if system == "darwin":
        return "host", "mac"
    elif system == "linux":
        return "host", "linux"
    elif system == "windows":
        return "host", "windows"

    return "host", "unknown"

def check_pcie_card_installation() -> Tuple[bool, str]:
    """
    Check whether the PCIe SiMa card is properly installed on a supported Linux host.

    Returns:
        tuple:
            - success (bool): True if all checks pass, False otherwise.
            - message (str): Summary of results or error message.
    """
    # Platform check
    if platform.system().lower() != "linux":
        return False, "❌ This check is only supported on Linux hosts."

    if is_sima_board():
        return False, "❌ This check is not applicable when running on a SiMa board."

    if is_palette_sdk():
        return False, "❌ This check is not applicable inside the Palette SDK container."

    try:
        # Check GStreamer plugin
        gst_result = subprocess.run(
            ["gst-inspect-1.0", "pciehost"],
            capture_output=True, text=True
        )
        if gst_result.returncode != 0 or "pciehost" not in gst_result.stdout:
            return False, "❌ GStreamer plugin 'pciehost' not found."

        # Check kernel module
        modinfo_result = subprocess.run(
            ["modinfo", "sima_mla_drv"],
            capture_output=True, text=True
        )
        if modinfo_result.returncode != 0 or "sima_mla_drv" not in modinfo_result.stdout:
            return False, "❌ sima_mla_drv kernel module not found or not loaded."

        # Check PCI device presence
        lspci_result = subprocess.run(
            ["lspci", "-vd", "1f06:abcd"],
            capture_output=True, text=True
        )
        if lspci_result.returncode != 0 or "Device 1f06:abcd" not in lspci_result.stdout:
            return False, "❌ PCIe SiMa card not detected."

        return True, "✅ PCIe SiMa card is properly installed and recognized."

    except FileNotFoundError as e:
        return False, f"❌ Required system tool not found: {e.filename}"

    except Exception as e:
        return False, f"❌ Unexpected error: {str(e)}"


if __name__ == "__main__":
    env_type, env_subtype = get_environment_type()
    print(f"Environment Type: {env_type}")
    print(f"Environment Subtype: {env_subtype}")