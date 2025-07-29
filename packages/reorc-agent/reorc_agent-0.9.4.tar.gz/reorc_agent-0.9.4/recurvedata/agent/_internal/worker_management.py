import asyncio
import os
from collections.abc import Sequence
from typing import Callable, TypeAlias

import aiofiles
from docker.models.containers import Container
from docker.models.images import Image
from loguru import logger

from recurvedata.agent._internal.cube.push_config import cube_push_config_service
from recurvedata.agent._internal.cube.restart_service import cube_restart_service
from recurvedata.agent._internal.docker import docker_client
from recurvedata.agent._internal.client import AgentClient
from recurvedata.agent.config import RECURVE_HOME, CONFIG

from .schemas import (
    Action,
    ContainerManagementPayload,
    CubePushConfigPayload,
    CubeRestartServicePayload,
    DeployServicePayload,
    DeployServiceResult,
    UndeployServicePayload,
    WorkerManagementPayload,
)

COMPOSE_FILE_NAME = os.path.join(RECURVE_HOME, "docker-compose.yml")
COMPOSE_PROJECT_NAME = "recurve_services"
CUBE_DIR = os.path.join(RECURVE_HOME, "cube")
CUBE_CONF_DIR = os.path.join(CUBE_DIR, "conf")

# Type aliases
TaskList: TypeAlias = Sequence[asyncio.Task[None]]


registry: dict[Action, Callable[[], None]] = {}


def register_action(action_type: Action):
    def decorator(func: Callable[[], None]) -> Callable[[], None]:
        registry[action_type] = func
        return func

    return decorator


def get_run_env() -> dict[str, str]:
    env = os.environ.copy()
    env["RECURVE_HOME"] = str(RECURVE_HOME)
    return env


