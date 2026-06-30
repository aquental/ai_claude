import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Declare the ProgramOfThought module with a signature that takes a question and returns an answer
example = dspy.ProgramOfThought("question -> answer")

# Define the candy distribution problem
question = "I have 15 candies, and I want to distribute them equally among 6 friends. How many candies will each friend get, and how many will I have left over?"

# Call the module with the problem
result = example(question=question)

# Access and print the answer
print(f"Question: {question}")
print(f"After ProgramOfThought process:")
print(f"\t- Final Reasoning: {result.reasoning}")
print(f"\t- Final Predicted Answer: {result.answer}")
