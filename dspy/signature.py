import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Define a signature for sentiment classification that takes a sentence as input
# and returns a sentiment as a boolean value (True for positive, False for negative)
classify = dspy.Predict('sentence -> sentiment: bool')

# Test with a positive example
positive_sentence = "it's a charming and often affecting journey."
result_positive = classify(sentence=positive_sentence)
print(f"Sentence: '{positive_sentence}'")
print(f"Sentiment: {result_positive.sentiment}")

# Test with a negative example
negative_sentence = "the film is a huge disappointment with poor acting and a weak plot."
result_negative = classify(sentence=negative_sentence)
print(f"Sentence: '{negative_sentence}'")
print(f"Sentiment: {result_negative.sentiment}")
