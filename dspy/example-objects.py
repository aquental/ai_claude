import dspy

# Create an Example object with three fields: question, answer, and category
qa_example = dspy.Example(
    question="What is the difference between a list and a tuple in Python?",
    # Add the missing fields here
    answer="Lists are mutable (can be modified: append, remove, etc.), use [], and are generally slower.\nTuples are immutable (cannot be changed after creation), use (), are faster, and hashable (usable as dict keys).\nUse lists for dynamic sequences; tuples for fixed data.",
    category="Python programming"
)

# Mark only the question as an input field
qa_example = qa_example.with_inputs("question")

# Print the entire Example object
print(f"Complete Example object: {qa_example}")

# Print individual fields using dot notation
print("\nAccessing individual fields:")
print(f"\tQuestion:   {qa_example.question}")
print(f"\t- Answer:     {qa_example.answer}")
print(f"\t- Category:   {qa_example.category}")
# Print only the input fields
input_fields = qa_example.inputs()
print(f"\nInput fields only: {input_fields}")
non_input_fields = qa_example.labels()
# Print only the non-input fields (labels)
print(f"\nNon-input fields only: {non_input_fields}")
