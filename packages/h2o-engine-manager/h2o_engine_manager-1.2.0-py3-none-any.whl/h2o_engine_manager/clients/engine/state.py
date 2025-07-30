from enum import Enum

from h2o_engine_manager.gen.model.v1_engine_state import V1EngineState


class EngineState(Enum):
    # Engine state is unspecified or unknown
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    # Engine is starting
    STATE_STARTING = "STATE_STARTING"
    # Engine is establishing a connection with the AI Engine Manager.
    STATE_CONNECTING = "STATE_CONNECTING"
    # Engine is running and can be used
    STATE_RUNNING = "STATE_RUNNING"
    # Engine is pausing
    STATE_PAUSING = "STATE_PAUSING"
    # Engine is paused, can be resumed again
    STATE_PAUSED = "STATE_PAUSED"
    # Engine has failed
    STATE_FAILED = "STATE_FAILED"
    # Engine is being deleted.
    STATE_DELETING = "STATE_DELETING"
    # Engine is terminating
    STATE_TERMINATING = "STATE_TERMINATING"
    # Engine is terminated, cannot be resumed
    STATE_TERMINATED = "STATE_TERMINATED"

    def to_api_object(self) -> V1EngineState:
        return V1EngineState(self.name)


def from_api_engine_state(state: V1EngineState) -> EngineState:
    return EngineState(str(state))
