from app.tools.calculator import calculate


# Map tool names to Python functions.
TOOL_FUNCTIONS = {
    "calculate": calculate,
}


# Describe the tools to the LLM.
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "calculate",
        "description": (
            "Perform a basic mathematical calculation. "
            "Use this tool for arithmetic operations."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number."
                },
                "b": {
                    "type": "number",
                    "description": "The second number."
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ],
                    "description": "The mathematical operation."
                }
            },
            "required": ["a", "b", "operation"],
            "additionalProperties": False
        }
    }
]


def get_tool_definitions():
    """Return tool definitions for the LLM."""
    return TOOL_DEFINITIONS


def get_tool_function(tool_name):
    """Return the Python function associated with a tool."""
    if tool_name not in TOOL_FUNCTIONS:
        raise ValueError(f"Unknown tool: {tool_name}")

    return TOOL_FUNCTIONS[tool_name]