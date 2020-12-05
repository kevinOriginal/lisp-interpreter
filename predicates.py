from data_types import null, atom
from parser import parse
from lex import tokenize
from exceptions import ArgumentsError, DuplicateError, UndefinedError, TypeError

predicates = {}

# decorator for primitves
def predicate(name):
    def add_to_predicate(func):
        def wrapper(*args, **kwargs):
            return "T" if func(*args, **kwargs) else "NIL"

        predicates[name] = wrapper

    return add_to_predicate


@predicate("ATOM")
def atom_p(value):
    return isinstance(value, atom)


@predicate("NULL")
def null_p(value):
    return value is null


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


# TODO: Move primitives to another file
# Primitives

primitives = {}


def primitive(name):
    """An annotation to convert a Python function into a PrimitiveProcedure."""

    def primitive_add(func):
        primitives[name] = func
        return func

    return primitive_add


# args[0]는 variable name, args[1]는 variable
@primitive("SETQ")
def set_q(args, env):
    if len(args) != 2:
        raise ArgumentsError("Number of arguments do not match for setting variable")
    evaluated = eval_variable(args[1], env)
    env[args[0]] = args[1]


# just make a list and return the list
@primitive("LIST")
def make_list(args, env):
    if not check_primitive(args):
        raise TypeError("Types inside a list should be XXXXXXXXXXXXXX")
    return


# TODO: Implement and maybe change name
def check_primitive(args):
    return True


def eval_variable(value, env):
    if value in env:
        return env[value]
    if value.startswith('"') and value.endswith('"'):
        print("It's a string!")
        return value
    if value.startswith("'") and value.endswith("'"):
        print("It's a symbol")
        return value
    if isinstance(value, int) or isinstance(value, float):
        print("It's a number!")
        return value
    raise UndefinedError("Variable ", value, " is undefined")


def main():
    # string = "(ATOM  X)"
    environment = {}
    string = '(STRINGP "A")'
    tokenized = tokenize(string)
    parsed = parse(tokenized)
    command = parsed[0]
    print("command " + command)
    if predicates[command]:
        result = predicates[command](parsed[1])
        print("result - ", result)
    print(parsed)


if __name__ == "__main__":
    main()
