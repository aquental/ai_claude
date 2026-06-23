from agent import Agent

# Define our complex problem
complex_problem = """
A rectangular garden is 12 meters long and 8 meters wide. 
How much fencing is needed to go around the perimeter? 
Also, if grass seed is needed at a rate of 0.25 kg per square meter, 
how much grass seed is required for the entire garden?
"""

# Create the Problem Analyzer Agent with a system prompt that tells it to break down problems into steps without doing calculations
analyzer = Agent(
    name="Problem Analyzer",
    system_prompt=(
        "You are a Problem Analyzer agent. Break down the given problem into clear, sequential steps. "
        "List each step explicitly. Do not perform any calculations or provide numerical answers. "
        "Focus only on the reasoning structure and what needs to be computed in each step."
    )
)
# Create the initial message with the complex problem for the analyzer
analysis_messages = [{"role": "user", "content": complex_problem}]

# Run the problem analyzer agent with the analysis_messages to break down the problem into steps
analysis_history, analysis_output = analyzer.run(analysis_messages)

# Print the analysis output to see how the agent breaks down the problem
print("Problem Analysis:")
print(analysis_output)
