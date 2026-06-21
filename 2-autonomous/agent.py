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

    def _extract_text(self, content):
        # Return a joined string of all text blocks from content
        return "".join(
            block.text for block in content
            if getattr(block, "type", None) == "text"
        )

    def _build_request_args(self, messages):
        # Create a dictionary with the basic request arguments
        request_args = {
            "model": self.model,
            "system": self.system_prompt,
            "messages": messages,
            "max_tokens": 8000,
        }

        # Add tool schemas only if they exist
        if self.tool_schemas:
            request_args["tools"] = self.tool_schemas

        # Return the complete set of arguments to use for the API call
        return request_args

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

    def run(self, input_messages):
        # Create a copy of the input messages to avoid modifying the original
        messages = input_messages.copy()
        # Initialize turn counter to track iterations
        turn = 0
        # Loop until the model returns a final answer or the max turns is reached
        while turn < self.max_turns:
            # Increment the turn
            turn += 1
            # Ask the model for a response
            response = self.client.messages.create(
                **self._build_request_args(messages))
            # Add Claude's response to messages exactly as returned (text + tool_use blocks)
            messages.append({"role": "assistant", "content": response.content})

            # Check if Claude wants to use any tools
            if response.stop_reason == "tool_use":
                # Initialize a list to store tool results
                tool_results = []
                # Execute each tool use
                for content_item in response.content:
                    # Check if the content item is a tool use
                    if content_item.type == "tool_use":
                        # Execute the tool with the input the given input
                        tool_result = self.call_tool(content_item)
                        # Add result to tool results list
                        tool_results.append(tool_result)
                # Add all tool results to messages
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                # Extract the text from the response
                response_text = self._extract_text(response.content)
                # Return the agent history and final output
                return messages, response_text

        # If the max turns is reached, raise an exception
        raise Exception("Max turns reached")
