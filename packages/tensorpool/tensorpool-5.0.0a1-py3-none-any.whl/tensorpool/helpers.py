import os
import time
from typing import Final, Optional, List, Dict, Tuple
import requests
from tqdm import tqdm
import importlib.metadata
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
import sys
import asyncio
import websockets
from .spinner import Spinner

# ENGINE: Final = "http://localhost:8000"
ENGINE: Final = "https://engine.tensorpool.dev/"

# TODO: deprecate, should all be in tpignore
IGNORE_FILE_SUFFIXES: Final = {
    "venv",
    "DS_Store",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
}


def get_tensorpool_key():
    """Get API key from env var first, then .env in cwd"""
    key = os.environ.get("TENSORPOOL_KEY")
    if key:
        return key

    try:
        with open(os.path.join(os.getcwd(), ".env")) as f:
            for line in f:
                if line.startswith("TENSORPOOL_KEY"):
                    return line.split("=", 1)[1].strip().strip("'").strip('"')
    except FileNotFoundError:
        return None

    return None


def save_tensorpool_key(api_key: str) -> bool:
    """Save API key to .env in current directory and set in environment"""
    try:
        with open(os.path.join(os.getcwd(), ".env"), "a+") as f:
            f.write(f"\nTENSORPOOL_KEY={api_key}\n")
        os.environ["TENSORPOOL_KEY"] = api_key
        assert os.getenv("TENSORPOOL_KEY") == api_key
        return True
    except Exception as e:
        print(f"Failed to save API key: {e}")
        return False


def login():
    """
    Store the API key in the .env file and set it in the environment variables.
    """
    print("https://tensorpool.dev/dashboard")
    api_key = input("Enter your TensorPool API key: ").strip()

    if not api_key:
        print("API key cannot be empty")
        return

    return save_tensorpool_key(api_key)


def get_version():
    try:
        return importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def health_check() -> (bool, str):
    """
    Checks if the TensorPool engine is online and if the package version is acceptable.
    Returns:
        bool: If the user can proceed
        str: A message to display to the user
    """

    key = os.getenv("TENSORPOOL_KEY")
    try:
        version = get_version()
        # print(f"Package version: {version}")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        response = requests.post(
            f"{ENGINE}/health",
            json={"package_version": version},
            headers=headers,
            timeout=15,
        )
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            # Malformed response handling
            # print(response.text)
            return (
                False,
                f"Received malformed response from server during health check. Status code: {response.status_code} \nIf this persists, please contact team@tensorpool.dev",
            )

        msg = data.get("message")

        if response.status_code == 200:
            # Healthy
            return (True, msg)
        else:
            # Engine online, but auth or health check failure
            return (False, msg)
    except requests.exceptions.ConnectionError:
        return (
            False,
            "Cannot reach the TensorPool. Please check your internet connection.\nHaving trouble? Contact team@tensorpool.dev",
        )
    except Exception as e:
        # Catch-all for unexpected failures
        return (False, f"Unexpected error during health check: {str(e)}")


def get_proj_paths():
    """
    Returns a list of all file paths in the project directory.
    """
    # TODO: make this use shouldignore
    files = [
        os.path.normpath(os.path.join(dirpath, f))
        for (dirpath, dirnames, filenames) in os.walk(".")
        if not any(i in dirpath for i in IGNORE_FILE_SUFFIXES)
        for f in filenames
        if not any(f.endswith(i) for i in IGNORE_FILE_SUFFIXES)
    ]

    return files


# TODO: ignore from tp config


# def should_ignore(path: str, ignore_patterns: set[str]) -> bool:
#     """
#     Check if path matches any ignore patterns.
#     """
#     path = Path(path)
#     name = path.name

#     for pattern in ignore_patterns:
#         # Handle both file/dir names and full paths
#         if fnmatch.fnmatch(name, pattern):
#             return True
#         if fnmatch.fnmatch(str(path), pattern):
#             return True
#     return False


def dump_file(content: str, path: str) -> bool:
    """
    Save raw text content to the specified file path
    Args:
        content: The raw text content to save
        path: The path to save the file
    Returns:
        A boolean indicating success
    """
    try:
        with open(path, "w") as f:
            f.write(content)
        return os.path.exists(path)
    except Exception:
        return False


