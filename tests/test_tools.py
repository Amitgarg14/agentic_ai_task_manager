import pytest

from app.main import execute_tool
from app.tools.calculator import calculate
from app.tools.datetime_tool import get_current_datetime
from app.tools.registry import (
    get_tool_definitions,
    get_tool_function,
)


def test_calculate_add():
    assert calculate(100, 25, "add") == 125


def test_calculate_subtract():
    assert calculate(100, 25, "subtract") == 75


def test_calculate_multiply():
    assert calculate(125, 48, "multiply") == 6000


def test_calculate_divide():
    assert calculate(100, 25, "divide") == 4


def test_calculate_divide_by_zero():
    with pytest.raises(ValueError):
        calculate(100, 0, "divide")


def test_calculate_invalid_operation():
    with pytest.raises(ValueError):
        calculate(100, 25, "invalid")


def test_registry_contains_calculate():
    tool_function = get_tool_function("calculate")

    assert tool_function is calculate


def test_registry_returns_calculate_definition():
    definitions = get_tool_definitions()

    assert len(definitions) >= 1
    assert definitions[0]["name"] == "calculate"
    assert definitions[0]["type"] == "function"


def test_get_current_datetime_returns_string():
    result = get_current_datetime()

    assert isinstance(result, str)
    assert result


def test_registry_contains_datetime_tool():
    tool_function = get_tool_function("get_current_datetime")

    assert tool_function is get_current_datetime

def test_registry_contains_datetime_definition():
    definitions = get_tool_definitions()

    datetime_definition = next(
        tool
        for tool in definitions
        if tool["name"] == "get_current_datetime"
    )

    assert datetime_definition["type"] == "function"


def test_registry_contains_both_tools():
    definitions = get_tool_definitions()

    tool_names = {
        tool["name"]
        for tool in definitions
    }

    assert tool_names == {
        "calculate",
        "get_current_datetime",
    }    

class FakeToolCall:
    name = "calculate"
    arguments = '{"a": 100, "b": 0, "operation": "divide"}'


def test_execute_tool_handles_tool_error():
    result = execute_tool(FakeToolCall())

    assert result == "Tool error: Cannot divide by zero."    