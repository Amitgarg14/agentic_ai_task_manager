import json

from app.tools.registry import get_tool_function


def execute_tool(tool_call):
    """Execute a tool requested by the model."""

    try:
        tool_function = get_tool_function(tool_call.name)

        arguments = json.loads(tool_call.arguments)

        result = tool_function(**arguments)

        print(f"\nTool called: {tool_call.name}")
        print(f"Arguments: {arguments}")
        print(f"Tool result: {result}")

        return str(result)

    except Exception as exc:
        error_message = f"Tool error: {exc}"

        print(f"\nTool called: {tool_call.name}")
        print(f"Tool error: {exc}")

        return error_message