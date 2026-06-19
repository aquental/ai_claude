import json
from anthropic import Anthropic
from functions import sum_numbers, multiply_numbers

# Initialize the Anthropic client
client = Anthropic()

# System prompt with explicit instructions to use tools
system_prompt = (
    "You are a helpful math assistant. "
    "Always use the available tools to perform calculations accurately."
)

# Load the schemas from JSON file
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Modify the user message to request two separate addition operations
messages = [
    {"role": "user", "content": "Please calculate 15 + 27 and 17 + 49 and multiply the results"}
]

# Send the messages to Claude
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2000,
    messages=messages,
    system=system_prompt,
    tools=tool_schemas
)

# Print stop reason
print(f"Stop Reason: {response.stop_reason}")

# Extract and print each content item
for i, content_item in enumerate(response.content):
    print(f"\nContent Item {i+1}:")
    print(f"Type: {content_item.type}")
    
    if content_item.type == "text":
        print(f"Text: {content_item.text}")
    elif content_item.type == "tool_use":
        print(f"Tool Name: {content_item.name}")
        print(f"Tool Input: {content_item.input}")
        print(f"Tool ID: {content_item.id}")
