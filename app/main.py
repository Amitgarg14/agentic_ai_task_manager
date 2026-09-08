import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.executor import execute_tool
from app.tools.registry import get_tool_definitions


def run_agent(client, user_task):
    """Run the agent until it produces a final answer."""

    tools = get_tool_definitions()

    response = client.responses.create(
        model="gpt-5-mini",
        input=(
            "You are an AI agent with access to tools.\n\n"
            "Available tools:\n"
            "- calculate: Use for arithmetic calculations.\n"
            "- get_current_datetime: Use when the user asks for "
            "the current date, current time, today, or now.\n\n"
            "Choose tools when they are useful for completing the "
            "user's task. For multi-step tasks, use previous tool "
            "results as inputs to subsequent tool calls.\n\n"
            f"User task:\n{user_task}"
        ),
        tools=tools,
    )

    max_iterations = 5

    for iteration in range(max_iterations):
        print(f"\n--- Agent iteration {iteration + 1} ---")

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

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