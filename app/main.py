import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.registry import (
    get_tool_definitions,
    get_tool_function,
)


def execute_tool(tool_call):
    """Execute a tool requested by the model."""

    tool_function = get_tool_function(tool_call.name)

    arguments = json.loads(tool_call.arguments)

    result = tool_function(**arguments)

    print(f"\nTool called: {tool_call.name}")
    print(f"Arguments: {arguments}")
    print(f"Tool result: {result}")

    return str(result)


def run_agent(client, user_task):
    """Run the agent until it produces a final answer."""

    tools = get_tool_definitions()

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are an agent with access to tools.\n"
            "When the user's task involves arithmetic, you MUST use "
            "the calculate tool instead of calculating the result yourself.\n"
            "For multi-step arithmetic, use the tool one step at a time "
            "and use the previous tool result for the next calculation.\n\n"
            f"User task:\n{user_task}"
        ),
        tools=tools,
        tool_choice="required",
    )

    max_iterations = 5

    for iteration in range(max_iterations):
        print(f"\n--- Agent iteration {iteration + 1} ---")

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tool call means the agent has produced its answer.
        if not tool_calls:
            return response.output_text

        tool_outputs = []

        for tool_call in tool_calls:
            result = execute_tool(tool_call)

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": result,
                }
            )

        # Send tool results back to the model.
        response = client.responses.create(
            model="gpt-5-mini",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools,
        )

    raise RuntimeError(
        f"Agent stopped after {max_iterations} iterations."
    )


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set in the .env file."
        )

    client = OpenAI(api_key=api_key)

    user_task = input("\nEnter your task: ")

    if not user_task.strip():
        print("Please enter a task.")
        return

    print("\nStarting agent...")

    final_answer = run_agent(
        client,
        user_task,
    )

    print("\nFinal Answer:")
    print(final_answer)


if __name__ == "__main__":
    main()