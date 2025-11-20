# README — Analisador Léxico (Lexer)

Arquivo: `src/lsi_lexer.py`

O `lsi_lexer.py` é responsável pela primeira fase da compilação: a análise léxica. Ele transforma a *string* de código-fonte em uma sequência de **tokens** reconhecíveis pela gramática da linguagem LSI.

***

## ⚙️ Definição e Categorias de Tokens

O Lexer reconhece a seguinte lista fixa de tokens, que são categorizados internamente para simplificar o processo de `maximal munch`:

| Categoria | Tokens (Lexemas) | Tipo de Token |
| :--- | :--- | :--- |
| **Palavras-Chave** (`KEYWORDS`) | `int`, `if`, `else`, `def`, `print`, `return` | DEF, INT, IF, ELSE, PRINT, RETURN |
| **Operadores Multi-Caractere** | `<=`, `>=`, `==`, `!=` | LE, GE, EQ, NE |
| **Operadores Simples** | `<`, `>` | LT, GT |
| **Tokens de Caractere Único** | `+`, `-`, `*`, `/`, `=`, `(`, `)`, `{`, `}`, `,`, `;` | PLUS, MINUS, TIMES, DIV, EQUAL, LPAREN, RPAREN, LBRACE, RBRACE, COMMA, SEMI |
| **Literais** | Qualquer sequência de dígitos. | NUM |
| **Identificadores** | Qualquer sequência que comece com letra ou `_`. | ID |
| **Fim de Arquivo** | `$` | EOF |

Todos os tokens são representados pela classe `Token` (`typ`, `lexeme`, `line`, `col`).

***

## 🧠 Mecanismo de Análise (FSM e Maximal Munch)

O analisador opera como uma **Máquina de Estados Finitos (FSM)** implícita, lendo a entrada **caractere por caractere** (`peek` e `advance`) e seguindo uma ordem estrita de precedência para tokenizar:

1.  **Pré-Processamento:** O método `skip_space_and_comments` remove:
    * **Espaços em branco:** Quebras de linha, tabulações, etc.
    * **Comentários de Linha Única:** O Lexer ignora qualquer texto que comece com `//` até o final da linha.

2.  **Maximal Munch:** O Lexer adere à regra de **`maximal munch`**, priorizando a captura do token mais longo possível. Isso é crucial para operadores:
    * **Prioridade 1 (Operadores Multi-Caractere):** Ele tenta identificar operadores de dois caracteres (`<=`, `!=`, etc.) antes de tratar seus componentes como tokens de caractere único. Por exemplo, `i <= j` é tokenizado como `LE`, e não `LT` seguido de `EQUAL`.
    * **Prioridade 2 (Identificadores e Palavras-Chave):** Uma vez que uma sequência de caracteres alfanuméricos é lida, o Lexer verifica se ela é uma das palavras-chave reservadas (`KEYWORDS`). Caso contrário, é classificada como um **ID**.

3.  **Números e Outros Tokens:** Sequências de dígitos são lidas como **NUM**s. Por fim, os operadores de caractere único e a pontuação simples são tratados.

***

## 🗃️ Tabela de Símbolos

O Lexer mantém uma **Tabela de Símbolos** (`self.symbol_table`), que é um dicionário que mapeia o lexema para um objeto de metadados.

* **Pré-Carregamento:** A tabela é inicializada com todas as **Palavras-Chave** da linguagem, marcando seu `kind` como `"keyword"`.
* **Identificadores (`ID`):** Sempre que um novo identificador é encontrado, ele é automaticamente inserido na tabela com `kind: "id"`.
* **Propósito:** Embora o Lexer use a tabela apenas para distinguir Identificadores de Palavras-Chave, essa estrutura é essencial para as fases subsequentes de Análise Semântica, onde informações adicionais (tipo, escopo, etc.) serão anexadas.

***

## 🛑 Saída e Tratamento de Erros

* **Saída:** O método principal `tokenize_all` retorna uma tupla contendo a **lista completa de tokens** (incluindo o token `EOF:$` no final) e a **tabela de símbolos** finalizada.
* **Erros:** O Lexer é robusto apenas para o erro de **caractere inválido**.
    * Em caso de um caractere que não inicia nenhum token válido (ex: `@`, `!`), uma exceção `LexerError` é lançada.
    * A mensagem de erro é formatada para incluir a localização exata: `Erro léxico em linha: L Coluna: C — caractere inválido 'x'`.
    * O fluxo de execução é encerrado imediatamente.
* **Execução:** O Lexer é instanciado e utilizado pelo `src/lsi_parser.py` para fornecer o fluxo de tokens para o Analisador Sintático.