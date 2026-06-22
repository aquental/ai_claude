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

# Increase max_turns to 15 to handle the more complex equation
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas,
    max_turns=15
)

# Change the equation to "2x² - 7x + 3 = 0" for a more complex challenge
messages = [{"role": "user", "content": "Solve this equation: 2x² - 7x + 3 = 0"}]

# Send message to the stateless agent
messages, result = agent.run(messages)

# Display the response
print("\nFinal response:")
print(result)

# Show the conversation history
print("\nConversation history:")
for i, msg in enumerate(messages):
    role = msg["role"]
    content = msg["content"]
    print(f"{i}. {role}: {content}")
