from functools import reduce
from data_types import nil, atom, string
from evaluators import eval_variable, safe_eval
from validators import (
    check_type_list,
    check_number_of_args,
    is_number,
)
from exceptions import (
    BoundError,
    TypeError,
)

identifiers = {}

# Identifier 을 정의하기 위한 decorator
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


# List 를 생성하여 return만 한다.
@identifier("LIST")
def make_list(arg, env):
    evaled_list = list(map(lambda x: eval_variable(x, env), arg))
    return evaled_list


# returns first argument of list
@identifier("CAR")
def car(arr, env):
    check_type_list(arr)
    evaled = eval_variable(arr, env)
    if not evaled:
        raise BoundError("Cannot get first item of empty List")
    return evaled[0]


@identifier("CDR")
def cdr(arg, env):
    evaled = eval_variable(arg, env)
    return evaled[1:]


@identifier("NTH")
def nth(args: list, env):
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
def cons(args: list, env):
    check_number_of_args(args, 2)
    (value, arr) = args
    arr = list(map(lambda x: safe_eval(x), arr))
    value = safe_eval(value)
    check_type_list(arr)
    arr.insert(0, value)
    return arr


@identifier("REVERSE")
def reverse(arr: list, env):
    check_type_list(arr)
    arr = list(map(lambda x: safe_eval(x), arr))
    arr.reverse()
    return arr


@identifier("APPEND")
def append(args: list, env):
    for item in args:
        check_type_list(item)
    return reduce(
        lambda x, y: x + y,
        list(map(lambda arr: list(map(lambda x: safe_eval(x), arr)), args)),
        [],
    )


@identifier("LENGTH")
def length(arr: list, env):
    check_type_list(arr)
    return len(arr)


@identifier("MEMBER")
def member(args: list, env):
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
def assoc(args: list, env):
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
def remove(args: list, env):
    check_number_of_args(args, 2)
    (key, lookup) = args
    target = eval_variable(key, env)
    arr = eval_variable(lookup, env)
    check_type_list(arr)
    return list(filter(lambda x: x != target, arr))


@identifier("SUBST")
def subst(args: list, env):
    check_number_of_args(args, 3)
    (replace_to, replace_from, lookup) = args
    replace_to = eval_variable(replace_to, env)
    replace_from = eval_variable(replace_from, env)
    arr = eval_variable(lookup, env)
    return list(map(lambda x: x if x != replace_from else replace_to, arr))


@identifier("PRINT")
def print_i(arg, env):
    return eval_variable(arg, env)