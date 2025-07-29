"""
interval.ddd._event
~~~~~~~~~~~~~~~~~~~

This module provides event base classes.
"""

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from ..utils import get_datetime_with_local_tz


@dataclass
class DomainEvent:
    """领域事件

    Attributes:
        id: 事件ID
        occurred_at: 事件发生时间（包含本地时区）
        delay_ms: 事件延迟时长（毫秒）
    """
    id: str = field(
        default_factory=lambda: str(uuid.uuid1()),
        init=False
    )
    occurred_at: datetime = field(
        default_factory=get_datetime_with_local_tz,
        init=False
    )
    delay_ms: int = field(
        default=0,
        init=False
    )

    @property
    def correlation_id(self) -> str:
        """相互关联标识（默认值为事件ID，事件之间不相关）"""
        return self.id

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return asdict(self)
