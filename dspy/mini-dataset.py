import dspy

# Create a list of at least three Example objects representing a mini-dataset
# Each Example should have question, answer, and a metadata field (like difficulty or category)
# Don't forget to mark the question field as the input for each Example
programming_questions = [
    dspy.Example(
        question="What is the difference between a list and a tuple in Python?",
        answer="Lists are mutable (can be modified), use [], and are generally slower. Tuples are immutable, use (), are faster, and hashable.",
        category="Python basics",
        difficulty="easy"
    ).with_inputs("question"),

    dspy.Example(
        question="How does list comprehension work in Python?",
        answer="List comprehension provides a concise way to create lists. Example: [x**2 for x in range(10)]",
        category="Python basics",
        difficulty="medium"
    ).with_inputs("question"),

    dspy.Example(
        question="Explain what a decorator is in Python.",
        answer="A decorator is a function that takes another function and extends its behavior without explicitly modifying it. Commonly used with @ syntax.",
        category="Python advanced",
        difficulty="hard"
    ).with_inputs("question"),
]

# Iterate through the dataset and print inputs and labels for each Example
print("Mini Programming Q&A Dataset:\n")
for i, ex in enumerate(programming_questions, 1):
    print(f"Example {i}:")
    print(f"  Inputs  : {ex.inputs()}")
    print(f"  Labels  : {ex.labels()}")
    print("-" * 60)
