from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()

# Choose a model to use
model = "claude-sonnet-4-6"

# Step 1: Ask Claude to write a summary with specific character constraints
summary_prompt = "You are a helpful assistant that writes clear, concise summaries."

summary_messages = [
    {
        "role": "user",
        "content": "Write up to 300 characters summary of artificial intelligence and its current applications in healthcare."
    }
]

# Send the first request to Claude for summary generation
summary_response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=summary_messages,
    system=summary_prompt
)

# Extract the summary text from Claude's response
summary_text = summary_response.content[0].text
print("Summary:")
print(summary_text)

# Step 2: Validate that the summary meets our character requirements
if not (250 <= len(summary_text) <= 350):
    raise ValueError(
        f"Summary does not meet character requirement (250-350 characters). Got {len(summary_text)} characters.")

print(
    f"✅ SUCCESS: Summary meets character requirement: {len(summary_text)} characters")

# Step 3: Chain the summary output as input to a translation task
translation_prompt = "You are a professional translator that provides accurate Spanish translations."

translation_messages = [
    {
        "role": "user",
        "content": f"Return me just the Spanish translation of the following text:\n\n{summary_text}"
    }
]

# Send the second request to Claude using the summary from the first call
translation_response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=translation_messages,
    system=translation_prompt
)

# Extract and display the final translation result
translation_text = translation_response.content[0].text
print("Spanish Translation:")
print(translation_text)

# Step 4: Review the translation quality by comparing both versions
# Create a system prompt that establishes Claude as a bilingual translation reviewer who can assess translation quality and accuracy
review_prompt = "You are a bilingual translation reviewer who can assess translation quality and accuracy"

# Create the messages list with a user message that uses f-string formatting to include both the summary_text (English) and translation_text (Spanish) while requesting feedback on translation quality
review_messages = [
    {
        "role": "user",
        "content": f"Compare the quality of the translation of the following text:\n\n{summary_text}\n\n with the spanish: {translation_text}"
    }
]

# Make the API call to Claude with model, max_tokens=2000, messages, and system parameters
review_response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=review_messages,
    system=review_prompt
)

# Extract the feedback text from the response and assign it to feedback_text
feedback_text = review_response.content[0].text

print("Translation Feedback:")
print(feedback_text)
