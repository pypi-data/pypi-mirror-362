import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from unittest.mock import patch
from uuid import UUID

import pytest
from pydantic import BaseModel, Field, ValidationError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from planar.object_registry import ObjectRegistry
from planar.rules.decorator import RULE_REGISTRY, rule, serialize_for_rule_evaluation
from planar.rules.models import JDMGraph, Rule, RuleEngineConfig, create_jdm_graph
from planar.rules.rule_configuration import rule_configuration
from planar.rules.runner import EvaluateError, EvaluateResponse, evaluate_rule
from planar.workflows.decorators import workflow
from planar.workflows.execution import lock_and_execute
from planar.workflows.models import StepType, WorkflowStatus, WorkflowStep


# Test Enums
class CustomerTier(str, Enum):
    """Customer tier enumeration."""

    STANDARD = "standard"
    PREMIUM = "premium"
    VIP = "vip"


# Test data models
class PriceCalculationInput(BaseModel):
    """Input for a price calculation rule."""

    product_id: str = Field(description="Product identifier")
    base_price: float = Field(description="Base price of the product")
    quantity: int = Field(description="Quantity ordered")
    customer_tier: CustomerTier = Field(description="Customer tier")


class PriceCalculationOutput(BaseModel):
    """Output from a price calculation rule."""

    final_price: float = Field(description="Final calculated price")
    discount_applied: float = Field(description="Discount percentage applied")
    discount_reason: str = Field(description="Reason for the discount")


# Default rule implementation for testing
DEFAULT_PRICE_CALCULATION = PriceCalculationOutput(
    final_price=95.0, discount_applied=5.0, discount_reason="Standard 5% discount"
)


# Sample JDM graph for overriding the rule
PRICE_RULE_JDM_OVERRIDE = {
    "nodes": [
        {
            "id": "input-node",
            "type": "inputNode",
            "name": "Input",
            "content": {
                "schema": json.dumps(PriceCalculationInput.model_json_schema())
            },
            "position": {"x": 100, "y": 100},
        },
        {
            "id": "output-node",
            "type": "outputNode",
            "name": "Output",
            "content": {
                "schema": json.dumps(PriceCalculationOutput.model_json_schema())
            },
            "position": {"x": 700, "y": 100},
        },
        {
            "id": "function-node",
            "type": "functionNode",
            "name": "Custom Pricing Logic",
            "content": {
                "source": """
                export const handler = async (input) => {
                  let discount = 0;
                  let reason = "No discount applied";
                  
                  if (input.customer_tier === "premium") {
                    discount = 10;
                    reason = "Premium customer discount";
                  } else if (input.customer_tier === "vip") {
                    discount = 15;
                    reason = "VIP customer discount";
                  }
                  
                  if (input.quantity > 10) {
                    discount += 5;
                    reason += " + bulk order discount";
                  }
                  
                  const finalPrice = input.base_price * input.quantity * (1 - discount/100);
                  
                  return {
                    final_price: finalPrice,
                    discount_applied: discount,
                    discount_reason: reason
                  };
                };
                """
            },
            "position": {"x": 400, "y": 100},
        },
    ],
    "edges": [
        {
            "id": "edge1",
            "sourceId": "input-node",
            "targetId": "function-node",
            "type": "edge",
        },
        {
            "id": "edge2",
            "sourceId": "function-node",
            "targetId": "output-node",
            "type": "edge",
        },
    ],
}


@pytest.fixture
def price_calculation_rule():
    """Returns a rule definition for price calculation testing."""

    @rule(
        description="Calculate the final price based on product, quantity, and customer tier"
    )
    def calculate_price(input: PriceCalculationInput) -> PriceCalculationOutput:
        # In a real implementation, this would contain business logic
        # For testing, simply return the default output
        return DEFAULT_PRICE_CALCULATION

    ObjectRegistry.get_instance().register(calculate_price.__rule__)  # type: ignore

    return calculate_price


