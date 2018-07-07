from globalna import *;
from identi import *;

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

        if is_letter(current_char) == True:
            token = Token(VAR, current_char)
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

        if current_char == '<':
            token = Token(MANJE, current_char)
            self.pos += 1
            return token

        if current_char == '>':
            token = Token(VECE, current_char)
            self.pos += 1
            return token
        print("get next token error")
        self.error()

    def eat(self, token_type):
        if self.current_token.type == SPACE:
            self.current_token = self.get_next_token();
            return self.eat(token_type);

        if token_type == VAR:
            if is_letter(self.text) == True:
                return True
            return False;

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
        x = -1.1
        test = False;

        while not self.eat(EOF):

            if len(self.text) == 1 and self.eat('VAR') == True:
                x = mapa[self.text];
                return x;
            else:
                if test == False and self.eat('VAR') == False:
                    left = self.current_token
                    if self.eat(INTEGER) == False:
                        print("left error")
                        self.error()

                    x = 0;
                    while self.eat(INTEGER) == True:
                        x *= 10;
                        left = self.current_token;
                        x += left.value
                        self.current_token = self.get_next_token()
                else:
                    if self.eat('VAR') == False:
                        x = 0;
                    else:
                        x = mapa[self.text];
                        #self.current_token = self.get_next_token();

            op = self.current_token

            operator = convert(self.current_token.type);
            self.current_token = self.get_next_token()

            right = self.current_token
            if self.eat(INTEGER) == False:
                print("right error")
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

                declaraction = Declaraction(text[par[0] + 1: par[1] + 2], text[(par[1] + 5) :]);
                
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