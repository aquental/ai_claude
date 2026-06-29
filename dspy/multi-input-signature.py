import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Create a string-based signature for retrieval-augmented question answering
# The signature should take a context (list of strings) and a question (string) as inputs
# and return an answer (string) as output
generate_answer = dspy.Predict("context: list[str], question -> answer")

# Example context passages
contexts = [
    "The Great Wall of China is a series of fortifications that were built across the historical northern borders of ancient Chinese states and Imperial China as protection against various nomadic groups from the Eurasian Steppe.",
    "Construction began in the 7th century BC and the walls were built and rebuilt over many centuries. The most well-known sections were built by the Ming dynasty (1368–1644).",
    "The Great Wall is approximately 13,171 miles (21,196 kilometers) long, although not all sections are still visible today."
]

# Example question
question = "When was the Great Wall of China built?"

# Use the signature to generate an answer
prediction = generate_answer(context=contexts, question=question)

# Print the answer
print("Answer:", prediction.answer)
