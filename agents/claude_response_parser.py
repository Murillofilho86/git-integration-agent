from pathlib import Path
import json


class ClaudeResponseParser:

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