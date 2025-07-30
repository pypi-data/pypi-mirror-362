from enum import Enum


class RecurveEnum(str, Enum):
    """Base Enum class for Recurve."""

    def __str__(self) -> str:
        return str.__str__(self)


class MessageType(RecurveEnum):
    # DP -> CP:
    HEARTBEAT = "heartbeat"
    REPORT_HOST_INFO = "report-host-info"
    RESULT = "result"
    TASK_ACK = "task-ack"

    # CP -> DP:
    HEARTBEAT_REQUEST = "heartbeat-request"
    WORKER_MANAGEMENT = "worker-management"
    BUSINESS = "business"
    CANCEL = "cancel"
    SOURCE_CODE_EXEC = "source-code-exec"
