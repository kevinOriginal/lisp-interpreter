from data_types import string
from validators import (
    check_number_of_args,
    is_number,
)

# 기본적으로 operation은 pure하기 때문에 따로 lazy eval해야할 부분은 없다.

# 사칙연산을 위한 기본 operator들을 operators 변수 안에 담에 나중에 evaluation 할때 operation 연산이 있으면 참조를 하여 연산을 한다.
operations = {}


def operation(name):
    def add_operation(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        operations[name] = wrapper

    return add_operation


@operation("+")
def add(args):
    if len(args) == 0:
        return 0
    (x, y) = args
    if is_number(x) and is_number(y):
        return x + y
    if isinstance(x, string) and isinstance(y, string):
        return x + y
    raise TypeError("Cannot apply addition on types {0}, {1}".format(type(x), type(y)))


@operation("-")
def subtract(args):
    if len(args) == 1:
        return 0
    (x, y) = args
    if is_number(x) and is_number(y):
        return x - y
    raise TypeError(
        "Cannot apply subtraction on two different types {0}, {1}".format(
            type(x), type(y)
        )
    )


@operation("*")
def multiply(args):
    if len(args) == 0:
        return 1
    check_number_of_args(args, 2)
    (x, y) = args
    if is_number(x) and is_number(y):
        return x * y
    raise TypeError(
        "Cannot apply multiplication on two different types {0}, {1}".format(
            type(x), type(y)
        )
    )


@operation("/")
def divide(args):
    if len(args) == 1:
        return 1
    check_number_of_args(args, 2)
    (x, y) = args
    if is_number(x) and is_number(y):
        return x * y
    raise TypeError(
        "Cannot apply division on two different types ({0}), ({1})".format(
            type(x), type(y)
        )
    )


# MOD 연산을 하는 것을 추가로 구현 하였다.
@operation("%")
def mod(args):
    if len(args) == 1:
        return 1
    check_number_of_args(args, 2)
    (x, y) = args
    if is_number(x) and is_number(y):
        return x % y
    raise TypeError(
        "Cannot apply modulo on two different types ({0}), ({1})".format(
            type(x), type(y)
        )
    )