def get_empty_tp_config() -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Fetch the default empty tp config from the job/init endpoint
    Returns:
        A tuple containing success status, empty config dict, and optional message
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['TENSORPOOL_KEY']}",
    }

    try:
        response = requests.get(
            f"{ENGINE}/job/init",
            headers=headers,
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        return False, None, f"Failed to fetch empty config: {str(e)}"

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        return False, None, "Received malformed response from server"

    if response.status_code != 200:
        message = res.get("message", "Failed to fetch empty config")
        return False, None, message

    empty_tp_config = res.get("empty_tp_config")
    message = res.get("message")

    if not empty_tp_config:
        return False, None, "No empty config received from server"

    return True, empty_tp_config, message


def listen_to_job(job_id: str) -> bool:
    """
    Connects to job stream and prints output in real-time.
    Returns if the job is completed or not.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['TENSORPOOL_KEY']}",
    }
    payload = {"id": job_id}

    # TODO: pull in stdout once job is succeeded

    try:
        response = requests.post(
            f"{ENGINE}/job/listen", json=payload, headers=headers, stream=True
        )

        if response.status_code != 200:
            print(f"Failed to connect to job stream: {response.text}")
            return

        for line in response.iter_lines():
            if not line:
                continue
            try:
                text = line.decode("utf-8")
            except UnicodeDecodeError:
                continue

            if text.startswith("data: "):
                pretty = text.replace("data: ", "", 1)
                print(pretty, flush=True)

                if pretty.startswith("[TP]") and pretty.endswith("COMPLETED"):
                    return True

    except KeyboardInterrupt:
        print("\nDetached from job stream")
        return False
    except Exception as e:
        print(f"Error while listening to job stream: {str(e)}")
        return False


def fetch_dashboard() -> str:
    """
    Fetch the TensorPool dashboard URL
    """

    timezone = time.strftime("%z")
    # print(timezone)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['TENSORPOOL_KEY']}",
    }
    payload = {
        "timezone": timezone,  # Timezone to formate timestamps
    }

    fallback_dashboard_msg = "https://tensorpool.dev/dashboard"

    try:
        response = requests.post(
            f"{ENGINE}/dashboard",
            json=payload,
            headers=headers,
            timeout=15,
        )

        try:
            res = response.json()
        except requests.exceptions.JSONDecodeError:
            return fallback_dashboard_msg

        message = res.get("message", fallback_dashboard_msg)
        return message

    except Exception as e:
        raise RuntimeError(f"Failed to fetch dashboard URL: {str(e)}")


async def _job_run_async(
    tp_config: str,
    public_key_contents: str,
    api_key: str,
    tensorpool_pub_key_path: str,
    tensorpool_priv_key_path: str,
) -> bool:
    """
    Async implementation of job_run using WebSocket
    """
    # Build WebSocket URL with API key
    ws_url = f"{ENGINE.replace('http://', 'ws://').replace('https://', 'wss://')}/job/run?api_key={api_key}"
    # print("ws_url:", ws_url)

    try:
        async with websockets.connect(
            ws_url, ping_interval=5, ping_timeout=10
        ) as websocket:
            # Send initial configuration
            initial_data = {
                "tp_config": tp_config,
                "public_key_path": tensorpool_pub_key_path,
                "private_key_path": tensorpool_priv_key_path,
                "public_keys": [public_key_contents],
            }
            await websocket.send(json.dumps(initial_data))

            # Process messages from server
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                # print("recieved data:", data)

                # Print status messages
                if "message" in data:
                    print(data["message"])

                # Execute commands sent by server
                if "command" in data:
                    command = data["command"]
                    show_stdout = data.get("command_show_stdout", False)

                    try:
                        # Set up environment to force unbuffered output
                        env = os.environ.copy()
                        env["PYTHONUNBUFFERED"] = "1"

                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.DEVNULL,  # Don't accept stdin
                            text=True,
                            bufsize=0,  # No buffering
                            universal_newlines=True,
                            env=env,
                        )

                        # Read stdout character by character for no buffering
                        stdout_chars = []
                        while True:
                            char = process.stdout.read(1)
                            if not char:
                                break
                            stdout_chars.append(char)
                            if show_stdout:
                                sys.stdout.write(char)
                                sys.stdout.flush()

                        # Wait for completion and get stderr
                        process.wait()
                        stderr = process.stderr.read()

                        stdout = "".join(stdout_chars)
                        returncode = process.returncode

                        # Print errors if command failed (and not already shown)
                        if returncode != 0 and not show_stdout:
                            if stderr:
                                print(f"Command error: {stderr}")
                            if stdout:
                                print(f"Command output: {stdout}")

                    except Exception as e:
                        print(f"Failed to execute command: {str(e)}")
                        stdout = ""
                        returncode = 1

                    # Send result back to server
                    response = {
                        "type": "command_result",
                        "command": command,
                        "exit_code": returncode,
                        "command_stdout": stdout,
                    }
                    await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed as e:
        # print(f"WebSocket connection closed: code = {e.code}, reason = {e.reason}")

        # TODO: not show for code 1000 bc that success?
        print(f"Job connection closed, code = {e.code}")
        if e.reason:
            print(e.reason)
        # else:
        #     print("No reason provided")
        return False

    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {str(e)}")
        return False

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

    # If we get here, the WebSocket closed normally
    return True


def job_run(
    tp_config_path: str,
    tensorpool_pub_key_path: str,
    tensorpool_priv_key_path: str,
) -> bool:
    """
    Run a job
    Args:
        tp_config_path: Path to the tp config file
        tensorpool_pub_key_path: Path to tensorpool public key
        tensorpool_priv_key_path: Path to tensorpool private key
    Returns:
        bool: True if job succeeded, False otherwise
    """
    if not os.path.exists(tp_config_path):
        print(f"Config file not found: {tp_config_path}")
        return False

    # Check that both key paths are provided
    if not tensorpool_pub_key_path or not tensorpool_priv_key_path:
        print("Both tensorpool public and private key paths are required")
        return False

    if not os.path.exists(tensorpool_pub_key_path):
        print(f"Public key file not found: {tensorpool_pub_key_path}")
        return False
    if not os.path.exists(tensorpool_priv_key_path):
        print(f"Private key file not found: {tensorpool_priv_key_path}")
        return False

    try:
        with open(tp_config_path, "r") as f:
            tp_config = f.read()
    except Exception as e:
        print(f"Failed to read {tp_config_path}: {str(e)}")
        return False

    try:
        with open(tensorpool_pub_key_path, "r") as f:
            public_key_contents = f.read().strip()
    except Exception as e:
        print(f"Failed to read {tensorpool_pub_key_path}: {str(e)}")
        return False

    api_key = get_tensorpool_key()
    if not api_key:
        print("TENSORPOOL_KEY not found. Please set your API key.")
        return False

    # Run the async function
    return asyncio.run(
        _job_run_async(
            tp_config,
            public_key_contents,
            api_key,
            tensorpool_pub_key_path,
            tensorpool_priv_key_path,
        )
    )


def job_pull(
    job_id: str,
    files: Optional[List[str]] = None,
    preview: bool = False,
) -> Tuple[Dict[str, str], str]:
    """
    Given a job ID, fetch the job's output files that changed during the job.
    Returns a download map and a message.
    """

    assert job_id, "A job ID is needed to pull a job"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['TENSORPOOL_KEY']}",
    }
    payload = {
        "id": job_id,
        "preview": preview,
    }
    if files:
        payload["files"] = files

    try:
        response = requests.post(
            f"{ENGINE}/job/pull", json=payload, headers=headers, timeout=60
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Job pull failed: {str(e)}")

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        # print(response.text)
        raise RuntimeError(
            f"Malformed response from server while pulling job. Status: {response.status_code}"
            "\nPlease try again or visit https://dashboard.tensorpool.dev/dashboard\nContact team@tensorpool.dev if this persists"
        )

    status = res.get("status")
    msg = res.get("message")
    if status != "success":
        return None, msg

    download_map = res.get("download_map")
    return download_map, msg


def download_files(download_map: Dict[str, str], overwrite: bool = False) -> bool:
    """
    Given a download map of file paths to signed GET URLs, download each file in parallel.
    If the same files exists locally, append a suffix to the filename.
    """

    max_workers = min(os.cpu_count() * 2 if os.cpu_count() else 6, 6)
    successes = []
    failures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:

        def _download_file(file_info):
            file_path, url = file_info
            headers = {"Content-Type": "application/octet-stream"}
            max_retries = 3
            base_delay = 1

            for retries in range(max_retries + 1):
                try:
                    response = requests.get(url, headers=headers, stream=True)
                    total_size = int(response.headers.get("content-length", 0))

                    if os.path.exists(file_path):
                        if overwrite:
                            print(f"Overwriting {file_path}")
                        else:
                            print(f"Skipping {file_path} - file already exists")
                            return True, (file_path, 200, "Skipped - file exists")

                    # Create directories for path if they don't exist
                    dir_name = os.path.dirname(file_path)
                    if dir_name:
                        os.makedirs(dir_name, exist_ok=True)

                    with open(file_path, "wb") as f:
                        with tqdm(
                            total=total_size,
                            unit="B",
                            unit_scale=True,
                            desc=f"Downloading {os.path.basename(file_path)}{' (attempt ' + str(retries + 1) + ')' if retries > 0 else ''}",
                        ) as pbar:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    pbar.update(len(chunk))

                    if response.status_code == 200:
                        return True, (file_path, response.status_code, "Success")

                    if retries < max_retries:
                        delay = base_delay * (2**retries)  # Exponential backoff
                        time.sleep(delay)
                        continue

                    return False, (file_path, response.status_code, response.text)

                except Exception as e:
                    if retries < max_retries:
                        delay = base_delay * (2**retries)
                        time.sleep(delay)
                        continue
                    return False, (file_path, "Exception", str(e))

        future_to_file = {
            executor.submit(_download_file, (file_path, url)): file_path
            for file_path, url in download_map.items()
        }

        for future in concurrent.futures.as_completed(future_to_file):
            success, result = future.result()
            if success:
                successes.append(result[0])
            else:
                failures.append(result)

    if failures:
        print("The following downloads failed:")
        for path, code, text in failures:
            print(f"{path}: Status {code} - {text}")
        return False

    return True


def job_cancel(job_id) -> Tuple[bool, Optional[str]]:
    """
    Given a job_id, attempt to cancel it.
    Returns (cancel successful, optional message to print)
    """
    assert job_id is not None, "A job ID is needed to cancel"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['TENSORPOOL_KEY']}",
    }
    payload = {
        "id": job_id,
    }

    try:
        response = requests.post(
            f"{ENGINE}/job/cancel",
            json=payload,
            headers=headers,
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        return False, f"Job cancellation failed: {str(e)}"

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        return (
            False,
            f"Malformed response from server. Status code: {response.status_code}",
        )

    status = res.get("status")
    message = res.get("message")

    if status == "success":
        return True, message
    else:
        return False, message


def cluster_create(
    identity_file: str,
    instance_type: str,
    name: Optional[str],
    num_nodes: Optional[int],
) -> Tuple[bool, str]:
    """
    Create a new cluster (cluster command)
    Args:
        identity_file: Path to public SSH key file
        instance_type: Instance type (e.g. 1xH100, 2xH100, 4xH100, 8xH100)
        name: Optional cluster name
        num_nodes: Number of nodes (must be >= 1)
    Returns:
        A tuple containing a boolean indicating success and a message
    """
    # Get API key
    api_key = get_tensorpool_key()
    if not api_key:
        return False, "TENSORPOOL_KEY not found. Please set your API key."

    if not instance_type:
        return False, "Instance type is required"
    # num_nodes will be validated server side

    if not identity_file:
        return False, "SSH public key path is required"

    # Resolve path and read key
    ssh_key_path = os.path.expanduser(identity_file)
    if not os.path.exists(ssh_key_path):
        return False, f"SSH key file not found: {ssh_key_path}"

    try:
        with open(ssh_key_path, "r") as f:
            ssh_key_content = f.read().strip()
    except Exception as e:
        return False, f"Failed to read SSH key: {e}"

    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "instance_type": instance_type,
        "public_keys": [ssh_key_content],
        "num_nodes": num_nodes,
    }

    if name:
        payload["tp_cluster_name"] = name

    response = requests.post(
        f"{ENGINE}/cluster/create",
        json=payload,
        headers=headers,
        stream=True,
        timeout=None,  # No timeout for SSE
    )

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("message")
        except Exception:
            error_msg = f"HTTP {response.status_code}"

        if error_msg:
            return False, error_msg
        else:
            return (
                False,
                f"Failed to create cluster. Response status code: {response.status_code}",
            )

    # Process SSE stream with spinner
    final_message = None
    status = None

    with Spinner("Creating cluster...") as spinner:
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])  # Remove "data: " prefix
                    status = data.get("status")
                    interm_message = data.get("message")

                    if interm_message:
                        spinner.update_text(interm_message)

                    # Break on completion
                    if status in ["success", "error"]:
                        final_message = data.get("final_message", data.get("message"))
                        break

                except json.JSONDecodeError:
                    spinner.update_text(f"JSONDecodeError - Received: {line}")

    if status == "success":
        return True, final_message
    else:
        return False, final_message


def cluster_destroy(cluster_id: str) -> Tuple[bool, str]:
    """
    Destroy a cluster (cluster command)
    Args:
        cluster_id: The ID of the cluster to destroy
    Returns:
        A tuple containing a boolean indicating success and a message
    """

    api_key = get_tensorpool_key()
    if not api_key:
        return False, "TENSORPOOL_KEY not found. Please set your API key."

    print(f"Preparing to destroy cluster: {cluster_id}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    confirm = (
        input(f"Are you sure you want to destroy cluster {cluster_id}? (y/N): ")
        .strip()
        .lower()
    )
    if confirm not in ["yes", "y"]:
        return False, "Cluster destroy cancelled"

    destroy_payload = {"cluster_id": cluster_id}

    response = requests.post(
        f"{ENGINE}/cluster/destroy",
        json=destroy_payload,
        headers=headers,
        timeout=60,
    )

    try:
        res = response.json()
    except requests.exceptions.JSONDecodeError:
        return (
            False,
            f"Error decoding response, status code: {response.status_code}",
        )

    if response.status_code == 200:
        message = res.get("message", f"Cluster {cluster_id} destroyed")

        return True, message
    else:
        message = res.get(
            "message", f"Failed to destroy cluster. Status code: {response.status_code}"
        )
        return False, message


def cluster_list(org: bool = False) -> Tuple[bool, str]:
    """
    List clusters - either user's clusters or all org clusters
    Args:
        org: If True, list all clusters in the user's organization
    Returns:
        A tuple containing a boolean indicating success and a message
    """
    api_key = get_tensorpool_key()
    if not api_key:
        return False, "TENSORPOOL_KEY not found. Please set your API key."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Add org parameter to request
    params = {"org": org} if org else {}

    response = requests.get(
        f"{ENGINE}/cluster/list",
        params=params,
        headers=headers,
        timeout=30,
    )

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        return (
            False,
            f"Failed to decode server response. Status code: {response.status_code}",
        )

    if response.status_code != 200:
        error_msg = result.get(
            "message", f"Error listing clusters. Status code {response.status_code}"
        )
        if result:
            error_msg += f"\n{result}"
        return False, error_msg

    message = result.get("message")

    return True, message


def ssh_to_instance(
    instance_id: str, ssh_args: Optional[List[str]] = None
) -> Tuple[bool, str]:
    """
    Get SSH command for an instance
    Args:
        instance_id: The ID of the instance to SSH into
        ssh_args: Additional SSH arguments to pass through
    Returns:
        A tuple containing a boolean indicating success and a message
    """
    if not instance_id:
        return False, "Instance ID is required"

    api_key = get_tensorpool_key()
    if not api_key:
        return False, "TENSORPOOL_KEY not found. Please set your API key."

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.get(
            f"{ENGINE}/ssh/{instance_id}",
            headers=headers,
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        return False, f"Failed to get SSH command: {str(e)}"

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        return False, f"Malformed server response. Status code: {response.status_code}"

    if response.status_code != 200:
        message = result.get(
            "message",
            f"Error fetching instance information. Status code: {response.status_code}\nRun `tp cluster list` to find the instance info",
        )
        return False, message

    command = result.get("command")
    message = result.get("message")

    if message:
        print(message)

    if command:
        # Execute the SSH command interactively
        try:
            # Append additional SSH arguments if provided
            if ssh_args:
                # Join the additional arguments into a single string
                additional_args = " ".join(ssh_args)
                full_command = f"{command} {additional_args}"
            else:
                full_command = command

            subprocess.run(full_command, shell=True)
            return True, ""
        except KeyboardInterrupt:
            return True, "\nSSH session terminated"
        except Exception as e:
            return False, f"Failed to execute SSH command: {str(e)}"
    else:
        return False, "ssh response not received from server"


def ssh_key_prechecks() -> Tuple[bool, str, str]:
    """
    Check if SSH keys named 'tensorpool' exist, prompt user to create if missing.
    Returns:
        A tuple containing (success, public_key_path, private_key_path)
    """
    unexpepanded_priv_key_path = "~/.ssh/tensorpool"
    private_key_path = os.path.expanduser(unexpepanded_priv_key_path)
    public_key_path = os.path.expanduser(unexpepanded_priv_key_path + ".pub")

    # Check if both keys exist
    private_exists = os.path.exists(private_key_path)
    public_exists = os.path.exists(public_key_path)

    if private_exists and public_exists:
        return True, public_key_path, private_key_path

    # Keys are missing, prompt user
    print(f"TensorPool SSH key pair not found at {unexpepanded_priv_key_path}{{,.pub}}")
    print(
        "This ssh key pair is used to directly interact with your instances"
    )  # needed to start jobs
    print("Options:")
    print(f"1. Create a new SSH key pair at {unexpepanded_priv_key_path}{{,.pub}}")
    print(
        f"2. Symlink an existing SSH key pair to {unexpepanded_priv_key_path}{{,.pub}}"
    )
    print("3. Cancel")

    choice = input("Choose an option (1/2/3): ").strip()

    if choice == "1":
        # Create new SSH key pair
        try:
            # Ensure .ssh directory exists
            ssh_dir = os.path.expanduser("~/.ssh")
            os.makedirs(ssh_dir, exist_ok=True)

            # Generate SSH key pair
            cmd = [
                "ssh-keygen",
                "-t",
                "ed25519",
                "-f",
                private_key_path,
                # "-N",
                # "",  # No passphrase
                # "-C",
                # "tensorpool-key",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print("SSH key pair created:")
                print(f"  Private key: {private_key_path}")
                print(f"  Public key: {public_key_path}")
                return True, public_key_path, private_key_path
            else:
                print(f"Failed to create SSH key: {result.stderr}")
                return False, "", ""

        except Exception as e:
            print(f"Error creating SSH key: {str(e)}")
            return False, "", ""

    elif choice == "2":
        # Symlink existing key
        existing_key = (
            input("Enter path to a private key: ").strip().strip('"').strip("'")
        )
        existing_key = os.path.expanduser(existing_key)

        if not os.path.exists(existing_key):
            print(f"Private key not found: {existing_key}")
            return False, "", ""

        # Determine public key path
        existing_pub_key = f"{existing_key}.pub"
        if not os.path.exists(existing_pub_key):
            print(f"Public key not found: {existing_pub_key}")
            return False, "", ""

        try:
            # Create symlinks
            if os.path.exists(private_key_path) or os.path.islink(private_key_path):
                os.remove(private_key_path)
            if os.path.exists(public_key_path) or os.path.islink(public_key_path):
                os.remove(public_key_path)

            os.symlink(existing_key, private_key_path)
            os.symlink(existing_pub_key, public_key_path)

            print("SSH keys symlinked:")
            print(f"  {existing_key} -> {private_key_path}")
            print(f"  {existing_pub_key} -> {public_key_path}")
            return True, public_key_path, private_key_path

        except Exception as e:
            print(f"Error creating symlinks: {str(e)}")
            return False, "", ""

    else:
        print("Operation cancelled.")
        return False, "", ""


def fetch_user_info() -> Tuple[bool, str]:
    """
    Fetch current user information from the engine
    Returns:
        A tuple containing a boolean indicating success and a message
    """
    api_key = get_tensorpool_key()
    if not api_key:
        return False, "TENSORPOOL_KEY not found. Please set your API key."

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.get(
            f"{ENGINE}/me/",
            headers=headers,
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        return False, f"Failed to fetch user info: {str(e)}"

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        return False, f"Malformed server response. Status code: {response.status_code}"

    if response.status_code != 200:
        message = result.get(
            "message",
            f"Error fetching user information. Status code: {response.status_code}",
        )
        return False, message

    message = result.get("message", "")
    return True, message
