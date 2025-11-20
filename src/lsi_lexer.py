# lsi_lexer.py
# Autores: <seu grupo>
# Implementação do analisador léxico da linguagem LSI-2025-2

from dataclasses import dataclass

KEYWORDS = {"int", "if", "else", "def", "print", "return"}

SINGLE_CHAR_TOKENS = {
    '+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'DIV', '=': 'EQUAL',
    '(': 'LPAREN', ')': 'RPAREN', '{': 'LBRACE', '}': 'RBRACE',
    ',': 'COMMA', ';': 'SEMI'
}

MULTI_CHAR = {'<=': 'LE', '>=': 'GE', '==': 'EQ', '!=': 'NE'}
SIMPLE_OPS = {'<': 'LT', '>': 'GT'}


@dataclass
class Token:
    typ: str
    lexeme: str
    line: int
    col: int


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

        self.symbol_table = {}
        for kw in KEYWORDS:
            self.symbol_table[kw] = {"kind": "keyword"}

    def peek(self):
        return None if self.i >= len(self.text) else self.text[self.i]

    def advance(self):
        c = self.peek()
        if c is None:
            return None
        self.i += 1

        if c == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1

        return c

    def make_token(self, typ, lexeme, line, col):
        # salva novo ID na tabela de símbolos
        if typ == "ID" and lexeme not in self.symbol_table:
            self.symbol_table[lexeme] = {"kind": "id"}
        return Token(typ, lexeme, line, col)

    def skip_space_and_comments(self):
        while True:
            c = self.peek()
            if c is None:
                return
            if c.isspace():
                self.advance()
                continue
            if c == '/' and self.i + 1 < len(self.text) and self.text[self.i + 1] == '/':
                # comentário até o fim da linha
                self.advance()
                self.advance()
                while self.peek() not in (None, "\n"):
                    self.advance()
                continue
            break

    def next_token(self):
        self.skip_space_and_comments()
        c = self.peek()

        if c is None:
            return None

        line, col = self.line, self.col

        # Identificadores e keywords
        if c.isalpha() or c == '_':
            lex = ""
            while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                lex += self.advance()

            if lex in KEYWORDS:
                return self.make_token(lex.upper(), lex, line, col)
            return self.make_token("ID", lex, line, col)

        # Números
        if c.isdigit():
            lex = ""
            while self.peek() and self.peek().isdigit():
                lex += self.advance()
            return self.make_token("NUM", lex, line, col)

        # operadores de dois caracteres
        two = self.text[self.i:self.i + 2]
        if two in MULTI_CHAR:
            self.advance(); self.advance()
            return self.make_token(MULTI_CHAR[two], two, line, col)

        # < e >
        if c in SIMPLE_OPS:
            return self.make_token(SIMPLE_OPS[self.advance()], c, line, col)

        # operadores e pontuação simples
        if c in SINGLE_CHAR_TOKENS:
            return self.make_token(SINGLE_CHAR_TOKENS[self.advance()], c, line, col)

        # caso contrário → erro léxico
        raise LexerError(f"Erro léxico em {line}:{col} — caractere inválido '{c}'")

    def tokenize_all(self):
        tokens = []
        while True:
            t = self.next_token()
            if t is None:
                break
            tokens.append(t)

        tokens.append(Token("EOF", "$", self.line, self.col))
        return tokens, self.symbol_table
