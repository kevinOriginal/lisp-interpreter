import sys
import traceback
from parser import parse
from lex import tokenize
from evaluators import eval_variable


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