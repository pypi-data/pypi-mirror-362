# Weni Data Lake SDK

The Weni Data Lake SDK is a Python library that provides an interface to interact with Weni's data lake services. It supports operations for sending data, managing message templates, and handling traces.

## Installation

```bash
pip install weni-datalake-sdk
In case you are using poetry, you can add the package to your project with the following command:
poetry add weni-datalake-sdk
```

## Environment Variables

To insert data into the data lake, you need to set the following environment variables:

```bash
DATALAKE_SERVER_ADDRESS=your_server_address
```

To get data from the data lake, you need to set the following environment variables:

```bash
REDSHIFT_QUERY_BASE_URL=your_redshift_url
REDSHIFT_SECRET=your_secret
REDSHIFT_ROLE_ARN=your_role_arn
MESSAGE_TEMPLATES_METRIC_NAME=your_metric_name (if you want to get message templates)
TRACES_METRIC_NAME=your_trace_metric_name (if you want to get traces)
EVENTS_METRIC_NAME=your_event_metric_name (if you want to get events)
```

Although you will need some AWS credentials to get data from the data lake, you can use the following environment variables:

```bash
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_DEFAULT_REGION=your_region
```

This is important that we will use assumed role to get data from the data lake.

## Usage Examples

### 1. Sending Data

```python
from weni_datalake_sdk.clients.client import send_data
from weni_datalake_sdk.paths.your_path import YourPath

# Prepare your data
data = {
    "field1": "value1",
    "field2": "value2"
}

# Send data using a path class
send_data(YourPath, data)

# Or using an instantiated path
path = YourPath()
send_data(path, data)
```

### 2. Send Event Data

```python
from weni_datalake_sdk.clients.client import send_event_data
from weni_datalake_sdk.paths.events_path import EventPath

# Prepare your data
data = {
    "event_name": "event_name",
    "key": "key",
    "value": "value",
    "value_type": "value_type",
    "date": "2021-01-01",
    "project": "project_uuid",
    "contact_urn": "contact_urn",
    "metadata": {
        "field1": "value1",
        "field2": "value2"
    }
}
```

### 2. Get Message Templates

```python
from weni_datalake_sdk.clients.redshift.message_templates import get_message_templates

# Get templates with specific parameters
result = get_message_templates(
    contact_urn="contact123",
    template_uuid="template_uuid"
)

```

### 3. Get Traces

```python
from weni_datalake_sdk.clients.redshift.traces import get_traces

# Get traces with query parameters
result = get_traces(
    query_params={
        "message_uuid": "123e4567-e89b-12d3-a456-426614174000"
    }
)
```

### 4. Get Events

```python
from weni_datalake_sdk.clients.redshift.events import get_events    

# Get events with query parameters
result = get_events(
    query_params={
        "date_start": "2021-01-01", # date_start is required
        "date_end": "2021-01-01", # date_end is required
        "project": "project_uuid", # project is optional
        "event_type": "event_type", # event_type is optional
        "contact_urn": "contact_urn", # contact_urn is optional
        "event_name": "event_name", # event_name is optional
        "key": "key", # key is optional
        "value": "value", # value is optional
        "value_type": "value_type" # value_type is optional
    }
)
```

## Error Handling

The SDK includes proper error handling. Always wrap your calls in try-except blocks:

```python
try:
    result = get_message_templates(template_id="template123")
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Environment Variables**: Always ensure all required environment variables are set before using the SDK.
2. **Path Validation**: Use proper path classes instead of raw strings.
3. **Error Handling**: Implement proper error handling in your code.
4. **Data Types**: Ensure you're passing the correct data types for each parameter.
5. **Security**: Never hardcode sensitive information like tokens or credentials.

## Common Issues and Solutions

1. **Connection Issues**
   - Ensure `DATALAKE_SERVER_ADDRESS` is correct and accessible
   - Check your network connectivity

2. **Authentication Errors**
   - Verify your AWS credentials are properly configured
   - Check if `REDSHIFT_SECRET` and `REDSHIFT_ROLE_ARN` are correct

3. **Missing Environment Variables**
   - Double-check all required environment variables are set
   - Use a `.env` file for local development

## Contributing

For contributing to this SDK, please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
