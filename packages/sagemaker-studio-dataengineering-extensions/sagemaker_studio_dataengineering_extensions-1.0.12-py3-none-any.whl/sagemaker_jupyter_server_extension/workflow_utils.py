import json
import logging
import os
import shutil
import subprocess
from datetime import UTC, datetime
from enum import Enum
from functools import wraps
from pathlib import Path

from botocore.exceptions import ClientError
from tornado.web import HTTPError

WORKFLOW_LOCAL_RUNNER_STATUS_FILE = "/home/sagemaker-user/.workflows_setup/health/status.json"
PROJECT_SNAPSHOT_DIR = "/tmp/workflows_project_snapshot"
S3_METADATA_FILE = "/workflows/project-files-git-history.json"
S3_SNAPSHOT_DIR = "/workflows/project-files"
S3_CONFIG_DIR = "/workflows/config-files"

# format for timestamps stored in the local runner status file
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"


class StrEnum(str, Enum):
    def __str__(self):
        return str(self.value)

    def _generate_next_value_(self, *_):
        return self


class ErrorMessage(StrEnum):
    INVALID_REQUEST_API_NOT_FOUND = "Invalid request, API not found."
    INVALID_REQUEST_METHOD_NOT_SUPPORTED = "Invalid request, method not supported."
    FILE_NOT_FOUND = "The file '%s' does not exist. It may have been removed."
    INVALID_JSON = "The file is not valid JSON."
    S3_PATH_NOT_FOUND = "The S3 path for this project is not available."
    COMMAND_FAILED = "A command failed with the following error: %s"
    UNEXPECTED_ERROR = "An unexpected error occurred: %s"
    # TODO: edit this message to be more generic once we can use the post-startup status API to check for a specific error
    STATUS_FILE_NOT_FOUND = "Local workflows failed to start. This may happen when the VPC for the project is misconfigured. Ensure your VPC can access DataZone, then try again."
    STATUS_FILE_EMPTY = "The status file is empty."


class WorkflowLocalRunnerStatus(StrEnum):
    STARTING = "starting"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STOPPING = "stopping"
    STOPPED = "stopped"


def parse_datetime(datetime_str: str) -> datetime:
    """Backwards-compatible datetime parsing for timestamps without milliseconds."""
    if "." in datetime_str:
        return datetime.strptime(datetime_str, TIMESTAMP_FORMAT)
    else:
        return datetime.strptime(datetime_str, TIMESTAMP_FORMAT.replace(".%f", ""))


