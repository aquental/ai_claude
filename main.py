import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env (e.g. ANTHROPIC_API_KEY)
load_dotenv()

# Initialize the Anthropic client
client = Anthropic()

# Define the model to use
model = "claude-sonnet-4-6"

# Create a short system prompt that makes Claude a helpful assistant who answers briefly
system_prompt = "You are a helpful assistant. Answer questions very briefly."

# Create an array of messages to send to Claude with a single user message
messages = [
    {
        "role": "user",
        "content": "What is the main difference between cats and dogs as pets"
    }
]

# Send the messages to Claude using client.messages.create() with your model, system prompt and max tokens
response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=messages,
    system=system_prompt
)

# Print the whole response as JSON
print(json.dumps(response.model_dump(), indent=2))
