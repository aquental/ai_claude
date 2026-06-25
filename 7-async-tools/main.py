import asyncio
import json
from agent import Agent
from functions import sum_numbers, multiply_numbers


# Simple class to mock a tool_use object from Claude's API
class MockToolUse:
    def __init__(self, name, input_data, id):
        self.name = name
        self.input = input_data
        self.id = id


# Load the schemas from JSON file
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Create a dictionary mapping tool names to functions
tools = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
}

# Create an agent with tools
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas,
)


async def test_async_tool():
    # Create multiple mock tool_use objects
    mock_tool_use_1 = MockToolUse(
        name="sum_numbers",
        input_data={"a": 5, "b": 3},
        id="test_123"
    )

    mock_tool_use_2 = MockToolUse(
        name="multiply_numbers",
        input_data={"a": 4, "b": 7},
        id="test_456"
    )

    mock_tool_use_3 = MockToolUse(
        name="sum_numbers",
        input_data={"a": 10, "b": 20},
        id="test_789"
    )

    # Create a list of tasks using asyncio.create_task() for each mock tool_use object
    # Schedule agent.call_tool() for mock_tool_use_1, mock_tool_use_2, and mock_tool_use_3
    tasks = [
        asyncio.create_task(agent.call_tool(mock_tool_use_1)),
        asyncio.create_task(agent.call_tool(mock_tool_use_2)),
        asyncio.create_task(agent.call_tool(mock_tool_use_3)),
    ]

    # Use asyncio.gather() with await to execute all tasks concurrently and store results
    results = await asyncio.gather(*tasks)

    # Print the results with a descriptive header and loop through each result
    print("=== Concurrent Tool Call Results ===")
    for i, result in enumerate(results, 1):
        print(f"Result {i}: {result}")


if __name__ == "__main__":
    asyncio.run(test_async_tool())
