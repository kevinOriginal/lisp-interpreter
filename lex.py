import re

def tokenize(chars: str):
    strings = []
    _text = chars
    #문자열 찾기(string) 
    while True:
        re_string = re.compile('"[\w+\s*]+"').search(_text)
        if re_string:
            strings.append(_text[re_string.start():re_string.end()])
            _text = _text[:re_string.start()] + _text[re_string.end():]
        else:
            break
    #문자열 중 공백(띄어쓰기) 있는 경우 띄어쓰기를 없앰. 
    while True:
        re_chars = re.compile('"(\w+\s+)[\w\s]+"').search(chars)
        if re_chars:
            chars = chars[:re_chars.start()] + chars[re_chars.start():re_chars.end()].replace(' ', '') + chars[re_chars.end():]
        else:
            break

    char = []
    _text = chars
    #문자 찾기(char) 
    while True:
        re_char = re.compile(r'#\\\w').search(_text)
        if re_char:
            char.append(_text[re_char.start():re_char.end()])
            _text = _text[:re_char.start()] + _text[re_char.end():]
        else:
            break
    # comment = {'comment': chars.split(';', 1)[1]} # 주석
    chars = chars.lower() #String 대소문자를 전부 소문자로 처리
    tokens = chars.split(';')[0].replace('#(', ' # (').replace('(', ' ( ').replace(')', ' ) ').replace("'", " ' ").split()
    tokenized = []
    
    for token in tokens:
        # (,),',# 같이 다른 토큰이랑 붙어있는 것들을 replace를 이용해 공백을 주고, 전체적으로 공백으로 문자열을 나눔. 
        if token in ['(',')',"'",'*','+','-','/','<','>','<=','>=','$','#']:
            token = {token: token}
        # = 은 EQUAL 함수와 같으므로 EQUAL 로 토큰화
        elif token == '=':
            token = {'EQUAL': 'EQUAL'}
        # % 는 / 와 같으므로 / 으로 토큰화
        elif token == '%':
            token = {'/' : '%' }
        #함수는 함수명으로 토큰화
        elif token in ['begin', 'define', 'setq', 'car','cdr', 'list', 'nth', 'nil', 'cons' ,'reverse','append','length','member','assoc','remove','subst','atom','null','numberp','zerop','minusp','equal','stringp','if','cond','nil'] :  
            token = {token.upper() : token.upper()} #함수들을 다 대문자로 토큰화 
        # print의 경우, 프로젝트에서 제시된 함수가 아니기에 문법적으로 순서가 비슷한 STRINGP로 key를 넘기고 value로는 PRINT를 넘김. parser에는 stringp의 문법 검증이 이루어지지만 반환값은 print로 하여 함수처리에서는 print 함수의 기능을 함.
        elif token == 'print':
            token = {'STRINGP': token.upper()}
        # car과 cdr의 합성인 c[a,d]r 은 key를 cadr로 토큰화
        elif re.compile(r'^c[a]*[d]*[a*,d*]*r').search(token):         
            token = {'CADR': token.upper()}  
        else:
            #숫자, 문자열인 경우 value : 숫자,스트링 으로 토큰화
            if re.compile("[\d]+.{0,1}[\d]*").search(token):
                token = {'value': token}                 
            elif re.compile('"\w+"').search(token):
                token = {'value': strings.pop(0)}
            #문자인 경우 char로 key를 주고, value에는 '문자'로 반환
            elif re.compile(r'^#\\\w').search(token):
                if token.upper() in char:
                    text = token.upper().replace('#\\','')
                elif token.lower() in char:
                    text = token.lower().replace('#\\','')
                token = {'char': f"'{text}'" }
            #위의 과정을 다 통과한 경우 , 식별자로 판단하여 id로 토큰화
            else:
                token = {'id': token}
        tokenized.append(token)
    return tokenized


if __name__ == "__main__":
    test_text = '(SETQ A "HI THERE")'
    print(tokenize(test_text))
