import json
from anthropic import Anthropic
from functions import sum_numbers, multiply_numbers

# Initialize the Anthropic client
client = Anthropic()

# Choose a Claude model
model = "claude-sonnet-4-6"

# System prompt with explicit instructions to use tools
system_prompt = (
    "You are a helpful math assistant. "
    "Always use the available tools to perform calculations accurately."
)

# Load the schemas from JSON file
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Create a dictionary mapping tool names to functions
tools = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers
}

# Create a list of messages to send to Claude
messages = [
    {"role": "user", "content": "Please calculate 15 + 27"}
]

# Send the messages to Claude
response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=messages,
    system=system_prompt,
    tools=tool_schemas
)

# Add the assistant's response to messages
messages.append({
    "role": "assistant",
    "content": response.content
})

# Check if Claude wants to use any functions and execute them
if response.stop_reason == "tool_use":
    # Define a list to collect all tool results
    tool_results = []

    for content_item in response.content:
        # Check if the content item is a tool use
        if content_item.type == "tool_use":
            # Get the tool name, input, and id
            tool_name = content_item.name
            tool_input = content_item.input
            tool_id = content_item.id

            # Print the tool name, input
            print(f"Executing: {tool_name}({tool_input})")

            # Use try-except to handle both missing tools and execution errors
            try:
                # Check if the requested tool exists and execute it
                if tool_name in tools:
                    result = tools[tool_name](**tool_input)
                else:
                    result = f"Error: Function {tool_name} not found"
            except Exception as e:
                # Handle any errors that occur during function execution
                result = f"Error executing {tool_name}: {str(e)}"

            # Print the result
            print(f"Result: {result}")

            # Append a properly structured tool_result for this specific tool_use
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": str(result)
            })

    # Add all tool results as a single user message
    messages.append({
        "role": "user",
        "content": tool_results
    })

    # Send the results back to Claude for the final response
    final_response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=messages,
        system=system_prompt,
        tools=tool_schemas
    )

    # Append the final response to messages
    messages.append({
        "role": "assistant",
        "content": final_response.content
    })

    # Print the final response
    print("\nClaude's final response:")
    print(final_response.content[0].text)

else:
    # Print the response if Claude did not use any tools
    print("Claude did not use any tools:")
    print(response.content[0].text)

# Print the messages history
print("\nMessages history:")

# Loop through each message to see the conversation development
for i, message in enumerate(messages):
    print(f"\nMessage {i + 1} - Role: {message['role']}")
    # Handle different content formats (string vs list)
    if isinstance(message['content'], str):
        print(f"Content: {message['content']}")
    else:
        # For list content, print each item separately
        for j, content in enumerate(message['content']):
            print(f"Content {j + 1}: {content}")
