#!/usr/bin/env python3
"""MCP Web Automation Server main entry point."""

import asyncio
import logging
from typing import Any

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server


from va.mcp_server.web_automation import WebAutomationTools, create_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

# Global instances
web_tools = WebAutomationTools()

# Create the MCP server
server = Server("web-automation")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    log.info("Listing available tools")
    tools = create_tools()
    log.info(f"Returning {len(tools)} tools")
    return tools


@server.call_tool()
async def call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    try:
        if name == "get_page_snapshot":
            result = await web_tools.get_page_snapshot()
            return [types.TextContent(type="text", text=result)]

        elif name == "execute_python_command":
            command = arguments.get("command", "")
            result = await web_tools.execute_python_command(command)
            return [types.TextContent(type="text", text=result)]

        elif name == "find_element_by_ref":
            ref = arguments.get("ref", "")
            result = await web_tools.find_element_by_ref(ref)
            return [types.TextContent(type="text", text=result)]

        elif name == "get_page_screenshot":
            result = await web_tools.get_page_screenshot()
            # Return as image if it's base64 data
            if not result.startswith("Error"):
                return [
                    types.ImageContent(type="image", data=result, mimeType="image/png")
                ]
            else:
                return [types.TextContent(type="text", text=result)]

        elif name == "navigate_to_url":
            url = arguments.get("url", "")
            result = await web_tools.navigate_to_url(url)
            return [types.TextContent(type="text", text=result)]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        log.error(f"Error in tool call {name}: {e}")
        return [types.TextContent(type="text", text=f"Error: {e}")]


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return []


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource."""
    return f"Resource {uri} not found"


async def main():
    """Main entry point for the MCP server."""
    try:
        # Browser will be started on-demand when first tool is called
        log.info("Starting MCP Web Automation Server...")

        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

    except KeyboardInterrupt:
        log.info("Server interrupted by user")
    except Exception as e:
        log.error(f"Server error: {e}")
        raise
    finally:
        log.info("Cleaning up...")
        await web_tools.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
