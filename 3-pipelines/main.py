import json
from agent import Agent
from functions import (
    sum_numbers,
    multiply_numbers,
    subtract_numbers,
    divide_numbers,
    power,
    square_root
)

# Load tool schemas
with open('schemas.json', 'r') as f:
    tool_schemas = json.load(f)

# Math tools
math_tools = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "subtract_numbers": subtract_numbers,
    "divide_numbers": divide_numbers,
    "power": power,
    "square_root": square_root
}

# Agent 1: Problem Analyzer
problem_analyzer = Agent(
    name="problem_analyzer",
    system_prompt=(
        "You are a mathematical problem analyzer. Your job is to:\n"
        "1. Break down complex math problems into clear, sequential steps\n"
        "2. Identify what calculations are needed at each step\n"
        "3. Output a structured plan that another agent can follow to perform "
        "calculations\n"
        "4. Do NOT perform the actual calculations - just create the "
        "step-by-step plan"
    )
)

# Agent 2: Calculator Agent
calculator_agent = Agent(
    name="calculator_agent",
    system_prompt=(
        "You are a calculator agent. Your job is to:\n"
        "1. Take a step-by-step calculation plan\n"
        "2. Execute each calculation using your available math tools\n"
        "3. Show your work clearly for each step\n"
        "4. Provide the numerical results in a structured format"
    ),
    tools=math_tools,
    tool_schemas=tool_schemas,
)

# Agent 3: Solution Presenter
solution_presenter = Agent(
    name="solution_presenter",
    system_prompt=(
        "You are a solution presenter. Your job is to:\n"
        "1. Take calculation results and present them as a complete, "
        "educational solution\n"
        "2. Explain what each step accomplished and why it was necessary\n"
        "3. Provide the final answer clearly\n"
        "4. Make the solution easy to understand for someone learning math"
    )
)

# Define our complex problem
complex_problem = """
A rectangular garden is 12 meters long and 8 meters wide. 
How much fencing is needed to go around the perimeter? 
Also, if grass seed is needed at a rate of 0.25 kg per square meter, 
how much grass seed is required for the entire garden?
"""

# Create the initial message with the complex problem for the analyzer
analysis_messages = [{"role": "user", "content": complex_problem}]

# Run the problem analyzer to break down the problem into steps
analysis_messages, analysis_output = problem_analyzer.run(analysis_messages)

# Pass the analysis plan to the calculator agent for execution
calculation_messages = [
    {
        "role": "user",
        "content": (
            "Execute this calculation plan: "
            f"{analysis_output}"  # Insert the step-by-step plan from stage 1
        ),
    }
]

# Run the calculator agent to perform all mathematical operations
calculation_messages, calculation_output = calculator_agent.run(
    calculation_messages)

# Add a validation request message to the existing calculation_messages asking the agent to validate its work and respond with only True or False
validation_request = (
    "\n\nValidate your previous calculations. "
    "Double-check all arithmetic. "
    "Respond with ONLY the word 'True' if everything is correct, "
    "or 'False' if there is any error."
)
calculation_messages.append({"role": "user", "content": validation_request})

# Run the calculator agent again using the existing calculation_messages to get the validation response
calculation_messages, validation_response = calculator_agent.run(
    calculation_messages)

# Check if the validation response contains "True" and store this result in validation_passed
validation_passed = "True" in validation_response

# Print the validation stage results showing the response and whether validation passed
print("\n=== VALIDATION STAGE ===")
print(f"Validation Response: {validation_response}")
print(f"Validation Passed: {validation_passed}")

# Only proceed to create and run the Solution Presenter if validation_passed is True, otherwise print an error message
if not validation_passed:
    print("\n❌ Validation failed. Aborting presentation stage.")
    presentation_output = "Validation failed - cannot proceed to final solution."
else:
    # Combine original problem and calculation results for final presentation
    presentation_prompt = (
        "Present this solution clearly based on the original problem and "
        "calculations:\n\n"
        f"Original Problem: {complex_problem}\n\n"    # Provide context
        # Include all calculations
        f"Calculation Results: {calculation_output}"
    )
# Create the final message for the solution presenter
presentation_messages = [{"role": "user", "content": presentation_prompt}]

# Run the solution presenter to create the final educational output
presentation_messages, presentation_output = solution_presenter.run(
    presentation_messages)

# Display the final output
print("\n=== PRESENTATION STAGE ===")
print(presentation_output)
