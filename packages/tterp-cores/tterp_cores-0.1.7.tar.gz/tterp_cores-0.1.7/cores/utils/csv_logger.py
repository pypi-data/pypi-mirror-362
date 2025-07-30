import csv
import json
from contextvars import ContextVar
from datetime import datetime
from functools import wraps
from pathlib import Path

from fastapi import Request

LOG_DIR = Path("log/csv")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Context global để lưu thông tin request hiện tại
request_context = ContextVar("request_context", default=None)


def set_request_context(request: Request):
    """Thiết lập context cho request hiện tại"""
    if request:
        # Lưu thông tin cần thiết từ request để tránh lưu toàn bộ request
        # object
        context = {"requester_id": None, "ip": None, "request_id": None}

        # Lấy requester_id từ state.requester
        if hasattr(request, "state") and hasattr(request.state, "requester"):
            requester = request.state.requester
            if hasattr(requester, "user_id"):
                context["requester_id"] = requester.user_id
            else:
                context["requester_id"] = str(requester)

        # Lấy IP và request_id
        if hasattr(request, "client"):
            context["ip"] = request.client.host if request.client else None
        if hasattr(request, "headers"):
            context["request_id"] = request.headers.get("x-request-id")

        # Lưu vào context
        request_context.set(context)
    return request_context


def get_requester_id(req_obj=None):
    """Lấy requester_id từ request object hoặc từ context"""
    # Ưu tiên lấy từ request object được truyền vào
    if req_obj:
        if hasattr(req_obj, "state") and hasattr(req_obj.state, "requester"):
            requester = req_obj.state.requester
            if hasattr(requester, "user_id"):
                return requester.user_id
            return str(requester)
        if hasattr(req_obj, "user_id"):
            return req_obj.user_id

    # Nếu không có, lấy từ context
    context = request_context.get()
    if context:
        return context.get("requester_id")

    return None


def log_to_csv(
    module: str,
    action: str,
    requester_id: int = None,
    params=None,
    status="success",
    error_message=None,
    ip: str = None,
    request_id: str = None,
):
    """Ghi log vào file CSV, chỉ lưu các thông tin cần thiết để truy vết"""
    log_file = LOG_DIR / f"{module}_log.csv"

    # Lấy thông tin từ context nếu không có
    context = request_context.get()
    if context:
        if requester_id is None:
            requester_id = context.get("requester_id")
        if ip is None:
            ip = context.get("ip")
        if request_id is None:
            request_id = context.get("request_id")

    # Xử lý params để tránh lỗi serialization
    params_str = ""
    if params:
        try:
            if isinstance(params, dict):
                # Lọc các đối tượng phức tạp không serialize được
                filtered_params = {
                    k: (
                        str(v)
                        if hasattr(v, "__dict__")
                        and not isinstance(
                            v, (str, int, float, bool, list, dict)
                        )
                        else v
                    )
                    for k, v in params.items()
                }
                params_str = json.dumps(
                    filtered_params, ensure_ascii=False, default=str
                )
            else:
                params_str = str(params)
        except Exception:
            params_str = str(params)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "action": action,
        "requester_id": requester_id,
        "params": params_str,
        "status": status,
        "error_message": error_message or "",
        "ip": ip or "",
        "request_id": request_id or "",
    }

    write_header = not log_file.exists()
    with open(log_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(log_entry)


def get_logs(module: str, limit: int = 100):
    """Lấy log từ file CSV với giới hạn số lượng"""
    log_file = LOG_DIR / f"{module}_log.csv"
    if not log_file.exists():
        return []
    with open(log_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        logs = list(reader)
    return logs[-limit:]


def auto_log(module: str, action: str = None):
    """
    Decorator để tự động log mọi hàm public của usecase/service.
    Log cả exception, log thêm IP/request_id nếu có trong context.
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Lọc bỏ các tham số không serialize được từ kwargs
            filtered_params = {}
            for k, v in kwargs.items():
                if k not in ["request", "req"]:  # Không log request object
                    if hasattr(v, "__dict__") and not isinstance(
                        v, (str, int, float, bool, list, dict)
                    ):
                        # Chỉ lưu class name hoặc các thuộc tính cơ bản
                        if hasattr(v, "id"):
                            filtered_params[k] = (
                                f"{v.__class__.__name__}(id={v.id})"
                            )
                        else:
                            filtered_params[k] = f"{v.__class__.__name__}"
                    else:
                        filtered_params[k] = v

            # Lấy requester_id từ context
            requester_id = None
            if "requester_id" in kwargs and kwargs["requester_id"]:
                requester_id = kwargs["requester_id"]
            else:
                context = request_context.get()
                if context:
                    requester_id = context.get("requester_id")

            try:
                result = await func(*args, **kwargs)
                log_to_csv(
                    module=module,
                    action=action or func.__name__,
                    requester_id=requester_id,
                    params=filtered_params,
                    status="success",
                )
                return result
            except Exception as e:
                log_to_csv(
                    module=module,
                    action=action or func.__name__,
                    requester_id=requester_id,
                    params=filtered_params,
                    status="fail",
                    error_message=str(e),
                )
                raise

        return async_wrapper

    return decorator
