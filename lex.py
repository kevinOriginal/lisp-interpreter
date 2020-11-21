program = "(begin (define 'r 10) (* pi (* r r)));;;; this is comment"


def tokenize(chars: str):
    comment = {'comment': chars.split(';', 1)[1]}
    tokens = chars.split(';')[0].replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ").split()
    tokenized = []
    for token in tokens:
        if token == '(':
            token = {'Lparen': token}
        elif token == ')':
            token = {'Rparen': token}
        elif token == "'":
            token = {'quote': token}
        # elif token in ['begin', 'define', ]:  # 함수명 식별자 값 형식
            # token = {'Function1': token} #예시
        # elif token in []:
            # token = {'Function2': token} #예시
        elif token == '*':
            token = {'multiply': token}
        elif token == '+':
            token = {'plus': token}
        elif token == '-':
            token = {'minus': token}
        elif token == '/':
            token = {'divide': token}
        else:
            token = {'identifier': token}
        tokenized.append(token)
    tokenized.append(comment)
    return tokenized


print(tokenize(program))
