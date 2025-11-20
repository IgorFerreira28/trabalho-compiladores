# 📄 Documentação da Análise Sintática Preditiva LL(1) (Parte 2)

Este documento detalha a transformação da gramática LSI-2025-2 em um formato LL(1), a construção dos conjuntos FIRST e FOLLOW, e a matriz da tabela de reconhecimento sintático preditivo.

## 1. Gramática LSI-2025-2 Transformada em LL(1)

A gramática original fornecida continha problemas de **recursão à esquerda** (`NUMEXPR`, `TERM`) e **fatoração à esquerda** (`STMT`, `FACTOR`, etc.), que são incompatíveis com o analisador preditivo LL(1). As regras foram reescritas para eliminar essas ambiguidades.

### 1.1. Detalhes das Transformações e Justificativas

| Problema Original | Não-Terminal(is) | Justificativa |
| :--- | :--- | :--- |
| **Recursão à Esquerda** | `NUMEXPR`, `TERM` | Implementação de regras de cauda (`\_TAIL`) para permitir que o parser determine a produção correta (adição/subtração ou multiplicação/divisão) olhando apenas para o próximo token. |
| **Fatoração à Esquerda** | `FACTOR`, `ATRIBST`, `RETURNST` | Fatoração dos prefixos comuns (`id`, `return`) para distinguir chamadas de função (`FCALL`) de variáveis (`EXPR`) e declarações completas de comandos incompletos. |
| **Listas** | `FLIST`, `PARLIST`, `STMTLIST` | Conversão de listas recursivas em estruturas que usam $\epsilon$ como produção de parada para sequências de zero ou mais elementos, adequadas para LL(1). |

### 1.2. Gramática LSI-2025-2 em Formato LL(1)

A gramática transformada utiliza não-terminais auxiliares (indicados com `_TAIL`).

| # | Produção |
| :--- | :--- |
| **1.** | $MAIN \rightarrow FLIST\ \$$ |
| **2.** | $FLIST \rightarrow FDEF\ FLIST\_TAIL\ |\ \epsilon$ |
| **3.** | $FLIST\_TAIL \rightarrow FDEF\ FLIST\_TAIL\ |\ \epsilon$ |
| **4.** | $FDEF \rightarrow def\ id\ LPAREN\ PARLIST\ RPAREN\ LBRACE\ STMTLIST\ RBRACE$ |
| **5.** | $PARLIST \rightarrow int\ id\ PARLIST\_TAIL\ |\ \epsilon$ |
| **6.** | $PARLIST\_TAIL \rightarrow COMMA\ int\ id\ PARLIST\_TAIL\ |\ \epsilon$ |
| **7.** | $STMTLIST \rightarrow STMT\ STMTLIST\ |\ \epsilon$ |
| **8.** | $STMT \rightarrow int\ VARLIST\ SEMI$ |
| **9.** | $STMT \rightarrow ATRIBST\ SEMI$ |
| **10.** | $STMT \rightarrow PRINTST\ SEMI$ |
| **11.** | $STMT \rightarrow RETURNST\ SEMI$ |
| **12.** | $STMT \rightarrow IFSTMT$ |
| **13.** | $STMT \rightarrow LBRACE\ STMTLIST\ RBRACE$ |
| **14.** | $STMT \rightarrow SEMI$ |
| **15.** | $VARLIST \rightarrow id\ VARLIST\_TAIL$ |
| **16.** | $VARLIST\_TAIL \rightarrow COMMA\ id\ VARLIST\_TAIL\ |\ \epsilon$ |
| **17.** | $ATRIBST \rightarrow id\ ASSIGN\ ATRIBST\_TAIL$ |
| **18.** | $ATRIBST\_TAIL \rightarrow EXPR\ |\ FCALL$ |
| **19.** | $FCALL \rightarrow id\ LPAREN\ PARLISTCALL\ RPAREN$ |
| **20.** | $PARLISTCALL \rightarrow EXPR\ PARLISTCALL\_TAIL\ |\ \epsilon$ |
| **21.** | $PARLISTCALL\_TAIL \rightarrow COMMA\ EXPR\ PARLISTCALL\_TAIL\ |\ \epsilon$ |
| **22.** | $PRINTST \rightarrow print\ EXPR$ |
| **23.** | $RETURNST \rightarrow return\ RETURNST\_TAIL$ |
| **24.** | $RETURNST\_TAIL \rightarrow EXPR\ |\ \epsilon$ |
| **25.** | $IFSTMT \rightarrow if\ LPAREN\ EXPR\ RPAREN\ LBRACE\ STMTLIST\ RBRACE\ IFSTMT\_TAIL$ |
| **26.** | $IFSTMT\_TAIL \rightarrow else\ LBRACE\ STMTLIST\ RBRACE\ |\ \epsilon$ |
| **27.** | $EXPR \rightarrow NUMEXPR\ EXPR\_TAIL$ |
| **28.** | $EXPR\_TAIL \rightarrow (LT\ |\ LE\ |\ GT\ |\ GE\ |\ EQ\ |\ NE)\ NUMEXPR\ EXPR\_TAIL\ |\ \epsilon$ |
| **29.** | $NUMEXPR \rightarrow TERM\ NUMEXPR\_TAIL$ |
| **30.** | $NUMEXPR\_TAIL \rightarrow (PLUS\ |\ MINUS)\ TERM\ NUMEXPR\_TAIL\ |\ \epsilon$ |
| **31.** | $TERM \rightarrow FACTOR\ TERM\_TAIL$ |
| **32.** | $TERM\_TAIL \rightarrow (TIMES\ |\ DIV)\ FACTOR\ TERM\_TAIL\ |\ \epsilon$ |
| **33.** | $FACTOR \rightarrow num\ |\ LPAREN\ EXPR\ RPAREN\ |\ id\ FACTOR\_TAIL$ |
| **34.** | $FACTOR\_TAIL \rightarrow LPAREN\ PARLISTCALL\ RPAREN\ |\ \epsilon$ |

