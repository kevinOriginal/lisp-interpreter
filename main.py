import sys
import traceback
from parser import parse
from lex import tokenize
from validators import is_number
from evaluators import eval_variable
from data_types import nil, atom, string

#  나온 결과값을 예쁘게 변환 (대소문자 -> 대문자로 변환)
#  리스트의 bracket 및 , 제거
def prettifyOutput(arg):
    print("Type is {0}".format(type(arg)))
    if isinstance(arg, string) or isinstance(arg, atom):
        return str(arg).capitalize()
    if is_number(arg):
        return str(arg)
    if isinstance(arg, list):
        result = list(map(lambda x: prettifyOutput(x), arg))
        return "(" + " ".join(result) + ")"
    return arg


def interpret(arg, env):
    tokenized = tokenize(arg)
    parsed = parse(tokenized)
    result = eval_variable(parsed, env)
    return prettifyOutput(result)


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
            print("--------Evaluate start----------")
            result = eval_variable(parsed, environment)
            print("--------Eval Complete-----------")
            prettified = prettifyOutput(result)
            print(prettified)
        except Exception as e:
            print(traceback.format_exc())
            print(e)


if __name__ == "__main__":
    main()