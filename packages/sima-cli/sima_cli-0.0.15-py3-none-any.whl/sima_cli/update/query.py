import requests
from sima_cli.utils.config_loader import load_resource_config, artifactory_url
from sima_cli.utils.config import get_auth_token

ARTIFACTORY_BASE_URL = artifactory_url() + '/artifactory'

def _list_available_firmware_versions_internal(board: str, match_keyword: str = None):
    fw_path = f"{board}" 
    aql_query = f"""
                items.find({{
                    "repo": "soc-images",
                    "path": {{
                        "$match": "{fw_path}/*"
                    }},
                    "type": "folder"
                }}).include("repo", "path", "name")
                """.strip()

    aql_url = f"{ARTIFACTORY_BASE_URL}/api/search/aql"
    headers = {
        "Content-Type": "text/plain",
        "Authorization": f"Bearer {get_auth_token(internal=True)}"
    }

    response = requests.post(aql_url, data=aql_query, headers=headers)
    if response.status_code != 200:
        return None

    results = response.json().get("results", [])

    # Reconstruct full paths and remove board prefix
    full_paths = {
        f"{item['path']}/{item['name']}".replace(fw_path + "/", "")
        for item in results
    }

    # Extract top-level folders
    top_level_folders = sorted({path.split("/")[0] for path in full_paths})

    if match_keyword:
        match_keyword = match_keyword.lower()
        top_level_folders = [
            f for f in top_level_folders if match_keyword in f.lower()
        ]

    return top_level_folders


def list_available_firmware_versions(board: str, match_keyword: str = None, internal: bool = False):
    """
    Public interface to list available firmware versions.

    Parameters:
    - board: str – Name of the board (e.g. 'davinci')
    - match_keyword: str – Optional keyword to filter versions (case-insensitive)
    - internal: bool – Must be True to access internal Artifactory

    Returns:
    - List[str] of firmware version folder names, or None if access is not allowed
    """
    if not internal:
        raise PermissionError("Internal access required to list firmware versions.")

    return _list_available_firmware_versions_internal(board, match_keyword)
