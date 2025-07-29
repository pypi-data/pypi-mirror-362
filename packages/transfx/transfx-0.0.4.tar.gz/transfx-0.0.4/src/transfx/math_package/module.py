"""transFX_math_package

This module provides basic mathematical operations with proper error handling.
"""

from typing import Union

Number = Union[int, float]


def sum(*args: Number) -> Number:
    """
    计算所有参数的和

    Examples:
        >>> sum(1, 2, 3)
        6
    """
    if not args:
        return 0

    result = 0
    for arg in args:
        if not isinstance(arg, (int, float)):
            raise TypeError(f"所有参数必须是数字类型，但收到了 {type(arg).__name__}: {arg}")
        result += arg
    return result


def add(*args: Number) -> Number:
    """
    计算所有参数的和

    Examples:
        >>> add(1, 2, 3)
        6
    """
    return sum(*args)


def sub(*args: Number) -> Number:
    """
    从第一个参数中依次减去后面的所有参数

    Examples:
        >>> sub(10, 3, 2)
        5
    """
    if not args:
        raise ValueError("至少需要提供一个参数")

    if not isinstance(args[0], (int, float)):
        raise TypeError(f"所有参数必须是数字类型，但收到了 {type(args[0]).__name__}: {args[0]}")

    result = args[0]
    for i in range(1, len(args)):
        arg = args[i]
        if not isinstance(arg, (int, float)):
            raise TypeError(f"所有参数必须是数字类型，但收到了 {type(arg).__name__}: {arg}")
        result -= arg

    return result


def mul(*args: Number) -> Number:
    """
    计算所有参数的乘积

    Examples:
        >>> mul(2, 3, 4)
        24
    """
    if not args:
        return 1

    result = 1
    for arg in args:
        if not isinstance(arg, (int, float)):
            raise TypeError(f"所有参数必须是数字类型，但收到了 {type(arg).__name__}: {arg}")
        if arg == 0:
            return 0
        result *= arg
    return result


def div(*args: Number) -> float:
    """
    从第一个参数开始，依次除以后面的所有参数

    Examples:
        >>> div(24, 2, 3)
        4.0
    """
    if not args:
        raise ValueError("至少需要提供一个参数")

    if not isinstance(args[0], (int, float)):
        raise TypeError(f"所有参数必须是数字类型，但收到了 {type(args[0]).__name__}: {args[0]}")

    result = float(args[0])
    for i in range(1, len(args)):
        arg = args[i]
        if not isinstance(arg, (int, float)):
            raise TypeError(f"所有参数必须是数字类型，但收到了 {type(arg).__name__}: {arg}")
        if arg == 0:
            raise ValueError("除数不能为零")
        result /= arg

    return result
