import asyncio
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
    async def agent_tool_function(message):
        # Call the agent asynchronously inside the tool (executed on the event loop)
        _, response = await agent.run([{"role": "user", "content": message}])

        print(f"📊 Agent ({agent.name}) as tool finished working")

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


async def main():
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
        "Call the calculator assistant to solve a single mathematical problem or equation."
    )

    # Create the orchestrator assistant
    orchestrator = Agent(
        name="orchestrator",
        system_prompt=(
            "You are a math orchestration coordinator. When given complex problems with multiple independent "
            "subproblems, you MUST break them down and delegate each subproblem to a separate calculator agent call. "
            "Issue multiple calculator_assistant_agent tool calls IN PARALLEL within the same turn for independent "
            "calculations. Each agent call should handle ONE specific calculation or equation. "
            "After all agents return results, synthesize them into a clear, complete final answer."
        ),
        tools={calculator_tool_schema["name"]: calculator_tool_function},
        tool_schemas=[calculator_tool_schema]
    )

    # Run the orchestrator on a problem that requires breaking into parallel subproblems
    messages = [
        {
            'role': 'user',
            'content': (
                'I need to calculate the total cost of three different purchases:\n'
                '- Store A: 15 items at $12.50 each, plus $8.99 shipping\n'
                '- Store B: 23 items at $9.75 each, plus $12.50 shipping\n'
                '- Store C: 8 items at $24.99 each, plus $6.25 shipping\n'
                'What is the grand total across all three stores?'
            )
        }
    ]
    result_messages, response = await orchestrator.run(messages)

    print('\n=== Final Response ===\n')
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
