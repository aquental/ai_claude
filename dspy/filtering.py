import dspy

# Sample mini-dataset of programming questions
programming_questions = [
    dspy.Example(
        question="What is the difference between a list and a tuple in Python?",
        answer="Lists are mutable and can be modified after creation, while tuples are immutable and cannot be changed after creation.",
        difficulty="Easy"
    ).with_inputs("question"),

    dspy.Example(
        question="How do you handle exceptions in Python?",
        answer="Exceptions in Python are handled using try-except blocks. You can also use finally to execute code regardless of whether an exception occurred.",
        difficulty="Medium"
    ).with_inputs("question"),

    dspy.Example(
        question="Explain the concept of decorators in Python.",
        answer="Decorators are functions that modify the behavior of other functions. They allow you to wrap a function to extend its functionality without modifying its code.",
        difficulty="Advanced"
    ).with_inputs("question"),

    dspy.Example(
        question="What are list comprehensions in Python?",
        answer="List comprehensions are a concise way to create lists in Python. They consist of brackets containing an expression followed by a for clause, then zero or more for or if clauses.",
        difficulty="Easy"
    ).with_inputs("question"),

    dspy.Example(
        question="How does garbage collection work in Python?",
        answer="Python uses reference counting and a cyclic garbage collector. When an object's reference count drops to zero, it's deallocated. The cyclic garbage collector identifies and collects objects in reference cycles that are no longer accessible.",
        difficulty="Advanced"
    ).with_inputs("question")
]


def filter_dataset(dataset, difficulty):
    """
    Filters a dataset of Example objects based on the difficulty level.

    Args:
        dataset: A list of Example objects
        difficulty: The difficulty level to filter by (e.g., "Easy", "Medium", "Advanced")

    Returns:
        A list of Example objects that match the specified difficulty
    """
    filtered_examples = []

    for example in dataset:
        if example.difficulty == difficulty:
            filtered_examples.append(example)

    return filtered_examples


def separate_dataset(dataset):
    """
    Separates a dataset of Example objects into two lists:
    one containing only input fields and one containing only label fields.
    """
    input_list = []
    label_list = []

    for example in dataset:
        input_list.append(example.inputs())
        label_list.append(example.labels())

    return input_list, label_list


def transform_questions(examples):
    """
    Transforms the question field in each Example by adding a prefix.
    Maintains the same input field marking.
    """
    transformed_examples = []

    # Loop through each example
    for example in examples:
        # Create transformed question
        new_question = "Question: " + example.question

        # Create a new Example with the transformed question (copy other fields)
        transformed = dspy.Example(
            question=new_question,
            answer=example.answer,
            difficulty=example.difficulty
        )

        # Make sure to mark the question as the input field
        transformed = transformed.with_inputs("question")

        # Add to the list
        transformed_examples.append(transformed)

    return transformed_examples


# Filter the dataset for Easy questions
easy_questions = filter_dataset(programming_questions, "Easy")
print(f"Found {len(easy_questions)} Easy questions")

# Print original questions before transformation
print("\nOriginal Easy Questions:")
for i, example in enumerate(easy_questions):
    print(f"{i+1}. {example.question}")

# Apply the transformation to the filtered dataset
transformed_easy = transform_questions(easy_questions)

# Print the transformed questions
print("\nTransformed Easy Questions:")
for i, example in enumerate(transformed_easy):
    print(f"{i+1}. {example.question}")

# Separate the transformed examples into inputs and labels
inputs_list, labels_list = separate_dataset(
    transformed_easy)  # using the function from before

print("\nSeparated Inputs (after transformation):")
for ex in inputs_list:
    print(ex)

print("\nSeparated Labels (after transformation):")
for ex in labels_list:
    print(ex)
