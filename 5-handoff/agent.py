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
        handoffs=None,
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
        self.handoffs = [] if handoffs is None else list(
            handoffs)  # list of other agents to handoff the control

        # Define handoff tool schema
        self.handoff_schema = {
            "name": "handoff",
            "description": "Transfer control to another specialized agent. Use this when the user's request is better handled by a different agent.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": f"Name of the agent to handoff to. Available agents: {[agent.name for agent in self.handoffs]}"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Brief explanation of why this handoff is needed"
                    }
                },
                "required": ["name", "reason"]
            }
        }

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

        # Build the complete tool schemas list
        all_tools = []

        # Add regular tool schemas if they exist
        if self.tool_schemas:
            all_tools.extend(self.tool_schemas)

        # Add handoff schema if handoffs are available
        if self.handoffs:
            all_tools.append(self.handoff_schema)

        # Add tools to request if any exist
        if all_tools:
            request_args["tools"] = all_tools

        # Return the complete set of arguments to use for the API call
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

    def call_handoff(self, tool_use, messages):
        # Extract the agent name from the handoff tool input
        agent_name = tool_use.input.get("name")
        reason = tool_use.input.get("reason", "No reason provided")

        print(f"🔄 Handoff to: {agent_name}")
        print(f"📝 Reason: {reason}")

        try:
            # Find the agent with the given name (raises StopIteration if not found)
            target_agent = next(
                agent for agent in self.handoffs if agent.name == agent_name)

            # Remove the last assistant message that contains the handoff tool_use
            clean_messages = messages[:-
                                      1] if messages and messages[-1]["role"] == "assistant" else messages

            # Handoff the control to the other agent
            return True, target_agent.run(clean_messages)

        except StopIteration:
            # Agent not found
            return False, {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"Handoff failed: Agent '{agent_name}' not found. Available agents: {[agent.name for agent in self.handoffs]}"
            }
        except Exception as e:
            # Any other error during handoff execution
            return False, {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"Handoff failed: Error during handoff to '{agent_name}': {str(e)}"
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
                        # If the tool use is a handoff
                        if content_item.name == "handoff":
                            # Try to transfer control to another agent
                            handoff_success, handoff_result = self.call_handoff(
                                content_item, messages)
                            # If handoff was successful, return the result from the other agent
                            if handoff_success:
                                return handoff_result
                            # If handoff failed, treat it as a regular tool result
                            else:
                                tool_results.append(handoff_result)
                        else:
                            # Execute regular tools
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
