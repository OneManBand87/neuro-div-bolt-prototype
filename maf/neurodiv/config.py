"""MAF configuration constants for NeuroDIV pipelines.

All secrets should be supplied via environment variables.
"""
import os

SLACK_CHANNEL = os.getenv("NEURODIV_SLACK_CHANNEL", "neuro-div")
NOTION_ROOT = os.getenv("NEURODIV_NOTION_ROOT", "Neuro DIV")
GDRIVE_FOLDER = os.getenv("NEURODIV_GDRIVE_FOLDER", "ADHD Projects")

# MCP tool endpoints (if using hosted HTTP/WebSocket MCP servers)
SLACK_MCP_URL = os.getenv("NEURODIV_SLACK_MCP_URL", "")
NOTION_MCP_URL = os.getenv("NEURODIV_NOTION_MCP_URL", "")
GDRIVE_MCP_URL = os.getenv("NEURODIV_GDRIVE_MCP_URL", "")
