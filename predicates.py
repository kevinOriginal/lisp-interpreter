from data_types import nil, atom, string
from validators import (
    check_number_of_args,
    check_type_number,
)

predicates = {}

# decorator for primitves
def predicate(name):
    def add_to_predicate(func):
        def wrapper(*args, **kwargs):
            return "T" if func(*args, **kwargs) else nil

        predicates[name] = wrapper

    return add_to_predicate


@predicate("ATOM")
def atom_p(value):
    return isinstance(value, atom)


@predicate("NULL")
def null_p(value):
    return value is nil


@predicate("NUMBERP")
def number_p(value):
    return isinstance(value, int) or isinstance(value, float)


@predicate("ZEROP")
def zero_p(value):
    check_type_number(value)
    return value == 0


@predicate("MINUSP")
def minus_p(value):
    check_type_number(value)
    return value < 0


# Equal Comparason 같은 경우는 atom, string, symbol, nil, number, evaled variable 등이 된다.
@predicate("EQUAL")
def equal(args):
    check_number_of_args(args, 2)
    (x, y) = args
    if type(x) is not type(y):
        return False
    return x == y


@predicate("<")
def less_than(args):
    check_number_of_args(args, 2)
    (x, y) = args
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x < y


# 추가 구현
@predicate(">")
def less_than(args):
    check_number_of_args(args, 2)
    (x, y) = args
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x > y


# 추가 구현
@predicate("<=")
def less_than(args):
    check_number_of_args(args, 2)
    (x, y) = args
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x <= y


@predicate(">=")
def greater_or_equal_to(args):
    check_number_of_args(args, 2)
    (x, y) = args
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x >= y


@predicate("STRINGP")
def string_p(value):
    return isinstance(value, string)
