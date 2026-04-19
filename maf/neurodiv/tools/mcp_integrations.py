"""MCP tool factories for Slack, Notion, and Google Drive.

Use env vars from maf.neurodiv.config to supply URLs.
"""
from __future__ import annotations

from agent_framework.mcp import MCPStdioTool, MCPStreamableHTTPTool, MCPWebsocketTool

from maf.neurodiv.config import (
    SLACK_MCP_URL,
    NOTION_MCP_URL,
    GDRIVE_MCP_URL,
)


def slack_mcp_tool():
    """Return a Slack MCP tool.

    If SLACK_MCP_URL is empty, assume stdio (start the server locally).
    """
    if SLACK_MCP_URL.startswith("wss://"):
        return MCPWebsocketTool(name="slack", description="Slack via MCP", url=SLACK_MCP_URL)
    if SLACK_MCP_URL:
        return MCPStreamableHTTPTool(name="slack", description="Slack via MCP", url=SLACK_MCP_URL)
    return MCPStdioTool(name="slack", description="Slack via MCP (stdio)" , command=["slack-mcp"])


def notion_mcp_tool():
    """Return a Notion MCP tool."""
    if NOTION_MCP_URL.startswith("wss://"):
        return MCPWebsocketTool(name="notion", description="Notion via MCP", url=NOTION_MCP_URL)
    if NOTION_MCP_URL:
        return MCPStreamableHTTPTool(name="notion", description="Notion via MCP", url=NOTION_MCP_URL)
    return MCPStdioTool(name="notion", description="Notion via MCP (stdio)", command=["notion-mcp"])


def gdrive_mcp_tool():
    """Return a Google Drive MCP tool."""
    if GDRIVE_MCP_URL.startswith("wss://"):
        return MCPWebsocketTool(name="google-drive", description="Google Drive via MCP", url=GDRIVE_MCP_URL)
    if GDRIVE_MCP_URL:
        return MCPStreamableHTTPTool(name="google-drive", description="Google Drive via MCP", url=GDRIVE_MCP_URL)
    return MCPStdioTool(
        name="google-drive", description="Google Drive via MCP (stdio)", command=["gdrive-mcp"]
    )
