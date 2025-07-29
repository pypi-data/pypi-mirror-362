"""
interval.ddd._exceptions
~~~~~~~~~~~~~~~~~~~~~~~~

This module provides exceptions.
"""

import functools
import sys


class DDDException(Exception):
    """根异常"""
    code: int = None  # 错误码
    msg: str = None  # 错误描述
    detail: dict = None  # 错误详情


class DomainException(DDDException):
    """领域异常"""
    pass


class ServiceLayerException(DDDException):
    """服务层异常"""
    pass


class AdapterException(DDDException):
    """适配器异常"""
    pass


class RemoteServiceException(AdapterException):
    """远程服务异常"""
    pass


class DBAPIError(AdapterException):
    """Wraps a DB-API 2.0 Error"""

    @property
    def orig(self) -> Exception | None:
        return self.__cause__

    def __str__(self):
        if self.orig:
            return self.orig.__str__()
        else:
            return super().__str__()


class InterfaceError(DBAPIError): pass
class DatabaseError(DBAPIError): pass
class DataError(DatabaseError): pass
class OperationalError(DatabaseError): pass
class IntegrityError(DatabaseError): pass
class InternalError(DatabaseError): pass
class ProgrammingError(DatabaseError): pass
class NotSupportedError(DatabaseError): pass


class DBAPIErrorWrapper:
    """DBAPIError包装器

    将数据库适配器抛出的异常转换成相应的统一定义的DBAPIError；作为装饰器或上下文管理器使用。

    Attributes:
        errors: 异常名称与DBAPIError类型的对应关系；默认使用STANDARD_DBAPI_ERRORS
        default: 如果没有在errors中找到对应关系，则将异常转换成该属性指定的DBAPIError类型；默认为None，不进行默认转换
    """

    def __init__(self,
                 errors: dict[str, type[DBAPIError]] = None,
                 default: type[DBAPIError] = None):
        if errors is None:
            self.errors = STANDARD_DBAPI_ERRORS
        else:
            self.errors = errors
        self.default = default

    def raise_from(self, exc_type, exc_val, exc_tb):
        if exc_type.__name__ in self.errors:
            new_type = self.errors[exc_type.__name__]
        elif self.default:
            new_type = self.default
        else:
            return
        new_exc = new_type(*exc_val.args)
        if exc_tb:
            raise new_exc.with_traceback(exc_tb) from exc_val
        else:
            raise new_exc from exc_val

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return
        self.raise_from(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                self.raise_from(*sys.exc_info())
                raise
        return _wrapper


STANDARD_DBAPI_ERRORS = {
    'InterfaceError': InterfaceError,
    'DatabaseError': DatabaseError,
    'DataError': DataError,
    'OperationalError': OperationalError,
    'IntegrityError': IntegrityError,
    'InternalError': InternalError,
    'ProgrammingError': ProgrammingError,
    'NotSupportedError': NotSupportedError
}
