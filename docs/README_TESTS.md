# 🧪 README — Testes do Compilador LSI

Este documento descreve os arquivos de teste localizados no diretório `tests/` e explica como executá-los usando o *script* principal do projeto.

-----

## 🚀 Como Rodar os Testes

Todos os testes são executados usando o *script* principal `run.sh`, que invoca sequencialmente o Lexer e o Parser.

### 📝 Comando de Execução

```bash
./run.sh <caminho_para_arquivo.lsi>
```

O analisador será executado em modo de depuração, mostrando a lista de tokens, o log da pilha e o resultado final da análise.

-----

## 🎯 Descrição dos Casos de Teste

Seus testes são categorizados em Sucesso (Parse OK), Erro Léxico e Erro Sintático.

### 1\. Testes de Sucesso (Parse OK)

Estes arquivos contêm código LSI sintaticamente válido e devem passar pelas fases Léxica e Sintática com sucesso.

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| **Teste Básico** | `tests/correct.lsi` | `./run.sh tests/correct.lsi` | **"Parse OK."** e Tabela de Símbolos |
| **Teste de Estresse** | `tests/correct_50_lines.lsi` | `./run.sh tests/correct_50_lines.lsi` | **"Parse OK."** e Tabela de Símbolos |

-----

### 2\. Teste de Erro Léxico

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| **Caractere Inválido** | `tests/lex_error.lsi` | `./run.sh tests/lex_error.lsi` | Mensagem **"=== ERRO LÉXICO ==="** (ex: Erro léxico em linha: 4 Coluna: 6 — caractere inválido '$') |

-----

### 3\. Testes de Erro Sintático

Estes testes validam a capacidade do analisador LL(1) de identificar e classificar as falhas de *parsing* com base na Tabela LL(1).

#### Erro Tipo 1: Terminal Mismatch (Esperado: T, Encontrado: t)

Este é o único caso que resulta em **Mismatch** (o topo da pilha é um terminal que não corresponde ao token de entrada).

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| **Erro Mismatch Explícito** | `tests/syn_error_2_15_lines.lsi` | `./run.sh tests/syn_error_2_15_lines.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Esperado 'EQUAL', encontrado 'NUM') |

#### Erro Tipo 2: No Rule (Não há Regra na Tabela LL(1))

Estes casos ocorrem quando o topo da pilha é um Não-Terminal ($A$) e o terminal de entrada ($t$) não possui uma produção definida na célula $(A, t)$.

| Objetivo | Arquivo de Teste | Comando de Exemplo | Saída Esperada (Resumo) |
| :--- | :--- | :--- | :--- |
| **Erro em Expressão (TERM)** | `tests/syn_error_1.lsi` | `./run.sh tests/syn_error_1.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Erro sintático: não há regra (TERM, RPAREN)) |
| **Erro em Expressão (FACTOR)** | `tests/syn_error_1_15_lines.lsi` | `./run.sh tests/syn_error_1_15_lines.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Erro sintático: não há regra (FACTOR\_TAIL, int)) |
| **Erro em Expressão Incompleta** | `tests/syn_error_2.lsi` | `./run.sh tests/syn_error_2.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Erro sintático: não há regra (NUMEXPR, RPAREN)) |
| **Erro Estrutural (Meio da Função)** | `tests/syn_error_3.lsi` | `./run.sh tests/syn_error_3.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Erro sintático: não há regra (TERM\_TAIL, return)) |
| **Erro Estrutural (EOF)** | `tests/syn_error_3_15_lines.lsi` | `./run.sh tests/syn_error_3_15_lines.lsi` | Mensagem **"=== ERRO SINTÁTICO ==="** (ex: Erro sintático: não há regra (STMTLIST, $)) |