import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os

def get_driver(soc, os_choice, device, interface):
    """
    Returns the list of filenames for the driver and script based on soc, os_choice, and device
    by fetching them dynamically from the GitHub repository and reading devices.json locally
    """
    # GitHub repository details
    owner = "compilewith-SURENDHAR"
    repo = "Device_Driver_integration"
    base_url = "https://raw.githubusercontent.com/compilewith-SURENDHAR/Device_Driver_integration/main"
    api_base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    pat_token = "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"  # Replace with your actual GitHub PAT token

    # Log inputs for debugging
    print(f"Inputs: soc={soc}, os_choice={os_choice}, device={device}, interface={interface}")

    # Path to local devices.json in the static folder
    devices_file_path = os.path.join("static", "devices.json")
    
    # Check if the file exists locally
    if not os.path.exists(devices_file_path):
        raise FileNotFoundError(f"devices.json not found at {devices_file_path}")

    # Read devices.json from the local static folder
    try:
        with open(devices_file_path, "r") as file:
            config = json.load(file)
        print(f"devices.json content: {config}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in devices.json: {e}")
    except Exception as e:
        raise ValueError(f"Failed to read devices.json: {e}")

    # Validate SoC
    if soc not in config:
        raise ValueError(f"Unsupported SoC: {soc}. Supported SoCs: {list(config.keys())}")

    # Validate config[soc] is a dictionary
    if not isinstance(config[soc], dict):
        raise ValueError(f"Invalid devices.json structure: config[{soc}] is {type(config[soc]).__name__}, expected dict")

    # Validate interface
    interfaces = config[soc].get("interfaces", [])
    if interface not in interfaces:
        raise ValueError(
            f"Invalid interface '{interface}' for SoC '{soc}'. "
            f"Supported interfaces: {interfaces}"
        )

    # Validate device (allow non-supported devices for template folders)
    devices = config[soc].get("devices", [])
    is_device_supported = device in devices
    print(f"Device supported: {is_device_supported}")

    # Determine the folder name
    folder = f"available_devices/{soc}-{os_choice}-{device}" if is_device_supported else f"template/{soc}-{os_choice}-template-{interface}"
    print(f"Constructed folder: {folder}")

    # GitHub API URL for the folder
    api_url = f"{api_base_url}/{soc}/{folder}"
    print(f"Fetching files from: {api_url}")

    # Make API request to list files
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    headers = {"Authorization": f"token {pat_token}", "Accept": "application/vnd.github.v3+json"}
    
    try:
        response = session.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        files = response.json()
        print(f"API response: {files}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(
                f"Folder '{folder}' not found in GitHub repository. "
                f"Please verify that the folder exists for soc={soc}, os_choice={os_choice}, "
                f"device={device}, interface={interface}. Check the repository structure at "
                f"https://github.com/compilewith-SURENDHAR/Device_Driver_integration/tree/main/{folder}"
            ) from e
        raise ValueError(f"Failed to fetch files from GitHub API for folder {folder}: {e}")

    # Validate response type
    if not isinstance(files, list):
        error_msg = (
            files.get("message", "Unknown error") if isinstance(files, dict)
            else f"Unexpected response type: {type(files).__name__}"
        )
        raise ValueError(f"Unexpected API response for folder {folder}: {error_msg}")

    # Filter relevant files (e.g., .c, .h, makefile, external_component.txt, .mk, script.sh)
    valid_extensions = (".c", ".h", ".mk", "")
    links = [
        file["name"] for file in files
        if file["type"] == "file" and (
            file["name"].endswith(valid_extensions) or
            file["name"] in ["makefile", "external_component.txt", "script.sh"]
        )
    ]

    # Ensure script.sh is included if it exists
    if "script.sh" not in links and any(file["name"] == "script.sh" for file in files):
        links.append("script.sh")

    if not links:
        raise ValueError(f"No valid files found in folder {folder} for soc={soc}, os_choice={os_choice}, device={device}")

    print(f"Retrieved files: {links}")
    return links