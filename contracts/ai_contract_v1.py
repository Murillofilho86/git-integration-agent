class AIContractV1:

    REQUIRED_FIELDS = [
        "estrategia_recomendada",
        "nivel_de_risco",
        "possiveis_conflitos",
        "complexidade",
        "plano_de_execucao",
        "arquivos_prioritarios",
        "ordem_recomendada_de_implementacao"
    ]

    FIELD_TYPES = {
        "estrategia_recomendada": dict,
        "nivel_de_risco": dict,
        "possiveis_conflitos": dict,
        "complexidade": dict,
        "plano_de_execucao": list,
        "arquivos_prioritarios": list,
        "ordem_recomendada_de_implementacao": list
    }