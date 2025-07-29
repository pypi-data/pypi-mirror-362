from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel

from examples.simple_service.models import (
    Invoice,
)
from planar import PlanarApp, sqlite_config

load_dotenv()


router = APIRouter()


class InvoiceRequest(BaseModel):
    message: str


class InvoiceResponse(BaseModel):
    status: str
    echo: str


app = PlanarApp(
    config=sqlite_config("simple_service.db"),
    title="Sample Invoice API",
    description="API for CRUD'ing invoices",
)


def test_register_model_deduplication():
    """Test that registering the same model multiple times only adds it once to the registry."""

    # Ensure Invoice is registered (ObjectRegistry gets reset before each test)
    app.register_entity(Invoice)
    initial_model_count = len(app._object_registry.get_entities())

    # Register the Invoice model again
    app.register_entity(Invoice)

    assert len(app._object_registry.get_entities()) == initial_model_count

    # Register the same model a second time
    app.register_entity(Invoice)

    assert len(app._object_registry.get_entities()) == initial_model_count

    # Verify that the model in the registry is the Invoice model
    registered_models = app._object_registry.get_entities()
    assert any(model.__name__ == "Invoice" for model in registered_models)
