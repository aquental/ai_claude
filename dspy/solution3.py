import dspy
import os

# Initialize a language model with custom parameters
# Hint: Set temperature higher (around 0.9), max_tokens to 3000, and disable caching
lm = dspy.LM(
    'openai/gpt-4o-mini',
    api_key=os.environ.get('OPENAI_API_KEY'),
    api_base=os.environ.get('OPENAI_BASE_URL'),
    temperature=0.9,
    max_tokens=3000,
    cache=False
)
# Make a creative call to the language model
# Hint: Ask for a short poem about programming
print("\n=== Generated Poem ===")
poem_prompt = "Write a short, creative poem about the joy and creativity of programming. Keep it to 6-8 lines."
poem_response = lm(poem_prompt)
print(poem_response[0] if poem_response else "No response generated.")

# Access the history to verify parameters
print("\n=== LM Call Metadata ===")
# Hint: Get the last call from history and print its parameters, usage, and prompt
last_call = lm.history[-1]
print("Prompt sent:")
print(last_call.get('prompt'))
print("\nParameters (kwargs) used in this call:")
print(last_call.get('kwargs'))
print("\nToken usage:")
print(last_call.get('usage'))
print(f"Cost: {last_call.get('cost')}")

# Verify our custom parameters were applied
print("\n=== Parameter Verification ===")
# Hint: Extract and print the specific parameter values from the history
kwargs = last_call.get('kwargs', {})

print(f"Temperature: {kwargs.get('temperature')}")
print(f"Max tokens: {kwargs.get('max_tokens')}")
# or check 'cache' in kwargs if present
print(f"Cache disabled: {lm.cache == False}")

print("\n=== Full last history entry keys ===")
print(last_call.keys())
