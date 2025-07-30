import json
from unittest.mock import Mock, patch

import pytest
from tornado.httpclient import HTTPClientError

from sagemaker_jupyter_server_extension.workflow_handler import (
    SageMakerWorkflowHandler,
    WorkflowLocalRunnerStatus,
)
from sagemaker_jupyter_server_extension.workflow_utils import ErrorMessage


async def test_get_local_runner_status(jp_fetch):
    mock_status = [
        {"timestamp": "2023-06-01 10:00:00.000+0000", "status": "healthy"},
        {"timestamp": "2023-06-01 11:00:00.000+0000", "status": "unhealthy"},
    ]
    with patch(
        "sagemaker_jupyter_server_extension.workflow_handler.from_json", return_value=mock_status
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_utils.os.path.exists", return_value=True
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.os.stat", return_value=Mock(st_size=1)
    ):
        response = await jp_fetch("api", "sagemaker", "workflows", "get-local-runner-status")
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"timestamp": "2023-06-01 11:00:00.000+0000", "status": "unhealthy"}


async def test_get_local_runner_status_empty_log(jp_fetch):
    mock_status = []
    with patch(
        "sagemaker_jupyter_server_extension.workflow_handler.from_json", return_value=mock_status
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_utils.os.path.exists", return_value=True
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.os.stat", return_value=Mock(st_size=1)
    ):
        response = await jp_fetch("api", "sagemaker", "workflows", "get-local-runner-status")
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result["status"] == "unhealthy"


async def test_get_local_runner_status_empty_file(jp_fetch):
    """
    Unlike test_get_local_runner_status_empty_log, this tests for the status file itself
    being empty (not even []).
    """
    with patch(
        "sagemaker_jupyter_server_extension.workflow_handler.os.stat", return_value=Mock(st_size=0)
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_utils.os.path.exists", return_value=True
    ), patch("sagemaker_jupyter_server_extension.workflow_handler.to_json") as mock_to_json:
        response = await jp_fetch("api", "sagemaker", "workflows", "get-local-runner-status")
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result["status"] == "unhealthy"
        assert result["detailed_status"] == ErrorMessage.STATUS_FILE_EMPTY
        mock_to_json.assert_called_once()


async def test_get_local_runner_status_file_not_found(jp_fetch):
    with patch(
        "sagemaker_jupyter_server_extension.workflow_utils.os.path.exists", return_value=False
    ):
        response = await jp_fetch("api", "sagemaker", "workflows", "get-local-runner-status")
        result = json.loads(response.body.decode())
        assert result["status"] == "unhealthy"
        assert result["detailed_status"] == ErrorMessage.STATUS_FILE_NOT_FOUND


async def test_update_local_runner_status(jp_fetch):
    mock_status = []
    with patch(
        "sagemaker_jupyter_server_extension.workflow_handler.from_json", return_value=mock_status
    ), patch("sagemaker_jupyter_server_extension.workflow_handler.to_json") as mock_to_json, patch(
        "sagemaker_jupyter_server_extension.workflow_utils.os.path.exists", return_value=True
    ):
        body = json.dumps(
            {
                "timestamp": "2023-06-01 12:00:00.000+0000",
                "status": WorkflowLocalRunnerStatus.HEALTHY.value,
            }
        )
        response = await jp_fetch(
            "api", "sagemaker", "workflows", "update-local-runner-status", method="POST", body=body
        )
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"success": "true"}
        mock_to_json.assert_called_once()


async def test_start_local_runner(jp_fetch):
    with patch("subprocess.Popen") as mock_popen, patch.object(
        SageMakerWorkflowHandler, "update_local_runner_status"
    ) as mock_update:
        response = await jp_fetch(
            "api", "sagemaker", "workflows", "start-local-runner", method="POST", body="{}"
        )
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"success": "true"}
        mock_update.assert_called_once()
        mock_popen.assert_called_once()


async def test_stop_local_runner(jp_fetch):
    with patch("subprocess.Popen") as mock_popen, patch.object(
        SageMakerWorkflowHandler, "update_local_runner_status"
    ) as mock_update:
        response = await jp_fetch(
            "api", "sagemaker", "workflows", "stop-local-runner", method="POST", body="{}"
        )
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"success": "true"}
        assert mock_update.call_count == 1
        mock_popen.assert_called_once()


async def test_deploy_project(jp_fetch):
    mock_metadata = {"AdditionalMetadata": {"ProjectS3Path": "s3://bucket/"}}
    with patch("builtins.open", create=True), patch("json.load", return_value=mock_metadata), patch(
        "boto3.Session"
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.hash_is_deployed", return_value=False
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.git_clone"
    ) as mock_git_clone, patch(
        "sagemaker_jupyter_server_extension.workflow_handler.upload_directory_to_s3"
    ) as mock_upload, patch(
        "sagemaker_jupyter_server_extension.workflow_handler.update_metadata"
    ) as mock_update_metadata, patch(
        "sagemaker_jupyter_server_extension.workflow_handler.remove_directory"
    ) as mock_remove, patch(
        "sagemaker_jupyter_server_extension.workflow_utils.from_s3_json"
    ), patch("sagemaker_jupyter_server_extension.workflow_utils.to_s3_json"), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.deploy_config_files"
    ) as mock_deploy_config:
        response = await jp_fetch(
            "api", "sagemaker", "workflows", "deploy-project", method="POST", body="{}"
        )
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"success": "true"}
        mock_git_clone.assert_called_once()
        mock_upload.assert_called_once()
        mock_deploy_config.assert_called_once()
        mock_update_metadata.assert_called_once()
        mock_remove.assert_called_once()


async def test_deploy_project_already_deployed(jp_fetch):
    mock_metadata = {"AdditionalMetadata": {"ProjectS3Path": "s3://bucket/"}}
    with patch("builtins.open", create=True), patch("json.load", return_value=mock_metadata), patch(
        "boto3.Session"
    ), patch(
        "sagemaker_jupyter_server_extension.workflow_handler.hash_is_deployed", return_value=True
    ), patch("sagemaker_jupyter_server_extension.workflow_utils.from_s3_json"), patch(
        "sagemaker_jupyter_server_extension.workflow_utils.to_s3_json"
    ):
        response = await jp_fetch(
            "api", "sagemaker", "workflows", "deploy-project", method="POST", body="{}"
        )
        assert response.code == 200
        result = json.loads(response.body.decode())
        assert result == {"success": "all project files have already been deployed"}


async def test_invalid_command(jp_fetch):
    with pytest.raises(HTTPClientError) as excinfo:
        await jp_fetch("api", "sagemaker", "workflows", "invalid-command")
    assert excinfo.value.code == 405
