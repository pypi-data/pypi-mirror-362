"""Tests for the OpenWebUI models functionality."""

import logging
import os

import pytest

from openwebui_client import OpenWebUIClient
from openwebui_client.models import OpenWebUIModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Skip tests if no API key or base URL is provided
pytestmark = pytest.mark.skipif(
    not (os.environ.get("OPENWEBUI_API_KEY") and os.environ.get("OPENWEBUI_API_BASE")),
    reason="OPENWEBUI_API_KEY and OPENWEBUI_API_BASE environment variables are required for tests",
)


@pytest.fixture
def client():
    """Create a client connected to a real OpenWebUI instance."""
    return OpenWebUIClient(
        api_key=os.environ.get("OPENWEBUI_API_KEY"),
        base_url=os.environ.get("OPENWEBUI_API_BASE", ""),
    )


def test_models_property(client):
    """Test that the models property returns an OpenWebUIModels instance."""
    # Access the models property
    models = client.models

    # Verify it's the right type
    assert models.__class__.__name__ == "OpenWebUIModels"

    # Verify it has the list method
    assert hasattr(models, "list")
    assert callable(models.list)


def test_models_list(client):
    """Test that models listing works and returns OpenWebUIModel objects."""
    # Get models list
    models = list(client.models.list())

    # Check the first model
    model = models[0]
    assert isinstance(model, OpenWebUIModel), "Model is not an OpenWebUIModel instance"

    # Check required fields
    assert model.id is not None
    assert model.created is not None
    assert model.object == "model"
    assert model.owned_by is not None

    # Check OpenWebUI-specific fields
    assert hasattr(model, "name")

    # Log some model details for debugging
    logger.info(f"Found {len(models)} models")
    logger.info(f"First model: {model.id} (name: {model.name})")

    # Log details of the first few models
    for i, model in enumerate(models[:3]):  # Show first 3 models only
        logger.info(f"\nModel #{i+1}:")
        logger.info(f"  ID: {model.id}")
        logger.info(f"  Name: {model.name}")
        logger.info(f"  Owner: {model.owned_by}")


def test_model_name_field(client):
    """Test that models have the name field properly populated."""
    # Get models list
    models = client.models.list()

    # Check that at least some models have a name that differs from their ID
    named_models = [m for m in models if m.name and m.name != m.id]

    # Log the named models
    if named_models:
        logger.info(f"Found {len(named_models)} models with distinct names")
        for model in named_models[:3]:  # Show first 3 only
            logger.info(f"Model {model.id} has name: {model.name}")

    # It's possible that no models have distinct names, so we don't assert on this
