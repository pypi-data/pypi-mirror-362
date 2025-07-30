from enum import Enum

from h2o_engine_manager.gen.model.v1_notebook_engine_state import V1NotebookEngineState


class NotebookEngineState(Enum):
    # Engine state is unspecified or unknown
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    # Engine is starting
    STATE_STARTING = "STATE_STARTING"
    # Engine is running and can be used.
    STATE_RUNNING = "STATE_RUNNING"
    # Engine is pausing.
    STATE_PAUSING = "STATE_PAUSING"
    # Engine is paused.
    STATE_PAUSED = "STATE_PAUSED"
    # Engine has failed.
    STATE_FAILED = "STATE_FAILED"
    # Engine is being deleted.
    STATE_DELETING = "STATE_DELETING"
    # Engine is terminated.
    STATE_TERMINATED = "STATE_TERMINATED"

    def to_api_object(self) -> V1NotebookEngineState:
        return V1NotebookEngineState(self.name)


def notebook_engine_state_from_api_object(api_object: V1NotebookEngineState) -> NotebookEngineState:
    return NotebookEngineState(str(api_object))
