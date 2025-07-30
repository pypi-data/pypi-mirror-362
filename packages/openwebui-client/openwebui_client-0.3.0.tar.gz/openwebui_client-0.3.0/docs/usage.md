# Usage

## Configuration

The OpenWebUI client can be configured using environment variables or by passing parameters directly to the client constructor.

### Environment Variables

* `OPENWEBUI_API_KEY`: Your OpenWebUI API key
* `OPENWEBUI_API_BASE`: Base URL for your OpenWebUI instance (default: http://localhost:5000)

### Direct Configuration

```python
from openwebui_client import OpenWebUIClient

client = OpenWebUIClient(
    api_key="your-openwebui-api-key",
    base_url="http://localhost:5000",
    default_model="gpt-4"
)
```

## Basic Usage

### Chat Completions

Create a simple chat completion:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is OpenWebUI?"}
    ]
)
print(response.choices[0].message.content)
```

### Chat Completions with Files

Include files with your chat completions:

```python
with open("document.pdf", "rb") as f:
    file_content = f.read()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the attached document."}
    ],
    files=[file_content]
)
print(response.choices[0].message.content)
```

## Models

### List Available Models

Retrieve a list of all available models in your OpenWebUI instance:

```python
# Get all available models
models = client.models.list()

# Print model information
for model in models:
    print(f"ID: {model.id}, Name: {model.name or model.id}")
```

### Access Model Properties

Each model has several properties you can access:

```python
# Get the first model
model = client.models.list()[0]

# Access model properties
print(f"Model ID: {model.id}")
print(f"Model Name: {model.name}")
print(f"Created: {model.created}")
print(f"Owner: {model.owned_by}")
```

See the [Models API documentation](api/models.md) for more details.

## File Management

### Upload a Single File

```python
with open("document.pdf", "rb") as f:
    file_content = f.read()

file_obj = client.files.create(
    file=file_content,
    file_metadata={"purpose": "assistants"}
)
print(f"File uploaded with ID: {file_obj.id}")
```

### Upload Multiple Files

```python
file_objects = client.files.create(
    files=[
        (file_content1, {"purpose": "assistants"}),
        (file_content2, {"purpose": "assistants"})
    ]
)
print(f"Uploaded {len(file_objects)} files")
```
