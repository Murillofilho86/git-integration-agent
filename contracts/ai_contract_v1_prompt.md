# AI Contract v1

Sua resposta será processada automaticamente por outro sistema.

Qualquer divergência deste contrato tornará a resposta inválida.

## Regras Gerais

- Retorne exclusivamente um JSON válido.
- Nunca utilize Markdown.
- Nunca utilize blocos ```json.
- Nunca escreva explicações.
- Nunca escreva comentários.
- Nunca escreva texto antes ou depois do JSON.
- Não omita nenhuma propriedade obrigatória.
- Caso alguma informação não possa ser determinada, utilize:
  - String vazia ("")
  - Lista vazia ([])
  - Objeto vazio ({})
- Nunca substitua objetos por texto livre.

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

## Regras dos Campos

### estrategia_recomendada

Descreva a estratégia mais adequada para integrar a branch de origem na branch de destino.

### nivel_de_risco

Avalie o risco global da integração.

Inclua:

- nível
- score
- fatores

### possiveis_conflitos

Liste:

- arquivos com alta probabilidade de conflito;
- arquivos com média probabilidade;
- conflitos semânticos.

### complexidade

Avalie:

- nível;
- estimativa de esforço;
- fatores que justificam a complexidade.

### plano_de_execucao

Lista ordenada de etapas necessárias para executar a integração.

Cada item deve conter:

- etapa
- titulo
- acoes

### arquivos_prioritarios

Liste os arquivos mais importantes para iniciar a integração.

Cada item deve conter:

- arquivo
- motivo
- prioridade

Prioridade sugerida:

- ALTA
- MEDIA
- BAIXA

### ordem_recomendada_de_implementacao

Defina a ordem lógica para implementação.

Cada item deve conter:

- etapa
- lote
- motivo
- arquivos_chave

## Validação Final

Antes de finalizar sua resposta, valide internamente que:

- O JSON é válido.
- Todas as propriedades obrigatórias existem.
- Todos os objetos possuem a estrutura definida.
- Todas as listas possuem objetos no formato correto.
- Não existe texto antes ou depois do JSON.