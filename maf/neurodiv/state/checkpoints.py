from agent_framework.checkpoints import JsonFileCheckpointStorage


def make_checkpoint_storage(path: str = ".checkpoints/neurodiv"):
    """Create checkpoint storage for resumable workflows."""
    return JsonFileCheckpointStorage(path=path)
