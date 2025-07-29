"""
interval.ddd._dto
~~~~~~~~~~~~~~~~~

This module provides data transfer object base classes.
"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class UseCaseDTO:
    """用例返回的数据传输对象"""

    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return asdict(self)
