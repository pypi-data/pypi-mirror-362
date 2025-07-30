"""rabbitmq.py
Module triển khai `RabbitMQClient` hỗ trợ publish / subscribe sự kiện qua
RabbitMQ sử dụng **exchange kiểu topic**.

Mục tiêu refactor: bổ sung tài liệu, type-hint, thứ tự import đúng PEP8, tuyệt
đối **không** thay đổi logic gốc nhằm đảm bảo mọi chức năng & test hiện tại
giữ nguyên.
"""

from __future__ import annotations

import json
import traceback
from typing import Callable, Dict, List, TypeVar

import pika
from fastapi.encoders import jsonable_encoder

from cores.config import service_config
from cores.logger.logging import ApiLogger
from cores.model.event import AppEvent

# Type variable for generic type
T = TypeVar("T")

# Define the event handler type
EventHandler = Callable[[str], None]


class RabbitMQClient:
    """Singleton quản lý kết nối RabbitMQ cho toàn bộ ứng dụng."""

    _instance = None
    _connection: pika.BlockingConnection | None = None
    _channel = None
    _subscriber_map: Dict[str, List[pika.BlockingConnection]] = {}

    def __init__(self):
        self._subscriber_map = {}

    @classmethod
    def init(cls):
        if not cls._instance:
            cls._instance = RabbitMQClient()
            cls._instance._connect()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "RabbitMQClient":
        if not cls._instance:
            raise Exception("RabbitMQClient instance not initialized")
        return cls._instance

    def _connect(self) -> None:
        """Tạo *blocking connection* và khai báo exchange mặc định."""
        try:
            credentials = pika.PlainCredentials(
                service_config.RABBITMQ_USER, service_config.RABBITMQ_PASS
            )
            parameters = pika.ConnectionParameters(
                host=service_config.RABBITMQ_HOST,
                port=service_config.RABBITMQ_PORT,
                credentials=credentials,
            )
            self._connection = pika.BlockingConnection(parameters)
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange="events", exchange_type="topic"
            )

            ApiLogger.success("Connected to RabbitMQ server")
        except Exception as error:
            ApiLogger.error("[RB] Err connection: " + str(error))

    async def publish(self, event: AppEvent[T]) -> None:
        """Publish một sự kiện lên exchange `events`.

        Args:
            event: Đối tượng `AppEvent` cần gửi.
        """
        try:
            if not self._channel or self._channel.is_closed:
                self._connect()
                if not self._channel or self._channel.is_closed:
                    raise Exception("Kết nối không thành công")

            message = jsonable_encoder(event)
            self._channel.basic_publish(
                exchange="events",
                routing_key=event.event_name,
                body=json.dumps(message).encode(),
            )
        except pika.exceptions.ChannelWrongStateError as e:
            ApiLogger.error("[RB] Channel is closed: " + str(e))
            self._connect()  # Attempt to reconnect
            await self.publish(event)  # Retry publishing the message
        except Exception:
            ApiLogger.error(
                "[RB] Err publish message: " + traceback.format_exc()
            )

    def process_message(
        self, message: str
    ) -> None:  # noqa: D401, D401 doc like imperative
        """Xử lý nội dung message.

        Mặc định *raise* để buộc subclass cài đặt.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def subscribe(self, topic: str) -> None:
        """Đăng ký lắng nghe một *routing_key* cụ thể trên exchange `events`.

        Args:
            topic: routing key (vd: `user.created`).
        """

        def callback(ch, method, properties, body):
            # print(
            #     f" [x] Received message: {truncated_message} for {self.queue_name}"
            # )
            try:
                self.process_message(body.decode())
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                if service_config.APP_ENV != "production":
                    print(123, traceback.format_exc())
                ApiLogger.error(
                    "[RB] Err publish message: " + traceback.format_exc()
                )

        # Create a new connection for each subscriber
        credentials = pika.PlainCredentials(
            service_config.RABBITMQ_USER, service_config.RABBITMQ_PASS
        )
        parameters = pika.ConnectionParameters(
            host=service_config.RABBITMQ_HOST,
            port=service_config.RABBITMQ_PORT,
            credentials=credentials,
        )
        subscriber_conn = pika.BlockingConnection(parameters)
        channel = subscriber_conn.channel()
        channel.exchange_declare(exchange="events", exchange_type="topic")
        queue_name = f"queue_{topic}_{id(subscriber_conn)}"
        channel.queue_declare(
            queue=queue_name, exclusive=True, auto_delete=True
        )
        channel.queue_bind(
            exchange="events", queue=queue_name, routing_key=topic
        )

        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print(
            f""" [*] Waiting for messages in
        routing key: {topic}
        queue: {queue_name}
        exchange: {"events"}
To exit press CTRL+C"""
        )
        channel.start_consuming()

    async def disconnect(self) -> None:
        """Đóng kết nối & channel (nếu còn mở)."""
        try:
            if self._channel:
                self._channel.close()
            if self._connection:
                self._connection.close()
            ApiLogger.info("Disconnected RabbitMQ server")
        except Exception as error:
            ApiLogger.error("[RB] Err disconnection: " + str(error))

    def delete_queue(self, queue_name: str) -> None:
        """Xóa queue chỉ khi queue không còn được sử dụng (if_unused=True)."""
        try:
            if self._channel:
                # Thử xóa queue mà không yêu cầu quyền truy cập exclusive
                self._channel.queue_delete(queue=queue_name, if_unused=True)
                ApiLogger.info(f"Queue '{queue_name}' has been deleted.")
        except pika.exceptions.AMQPChannelError as e:
            ApiLogger.error(
                f"[RB] Error deleting queue (channel error): {str(e)}"
            )
        except pika.exceptions.AMQPResourceError as e:
            ApiLogger.error(
                f"[RB] Error deleting queue (resource error): {str(e)}"
            )
        except Exception as e:
            ApiLogger.error(f"[RB] Error deleting queue: {str(e)}")

    def close_all_connections(self, queue_name: str) -> None:
        """Đóng tất cả connection trong `_subscriber_map` liên quan `queue_name`."""
        try:
            # Duyệt qua tất cả các kết nối và đóng những kết nối liên quan đến
            # queue_name
            for topic, subs in self._subscriber_map.items():
                for conn in subs:
                    if conn.is_open:
                        conn.close()
                        ApiLogger.info(
                            f"Closed connection for queue '{queue_name}'"
                        )
        except Exception as e:
            ApiLogger.error(
                f"[RB] Error closing connections for queue '{queue_name}': {str(e)}"
            )


# Ví dụ sử dụng pub/sub
async def example_usage():
    # Khởi tạo RabbitMQClient
    RabbitMQClient.init()
    client = RabbitMQClient.get_instance()

    # Hàm xử lý khi nhận được message
    def handle_message(message: str):
        data = json.loads(message)
        print(f"Nhận được sự kiện: {data['eventName']}")
        print(f"Payload: {data['payload']}")
        print(f"Thời điểm: {data['occurredAt']}")
        print("-" * 50)

    # Subscribe vào topic 'user.created'
    await client.subscribe("user.created", handle_message)

    # Publish một sự kiện
    event = AppEvent(
        event_name="user.created",
        payload={"user_id": "123", "name": "Nguyen Van A"},
    )
    await client.publish(event)

    # Giữ chương trình chạy để nhận message
    print("Đang chờ nhận sự kiện... (Ctrl+C để thoát)")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.disconnect()
        print("Đã thoát chương trình")


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_usage())
