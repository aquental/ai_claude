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

# Create a calculator assistant
calculator_assistant = Agent(
    name="calculator_assistant",
    system_prompt="You are a calculator assistant. You specialize in mathematical calculations and solving equations.",
    tools=math_tools,
    tool_schemas=tool_schemas,
    handoffs=[]
)

# Create a general assistant (can handoff to calculator)
helpful_assistant = Agent(
    name="helpful_assistant",
    system_prompt="You are a helpful assistant. You can assist with various tasks and handoff to the calculator assistant for math problems.",
    tools={},
    tool_schemas=[],
    handoffs=[calculator_assistant]
)

# Example test messages
messages1 = [
    {
        'role': 'user',
        'content': 'What is the capital of France?'
    }
]

messages2 = [
    {
        'role': 'user',
        'content': 'What is the solution to the equation 4x - 7 = 9?'
    }
]

# Call helpful_assistant.run with messages1 and print the response
result_messages, response = helpful_assistant.run(messages1)
print(response)

# Call helpful_assistant.run with messages2 and print the response
result_messages, response = helpful_assistant.run(messages2)
print(response)
