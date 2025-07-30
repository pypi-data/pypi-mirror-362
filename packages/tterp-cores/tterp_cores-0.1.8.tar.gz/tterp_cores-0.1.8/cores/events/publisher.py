
from .event_bus import EventBus
from .schemas.base_event import Event


class EventPublisher:
    def __init__(self, bus: EventBus):
        self.bus = bus

    async def publish(self, event: Event):
        await self.bus.publish(event)
