# AI Contract v1

Sua resposta será processada automaticamente por outro sistema Python.

Não existe intervenção humana entre sua resposta e o processamento.

Qualquer violação deste contrato tornará toda a execução inválida.

---

## Contrato de Resposta

Considere este contrato como obrigatório.

Sua resposta será consumida diretamente por:

```python
json.loads(resposta)
```

utilizando Python 3.14.

Caso sua resposta não possa ser carregada diretamente por `json.loads()`, toda a execução será considerada uma falha.

Nunca faça aproximações.

Nunca altere a estrutura definida neste contrato.

Nunca simplifique o formato solicitado.

Sempre produza exatamente a estrutura especificada.

---

## Regras Gerais

* Retorne exclusivamente um JSON válido.
* Nunca utilize Markdown.
* Nunca utilize blocos `ou`json.
* Nunca escreva explicações.
* Nunca escreva comentários.
* Nunca escreva texto antes do JSON.
* Nunca escreva texto após o JSON.
* Não omita nenhuma propriedade obrigatória.
* Nunca substitua objetos por texto livre.
* Caso alguma informação não possa ser determinada, utilize:

  * String vazia ("")
  * Lista vazia ([])
  * Objeto vazio ({})

---

## Estrutura Obrigatória

```json
{
    "estrategia_recomendada": {
        "estrategia": "",
        "nome": "",
        "descricao": "",
        "alinhado_com_heuristica": false,
        "confianca": 0.0
    },
    "nivel_de_risco": {
        "nivel": "",
        "score": 0.0,
        "fatores": []
    },
    "possiveis_conflitos": {
        "alta_probabilidade": [],
        "media_probabilidade": [],
        "conflitos_semanticos_e_nao_textuais": []
    },
    "complexidade": {
        "nivel": "",
        "estimativa_esforco": "",
        "drivers": []
    },
    "plano_de_execucao": [
        {
            "etapa": 1,
            "titulo": "",
            "acoes": []
        }
    ],
    "arquivos_prioritarios": [
        {
            "arquivo": "",
            "motivo": "",
            "prioridade": ""
        }
    ],
    "ordem_recomendada_de_implementacao": [
        {
            "etapa": 1,
            "lote": "",
            "motivo": "",
            "arquivos_chave": []
        }
    ]
}
```

---

## Regras dos Campos

### estrategia_recomendada

Descreva a estratégia mais adequada para integrar a branch de origem na branch de destino.

---

### nivel_de_risco

Avalie o risco global da integração.

Inclua obrigatoriamente:

* nível
* score
* fatores

---

### possiveis_conflitos

Liste:

* arquivos com alta probabilidade de conflito;
* arquivos com média probabilidade;
* conflitos semânticos.

---

### complexidade

Avalie:

* nível;
* estimativa de esforço;
* drivers da complexidade.

---

### plano_de_execucao

Lista ordenada de etapas necessárias para executar a integração.

Cada item deve conter:

* etapa
* titulo
* acoes

---

### arquivos_prioritarios

Liste os arquivos mais importantes para iniciar a integração.

Cada item deve conter:

* arquivo
* motivo
* prioridade

Prioridades permitidas:

* ALTA
* MEDIA
* BAIXA

---

### ordem_recomendada_de_implementacao

Defina a ordem lógica para implementação.

Cada item deve conter:

* etapa
* lote
* motivo
* arquivos_chave

---

## Regras de Produção

Nunca utilize Markdown.

Nunca utilize blocos de código.

Nunca utilize comentários.

Nunca escreva explicações.

Nunca escreva observações.

Nunca escreva mensagens de confirmação.

Nunca escreva notas.

Nunca escreva texto antes do primeiro caractere '{'.

Nunca escreva texto após o último caractere '}'.

Retorne exclusivamente o JSON.

---

## Regras de JSON

O JSON deve seguir rigorosamente a RFC 8259.

Utilize exclusivamente aspas duplas.

Nunca utilize trailing commas.

Nunca utilize comentários.

Nunca utilize NaN.

Nunca utilize Infinity.

Nunca utilize Undefined.

Nunca utilize propriedades duplicadas.

Nunca utilize chaves duplicadas.

Nunca utilize valores não compatíveis com JSON.

O JSON deve ser aceito diretamente por:

```python
json.loads(resposta)
```

utilizando Python 3.14.

---

## Autovalidação Obrigatória

Antes de responder:

1. Gere toda a resposta.

2. Faça uma revisão completa do JSON.

3. Valide mentalmente que a resposta pode ser carregada diretamente por:

```python
json.loads(resposta)
```

utilizando Python 3.14.

Verifique obrigatoriamente:

* existência de vírgulas antes de '}'
* existência de vírgulas antes de ']'
* chaves abertas e fechadas corretamente
* colchetes abertos e fechados corretamente
* aspas duplas em todas as propriedades
* aspas duplas em todas as strings
* ausência de caracteres inválidos
* ausência de propriedades duplicadas
* ausência de comentários
* ausência de markdown
* ausência de texto antes do primeiro '{'
* ausência de texto após o último '}'

Caso qualquer validação falhe:

* corrija toda a resposta;
* execute novamente todas as validações;
* somente continue quando todas forem aprovadas.

Nunca mostre essa validação.

---

## Critério de Liberação

A resposta somente poderá ser enviada quando TODAS as condições abaixo forem verdadeiras:

* O JSON é válido.
* O JSON pode ser carregado por `json.loads()` do Python.
* Todas as propriedades obrigatórias existem.
* Todos os objetos seguem exatamente a estrutura definida.
* Todas as listas possuem o formato esperado.
* Não existe texto antes do JSON.
* Não existe texto após o JSON.
* Nenhuma regra deste contrato foi violada.

Caso exista qualquer dúvida, nunca simplifique a resposta.

Reavalie completamente o JSON antes de enviá-lo.

Somente após todas as validações serem aprovadas retorne o JSON final.
