from agent_framework.openai import OpenAIChatClient


def make_openai_client(model: str = "gpt-4.1-mini"):
    # TODO: wire auth via env/config; keep config separate from code
    return OpenAIChatClient(model=model)
