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

# Create a single agent that will handle multiple conversations concurrently
agent = Agent(
    name="math_assistant",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas,
    max_turns=15
)


async def main():
    # Create a list with 2 math problem prompts of your choice
    prompts = [
        "Solve this step by step: What is (25 * 4) + (100 / 5) - (3 ** 2)? Use the available tools.",
        "Calculate the square root of 625, then raise that result to the power of 2, and finally subtract 500 from it. Show your work using the tools."
    ]

    # Create a list of tasks by calling agent.run() for each prompt
    tasks = [
        agent.run([{"role": "user", "content": prompt}])
        for prompt in prompts
    ]

    # Use asyncio.gather() to run all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Loop through results and print each conversation output
    for i, (messages, result) in enumerate(results):
        print(f"\n=== Conversation {i+1} Result ===")
        print(result)
        print("=" * 40)

# Entry point - creates event loop and runs the async main() function
if __name__ == "__main__":
    asyncio.run(main())
