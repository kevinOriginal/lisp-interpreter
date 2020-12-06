# Validators
from exceptions import (
    ArgumentsError,
    TypeError,
)

# 각종 type validation, argument 개수 validation 등이 있다.
# True/false로 리턴하는 경와와 Error을 raise하는 경우 두 가지가 있다.


def check_type_number(arg):
    if not isinstance(arg, int) and not isinstance(arg, float):
        raise TypeError(
            "Argument should be Type Number, instead received: {0}".format(type(arg))
        )


def check_type_list(arg):
    if not isinstance(arg, list):
        raise TypeError(
            "Argument should be Type List, instead received: {0}".format(type(arg))
        )


def check_number_of_args(arg_arr: list, target: int):
    if not len(arg_arr) == target:
        raise ArgumentsError(
            "Number of arguments should be {0}, instead received {1}".format(
                target, len(arg_arr)
            )
        )


def is_number(x):
    return isinstance(x, int) or isinstance(x, float)
