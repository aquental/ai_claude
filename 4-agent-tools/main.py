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
    """
    def agent_tool_function(message):
        print(f"🦾 Agent tool called ({agent.name}): {message}")
        
        _, response = agent.run([{"role": "user", "content": message}])
        
        print(f"📊 Agent response ({agent.name}): {response}")
        return response
    
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


# === Sub-agents ===
calculator_assistant = Agent(
    name="calculator_assistant",
    system_prompt="You are a calculator assistant. You specialize in mathematical calculations and solving equations.",
    tools=math_tools,
    tool_schemas=tool_schemas
)

verifier_assistant = Agent(
    name="verifier_assistant",
    system_prompt="You are a solution verifier. You specialize in checking and verifying mathematical calculations and solutions.",
    tools=math_tools,
    tool_schemas=tool_schemas
)

# === Agent Tools ===
calculator_tool_function, calculator_tool_schema = create_agent_tool(
    calculator_assistant,
    "Call the calculator assistant to solve mathematical problems and equations."
)

verifier_tool_function, verifier_tool_schema = create_agent_tool(
    verifier_assistant,
    "Call the verifier assistant to double-check and verify mathematical calculations and solutions."
)

# === Main Orchestrator ===
helpful_assistant = Agent(
    name="helpful_assistant",
    system_prompt=(
        "You are a helpful assistant. You can assist with various tasks. "
        "For any mathematical problem, use the calculator tool to get the solution "
        "and the verifier tool to double-check the result before giving the final answer."
    ),
    tools={
        calculator_tool_schema["name"]: calculator_tool_function,
        verifier_tool_schema["name"]: verifier_tool_function,
    },
    tool_schemas=[calculator_tool_schema, verifier_tool_schema]
)

# Test
messages = [
    {
        'role': 'user', 
        'content': 'What is the solution to the equation 4x - 7 = 9?'
    }
]

result_messages, response = helpful_assistant.run(messages)

print('\n=== Final Response ===\n')
print(response)
