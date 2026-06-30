import dspy
import os

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini',
             api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)


# Define a signature for multiple-choice questions with input fields for question and options,
# and output fields for answer and reasoning
class MultipleChoice(dspy.Signature):
    """Answer multiple choice questions by comparing options."""

    question = dspy.InputField()
    options = dspy.InputField()
    answer = dspy.OutputField(desc="The correct answer (A, B, C, or D)")
    reasoning = dspy.OutputField(desc="Explanation for the answer")


# Create a basic predictor using the signature
predictor = dspy.Predict(MultipleChoice)

# Create a MultiChainComparison module with M=3 (to compare 3 reasoning paths)
mc_solver = dspy.MultiChainComparison(MultipleChoice, M=3)

# Define a multiple-choice question
question = "Which planet is known as the 'Red Planet'?"
options = {
    "A": "Venus",
    "B": "Mars",
    "C": "Jupiter",
    "D": "Saturn"
}

# Generate multiple predictions (at least 3) using the basic predictor
completions = [predictor(question=question, options=options) for _ in range(3)]

# Use MultiChainComparison to select the best answer based on the generated predictions
result = mc_solver(completions=completions, question=question, options=options)

# Display the question, options, selected answer, and reasoning
print(f"Question: {question}")
print(f"Options: {options}")
print(f"Answer:    {result.answer}")
print(f"Rationale: {result.rationale}")
print(f"Reasoning: {result.reasoning}")
