"""
Event Publisher - Lớp để publish các sự kiện

Cung cấp lớp EventPublisher để publish các sự kiện thông qua EventBus
"""

from cores.events.event_bus import EventBus
from cores.events.schemas.base_event import Event
from cores.logger.logging import ApiLogger


class EventPublisher:
    """
    Lớp để publish các sự kiện thông qua EventBus

    Lớp này đóng vai trò là một wrapper đơn giản cho EventBus,
    cho phép ghi log và xử lý lỗi khi publish sự kiện.
    """

    def __init__(self, bus: EventBus):
        """
        Khởi tạo EventPublisher với một EventBus

        Args:
            bus: EventBus để publish sự kiện
        """
        self.bus = bus
        self.logger = ApiLogger.get_logger()

    async def publish(self, event: Event):
        """
        Publish một sự kiện thông qua EventBus

        Args:
            event: Sự kiện cần publish
        """
        try:
            await self.bus.publish(event)
            self.logger.info(f"Published event: {event.event_name}")
        except Exception as e:
            self.logger.error(
                f"Failed to publish event {event.event_name}: {e}"
            )
            raise
