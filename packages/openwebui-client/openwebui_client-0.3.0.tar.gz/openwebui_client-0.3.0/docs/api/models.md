# Models

The OpenWebUI client provides access to the models available in your OpenWebUI instance through the `models` property of the client.

## Listing Models

You can list all available models using the `list()` method:

```python
from openwebui_client import OpenWebUIClient

client = OpenWebUIClient(
    api_key="your-api-key",
    base_url="https://your-openwebui-instance.com"
)

# List all available models
models = client.models.list()

# Print model information
for model in models:
    print(f"ID: {model.id}, Name: {model.name}, Owner: {model.owned_by}")
```

## Model Object

The `OpenWebUIModel` object has the following properties:

- `id` (str): The unique identifier for the model
- `name` (Optional[str]): Human-readable name of the model (may be None)
- `created` (int): Unix timestamp for when the model was created
- `object` (str): Always "model"
- `owned_by` (str): Organization that owns the model

## Implementation Notes

The OpenWebUI client extends the OpenAI client's Models class to handle the different response format from OpenWebUI's API. The models endpoint in OpenWebUI is located at `/models` rather than `/v1/models` as in the OpenAI API.

The client automatically adds the appropriate headers to ensure JSON responses from the API.
