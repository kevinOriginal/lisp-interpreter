from data_types import nil
from validators import (
    check_number_of_args,
)
from evaluators import eval_variable

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