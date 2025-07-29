from abc import ABC, abstractmethod

from loguru import logger

from recurvedata.agent._internal import host, worker
from recurvedata.agent._internal.schemas import (
    CancelPayload,
    Heartbeat,
    SourceCodeExecPayload,
    TaskStatus,
    WorkerManagementPayload,
)
from recurvedata.agent._internal.task_manager import global_task_manager
from recurvedata.agent._internal.websocket.connector import WebSocketConnector
from recurvedata.agent._internal.websocket.schemas import MessageType, WebSocketMessage
from recurvedata.agent.dpserver.client import request_dpserver
from recurvedata.agent.dpserver.schema import DPServerRequestPayload

from ..worker_management import WorkerManagementTask


class BaseMessageHandler(ABC):
    _bind_message_type = None

    @abstractmethod
    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        raise NotImplementedError


class MessageHandlerRegistry:
    def __init__(self):
        self.handlers = {}

    def register(self, message_type: MessageType, handler: BaseMessageHandler):
        self.handlers[message_type] = handler

    def register_handler(self):
        """
        Decorator: Automatically register handler to registry

        Args:
            message_type: Message type used as registry key
        """

        def decorator(handler_class):
            # Ensure handler_class is a subclass of BaseMessageHandler
            if not issubclass(handler_class, BaseMessageHandler):
                raise ValueError(f"Handler class {handler_class.__name__} must inherit from BaseMessageHandler")

            message_type = handler_class._bind_message_type
            # check in development stage
            assert message_type in MessageType, f"Register Message Handler Error, unknown message type: {message_type}"

            # Register to registry
            self.register(message_type, handler_class())

            return handler_class

        return decorator

    def get_handler(self, message_type: MessageType | None) -> BaseMessageHandler | None:
        """Get handler for specified message type"""
        return self.handlers.get(message_type)

    def get_all_handlers(self) -> dict:
        """Get all registered handlers"""
        return self.handlers.copy()

    def has_handler(self, message_type: str | None) -> bool:
        """Check if handler is registered for specified message type"""
        return message_type in self.handlers


# global registry instance
registry = MessageHandlerRegistry()


@registry.register_handler()
class HeartBeatRequestMessageHandler(BaseMessageHandler):
    """
    Handle heartbeat request message from server.
    Reply with heartbeat message to server.
    """

    _bind_message_type = MessageType.HEARTBEAT_REQUEST

    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        logger.info(f"received heartbeat request: {message}")
        path = worker.get_docker_root_dir()
        payload = Heartbeat(
            agent_id=ws_connector.config.agent_id,
            metrics=host.get_host_metrics(path=path),
            service_status=worker.get_service_status(),
        )
        message = WebSocketMessage(
            type=MessageType.HEARTBEAT,
            payload=payload.model_dump(mode="json"),
            reply_to=message.message_id,  # reply to the same message id
        )
        await ws_connector.send_json(message.model_dump())


@registry.register_handler()
class WorkerManagementMessageHandler(BaseMessageHandler):
    _bind_message_type = MessageType.WORKER_MANAGEMENT

    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        logger.info(f"received worker management message: {message.type}-{message.message_id}")
        payload = WorkerManagementPayload.model_validate(
            {
                "action": message.payload.get("action"),
                # inner payload is task payload
                "payload": message.payload,
            }
        )
        result, error_msg = await WorkerManagementTask.handle(payload)
        response_message = WebSocketMessage(
            type=MessageType.RESULT,
            payload={
                "result": result.model_dump(mode="json") if result else None,
                "error": {"reason": error_msg} if error_msg else None,
                "status": TaskStatus.SUCCESS if not error_msg else TaskStatus.FAILED,
            },
            reply_to=message.message_id,
            message_id=message.message_id,
        )
        await ws_connector.send_json(response_message.model_dump())


@registry.register_handler()
class CancelMessageHandler(BaseMessageHandler):
    _bind_message_type = MessageType.CANCEL

    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        logger.info(f"received cancel message: {message.type}-{message.message_id}")
        task_id = CancelPayload.model_validate(message.payload).task_id
        await global_task_manager.cancel_task(task_id)


@registry.register_handler()
class BusinessMessageHandler(BaseMessageHandler):
    """
    Handle business message from server.
    Forward dpserver requests to dpserver and return the response.
    """

    _bind_message_type = MessageType.BUSINESS

    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        logger.info(f"received business message: {message.type}-{message.message_id}")

        try:
            # Parse request payload
            payload = DPServerRequestPayload.model_validate(message.payload)

            # Call dpserver to process request
            result = await request_dpserver(payload)

            # Send success response, DPServer has nothing need to be sent as log
            response_message = WebSocketMessage(
                type=MessageType.RESULT,
                payload={
                    "result": result.model_dump() if result else None,
                    "error": result.error if result else None,
                    "status": TaskStatus.SUCCESS if result.ok else TaskStatus.FAILED,
                },
                reply_to=message.message_id,
                message_id=message.message_id,
            )
            await ws_connector.send_json(response_message.model_dump())
            # return for logger
            return result

        except Exception as e:
            logger.error(f"Error processing business message: {e}")

            # Send error response
            response_message = WebSocketMessage(
                type=MessageType.RESULT,
                payload={
                    # if result is not None, it means failed after request dpserver,
                    # so we need to upload the result of dpserver
                    "result": result.model_dump() if result else None,
                    "error": {"reason": str(e)},
                    "status": TaskStatus.FAILED,
                },
                reply_to=message.message_id,
                message_id=message.message_id,
            )
            await ws_connector.send_json(response_message.model_dump())
            raise e


@registry.register_handler()
class SourceCodeExecMessageHandler(BaseMessageHandler):
    _bind_message_type = MessageType.SOURCE_CODE_EXEC

    async def handle(self, message: WebSocketMessage, ws_connector: WebSocketConnector):
        from recurvedata.agent._internal.task_executor import TaskExecutor

        logger.info(f"received source code exec message: {message.type}-{message.message_id}")
        payload = SourceCodeExecPayload.model_validate(message.payload)
        task_executor = TaskExecutor()
        result = await task_executor.execute(payload)

        response_message = WebSocketMessage(
            type=MessageType.RESULT,
            payload=result.model_dump(),
            reply_to=message.message_id,
            message_id=message.message_id,
        )
        await ws_connector.send_json(response_message.model_dump())

        return result