@pytest.fixture
def price_calculation_rule_with_body_variables():
    """Returns a rule definition for price calculation testing."""

    @rule(
        description="Calculate the final price based on product, quantity, and customer tier"
    )
    def calculate_price(input: PriceCalculationInput) -> PriceCalculationOutput:
        some_variable = 10
        return PriceCalculationOutput(
            final_price=input.base_price * some_variable,
            discount_applied=0,
            discount_reason="No discount applied",
        )

    return calculate_price


@pytest.fixture
def price_calculation_input():
    """Returns sample price calculation input for testing."""
    return {
        "product_id": "PROD-123",
        "base_price": 100.0,
        "quantity": 1,
        "customer_tier": "standard",
    }


async def test_rule_initialization():
    """Test that a rule function is properly initialized with the @rule decorator."""

    @rule(description="Test rule initialization")
    def test_rule(input: PriceCalculationInput) -> PriceCalculationOutput:
        return DEFAULT_PRICE_CALCULATION

    # The rule should be registered in the RULE_REGISTRY
    assert "test_rule" in RULE_REGISTRY
    registered_rule = RULE_REGISTRY["test_rule"]

    # Verify initialization
    assert registered_rule.name == "test_rule"
    assert registered_rule.description == "Test rule initialization"
    assert registered_rule.input == PriceCalculationInput
    assert registered_rule.output == PriceCalculationOutput


async def test_rule_type_validation():
    """Test that the rule decorator properly validates input and output types."""

    # Should raise ValueError when input type is not a Pydantic model
    with pytest.raises(ValueError):
        # Using Any to avoid the actual type check in pytest itself
        # The validation function in the decorator will still catch this
        @rule(description="Invalid input type")
        def invalid_input_rule(input: Any) -> PriceCalculationOutput:
            return DEFAULT_PRICE_CALCULATION

    # Should raise ValueError when output type is not a Pydantic model
    with pytest.raises(ValueError):
        # Using Any to avoid the actual type check in pytest itself
        @rule(description="Invalid output type")
        def invalid_output_rule(input: PriceCalculationInput) -> Any:
            return "Invalid"

    # Should raise ValueError when missing type annotations
    with pytest.raises(ValueError):
        # Missing type annotation for input
        @rule(description="Missing annotations")
        def missing_annotations_rule(input):
            return DEFAULT_PRICE_CALCULATION

    # Should raise ValueError when missing return type
    with pytest.raises(ValueError):
        # The decorator function should catch this
        @rule(description="Missing return type")
        def missing_return_type(input: PriceCalculationInput):
            return DEFAULT_PRICE_CALCULATION


async def test_rule_in_workflow(session: AsyncSession, price_calculation_rule):
    """Test that a rule can be used in a workflow."""

    @workflow()
    async def pricing_workflow(input_data: Dict):
        input_model = PriceCalculationInput(**input_data)
        result = await price_calculation_rule(input_model)
        return result

    # Start the workflow and run it
    input_data = {
        "product_id": "PROD-123",
        "base_price": 100.0,
        "quantity": 1,
        "customer_tier": "standard",
    }

    wf = await pricing_workflow.start(input_data)
    result = await lock_and_execute(wf)

    # Verify workflow completed successfully
    assert wf.status == WorkflowStatus.SUCCEEDED
    assert wf.result == DEFAULT_PRICE_CALCULATION.model_dump()

    assert isinstance(result, PriceCalculationOutput)
    assert result.final_price == DEFAULT_PRICE_CALCULATION.final_price
    assert result.discount_applied == DEFAULT_PRICE_CALCULATION.discount_applied
    assert result.discount_reason == DEFAULT_PRICE_CALCULATION.discount_reason

    # Verify steps were recorded correctly
    steps = (
        await session.exec(
            select(WorkflowStep).where(WorkflowStep.workflow_id == wf.id)
        )
    ).all()
    assert len(steps) >= 1

    # Find the rule step
    rule_step = next((step for step in steps if step.step_type == StepType.RULE), None)
    assert rule_step is not None
    assert price_calculation_rule.__name__ in rule_step.function_name


