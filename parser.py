import pickle
import pip
import pandas
from lex import tokenize
import re

"""
You can run the program by using such format:

        syntax_analyzer("test_file.out")

"""


class UndefinedDecisionError(Exception):
    pass


class UndefinedGrammarError(Exception):
    pass


# Stating CFG rules with its ancestor and length
with open("./cfg.pickle", "rb") as f:
    CFG = pickle.load(f)


# Collecting all the CFGs into one list, so that it can be reached by its number
with open("./slr_table11.pickle", "rb") as f:

    States = pickle.load(f)


def tokens_to_ast(values: list):
    token = values.pop(0)
    if token == "'":
        peek = values[0]
        l = tokens_to_ast(values)  # [ 1, 2, 3] 이 리턴된다
        if peek[0] == "(":
            return l
        else:
            return "'" + l + "'"

    if token == "#":
        peek = values[0]
        l = tokens_to_ast(values)  # [ 1, 2, 3] 이 리턴된다
        if peek[0] == "(":
            l.insert(0, "#")
            return l
        else:
            return '"' + l + '"'

    if token == "(":
        L = []
        while values[0] != ")":
            L.append(tokens_to_ast(values))
        values.pop(0)  # pop off ')'
        try:
            CADR = re.match("^C[AD]+R$", L[0])
        except:
            CADR = False
        if CADR:
            L = CADRtransform(L)
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        try:
            return int(token)
        except:
            try:
                return float(token)
            except:
                return token


def CADRtransform(cadr_l: list):
    cadr = cadr_l[0]
    result = []
    if cadr == "CAR" or cadr == "CDR":
        return cadr_l

    if cadr[1] == "A":
        return ["CAR", CADRtransform(["C" + cadr[2:], cadr_l[1]])]
    elif cadr[1] == "D":
        return ["CDR", CADRtransform(["C" + cadr[2:], cadr_l[1]])]


def parse(in_put: list) -> bool:
    if in_put == []:
        print("accepted")
        return ""
    tokens = list()
    values = list()
    for d in in_put:
        for k, v in d.items():
            tokens.append(k)
            values.append(v)
    tokens.append("$")
    stack = [0]
    token_len = len(tokens)
    splitter = -token_len

    while splitter != 0:  # repeats until there is no more input
        next_input = tokens[splitter]  # define next input
        state_num = stack[0]  # define stack number to the first value on the stack
        stack[::-1]
        tokens[splitter:]
        try:
            decision = States[state_num][
                next_input
            ]  # find decision from the SLR parsing table

        except:
            print("Token not defined")
            break
        if type(decision) == str:
            if decision[0] == "s":  # if the decision is to shift
                shift_num = int(decision[1:])
                stack.insert(0, shift_num)  # insert the next state into the stack
                splitter += 1  # move the splitter to the right
            elif decision[0] == "r":  # if the decision is to reduce
                replace_num = int(decision[1:])
                stack = stack[CFG[replace_num][1] :]  # pop contents from the stack
                tokens = (
                    tokens[: splitter - CFG[replace_num][1]]
                    + [CFG[replace_num][0]]
                    + tokens[splitter:]
                )  # reduce tokens according to the CFG G

                stack.insert(
                    0, int(States[stack[0]].get(CFG[replace_num][0]))
                )  # push GOTO into the stack
            elif decision == "acc":
                print("accepted")
                return tokens_to_ast(values)

            else:
                raise UndefinedDecisionError(
                    "There is an invalid value at the SLR Parsing Table : ",
                    decision,
                    " at state",
                    stack[0],
                    " & ",
                    next_input,
                )  # this is for checking errors in SLR table

        elif type(decision) == int:  # if the decision is GOTO
            stack.insert(0, decision)  # push GOTO into the stack
        elif (
            type(decision) == float
        ):  # if decision is undefined raise UndefinedGrammarError
            print("Not accepted")
            break


if __name__ == "__main__":
    f = open("testcase.in")
    lines = f.readlines()
    for string in lines:
        tokenized = tokenize(string)
        print(string)
        print(parse(tokenized))