def check_file_exists(filename):
    """
    Checks if the specified file exists. If it does, runs the decorated function.
    FileNotFoundErrors are handled as 404.
    Other unhandled errors are handled as 500.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if not os.path.exists(filename):
                    raise FileNotFoundError
                return func(*args, **kwargs)
            except FileNotFoundError:
                raise HTTPError(404, ErrorMessage.FILE_NOT_FOUND % filename)
            except Exception as e:
                raise HTTPError(500, ErrorMessage.UNEXPECTED_ERROR % e)

        return wrapper

    return decorator


def check_object_exists(s3_client, bucket, key) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


def from_s3_json(s3_path, s3_client) -> dict | list:
    # Parse the S3 path to extract bucket and key
    parts = s3_path.replace("s3://", "").split("/")
    bucket = parts[0]
    key = "/".join(parts[1:])
    # Get the object from S3
    if not check_object_exists(s3_client, bucket, key):
        return {}
    response = s3_client.get_object(Bucket=bucket, Key=key)
    # Read the content of the file
    file_content = response["Body"].read().decode("utf-8")
    # Parse the JSON content
    json_content = json.loads(file_content)
    return json_content


def to_s3_json(data, s3_path, s3_client):
    # Parse the S3 path to extract bucket and key
    parts = s3_path.replace("s3://", "").split("/")
    bucket = parts[0]
    key = "/".join(parts[1:])
    # Convert the data to JSON string
    json_data = json.dumps(data, indent=2)
    # Upload the JSON string to S3
    s3_client.put_object(Bucket=bucket, Key=key, Body=json_data, ContentType="application/json")


def from_json(file_path: str) -> dict | list:
    """Gets contents of JSON file as dict."""
    try:
        with open(file_path) as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise ValueError(ErrorMessage.INVALID_JSON)


def to_json(contents: dict | list, file_path: str):
    """Saves contents of `contents` to `file_path`. Overwrites contents of file if it exists."""
    with open(file_path, "w") as file:
        file.write(json.dumps(contents))


def get_project_s3_path() -> str:
    with open("/opt/ml/metadata/resource-metadata.json") as metadata_file:
        project_s3_path = (
            json.load(metadata_file).get("AdditionalMetadata", {}).get("ProjectS3Path")
        )
        if not project_s3_path:
            raise HTTPError(404, ErrorMessage.S3_PATH_NOT_FOUND)
        return project_s3_path


def get_git_hash(_dir: str, branch: str) -> str:
    """Retrieve git hash of HEAD commit for repository at `_dir` and branch `branch`."""
    try:
        return (
            subprocess.run(
                ["/usr/bin/git", "-C", _dir, "ls-remote", "origin", branch],
                capture_output=True,
                check=True,
                text=True,
            )
            .stdout.strip()
            .split("\t")[0]
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"[GET_GIT_HASH] Failed to retrieve git hash of {branch} at {_dir}: {e!s}"
        )


def hash_is_deployed(metadata_file_path, s3_client) -> bool:
    """Checks if the HEAD of the project repository has already been deployed to S3."""
    git_hash = get_git_hash("/home/sagemaker-user/src", "HEAD")
    metadata = from_s3_json(metadata_file_path, s3_client)
    return True if metadata and (git_hash in metadata) else False


def git_clone(target_dir_path: str):
    """Clones project repository into a target directory."""
    try:
        subprocess.run(["/bin/bash", "/etc/sagemaker-ui/git_clone.sh", target_dir_path], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"[GIT_CLONE] Failed to clone git repo to {target_dir_path}: {e!s}")


def upload_directory_to_s3(source_dir_path: str, s3_path: str):
    """Syncs a whole directory to S3."""
    try:
        subprocess.run(
            ["/usr/local/bin/aws", "s3", "sync", source_dir_path, s3_path, "--delete"],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "[UPLOAD_TO_S3] Failed to sync directory repo "
            + f"at {source_dir_path} to {s3_path}: {e!s}"
        )


def _copy_with_prepend(src: str, dst: str) -> str:
    """
    Copy file object at `src` into `dst`, but prepend `src` before `dst` if `dst` exists.
    """
    if os.path.exists(src):
        if os.path.exists(dst) and os.stat(dst).st_size > 0:
            with open(dst) as dst_file:
                # for shell scripts, ignore the first line
                if Path(src).suffix == ".sh":
                    dst_file.readline()
                dst_content = dst_file.read()
            with open(dst, "w") as dst_file:
                with open(src) as src_file:
                    dst_file.write(src_file.read())
                dst_file.write("\n")
                dst_file.write(dst_content)
        else:
            shutil.copy2(src, dst)
    return dst


def deploy_config_files(
    config_s3_path,
    snapshot_dir=PROJECT_SNAPSHOT_DIR,
    system_config_src="/etc/sagemaker-ui/workflows",
):
    """
    Deploys config files to the config files folder in S3.
    Assumes git HEAD is already cloned to `dir`. Roughly, this does the following:
        1. Appends dependencies and startup commands from /etc/sagemaker-ui/workflows
        to customer's requirements/startup files (to snapshot dir)
        2. Merges plugins in /etc/sagemaker-ui/workflows with customer's plugins (to snapshot dir)
        3. Uploads requirements and startup file from snapshot dir to S3
        4. Zips plugins folder from snapshot dir and Uploads to S3
    """
    config_folder_in_snapshot = "workflows/config"
    reqs_in_snapshot = os.path.join(snapshot_dir, config_folder_in_snapshot, "requirements.txt")
    startup_in_snapshot = os.path.join(snapshot_dir, config_folder_in_snapshot, "startup.sh")
    plugins_folder_in_snapshot = os.path.join(snapshot_dir, config_folder_in_snapshot, "plugins")
    try:
        # Create config folder in snapshot if it doesn't already exist
        os.makedirs(plugins_folder_in_snapshot, exist_ok=True)
        # Copy and merge requirements
        _copy_with_prepend(
            os.path.join(system_config_src, "requirements", "requirements.txt"),
            reqs_in_snapshot,
        )
        # Copy and merge startup script
        _copy_with_prepend(
            os.path.join(system_config_src, "startup", "startup.sh"),
            startup_in_snapshot,
        )
        # Copy and merge plugins
        shutil.copytree(
            os.path.join(system_config_src, "plugins"),
            plugins_folder_in_snapshot,
            dirs_exist_ok=True,
        )
        # For plugins, we also need to create a .zip and upload that
        shutil.make_archive(plugins_folder_in_snapshot, "zip", plugins_folder_in_snapshot)
        remove_directory(plugins_folder_in_snapshot)
    except Exception as e:
        raise RuntimeError(
            f"[COPY_FILES] Failed to copy user's config files to {snapshot_dir}: {e!s}"
        )
    upload_directory_to_s3(os.path.join(snapshot_dir, config_folder_in_snapshot), config_s3_path)


def update_metadata(operation, _dir, metadata_file_path, s3_client):
    """
    Takes a git-initialized directory and updates its hash in the file
    specified in `metadata_file_path` (assumed to be an S3 path).
    """
    git_hash = get_git_hash(_dir, "HEAD")
    metadata = from_s3_json(metadata_file_path, s3_client)
    match operation:
        case "insert":
            metadata[git_hash] = {
                "timestamp": datetime.now(UTC).strftime(TIMESTAMP_FORMAT),
                "user": os.getenv("LOGNAME", None),
            }
        case "delete":
            metadata.pop(git_hash, None)
        case _:
            raise ValueError("Unsupported operation")
    to_s3_json(metadata, metadata_file_path, s3_client)


def remove_directory(dir_path: str):
    """Removes a directory."""
    if dir_path != "/" and dir_path.startswith("/"):
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
            except Exception as e:
                raise RuntimeError(
                    f"[REMOVE_DIRECTORY] Failed to remove directory at {dir_path}: {e!s}"
                )
        else:
            logging.info(f"{dir_path} doesn't exist")
            return
    else:
        raise ValueError("Cannot remove root or relative paths for stability.")