async def test_rule_in_workflow_with_body_variables(
    session: AsyncSession, price_calculation_rule_with_body_variables
):
    """Test that a rule can be used in a workflow."""

    @workflow()
    async def pricing_workflow(input_data: Dict):
        input_model = PriceCalculationInput(**input_data)
        result = await price_calculation_rule_with_body_variables(input_model)
        return result

    # Start the workflow and run it
    input_data = {
        "product_id": "PROD-123",
        "base_price": 10.0,
        "quantity": 1,
        "customer_tier": "standard",
    }

    wf = await pricing_workflow.start(input_data)
    result = await lock_and_execute(wf)

    # Verify workflow completed successfully
    assert wf.status == WorkflowStatus.SUCCEEDED
    assert (
        wf.result
        == PriceCalculationOutput(
            final_price=100.0, discount_applied=0, discount_reason="No discount applied"
        ).model_dump()
    )

    assert isinstance(result, PriceCalculationOutput)
    assert result.final_price == 100.0
    assert result.discount_applied == 0
    assert result.discount_reason == "No discount applied"


async def test_rule_override(session: AsyncSession, price_calculation_rule):
    """Test that a rule can be overridden with a JDM graph."""

    # Create and save an override
    override = RuleEngineConfig(jdm=JDMGraph.model_validate(PRICE_RULE_JDM_OVERRIDE))

    cfg = await rule_configuration.write_config(
        price_calculation_rule.__name__, override
    )
    await rule_configuration.promote_config(cfg.id)

    @workflow()
    async def pricing_workflow(input_data: Dict):
        input_model = PriceCalculationInput(**input_data)
        result = await price_calculation_rule(input_model)
        return result

    # Start the workflow with premium customer input
    premium_input = {
        "product_id": "PROD-456",
        "base_price": 100.0,
        "quantity": 5,
        "customer_tier": "premium",
    }

    wf = await pricing_workflow.start(premium_input)
    _ = await lock_and_execute(wf)

    # Verify the workflow used the override logic
    assert wf.status == WorkflowStatus.SUCCEEDED
    assert wf.result is not None
    assert wf.result != DEFAULT_PRICE_CALCULATION.model_dump()
    assert wf.result["discount_applied"] == 10.0
    assert "Premium customer discount" in wf.result["discount_reason"]

    # Now test with VIP customer and bulk order
    vip_bulk_input = {
        "product_id": "PROD-789",
        "base_price": 100.0,
        "quantity": 15,
        "customer_tier": "vip",
    }

    wf2 = await pricing_workflow.start(vip_bulk_input)
    _ = await lock_and_execute(wf2)

    # Verify the workflow used the override logic with both discounts
    assert wf2.status == WorkflowStatus.SUCCEEDED
    assert wf2.result is not None
    assert wf2.result["discount_applied"] == 20.0  # 15% VIP + 5% bulk
    assert "VIP customer discount" in wf2.result["discount_reason"]
    assert "bulk order discount" in wf2.result["discount_reason"]


async def test_evaluate_rule_function():
    """Test the evaluate_rule function directly."""

    # Create test input data
    input_data = {
        "product_id": "PROD-123",
        "base_price": 100.0,
        "quantity": 5,
        "customer_tier": "premium",
    }

    # Test error handling
    with patch("planar.rules.runner.ZenEngine") as MockZenEngine:
        mock_decision = MockZenEngine.return_value.create_decision.return_value
        error_json = json.dumps(
            {
                "type": "RuleEvaluationError",
                "source": json.dumps({"error": "Invalid rule logic"}),
                "nodeId": "decision-table-node",
            }
        )
        mock_decision.evaluate.side_effect = RuntimeError(error_json)

        result = evaluate_rule(
            JDMGraph.model_validate(PRICE_RULE_JDM_OVERRIDE), input_data
        )

        assert isinstance(result, EvaluateError)
        assert result.success is False
        assert result.title == "RuleEvaluationError"
        assert result.message == {"error": "Invalid rule logic"}
        assert result.data["nodeId"] == "decision-table-node"


