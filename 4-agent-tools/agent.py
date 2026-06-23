import json
import anthropic


class Agent:
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

        # Avoid shared mutable defaults and protect against external mutation
        self.tools = {} if tools is None else dict(tools)
        self.tool_schemas = [] if tool_schemas is None else list(tool_schemas)

    def _extract_text(self, content):
        return "".join(
            block.text for block in content
            if getattr(block, "type", None) == "text"
        )

    def _build_request_args(self, messages):
        request_args = {
            "model": self.model,
            "system": self.system_prompt,
            "messages": messages,
            "max_tokens": 8000,
        }

        # Add tool schemas only if they exist
        if self.tool_schemas:
            request_args["tools"] = self.tool_schemas

        return request_args

    def call_tool(self, tool_use):
        tool_name = tool_use.name
        tool_input = tool_use.input or {}
        tool_use_id = tool_use.id

        print(f"🔧 Tool called: {tool_name}({tool_input})")

        try:
            result = str(self.tools[tool_name](**tool_input))
        except KeyError:
            result = f"Error: Tool {tool_name} not found"
        except Exception as e:
            result = f"Error: {str(e)}"

        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": result
        }

    def run(self, input_messages):
        # Create a copy of the input messages to avoid modifying the original
        messages = input_messages.copy()

        # Loop until the model returns a final answer or the max turns is reached
        turn = 0
        while turn < self.max_turns:
            turn += 1

            response = self.client.messages.create(
                **self._build_request_args(messages))

            messages.append({"role": "assistant", "content": response.content})

            # Execute all tools if Claude requests any
            if response.stop_reason == "tool_use":
                tool_results = []
                for content_item in response.content:
                    if content_item.type == "tool_use":
                        tool_result = self.call_tool(content_item)
                        tool_results.append(tool_result)

                # Add all tool results to messages
                messages.append({
                    "role": "user",
                    "content": tool_results
                })

            else:
                # Return if no tools are requested
                response_text = self._extract_text(response.content)

                return messages, response_text

        # If the max turns is reached, raise an exception
        raise Exception("Max turns reached")
