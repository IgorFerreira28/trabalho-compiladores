# README — Analisador Sintático (Parser LL(1))

Arquivo: `src/lsi_parser.py`

O `lsi_parser.py` é responsável por verificar a correção estrutural (sintática) do código-fonte, garantindo que a sequência de tokens obedeça à **Gramática LL(1)** definida.

***

## 🧩 Componentes Chave

O Parser é dividido em três módulos principais que garantem a conformidade com o método LL(1):

1.  ### Definição Formal da Linguagem
    * **Terminais (`TERMINALS`):** Conjunto de todos os símbolos terminais reconhecidos pela gramática. Estes são mapeados diretamente dos tipos de tokens do Lexer, incluindo palavras-chave (ex: `"int"`, `"def"`) e operadores (ex: `"PLUS"`, `"EQUAL"`) e o símbolo de Fim de Arquivo (`$`).
    * **Gramática (`GRAMMAR`):** Dicionário que mapeia cada **Não-Terminal** (NT) para uma lista de suas possíveis produções (regras).
    * **Mapeamento (`LEX_TO_GR`):** Garante que os tipos de tokens produzidos pelo Lexer (ex: `"ID"`, `"DEF"`) sejam traduzidos corretamente para os símbolos terminais usados na Gramática (ex: `"id"`, `"def"`).

2.  ### Geração de Conjuntos e Tabela (Pré-Análise)
    * **`compute_first()`:** Calcula o conjunto $\text{FIRST}(A)$ para cada Não-Terminal $A$, determinando quais terminais podem iniciar uma sequência derivada de $A$.
    * **`compute_follow(FIRST)`:** Calcula o conjunto $\text{FOLLOW}(A)$ para cada Não-Terminal $A$, determinando quais terminais podem seguir $A$ no corpo de uma produção. O símbolo $\$$ é adicionado ao $\text{FOLLOW}(\text{MAIN})$.
    * **`build_table(FIRST, FOLLOW)`:** Constrói a **Tabela de Análise LL(1)**. Esta tabela é um mapeamento de `(Não-Terminal, Terminal) -> Regra de Produção`, seguindo as regras de construção LL(1).

3.  ### Algoritmo de Parsing (A Análise)
    * O método `parse()` implementa o algoritmo preditivo usando uma **pilha** e o *stream* de tokens de entrada.

***

## 🛠️ Detalhes do Algoritmo de Parsing

O parser utiliza o **Algoritmo Predutivo Não-Recursivo** com a tabela e opera em um *loop* contínuo até que a pilha e o *stream* de entrada contenham apenas o marcador de Fim de Arquivo (`$`).

1.  **Inicialização:**
    * A pilha é inicializada com o símbolo de Fim de Arquivo (`$`) e o símbolo inicial da gramática (`MAIN`).
    * O *input pointer* (`ip`) aponta para o primeiro token da *stream* de terminais.
2.  **Processamento da Pilha:** Em cada passo, o elemento no topo da pilha (`top`) é comparado com o token de entrada atual (`cur`):
    * **Aparar Sucesso (`$` e `$`):** Se `top` é `$` e `cur` é `$`, o *parsing* é concluído com sucesso (**"Parse OK."**).
    * **Match de Terminal:** Se `top` é um **Terminal** e `top == cur`, o terminal é consumido: `top` é removido da pilha e o *input pointer* (`ip`) avança.
    * **Expansão de Não-Terminal:** Se `top` é um **Não-Terminal**, a Tabela LL(1) é consultada para o par `(top, cur)`:
        * Se uma **Regra** $R$ for encontrada, $R$ substitui `top` na pilha (em ordem reversa).
        * Se $R$ for $\text{epsilon}$ ($\epsilon$), `top` é simplesmente removido.

***

## 🛑 Tratamento de Erros Sintáticos

O Parser detecta e reporta dois tipos de erros sintáticos, parando a análise imediatamente:

1.  ### Erro Tipo 1: Terminal Mismatch
    Ocorre quando o **topo da pilha é um Terminal ($T$)** e ele **não coincide** com o token de entrada ($t$).
    > **Mensagem:** `Esperado 'T', encontrado 't'.`
    > **Exemplo:** A pilha espera um `SEMI` (`;`), mas encontra um `id`.

2.  ### Erro Tipo 2: No Rule (Error Cell)
    Ocorre quando o **topo da pilha é um Não-Terminal ($A$)** e o par `(A, t)` não possui nenhuma regra definida na Tabela LL(1). Isso significa que, sintaticamente, o terminal $t$ é ilegal neste ponto do código para o não-terminal $A$.
    > **Mensagem:** `Erro sintático: não há regra (A, t)`
    > **Exemplo:** A pilha espera por `FACTOR_TAIL` ($\mathbf{A}$), mas o *lookahead* é `int` ($\mathbf{t}$), o que não está nos $\text{FIRST}(\text{FACTOR\_TAIL})$ nem $\text{FOLLOW}(\text{FACTOR\_TAIL})$.

***

## 🔬 Debug e Teste

* **Exibição de Conjuntos:** O parser calcula `FIRST`, `FOLLOW` e a Tabela LL(1) na inicialização, permitindo que estas estruturas sejam inspecionadas para depuração da gramática.
* **Trace de Pilha:** Durante a execução de `parse()`, o parser imprime o estado do topo da pilha e do token atual (input pointer) a cada passo: `STACK TOP:X | CURRENT TOKEN:Y`.