async def test_rule_override_validation(session: AsyncSession, price_calculation_rule):
    """Test validation when creating a rule override."""

    ObjectRegistry.get_instance().register(price_calculation_rule.__rule__)

    # Test with valid JDMGraph
    valid_jdm = create_jdm_graph(price_calculation_rule.__rule__)
    valid_override = RuleEngineConfig(jdm=valid_jdm)
    assert valid_override is not None
    assert isinstance(valid_override.jdm, JDMGraph)
    await rule_configuration.write_config(
        price_calculation_rule.__name__, valid_override
    )

    # Query back and verify
    configs = await rule_configuration._read_configs(price_calculation_rule.__name__)
    assert len(configs) == 1
    assert configs[0].object_name == price_calculation_rule.__name__
    assert JDMGraph.model_validate(configs[0].data.jdm) == valid_jdm

    # Test with invalid JDMGraph (missing required fields)
    with pytest.raises(ValidationError):
        # Test with incomplete dictionary
        invalid_dict = {"invalid": "structure"}
        JDMGraph.model_validate(invalid_dict)

    # Test with invalid JDMGraph type
    with pytest.raises(ValidationError):
        # Test with completely wrong type
        RuleEngineConfig(jdm="invalid_string")  # type: ignore


def test_serialize_for_rule_evaluation_dict():
    """Test serialization of dictionaries with nested datetime and UUID objects."""

    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    naive_dt = datetime(2023, 12, 25, 14, 30, 45)
    aware_dt = datetime(2023, 12, 25, 14, 30, 45, tzinfo=timezone.utc)

    test_dict = {
        "id": test_uuid,
        "created_at": naive_dt,
        "updated_at": aware_dt,
        "name": "test_item",
        "count": 42,
        "nested": {"another_id": test_uuid, "another_date": naive_dt},
    }

    serialized = serialize_for_rule_evaluation(test_dict)

    assert serialized["id"] == "12345678-1234-5678-1234-567812345678"
    assert serialized["created_at"] == "2023-12-25T14:30:45Z"
    assert serialized["updated_at"] == "2023-12-25T14:30:45+00:00"
    assert serialized["name"] == "test_item"
    assert serialized["count"] == 42
    assert serialized["nested"]["another_id"] == "12345678-1234-5678-1234-567812345678"
    assert serialized["nested"]["another_date"] == "2023-12-25T14:30:45Z"


def test_serialize_for_rule_evaluation():
    """Test serialization of complex nested structures."""

    test_uuid1 = UUID("12345678-1234-5678-1234-567812345678")
    test_uuid2 = UUID("87654321-4321-8765-4321-876543218765")
    naive_dt = datetime(2023, 12, 25, 14, 30, 45, 123456)
    aware_dt = datetime(2023, 12, 25, 14, 30, 45, 123456, timezone.utc)

    complex_data = {
        "metadata": {
            "id": test_uuid1,
            "created_at": naive_dt,
            "updated_at": aware_dt,
            "tags": ["tag1", "tag2", test_uuid2],
        },
        "items": [
            {
                "item_id": test_uuid1,
                "timestamp": naive_dt,
                "values": (1, 2, 3, aware_dt),
            },
            {
                "item_id": test_uuid2,
                "timestamp": aware_dt,
                "nested_list": [{"deep_uuid": test_uuid1, "deep_date": naive_dt}],
            },
        ],
        "enum_values": [CustomerTier.STANDARD],
        "simple_values": [1, "test", True, None],
    }

    serialized = serialize_for_rule_evaluation(complex_data)

    # Verify metadata
    assert serialized["metadata"]["id"] == "12345678-1234-5678-1234-567812345678"
    assert serialized["metadata"]["created_at"] == "2023-12-25T14:30:45.123456Z"
    assert serialized["metadata"]["updated_at"] == "2023-12-25T14:30:45.123456+00:00"
    assert serialized["metadata"]["tags"][2] == "87654321-4321-8765-4321-876543218765"

    # Verify items
    assert serialized["items"][0]["item_id"] == "12345678-1234-5678-1234-567812345678"
    assert serialized["items"][0]["timestamp"] == "2023-12-25T14:30:45.123456Z"
    assert serialized["items"][0]["values"][3] == "2023-12-25T14:30:45.123456+00:00"

    assert serialized["items"][1]["item_id"] == "87654321-4321-8765-4321-876543218765"
    assert serialized["items"][1]["timestamp"] == "2023-12-25T14:30:45.123456+00:00"
    assert (
        serialized["items"][1]["nested_list"][0]["deep_uuid"]
        == "12345678-1234-5678-1234-567812345678"
    )
    assert (
        serialized["items"][1]["nested_list"][0]["deep_date"]
        == "2023-12-25T14:30:45.123456Z"
    )

    # Verify simple values remain unchanged
    assert serialized["simple_values"] == [1, "test", True, None]


