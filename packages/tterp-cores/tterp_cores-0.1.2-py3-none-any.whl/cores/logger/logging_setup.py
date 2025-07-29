"""
Module thiết lập logging cho ELK Stack (Elasticsearch, Logstash, Kibana).

Module này cung cấp các thành phần để gửi logs đến ELK Stack thông qua Filebeat:
- JSONFormatter để format logs dưới dạng JSON
- AsyncTCPLogHandler để gửi logs bất đồng bộ qua TCP
- ELKLogger để log các loại thông tin khác nhau với cấu trúc phù hợp cho ELK
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from cores.config import logging_config, service_config
from cores.logger.logging import ApiLogger


class JSONFormatter(logging.Formatter):
    """
    Custom JSON Formatter để định dạng log messages dưới dạng JSON.

    Format log messages thành cấu trúc JSON phù hợp với ELK Stack,
    bao gồm các thông tin như environment, timestamp, log level, và các
    thông tin bổ sung.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record thành chuỗi JSON.

        Args:
            record: Log record cần format

        Returns:
            Chuỗi JSON chứa thông tin log đã được format
        """
        message_data = record.getMessage()
        # ApiLogger.error(message_data)
        message_data_as_dict: Dict[str, Any] = json.loads(message_data)

        log_record = {
            "env": service_config.APP_ENV,
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": message_data_as_dict.get("message", ""),
            "log_type": message_data_as_dict.get("log_type"),
            "user_id": message_data_as_dict.get("user_id", -1),
            "item_id": message_data_as_dict.get("item_id", -1),
            "processing_time": message_data_as_dict.get("processing_time", -1),
            "extra_info": json.dumps(message_data_as_dict.get("extra_info")),
            "logger_name": record.name,
            "service_id": service_config.BASE_SERVICE_ID,  # Tên service hiện tại
            # "host": socket.gethostname(),
            # "path": record.pathname,
            # "line": record.lineno,
            # "module": record.module,
            # "function": record.funcName,
            # "exc_info": self.formatException(record.exc_info) if record.exc_info else None
        }
        # ApiLogger.error(log_record)
        return json.dumps(log_record)


class AsyncTCPLogHandler(logging.Handler):
    """
    Handler để gửi logs bất đồng bộ qua TCP socket.

    Sử dụng asyncio để gửi logs mà không chặn luồng chính của ứng dụng.
    Logs được đưa vào queue và được xử lý bởi một task riêng biệt.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Khởi tạo handler với host và port của Filebeat.

        Args:
            host: Địa chỉ host của Filebeat
            port: Port của Filebeat
        """
        super().__init__()
        self.host = host
        self.port = port
        self.queue: asyncio.Queue = (
            asyncio.Queue()
        )  # Hàng đợi cho log messages
        self.loop = asyncio.get_event_loop()  # Lấy event loop hiện tại
        self.task = self.loop.create_task(
            self.send_logs()
        )  # Bắt đầu task để gửi log

    async def send_logs(self) -> None:
        """
        Task bất đồng bộ để gửi logs từ queue.

        Chạy vô hạn cho đến khi nhận được giá trị None trong queue,
        lấy log messages từ queue và gửi chúng qua TCP.
        """
        while True:
            log_message = await self.queue.get()  # Chờ đến khi có log message
            if log_message is None:  # Nếu nhận được None, dừng task
                break
            await self._send_log(log_message)  # Gửi log

    async def _send_log(self, log_message: str) -> None:
        """
        Gửi một log message qua TCP socket.

        Args:
            log_message: Message cần gửi
        """
        try:
            reader, writer = await asyncio.open_connection(
                self.host, self.port
            )
            writer.write(log_message.encode("utf-8"))  # Ghi log vào socket
            await writer.drain()  # Đợi cho tới khi log được gửi
            writer.close()  # Đóng kết nối
            await writer.wait_closed()  # Đợi cho đến khi kết nối đóng hoàn toàn
        except Exception as e:
            ApiLogger.error(f"Error sending log: {e}")

    def emit(self, record: logging.LogRecord) -> None:
        """
        Xử lý một log record bằng cách đưa vào queue.

        Args:
            record: Log record cần xử lý
        """
        log_message = self.format(record) + "\n"
        # Đưa log vào hàng đợi, nhưng sử dụng await để chắc chắn coroutine được
        # chờ
        asyncio.create_task(
            self.queue.put(log_message)
        )  # Đưa log vào hàng đợi

    async def async_close(self) -> None:
        """
        Đóng handler một cách bất đồng bộ.

        Đưa None vào queue để kết thúc task send_logs và chờ task hoàn thành.
        """
        # Đưa None vào hàng đợi để kết thúc task và chờ task hoàn thành
        await self.queue.put(None)
        await self.task

    def close(self) -> None:
        """
        Đóng handler và giải phóng tài nguyên.

        Gọi async_close trong event loop và sau đó gọi close của lớp cha.
        """
        if not self.loop.is_closed():  # Kiểm tra xem loop đã bị đóng chưa
            try:
                self.loop.run_until_complete(
                    self.async_close()
                )  # Đóng một cách an toàn
            except RuntimeError as e:
                ApiLogger.error(
                    f"Failed to close AsyncTCPLogHandler cleanly: {e}"
                )
        super().close()


# Create AsyncTCPLogHandler
tcp_handler = AsyncTCPLogHandler(
    logging_config.FILEBEAT_HOST, logging_config.FILEBEAT_PORT
)
tcp_handler.setLevel(logging.INFO)

# Set JSON Formatter for TCP handler
json_formatter = JSONFormatter()
tcp_handler.setFormatter(json_formatter)

# Create logger
logger = logging.getLogger("my_fastapi_app")
logger.addHandler(tcp_handler)
logger.setLevel(logging.INFO)


class ELKLogger:
    """
    Logger chuyên biệt để gửi logs đến ELK Stack.

    Cung cấp các phương thức tiện ích để log các loại thông tin khác nhau
    với cấu trúc phù hợp cho việc phân tích trong ELK Stack.
    """

    @staticmethod
    def log(
        message: str,
        log_type: str = "info",
        extra_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log một thông điệp với loại và thông tin bổ sung.

        Args:
            message: Thông điệp cần log
            log_type: Loại log (info, action, error, etc.)
            extra_info: Thông tin bổ sung dưới dạng dictionary
        """
        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "log_type": log_type,  # Thêm loại log vào thông tin
            }
        )
        if log_type == "action":
            logger.info(log_message)
        elif log_type == "error":
            logger.error(log_message)
        else:
            logger.info(log_message)  # Mặc định là log info

    @staticmethod
    def log_action(
        action: str,
        current_user_id: int,
        entity_id: int,
        payload: Dict[str, Any] = {},
        is_success: bool = True,
        error: Optional[str] = None,
    ) -> None:
        """
        Log một hành động người dùng với các thông tin liên quan.

        Args:
            action: Tên hành động
            current_user_id: ID của người dùng thực hiện hành động
            entity_id: ID của đối tượng liên quan đến hành động
            payload: Dữ liệu bổ sung của hành động
            is_success: Hành động có thành công hay không
            error: Thông báo lỗi nếu hành động thất bại
        """
        tag = "[Success]" if is_success else "[Error]"
        message = f"{tag} {action}"
        extra_info = {"error": error, "payload": payload}

        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "log_type": "action",  # Thêm loại log vào thông tin
                "user_id": current_user_id,
                "item_id": entity_id,
            }
        )
        logger.info(log_message)

    @staticmethod
    def log_processing_time(
        message: str,
        processing_time: float,
        extra_info: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log thời gian xử lý của một hoạt động.

        Args:
            message: Mô tả hoạt động
            processing_time: Thời gian xử lý (giây)
            extra_info: Thông tin bổ sung
        """
        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "processing_time": processing_time,
                "log_type": "processing_time",  # Thêm loại log vào thông tin
            }
        )
        logger.info(log_message)


# # Example usage for action log
# def log_action(action, user_id, item_id):
#     ELKLogger.log(f"Action performed: {action}", log_type="action", extra_info={
#         "action": action,
#         "user_id": user_id,
#         "item_id": item_id
#     })

# def log_processing_time(action_name: str):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             start_time = datetime.utcnow()  # Bắt đầu tính thời gian
#             result = await func(*args, **kwargs)
#             end_time = datetime.utcnow()  # Kết thúc tính thời gian
#             processing_time = (end_time - start_time).total_seconds()
#             ELKLogger.log(f"Processing time for {action_name}: {processing_time}s", log_type="processing_time")
#             return result
#         return wrapper
#     return decorator

# def log_action(action_name: str):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Lấy request từ args (giả sử request luôn là tham số đầu tiên hoặc có trong kwargs)
#             request: Request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)
#             if request:
#                 route_name = request.scope["path"]
#             else:
#                 route_name = "unknown"
#             # Lấy current_user_id từ kwargs (nếu có)
#             current_user_id = kwargs.get('user_id', 'Unknown User')
#             ELKLogger.log(f"Action performed: {action_name}", log_type="action", extra_info={
#                 "action": route_name,
#                 "user_id": current_user_id,
#             })
#             result = await func(*args, **kwargs)
#             return result
#         return wrapper
#     return decorator
