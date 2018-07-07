from identi import *;

def izracunaj(x, y, operator):
    if operator == 'MINUS':
        return (x - y);
    if operator == 'PLUS':
        print("stigo do PLUS")
        return (x + y);
    if operator == 'PUTA':
        return (x * y);
    if operator == 'DELI':
        return (x // y);
    if operator == '<':
        print('stigo do MANJE')
        return (x < y);
    if operator == '>':
        print('stigo do VISE')
        return (x > y);
    else:
        print("izracunaj greska")
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
    if s == MANJE:
        return 'MANJE'
    if s == VECE:
        return 'VECE'
def is_type(text):
    if text.startswith("bool ") or text.startswith("int "):
        return True;
    return False;

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

def is_letter(text):
    if len(text) > 1:
        return False

    if (text >= 'a' and text <= 'z') or (text >= 'A' and text <= 'Z'):
        return True
    return False;


