import os

import grpc

from weni_datalake_sdk.clients import (
    events_pb2,
    events_pb2_grpc,
    message_templates_pb2,
    message_templates_pb2_grpc,
    msgs_pb2,
    msgs_pb2_grpc,
    traces_pb2,
    traces_pb2_grpc,
)
from weni_datalake_sdk.paths.validator import validate_path

SERVER_ADDRESS = os.environ.get("DATALAKE_SERVER_ADDRESS")


def send_data(path, data):
    channel = grpc.insecure_channel(target=SERVER_ADDRESS)
    stub = msgs_pb2_grpc.DatalakeManagerServiceStub(channel)

    if isinstance(path, type):
        path = path()

    validate_path(path)

    request = msgs_pb2.InsertRequest(path=path.get_table_name(), data=data)

    response = stub.InsertData(request)
    print("Server response:", response.status)


def send_trace_data(path_class, data):
    validate_path(path_class)

    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = traces_pb2_grpc.DatalakeManagerServiceStub(channel)

    request = traces_pb2.InsertTraceRequest(path=path_class.get_table_name(), data=data)

    response = stub.InsertTraceData(request)
    return response.status


def send_message_template_data(path_class, data):
    validate_path(path_class)

    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = message_templates_pb2_grpc.DatalakeManagerServiceStub(channel)

    request = message_templates_pb2.InsertMessageTemplateRequest(data=data)

    response = stub.InsertMessageTemplateData(request)
    return response.status


def send_message_template_status_data(path_class, data):
    validate_path(path_class)

    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = message_templates_pb2_grpc.DatalakeManagerServiceStub(channel)

    request = message_templates_pb2.InsertMessageTemplateStatusRequest(data=data)

    response = stub.InsertMessageTemplateStatusData(request)
    return response.status


def send_event_data(path_class, data):
    validate_path(path_class)

    from datetime import datetime

    from google.protobuf import struct_pb2, timestamp_pb2

    channel = grpc.insecure_channel(SERVER_ADDRESS)
    stub = events_pb2_grpc.DatalakeManagerServiceStub(channel)

    # Convert date to Timestamp
    timestamp = timestamp_pb2.Timestamp()
    if data.get("date"):
        try:
            dt = datetime.fromisoformat(data["date"].replace("Z", "+00:00"))
            timestamp.FromDatetime(dt)
        except Exception:
            timestamp.GetCurrentTime()
    else:
        timestamp.GetCurrentTime()

    # Create ValueData for the value
    value_data = events_pb2.ValueData()
    value_data.string_value = str(data.get("value", ""))

    # Create metadata struct
    metadata = None
    if data.get("metadata"):
        metadata = struct_pb2.Struct()
        metadata.update(data["metadata"])

    # Create request with individual fields as defined in proto
    request = events_pb2.InsertEventRequest(
        event_name=data.get("event_name", ""),
        key=data.get("key", ""),
        date=timestamp,
        project=data.get("project", ""),
        contact_urn=data.get("contact_urn", ""),
        value_type=events_pb2.VALUE_TYPE_STRING,
        value=value_data,
        metadata=metadata,
    )

    response = stub.InsertEventData(request)
    return response.status
