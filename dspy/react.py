import dspy
import os
import pprint

# Configure a language model
lm = dspy.LM('openai/gpt-4o-mini', api_key=os.environ['OPENAI_API_KEY'], api_base=os.environ['OPENAI_BASE_URL'])
dspy.configure(lm=lm)

# Define a tool function for mathematical calculations
def calculate_math(expression: str) -> float:
    """Evaluates a mathematical expression and returns the result."""
    return dspy.PythonInterpreter({}).execute(expression)

# Declare the ReAct module with a signature and the calculation tool
react = dspy.ReAct("question -> answer: float", tools=[calculate_math])

# Define a question that requires calculation
question = "If I have 5 boxes with 12 items in each, and I need to distribute them equally among 8 people, how many items will each person get?"

# Call the module with the question
pred = react(question=question)

# Helper function to traverse and pretty-print any nested structure
def traverse_and_print(obj, indent=0):
    prefix = "  " * indent
    if isinstance(obj, dict):
        print(f"{prefix}{{")
        for key, value in obj.items():
            print(f"{prefix}  {key}: ", end="")
            if isinstance(value, (dict, list)):
                print()
                traverse_and_print(value, indent + 1)
            else:
                print(repr(value))
        print(f"{prefix}}}")
    elif isinstance(obj, list):
        print(f"{prefix}[")
        for item in obj:
            traverse_and_print(item, indent + 1)
        print(f"{prefix}]")
    else:
        print(f"{prefix}{repr(obj)}")

print("ReAct - Reasoning and Acting framework")
print("Trajectory (fully traversed):")
traverse_and_print(pred.trajectory)

# Keep original prints for reference
print(f"\nReasoning:    {pred.reasoning}")
print(f"Answer:       {pred.answer}")
