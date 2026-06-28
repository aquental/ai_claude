import dspy
import os

# Initialize two different language models
# Hint: Create one primary model (e.g., GPT-4o-mini) and one secondary model (e.g., GPT-3.5-turbo). Remember to set api_key to os.environ['OPENAI_API_KEY'] and api_base to os.environ['OPENAI_BASE_URL']
lm4 = dspy.LM('openai/gpt-4o-mini', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
lm3 = dspy.LM('openai/gpt-3.5-turbo', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])

# Set the primary model as the global default
# Hint: Use dspy.configure()
dspy.configure(lm=lm4)

# Create a prompt that we'll use for both models
prompt = "Explain the concept of recursion in one sentence."

# Make a direct call using the global default model
print("=== Using Primary Model (Global Default) ===")
# Hint: Call the primary model with the prompt and print the response
response = lm4(prompt, temperature=0.7)
print(response)

# Check the history before context switch
# Hint: Get the length of the primary model's history and print relevant metadata
print(f"Primary model (lm4) history length before context switch: {len(lm4.history)}")
before_primary_len = len(lm4.history)

# TODO: Use a context manager to temporarily switch to the secondary model
print("\n=== Using Secondary Model (Context Override) ===")
# Hint: Use dspy.context() to temporarily set the secondary model as the active LM
with dspy.context(lm=lm3):
    # TODO: Make the same call with the secondary model
    # Hint: Call the secondary model with the same prompt and print the response
    response_secondary = lm3(prompt, temperature=0.7)
    print(response_secondary)

# TODO: Check the history after context switch
# Hint: Compare the history lengths before and after the context switch
print(f"\nPrimary model (lm4) history length after context switch: {len(lm4.history)} (was {before_primary_len})")
print(f"Secondary model (lm3) history length: {len(lm3.history)}")

# TODO: Verify both interactions are in their respective histories
print("\n=== History Verification ===")
# Hint: Check if the primary model's history length changed and print a message
if len(lm4.history) == before_primary_len:
    print("✓ Primary model's history length did NOT change during the context switch (as expected).")
else:
    print("⚠ Primary model's history length changed unexpectedly.")

print(f"Secondary model now has {len(lm3.history)} interaction(s) in its history.")

# TODO: Print metadata from the secondary model's history
# Hint: Access the last call in the secondary model's history
if lm3.history:
    last_call = lm3.history[-1]
    print("\nMetadata keys from secondary model's last history entry:")
    print(last_call.keys())
    print(f"  Model: {last_call.get('model', 'N/A')}")
    print(f"  Timestamp: {last_call.get('timestamp', 'N/A')}")
    if 'usage' in last_call and last_call['usage']:
        print(f"  Usage: {last_call['usage']}")

# TODO: Compare the responses from both models
print("\n=== Response Comparison ===")
# Hint: Print both responses side by side to see the differences
print("Primary Model (lm4 / GPT-4o-mini):")
print(response)
print("\nSecondary Model (lm3 / GPT-3.5-turbo):")
print(response_secondary)

