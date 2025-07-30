import json
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch

import boto3
import pytest

# Import the functions you want to test
from sagemaker_jupyter_server_extension.workflow_utils import (
    _copy_with_prepend,
    deploy_config_files,
    from_json,
    from_s3_json,
    git_clone,
    hash_is_deployed,
    parse_datetime,
    remove_directory,
    to_json,
    to_s3_json,
    update_metadata,
    upload_directory_to_s3,
)

# Constants
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


@pytest.mark.parametrize(
    "datetime_str", ["2024-10-31 15:35:50+0000", "2024-10-31 15:35:50.500+0000"]
)
def test_parse_datetime(datetime_str):
    # Test parsing completes with no ValueError
    assert str(type(parse_datetime(datetime_str))) == "<class 'datetime.datetime'>"


@pytest.fixture
def mock_s3_client():
    return Mock(spec=boto3.client("s3"))


def test_from_s3_json(mock_s3_client):
    mock_s3_client.get_object.return_value = {
        "Body": Mock(read=lambda: json.dumps({"key": "value"}).encode("utf-8"))
    }
    result = from_s3_json("s3://bucket/key.json", mock_s3_client)
    assert result == {"key": "value"}
    mock_s3_client.get_object.assert_called_once_with(Bucket="bucket", Key="key.json")


def test_to_s3_json(mock_s3_client):
    data = {"key": "value"}
    to_s3_json(data, "s3://bucket/key.json", mock_s3_client)
    mock_s3_client.put_object.assert_called_once_with(
        Bucket="bucket",
        Key="key.json",
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
    )


@pytest.fixture
def temp_json_file(tmp_path):
    file = tmp_path / "test.json"
    file.write_text('{"key": "value"}')
    return str(file)


def test_from_json(temp_json_file):
    result = from_json(temp_json_file)
    assert result == {"key": "value"}


def test_to_json(tmp_path):
    file_path = str(tmp_path / "output.json")
    contents = {"key": "value"}
    to_json(contents, file_path)
    with open(file_path) as f:
        assert json.load(f) == contents


@patch("sagemaker_jupyter_server_extension.workflow_utils.subprocess.run")
@patch("sagemaker_jupyter_server_extension.workflow_utils.from_s3_json")
def test_hash_is_deployed(mock_from_s3_json, mock_subprocess_run, mock_s3_client):
    # Set up the mock for subprocess.run
    mock_subprocess_run.return_value = Mock(stdout="test_hash\n")

    # Test case: hash is in metadata
    mock_from_s3_json.return_value = {"test_hash": {}}
    assert hash_is_deployed("s3://bucket/metadata.json", mock_s3_client)

    # Test case: hash is not in metadata
    mock_from_s3_json.return_value = {"other_hash": {}}
    assert not hash_is_deployed("s3://bucket/metadata.json", mock_s3_client)

    # Verify subprocess.run was called correctly
    mock_subprocess_run.assert_called_with(
        ["/usr/bin/git", "-C", "/home/sagemaker-user/src", "ls-remote", "origin", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    )

    # Test case: subprocess.run raises CalledProcessError
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "cmd", "output")
    with pytest.raises(RuntimeError) as excinfo:
        hash_is_deployed("s3://bucket/metadata.json", mock_s3_client)
    assert "[GET_GIT_HASH] Failed to retrieve git hash of HEAD at /home/sagemaker-user/src" in str(
        excinfo.value
    )


@patch("subprocess.run")
def test_git_clone(mock_run):
    git_clone("/target/dir")
    mock_run.assert_called_once_with(
        ["/bin/bash", "/etc/sagemaker-ui/git_clone.sh", "/target/dir"], check=True
    )


@patch("subprocess.run")
def test_upload_directory_to_s3(mock_run):
    upload_directory_to_s3("/source/dir", "s3://bucket/key")
    mock_run.assert_called_once_with(
        ["/usr/local/bin/aws", "s3", "sync", "/source/dir", "s3://bucket/key", "--delete"],
        check=True,
    )


