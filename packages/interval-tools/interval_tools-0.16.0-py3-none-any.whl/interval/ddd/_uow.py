"""
interval.ddd._uow
~~~~~~~~~~~~~~~~~

This module provides unit of work base classes.
"""

import abc
from typing import Self

from ._messagebus import AbstractMessageBus
from ._repo import Repository


class AbstractUnitOfWork(abc.ABC):
    """工作单元抽象基类

    Attributes:
        message_bus: 消息总线
        repo: 资源库
    """
    message_bus: AbstractMessageBus
    repo: Repository

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        """事务提交"""
        self._commit()
        self.publish_domain_events()

    def rollback(self):
        """事务回滚"""
        self._rollback()

    def publish_domain_events(self):
        """通过消息总线发布领域事件"""
        for entity in self.repo.seen:
            while entity.domain_events:
                event = entity.domain_events.pop(0)
                self.message_bus.publish_domain_event(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _rollback(self):
        raise NotImplementedError
