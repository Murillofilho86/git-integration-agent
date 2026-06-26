from pathlib import Path
import json

from contracts.ai_contract_v1 import (
    AIContractV1
)


class ClaudeResponseParser:

    def __init__(
        self,
        contract=AIContractV1
    ):

        self._contract = contract

    def _validate_contract(
        self,
        analysis: dict
    ) -> None:

        for field in (
            self._contract.REQUIRED_FIELDS
        ):

            if field not in analysis:

                raise RuntimeError(
                    f"Campo obrigatório ausente: {field}"
                )

        for field, expected_type in (
            self._contract.FIELD_TYPES.items()
        ):

            if not isinstance(
                analysis[field],
                expected_type
            ):

                raise RuntimeError(
                    f"Campo '{field}' deve ser do tipo "
                    f"{expected_type.__name__}."
                )

    def parse(
        self,
        workspace_path: str
    ) -> str:

        workspace = Path(
            workspace_path
        )

        response_file = (
            workspace /
            "claude-response.json"
        )

        if not response_file.exists():

            raise RuntimeError(
                "Arquivo claude-response.json não encontrado."
            )

        response = json.loads(
            response_file.read_text(
                encoding="utf-8"
            )
        )

        if "result" not in response:

            raise RuntimeError(
                "Campo 'result' não encontrado na resposta do Claude."
            )

        try:

            analysis = json.loads(
                response["result"]
            )

        except json.JSONDecodeError as exception:

            raise RuntimeError(
                "O campo 'result' não contém um JSON válido."
            ) from exception

        self._validate_contract(
            analysis
        )

        output_file = (
            workspace /
            "integration-analysis.json"
        )

        output_file.write_text(
            json.dumps(
                analysis,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return str(
            output_file
        )