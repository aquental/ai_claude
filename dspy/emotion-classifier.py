import dspy
import os
from typing import Literal

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)


# Create a class-based signature for emotion classification
# The class should inherit from dspy.Signature and include a descriptive docstring
class Emotion(dspy.Signature):
    """Classify emotion."""
    # Define input field for the sentence and output field for the sentiment
    sentence: str = dspy.InputField(desc="Relevant information to distill the sentiment")
    # Use Literal type to constrain the output to specific emotions
    sentiment: Literal['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'] = dspy.OutputField(desc="A concise sentiment based solely on the provided phrase")
    # Add helpful descriptions to both fields using the desc parameter

# Example sentence to classify
sentence = "i started feeling a little vulnerable when the giant spotlight started blinding me"

# Create a predictor using your Emotion signature
classify = dspy.Predict(Emotion)
# Use the predictor to classify the sentence
result = classify(sentence=sentence)
# Print the result
print(result.sentiment)
