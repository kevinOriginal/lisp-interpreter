import sys, os
import traceback
from typing import List
from data_types import nil, atom, string
from parser import parse
from lex import tokenize
from exceptions import (
    ArgumentsError,
    DuplicateError,
    UndefinedError,
    TypeError,
    BoundError,
)
from functools import reduce

# TODO: Implement operations
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


# 추가 구현
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


# TODO: Need to know which kind of data types for equal and arithmatic comparasons
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


# TODO: need to handle dobule quotes
@predicate("STRINGP")
def string_p(value):
    return isinstance(value, string)


# TODO: Move identifiers to another file
# identifiers

identifiers = {}


def identifier(name):
    def add_identifier(func):
        identifiers[name] = func
        return func

    return add_identifier


# args[0]는 variable name, args[1]는 variable
@identifier("SETQ")
def set_q(args, env):
    check_number_of_args(args, 2)
    (variable, insert) = args
    evaluated = eval_variable(insert, env)
    env[variable] = evaluated
    return env[variable]


# just returns the list
@identifier("LIST")
def make_list(arg, env):
    evaled_list = list(map(lambda x: eval_variable(x, env), arg))
    if not check_primitive(arg):
        raise TypeError("Types inside a list should be XXXXXXXXXXXXXX")
    return evaled_list


# returns first argument of list
@identifier("CAR")
def car(arr, env):
    check_type_list(arr)
    # arr = list(map(lambda x: eval_variable(x, env), arr))
    evaled = eval_variable(arr, env)
    if not evaled:
        raise BoundError("Cannot get first item of empty List")
    return evaled[0]


@identifier("CDR")
def cdr(arg, env):
    print("CDR REceived", arg)
    # check_type_list(arr)
    evaled = eval_variable(arg, env)
    # arr = list(map(lambda x: eval_variable(x, env), arr))
    return evaled[1:]


# TODO: Implement CXXXR


@identifier("NTH")
def nth(args: List, env):
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
def cons(args: List, env):
    check_number_of_args(args, 2)
    (value, arr) = args
    arr = list(map(lambda x: safe_eval(x), arr))
    value = safe_eval(value)
    check_type_list(arr)
    arr.insert(0, value)
    return arr


@identifier("REVERSE")
def reverse(arr: List, env):
    check_type_list(arr)
    arr = list(map(lambda x: safe_eval(x), arr))
    arr.reverse()
    return arr


@identifier("APPEND")
def append(args: List, env):
    for item in args:
        check_type_list(item)
    return reduce(
        lambda x, y: x + y,
        list(map(lambda arr: list(map(lambda x: safe_eval(x), arr)), args)),
        [],
    )


@identifier("LENGTH")
def length(arr: List, env):
    check_type_list(arr)
    return len(arr)


@identifier("MEMBER")
def member(args: List, env):
    check_number_of_args(args, 2)
    (key, lookup) = args
    target = eval_variable(key, env)
    arr = eval_variable(lookup, env)
    check_type_list(arr)
    try:
        # list.index 에 들어가면 str 형태로 비교가 되기 떄문에 str type으로 변환 후 비교를 한다.
        index = arr.index(str(target))
        return arr[index:]
    except:
        return nil


@identifier("ASSOC")
def assoc(args: List, env):
    check_number_of_args(args, 2)
    (key, lookup) = args
    target = eval_variable(key, env)
    arr = eval_variable(lookup, env)
    check_type_list(arr)
    result = list(filter(lambda x: x[0] == target, arr))
    if not result:
        return nil
    if len(result) == 1:
        result = result[0]
    # 같은 키가 여러 개 있을 경우 List에 담아 return을 한다.
    return result


@identifier("REMOVE")
def remove(args: List, env):
    check_number_of_args(args, 2)
    (key, lookup) = args
    target = eval_variable(key, env)
    arr = eval_variable(lookup, env)
    check_type_list(arr)
    return list(filter(lambda x: x != target, arr))


@identifier("SUBST")
def subst(args: List, env):
    check_number_of_args(args, 3)
    (replace_to, replace_from, lookup) = args
    replace_to = eval_variable(replace_to, env)
    replace_from = eval_variable(replace_from, env)
    arr = eval_variable(lookup, env)
    return list(map(lambda x: x if x != replace_from else replace_to, arr))


