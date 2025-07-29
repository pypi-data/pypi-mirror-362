"""
interval.ddd
~~~~~~~~~~~~

This package provides basic components of Domain-Driven Design.
"""

from ._dto import UseCaseDTO
from ._entity import Entity, Aggregate
from ._event import DomainEvent
from ._exceptions import (
    DDDException,
    DomainException,
    ServiceLayerException,
    AdapterException,
    RemoteServiceException,
    DBAPIError,
    InterfaceError,
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
    DBAPIErrorWrapper,
    STANDARD_DBAPI_ERRORS
)
from ._messagebus import AbstractMessageBus
from ._repo import Repository
from ._uow import AbstractUnitOfWork
from ._valueobject import (
    ValueObject,
    IntegerRef,
    StringRef,
    UUIDRef,
    OIDRef
)
