"""Web automation tools for MCP server."""

import base64
import logging
from mcp import types

from va.playwright import create_browser_context_async
from va.playwright.page import Page

log = logging.getLogger(__name__)


class WebAutomationTools:
    """Web automation tools that can be exposed via MCP."""

    def __init__(self):
        self.context = None
        self.stagehand = None
        self.page = None

    async def _get_or_create_page(self) -> Page:
        """Get or create a page with VibePage functionality."""
        if self.page is None:
            if self.context is None:
                self.context, self.stagehand = await create_browser_context_async(
                    headless=False
                )

            # Get existing page or create new one
            if self.context.pages:
                self.page = self.context.pages[0]
            else:
                self.page = await self.context.new_page()

        return self.page

    async def cleanup(self):
        """Clean up browser resources."""
        if self.context and self.stagehand:
            await self.context._wait_for_login_tasks()
            await self.context.close()
            await self.stagehand.close()
            self.stagehand = None
            self.context = None
            self.page = None

    async def get_page_snapshot(self) -> str:
        """Get an AI-optimized snapshot of the current page."""
        page = await self._get_or_create_page()
        snapshot = await page.snapshot_for_ai()
        return str(snapshot)

    async def execute_python_command(self, command: str) -> str:
        """Execute Python command and return result."""
        page = await self._get_or_create_page()

        # Create execution context with captured output
        captured_output = []
        execution_context = {
            "page": page,
            "print": lambda *args: captured_output.append(
                " ".join(str(arg) for arg in args)
            ),
        }

        result = None

        try:
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
        except Exception as e:
            log.error(f"Error executing command: {e}")
            return f"Success: False\nError executing command: {e}"

        # Build response message
        response_parts = []
        if captured_output:
            response_parts.append("Output: " + "\n".join(captured_output))
        if result is not None:
            response_parts.append(f"Return value: {result}")
        if not response_parts:
            response_parts.append("Command executed successfully")

        return "Success: True\n" + "\n".join(response_parts)

    async def find_element_by_ref(self, ref: str) -> str:
        """Find element by ref from AI snapshot and return locator string."""
        try:
            page = await self._get_or_create_page()
            locator = page.locator(f"aria-ref={ref}")
            count = await locator.count()

            if count > 0:
                # Generate locator string for the element
                locator_string = await locator.first.generate_locator_string()
                return "page." + locator_string
            else:
                return "Element not found"

        except Exception as e:
            log.error(f"Failed to find element by ref {ref}: {e}")
            return f"Error finding element: {e}"

    async def get_page_screenshot(self) -> str:
        """Take a screenshot of the current page and return as base64."""
        try:
            page = await self._get_or_create_page()
            screenshot_bytes = await page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            return screenshot_base64
        except Exception as e:
            log.error(f"Failed to take screenshot: {e}")
            return f"Error taking screenshot: {e}"

    async def navigate_to_url(self, url: str) -> str:
        """Navigate to a specific URL."""
        try:
            page = await self._get_or_create_page()
            await page.goto(url)
            return f"Successfully navigated to: {url}"
        except Exception as e:
            log.error(f"Failed to navigate to {url}: {e}")
            return f"Error navigating to {url}: {e}"


def create_tools() -> list[types.Tool]:
    """Create MCP tool definitions."""
    return [
        types.Tool(
            name="get_page_snapshot",
            description="Get AI-optimized page structure. Use this first to understand what you're working with.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="execute_python_command",
            description="Execute Python code. Intended for Playwright automation, but flexible. Test commands incrementally and build your script from successful ones. IMPORTANT: Use 'await' for all Playwright operations (page.fill, page.click, etc.) since they are asynchronous. Never use refs (like 'e3') directly in Playwright code - always call find_element_by_ref() first to get the proper locator. Examples: await page.fill('input[name=\"field\"]', 'value'), await page.click('button'), await page.screenshot(path='screenshot.png')",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Python command to execute",
                    }
                },
                "required": ["command"],
            },
        ),
        types.Tool(
            name="find_element_by_ref",
            description="Find element by ref from snapshot. Use refs from page snapshots to locate elements precisely.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ref": {
                        "type": "string",
                        "description": "Element ref (e.g., 'e3')",
                    }
                },
                "required": ["ref"],
            },
        ),
        types.Tool(
            name="get_page_screenshot",
            description="Take screenshot for visual understanding. Use when you need to see the page visually.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="navigate_to_url",
            description="Navigate to a specific URL to start web automation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to",
                    }
                },
                "required": ["url"],
            },
        ),
    ]
