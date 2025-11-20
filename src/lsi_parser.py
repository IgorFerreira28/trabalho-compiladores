from lsi_lexer import *

EPS = "epsilon"

# =========================================
# TERMINAIS
# =========================================
TERMINALS = {
    "id", "NUM",

    "PLUS", "MINUS", "TIMES", "DIV",
    "EQUAL",

    "LPAREN", "RPAREN",
    "LBRACE", "RBRACE",

    "COMMA", "SEMI",

    "LT","LE","GT","GE","EQ","NE",

    "def","int","if","else","print","return",

    "$"
}

# =========================================
# GRAMÁTICA LL(1)
# =========================================
GRAMMAR = {

    "MAIN": [["FLIST"], [EPS]],

    "FLIST": [
        ["FDEF", "FLIST"],
        [EPS]
    ],

    "FDEF": [["def", "id", "LPAREN", "PARLIST", "RPAREN", "LBRACE", "STMTLIST", "RBRACE"]],

    # -------------------------------------
    # PARÂMETROS
    # -------------------------------------
    "PARLIST": [["PARAM", "PARLIST_TAIL"], [EPS]],

    "PARLIST_TAIL": [["COMMA", "PARAM", "PARLIST_TAIL"], [EPS]],

    "PARAM": [["int", "id"]],

    # -------------------------------------
    # DECLARAÇÕES
    # -------------------------------------
    "VARLIST": [
        ["id", "VARLIST_TAIL"]
    ],

    "VARLIST_TAIL": [
        ["COMMA", "id", "VARLIST_TAIL"],
        [EPS]
    ],

    "STMTLIST": [["STMT", "STMTLIST"], [EPS]],

    "STMT": [
        ["int", "VARLIST", "SEMI"],
        ["ATRIBST", "SEMI"],
        ["PRINTST", "SEMI"],
        ["RETURNST", "SEMI"],
        ["IFSTMT"],
        ["LBRACE", "STMTLIST", "RBRACE"],
        ["SEMI"]
    ],

    # -------------------------------------
    # ATRIBUIÇÃO / CHAMADA
    # -------------------------------------
    "ATRIBST": [
        ["id", "EQUAL", "EXPR"]
    ],

    "FCALL": [["id", "LPAREN", "PARLISTCALL", "RPAREN"]],

    "PARLISTCALL": [
        ["EXPR", "PARLISTCALL_TAIL"], 
        [EPS]
    ],

    "PARLISTCALL_TAIL": [
        ["COMMA", "EXPR", "PARLISTCALL_TAIL"],
        [EPS]
    ],

    # -------------------------------------
    # PRINT / RETURN
    # -------------------------------------
    "PRINTST": [["print", "EXPR"]],

    "RETURNST": [ ["return", "RETURN_TAIL"] ],

    "RETURN_TAIL": [
        ["EXPR"],
        [EPS]
    ],

    # -------------------------------------
    # IF
    # -------------------------------------
    "IFSTMT": [
        ["if", "LPAREN", "EXPR", "RPAREN", "LBRACE", "STMTLIST", "RBRACE", "IF_TAIL"]
    ],

    "IF_TAIL": [
        ["else", "LBRACE", "STMTLIST", "RBRACE"],
        [EPS]
    ],

    # -------------------------------------
    # EXPRESSÕES (corrigido LL(1))
    # -------------------------------------
    "EXPR": [["NUMEXPR", "EXPR_TAIL"]],

    "EXPR_TAIL": [
        ["LT", "NUMEXPR", "EXPR_TAIL"],
        ["LE", "NUMEXPR", "EXPR_TAIL"],
        ["GT", "NUMEXPR", "EXPR_TAIL"],
        ["GE", "NUMEXPR", "EXPR_TAIL"],
        ["EQ", "NUMEXPR", "EXPR_TAIL"],
        ["NE", "NUMEXPR", "EXPR_TAIL"],
        [EPS]
    ],

    "NUMEXPR": [["TERM", "NUMEXPR_TAIL"]],

    "NUMEXPR_TAIL": [
        ["PLUS", "TERM", "NUMEXPR_TAIL"],
        ["MINUS", "TERM", "NUMEXPR_TAIL"],
        [EPS]
    ],

    "TERM": [["FACTOR", "TERM_TAIL"]],

    "TERM_TAIL": [
        ["TIMES", "FACTOR", "TERM_TAIL"],
        ["DIV", "FACTOR", "TERM_TAIL"],
        [EPS]
    ],

    "FACTOR": [
        ["NUM"],
        ["id", "FACTOR_TAIL"],
        ["LPAREN", "EXPR", "RPAREN"]
    ],

    "FACTOR_TAIL": [
        ["LPAREN", "PARLISTCALL", "RPAREN"],
        [EPS]
    ],

}

