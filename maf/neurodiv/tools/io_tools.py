from agent_framework.tools import tool


@tool
def fetch_url(url: str) -> str:
    """Fetch raw text from a URL."""
    # TODO: replace with real fetch + error handling
    return f"[raw html/text for {url}]"


@tool
def save_record(key: str, value: dict) -> str:
    """Persist a structured record and return an ID."""
    # TODO: replace with DB/Google Sheets/whatever persistence layer
    return key
