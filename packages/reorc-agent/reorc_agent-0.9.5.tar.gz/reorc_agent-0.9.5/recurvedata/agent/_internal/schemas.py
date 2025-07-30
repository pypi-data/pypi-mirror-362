from __future__ import annotations

import datetime
from enum import Enum
from typing import Annotated, Any, Generic, Literal, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .host import HostInfo, HostMetrics
from .utils import utcnow

T = TypeVar("T")


class RecurveEnum(str, Enum):
    """Base Enum class for Recurve."""

    def __str__(self) -> str:
        return str.__str__(self)


class ServiceStatusInfo(BaseModel):
    container_name: str
    status: str


class AgentHostInfo(BaseModel):
    ip_address: str
    hostname: str
    agent_version: str
    host_info: HostInfo


class LoginPayload(AgentHostInfo):
    tenant_domain: str
    agent_id: UUID
    auth_token: str


class Heartbeat(BaseModel):
    agent_id: UUID
    metrics: HostMetrics
    sent_time: datetime.datetime = Field(default_factory=utcnow)
    service_status: list[ServiceStatusInfo] = Field(default_factory=list)


class Pagination(BaseModel, Generic[T]):
    total: int
    items: list[T]


class SourceCodeExecPayload(BaseModel):
    task_instance_id: int
    agent_id: UUID
    queue: str
    max_retries: int
    max_duration: int
    handler_code: str  # base64 encoded content of the handler file
    handler_format: str  # format of the handler file, either "py" or "zip"
    payload: dict  # payload for the task, will be passed to the handler in JSON format


class TaskResultPayload(BaseModel):
    status: TaskStatus
    result: dict | None = None
    error: dict | None = None
    logs: list[str] | None = None


class TaskStatus(RecurveEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"


class TaskInstanceInfo(BaseModel):
    task_pid: int | None = None
    task_id: str | None = None


class UpdateTaskInstanceStatus(BaseModel):
    status: TaskStatus
    logs: Optional[list[str]] = None
    result: Optional[dict[str, Any]] = None
    error: Optional[dict[str, str]] = None
    info: Optional[TaskInstanceInfo] = None


class Action(str, Enum):
    DEPLOY = "deploy"
    UNDEPLOY = "undeploy"
    START = "start"
    RESTART = "restart"
    STOP = "stop"
    CUBE_PUSH_CONFIG = "cube-push-config"
    CUBE_RESTART_SERVICE = "cube-restart-service"


class BaseWorkerManagementPayload(BaseModel):
    """Base schema for all worker management payloads"""

    model_config = ConfigDict(extra="ignore")
    action: Action


class DeployServicePayload(BaseWorkerManagementPayload):
    action: Literal[Action.DEPLOY]
    docker_compose: str
    worker_image: str
    cube_env: str | None = None
    cube_proxy_config: dict | None = None
    cube_python: str | None = None


class DeployServiceResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    worker_version: str | None


class UndeployServicePayload(BaseWorkerManagementPayload):
    action: Literal[Action.UNDEPLOY]
    remove_volumes: bool = False


class ContainerManagementPayload(BaseWorkerManagementPayload):
    action: Literal[Action.START, Action.RESTART, Action.STOP]
    container_names: list[str]
    cube_proxy_config: dict | None = None


class CubePushConfigPayload(BaseWorkerManagementPayload):
    action: Literal[Action.CUBE_PUSH_CONFIG]
    env_id: int
    project_id: int | None = None
    cube_ids: list[int] | None = None
    view_ids: list[int] | None = None
    regenerate: bool | None = None
    only_base_config: bool | None = None
    container_names: list[str] | None = None
    tracing_context: dict | None = None


class CubeRestartServicePayload(BaseWorkerManagementPayload):
    action: Literal[Action.CUBE_RESTART_SERVICE]
    env_id: int
    tenant_id: int
    container_names: list[str] | None = None
    tracing_context: dict | None = None


class WorkerManagementPayload(BaseWorkerManagementPayload):
    payload: Annotated[
        DeployServicePayload
        | ContainerManagementPayload
        | UndeployServicePayload
        | CubePushConfigPayload
        | CubeRestartServicePayload,
        Field(discriminator="action"),
    ]


class TaskResult(BaseModel):
    code: int


class CancelPayload(BaseModel):
    task_id: UUID
