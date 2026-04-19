from dataclasses import dataclass


# Stub: keep the scaffold importable even if agent-framework isn't installed yet.
try:
    from agent_framework.workflow import Workflow, SequentialBuilder
except ImportError:  # pragma: no cover
    Workflow = object  # type: ignore
    SequentialBuilder = None  # type: ignore


@dataclass
class IngestState:
    url: str
    raw_text: str | None = None


def build_ingest_workflow():
    """Scaffold for a sequential ingestion pipeline."""
    if SequentialBuilder is None:
        raise RuntimeError("agent-framework not installed")

    builder = SequentialBuilder[IngestState](name="ingest")
    return builder.build()
