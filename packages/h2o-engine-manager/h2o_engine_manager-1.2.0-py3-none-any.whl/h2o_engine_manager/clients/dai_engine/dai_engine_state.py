from enum import Enum
from typing import List

from h2o_engine_manager.gen.model.v1_dai_engine_state import V1DAIEngineState


class DAIEngineState(Enum):
    # Engine state is unspecified or unknown
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    # Engine is starting
    STATE_STARTING = "STATE_STARTING"
    # Engine is establishing a connection with the AI Engine Manager.
    STATE_CONNECTING = "STATE_CONNECTING"
    # Engine is running and can be used
    STATE_RUNNING = "STATE_RUNNING"
    # Engine is stopping
    STATE_PAUSING = "STATE_PAUSING"
    # Engine is stopped, can be started again
    STATE_PAUSED = "STATE_PAUSED"
    # Engine has failed
    STATE_FAILED = "STATE_FAILED"
    # Engine is being deleted.
    STATE_DELETING = "STATE_DELETING"

    def to_api_object(self) -> V1DAIEngineState:
        return V1DAIEngineState(self.name)


def from_dai_engine_state_api_object(state: V1DAIEngineState) -> DAIEngineState:
    return DAIEngineState(str(state))


def final_states() -> List[DAIEngineState]:
    return [DAIEngineState.STATE_RUNNING, DAIEngineState.STATE_PAUSED]
