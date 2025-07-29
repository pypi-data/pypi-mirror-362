"""transFX_math_package"""

def transFX_sum(*args):
    """sum函数"""
    result = 0
    for i in args:
        result += i
    return result

def transFX_add(*args):
    """add函数"""
    result = 0
    for i in args:
        result += i
    return result

def transFX_sub(*args):
    """sub函数"""
    result = 0
    for i in args:
        result -= i
    return result

def transFX_mul(*args):
    """mul函数"""
    result = 1
    for i in args:
        result *= i
    return result

def transFX_div(*args):
    """div函数"""
    result = 1
    for i in args:
        result /= i
    return result