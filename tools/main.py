import json
from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()

# Enhance this system prompt to guide Claude toward using tools for calculations
system_prompt = (
    "You are a helpful assistant."
    "When performing calculations, use the available tools for accuracy."
)

# Load the tool schemas from JSON file
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Create a message requesting a calculation
messages = [
    {"role": "user", "content": "Please calculate 15 + 27"}
]

# Send the request with tools enabled
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=2000,
    messages=messages,
    system=system_prompt,
    tools=tool_schemas
)

# Print the complete response structure
print(json.dumps(response.model_dump(), indent=2))
