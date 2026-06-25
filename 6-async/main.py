import asyncio
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

# Create a single agent with math tools
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas,
    max_turns=15
)

# Define a single user prompt
prompt = "What is 15 + 27?"

# Create a message list with the prompt
messages = [{"role": "user", "content": prompt}]

# Run the async agent
async def main():
    _, result = await agent.run(messages)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
