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

    SCHEMA = {
        "estrategia_recomendada": {
            "type": dict,
            "required": [
                "estrategia",
                "nome",
                "descricao",
                "alinhado_com_heuristica",
                "confianca"
            ]
        },
        "nivel_de_risco": {
            "type": dict,
            "required": [
                "nivel",
                "score",
                "fatores"
            ]
        },
        "possiveis_conflitos": {
            "type": dict,
            "required": [
                "alta_probabilidade",
                "media_probabilidade",
                "conflitos_semanticos_e_nao_textuais"
            ]
        },
        "complexidade": {
            "type": dict,
            "required": [
                "nivel",
                "estimativa_esforco",
                "drivers"
            ]
        },
        "plano_de_execucao": {
            "type": list
        },
        "arquivos_prioritarios": {
            "type": list
        },
        "ordem_recomendada_de_implementacao": {
            "type": list
        }
    }

    @classmethod
    def validate(
        cls,
        analysis: dict
    ) -> None:

        for field in cls.REQUIRED_FIELDS:

            if field not in analysis:

                raise RuntimeError(
                    f"Campo obrigatório ausente: {field}"
                )

        for field, expected_type in cls.FIELD_TYPES.items():

            if not isinstance(
                analysis[field],
                expected_type
            ):

                raise RuntimeError(
                    f"Campo '{field}' deve ser do tipo "
                    f"{expected_type.__name__}."
                )

        for field, definition in cls.SCHEMA.items():

            if definition["type"] is not dict:

                continue

            value = analysis[field]

            for required in definition["required"]:

                if required not in value:

                    raise RuntimeError(
                        f"Campo '{required}' ausente em '{field}'."
                    )