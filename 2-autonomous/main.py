import json
from agent import Agent
from functions import (
    sum_numbers,
    multiply_numbers,
    subtract_numbers,
    divide_numbers,
    power,
    square_root
)

# Load the schemas from JSON file
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Create a dictionary mapping tool names to functions
tools = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "subtract_numbers": subtract_numbers,
    "divide_numbers": divide_numbers,
    "power": power,
    "square_root": square_root
}

# Create a math assistant agent
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas
)


# Mock tool_use class to test call_tool
class MockToolUse:
    def __init__(self, name, input_data, id):
        self.name = name
        self.input = input_data
        self.id = id


# Mock tool_use object to test call_tool
mock_tool_use = MockToolUse(
    name="sum_numbers",
    input_data={"a": 5, "b": 3},
    id="test_123"
)

# TODO: Call agent.call_tool with the mock tool_use object and store the result
result = agent.call_tool(mock_tool_use)

# TODO: Print the result of the successful tool call
print(f" result: {result}")

# TODO: Create another mock tool_use object for a non-existent tool to test error handling
mock_tool_use_fake = MockToolUse(
    name="nonexistant",
    input_data={"a": 5, "b": 3},
    id="missing_123"
)
# TODO: Call agent.call_tool with the error mock object and store the result
result = agent.call_tool(mock_tool_use_fake)
# TODO: Print the error scenario result
print(f" result: {result}")
