# app/events/event_bus.py

from abc import ABC, abstractmethod

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractExchange,
    AbstractQueue,
)

from cores.config import messaging_config

# Import các thành phần cần thiết
from cores.events.schemas.base_event import Event


class EventBus(ABC):
    @abstractmethod
    async def connect(self): ...
    @abstractmethod
    async def disconnect(self): ...
    @abstractmethod
    async def publish(self, event: Event): ...
    @abstractmethod
    async def setup_consumer(
        self, queue_name: str, binding_keys: list[str]
    ) -> AbstractQueue: ...


# Lớp InMemoryEventBus giữ nguyên để testing


class InMemoryEventBus(EventBus):
    async def connect(self):
        print("InMemoryEventBus connected.")

    async def disconnect(self):
        print("InMemoryEventBus disconnected.")

    async def publish(self, event: Event):
        print(f"--- Event Published (In-Memory): {event.event_name} ---")
        print(f"Data: {event.model_dump_json(indent=2)}")

    async def setup_consumer(
        self, queue_name: str, binding_keys: list[str]
    ) -> AbstractQueue:
        print(
            f"InMemoryEventBus: Queue '{queue_name}' bound to exchange with key '{binding_keys}'"
        )
        return None


# --- TRIỂN KHAI RABBITMQQEVENTBUS HOÀN CHỈNH ---
class RabbitMQEventBus(EventBus):
    def __init__(self):
        self.exchange_name = messaging_config.RABBITMQ_EXCHANGE
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None
        self.exchange: AbstractExchange = None

    async def connect(self):
        """
        Sử dụng connect_robust để kết nối tự động lại nếu bị mất kết nối.
        Khai báo một exchange loại 'topic' để định tuyến sự kiện linh hoạt.
        """
        try:
            self.connection = await aio_pika.connect_robust(
                host=messaging_config.RABBITMQ_HOST,
                port=messaging_config.RABBITMQ_PORT,
                login=messaging_config.RABBITMQ_USER,
                password=messaging_config.RABBITMQ_PASS,
                virtualhost=messaging_config.RABBITMQ_VHOST,
            )
            self.channel = await self.connection.channel()
            # Khai báo exchange, durable=False để phù hợp với cấu hình hiện tại
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name, aio_pika.ExchangeType.TOPIC, durable=False
            )
            print("Successfully connected to RabbitMQ and declared exchange.")
        except Exception as e:
            print(f"Failed to connect to RabbitMQ. Error: {e}")
            # Có thể thêm logic retry hoặc thoát ứng dụng ở đây
            raise

    async def disconnect(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        print("EventBus: Disconnected from RabbitMQ.")

    async def publish(self, event: Event):
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
        if not self.channel or not self.exchange:
            raise ConnectionError("EventBus is not connected.")

        queue = await self.channel.declare_queue(queue_name, durable=False)

        for key in binding_keys:
            await queue.bind(self.exchange, routing_key=key)
            print(
                f"EventBus: Queue '{queue_name}' bound to exchange with key '{key}'"
            )

        return queue
