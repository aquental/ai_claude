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

# Create the Solution Presenter Agent with a system prompt that tells it to present calculation results as educational solutions
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

# Create presentation_prompt that combines the original problem and calculation results for final presentation
presentation_prompt = (
    f"Original problem:\n{complex_problem}\n\n"
    f"Calculation results:\n{calculation_output}\n\n"
    "Present this as a complete educational solution."
)
# Create presentation_messages with the presentation_prompt for the solution presenter
presentation_messages = [{"role": "user", "content": presentation_prompt}]

# Run the solution presenter agent to create the final educational output
presentation_messages, presentation_output = solution_presenter.run(
    presentation_messages)

# Print the presentation_output to see the complete pipeline result
print("\n=== FINAL EDUCATIONAL SOLUTION ===")
print(presentation_output)
