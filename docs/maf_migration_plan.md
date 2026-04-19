# NeuroDIV AutoGen → Microsoft Agent Framework Migration Plan

## Objectives
- Move the NeuroDIV multi-agent pipeline architecture off AutoGen (maintenance-mode) and onto Microsoft Agent Framework (MAF).
- Make orchestration explicit and typed (workflows + state models), not implicit "chat team" behavior.
- Keep the migration safe/reversible by doing it in small slices.

## Dependency plan
- Add: `agent-framework`
- Phase out: AutoGen runtime deps (`autogen-agentchat`, etc.) once parity is achieved.
- Anthropic note: treat Anthropic-dependent flows as high risk; either keep them on the legacy stack temporarily or wrap them behind deterministic executors.

## Repository scaffold (MAF-friendly)
- `neurodiv/clients/` – model clients
- `neurodiv/tools/` – shared tools (native + MCP)
- `neurodiv/agents/` – agent definitions
- `neurodiv/workflows/` – orchestration graphs
- `neurodiv/state/` – typed state models + checkpoint storage wiring
- `neurodiv/middleware/` – logging + guardrails
- `tests/` – unit + workflow contract + resume tests

## Migration order
1. Tools first (FunctionTool → @tool / MCP tool classes)
2. Single agents (AssistantAgent → Agent)
3. Deterministic pipelines (RoundRobin-group-chat-style → Sequential workflow)
4. Planner-led pipelines (MagenticOne → Magentic workflow)
5. Checkpointing (resume/recovery)
6. Human approval gates (publish/labels/outbound)
7. Observability + middleware

---

# Code stubs (ready to implement)

## `neurodiv/clients/openai_client.py`
```python
from agent_framework.openai import OpenAIChatClient

def make_openai_client(model: str = "gpt-4.1-mini"):
    return OpenAIChatClient(model=model)
```

## `neurodiv/tools/io_tools.py`
```python
from agent_framework.tools import tool

@tool
def fetch_url(url: str) -> str:
    """Fetch raw text from a URL."""
    # TODO: real fetch + error handling
    return f"[raw html/text for {url}]"

@tool
def save_record(key: str, value: dict) -> str:
    """Persist a structured record and return an ID/key."""
    # TODO: real DB/write
    return key
```

## `neurodiv/agents/researcher.py`
```python
from agent_framework import Agent
from neurodiv.clients.openai_client import make_openai_client
from neurodiv.tools.io_tools import fetch_url

def researcher_agent():
    return Agent(
        name="researcher",
        client=make_openai_client("gpt-4.1-mini"),
        instructions=(
            "You are a structured researcher. "
            "Always return JSON with fields: title, findings, citations."
        ),
        tools=[fetch_url],
    )
```

## `neurodiv/workflows/ingest_workflow.py`
```python
from dataclasses import dataclass
from agent_framework.workflow import Workflow, SequentialBuilder, Executor

@dataclass
class IngestState:
    url: str
    raw_text: str | None = None
    parsed: dict | None = None
    summary: str | None = None
    persisted_id: str | None = None

class ParseExecutor(Executor):
    async def run(self, state: IngestState) -> IngestState:
        state.parsed = {"words": len(state.raw_text or "")}
        return state

class SummarizeExecutor(Executor):
    async def run(self, state: IngestState) -> IngestState:
        state.summary = f"Summary of {state.url}"
        return state

class PersistExecutor(Executor):
    async def run(self, state: IngestState) -> IngestState:
        state.persisted_id = state.url
        return state

def build_ingest_workflow() -> Workflow[IngestState]:
    builder = SequentialBuilder[IngestState](name="ingest")
    builder.add_executor("parse", ParseExecutor())
    builder.add_executor("summarize", SummarizeExecutor())
    builder.add_executor("persist", PersistExecutor())
    return builder.build()
```

## `neurodiv/workflows/research_magentic.py`
```python
from dataclasses import dataclass
from agent_framework.workflow import Workflow, MagenticBuilder
from neurodiv.agents.researcher import researcher_agent

@dataclass
class ResearchState:
    question: str
    answer: str | None = None

def build_research_magentic() -> Workflow[ResearchState]:
    builder = MagenticBuilder[ResearchState](name="neurodiv_research")
    builder.add_agent(researcher_agent())
    return builder.build()
```

## Checkpointing
- Use `JsonFileCheckpointStorage` (or whatever storage you prefer) to enable resume/recovery.
- Test recovery by killing the workflow mid-run and resuming from checkpoints.

---

## Open tasks
- Locate the actual NeuroDIV agent codebase (this repo is currently a Slack Bolt prototype).
- Once the correct repo is located/available, instantiate the full scaffold in a `maf-migration` branch and port pipelines one-by-one.
