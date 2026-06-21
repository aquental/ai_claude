import json
from agent import Agent
from functions import (
    sum_numbers,
    subtract_numbers
)
# Create a simple agent for general conversation with an appropriate system prompt
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)
tools = {
    "sum_numbers": sum_numbers,
    "subtract_numbers": subtract_numbers,
}
agent = Agent(
    name="simple_agent",
    system_prompt="You are a helpful math assistant.",
    tools=tools,
    tool_schemas=tool_schemas
)
# Start with a message list containing one user message
messages = [{"role": "user", "content": "Solve this equation: 2 - 7 + 3"}]

# Send the first message to the agent and print the response
messages, result = agent.run(messages)
print("=== First Response ===")
print(result)

# Add a follow-up user question to the conversation history
messages.append({
    "role": "user",
    "content": "Now add 10 to the previous result."
})
# Send the updated conversation to the agent and print the response
messages, result = agent.run(messages)
print("=== Second Response ===")
print(result)
