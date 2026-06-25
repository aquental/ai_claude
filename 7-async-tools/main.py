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

# Write multiple prompts that we'll process synchronously
prompts = [
    "Solve this: (2 + 3) * (4*4)",
    "Find the roots of x^2 - 5x + 6 = 0",
]

# Create a single agent that will handle conversations
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas,
    max_turns=15
)

# Loop through each prompt in the prompts list using enumerate with start=1
for i, prompt in enumerate(prompts, 1):
    # Call agent.run_sync() with the proper message format for each prompt (no await needed!)
    messages, response_text = agent.run_sync(
        [{"role": "user", "content": prompt}])

    # Print the result with run number and final response text
    print(f"\n=== Run {i} ===")
    print(f"Prompt: {prompt}")
    print(f"Response: {response_text}")