---

## 2. Conjuntos FIRST e FOLLOW

### 2.1. Conjuntos FIRST

| Não-Terminal | $FIRST$ |
| :--- | :--- |
| **MAIN** | `{def, int, id, print, return, if, LBRACE, SEMI, $\epsilon$}` |
| **FLIST** | `{def, $\epsilon$}` |
| **FLIST\_TAIL** | `{def, $\epsilon$}` |
| **FDEF** | `{def}` |
| **PARLIST** | `{int, $\epsilon$}` |
| **PARLIST\_TAIL** | `{COMMA, $\epsilon$}` |
| **STMTLIST** | `{int, id, print, return, if, LBRACE, SEMI, $\epsilon$}` |
| **STMT** | `{int, id, print, return, if, LBRACE, SEMI}` |
| **VARLIST** | `{id}` |
| **VARLIST\_TAIL** | `{COMMA, $\epsilon$}` |
| **ATRIBST** | `{id}` |
| **ATRIBST\_TAIL** | `{num, LPAREN, id}` |
| **FCALL** | `{id}` |
| **PARLISTCALL** | `{num, LPAREN, id, $\epsilon$}` |
| **PARLISTCALL\_TAIL** | `{COMMA, $\epsilon$}` |
| **PRINTST** | `{print}` |
| **RETURNST** | `{return}` |
| **RETURNST\_TAIL** | `{num, LPAREN, id, $\epsilon$}` |
| **IFSTMT** | `{if}` |
| **IFSTMT\_TAIL** | `{else, $\epsilon$}` |
| **EXPR** | `{num, LPAREN, id}` |
| **EXPR\_TAIL** | `{LT, LE, GT, GE, EQ, NE, $\epsilon$}` |
| **NUMEXPR** | `{num, LPAREN, id}` |
| **NUMEXPR\_TAIL** | `{PLUS, MINUS, $\epsilon$}` |
| **TERM** | `{num, LPAREN, id}` |
| **TERM\_TAIL** | `{TIMES, DIV, $\epsilon$}` |
| **FACTOR** | `{num, LPAREN, id}` |
| **FACTOR\_TAIL** | `{LPAREN, $\epsilon$}` |

### 2.2. Conjuntos FOLLOW

