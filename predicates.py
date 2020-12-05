import sys
from typing import List
from data_types import nil, atom
from parser import parse
from lex import tokenize
from exceptions import (
    ArgumentsError,
    DuplicateError,
    UndefinedError,
    TypeError,
    BoundError,
)

# TODO: Implement operations
operations = {}


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
    return value == 0


@predicate("MINUSP")
def minus_p(value):
    return value < 0


# TODO: Need to know which kind of data types for equal and arithmatic comparasons
@predicate("EQUAL")
def equal(x, y):
    if type(x) is not type(y):
        return False
    return x == y


@predicate("<")
def less_than(x, y):
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x < y


@predicate(">=")
def greater_or_equal_to(x, y):
    if type(x) is not type(y):
        raise TypeError("Argument Type", x, " and ", y, " do not match")
    return x >= y


# TODO: need to handle dobule quotes
@predicate("STRINGP")
def string_p(value):
    return isinstance(value, str)


# TODO: Move identifiers to another file
# identifiers

identifiers = {}


def identifier(name):
    """An annotation to convert a Python function into a PrimitiveProcedure."""

    def add_identifier(func):
        identifiers[name] = func
        return func

    return add_identifier


# args[0]는 variable name, args[1]는 variable
@identifier("SETQ")
def set_q(args, env):
    check_number_of_args(args, 2)
    evaluated = eval_variable(args[1], env)
    env[args[0]] = args[1]
    print("[Debug] Set var {0} = {1}".format(args[0], env[args[0]]))


# just returns the list
@identifier("LIST")
def make_list(arg):
    if not check_primitive(arg):
        raise TypeError("Types inside a list should be XXXXXXXXXXXXXX")
    return arg


# returns first argument of list
@identifier("CAR")
def car(arr):
    check_type_list(arr)
    if not arr:
        raise BoundError("Cannot get first item of empty List")
    return arr[0]


@identifier("CDR")
def cdr(arr):
    check_type_list(arr)
    return arr[1:]


# TODO: Implement CXXXR


@identifier("NTH")
def nth(args: List):
    check_number_of_args(args, 2)
    (index, arr) = args
    check_type_list(arr)
    if not isinstance(index, int):
        raise TypeError(
            "1st Argument shoud be type int, insted received: {0}".format(type(index))
        )
    if len(arr) < index:
        return nil
    return arr[index]


@identifier("CONS")
def cons(args: List):
    check_number_of_args(args, 2)
    (arr, value) = args
    check_type_list(arr)
    return arr.append(value)


# TODO: single arguments should be flattend before comming in?
@identifier("REVERSE")
def reverse(arr: List):
    check_type_list(arr)
    return arr.reversed()


@identifier("APPEND")
def append(arr1, arr2):
    if not isinstance(arr1, list) or not isinstance(arr2, list):
        raise TypeError("Both arguments should be Type List, instead received")
    return arr1.extend(arr2)


@identifier("LENGTH")
def length(arr: List):
    check_type_list(arr)
    return len(arr)


# @identifier("MEMBER")
# def member()


# Validators
# TODO: Implement primitive checker and maybe change name
def check_primitive(args):
    return True


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


def eval_variable(value, env):
    print("Eval variable", value)
    if isinstance(value, list):
        return eval_brackets(value, env)
    if value in env:
        return env[value]
    if value.startswith('"') and value.endswith('"'):
        print("It's a string!")
        return value
    if value.startswith("'") and value.endswith("'"):
        print("It's a symbol(atom)")
        print("atom - ", atom(value))
        return atom(value)
    if isinstance(value, int) or isinstance(value, float):
        print("It's a number!")
        return value
    # raise UndefinedError("Variable {0} is undefined".format(value))
    return value


def eval_brackets(arg: List, env):
    (first, *rest) = arg
    if first in predicates:
        print(
            "Fist arguement <{0}> is a predicate <{1}>".format(
                first, predicate[first].__name__
            )
        )
        args = list(map(lambda x: eval_variable(x, env), rest))
        if len(args) == 1:
            args = args[0]
        result = predicates[first](args)
        return result
    if first in identifiers:
        print(
            "Fist arguement <{0}> is a identifier <{1}>".format(
                first, identifiers[first].__name__
            )
        )
        args = list(map(lambda x: eval_variable(x, env), rest))
        if len(args) == 1:
            args = args[0]
        result = identifiers[first](args)
        return result
    if first in operations:
        # do sth
        return

    # If first keyword is not reserved, than it's a plain list
    return arg


def main():
    environment = {}
    while True:
        try:
            tokens = []
            words = []
            print(">> ", end="")
            tokens = input()
            if tokens == "exit":
                sys.exit()
            tokenized = tokenize(tokens)
            parsed = parse(tokenized)
            print("parsed - {0}".format(parsed))
            print("--------Evaluate start ----------")
            print(eval_variable(parsed, environment))
        except UndefinedError as err:
            print(err)


if __name__ == "__main__":
    main()
