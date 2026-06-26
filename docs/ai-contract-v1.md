# AI Contract v1

## Objetivo

Este documento define o contrato oficial entre qualquer modelo de IA e o Git Integration Agent.

Todo modelo (Claude, OpenAI, Gemini, Ollama, etc.) deve produzir um JSON compatível com esta especificação.

---

# Version

```json
{
    "contract_version": "1.0"
}
```

---

# Estrutura

## estrategia_recomendada

**Tipo**

object

**Obrigatório**

Sim

**Campos**

| Campo | Tipo |
|--------|------|
| estrategia | string |
| nome | string |
| descricao | string |
| alinhado_com_heuristica | boolean |
| confianca | number |

---

## nivel_de_risco

**Tipo**

object

**Obrigatório**

Sim

**Campos**

| Campo | Tipo |
|--------|------|
| nivel | string |
| score | number |
| fatores | array[string] |

---

## possiveis_conflitos

**Tipo**

object

**Obrigatório**

Sim

**Campos**

| Campo | Tipo |
|--------|------|
| alta_probabilidade | array[string] |
| media_probabilidade | array[string] |
| conflitos_semanticos_e_nao_textuais | array[string] |

---

## complexidade

**Tipo**

object

**Obrigatório**

Sim

**Campos**

| Campo | Tipo |
|--------|------|
| nivel | string |
| estimativa_esforco | string |
| drivers | array[string] |

---

## plano_de_execucao

**Tipo**

array[string]

**Obrigatório**

Sim

---

## arquivos_prioritarios

**Tipo**

array[string]

**Obrigatório**

Sim

---

## ordem_recomendada_de_implementacao

**Tipo**

array

**Obrigatório**

Sim

Cada item deve possuir:

| Campo | Tipo |
|--------|------|
| etapa | number |
| lote | string |
| arquivos_chave | array[string] |
| motivo | string |

---

## observacoes

**Tipo**

array[string]

**Obrigatório**

Não

---

# Compatibilidade

O ClaudeResponseParser deve validar este contrato.

Mudanças incompatíveis exigem incremento da versão do contrato.

Exemplo:

- v1.0
- v1.1
- v2.0

---

# Objetivo

O restante do Git Integration Agent nunca deve depender diretamente do formato retornado pela IA.

Toda integração deve ocorrer através deste contrato.