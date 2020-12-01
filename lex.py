import re

def tokenize(chars: str):
    chars = chars.lower() #String 대소문자를 전부 소문자로 처리
    # comment = {'comment': chars.split(';', 1)[1]} # 주석
    tokens = chars.split(';')[0].replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ").split() # 주석 제거
    tokenized = []
    for token in tokens:
        if token in ['(',')',"'",'*','+','-','/','<','>','<=','>=','$']:
            token = {token: token}
        elif token in ['begin', 'define', 'setq', 'car','cdr', 'list', 'nth', 'nil', 'cons','reverse','append','length','member','assoc','remove','subst','atom','null','numberp','zerop','minusp','equal','stringp','if','cond'] :  
            token = {token.upper() : token.upper()} #함수들을 다 대문자로 토큰화 
        elif re.compile(r'^ca[d]+r').search(token): #car {cdr}  == ca{d}r , 토큰은 cadr로 
            token = {'CADR': token.upper()}
        else:
            if re.compile(r'^[\d]+.[\d]*$').search(token):
                token = {'value': token} 
            else:
                token = {'id': token}
        tokenized.append(token)
    return tokenized


if __name__ == "__main__":
    test_text = '(cadddr X) ;this is comment'
    print(tokenize(test_text))
