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


def filter_dataset(dataset, difficulty):
    """
    Filters a dataset of Example objects based on the difficulty level.
    """
    filtered_examples = []

    # Loop through each example in the dataset
    for example in dataset:
        # Check if the example's difficulty matches the specified difficulty
        if example.difficulty == difficulty:
            # If it matches, add the example to filtered_examples
            filtered_examples.append(example)

    # Return the filtered list
    return filtered_examples


# Filter the dataset for Easy questions
easy_examples = filter_dataset(programming_questions, "Easy")

# Use the separate_dataset function on the filtered results
easy_inputs, easy_labels = separate_dataset(easy_examples)

# Print the inputs and labels from the filtered examples
print("Easy Questions (Inputs):")
for ex in easy_inputs:
    print(ex)

print("\nEasy Questions (Labels):")
for ex in easy_labels:
    print(ex)


# Filter for Advanced questions
advanced_examples = filter_dataset(programming_questions, "Advanced")

# Use the separate_dataset function on the new filtered results
advanced_inputs, advanced_labels = separate_dataset(advanced_examples)

print("\nAdvanced Questions (Inputs):")
for ex in advanced_inputs:
    print(ex)

print("\nAdvanced Questions (Labels):")
for ex in advanced_labels:
    print(ex)
