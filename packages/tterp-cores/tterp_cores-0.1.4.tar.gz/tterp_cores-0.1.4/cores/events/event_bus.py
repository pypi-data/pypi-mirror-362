"""
Event Bus - Định nghĩa các lớp EventBus để xử lý sự kiện

Cung cấp các lớp:
- EventBus: Lớp trừu tượng định nghĩa interface cho event bus
- InMemoryEventBus: Triển khai đơn giản cho môi trường phát triển và testing
- RabbitMQEventBus: Triển khai sử dụng RabbitMQ cho môi trường production
"""

from abc import ABC, abstractmethod

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractQueue,
)

from cores.config import messaging_config
from cores.events.schemas.base_event import Event


class EventBus(ABC):
    """
    Lớp trừu tượng định nghĩa interface cho event bus
    """

    @abstractmethod
    async def connect(self):
        """Kết nối tới message broker"""

    @abstractmethod
    async def disconnect(self):
        """Ngắt kết nối khỏi message broker"""

    @abstractmethod
    async def publish(self, event: Event):
        """Publish một sự kiện"""

    @abstractmethod
    async def setup_consumer(
        self, queue_name: str, binding_keys: list[str]
    ) -> AbstractQueue:
        """Thiết lập consumer cho các routing keys cụ thể"""


class InMemoryEventBus(EventBus):
    """
    Triển khai EventBus đơn giản sử dụng bộ nhớ, dùng cho môi trường phát triển và testing
    """

    async def connect(self):
        """Giả lập kết nối"""
        print("InMemoryEventBus connected.")

    async def disconnect(self):
        """Giả lập ngắt kết nối"""
        print("InMemoryEventBus disconnected.")

    async def publish(self, event: Event):
        """In sự kiện ra console thay vì publish thực sự"""
        print(f"--- Event Published (In-Memory): {event.event_name} ---")
        print(f"Data: {event.model_dump_json(indent=2)}")

    async def setup_consumer(
        self, queue_name: str, binding_keys: list[str]
    ) -> AbstractQueue:
        """Giả lập thiết lập consumer"""
        print(
            f"InMemoryEventBus: Queue '{queue_name}' bound to exchange with key '{binding_keys}'"
        )
        return None


class RabbitMQEventBus(EventBus):
    """
    Triển khai EventBus sử dụng RabbitMQ, dùng cho môi trường production
    """

    def __init__(self):
        self.exchange_name = messaging_config.RABBITMQ_EXCHANGE
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange = None

    async def connect(self):
        """
        Kết nối tới RabbitMQ và khai báo exchange

        Sử dụng connect_robust để kết nối tự động lại nếu bị mất kết nối.
        Khai báo một exchange loại 'topic' để định tuyến sự kiện linh hoạt.
        """
        try:
            self.connection = await aio_pika.connect_robust(
                host=messaging_config.RABBITMQ_HOST,
                port=messaging_config.RABBITMQ_PORT,
                login=messaging_config.RABBITMQ_USER,
                password=messaging_config.RABBITMQ_PASSWORD,
                virtualhost=messaging_config.RABBITMQ_VHOST,
            )
            self.channel = await self.connection.channel()
            # Khai báo exchange, durable=True để đảm bảo tồn tại sau khi
            # restart
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
            )
            print("Successfully connected to RabbitMQ and declared exchange.")
        except Exception as e:
            print(f"Failed to connect to RabbitMQ. Error: {e}")
            raise

    async def disconnect(self):
        """Đóng kết nối tới RabbitMQ"""
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        print("EventBus: Disconnected from RabbitMQ.")

    async def publish(self, event: Event):
        """
        Publish một sự kiện tới RabbitMQ exchange

        Args:
            event: Sự kiện cần publish

        Raises:
            ConnectionError: Nếu chưa kết nối tới RabbitMQ
        """
        if not self.exchange:
            raise ConnectionError(
                "RabbitMQ exchange not available. Is the bus connected?"
            )

        routing_key = event.event_name
        message = aio_pika.Message(
            body=event.model_dump_json().encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self.exchange.publish(message, routing_key=routing_key)
        print(f"EventBus: Published event with routing key '{routing_key}'")

    async def setup_consumer(
        self, queue_name: str, binding_keys: list[str]
    ) -> AbstractQueue:
        """
        Thiết lập consumer cho các routing keys cụ thể

        Args:
            queue_name: Tên của queue
            binding_keys: Danh sách các routing key để bind

        Returns:
            Queue đã được khai báo và bind

        Raises:
            ConnectionError: Nếu chưa kết nối tới RabbitMQ
        """
        if not self.channel or not self.exchange:
            raise ConnectionError("EventBus is not connected.")

        queue = await self.channel.declare_queue(queue_name, durable=True)

        for key in binding_keys:
            await queue.bind(self.exchange, routing_key=key)
            print(
                f"EventBus: Queue '{queue_name}' bound to exchange with key '{key}'"
            )

        return queue
