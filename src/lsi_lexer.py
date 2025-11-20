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
    """
    Representa um token léxico gerado pelo Lexer.

    Atributos:
      typ (str): O tipo do token (ex: 'ID', 'NUM', 'PLUS', 'DEF').
      lexeme (str): A string exata que corresponde ao token no código-fonte.
      line (int): O número da linha onde o token começa.
      col (int): O número da coluna onde o token começa.
    """
    typ: str
    lexeme: str
    line: int
    col: int


class LexerError(Exception):
    """
    Exceção customizada para erros léxicos, utilizada para sinalizar
    a ocorrência de caracteres inválidos.
    """
    pass


class Lexer:
    """
    Analisador Léxico (Lexer) para a linguagem LSI.

    Percorre o código-fonte (string de texto) e o transforma em uma sequência de Tokens.
    Mantém o controle da posição atual (índice, linha e coluna) e gerencia uma Tabela de Símbolos.
    """

    def __init__(self, text: str):
        """
        Inicializa o Lexer.

        Parâmetros:
          text (str): A string contendo o código-fonte completo.
        """
        self.text = text
        self.i = 0  # Índice de leitura atual
        self.line = 1  # Número da linha atual
        self.col = 1  # Número da coluna atual

        # Inicializa a tabela de símbolos com as palavras-chave
        self.symbol_table = {}
        for kw in KEYWORDS:
            self.symbol_table[kw] = {"kind": "keyword"}

    def peek(self):
        """
        Retorna o próximo caractere sem avançar o ponteiro (lookahead).
        Retorna None se o fim do arquivo for alcançado.
        """
        return None if self.i >= len(self.text) else self.text[self.i]

    def advance(self):
        """
        Consome o caractere atual, avança o ponteiro de leitura (i)
        e atualiza os contadores de linha e coluna.
        """
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
        """
        Cria um novo objeto Token e gerencia a Tabela de Símbolos.

        Se o tipo for 'ID' e o lexema não estiver na tabela (ou seja, é um novo
        identificador), ele é registrado.
        """
        # salva novo ID na tabela de símbolos
        if typ == "ID" and lexeme not in self.symbol_table:
            self.symbol_table[lexeme] = {"kind": "id"}
        return Token(typ, lexeme, line, col)

    def skip_space_and_comments(self):
        """
        Avança o ponteiro de leitura, ignorando espaços em branco (incluindo quebras de linha)
        e comentários de linha única ('//').
        """
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
        """
        Analisa e retorna o próximo token léxico do stream de entrada.
        Implementa a lógica de reconhecimento de padrões (autômatos).

        Retorno:
          Token: O próximo token válido, ou None se o EOF for alcançado.

        Lança:
          LexerError: Se um caractere inválido for encontrado.
        """
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
        raise LexerError(f"Erro léxico em linha: {line} Coluna: {col} — caractere inválido '{c}'")

    def tokenize_all(self):
        """
        Executa o Lexer para produzir todos os tokens do código-fonte.

        Retorno:
          tuple: (list de Tokens, dict Tabela de Símbolos)
        """
        tokens = []
        while True:
            t = self.next_token()
            if t is None:
                break
            tokens.append(t)

        tokens.append(Token("EOF", "$", self.line, self.col))
        return tokens, self.symbol_table
