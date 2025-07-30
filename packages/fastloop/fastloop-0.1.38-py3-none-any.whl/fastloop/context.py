import asyncio
from typing import TYPE_CHECKING, Any, TypeVar, Union

from .constants import EVENT_POLL_INTERVAL_S
from .exceptions import EventTimeoutError, LoopPausedError, LoopStoppedError
from .state.state import StateManager
from .types import LoopEventSender

if TYPE_CHECKING:
    from .loop import LoopEvent

T = TypeVar("T")


class LoopContext:
    def __init__(
        self,
        loop_id: str | None = None,
        initial_event: dict[str, Any] | None = None,
        state_manager: StateManager | None = None,
    ):
        self._stop_requested: bool = False
        self._pause_requested: bool = False
        self.loop_id: str | None = loop_id
        self.initial_event: dict[str, Any] = initial_event or {}
        self.state_manager: StateManager = state_manager
        self.event_this_cycle: bool = False

    def stop(self):
        """Request the loop to stop on the next iteration."""
        self._stop_requested = True

    def pause(self):
        """Request the loop to pause on the next iteration."""
        self._pause_requested = True

    def sleep(self, seconds: float):
        raise NotImplementedError("Sleep is not implemented")

    async def wait_for(
        self,
        event: "LoopEvent",
        timeout: float | int = 10.0,
        raise_on_timeout: bool = True,
    ) -> Union["LoopEvent", None]:
        start = asyncio.get_event_loop().time()
        pubsub = await self.state_manager.subscribe_to_events(self.loop_id)

        if isinstance(timeout, int):
            timeout = float(timeout)
        elif not isinstance(timeout, float):
            raise ValueError("Timeout must be a float")

        if timeout <= 0:
            raise ValueError("Timeout must be greater than 0.0")

        try:
            while not self.should_stop:
                if asyncio.get_event_loop().time() - start >= timeout:
                    break

                if self.should_pause:
                    raise LoopPausedError()

                if self.should_stop:
                    raise LoopStoppedError()

                # Try to get event immediately
                event_result = await self.state_manager.pop_event(
                    self.loop_id, event, sender=LoopEventSender.CLIENT
                )
                if event_result is not None:
                    self.event_this_cycle = True
                    return event_result

                # Wait for notification or timeout
                remaining_timeout = timeout - (asyncio.get_event_loop().time() - start)
                if remaining_timeout <= 0:
                    break

                # Wait for event notification or poll interval
                poll_timeout = min(
                    EVENT_POLL_INTERVAL_S, remaining_timeout or EVENT_POLL_INTERVAL_S
                )
                await self.state_manager.wait_for_event_notification(
                    pubsub, timeout=poll_timeout
                )

        finally:
            if pubsub is not None:
                await pubsub.unsubscribe()
                await pubsub.close()

        if raise_on_timeout:
            raise EventTimeoutError(f"Timeout waiting for event {event.type}")
        else:
            return None

    async def emit(
        self,
        event: "LoopEvent",
    ):
        event.sender = LoopEventSender.SERVER
        event.loop_id = self.loop_id
        event.nonce = await self.state_manager.get_next_nonce(self.loop_id)
        self.event_this_cycle = True
        await self.state_manager.push_event(self.loop_id, event)

    async def set(self, key: str, value: Any):
        await self.state_manager.set_context_value(self.loop_id, key, value)
        setattr(self, key, value)

    async def get(self, key: str, default: Any = None) -> Any:
        if not hasattr(self, key):
            value = await self.state_manager.get_context_value(self.loop_id, key)
            if value is None:
                if default is None:
                    return None

                value = default

            setattr(self, key, value)

        return getattr(self, key)

    async def get_event_history(self) -> list["LoopEvent"]:
        return await self.state_manager.get_event_history(self.loop_id)

    @property
    def should_stop(self) -> bool:
        """Check if the loop should stop."""
        return self._stop_requested

    @property
    def should_pause(self) -> bool:
        """Check if the loop should pause."""
        return self._pause_requested
