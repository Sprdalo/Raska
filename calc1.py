INTEGER, PLUS, EOF, SPACE, MINUS, PUTA, DELI = 'INTEGER', 'PLUS', 'EOF', 'SPACE', 'MINUS', 'PUTA', 'DELI'
ZNAK = 'ZNAK'

def izracunaj(x, y, operator):
    if operator == 'MINUS':
        return (x - y);
    if operator == 'PLUS':
        return (x + y);
    if operator == 'PUTA':
        return (x * y);
    if operator == 'DELI':
        return (x / y);
    return 0;

def convert(s):
    if s == PLUS:
        return 'PLUS'
    if s == MINUS:
        return 'MINUS'
    if s == PUTA:
        return 'PUTA'
    if s == DELI:
        return 'DELI'

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


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

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
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()