| Não-Terminal | $FOLLOW$ |
| :--- | :--- |
| **MAIN** | `{ $ }` |
| **FLIST** | `{ $ }` |
| **FLIST\_TAIL** | `{ $ }` |
| **FDEF** | `{def, $ }` |
| **PARLIST** | `{RPAREN}` |
| **PARLIST\_TAIL** | `{RPAREN}` |
| **STMTLIST** | `{RBRACE}` |
| **STMT** | `{int, id, print, return, if, LBRACE, SEMI, RBRACE}` |
| **VARLIST** | `{SEMI}` |
| **VARLIST\_TAIL** | `{SEMI}` |
| **ATRIBST** | `{SEMI}` |
| **ATRIBST\_TAIL** | `{SEMI}` |
| **FCALL** | `{SEMI, COMMA, RPAREN}` |
| **PARLISTCALL** | `{RPAREN}` |
| **PARLISTCALL\_TAIL** | `{RPAREN}` |
| **PRINTST** | `{SEMI}` |
| **RETURNST** | `{SEMI}` |
| **RETURNST\_TAIL** | `{SEMI}` |
| **IFSTMT** | $FOLLOW(STMT)$ |
| **IFSTMT\_TAIL** | $FOLLOW(IFSTMT)$ |
| **EXPR** | `{RPAREN, SEMI, COMMA}` |
| **EXPR\_TAIL** | `{RPAREN, SEMI, COMMA}` |
| **NUMEXPR** | `{LT, LE, GT, GE, EQ, NE, RPAREN, SEMI, COMMA}` |
| **NUMEXPR\_TAIL** | $FOLLOW(NUMEXPR)$ |
| **TERM** | `{PLUS, MINUS, LT, LE, GT, GE, EQ, NE, RPAREN, SEMI, COMMA}` |
| **TERM\_TAIL** | $FOLLOW(TERM)$ |
| **FACTOR** | `{TIMES, DIV, PLUS, MINUS, LT, LE, GT, GE, EQ, NE, RPAREN, SEMI, COMMA}` |
| **FACTOR\_TAIL** | $FOLLOW(FACTOR)$ |

---

## 3. Tabela de Reconhecimento Sintático LL(1)

A matriz M[A, t] é preenchida com o número da produção $A \rightarrow \alpha$ a ser aplicada, onde $t \in FIRST(\alpha)$ ou $t \in FOLLOW(A)$ se $\epsilon \in FIRST(\alpha)$. As células vazias representam um erro sintático.

