import json
from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()

# Choose a model to use
model = "claude-sonnet-4-6"

# Short system prompt
system_prompt = "You are a helpful assistant. Answer questions very briefly."

# Create an array of messages to send to Claude
messages = [
    {
        "role": "user",
        "content": "What is the main difference between cats and dogs as pets"
    }
]

# Send the messages to Claude
response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=messages,
    system=system_prompt
)

# Print the text response
print("First response text:")
print(response.content[0].text)

# Append Claude's response to messages
messages.append({"role": "assistant", "content": response.content})

# Append a new user message
messages.append({"role": "user", "content": "Which one is easier to train?"})

# Add thinking parameter with type "enabled" and budget_tokens 10000
# Remember to increase your max_tokens to accomodate all the tokens
second_response = client.messages.create(
    model=model,
    max_tokens=16000,
    messages=messages,
    system=system_prompt,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    }
)

# Print the whole response as JSON
print("\nSecond response JSON:")
print(json.dumps(second_response.model_dump(), indent=2))

# Get all text content from the response
print("\nSecond response text:")
text_contents = [
    block.text for block in second_response.content if block.type == "text"]
print("\n".join(text_contents))
