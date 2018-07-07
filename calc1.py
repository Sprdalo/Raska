INTEGER, PLUS, EOF, SPACE, MINUS, PUTA, DELI = 'INTEGER', 'PLUS', 'EOF', 'SPACE', 'MINUS', 'PUTA', 'DELI'
ZNAK, BOOL = 'ZNAK', 'BOOL'

def izracunaj(x, y, operator):
    if operator == 'MINUS':
        return (x - y);
    if operator == 'PLUS':
        return (x + y);
    if operator == 'PUTA':
        return (x * y);
    if operator == 'DELI':
        return (x // y);
    return 0;

def clean(text):
    return text.replace(" ", "");

def convert(s):
    if s == PLUS:
        return 'PLUS'
    if s == MINUS:
        return 'MINUS'
    if s == PUTA:
        return 'PUTA'
    if s == DELI:
        return 'DELI'

def is_type(text):
    if text.startswith("bool ") or text.startswith("int "):
        return True;
    return False;

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):

        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

mapa = {}

class Declaraction(object):
    def __init__(self, name, v):

        if name in mapa:
            raise Exception('Vec inicijalizovana vrednost');

        v = clean(v);
        interpreter = Interpreter(v);
        self.value = interpreter.expr();
        self.name = name;
        mapa[name] = self.value;

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Greska pri parsiranju unosa')

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == '*':
            token = Token(PUTA, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DELI, current_char)
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == SPACE:
            self.current_token = self.get_next_token();
            return self.eat(token_type);

        if self.current_token.type == token_type:
            return True;
        else:
            return False;

    def expr(self):

        self.text = clean(self.text);
        if not self.text:
            return 0;

        tester = True
        for i in self.text:
            if not i.isdigit():
                tester = False;

        if tester:
            return int(self.text);

        self.current_token = self.get_next_token()

        result = 0;
        test = False;

        while not self.eat(EOF):

            if test == False:
                left = self.current_token
                if self.eat(INTEGER) == False:
                    self.error()

                x = 0;
                while self.eat(INTEGER) == True:
                    x *= 10;
                    left = self.current_token;
                    x += left.value
                    self.current_token = self.get_next_token()
            else:
                x = 0;
            op = self.current_token

            operator = convert(self.current_token.type);

            self.current_token = self.get_next_token()

            right = self.current_token
            if self.eat(INTEGER) == False:
                self.error()
            
            y = 0;
            while self.eat(INTEGER) == True:
                y *= 10;
                right = self.current_token;
                y += right.value
                self.current_token = self.get_next_token()


            if x == 0:
                result = izracunaj(result, y, operator);
            else:
                result += izracunaj(x, y, operator);
            test = True;
        return result;

def pozicije(text):
    pos = [-1]
    for i in range(len(text)):
        if text[i] == '+' or text[i] == '-':
            pos.append(i);
    return pos;

def segment(text):
    l = -1; r = -1;
    for i in range(len(text)):
        if text[i] == ' ':
            if l == -1:
                l = i;
            if r == -1 and l != -1:
                r = i;
    return (l, r);

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        if is_type(text):
            if (text.startswith("int ")):
                par = segment(text);

                declaraction = Declaraction(text[par[0] + 1: par[1] + 3], text[(par[1] + 5) :]);
                text = text[(par[1] + 5) :];

        text = clean(text);

        pos = pozicije(text);
        tekst = "";
        for i in range(len(pos) - 1):
            interpreter = Interpreter(text[pos[i] + 1 : pos[i + 1]]);
            tekst += str(interpreter.expr()) + text[pos[i + 1]];
        interpreter = Interpreter(text[pos[len(pos) - 1] + 1 :])
        tekst += str(interpreter.expr())

        interpreter = Interpreter(tekst)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()