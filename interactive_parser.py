import pickle
import pip
from lex import tokenize
from parser import parse

try:
    import pandas
except:
    pip.main(["install", "pandas"])
    import pandas


def main():
    while True:
        tokens = []
        words = []
        print(">> ", end="")
        tokens = input()
        tokenized = tokenize(tokens)
        parsed = parse(tokenized)
        print(parsed)


if __name__ == "__main__":
    main()
