import dspy

# Initialize a language model
lm = dspy.LM('openai/gpt-4o-mini')

# Make a direct call using a simple string
print("=== String-based LM Call ===")
string_prompt = "Explain what a language model is in one sentence."
string_response = lm(string_prompt)
print(f"Response: {string_response[0]}")

# Make a call using the structured message format
print("\n=== Structured Message LM Call ===")
# Hint: Create a list of message dictionaries with "role" and "content" keys
# and pass it to the LM using the messages parameter
messages = [
    {"role": "system", "content": "You are a helpful and concise assistant."},
    {"role": "user", "content": "Explain what a language model is in one sentence."}
]
structured_response = lm(messages=messages)
print(
    f"Response: {structured_response[0] if structured_response else 'No response'}")

# Compare history entries for both calls
print("\n=== History Comparison ===")
# Hint: Access the second-to-last call for the string-based call
# and the last call for the structured message call
string_call = lm.history[-2]
structured_call = lm.history[-1]

print("String call metadata keys:", string_call.keys())
print("Structured call metadata keys:", structured_call.keys())

# Examine the prompt format in history
print("\n=== Prompt Format in History ===")
# Hint: Print the 'prompt' field from both history entries to see
# how they differ between string and structured formats
print("String-based call 'prompt' field:")
print(repr(string_call.get('prompt')))
print("\nStructured call 'prompt' field:")
print(repr(structured_call.get('prompt')))
print("\nStructured call 'messages' field:")
print(structured_call.get('messages'))

# Display detailed metadata from the structured call
print("\n=== Detailed Metadata from Structured Call ===")
# Hint: Extract and print timestamp, parameters, and token usage
# from the structured call's history entry
print(f"Timestamp: {structured_call.get('timestamp')}")
print(f"Parameters (kwargs): {structured_call.get('kwargs')}")
print(f"Token usage: {structured_call.get('usage')}")
print(f"Cost: {structured_call.get('cost')}")
print(f"Model: {structured_call.get('model')}")

# TODO: Compare responses
print("\n=== Response Comparison ===")
# Hint: Print the 'response' field from both history entries
print("String-based call response (from history):")
print(string_call.get('response'))
print("\nStructured message call response (from history):")
print(structured_call.get('response'))

print("\n=== Summary ===")
print("String calls store the raw prompt in the 'prompt' field.")
print("Structured (messages=) calls store the chat history in the 'messages' field and usually leave 'prompt' as None or the rendered version.")
print("Both calls are recorded independently in lm.history with rich metadata (usage, cost, timestamp, etc.).")
