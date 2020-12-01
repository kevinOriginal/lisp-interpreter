import pickle
import pip
import pandas

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
with open("./slr_table3.pickle", "rb") as f:

    States = pickle.load(f)


def parse(in_put: list) -> bool:
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
        print(stack[::-1], tokens[splitter:])
        try:
            decision = States[state_num][
                next_input
            ]  # find decision from the SLR parsing table
        except:
            # print(state_num, next_input)
            print("Token not defined")
            break
        if type(decision) == str:
            if decision[0] == "s":  # if the decision is to shift
                shift_num = int(decision[1:])
                stack.insert(0, shift_num)  # insert the next state into the stack
                splitter += 1  # move the splitter to the right
            elif decision[0] == "r":  # if the decision is to reduce
                if (
                    decision == "r0"
                ):  # if the decision is to reduce to the dummy start symbol X'
                    print("Accepted")  # print Acceptance message
                    # return True  # return True
                else:
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
                break
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
    parse([{"(": "("}, {"CADR": "cadddr"}, {"id": "x"}, {")": ")"}])