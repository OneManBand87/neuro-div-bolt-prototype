from agent_framework import Agent

from maf.neurodiv.tools.io_tools import fetch_url
from maf.neurodiv.clients.openai_client import make_openai_client


def make_researcher() -> Agent:
    return Agent(
        name="researcher",
        client=make_openai_client("gpt-4.1-mini"),
        instructions="Structured output only. Return JSON with title, findings, citations.",
        tools=[fetch_url],
    )
