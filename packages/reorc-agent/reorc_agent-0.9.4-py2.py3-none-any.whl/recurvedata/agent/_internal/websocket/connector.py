import json
import time
from datetime import UTC, datetime
from typing import Any, Callable, Coroutine

import tenacity
import websockets
from loguru import logger
from websockets.exceptions import ConnectionClosed, WebSocketException

from recurvedata.agent._version import VERSION
from recurvedata.agent.config import AgentConfig
from recurvedata.agent.exceptions import UnauthorizedError

KiB = 1024
MiB = 1024 * KiB
GiB = 1024 * MiB


class RetryableWebSocketException(Exception):
    pass


class WebSocketConnector:
    """Simple async WebSocket connector for agent communication"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.ws: websockets.ClientConnection | None = None

        # Callback functions
        self.on_receive_message: Callable[[str, "WebSocketConnector"], Coroutine[Any, Any, None]] | None = None
        self.on_connect: Callable[[], Coroutine[Any, Any, None]] | None = None
        self.on_disconnect: Callable[[], Coroutine[Any, Any, None]] | None = None
        self.on_error: Callable[[Exception], Coroutine[Any, Any, None]] | None = None

        # Logger
        self.logger = logger

    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected"""
        return self.ws is not None

    def _get_websocket_url(self) -> str:
        """Build WebSocket URL"""
        base_url = self.config.websocket_url
        return f"{base_url}/ws/"

    def _get_headers(self) -> dict:
        """Get authentication headers"""
        return {
            "Authorization": f"Bearer {self.config.agent_id}:{self.config.token.get_secret_value()}",
            "X-Tenant-Domain": self.config.tenant_domain,
            "User-Agent": f"RecurveAgent/{VERSION}",
        }

    async def connect(self) -> bool:
        """Connect to WebSocket server"""
        if self.is_connected:
            return True

        self.logger.info("Connecting to WebSocket server...")

        try:
            url = self._get_websocket_url()
            headers = self._get_headers()

            self.ws = await websockets.connect(
                url,
                additional_headers=headers,
                # Auto ping for keepalive
                ping_interval=10,
                ping_timeout=8,
                max_size=10 * MiB,
            )

            self._last_activity = time.time()
            self.logger.info("WebSocket connected successfully")

            if self.on_connect:
                try:
                    await self.on_connect()
                except Exception as e:
                    self.logger.error(f"Connect callback failed: {e}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")
            self.ws = None
            if self.on_error:
                try:
                    await self.on_error(e)
                except Exception as callback_error:
                    self.logger.error(f"Error callback failed: {callback_error}")
                    raise callback_error from e

            raise

    async def disconnect(self) -> None:
        """Disconnect from WebSocket server"""
        if self.is_connected:
            self.logger.info("Disconnecting from WebSocket server...")
            try:
                await self.ws.close()
            except Exception as e:
                self.logger.debug(f"Error closing WebSocket (might be already closed): {e}")

        # Always release the instance and call disconnect callback
        self.ws = None

        if self.on_disconnect:
            try:
                await self.on_disconnect()
            except Exception as e:
                self.logger.error(f"Disconnect callback failed: {e}")

    async def send_message(self, message: str) -> bool:
        """Send text message"""
        if not self.is_connected:
            self.logger.warning("Not connected, cannot send message")
            self.logger.info("Attempting to reconnect...")
            await self.connect()

        try:
            await self.ws.send(message)
            self.logger.debug(f"Sent: {message[:100]}{'...' if len(message) > 100 else ''}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    async def send_json(self, data: dict) -> bool:
        """Send JSON message"""
        # auto add sending_time
        if data.get("sending_time") is None:
            data["sending_time"] = datetime.now(UTC).isoformat()

        try:
            message = json.dumps(data, ensure_ascii=False)
            return await self.send_message(message)
        except Exception as e:
            self.logger.error(f"JSON serialization failed: {e}")
            return False

    @tenacity.retry(
        # include the first time call
        stop=tenacity.stop_after_attempt(4),
        # wait time: 0s-10s-20s
        wait=tenacity.wait_exponential(multiplier=5, min=0, max=120),
        retry=tenacity.retry_if_exception_type(RetryableWebSocketException),
    )
    async def listen_loop(self) -> None:
        """Message listening loop"""
        self.logger.info("Starting WebSocket message loop...")

        if not self.is_connected:
            self.logger.error("No WebSocket connection to listen on!")
            self.logger.info("Attempting to reconnect...")
            try:
                await self.connect()
            except Exception as e:
                self.logger.error(f"Failed to connect: {e}")
                raise RetryableWebSocketException() from e

        try:
            self.logger.info("Entering message listening loop...")
            async for message in self.ws:
                self.logger.info(f"Received: {message[:100]}{'...' if len(message) > 100 else ''}")

                if self.on_receive_message:
                    try:
                        await self.on_receive_message(message, self)
                    except Exception as e:
                        self.logger.error(f"Message callback failed: {e}")

            # Listen loop exit with no error, maybe server closed the connection
            # try to reconnect
            logger.warning("Listen loop exit with no error, maybe server closed the connection, try to reconnect")
            raise RetryableWebSocketException()

        except RetryableWebSocketException:
            raise
        except ConnectionClosed as e:
            self.logger.warning(f"WebSocket connection closed by peer: {e}")
            # when connection closed for unauthorized, raise exception and exit the agent
            if e.code == 3000:
                self.logger.info("Unauthorized, agent was removed by server")
                raise UnauthorizedError() from e
            raise RetryableWebSocketException() from e
        except WebSocketException as e:
            self.logger.error(f"WebSocket error: {e}")
            if self.on_error:
                try:
                    await self.on_error(e)
                except Exception as callback_error:
                    self.logger.error(f"Error callback failed: {callback_error}")
            raise RetryableWebSocketException() from e
        except Exception as e:
            self.logger.error(f"Unexpected error in message loop: {e}")
            if self.on_error:
                try:
                    await self.on_error(e)
                except Exception as callback_error:
                    self.logger.error(f"Error callback failed: {callback_error}")
            # critical error, exit the agent and restart by systemd
            raise e
        finally:
            # Once the loop is exited, the connection is closed and can be retried
            self.ws = None
            self.logger.info("Message listening loop exit...")

    def set_callbacks(
        self,
        on_receive_message: Callable[[str, "WebSocketConnector"], Coroutine[Any, Any, None]] | None = None,
        on_connect: Callable[[], Coroutine[Any, Any, None]] | None = None,
        on_disconnect: Callable[[], Coroutine[Any, Any, None]] | None = None,
        on_error: Callable[[Exception], Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        """Set callback functions"""
        if on_receive_message is not None:
            self.on_receive_message = on_receive_message
        if on_connect is not None:
            self.on_connect = on_connect
        if on_disconnect is not None:
            self.on_disconnect = on_disconnect
        if on_error is not None:
            self.on_error = on_error

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