# Conditionals

conditionals = {}


def conditional(name):
    def add_conditional(func):
        conditionals[name] = func
        return func

    return add_conditional


@conditional("IF")
def if_stmt(args, env):
    if len(args) == 2:
        (condition, on_true) = args
    if len(args) == 3:
        (condition, on_true, on_false) = args
    condition = eval_variable(condition, env)
    if condition:
        return eval_variable(on_true, env)
    else:
        return eval_variable(args[2], env) if len(args) == 3 else nil


@conditional("COND")
def cond_stmt(args, env):
    for stmt in args:
        check_number_of_args(stmt, 2)
        (condition, on_true) = stmt
        if eval_variable(condition, env):
            return eval_variable(on_true, env)


# Validators
# TODO: Implement primitive checker and maybe change name
def check_primitive(args):
    return True


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


def eval_primitive(value):
    if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
        print("It's a string - ", string(value))
        return (string(value), True)
    if isinstance(value, str) and value.startswith("'") and value.endswith("'"):
        print("It's a atom - ", atom(value))
        return (atom(value), True)
    if isinstance(value, int) or isinstance(value, float):
        print("It's a number!")
        return (value, True)
    if isinstance(value, str) and (value == "NIL"):
        print("It's nil!")
        return (nil, True)
    print("[IDK - Not primitive]")
    return (value, False)


def safe_eval(value):
    if isinstance(value, list):
        print("It's a list")
        return list(map(lambda x: safe_eval(x), value))
    (evaled, is_primitive) = eval_primitive(value)
    if is_primitive:
        return evaled
    print("[Assuming Inside List] converting into atom - ", value)
    return atom(value)


def eval_variable(value, env):
    print("Eval variable", value)
    if isinstance(value, list):
        return eval_brackets(value, env)
    if value in env:
        return env[value]
    (evaled, is_primitive) = eval_primitive(value)
    if is_primitive:
        return evaled
    raise UndefinedError("Variable {0} is undefined".format(value))


#  WARNING!! : Some variables must be lazy evaluated!
def eval_brackets(arg: List, env):
    print("Eval brackets", arg)
    (first, *rest) = arg
    if isinstance(first, str) and first in predicates:
        print("First arguement <{0}> is a [predicate]".format(first))

        # Predicate은 모두 eval된 값을 연산 하기 때문에 미리 eval 해줘도 괜찮다.
        rest = list(map(lambda x: eval_variable(x, env), rest))
        if len(rest) == 1:
            rest = rest[0]
        result = predicates[first](rest)
        return result
    if isinstance(first, str) and first in identifiers:
        print(
            "Fist arguement <{0}> is a [identifier] <{1}>".format(
                first, identifiers[first].__name__
            )
        )
        if len(rest) == 1:
            rest = rest[0]
        result = identifiers[first](rest, env)
        return result
    if isinstance(first, str) and first in operations:
        print("First arguement <{0}> is a [operator]".format(first))
        # Operation 역시 모두 eval 된 값만 연산 하면 되기 때문에 미리 한다.
        rest = list(map(lambda x: eval_variable(x, env), rest))
        result = operations[first](rest)
        return result
    if isinstance(first, str) and first in conditionals:
        print("First arguement <{0}> is a [conditional]".format(first))
        # TODO: implement lazy evaluation
        result = conditionals[first](rest, env)
        return result

    # If first keyword is not reserved, than it's a plain list so we should convert it to atoms
    return list(map(lambda x: safe_eval(x), arg))


def main():
    environment = {}
    while True:
        try:
            tokens = []
            words = []
            print(">> ", end="")
            tokens = input()
            # while True:
            #     if keyboard.is_pressed("enter"):
            #         break
            #     try:
            #         line = input()
            #     except EOFError:
            #         break
            #     tokens.append(line)
            #  print("contents", tokens)
            if tokens == "exit":
                sys.exit()
            tokenized = tokenize(tokens)
            parsed = parse(tokenized)
            print("parsed - {0}".format(parsed))
            print("--------Evaluate start ----------")
            print(eval_variable(parsed, environment))
        except Exception as e:
            print(traceback.format_exc())
            print(e)


if __name__ == "__main__":
    main()
