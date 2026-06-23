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

# Define our complex problem
complex_problem = """
A rectangular garden is 12 meters long and 8 meters wide. 
How much fencing is needed to go around the perimeter? 
Also, if grass seed is needed at a rate of 0.25 kg per square meter, 
how much grass seed is required for the entire garden?
"""

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

# Create the initial message with the complex problem for the analyzer
analysis_messages = [{"role": "user", "content": complex_problem}]

# Run the problem analyzer to break down the problem into steps
analysis_messages, analysis_output = problem_analyzer.run(analysis_messages)

# Create the Calculator Agent with a system prompt that tells it to execute calculations using math tools
calculator = Agent(
    name="calculator",
    system_prompt=(
        "You are a Calculator agent specialized in performing mathematical operations. "
        "Use the available math tools to execute each calculation step from the plan. "
        "Follow the plan exactly, calling tools as needed. Provide the final numerical results."
    ),
    tools=math_tools,
    tool_schemas=tool_schemas
)

# Create calculation_messages by combining a prompt with the analysis_output from stage 1
calculation_prompt = (
    "Here is the step-by-step plan for solving the garden problem:\n"
    f"{analysis_output}\n\n"
    "Now execute the calculations using the available math tools. "
    "Provide the final answers for fencing needed and grass seed required."
)
calculation_messages = [{"role": "user", "content": calculation_prompt}]

# Run the calculator agent with the calculation_messages to get the calculation results
calculation_history, calculation_output = calculator.run(calculation_messages)

# Print the calculation_output to see the mathematical execution results
print("\nCalculation Results:")
print(calculation_output)
