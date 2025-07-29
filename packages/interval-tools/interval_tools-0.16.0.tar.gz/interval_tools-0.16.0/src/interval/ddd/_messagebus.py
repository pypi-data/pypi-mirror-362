"""
interval.ddd._messagebus
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides message bus base classes.
"""

import abc

from ._event import DomainEvent


class AbstractMessageBus(abc.ABC):
    """消息总线抽象基类"""

    @abc.abstractmethod
    def publish_domain_event(self, event: DomainEvent, **kwargs):
        """发布领域事件

        Args:
            event: 领域事件
        """
        raise NotImplementedError