class WorkerManagementTask:
    @staticmethod
    async def _create_cube_conf_dir(payload: DeployServicePayload) -> None:
        if not payload.cube_env:
            return

        if not os.path.exists(CUBE_CONF_DIR):
            os.makedirs(CUBE_CONF_DIR)

        if payload.cube_env:
            async with aiofiles.open(os.path.join(CUBE_CONF_DIR, ".env"), "w") as f:
                await f.write(payload.cube_env)

        if payload.cube_python:
            # async with aiofiles.open(os.path.join(CUBE_CONF_DIR, "cube.py"), "w") as f:
                # await f.write(payload.cube_python)
            client = AgentClient(CONFIG)
            response = await client.request("GET", "/api/cube/config/cube-python")
            if response.get("cube_python"):
                cube_python_file = response.get("cube_python")
            else:
                cube_python_file = payload.cube_python
            
            async with aiofiles.open(os.path.join(CUBE_CONF_DIR, "cube.py"), "w") as f:
                await f.write(cube_python_file)

    @staticmethod
    async def _write_cube_proxy_config(payload: DeployServicePayload) -> None:
        if not payload.cube_proxy_config:
            return

        tasks: list[asyncio.Task[None]] = []
        proxy_config = payload.cube_proxy_config
        if proxy_config and isinstance(proxy_config, dict):
            for key, value in proxy_config.items():
                tasks.append(asyncio.create_task(WorkerManagementTask._write_proxy_config_file(str(key), str(value))))
            await asyncio.gather(*tasks)

    @staticmethod
    async def _write_proxy_config_file(key: str, value: str) -> None:
        async with aiofiles.open(os.path.join(CUBE_DIR, f"{key}.toml"), "w") as f:
            await f.write(value)

    @staticmethod
    async def _write_docker_compose_file(payload: DeployServicePayload) -> None:
        async with aiofiles.open(COMPOSE_FILE_NAME, "w") as f:
            await f.write(payload.docker_compose)

    @staticmethod
    async def _fetch_local_image_version(worker_image: str) -> str:
        try:
            image: Image = await asyncio.to_thread(docker_client.images.get, worker_image)
            worker_version = image.labels.get("VERSION")
            return worker_version or "Unknown version"
        except Exception:
            return f"Image {worker_image} not found."

    @staticmethod
    @register_action(Action.DEPLOY)
    async def deploy_service(payload: DeployServicePayload) -> tuple[DeployServiceResult | None, str | None]:
        tasks: list[asyncio.Task[None]] = [
            asyncio.create_task(WorkerManagementTask._create_cube_conf_dir(payload)),
            asyncio.create_task(WorkerManagementTask._write_cube_proxy_config(payload)),
            asyncio.create_task(WorkerManagementTask._write_docker_compose_file(payload)),
        ]
        await asyncio.gather(*tasks)

        env = get_run_env()

        error_msg = None
        docker_compose_cmd = [
            "docker",
            "compose",
            "-f",
            COMPOSE_FILE_NAME,
            "-p",
            COMPOSE_PROJECT_NAME,
            "up",
            "-d",
        ]
        try:
            process = await asyncio.create_subprocess_exec(
                *docker_compose_cmd,
                env=env,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = f"Docker compose failed: {stderr or stdout}"
                logger.error(error_msg)
                return None, error_msg
        except Exception as e:
            error_msg = f"Docker compose failed: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

        logger.info("Docker Compose started successfully.")

        worker_version = await WorkerManagementTask._fetch_local_image_version(payload.worker_image)
        return DeployServiceResult(worker_version=worker_version), error_msg

    @staticmethod
    @register_action(Action.UNDEPLOY)
    async def undeploy_service(payload: UndeployServicePayload) -> tuple[None, str | None]:
        error_msg = None
        try:
            cmd = ["docker", "compose", "-f", COMPOSE_FILE_NAME, "-p", COMPOSE_PROJECT_NAME, "down"]
            if payload.remove_volumes:
                cmd.append("-v")

            env = get_run_env()

            process = await asyncio.create_subprocess_exec(
                *cmd,
                env=env,
            )
            _, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = f"Docker compose failed: {stderr.decode()}"
                logger.error(error_msg)
        except Exception as e:
            error_msg = f"Docker compose failed: {str(e)}"
            logger.error(error_msg)

        logger.info("Undeploy service successfully")
        return None, error_msg

    @staticmethod
    @register_action(Action.START)
    async def start_container(payload: ContainerManagementPayload) -> tuple[None, str | None]:
        error_msg = None
        for container_name in payload.container_names:
            try:
                container: Container = await asyncio.to_thread(docker_client.containers.get, container_name)
                await asyncio.to_thread(container.start)
                logger.info(f"Container {container_name} started successfully")
            except Exception as e:
                error_msg = f"Failed to start container {container_name}: {str(e)}"
                logger.error(error_msg)
                break

        return None, error_msg

    @staticmethod
    @register_action(Action.RESTART)
    async def restart_container(payload: ContainerManagementPayload) -> tuple[None, str | None]:
        error_msg = None
        for container_name in payload.container_names:
            try:
                container: Container = await asyncio.to_thread(docker_client.containers.get, container_name)
                await asyncio.to_thread(container.restart)
                logger.info(f"Container {container_name} restarted successfully")
            except Exception as e:
                error_msg = f"Failed to restart container {container_name}: {str(e)}"
                logger.error(error_msg)
                break

        return None, error_msg

    @staticmethod
    @register_action(Action.STOP)
    async def stop_container(payload: ContainerManagementPayload) -> tuple[None, str | None]:
        error_msg = None
        for container_name in payload.container_names:
            try:
                container: Container = await asyncio.to_thread(docker_client.containers.get, container_name)
                await asyncio.to_thread(container.stop)
                logger.info(f"Container {container_name} stopped successfully")
            except Exception as e:
                error_msg = f"Failed to stop container {container_name}: {str(e)}"
                logger.error(error_msg)
                break

        return None, error_msg

    @staticmethod
    @register_action(Action.CUBE_PUSH_CONFIG)
    async def push_cube_config(payload: CubePushConfigPayload) -> tuple[None, str | None]:
        success, message = await cube_push_config_service.push_cube_config(payload)
        if success:
            return None, None
        else:
            return None, message

    @staticmethod
    @register_action(Action.CUBE_RESTART_SERVICE)
    async def restart_cube_service(payload: CubeRestartServicePayload) -> tuple[None, str | None]:
        success, message = await cube_restart_service.restart_cube_service(payload)
        if success:
            return None, None
        else:
            return None, message

    @staticmethod
    async def handle(payload: WorkerManagementPayload) -> tuple[DeployServiceResult | None, str | None]:
        try:
            return await registry[payload.action](payload.payload)
        except Exception as e:
            logger.error(f"Failed to handle worker management payload: {str(e)}")
            return None, str(e)
