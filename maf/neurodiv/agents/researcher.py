from agent_framework import Agent

from maf.neurodiv.clients.openai_client import make_openai_client
from maf.neurodiv.config import SLACK_CHANNEL
from maf.neurodiv.tools.io_tools import fetch_url
from maf.neurodiv.tools.mcp_integrations import (
    slack_mcp_tool,
    notion_mcp_tool,
    gdrive_mcp_tool,
)


def make_researcher() -> Agent:
    return Agent(
        name="researcher",
        client=make_openai_client("gpt-4.1-mini"),
        instructions=(
            "Structured output only. Return JSON with title, findings, citations. "
            "Use MCP tools when available."
        ),
        tools=[
            fetch_url,
            slack_mcp_tool(),
            notion_mcp_tool(),
            gdrive_mcp_tool(),
        ],
    )
