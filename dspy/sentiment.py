import dspy
import os
from dspy.predict import Predict

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Example sentence for sentiment analysis
sentence = "it's a charming and often affecting journey."

# Step 1 - Declare a Predict module with a signature that takes a sentence and returns a boolean sentiment
classify = dspy.Predict('sentence -> sentiment: bool')

# Step 2 - Call the module with the sentence as input
sentence = "it's a charming and often affecting journey."
response = classify(sentence=sentence)

# Step 3 - Access and print the sentiment from the response
print(f"Sentence: {sentence}")
print(f"Sentiment (True = positive, False = negative): {response.sentiment}")
