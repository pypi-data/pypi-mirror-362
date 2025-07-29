"""
interval.ddd._entity
~~~~~~~~~~~~~~~~~~~~

This module provides Entity base class and derived classes.
"""


class Entity:
    """实体

    Attributes:
        ref: 唯一标识
    """

    def __init__(self, ref):
        self.ref = ref

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return other.ref == self.ref

    def __hash__(self):
        return hash(self.ref)

    def __repr__(self):
        return f'<{type(self).__name__} {self.ref!r}>'


class Aggregate(Entity):
    """聚合根实体

    Attributes:
        ref: 唯一标识
        version_number: 版本号，用于支持乐观锁
        domain_events: 领域事件列表
    """

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.domain_events = []
        return obj

    def __init__(self, ref, version_number: int = 1):
        super().__init__(ref)
        self.version_number = version_number

    def add_lock(self):
        """主动添加乐观锁"""
        self.version_number += 1
