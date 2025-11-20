# lsi_parser.py
# Autores: <seu grupo>

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

    "PARLISTCALL": [["id", "PARLISTCALL_TAIL"], [EPS]],

    "PARLISTCALL_TAIL": [
        ["COMMA", "id", "PARLISTCALL_TAIL"],
        [EPS]
    ],

    # -------------------------------------
    # PRINT / RETURN
    # -------------------------------------
    "PRINTST": [["print", "EXPR"]],

    "RETURNST": [ ["return", "RETURN_TAIL"] ],

    "RETURN_TAIL": [
        ["id"],
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
        ["LPAREN", "PARLISTCALL", "RPAREN"], # chamada de função
        [EPS]                                # variável simples
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
    if tok.typ == "EOF":
        return "$"
    return LEX_TO_GR.get(tok.typ, tok.lexeme)

# =========================================
# FIRST
# =========================================
def compute_first():
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

                    FOLLOW[X].update(a for a in fs if a != EPS)

                    if EPS in fs or not beta:
                        FOLLOW[X].update(FOLLOW[A])

                    if len(FOLLOW[X]) != before:
                        changed = True

    return FOLLOW


# =========================================
# TABELA LL(1)
# =========================================
def build_table(FIRST, FOLLOW):
    table = {}

    for A, prods in GRAMMAR.items():
        for prod in prods:

            fs = first_sequence(prod, FIRST)

            for t in fs:
                if t != EPS:
                    table[(A, t)] = prod

            if EPS in fs:
                for b in FOLLOW[A]:
                    table[(A, b)] = prod

    return table


# =========================================
# PARSER
# =========================================
class Parser:
    def __init__(self):
        self.FIRST = compute_first()
        self.FOLLOW = compute_follow(self.FIRST)
        self.table = build_table(self.FIRST, self.FOLLOW)

    def parse(self, tokens):
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
