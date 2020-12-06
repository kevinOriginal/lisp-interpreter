import re

def tokenize(chars: str):
    strings = []
    _text = chars
    while True:
        re_string = re.compile('"[\w+\s*]+"').search(_text)
        if re_string:
            strings.append(_text[re_string.start():re_string.end()])
            _text = _text[:re_string.start()] + _text[re_string.end():]
        else:
            break
    while True:
        re_chars = re.compile("(\w+\s+)+").search(chars)
        if re_chars:
            chars = chars[:re_chars.start()] + chars[re_chars.start():re_chars.end()].replace(' ', '') + chars[re_chars.end():]
        else:
            break

    char = []
    _text = chars
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
        if token in ['(',')',"'",'*','+','-','/','<','>','<=','>=','$','#']:
            token = {token: token}
        elif token == '%':
            token = {'/' : '%' }
        elif token in ['begin', 'define', 'setq', 'car','cdr', 'list', 'nth', 'nil', 'cons','reverse','append','length','member','assoc','remove','subst','atom','null','numberp','zerop','minusp','equal','stringp','if','cond','print','nil'] :  
            token = {token.upper() : token.upper()} #함수들을 다 대문자로 토큰화 
        elif re.compile(r'^c[a]*[d]*[a*,d*]*r').search(token):         
            token = {'CADR': token.upper()}  #car {cdr}  == ca{d}r , 토큰은 cadr로 
        else:
            if re.compile("[\d]+.{0,1}[\d]*").search(token):
                token = {'value': token}                 
            elif re.compile('"\w+"').search(token):
                token = {'value': strings.pop(0)}
            elif re.compile(r'^#\\\w').search(token):
                if token.upper() in char:
                    text = token.upper().replace('#\\','')
                elif token.lower() in char:
                    text = token.lower().replace('#\\','')
                token = {'char': f"'{text}'" }
            else:
                token = {'id': token}
        tokenized.append(token)
    return tokenized


if __name__ == "__main__":
    test_text = '(+ "xhi h" "y")'
    print(tokenize(test_text))
