import pytest

from app.tools.calculator import calculate
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