| A / t | id | num | int | if | else | def | print | return | ASSIGN | LPAREN | RPAREN | LBRACE | RBRACE | COMMA | SEMI | LT | LE | GT | GE | EQ | NE | PLUS | MINUS | TIMES | DIV | $ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MAIN** | 2, $\epsilon$ | $\epsilon$ | 2, $\epsilon$ | 2, $\epsilon$ | | 1 | 2, $\epsilon$ | 2, $\epsilon$ | | $\epsilon$ | | 2, $\epsilon$ | | $\epsilon$ | 2, $\epsilon$ | | | | | | | | | | | $\epsilon$ |
| **FLIST** | | | | | | 2 | | | | | | | | | | | | | | | | | | | | $\epsilon$ |
| **FLIST\_TAIL** | | | | | | 3 | | | | | | | | | | | | | | | | | | | | $\epsilon$ |
| **FDEF** | | | | | | 4 | | | | | | | | | | | | | | | | | | | | |
| **PARLIST** | | | 5 | | | | | | | | 6 | | | | | | | | | | | | | | | |
| **PARLIST\_TAIL** | | | | | | | | | | | $\epsilon$ | | | 6 | | | | | | | | | | | | |
| **STMTLIST** | 7 | | 7 | 7 | $\epsilon$ | | 7 | 7 | | | | 7 | $\epsilon$ | | 7 | | | | | | | | | | | $\epsilon$ |
| **STMT** | 9 | | 8 | 12 | | | 10 | 11 | | | | 13 | | | 14 | | | | | | | | | | | |
| **VARLIST** | 15 | | | | | | | | | | | | | | | | | | | | | | | | | |
| **VARLIST\_TAIL** | | | | | | | | | | | | | | 16 | $\epsilon$ | | | | | | | | | | | |
| **ATRIBST** | 17 | | | | | | | | | | | | | | | | | | | | | | | | | |
| **ATRIBST\_TAIL** | 18.2 | 18.1 | | | | | | | | 18.1 | | | | | | | | | | | | | | | | |
| **FCALL** | 19 | | | | | | | | | | | | | | | | | | | | | | | | | |
| **PARLISTCALL** | 20 | 20 | | | | | | | | 20 | 21 | | | | | | | | | | | | | | | |
| **PARLISTCALL\_TAIL** | | | | | | | | | | | $\epsilon$ | | | 21 | | | | | | | | | | | | |
| **PRINTST** | | | | | | | 22 | | | | | | | | | | | | | | | | | | | |
| **RETURNST** | | | | | | | | 23 | | | | | | | | | | | | | | | | | | |
| **RETURNST\_TAIL** | 24 | 24 | | | | | | | | 24 | $\epsilon$ | | | | $\epsilon$ | | | | | | | | | | | |
| **IFSTMT** | | | | 25 | | | | | | | | | | | | | | | | | | | | | | |
| **IFSTMT\_TAIL** | 26.2 | | 26.2 | 26.2 | 26.1 | | 26.2 | 26.2 | | | | 26.2 | 26.2 | | 26.2 | | | | | | | | | | | $\epsilon$ |
| **EXPR** | 27 | 27 | | | | | | | | 27 | | | | | | | | | | | | | | | | |
| **EXPR\_TAIL** | | | | | $\epsilon$ | | | | | | $\epsilon$ | | $\epsilon$ | $\epsilon$ | $\epsilon$ | 28 | 28 | 28 | 28 | 28 | 28 | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ |
| **NUMEXPR** | 29 | 29 | | | | | | | | 29 | | | | | | | | | | | | | | | | |
| **NUMEXPR\_TAIL** | | | | | $\epsilon$ | | | | | | $\epsilon$ | | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | 30 | 30 | $\epsilon$ | $\epsilon$ | $\epsilon$ |
| **TERM** | 31 | 31 | | | | | | | | 31 | | | | | | | | | | | | | | | | |
| **TERM\_TAIL** | | | | | $\epsilon$ | | | | | | $\epsilon$ | | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | 32 | 32 | $\epsilon$ |
| **FACTOR** | 33.3 | 33.1 | | | | | | | | 33.2 | | | | | | | | | | | | | | | | |
| **FACTOR\_TAIL** | | | | | $\epsilon$ | | | | | 34 | $\epsilon$ | | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ | $\epsilon$ |

---

## 4. Exemplo de Aplicação da Tabela (Rastreamento da Pilha)

**String de Teste (Entrada):** `def main ( ) { int x ; x = 1 ; return x ; } $`