# =========================================
# MAPEAMENTO DO LEXER PARA TERMINAIS
# =========================================
LEX_TO_GR = {
    "ID": "id",
    "NUM": "NUM",

    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "TIMES": "TIMES",
    "DIV": "DIV",

    "EQUAL": "EQUAL",

    "LPAREN": "LPAREN", "RPAREN": "RPAREN",
    "LBRACE": "LBRACE", "RBRACE": "RBRACE",

    "COMMA": "COMMA", "SEMI": "SEMI",

    "LT": "LT", "LE": "LE", "GT": "GT", "GE": "GE",
    "EQ": "EQ", "NE": "NE",

    "DEF": "def", "INT": "int",
    "IF": "if", "ELSE": "else",
    "PRINT": "print", "RETURN": "return",
}

def token_to_terminal(tok):
    """
    Mapeia um objeto Token (saída do Lexer) para seu símbolo Terminal correspondente
    na gramática.

    O Lexer pode produzir tipos como 'ID' ou 'DEF', que são mapeados para 'id' e 'def',
    respectivamente, na gramática.

    Parâmetros:
      tok (Token): O token a ser mapeado.

    Retorno:
      str: O símbolo terminal da gramática, ou '$' para EOF.
    """

    if tok.typ == "EOF":
        return "$"
    return LEX_TO_GR.get(tok.typ, tok.lexeme)

# =========================================
# FIRST
# =========================================
def compute_first():
    """
    Calcula o conjunto FIRST para todos os Não-Terminais da GRAMMAR.

    O algoritmo é iterativo (fixed-point iteration), repetindo o cálculo até que
    nenhum novo terminal possa ser adicionado a nenhum conjunto FIRST, garantindo a convergência.

    Regras:
    1. Se A -> X..., onde X é terminal, então X está em FIRST(A).
    2. Se A -> X1 X2..., onde X1 é Não-Terminal:
        - FIRST(X1) (exceto EPS) é adicionado a FIRST(A).
        - Se EPS está em FIRST(X1), o processo continua para X2.
    3. Se A pode derivar a string vazia (A -> EPS ou todos os símbolos derivam EPS),
        então EPS está em FIRST(A).

    Retorno:
      dict: Um dicionário onde as chaves são os Não-Terminais e os valores são os
        conjuntos de seus FIRST (set de str).
    """

    FIRST = {A: set() for A in GRAMMAR}

    changed = True
    while changed:
        changed = False

        for A, prods in GRAMMAR.items():
            for prod in prods:

                if prod == [EPS]:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
                    continue

                for X in prod:

                    if X in TERMINALS:
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break

                    if X in GRAMMAR:
                        before = len(FIRST[A])
                        FIRST[A].update(a for a in FIRST[X] if a != EPS)
                        if len(FIRST[A]) != before:
                            changed = True
                        if EPS in FIRST[X]:
                            continue
                        break

                else:
                    if EPS not in FIRST[A]:
                        FIRST[A].add(EPS)
                        changed = True
    return FIRST


# =========================================
# FIRST de sequência
# =========================================
def first_sequence(seq, FIRST):
    """
    Calcula o FIRST de uma sequência de símbolos (a parte direita de uma produção).

    O cálculo itera sobre os símbolos da sequência. Se um símbolo não produz
    EPS, o cálculo para. Se todos produzem EPS, então EPS está no FIRST da sequência.

    Parâmetros:
      seq (list): A sequência de símbolos (terminais ou não-terminais).
      FIRST (dict): Os conjuntos FIRST pré-calculados para os Não-Terminais.

    Retorno:
      set: O conjunto FIRST da sequência.
    """

    result = set()

    # seq vazia → epsilon
    if not seq:
        result.add(EPS)
        return result

    for X in seq:

        # X é epsilon literal
        if X == EPS:
            result.add(EPS)
            return result

        # X é terminal real
        if X in TERMINALS:
            result.add(X)
            return result

        # X é não-terminal
        # adiciona FIRST(X) exceto epsilon
        for a in FIRST[X]:
            if a != EPS:
                result.add(a)

        # se X não produz epsilon → para
        if EPS not in FIRST[X]:
            return result

        # senão: X produz epsilon → continuar para o próximo

    # se todos produzem epsilon
    result.add(EPS)
    return result



# =========================================
# FOLLOW
# =========================================
def compute_follow(FIRST):
    """
    Calcula o conjunto FOLLOW para todos os Não-Terminais da GRAMMAR.

    O algoritmo é iterativo, repetindo o cálculo até que nenhum novo terminal
    possa ser adicionado a nenhum conjunto FOLLOW (convergência).

    Regras:
    1. FOLLOW(MAIN) contém '$' (fim de arquivo).
    2. Se A -> alpha X beta:
        - FOLLOW(X) inclui FIRST(beta) (exceto EPS).
    3. Se A -> alpha X beta e beta pode derivar EPS (ou beta é vazio):
        - FOLLOW(X) inclui FOLLOW(A). (Regra de propagação que exige a iteração).

    Parâmetros:
      FIRST (dict): Os conjuntos FIRST pré-calculados.

    Retorno:
      dict: Um dicionário onde as chaves são os Não-Terminais e os valores são os
        conjuntos de seus FOLLOW (set de str).
    """

    FOLLOW = {A: set() for A in GRAMMAR}

    FOLLOW["MAIN"].add("$")

    changed = True
    while changed:
        changed = False

        for A, prods in GRAMMAR.items():
            for prod in prods:

                for i, X in enumerate(prod):

                    if X not in GRAMMAR:
                        continue

                    beta = prod[i+1:]
                    fs = first_sequence(beta, FIRST)

                    before = len(FOLLOW[X])

                    # Regra 2: FOLLOW(X) inclui FIRST(beta) - {EPS}
                    FOLLOW[X].update(a for a in fs if a != EPS)

                    # Regra 3: Se beta -> EPS, FOLLOW(X) inclui FOLLOW(A)
                    if EPS in fs or not beta:
                        FOLLOW[X].update(FOLLOW[A])

                    if len(FOLLOW[X]) != before:
                        changed = True

    return FOLLOW


