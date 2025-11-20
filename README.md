# 🚀 Analisador Léxico e Sintático (Linguagem LSI-2025-2)

Este projeto implementa um **Analisador Léxico** e um **Analisador Sintático Preditivo LL(1)** para a linguagem LSI-2025-2, cobrindo as Partes 1, 2 e 3 do trabalho.

## ⚙️ Pré-requisitos e Setup

O projeto foi desenvolvido em Python 3 e é compatível com sistemas operacionais GNU/Linux.

* **Python:** Versão 3.12.3 ou superior.

### 📁 Estrutura do Projeto (Organização dos Arquivos)

A estrutura de diretórios do projeto é a seguinte:

* `.` (Raiz do Projeto)
    * `README.md` (Este arquivo)
    * `run.sh` (Script de execução)
    * `docs/`
        * `parte2.md` (Documentação da Gramática, FIRST, FOLLOW e Tabela LL(1))
        * `README_LEXER.md` (Documentação do Funcionamento do Lexer)
        * `README_PARSER.md` (Documentação da Funcionamento do Parser)
        * `README_TESTS.md` (Documentação da Funcionamento dos Testes)
    * `src/` (Código Fonte)
        * `lsi_lexer.py` (Analisador Léxico - **Parte 1**)
        * `lsi_parser.py` (Analisador Sintático LL(1) - **Partes 2 e 3**)
    * `tests/` (Arquivos de Teste)
        * `correct.lsi` (Programa válido, versão base)
        * `correct_50_lines.lsi` (Programa válido, versão mais longa para teste de estresse)
        * `lex_error.lsi` (Programa com erro léxico)
        * `syn_error_1.lsi` (Erro sintático: Tipo 2 - No Rule, ex: `;` ausente ou token inesperado em expressão)
        * `syn_error_1_15_lines.lsi` (Versão do Erro Sintático 1 com 15 linhas)
        * `syn_error_2.lsi` (Erro sintático: Tipo 1 - Terminal Mismatch, ex: `)` ausente em `if`)
        * `syn_error_2_15_lines.lsi` (Versão do Erro Sintático 2 com 15 linhas)
        * `syn_error_3.lsi` (Erro sintático: Tipo 2 - No Rule, ex: `}` ou outro token estrutural ausente)
        * `syn_error_3_15_lines.lsi` (Versão do Erro Sintático 3 com 15 linhas)

---

## 💻 Instruções de Execução

O `lsi_parser.py` integra o analisador léxico, realizando a análise completa de um arquivo de entrada (léxica e sintática) em uma única execução.

### **Execução (Usando `run.sh`)**

O script `run.sh` simplifica a execução do analisador no ambiente Linux

## Como Executar

1. Criar virtualenv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

2. Tornar run.sh executável:
    ```bash
    chmod +x run.sh

Para executar a análise de um arquivo de teste, utilize o script `run.sh` seguido do caminho para o arquivo LSI:



```bash
./run.sh <caminho_para_arquivo.lsi>
```

### **Exemplos de Uso**

O analisador será executado em modo de depuração, mostrando a lista de tokens, o log da pilha e o resultado final da análise.

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| Teste Completo (Sucesso) | `tests/correct.lsi` | `./run.sh tests/correct.lsi` | "Parse OK." e Tabela de Símbolos |
| Teste Completo (50 linhas) | `tests/correct_50_lines.lsi` | `./run.sh tests/correct_50_lines.lsi` | "Parse OK." e Tabela de Símbolos |
| Captura de Erro Léxico | `tests/lex_error.lsi` | `./run.sh tests/lex_error.lsi` | Mensagem "=== ERRO LÉXICO ===" (Erro léxico em linha: 4 Coluna: 6 — caractere inválido '$') |
| Captura de Erro Sintático 1 (Erro Tipo 2: No Rule) | `tests/syn_error_1.lsi` | `./run.sh tests/syn_error_1.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Erro sintático: não há regra (TERM, RPAREN)) |
| Captura de Erro Sintático 1 (15 linhas) | `tests/syn_error_1_15_lines.lsi` | `./run.sh tests/syn_error_1_15_lines.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Erro sintático: não há regra (FACTOR_TAIL, int)) |
| Captura de Erro Sintático 2 (Erro Tipo 2: No Rule) | **`tests/syn_error_2.lsi`** | `./run.sh tests/syn_error_2.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Erro sintático: não há regra (NUMEXPR, RPAREN)) |
| Captura de Erro Sintático 2 (15 linhas) | `tests/syn_error_2_15_lines.lsi` | `./run.sh tests/syn_error_2_15_lines.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Esperado 'EQUAL', encontrado 'NUM') |
| Captura de Erro Sintático 3 (Erro Tipo 2: No Rule) | `tests/syn_error_3.lsi` | `./run.sh tests/syn_error_3.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Erro sintático: não há regra (TERM_TAIL, return)) |
| Captura de Erro Sintático 3 (15 linhas) | `tests/syn_error_3_15_lines.lsi` | `./run.sh tests/syn_error_3_15_lines.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: EErro sintático: não há regra (STMTLIST, $)) |
