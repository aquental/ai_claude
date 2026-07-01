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
    ).with_inputs("question")
]


def separate_dataset(dataset):
    """
    Separates a dataset of Example objects into two lists:
    one containing only input fields and one containing only label fields.

    Args:
        dataset: A list of Example objects

    Returns:
        A tuple of (input_list, label_list) where each list contains Example objects
    """
    input_list = []
    label_list = []

    # Loop through each example in the dataset
    for example in dataset:
        # Add its input fields to input_list
        input_list.append(example.inputs())
        # Add its label fields to label_list
        label_list.append(example.labels())

    # Return both lists as a tuple
    return input_list, label_list


# Test the function with our dataset
input_examples, label_examples = separate_dataset(programming_questions)

# Print the results
print("Input fields from dataset:")
for ex in input_examples:
    print(ex)

print("\nLabel fields from dataset:")
for ex in label_examples:
    print(ex)
