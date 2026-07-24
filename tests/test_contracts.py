import pytest

from contracts.ai_contract_v1 import AIContractV1
from contracts.implementation_contract_v1 import ImplementationContractV1


def valid_ai_analysis() -> dict:
    return {
        "estrategia_recomendada": {
            "estrategia": "A",
            "nome": "Merge",
            "descricao": "Merge direto",
            "alinhado_com_heuristica": True,
            "confianca": 0.9,
        },
        "nivel_de_risco": {
            "nivel": "baixo",
            "score": 0.1,
            "fatores": [],
        },
        "possiveis_conflitos": {
            "alta_probabilidade": [],
            "media_probabilidade": [],
            "conflitos_semanticos_e_nao_textuais": [],
        },
        "complexidade": {
            "nivel": "baixa",
            "estimativa_esforco": "1h",
            "drivers": [],
        },
        "plano_de_execucao": [],
        "arquivos_prioritarios": [],
        "ordem_recomendada_de_implementacao": [],
    }


class TestAIContractV1:

    def test_valid_analysis_passes(self):
        AIContractV1.validate(valid_ai_analysis())

    def test_missing_required_field_raises(self):
        analysis = valid_ai_analysis()
        del analysis["nivel_de_risco"]

        with pytest.raises(RuntimeError, match="nivel_de_risco"):
            AIContractV1.validate(analysis)

    def test_wrong_top_level_type_raises(self):
        analysis = valid_ai_analysis()
        analysis["plano_de_execucao"] = "not-a-list"

        with pytest.raises(RuntimeError, match="plano_de_execucao"):
            AIContractV1.validate(analysis)

    def test_missing_nested_required_field_raises(self):
        analysis = valid_ai_analysis()
        del analysis["estrategia_recomendada"]["confianca"]

        with pytest.raises(RuntimeError, match="confianca"):
            AIContractV1.validate(analysis)

    def test_agnostic_to_technology_specific_content(self):
        # The contract only validates shape/types, never file content or
        # language -- a React-flavoured payload must pass exactly like a
        # .NET one as long as the shape is respected.
        analysis = valid_ai_analysis()
        analysis["estrategia_recomendada"]["descricao"] = (
            "Reconciliar hooks e componentes React divergentes"
        )
        analysis["complexidade"]["drivers"] = ["JSX", "hooks", "context-api"]

        AIContractV1.validate(analysis)


class TestImplementationContractV1:

    def test_required_fields_and_types(self):
        assert ImplementationContractV1.REQUIRED_FIELDS == ["generated_files"]
        assert ImplementationContractV1.FIELD_TYPES == {"generated_files": list}
