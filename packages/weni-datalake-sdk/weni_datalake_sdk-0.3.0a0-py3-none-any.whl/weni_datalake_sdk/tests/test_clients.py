from unittest import mock

import pytest
import requests_mock

from weni_datalake_sdk.clients.client import send_data, send_trace_data
from weni_datalake_sdk.clients.dl_manager_client import DLManagerClient
from weni_datalake_sdk.paths.msg_path import MsgPath
from weni_datalake_sdk.paths.trace_path import TracePath
from weni_datalake_sdk.utils.exceptions import DLManagerError

BASE_URL = "https://dl-manager.example.com/api"


@pytest.fixture
def client():
    return DLManagerClient(base_url=BASE_URL)


@pytest.fixture
def mock_grpc_stub_msgs():
    with mock.patch(
        "weni_datalake_sdk.clients.msgs_pb2_grpc.DatalakeManagerServiceStub"
    ) as mock_stub:
        yield mock_stub


@pytest.fixture
def mock_grpc_stub_traces():
    with mock.patch(
        "weni_datalake_sdk.clients.traces_pb2_grpc.DatalakeManagerServiceStub"
    ) as mock_stub:
        yield mock_stub


@pytest.fixture
def mock_grpc_channel():
    with mock.patch("grpc.insecure_channel") as mock_channel:
        yield mock_channel


def test_insert_data_success(client):
    with requests_mock.Mocker() as m:
        m.post(f"{BASE_URL}/messages/send", json={"status": "success"}, status_code=200)

        msg_instance = dict(
            project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", text="Oi!"
        )
        response = client.insert(MsgPath, msg_instance)
        assert response == {"status": "success"}


def test_insert_data_fail_dl_manager(client):
    with requests_mock.Mocker() as m:
        m.post(
            f"{BASE_URL}/messages/send",
            status_code=500,
            json={"error": "Internal Server Error"},
        )

        with pytest.raises(DLManagerError):
            client.insert(
                MsgPath,
                dict(project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", text="Oi!"),
            )


def test_insert_trace_data_success(client):
    with requests_mock.Mocker() as m:
        m.post(f"{BASE_URL}/traces/send", json={"status": "success"}, status_code=200)

        trace_instance = dict(
            project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", receive="Wow!"
        )
        response = client.insert(TracePath, trace_instance)
        assert response == {"status": "success"}


def test_insert_trace_data_fail_dl_manager(client):
    with requests_mock.Mocker() as m:
        m.post(
            f"{BASE_URL}/traces/send",
            status_code=500,
            json={"error": "Internal Server Error"},
        )

        with pytest.raises(DLManagerError):
            client.insert(
                TracePath,
                dict(project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", trace="Wow!"),
            )


def test_send_data_success(mock_grpc_stub_msgs, mock_grpc_channel):
    mock_stub_instance = mock_grpc_stub_msgs.return_value
    mock_stub_instance.InsertData.return_value.status = "success"

    msg_instance = dict(project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", text="Oi!")

    send_data(MsgPath, msg_instance)

    mock_stub_instance.InsertData.assert_called_once()


def test_send_trace_data_success(mock_grpc_stub_traces, mock_grpc_channel):
    mock_stub_instance = mock_grpc_stub_traces.return_value
    mock_stub_instance.InsertTraceData.return_value.status = "success"

    trace_instance = dict(
        project_uuid="68c84e84-2d7d-4dc7-8193-50d0e2321b2e", receive="Wow!"
    )

    send_trace_data(TracePath, trace_instance)

    mock_stub_instance.InsertTraceData.assert_called_once()
