import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Declare a ChainOfThought module with a signature that takes a question and returns an answer
math = dspy.ChainOfThought("question -> answer: float")

# Define the math problem
question = "Two dice are tossed. What is the probability that the sum equals two?"

# Call the module with the problem
response = math(question=question)

# Access and print both the reasoning and the answer
print(f" - Reasoning: {response.reasoning}")
print(f" - Answer: {response.answer}")
