"""
interval.utils
~~~~~~~~~~~~~~

This module provides utility functions and classes.
"""

import random
import re
import string
import sys
from collections.abc import Collection, Iterable, Iterator
from contextvars import ContextVar
from datetime import datetime, UTC
from decimal import Decimal
from itertools import islice
from logging import Filter, Formatter, getLogger, Logger, LogRecord, StreamHandler
from typing import Any, Callable, TextIO

import orjson

if sys.version_info >= (3, 12):
    from itertools import batched  # noqa
else:
    def batched(iterable: Iterable[Any], n: int) -> Iterator[tuple]:
        """Python 3.12标准库itertools.batched函数的等价实现

        参考文档：https://docs.python.org/3.12/library/itertools.html#itertools.batched
        """
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch


def safe_issubclass(class_or_object, classinfo) -> bool:
    """调用内置函数issubclass，当参数类型错误时返回False，而非抛出异常"""
    try:
        return issubclass(class_or_object, classinfo)
    except TypeError:
        return False


def get_datetime_with_local_tz(datetime_obj: datetime = None,
                               timestamp: float = None) -> datetime:
    """获取带有本地时区的datetime对象

    处理逻辑如下：
    1、如果传入了已有的datetime对象，若是naive对象，则添加本地时区信息，若是aware对象，则将其转换为本地时区；
    2、如果传入了已有的时间戳，则将其转换为datetime对象；
    3、如果二者均默认不传，则获取当前系统时间。

    Args:
        datetime_obj: datetime对象
        timestamp: 时间戳

    Returns:
        datetime对象
    """
    if datetime_obj is not None:
        dt = datetime_obj
    elif timestamp is not None:
        dt = datetime.fromtimestamp(timestamp)
    else:
        dt = datetime.now()
    return dt.astimezone()


def get_datetime_with_utc_tz(datetime_obj: datetime = None,
                             timestamp: float = None) -> datetime:
    """获取带有UTC时区的datetime对象

    处理逻辑如下：
    1、如果传入了已有的datetime对象，若是naive对象，则添加UTC时区信息，若是aware对象，则将其转换为UTC时区；
    2、如果传入了已有的时间戳，则将其转换为datetime对象；
    3、如果二者均默认不传，则获取当前系统时间。

    Args:
        datetime_obj: datetime对象
        timestamp: 时间戳

    Returns:
        datetime对象
    """
    if datetime_obj is not None:
        if datetime_obj.tzinfo:
            return datetime_obj.astimezone(tz=UTC)
        else:
            return datetime_obj.replace(tzinfo=UTC)
    elif timestamp is not None:
        return datetime.fromtimestamp(timestamp, tz=UTC)
    else:
        return datetime.now(tz=UTC)


def _orjson_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if callable(getattr(obj, 'to_dict', None)):
        return obj.to_dict()
    try:
        return list(obj)
    except Exception:
        raise TypeError


def orjson_dumps(obj: Any) -> bytes:
    """使用orjson进行JSON序列化操作

    除了orjson默认支持的数据类型，还支持以下类型的对象：
    1、Decimal对象，转化为字符串；
    2、带有to_dict()方法的对象，转化为字典；
    3、可迭代对象，转化为列表。

    Args:
        obj: Python对象

    Returns:
        JSON字节流

    Raises:
        orjson.JSONEncodeError: TypeError的子类
    """
    return orjson.dumps(
        obj,
        default=_orjson_default,
        option=orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_SERIALIZE_NUMPY
    )


def orjson_loads(obj: bytes | bytearray | memoryview | str) -> Any:
    """使用orjson进行JSON反序列化操作

    Args:
        obj: JSON字节流或字符串

    Returns:
        Python对象

    Raises:
        orjson.JSONDecodeError: ValueError的子类
    """
    return orjson.loads(obj)


def get_stream_logger(name: str, level: int | str,
                      stream: TextIO = None,
                      filters: Collection[Filter | Callable[[LogRecord], Any]] = None,
                      formatter: Formatter = None,
                      exclusive: bool = False) -> Logger:
    """获取日志记录器（StreamHandler作为处理器）

    Args:
        name: 日志名称
        level: 日志级别
        stream: 处理器的输出流，默认为sys.stderr
        filters: 处理器的过滤器列表
        formatter: 处理器的格式器
        exclusive: 是否移除该日志记录器原有的全部处理器

    Returns:
        日志记录器
    """
    logger = getLogger(name)
    logger.setLevel(level)
    if exclusive and logger.handlers:
        logger.handlers.clear()
    handler = StreamHandler(stream)
    if filters:
        for f in filters:
            handler.addFilter(f)
    if formatter:
        handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def generate_nonce(length: int, chars: str = 'uld', population: str = '',
                   *, prefix: str = '', suffix: str = '') -> str:
    """生成固定长度的随机字符串

    Args:
        length: 字符串总长度
        chars: 使用的字符种类，可组合使用：'u' - 大写字母，'l' - 小写字母，'d' - 数字
        population: 使用的字符集合；若指定了population则忽略chars
        prefix: 字符串前缀
        suffix: 字符串后缀

    Returns:
        随机字符串

    Raises:
        ValueError: 前缀和后缀的长度之和大于总长度；没有指定有效的字符种类或者字符集合
    """
    random_part_len = length - len(prefix + suffix)
    if random_part_len < 0:
        raise ValueError('Invalid length')
    if random_part_len == 0:
        return prefix + suffix
    if not population:
        if 'u' in chars:
            population += string.ascii_uppercase
        if 'l' in chars:
            population += string.ascii_lowercase
        if 'd' in chars:
            population += string.digits
        if not population:
            raise ValueError('Invalid chars')
    elements = random.choices(population, k=random_part_len)
    return prefix + ''.join(elements) + suffix


def check_mobile_number(number: str) -> bool:
    """检查手机号码格式是否正确

    Args:
        number: 手机号码

    Returns:
        格式正确返回True，否则返回False
    """
    pattern = r'1[3-9]\d{9}'
    match_obj = re.fullmatch(pattern, number)
    return bool(match_obj)


def check_id_card_number(number: str) -> bool:
    """检查身份证号码格式是否正确

    Args:
        number: 身份证号码

    Returns:
        格式正确返回True，否则返回False
    """
    if len(number) == 18:
        pattern = r'[1-9]\d{5}[12]\d{3}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dxX]'
        match_obj = re.fullmatch(pattern, number)
        return bool(match_obj)
    if len(number) == 15:
        pattern = r'[1-9]\d{7}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}'
        match_obj = re.fullmatch(pattern, number)
        return bool(match_obj)
    return False


class ContextGlobals:
    """上下文全局变量类

    全局变量实例支持任意属性的读写，属性使用ContextVar实现，默认值为None。
    """
    __slots__ = ('_vars',)

    _vars: dict[str, ContextVar]

    def __init__(self):
        super().__setattr__('_vars', {})

    def reset(self):
        for var in self._vars.values():
            var.set(None)

    def _ensure_var(self, name: str):
        if name not in self._vars:
            self._vars[name] = ContextVar(f'globals:{name}', default=None)

    def __getattr__(self, name: str) -> Any:
        self._ensure_var(name)
        return self._vars[name].get()

    def __setattr__(self, name: str, value: Any):
        self._ensure_var(name)
        self._vars[name].set(value)
