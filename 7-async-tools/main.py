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


async def main():
    # Write multiple prompts that we'll process concurrently
    prompts = [
        "Solve this: (2 + 3) * (4*4)",
        "Find the roots of x^2 - 5x + 6 = 0",
    ]

    # Create a single agent that will handle multiple conversations concurrently
    agent = Agent(
        name="math_assistant",
        system_prompt="You are a helpful math assistant.",
        tools=tools,
        tool_schemas=tool_schemas,
        max_turns=15
    )

    # Create a list of coroutine tasks, one for each prompt (not started yet)
    tasks = [
        agent.run([{"role": "user", "content": prompt}])
        for prompt in prompts
    ]

    # Run all tasks concurrently and wait for all to complete
    results = await asyncio.gather(*tasks)

    # Display the final response from each conversation
    for idx, (_, result) in enumerate(results, start=1):
        print(f"\n=== run {idx} ===")
        print(result)

# Entry point - creates event loop and runs the async main() function
if __name__ == "__main__":
    asyncio.run(main())
