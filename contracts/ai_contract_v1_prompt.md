# AI Contract v1

Sua resposta deve seguir rigorosamente este contrato.

## Regras obrigatórias

- Retorne exclusivamente um JSON válido.
- Não utilize Markdown.
- Não utilize blocos ```json.
- Não escreva comentários.
- Não escreva explicações.
- Não adicione texto antes ou depois do JSON.
- Não altere os nomes das propriedades.
- Não adicione prefixos numéricos.
- Não renomeie propriedades.
- Caso alguma informação não exista, utilize listas vazias ou strings vazias.

## Estrutura obrigatória

```json
{
    "estrategia_recomendada": {
        "estrategia": "",
        "nome": "",
        "descricao": "",
        "alinhado_com_heuristica": true,
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
    ]
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
    ],
    "observacoes": []
}
```