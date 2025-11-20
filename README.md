# 🚀 Analisador Léxico e Sintático (Linguagem LSI-2025-2)

Este projeto implementa um **Analisador Léxico** e um **Analisador Sintático Preditivo LL(1)** para a linguagem LSI-2025-2, cobrindo as Partes 1, 2 e 3 do trabalho.

## ⚙️ Pré-requisitos e Setup

O projeto foi desenvolvido em Python 3 e é compatível com sistemas operacionais GNU/Linux.

* **Python:** Versão 3.12.3 ou superior.

### 📁 Estrutura do Projeto (Organização dos Arquivos)

A estrutura de diretórios do projeto é a seguinte:

* `.` (Raiz do Projeto)
    * `README.md`
    * `run.sh` (Script de execução)
    * `docs/`
        * `parte2.md` (Documentação da Gramática, FIRST, FOLLOW e Tabela LL(1))
    * `src/` (Código Fonte)
        * `lsi_lexer.py` (Analisador Léxico - **Parte 1**)
        * `lsi_parser.py` (Analisador Sintático LL(1) - **Partes 2 e 3**)
    * `tests/` (Arquivos de Teste)
        * `correct.lsi` (Programa válido, $\ge 50$ linhas)
        * `lex_error.lsi` (Programa com erro léxico)
        * `syn_error_1.lsi` (Erro sintático: falta ';')
        * `syn_error_2.lsi` (Erro sintático: falta ')' em `if`)
        * `syn_error_3.lsi` (Erro sintático: falta '(' em `def`)

---

## 💻 Instruções de Execução

O `lsi_parser.py` integra o analisador léxico, realizando a análise completa de um arquivo de entrada (léxica e sintática) em uma única execução.

### **Execução (Usando `run.sh`)**

O script `run.sh` simplifica a execução do analisador no ambiente Linux:

```bash
./run.sh <caminho_para_arquivo.lsi>

### **Exemplos de Uso**

O analisador será executado em modo de depuração, mostrando a lista de tokens, o log da pilha e o resultado final da análise.

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| Teste Completo (Sucesso) | `tests/correct.lsi` | `./run.sh tests/correct.lsi` | "Parse OK." e Tabela de Símbolos |
| Captura de Erro Léxico | `tests/lex_error.lsi` | `./run.sh tests/lex_error.lsi` | Mensagem "=== ERRO LÉXICO ===" |
| Captura de Erro Sintático 1 | `tests/syn_error_1.lsi` | `./run.sh tests/syn_error_1.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Esperado ';', encontrado 'id') |
| Captura de Erro Sintático 2 | `tests/syn_error_2.lsi` | `./run.sh tests/syn_error_2.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Esperado ')', encontrado '{') |
| Captura de Erro Sintático 3 | `tests/syn_error_3.lsi` | `./run.sh tests/syn_error_3.lsi` | Mensagem "=== ERRO SINTÁTICO ===" (ex: Esperado '(', encontrado '{') |