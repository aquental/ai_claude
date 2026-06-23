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


def create_agent_tool(agent, description):
    """
    Create a tool function and schema for using an agent as a tool.
    
    Args:
        agent: The agent to wrap as a tool
        description: Description of what this agent tool does
    
    Returns:
        tuple: (tool_function, tool_schema)
    """
    def agent_tool_function(message):
        print(f"🦾 Agent tool called ({agent.name}): {message}")
        
        # Call the agent
        _, response = agent.run([{"role": "user", "content": message}])
        
        print(f"📊 Agent response ({agent.name}): {response}")
        
        return response
    
    # Create schema for this agent tool
    tool_schema = {
        "name": f"{agent.name}_agent",
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to send to the agent"
                }
            },
            "required": ["message"]
        }
    }
    
    return agent_tool_function, tool_schema


# Create a calculator assistant
calculator_assistant = Agent(
    name="calculator_assistant",
    system_prompt="You are a calculator assistant. You specialize in mathematical calculations and solving equations.",
    tools=math_tools,
    tool_schemas=tool_schemas
)

# Create agent tool for calculator
calculator_tool_function, calculator_tool_schema = create_agent_tool(
    calculator_assistant,
    "Call the calculator assistant to solve mathematical problems and equations."
)

# Create a general assistant
helpful_assistant = Agent(
    name="helpful_assistant",
    system_prompt="You are a helpful assistant. You can assist with various tasks and use the calculator tool for math problems.",
    tools={calculator_tool_schema["name"]:calculator_tool_function},
    tool_schemas=[calculator_tool_schema]
)

# Create a message list with a general knowledge question
messages = [
    {
        'role': 'user', 
        'content': 'What is the capital of France?'
    }
]

# Run the orchestrator agent
result_messages, response = helpful_assistant.run(messages)

# Display the orchestrator's response to the user
print(response)

# Create a message list with a general knowledge question
messages = [
    {
        'role': 'user', 
        'content': 'What is the solution to the equation x² - 5x + 6 = 0?'
    }
]

# Run the orchestrator agent
result_messages, response = helpful_assistant.run(messages)

# Display the orchestrator's response to the user
print('\n=== Final Response ===\n')
print(response)
