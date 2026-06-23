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

# Load tool schemas
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Math tools
math_tools = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "subtract_numbers": subtract_numbers,
    "divide_numbers": divide_numbers,
    "power": power,
    "square_root": square_root
}


# Define the create_agent_schema function that takes an agent and description as parameters
def create_agent_schema(agent, description):
    """Create a tool schema for an agent that can be used by other agents."""
    return {
        "name": f"{agent.name}_agent",
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message or task to send to the agent"
                }
            },
            "required": ["message"]
        }
    }


# Create a calculator assistant
calculator_assistant = Agent(
    name="calculator_assistant",
    system_prompt="You are a calculator assistant. You specialize in mathematical calculations and solving equations.",
    tools=math_tools,
    tool_schemas=tool_schemas
)

# Call your create_agent_schema function with the calculator_assistant and an appropriate description
schema = create_agent_schema(
    calculator_assistant,
    "Use this tool to delegate mathematical calculations and equation solving to a specialized calculator assistant."
)

# Print the resulting schema using a readable output
print("Agent Tool Schema:")
print(json.dumps(schema, indent=2))
