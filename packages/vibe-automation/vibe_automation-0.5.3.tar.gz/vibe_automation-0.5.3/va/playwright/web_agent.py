import base64
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from playwright.async_api import Page
from ..agent.agent import Agent


log = logging.getLogger("va.playwright.web_agent")


# Define available tools (Anthropic format)
TOOLS = [
    {
        "name": "get_page_snapshot",
        "description": "Get an AI-optimized snapshot of the current page structure",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "execute_python_command",
        "description": "Execute a Python command to interact with the page",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Python command to execute",
                }
            },
            "required": ["command"],
        },
    },
    {
        "name": "find_element_by_ref",
        "description": "Find an element by its ref from the AI snapshot",
        "input_schema": {
            "type": "object",
            "properties": {
                "ref": {
                    "type": "string",
                    "description": "Element ref (e.g., 'e3')",
                }
            },
            "required": ["ref"],
        },
    },
    {
        "name": "get_page_screenshot",
        "description": "Take a screenshot of the current page",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


def build_system_prompt(command: str, context: Dict[str, Any]) -> str:
    """Build the system prompt for the interactive executor."""
    context_str = json.dumps(context, indent=2) if context else "{}"

    return f"""You are an expert web automation engineer helping to execute this command with Playwright: "{command}"

Context variables available: {context_str}

You have access to the following tools:
1. get_page_snapshot() - Get the current page structure as an AI-optimized accessibility tree
2. execute_python_command(command) - Execute Python code to interact with the page
3. find_element_by_ref(ref) - Find an element by its ref from the snapshot and get a locator string
4. get_page_screenshot() - Take a screenshot of the current page

Your goal is to:
1. Understand the current page structure using get_page_snapshot()
2. Identify the elements you need to interact with
3. Test different approaches using execute_python_command()
4. Build up the final script gradually, testing each step
5. Use refs from the snapshot to locate elements precisely

Guidelines:
- Use the page snapshot to understand the page structure, and use the page screenshot if needed to better understand the page structure and verify action result
- Use refs (like [ref=e3]) to locate specific elements
- Test each command before adding it to the final script
- Build the script incrementally, verifying each step works
- Use context variables with context["key"] syntax, don't directly use the variable value directly since we want the generated code to be reusable.
- Always use async/await for page interactions
- Prefer to use Playwright native methods to achieve the task, instead of using page.evaluate with custom JavaScript code.

NOTE that Python Playwright APIs uses snake_case naming such as select_option instead of selectOption.

When you're done, provide the final working script in this format:
```python
# Final working script
await page.click("button")
# ... more commands
```

Start by getting the page snapshot to understand what you're working with."""


@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation."""

    role: str  # "user", "tool" or "assistant"
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None
    tool_name: Optional[str] = None  # Only if role is tool


class WebAgent(Agent):
    """
    Web automation agent that allows the LLM to gradually build a script
    by using tools to explore and interact with the page.
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.conversation_history: List[ConversationTurn] = []
        self.final_script = ""
        self.working_script_lines: List[str] = []

    def add_conversation_turn(
        self,
        role: str,
        content: str,
        tool_calls=None,
        tool_results=None,
        tool_name=None,
    ):
        """Add a turn to the conversation history and print it immediately."""
        turn = ConversationTurn(
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results,
            tool_name=tool_name,
        )
        self.conversation_history.append(turn)

        # Stream the conversation turn immediately
        self._print_conversation_turn(len(self.conversation_history), turn)

    def _print_conversation_turn(
        self,
        turn_number: int,
        turn: ConversationTurn,
        log_level: str = "debug",
    ):
        """Print a single conversation turn in a formatted way."""

        if log_level == "debug":
            log_fn = log.debug
        else:
            log_fn = log.info

        log_fn(f"\n--- Turn {turn_number}: {turn.role.upper()} {turn.tool_name} ---")

        if turn.content:
            log_fn(f"Content: {turn.content}")

        if turn.tool_calls:
            log_fn("Tool Calls:")
            for j, tool_call in enumerate(turn.tool_calls, 1):
                log_fn(f"  {j}. {tool_call.name}")
                if hasattr(tool_call, "input") and tool_call.input:
                    for key, value in tool_call.input.items():
                        # Truncate long values for readability
                        display_value = str(value)
                        if len(display_value) > 100:
                            display_value = display_value[:97] + "..."
                        log_fn(f"     {key}: {display_value}")

        if turn.tool_results:
            log_fn("Tool Results:")
            for j, result in enumerate(turn.tool_results, 1):
                result_content = result.get("content", "No content")
                # Truncate long results for readability
                if len(result_content) > 200:
                    result_content = result_content[:197] + "..."
                log_fn(f"  {j}. {result_content}")

    async def get_page_snapshot(self) -> str:
        """Tool: Get an AI-optimized snapshot of the current page."""
        try:
            # Use our monkey-patched method
            snapshot = await self.page.snapshot_for_ai()
            return snapshot
        except Exception as e:
            log.error(f"Failed to get page snapshot: {e}")
            return f"Error getting page snapshot: {e}"

    async def execute_python_command(
        self, command: str, context: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """Tool: Execute a Python command on the page and return success status and result."""
        try:
            # Create execution context with captured output
            captured_output = []
            execution_context = {
                "page": self.page,
                "print": lambda *args: captured_output.append(
                    " ".join(str(arg) for arg in args)
                ),
                "context": context,
            }

            result = None
            # Handle async commands
            if "await " in command:
                # Wrap in async function and capture return value
                async_command = f"""
async def __execute_command():
    {command.replace(chr(10), chr(10) + "    ")}
    
__result = __execute_command()
"""
                exec(compile(async_command, "<string>", "exec"), execution_context)
                if "__result" in execution_context:
                    result = await execution_context["__result"]
            else:
                # Execute synchronous command and capture return value
                result = exec(command, execution_context)

            # Build response message
            response_parts = []
            if captured_output:
                response_parts.append("Output: " + "\n".join(captured_output))
            if result is not None:
                response_parts.append(f"Return value: {result}")
            if not response_parts:
                response_parts.append("Command executed successfully")

            return True, "\n".join(response_parts)
        except Exception as e:
            return False, f"Error executing command: {e}"

    async def find_element_by_ref(self, ref: str) -> Optional[str]:
        """Tool: Find an element by its ref from the AI snapshot and return a locator string."""
        try:
            locator = self.page.locator(f"aria-ref={ref}")
            count = await locator.count()

            if count > 0:
                # Generate locator string for the element
                locator_string = await locator.first.generate_locator_string()
                return "page." + locator_string
            else:
                return None
        except Exception as e:
            log.error(f"Failed to find element by ref {ref}: {e}")
            return None

    async def get_page_screenshot(self) -> str:
        """Tool: Take a screenshot of the current page."""
        try:
            # Take screenshot and return as base64 string
            screenshot_bytes = await self.page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            return screenshot_base64
        except Exception as e:
            log.error(f"Failed to take screenshot: {e}")
            return f"Error taking screenshot: {e}"

    async def process_anthropic_tool_call(
        self, tool_call, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single Anthropic tool call and return the result."""
        tool_name = tool_call.name
        arguments = tool_call.input

        try:
            if tool_name == "get_page_snapshot":
                result = await self.get_page_snapshot()
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result,
                }

            elif tool_name == "execute_python_command":
                command = arguments.get("command", "")
                success, result = await self.execute_python_command(command, context)
                # Add successful commands to our working script
                if success and not command.strip().startswith("print"):
                    self.working_script_lines.append(command)
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": f"Success: {success}\n{result}",
                }

            elif tool_name == "find_element_by_ref":
                ref = arguments.get("ref", "")
                result = await self.find_element_by_ref(ref)
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": result or "Element not found",
                }

            elif tool_name == "get_page_screenshot":
                result = await self.get_page_screenshot()
                if result.startswith("Error"):
                    # Return error as text
                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": result,
                    }
                else:
                    # Return image in proper format
                    return {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": result,
                                },
                            }
                        ],
                    }

            else:
                return {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": f"Unknown tool: {tool_name}",
                }

        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": f"Error: {e}",
            }

    def build_messages(
        self, command: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Build the message history for the LLM (Anthropic format)."""
        messages = [
            {"role": "user", "content": f"Please execute this command: {command}"}
        ]

        # Add conversation history
        for turn in self.conversation_history:
            if turn.role == "assistant":
                content = []
                if turn.content:
                    content.append({"type": "text", "text": turn.content})

                # Add tool calls
                if turn.tool_calls:
                    for tool_call in turn.tool_calls:
                        content.append(
                            {
                                "type": "tool_use",
                                "id": tool_call.id,
                                "name": tool_call.name,
                                "input": tool_call.input,
                            }
                        )

                messages.append({"role": "assistant", "content": content})

            elif turn.role == "tool":
                # Tool results are added as user messages in Anthropic format
                if turn.tool_results:
                    content = []
                    for tool_result in turn.tool_results:
                        content.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_result["tool_use_id"],
                                "content": tool_result["content"],
                            }
                        )
                    messages.append({"role": "user", "content": content})

            elif turn.role == "user":
                messages.append({"role": "user", "content": turn.content})

        return messages

    async def execute_interactive_step(
        self, command: str, context: Dict[str, Any], max_turns: int = 10
    ) -> Dict[str, Any]:
        """
        Execute a step using interactive conversation with the LLM.

        Parameters:
        -----------
        command (str): The natural language command to execute
        context (Dict[str, Any]): Context variables
        max_turns (int): Maximum number of conversation turns

        Returns:
        --------
        Dict[str, Any]: Result with success status and final script
        """
        for turn in range(max_turns):
            try:
                # Build messages for this turn
                messages = self.build_messages(command, context)

                # Call the LLM
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    messages=messages,
                    tools=TOOLS,
                    system=build_system_prompt(command, context),
                )

                # Process response
                if response.content:
                    assistant_content = ""
                    tool_calls = []

                    # Process each content block
                    for content in response.content:
                        if content.type == "text":
                            assistant_content += content.text
                        elif content.type == "tool_use":
                            tool_calls.append(content)

                    # Check if this is the final response with the script
                    if (
                        "```python" in assistant_content
                        and "Final working script" in assistant_content
                    ):
                        # Extract the final script
                        script_start = assistant_content.find("```python")
                        script_end = assistant_content.find("```", script_start + 9)
                        if script_start != -1 and script_end != -1:
                            self.final_script = assistant_content[
                                script_start + 9 : script_end
                            ].strip()
                            # Remove the "# Final working script" comment if present
                            lines = self.final_script.split("\n")
                            self.final_script = "\n".join(
                                line
                                for line in lines
                                if not line.strip().startswith("# Final working script")
                            )

                        self.add_conversation_turn("assistant", assistant_content)
                        break

                    # Check for tool calls
                    if tool_calls:
                        self.add_conversation_turn(
                            "assistant", assistant_content, tool_calls=tool_calls
                        )

                        # Process each tool call
                        tool_results = []
                        for tool_call in tool_calls:
                            result = await self.process_anthropic_tool_call(
                                tool_call, context
                            )
                            tool_results.append(result)

                        # Add tool results to conversation
                        self.add_conversation_turn(
                            "tool",
                            "",
                            tool_results=tool_results,
                            tool_name=", ".join(
                                tool_call.name for tool_call in tool_calls
                            ),
                        )
                    else:
                        # No tool calls, just add the response
                        self.add_conversation_turn("assistant", assistant_content)

                        # If the assistant seems to be done, break
                        if (
                            "final script" in assistant_content.lower()
                            or "completed" in assistant_content.lower()
                        ):
                            break
                else:
                    log.error("No content in LLM response")
                    # Continue to next turn instead of breaking
                    continue

            except Exception as e:
                # Log the error but continue to next turn
                log.error(f"Error in conversation turn {turn}: {e}")
                # Add error message to conversation to inform the LLM
                self.add_conversation_turn(
                    "user", f"An error occurred: {e}. Please try a different approach."
                )
                continue

        # Return the result
        if self.final_script:
            return {
                "success": True,
                "message": "Interactive step completed successfully",
                "script": self.final_script,
                "conversation_turns": len(self.conversation_history),
            }
        else:
            # Fallback to working script lines
            fallback_script = "\n".join(self.working_script_lines)
            return {
                "success": bool(fallback_script),
                "message": "Interactive step completed with working commands",
                "script": fallback_script,
                "conversation_turns": len(self.conversation_history),
            }
