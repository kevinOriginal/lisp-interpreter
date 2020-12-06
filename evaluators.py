import sys, os
import traceback
from typing import List
from data_types import nil, atom, string
from predicates import predicates
from operations import operations
from exceptions import (
    UndefinedError,
)
from parser import parse
from lex import tokenize


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


def eval_brackets(arg: list, env):
    # Circular dependency 때문에 밑에서 import를 함
    from identifiers import identifiers
    from conditionals import conditionals

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

    # 만약에 bracket의 첫번 째 keyword가 reserved된 예약어가 아니라면 이것은 list이므로 이를 parsing해야 한다.
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