@patch("sagemaker_jupyter_server_extension.workflow_utils.from_s3_json")
@patch("sagemaker_jupyter_server_extension.workflow_utils.to_s3_json")
@patch("subprocess.run")
@patch("os.getenv", return_value="test-user")
def test_update_metadata(mock_getenv, mock_run, mock_to_s3_json, mock_from_s3_json, mock_s3_client):
    mock_run.return_value.stdout = "test_hash"
    mock_from_s3_json.return_value = {}

    update_metadata("insert", "/repo/dir", "s3://bucket/metadata.json", mock_s3_client)

    mock_run.assert_called_once_with(
        ["/usr/bin/git", "-C", "/repo/dir", "ls-remote", "origin", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert mock_to_s3_json.call_args[0][0]["test_hash"]["timestamp"]
    assert mock_to_s3_json.call_args[0][0]["test_hash"]["user"] == "test-user"
    mock_to_s3_json.assert_called_once()


@patch("sagemaker_jupyter_server_extension.workflow_utils.from_s3_json")
@patch("sagemaker_jupyter_server_extension.workflow_utils.to_s3_json")
@patch("subprocess.run")
@patch("os.getenv", return_value=None)
def test_update_metadata_no_user(
    mock_getenv,
    mock_run,
    mock_to_s3_json,
    mock_from_s3_json,
    mock_s3_client,
):
    """Gracefully handle case where the LOGNAME env variable is not set"""

    mock_run.return_value.stdout = "test_hash"
    mock_from_s3_json.return_value = {}

    update_metadata("insert", "/repo/dir", "s3://bucket/metadata.json", mock_s3_client)

    mock_run.assert_called_once_with(
        ["/usr/bin/git", "-C", "/repo/dir", "ls-remote", "origin", "HEAD"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert mock_to_s3_json.call_args[0][0]["test_hash"]["timestamp"]
    assert mock_to_s3_json.call_args[0][0]["test_hash"]["user"] is None
    mock_to_s3_json.assert_called_once()


@patch("shutil.rmtree")
@patch("os.path.exists")
def test_remove_directory(mock_exists, mock_rmtree):
    mock_exists.return_value = True
    remove_directory("/test/dir")
    mock_rmtree.assert_called_once_with("/test/dir")

    with pytest.raises(ValueError):
        remove_directory("relative/path")

    with pytest.raises(ValueError):
        remove_directory("/")


def test__copy_with_prepend_empty_file():
    with tempfile.NamedTemporaryFile(delete=False) as src:
        src.write(b"This is a test.\n")
        src_path = src.name

    with tempfile.NamedTemporaryFile(delete=False) as dst:
        dst_path = dst.name

    _copy_with_prepend(src_path, dst_path)

    # Append content again
    _copy_with_prepend(src_path, dst_path)

    with open(dst_path, "rb") as f:
        data = f.read()

    assert data == b"This is a test.\n\nThis is a test.\n"

    # Clean up temp files
    os.remove(src_path)
    os.remove(dst_path)


def test__copy_with_prepend_create_new_file():
    with tempfile.NamedTemporaryFile(delete=False) as src:
        src.write(b"New file content")
        src_path = src.name
    # Nonexistent destination file path
    dst_path = tempfile.mktemp()

    _copy_with_prepend(src_path, dst_path)

    with open(dst_path, "rb") as f:
        data = f.read()

    assert data == b"New file content"

    # Clean up temp files
    os.remove(src_path)
    os.remove(dst_path)


def test__copy_with_prepend_non_empty_file():
    with tempfile.NamedTemporaryFile(delete=False) as src:
        src.write(b"Source file content")
        src_path = src.name

    with tempfile.NamedTemporaryFile(delete=False) as dst:
        dst.write(b"Destination file content")
        dst_path = dst.name

    _copy_with_prepend(src_path, dst_path)

    with open(dst_path, "rb") as f:
        data = f.read()

    assert data == b"Source file content\nDestination file content"

    os.remove(src_path)
    os.remove(dst_path)


class TestDeployConfigFiles(unittest.TestCase):
    def setUp(self):
        # Create temporary directories
        self.snapshot_dir = tempfile.mkdtemp()
        self.workflows_setup = tempfile.mkdtemp()

        # Create sample files in workflows_setup
        os.makedirs(os.path.join(self.workflows_setup, "requirements"))
        with open(os.path.join(self.workflows_setup, "requirements", "requirements.txt"), "w") as f:
            f.write("workflows requirement")
        # We're no longer specifying a startup script, so don't set one up
        os.makedirs(os.path.join(self.workflows_setup, "plugins"))
        with open(os.path.join(self.workflows_setup, "plugins", "workflows_plugin.py"), "w") as f:
            f.write("print('Workflows plugin')")

        self.config_folder_in_snapshot = os.path.join(self.snapshot_dir, "workflows", "config")

        self.config_s3_path = "s3://bucket/config/"
        self.s3_client = Mock(spec=boto3.client("s3"))

    def create_all_user_config_files(self):
        """(Happy path) Creates all config files for user in project snapshot."""
        # Create sample directory structure in snapshot_dir
        os.makedirs(self.config_folder_in_snapshot)
        os.makedirs(os.path.join(self.config_folder_in_snapshot, "plugins"))

        # Create sample files in snapshot_dir
        with open(os.path.join(self.config_folder_in_snapshot, "requirements.txt"), "w") as f:
            f.write("customer requirement\n")
        with open(os.path.join(self.config_folder_in_snapshot, "startup.sh"), "w") as f:
            f.write("#!/bin/sh\necho 'Customer startup'\n")
        with open(
            os.path.join(self.config_folder_in_snapshot, "plugins", "customer_plugin.py"), "w"
        ) as f:
            f.write("print('Customer plugin')")

    def create_only_requirements_file(self):
        """Only create a requirements.txt file in the user's project snapshot."""
        # Create sample directory structure in snapshot_dir
        os.makedirs(self.config_folder_in_snapshot)
        with open(os.path.join(self.config_folder_in_snapshot, "requirements.txt"), "w") as f:
            f.write("customer requirement\n")

    def create_no_config_files(self):
        """
        Don't create any config files in the user's project snapshot.
        Just create a single dag in the dags folder.
        """
        self.dags_folder_in_snapshot = os.path.join(self.snapshot_dir, "workflows", "dags")
        os.makedirs(self.dags_folder_in_snapshot)

        # Add a sample dag
        with open(os.path.join(self.dags_folder_in_snapshot, "sample_dag.py"), "w") as f:
            f.write("print('hello world!')")

    def tearDown(self):
        # Clean up temporary directories
        shutil.rmtree(self.snapshot_dir)
        shutil.rmtree(self.workflows_setup)

    @patch("sagemaker_jupyter_server_extension.workflow_utils.upload_directory_to_s3")
    @patch("sagemaker_jupyter_server_extension.workflow_utils.remove_directory")
    def test_deploy_config_files(self, mock_remove_directory, mock_upload):
        self.create_all_user_config_files()

        deploy_config_files(
            config_s3_path=self.config_s3_path,
            snapshot_dir=self.snapshot_dir,
            system_config_src=self.workflows_setup,
        )

        # Check if files were merged correctly
        with open(os.path.join(self.config_folder_in_snapshot, "requirements.txt")) as f:
            # Workflows requirements need to come before startup requirements
            self.assertEqual(f.read(), "workflows requirement\ncustomer requirement\n")
        with open(os.path.join(self.config_folder_in_snapshot, "startup.sh")) as f:
            self.assertEqual(
                f.read(),
                "#!/bin/sh\necho 'Customer startup'\n",
            )
        # Check if plugins.zip was created
        self.assertTrue(os.path.exists(os.path.join(self.config_folder_in_snapshot, "plugins.zip")))

        # Check if plugins folder was removed
        mock_remove_directory.assert_called_once_with(
            os.path.join(self.config_folder_in_snapshot, "plugins")
        )

        # Check if upload_directory_to_s3 was called with correct arguments
        mock_upload.assert_called_once_with(self.config_folder_in_snapshot, self.config_s3_path)

    @patch("sagemaker_jupyter_server_extension.workflow_utils.upload_directory_to_s3")
    @patch("sagemaker_jupyter_server_extension.workflow_utils.remove_directory")
    def test_deploy_missing_config_folder(self, mock_remove_directory, mock_upload):
        """When user is missing the config folder, only upload system-specified contents."""
        self.create_no_config_files()

        deploy_config_files(
            snapshot_dir=self.snapshot_dir,
            config_s3_path=self.config_s3_path,
            system_config_src=self.workflows_setup,
        )

        # Check that we only have system-specified contents in s3
        with open(os.path.join(self.config_folder_in_snapshot, "requirements.txt")) as f:
            # Should only contain workflows requirements
            self.assertEqual(f.read(), "workflows requirement")
        # Check if plugins.zip was created
        self.assertTrue(os.path.exists(os.path.join(self.config_folder_in_snapshot, "plugins.zip")))

        # Check if plugins folder was removed
        mock_remove_directory.assert_called_once_with(
            os.path.join(self.config_folder_in_snapshot, "plugins")
        )

        # Check if upload_directory_to_s3 was called with correct arguments
        mock_upload.assert_called_once_with(self.config_folder_in_snapshot, self.config_s3_path)

    @patch("sagemaker_jupyter_server_extension.workflow_utils.upload_directory_to_s3")
    @patch("sagemaker_jupyter_server_extension.workflow_utils.remove_directory")
    def test_deploy_missing_config_files(self, mock_remove_directory, mock_upload):
        """
        When user specifies only 1/3 of the config files, ensure we're uploading the others, too
        so that we don't lose any system-specified contents.
        """
        self.create_only_requirements_file()

        deploy_config_files(
            snapshot_dir=self.snapshot_dir,
            config_s3_path=self.config_s3_path,
            system_config_src=self.workflows_setup,
        )

        # Check that we only have system-specified contents in s3
        with open(os.path.join(self.config_folder_in_snapshot, "requirements.txt")) as f:
            # Should only contain workflows requirements
            self.assertEqual(f.read(), "workflows requirement\ncustomer requirement\n")
        # Check if plugins.zip was created
        self.assertTrue(os.path.exists(os.path.join(self.config_folder_in_snapshot, "plugins.zip")))
        # Check that no startup script exists (because customer didn't specify one)
        self.assertFalse(os.path.exists(os.path.join(self.config_folder_in_snapshot, "startup.sh")))

        # Check if plugins folder was removed
        mock_remove_directory.assert_called_once_with(
            os.path.join(self.config_folder_in_snapshot, "plugins")
        )

        # Check if upload_directory_to_s3 was called with correct arguments
        mock_upload.assert_called_once_with(self.config_folder_in_snapshot, self.config_s3_path)

    @patch("sagemaker_jupyter_server_extension.workflow_utils.upload_directory_to_s3")
    @patch(
        "sagemaker_jupyter_server_extension.workflow_utils._copy_with_prepend",
        side_effect=OSError(),
    )
    def test_deploy_config_files_copy_failure(self, mock_copy_with_prepend, mock_upload):
        self.create_only_requirements_file()

        with self.assertRaises(RuntimeError):
            deploy_config_files(
                snapshot_dir=self.snapshot_dir,
                config_s3_path=self.config_s3_path,
                system_config_src=self.workflows_setup,
            )

        # Check that upload_directory_to_s3 was not called
        mock_upload.assert_not_called()
