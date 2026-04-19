from dataclasses import dataclass
from agent_framework.workflow import Workflow, SequentialBuilder, Executor
from agent_framework.workflow.controls import Pending, RequestResponse


@dataclass
class PublishState:
    content: dict
    approved: bool | None = None
    publish_result: str | None = None


class ApprovalGate(Executor):
    async def run(self, state: PublishState):
        req = RequestResponse(
            id="publish_approval",
            prompt="Approve publish?",
            payload=state.content,
        )
        return Pending(request=req)


class PublishExecutor(Executor):
    async def run(self, state: PublishState) -> PublishState:
        # TODO: replace with real publish logic
        state.publish_result = "published"
        return state


def build_publish_workflow(checkpoints=None) -> Workflow[PublishState]:
    builder = SequentialBuilder[PublishState](name="publish")
    if checkpoints:
        builder.with_checkpoints(checkpoints)
    builder.add_executor("approval", ApprovalGate())
    builder.add_executor("publish", PublishExecutor())
    return builder.build()
