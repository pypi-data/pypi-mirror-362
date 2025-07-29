from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, Field
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from examples.expense_approval_workflow.models import (
    Expense,
    ExpenseStatus,
)
from planar import PlanarApp, get_session, sqlite_config
from planar.files.models import PlanarFile, PlanarFileMetadata
from planar.files.storage.base import Storage
from planar.testing.planar_test_client import PlanarTestClient
from planar.testing.workflow_observer import WorkflowObserver
from planar.workflows import step, workflow
from planar.workflows.models import StepType, Workflow, WorkflowStatus, WorkflowStep

# ------ SETUP ------


async def get_expense(expense_id: str) -> Expense:
    session = get_session()
    expense = (
        await session.exec(select(Expense).where(Expense.id == UUID(expense_id)))
    ).first()
    if not expense:
        raise ValueError(f"Expense {expense_id} not found")
    return expense


@workflow(name="test_expense_approval_workflow")
async def expense_approval_workflow(expense_id: str):
    """
    Main workflow that orchestrates the expense approval process
    """
    await validate_expense(expense_id)

    expense = await get_expense(expense_id)

    return expense


@step()
async def validate_expense(expense_id: str):
    expense = await get_expense(expense_id)

    if expense.status != ExpenseStatus.SUBMITTED:
        raise ValueError(f"Expense {expense_id} is not in SUBMITTED status")


class FileProcessingResult(BaseModel):
    """Result of processing a text file."""

    filename: str = Field(description="Original filename")
    character_count: int = Field(description="Number of characters in the file")
    content_preview: str = Field(description="Preview of the file content")
    file_id: UUID = Field(description="ID of the processed file")


@workflow(name="test_file_processing_workflow")
async def file_processing_workflow(file: PlanarFile):
    """
    Workflow that processes a text file and returns basic information about it.
    """
    file_content = await file.get_content()
    char_count = len(file_content)
    preview = file_content[:100].decode("utf-8")

    # Return structured result
    return FileProcessingResult(
        filename=file.filename,
        character_count=char_count,
        content_preview=preview,
        file_id=file.id,
    )


app = PlanarApp(
    config=sqlite_config("test_workflow_router.db"),
    title="Test Workflow Router API",
    description="API for testing workflow routers",
)


# ------ TESTS ------


@pytest.fixture(name="app")
def app_fixture():
    # Re-register workflows since ObjectRegistry gets reset before each test
    app.register_workflow(expense_approval_workflow)
    app.register_workflow(file_processing_workflow)
    yield app


@pytest.fixture
async def planar_file(storage: Storage) -> PlanarFile:
    """Create a PlanarFile instance for testing."""
    # Store test content
    test_data = b"This is a test file for the workflow router API test."
    mime_type = "text/plain"

    # Store the file and get a reference
    storage_ref = await storage.put_bytes(test_data, mime_type=mime_type)

    # Create and store the file metadata
    session = get_session()
    file_metadata = PlanarFileMetadata(
        filename="router_test_file.txt",
        content_type=mime_type,
        size=len(test_data),
        storage_ref=storage_ref,
    )
    session.add(file_metadata)
    await session.commit()

    # Return a PlanarFile reference (not the full metadata)
    return PlanarFile(
        id=file_metadata.id,
        filename=file_metadata.filename,
        content_type=file_metadata.content_type,
        size=file_metadata.size,
    )


async def test_list_workflows(client: PlanarTestClient):
    """
    Test that the workflow management router correctly lists registered workflows.
    """
    # Call the workflow management endpoint to list workflows
    response = await client.get("/planar/v1/workflows/")

    # Verify the response status code
    assert response.status_code == 200

    # Parse the response data
    data = response.json()

    # Verify that two workflows are returned
    assert data["total"] == 2
    assert len(data["items"]) == 2

    assert data["offset"] == 0
    assert data["limit"] == 10

    # Verify the expense workflow details
    expense_workflow = next(
        item
        for item in data["items"]
        if item["name"] == "test_expense_approval_workflow"
    )
    assert expense_workflow["fully_qualified_name"] == "test_expense_approval_workflow"
    assert (
        "Main workflow that orchestrates the expense approval process"
        in expense_workflow["description"]
    )

    # Verify the file workflow details
    file_workflow = next(
        item
        for item in data["items"]
        if item["name"] == "test_file_processing_workflow"
    )
    assert file_workflow["fully_qualified_name"] == "test_file_processing_workflow"
    assert "Workflow that processes a text file" in file_workflow["description"]

    # Verify that the workflows have input and output schemas
    assert "input_schema" in expense_workflow
    assert "output_schema" in expense_workflow
    assert "input_schema" in file_workflow
    assert "output_schema" in file_workflow

    # Verify that the file workflow input schema includes file parameter
    assert "file" in file_workflow["input_schema"]["properties"]

    # Verify run statistics are present
    assert "total_runs" in expense_workflow
    assert "run_statuses" in expense_workflow
    assert "total_runs" in file_workflow
    assert "run_statuses" in file_workflow


async def test_start_file_workflow(
    client: PlanarTestClient,
    planar_file: PlanarFile,
    observer: WorkflowObserver,
    session: AsyncSession,
):
    """Test starting a workflow with a PlanarFile through the API."""
    # Prepare the request payload with the file reference
    payload = {
        "file": {
            "id": str(planar_file.id),
            "filename": planar_file.filename,
            "content_type": planar_file.content_type,
            "size": planar_file.size,
        }
    }

    response = await client.post(
        "/planar/v1/workflows/test_file_processing_workflow/start",
        json=payload,
    )

    # Verify the response status code
    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    workflow_id = data["id"]

    await observer.wait("workflow-succeeded", workflow_id=workflow_id)

    workflow = await session.get(Workflow, UUID(workflow_id))
    await session.commit()
    assert workflow

    # Verify the workflow completed successfully
    assert workflow.status == WorkflowStatus.SUCCEEDED

    # Check the workflow result
    result = workflow.result
    assert result
    assert result["filename"] == planar_file.filename
    assert result["character_count"] == planar_file.size
    assert "This is a test file" in result["content_preview"]
    assert result["file_id"] == str(planar_file.id)


async def test_get_compute_step(
    client: PlanarTestClient, session: AsyncSession, observer: WorkflowObserver
):
    """Ensure compute steps can be retrieved without metadata."""

    expense = Expense(
        title="Test Expense",
        amount=100.0,
        description="test",
        status=ExpenseStatus.SUBMITTED,
        submitter_id=uuid4(),
        category="misc",
    )
    session.add(expense)
    await session.commit()

    payload = {"expense_id": str(expense.id)}
    resp = await client.post(
        "/planar/v1/workflows/test_expense_approval_workflow/start",
        json=payload,
    )
    assert resp.status_code == 200
    wf_id = resp.json()["id"]

    await observer.wait("workflow-succeeded", workflow_id=wf_id)

    step = (
        await session.exec(
            select(WorkflowStep).where(WorkflowStep.workflow_id == UUID(wf_id))
        )
    ).first()
    await session.commit()
    assert step
    assert step.step_type == StepType.COMPUTE

    resp = await client.get(
        f"/planar/v1/workflows/test_expense_approval_workflow/runs/{wf_id}/steps/{step.step_id}"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "meta" in data
    assert data["meta"] is None
