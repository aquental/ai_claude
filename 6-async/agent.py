from anthropic import AsyncAnthropic


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
        self.client = AsyncAnthropic()
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

        all_tools = []

        if self.tool_schemas:
            all_tools.extend(self.tool_schemas)
        if self.handoffs:
            all_tools.append(self.handoff_schema)
        if all_tools:
            request_args["tools"] = all_tools

        return request_args

    def call_tool(self, tool_use):
        tool_name = tool_use.name
        tool_input = tool_use.input or {}
        tool_use_id = tool_use.id

        print(f"🔧 Tool called: {tool_name}({tool_input})")

        try:
            tool_fn = self.tools[tool_name]
        except KeyError:
            result = f"Error: Tool {tool_name} not found"
        except Exception as e:
            result = f"Error: {str(e)}"
        else:
            try:
                result = str(tool_fn(**tool_input))
            except Exception as e:
                result = f"Error: {str(e)}"

        return {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": result
        }

    async def call_handoff(self, tool_use, messages):
        agent_name = tool_use.input.get("name")
        reason = tool_use.input.get("reason", "No reason provided")

        print(f"🔄 Handoff to: {agent_name}")
        print(f"📝 Reason: {reason}")

        try:
            target_agent = next(
                agent for agent in self.handoffs if agent.name == agent_name)
            clean_messages = messages[:-
                                      1] if messages and messages[-1]["role"] == "assistant" else messages
            result = await target_agent.run(clean_messages)

            return True, result
        except StopIteration:
            return False, {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"Handoff failed: Agent '{agent_name}' not found. Available agents: {[agent.name for agent in self.handoffs]}"
            }
        except Exception as e:
            return False, {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": f"Handoff failed: Error during handoff to '{agent_name}': {str(e)}"
            }

    async def run(self, input_messages):
        # Create a copy of the input messages to avoid modifying the original
        messages = input_messages.copy()

        # Loop until the model returns a final answer or the max turns is reached
        turn = 0
        while turn < self.max_turns:
            turn += 1

            response = await self.client.messages.create(
                **self._build_request_args(messages)
            )

            messages.append({"role": "assistant", "content": response.content})

            # Execute all tools if Claude requests any
            if response.stop_reason == "tool_use":
                tool_results = []
                for content_item in response.content:
                    if content_item.type == "tool_use":
                        # Transfer control to another agent, if the tool use is a handoff
                        if content_item.name == "handoff":
                            handoff_success, handoff_result = await self.call_handoff(content_item, messages)
                            if handoff_success:
                                return handoff_result
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
