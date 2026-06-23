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


def create_agent_schema(agent, description):

    # Define an inner function called agent_tool_function that accepts a message parameter
    def agent_tool_function(message):
        print(f"🦾 Agent tool called ({agent.name}): {message}")

        # Call the agent
        _, response = agent.run([{"role": "user", "content": message}])

        print(f"📊 Agent response ({agent.name}): {response}")

        return response

    # Create schema for this agent tool
    tool_schema = {
        "name": f"{agent.name}_agent",
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to send to the agent"
                }
            },
            "required": ["message"]
        }
    }

    # Return a tuple containing both the agent_tool_function and the tool_schema
    return agent_tool_function, tool_schema


# Create a calculator assistant
calculator_assistant = Agent(
    name="calculator_assistant",
    system_prompt="You are a calculator assistant. You specialize in mathematical calculations and solving equations.",
    tools=math_tools,
    tool_schemas=tool_schemas
)

# Call create_agent_schema with the calculator_assistant and description
# Use tuple unpacking to capture both the tool function and the schema
calculator_tool, calculator_schema = create_agent_schema(
    calculator_assistant,
    "A specialized calculator assistant that can perform mathematical calculations and solve equations."
)

# Test the tool function directly by calling it with a math question like "What is 25 multiplied by 4?"
result = calculator_tool("What is 25 multiplied by 4?")

# Print the returned result
print("\nTool test result:")
print(result)
