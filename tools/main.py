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

# Create a list of messages to send to Claude
messages = [
    {"role": "user", "content": "Please calculate 15 + 27"}
]

# Send the messages to Claude
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2000,
    messages=messages,
    system=system_prompt,
    tools=tool_schemas
)

# Extract and print the stop_reason from the response
print(f"Stop Reason: {response.stop_reason}")


# Create a loop to iterate through each content item in response.content with enumeration
for i, content_item in enumerate(response.content):
    # Print the content item number and type
    print(f"\nContent Item {i+1}:")
    print(f"Type: {content_item.type}")
    # Check if the content item type is "text" and print the text content
    if content_item.type == "text":
        print(f"Text: {content_item.text}")
    # Check if the content item type is "tool_use" and print the tool name, input, and ID
    elif content_item.type == "tool_use":
        print(f"Tool Name: {content_item.name}")
        print(f"Tool Input: {content_item.input}")
        print(f"Tool ID: {content_item.id}")