class DateTimeTestModel(BaseModel):
    """Test model with datetime fields for integration testing."""

    id: UUID = Field(description="Unique identifier")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Update timestamp")
    name: str = Field(description="Name of the item")


def test_serialize_pydantic_model_with_datetime():
    """Test serialization of Pydantic models containing datetime fields."""

    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    naive_dt = datetime(2023, 12, 25, 14, 30, 45, 123456)
    aware_dt = datetime(2023, 12, 25, 14, 30, 45, 123456, timezone.utc)

    model = DateTimeTestModel(
        id=test_uuid, created_at=naive_dt, updated_at=aware_dt, name="test_model"
    )

    # Serialize the model's dict representation
    model_dict = model.model_dump()
    serialized = serialize_for_rule_evaluation(model_dict)

    assert serialized["id"] == "12345678-1234-5678-1234-567812345678"
    assert serialized["created_at"] == "2023-12-25T14:30:45.123456Z"
    assert serialized["updated_at"] == "2023-12-25T14:30:45.123456+00:00"
    assert serialized["name"] == "test_model"


async def test_rule_with_complex_types_serialization(session: AsyncSession):
    """Integration test: Test that complex types serialization works in rule evaluation."""

    class ComplexTypesInput(BaseModel):
        event_id: UUID
        event_time: datetime
        event_name: str
        enum_value: CustomerTier

    class ComplexTypesOutput(BaseModel):
        processed_id: UUID
        processed_time: datetime
        enum_value: CustomerTier
        message: str

    @rule(description="Process datetime input")
    def process_datetime_rule(input: ComplexTypesInput) -> ComplexTypesOutput:
        # Should actually be using the rule override below.
        return ComplexTypesOutput(
            processed_id=UUID("12345678-1234-5678-1234-567812345678"),
            processed_time=datetime.now(timezone.utc),
            enum_value=CustomerTier.STANDARD,
            message="Should not be using this default rule",
        )

    ObjectRegistry.get_instance().register(process_datetime_rule.__rule__)  # type: ignore

    # Create a JDM override that uses the datetime fields
    datetime_jdm_override = {
        "nodes": [
            {
                "id": "input-node",
                "type": "inputNode",
                "name": "Input",
                "content": {
                    "schema": json.dumps(ComplexTypesInput.model_json_schema())
                },
                "position": {"x": 100, "y": 100},
            },
            {
                "id": "output-node",
                "type": "outputNode",
                "name": "Output",
                "content": {
                    "schema": json.dumps(ComplexTypesOutput.model_json_schema())
                },
                "position": {"x": 700, "y": 100},
            },
            {
                "id": "function-node",
                "type": "functionNode",
                "name": "DateTime Processing",
                "content": {
                    "source": """
                    export const handler = async (input) => {
                      return {
                        processed_id: input.event_id,
                        processed_time: input.event_time,
                        enum_value: input.enum_value,
                        message: `Override processed ${input.event_name}`
                      };
                    };
                    """
                },
                "position": {"x": 400, "y": 100},
            },
        ],
        "edges": [
            {
                "id": "edge1",
                "sourceId": "input-node",
                "targetId": "function-node",
                "type": "edge",
            },
            {
                "id": "edge2",
                "sourceId": "function-node",
                "targetId": "output-node",
                "type": "edge",
            },
        ],
    }

    # Create and save an override
    override = RuleEngineConfig(jdm=JDMGraph.model_validate(datetime_jdm_override))
    cfg = await rule_configuration.write_config(
        process_datetime_rule.__name__, override
    )
    await rule_configuration.promote_config(cfg.id)

    @workflow()
    async def datetime_workflow(input: ComplexTypesInput):
        result = await process_datetime_rule(input)
        return result

    # Test with naive datetime
    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    naive_dt = datetime(2023, 12, 25, 14, 30, 45, 123456)

    input = ComplexTypesInput(
        event_id=test_uuid,
        event_time=naive_dt,
        event_name="test_event",
        enum_value=CustomerTier.STANDARD,
    )

    wf = await datetime_workflow.start(input)
    await lock_and_execute(wf)

    # Verify the workflow completed successfully
    assert wf.status == WorkflowStatus.SUCCEEDED
    assert wf.result is not None
    assert ComplexTypesOutput.model_validate(wf.result) == ComplexTypesOutput(
        processed_id=test_uuid,
        processed_time=naive_dt.replace(tzinfo=timezone.utc),
        enum_value=CustomerTier.STANDARD,
        message="Override processed test_event",
    )


