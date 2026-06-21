import json
import anthropic


class Agent:
    # Base system prompt to be used for all agents
    BASE_SYSTEM_PROMPT = (
        "You are an autonomous agent that can take multiple tool-calling steps when helpful. "
        "The user only sees your response when you stop using tools, not your tool usage or reasoning steps. "
        "When you provide your answer without calling tools, make it complete and standalone.\n"
        "Additional instructions:\n"
    )

    def __init__(
        self,
        name,
        system_prompt="You are a helpful assistant.",
        model="claude-sonnet-4-6",
        tools=None,
        tool_schemas=None,
        max_turns=10
    ):
        self.client = anthropic.Anthropic()
        self.name = name
        self.model = model
        self.system_prompt = self.BASE_SYSTEM_PROMPT + system_prompt
        self.max_turns = max_turns
        self.tools = {} if tools is None else dict(tools)
        self.tool_schemas = [] if tool_schemas is None else list(tool_schemas)

    def call_tool(self, tool_use):
        # Get the tool name, input, and id
        tool_name = tool_use.name
        tool_input = tool_use.input or {}
        tool_use_id = tool_use.id

        # Display which tool is being called
        print(f"🔧 Tool called: {tool_name}({tool_input})")

        try:
            # Execute the tool with the input the given input
            result = str(self.tools[tool_name](**tool_input))
        except KeyError:
            # Return an error message if the tool is not found
            result = f"Error: Tool {tool_name} not found"
        except Exception as e:
            # Return an error message if the tool fails
            result = f"Error: {str(e)}"

        # Return the tool result
        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": result
        }
