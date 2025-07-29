import asyncio
from typing import Coroutine
from uuid import UUID

from loguru import logger


class TaskManager:
    """
    A Thread-safe task manager.
    """

    def __init__(self):
        self._task_registry: dict[UUID, asyncio.Task] = dict()
        self._task_lock = asyncio.Lock()

    async def create(self, task_id: UUID, coro: Coroutine) -> None:
        async with self._task_lock:
            task = asyncio.create_task(coro)
            task.add_done_callback(lambda t: self._on_done(task_id, t))
            self._task_registry[task_id] = task

    def _on_done(self, task_id: UUID, task: asyncio.Task) -> None:
        self._task_registry.pop(task_id, None)

        try:
            result = task.result()
            logger.info(f"Task {task_id} has been completed: {result}")
        except Exception as e:
            logger.error(f"Task {task_id} has been failed: {e}")

    async def unregister_task(self, task_id: UUID) -> None:
        """
        remove the control of the task
        """
        async with self._task_lock:
            self._task_registry.pop(task_id, None)

    async def cancel_task(self, task_id: UUID) -> None:
        async with self._task_lock:
            task = self._task_registry.pop(task_id, None)

        if task:
            task.cancel()
            try:
                await task
                logger.info(f"Task {task_id} has been cancelled")
            except asyncio.CancelledError as e:
                logger.warning(f"Cancel task {task_id} failed: {e}")
        else:
            logger.warning(f"Task {task_id} not found")


global_task_manager = TaskManager()