async def test_create_jdm_graph():
    """Test JDM graph generation from rule schemas."""
    rule = Rule(
        name="test_price_rule",
        description="Test price calculation rule",
        input=PriceCalculationInput,
        output=PriceCalculationOutput,
    )

    # Generate the JDM graph
    jdm_graph = create_jdm_graph(rule)

    # Verify the structure
    assert len(jdm_graph.nodes) == 3  # input, decision table, output
    assert len(jdm_graph.edges) == 2  # input->table, table->output

    # Verify node types
    node_types = {node.type for node in jdm_graph.nodes}
    assert node_types == {"inputNode", "decisionTableNode", "outputNode"}

    # Find the decision table node
    decision_table = next(
        node for node in jdm_graph.nodes if node.type == "decisionTableNode"
    )

    # Verify output columns match the output schema
    output_columns = decision_table.content.outputs
    assert len(output_columns) == 3  # final_price, discount_applied, discount_reason

    output_fields = {col.field for col in output_columns}
    assert output_fields == {"final_price", "discount_applied", "discount_reason"}

    # Verify rule values have correct default types
    rule_values = decision_table.content.rules[0]

    # Find column IDs for each field
    final_price_col = next(col for col in output_columns if col.field == "final_price")
    discount_applied_col = next(
        col for col in output_columns if col.field == "discount_applied"
    )
    discount_reason_col = next(
        col for col in output_columns if col.field == "discount_reason"
    )

    assert getattr(rule_values, final_price_col.id) == "0"  # number default
    assert getattr(rule_values, discount_applied_col.id) == "0"  # number default
    assert (
        getattr(rule_values, discount_reason_col.id) == '"default value"'
    )  # string default

    # Verify input and output nodes have proper schemas
    input_node = next(node for node in jdm_graph.nodes if node.type == "inputNode")
    output_node = next(node for node in jdm_graph.nodes if node.type == "outputNode")

    input_schema = json.loads(input_node.content.schema_)
    output_schema = json.loads(output_node.content.schema_)

    assert input_schema == PriceCalculationInput.model_json_schema()
    assert output_schema == PriceCalculationOutput.model_json_schema()


async def test_jdm_graph_evaluation():
    """Test evaluating a JDM graph with a simple rule."""

    # Create a rule and generate its JDM graph
    @rule(description="Test JDM evaluation")
    def simple_rule(input: PriceCalculationInput) -> PriceCalculationOutput:
        return DEFAULT_PRICE_CALCULATION

    jdm_graph = create_jdm_graph(RULE_REGISTRY[simple_rule.__name__])

    # Test input data
    test_input = {
        "product_id": "PROD-EVAL",
        "base_price": 200.0,
        "quantity": 2,
        "customer_tier": "vip",
    }

    # Evaluate the rule
    result = evaluate_rule(jdm_graph, test_input)

    # Verify the result
    assert isinstance(result, EvaluateResponse)
    assert result.success is True
    assert result.result["final_price"] == 0.0
    assert result.result["discount_applied"] == 0.0
    assert "default value" in result.result["discount_reason"]
