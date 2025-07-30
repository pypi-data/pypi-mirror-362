from typing import List

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngineState
from h2o_engine_manager.clients.dai_engine.dai_engine import (
    from_dai_engine_state_api_object,
)


# Tests that all defined states can be transformed to and from generated client stubs.
def test_engine_state_api_conversion():
    all_states: List[DAIEngineState] = [s for s in DAIEngineState]
    for state in all_states:
        api_object = state.to_api_object()
        from_dai_engine_state_api_object(api_object)
