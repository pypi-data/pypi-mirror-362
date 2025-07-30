from enum import Enum
from typing import List

from h2o_engine_manager.gen.model.v1_h2_o_engine_state import V1H2OEngineState


class H2OEngineState(Enum):
    # Engine state is unspecified or unknown
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    # Engine is starting
    STATE_STARTING = "STATE_STARTING"
    # Engine is establishing a connection with the AI Engine Manager.
    STATE_CONNECTING = "STATE_CONNECTING"
    # Engine is running and can be used
    STATE_RUNNING = "STATE_RUNNING"
    # Engine is pausing. Deprecated, use TERMINATING instead.
    STATE_PAUSING = "STATE_PAUSING"
    # Engine is stopped, cannot be started. Deprecated, use TERMINATED instead.
    STATE_PAUSED = "STATE_PAUSED"
    # Engine has failed
    STATE_FAILED = "STATE_FAILED"
    # Engine is being deleted.
    STATE_DELETING = "STATE_DELETING"
    # Engine is terminating
    STATE_TERMINATING = "STATE_TERMINATING"
    # Engine is terminated, cannot be started
    STATE_TERMINATED = "STATE_TERMINATED"

    def to_api_object(self) -> V1H2OEngineState:
        return V1H2OEngineState(self.name)


def from_h2o_engine_state_api_object(state: V1H2OEngineState) -> H2OEngineState:
    return H2OEngineState(str(state))


def final_states() -> List[H2OEngineState]:
    return [H2OEngineState.STATE_RUNNING, H2OEngineState.STATE_PAUSED, H2OEngineState.STATE_TERMINATED]
