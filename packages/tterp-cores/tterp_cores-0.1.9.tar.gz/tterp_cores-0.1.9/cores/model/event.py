from datetime import datetime
from typing import Generic, Optional, TypeVar

from cores.model.base_model import CamelCaseModel

# Định nghĩa generic type cho Payload
Payload = TypeVar("Payload")


class DTOProps(CamelCaseModel):
    id: Optional[str] = None
    occurred_at: Optional[datetime] = None
    sender_id: Optional[str] = None


class AppEvent(CamelCaseModel, Generic[Payload]):
    event_name: str
    payload: Payload
    dto_props: DTOProps | None = None