| Pilha | Entrada (Próximo Token) | Ação | Produção Aplicada |
| :--- | :--- | :--- | :--- |
| `[$, MAIN]` | `def` | $M[MAIN, def] \rightarrow FLIST$ | 1. $MAIN \rightarrow FLIST$ |
| `[$, FLIST]` | `def` | $M[FLIST, def] \rightarrow FDEF\ FLIST\_TAIL$ | 2. $FLIST \rightarrow FDEF\ FLIST\_TAIL$ |
| `[$, FLIST\_TAIL, FDEF]` | `def` | $M[FDEF, def] \rightarrow def\ id\ LPAREN\ PARLIST\ RPAREN\ LBRACE\ STMTLIST\ RBRACE$ | 4. $FDEF \rightarrow \dots$ |
| `[$, \dots, def]` | `def` | **MATCH** `def` | - |
| `[$, \dots, id]` | `main` | **MATCH** `id` | - |
| `[$, \dots, LPAREN]` | `(` | **MATCH** `LPAREN` | - |
| `[$, \dots, PARLIST]` | `)` | $M[PARLIST, RPAREN] \rightarrow \epsilon$ | 5. $PARLIST \rightarrow \epsilon$ |
| `[$, \dots, RPAREN]` | `)` | **MATCH** `RPAREN` | - |
| `[$, \dots, LBRACE]` | `{` | **MATCH** `LBRACE` | - |
| `[$, \dots, STMTLIST]` | `int` | $M[STMTLIST, int] \rightarrow STMT\ STMTLIST$ | 7. $STMTLIST \rightarrow STMT\ STMTLIST$ |
| `[$, \dots, STMT]` | `int` | $M[STMT, int] \rightarrow int\ VARLIST\ SEMI$ | 8. $STMT \rightarrow int\ VARLIST\ SEMI$ |
| `[$, \dots, int]` | `int` | **MATCH** `int` | - |
| `[$, \dots, VARLIST]` | `id` (`x`) | $M[VARLIST, id] \rightarrow id\ VARLIST\_TAIL$ | 15. $VARLIST \rightarrow \dots$ |
| `[$, \dots, id]` | `x` | **MATCH** `id` | - |
| `[$, \dots, VARLIST\_TAIL]`| `;` | $M[VARLIST\_TAIL, SEMI] \rightarrow \epsilon$ | 16. $VARLIST\_TAIL \rightarrow \epsilon$ |
| `[$, \dots, SEMI]` | `;` | **MATCH** `SEMI` | - |
| `[$, \dots, STMTLIST]` | `id` (`x`) | $M[STMTLIST, id] \rightarrow STMT\ STMTLIST$ | 7. $STMTLIST \rightarrow STMT\ STMTLIST$ |
| `[$, \dots, STMT]` | `id` (`x`) | $M[STMT, id] \rightarrow ATRIBST\ SEMI$ | 9. $STMT \rightarrow ATRIBST\ SEMI$ |
| `[$, \dots, ATRIBST]` | `x` | $M[ATRIBST, id] \rightarrow id\ ASSIGN\ ATRIBST\_TAIL$ | 17. $ATRIBST \rightarrow \dots$ |
| `[$, \dots, id]` | `x` | **MATCH** `id` | - |
| `[$, \dots, ASSIGN]` | `=` | **MATCH** `ASSIGN` | - |
| `[$, \dots, ATRIBST\_TAIL]`| `num` (`1`) | $M[ATRIBST\_TAIL, num] \rightarrow EXPR$ | 18. $ATRIBST\_TAIL \rightarrow EXPR$ |
| `[$, \dots, EXPR]` | `1` | $\dots$ | $\dots$ (Consumo de `1` via expressões) |
| `[$, \dots, EXPR\_TAIL]` | `;` | $M[EXPR\_TAIL, SEMI] \rightarrow \epsilon$ | 28. $EXPR\_TAIL \rightarrow \epsilon$ |
| `[$, \dots, SEMI]` | `;` | **MATCH** `SEMI` | - |
| `[$, \dots, STMTLIST]` | `return` | $M[STMTLIST, return] \rightarrow STMT\ STMTLIST$ | 7. $STMTLIST \rightarrow STMT\ STMTLIST$ |
| `[$, \dots, STMT]` | `return` | $M[STMT, return] \rightarrow RETURNST\ SEMI$ | 11. $STMT \rightarrow RETURNST\ SEMI$ |
| `[$, \dots, RETURNST]` | `return` | $M[RETURNST, return] \rightarrow return\ RETURNST\_TAIL$ | 23. $RETURNST \rightarrow \dots$ |
| `[$, \dots, return]` | `return` | **MATCH** `return` | - |
| `[$, \dots, RETURNST\_TAIL]`| `id` (`x`) | $M[RETURNST\_TAIL, id] \rightarrow EXPR$ | 24. $RETURNST\_TAIL \rightarrow EXPR$ |
| `[$, \dots, EXPR]` | `x` | $\dots$ | $\dots$ (Consumo de `x` via expressões) |
| `[$, \dots, EXPR\_TAIL]` | `;` | $M[EXPR\_TAIL, SEMI] \rightarrow \epsilon$ | 28. $EXPR\_TAIL \rightarrow \epsilon$ |
| `[$, \dots, SEMI]` | `;` | **MATCH** `SEMI` | - |
| `[$, \dots, STMTLIST]` | `}` | $M[STMTLIST, RBRACE] \rightarrow \epsilon$ | 7. $STMTLIST \rightarrow \epsilon$ |
| `[$, \dots, RBRACE]` | `}` | **MATCH** `RBRACE` | - |
| `[$, FLIST\_TAIL]` | `$` | $M[FLIST\_TAIL, $] \rightarrow \epsilon$ | 3. $FLIST\_TAIL \rightarrow \epsilon$ |
| `[$, $]` | `$` | **SUCESSO** | - |

A string foi **aceita** pela gramática LL(1) e pela tabela de reconhecimento sintático.