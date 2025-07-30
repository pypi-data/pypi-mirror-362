from enum import Enum

from h2o_engine_manager.gen.model.notebook_engine_failure_reason import (
    NotebookEngineFailureReason as V1NotebookEngineFailureReason,
)


class NotebookEngineFailureReason(Enum):
    # NotebookEngine failure reason is unspecified.
    FAILURE_REASON_UNSPECIFIED = "FAILURE_REASON_UNSPECIFIED"
    # NotebookEngine failure reason is unknown.
    FAILURE_REASON_UNKNOWN = "FAILURE_REASON_UNKNOWN"
    # NotebookEngine exceeded its memory limit and was killed.
    FAILURE_REASON_OOM_KILLED = "FAILURE_REASON_OOM_KILLED"
    # NotebookEngine application crashed.
    FAILURE_REASON_PROCESS_FAILED = "FAILURE_REASON_PROCESS_FAILED"
    # NotebookEngine cannot access the assigned PVC.
    FAILURE_REASON_PVC_ACCESS_FAILURE = "FAILURE_REASON_PVC_ACCESS_FAILURE"

    def to_api_object(self) -> V1NotebookEngineFailureReason:
        return V1NotebookEngineFailureReason(self.name)


def notebook_engine_failure_reason_from_api_object(
        api_object: V1NotebookEngineFailureReason
) -> NotebookEngineFailureReason:
    return NotebookEngineFailureReason(str(api_object))
