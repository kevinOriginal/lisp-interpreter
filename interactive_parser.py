import pickle
import pip

try:
    import pandas
except:
    pip.main(["install", "pandas"])
    import pandas

"""
You can run the program by using such format:

        syntax_analyzer("test_file.out")

"""


class UndefinedDecisionError(Exception):
    pass


class UndefinedGrammarError(Exception):
    pass


with open("./slrTable.pickle", "rb") as f:

    States = pickle.load(f)
    States = States.T


# Stating CFG rules with its ancestor and length
CFG = dict()
CFG[0] = ["S'", 1]
CFG[1] = ["S'", 0]
CFG[2] = ["s", 1]
CFG[3] = ["s", 1]
CFG[4] = ["s", 1]
CFG[5] = ["s", 1]
CFG[6] = ["stmt", 1]
CFG[7] = ["arith", 4]
CFG[8] = ["arith", 5]
CFG[9] = ["stmt", 5]

CFG[10] = ["stmt", 5]
CFG[11] = ["stmt", 6]
CFG[12] = ["stmt", 5]
CFG[13] = ["stmt", 5]
CFG[14] = ["stmt", 5]
CFG[15] = ["stmt", 5]
CFG[16] = ["stmt", 4]
CFG[17] = ["stmt", 1]
CFG[18] = ["pred", 4]
CFG[19] = ["pred", 5]

CFG[20] = ["stmt", 1]
CFG[21] = ["stmt", 1]
CFG[22] = ["if", 5]
CFG[23] = ["if", 6]
CFG[24] = ["cond", 8]
CFG[25] = ["actions", 5]
CFG[26] = ["actions", 0]
CFG[27] = ["type", 1]
CFG[28] = ["type", 1]
CFG[29] = ["type", 1]

CFG[30] = ["type", 1]
CFG[31] = ["type", 1]
CFG[32] = ["type", 1]
CFG[33] = ["compare", 1]
CFG[34] = ["compare", 1]
CFG[35] = ["compare", 1]
CFG[36] = ["compare", 1]
CFG[37] = ["compare", 1]
CFG[38] = ["listop", 1]
CFG[39] = ["listop", 1]


CFG[40] = ["listop", 1]
CFG[41] = ["listop", 1]
CFG[42] = ["listop", 1]
CFG[43] = ["multis", 2]
CFG[44] = ["multis", 0]
CFG[45] = ["subdiv", 1]
CFG[46] = ["subdiv", 1]
CFG[47] = ["addmul", 1]
CFG[48] = ["addmul", 1]


# Collecting all the CFGs into one list, so that it can be reached by its number


while True:
    tokens = []
    words = []
    print(">> ", end="")
    tokens = input().split()
    tokens.append("$")
    stack = [0]
    token_len = len(tokens)
    splitter = -token_len

    while splitter != 0:  # repeats until there is no more input
        next_input = tokens[splitter]  # define next input
        state_num = stack[0]  # define stack number to the first value on the stack
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
                        0, States[stack[0]].get(CFG[replace_num][0])
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