# =========================================
# TABELA LL(1)
# =========================================
def build_table(FIRST, FOLLOW):
    """
    Constrói a Tabela de Análise Preditiva LL(1) a partir dos conjuntos FIRST e FOLLOW.

    O resultado é um dicionário que mapeia o par (Não-Terminal, Terminal) para a Regra de Produção.
    - Chave: (str Não-Terminal, str Terminal)
    - Valor: list Regra de Produção (ex: ['def', 'id', 'LPAREN', ...])

    Regras de Preenchimento:
    1. Para toda produção A -> alpha e para todo terminal t em FIRST(alpha) (t != EPS),
       adiciona-se a regra A -> alpha na célula [A, t].
    2. Se EPS está em FIRST(alpha), para todo terminal b em FOLLOW(A), adiciona-se
       a regra A -> alpha na célula [A, b].

    Parâmetros:
      FIRST (dict): Os conjuntos FIRST.
      FOLLOW (dict): Os conjuntos FOLLOW.

    Retorno:
      dict: A Tabela LL(1) de análise.
    """

    table = {}

    for A, prods in GRAMMAR.items():
        for prod in prods:

            fs = first_sequence(prod, FIRST)

            # Regra 1: Para cada terminal em FIRST(alpha), insere na tabela
            for t in fs:
                if t != EPS:
                    table[(A, t)] = prod

            # Regra 2: Se EPS está em FIRST(alpha), usa FOLLOW(A)
            if EPS in fs:
                for b in FOLLOW[A]:
                    table[(A, b)] = prod

    return table


# =========================================
# PARSER
# =========================================
class Parser:
    """
    Implementa o Analisador Sintático (Parser) Preditivo Não-Recursivo LL(1).
   
    Ele utiliza a pilha e a Tabela LL(1) pré-calculada para guiar a análise
    dos tokens de entrada.
    """

    def __init__(self):
        """
        Inicializa o Parser calculando os conjuntos FIRST, FOLLOW e a Tabela LL(1).
        """

        self.FIRST = compute_first()
        self.FOLLOW = compute_follow(self.FIRST)
        self.table = build_table(self.FIRST, self.FOLLOW)

    def parse(self, tokens):
        """
        Executa o algoritmo de Parsing LL(1) não-recursivo.

        O parser usa uma pilha e a Tabela de Análise para determinar a próxima
        ação (match de terminal ou expansão de Não-Terminal).

        Parâmetros:
          tokens (list): Lista de objetos Token fornecida pelo Lexer.

        Retorno:
          bool: True se o parsing foi bem-sucedido.

        Lança:
          Exception: Em caso de Erro Sintático (Terminal Mismatch ou No Rule).
        """

        stream = [token_to_terminal(t) for t in tokens]
        stack = ["$", "MAIN"]
        ip = 0

        while True:

            top = stack.pop()
            cur = stream[ip]
            print(f"STACK TOP:{top:10} | CURRENT TOKEN:{cur}")


            if top == "$" and cur == "$":
                print("Parse OK.")
                return True

            if top in TERMINALS:
                if top == cur:
                    ip += 1
                    continue
                raise Exception(f"Esperado '{top}', encontrado '{cur}'.")

            rule = self.table.get((top, cur))
            if rule is None:
                raise Exception(f"Erro sintático: não há regra ({top}, {cur})")

            if rule != [EPS]:
                for s in reversed(rule):
                    stack.append(s)


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    import sys
    from lsi_lexer import LexerError

    """
    Ponto de entrada do programa.
    1. Lê o arquivo de entrada.
    2. Executa o Lexer para obter tokens e a tabela de símbolos (com tratamento de erro léxico).
    3. Instancia e executa o Parser (com tratamento de erro sintático).
    """

    fname = sys.argv[1]
    text = open(fname).read()

    lexer = Lexer(text)

    try:
        tokens, symtab = lexer.tokenize_all()
    except LexerError as e:
        print(f"\n=== ERRO LÉXICO ===")
        print(e)
        sys.exit(1)

    print("TOKENS:", [f"{t.typ}:{t.lexeme}" for t in tokens])

    try:
        parser = Parser()
        parser.parse(tokens)
    except Exception as e:
        print(f"\n=== ERRO SINTÁTICO ===")
        print(e)
        sys.exit(1)
