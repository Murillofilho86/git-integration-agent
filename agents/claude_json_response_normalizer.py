from pathlib import Path
import json


class ClaudeJsonResponseNormalizer:

    def normalize(
        self,
        workspace: str,
        response_file: str,
        backup_file: str | None = None
    ) -> None:

        workspace_path = Path(
            workspace
        )

        response_path = (
            workspace_path /
            response_file
        )

        if not response_path.exists():

            raise RuntimeError(
                f"Arquivo não encontrado: {response_file}"
            )

        response = json.loads(
            response_path.read_text(
                encoding="utf-8"
            )
        )

        if "result" not in response:

            raise RuntimeError(
                "Campo 'result' não encontrado."
            )

        raw = response[
            "result"
        ]

        backup = (
            workspace_path /
            backup_file
        )

        if not backup.exists():

            backup.write_text(
                json.dumps(
                    response,
                    indent=4,
                    ensure_ascii=False
                ),
                encoding="utf-8"
            )

        json_text = (
            self._extract_json(
                raw
            )
        )

        try:

            json.loads(
                json_text
            )

        except json.JSONDecodeError as exception:

            raise RuntimeError(
                "JSON encontrado, porém inválido."
            ) from exception

        response[
            "result"
        ] = json_text

        response_path.write_text(
            json.dumps(
                response,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

    def _extract_json(
        self,
        text: str
    ) -> str:

        start = (
            text.find("{")
        )

        if start == -1:

            raise RuntimeError(
                "Nenhum JSON encontrado na resposta do Claude."
            )

        inside_string = False

        escaped = False

        level = 0

        end = None

        for index in range(
            start,
            len(text)
        ):

            character = text[
                index
            ]

            if escaped:

                escaped = False

                continue

            if character == "\\":

                escaped = True

                continue

            if character == '"':

                inside_string = (
                    not inside_string
                )

                continue

            if inside_string:

                continue

            if character == "{":

                level += 1

            elif character == "}":

                level -= 1

                if level == 0:

                    end = (
                        index + 1
                    )

                    break

        if end is None:

            raise RuntimeError(
                "JSON incompleto encontrado na resposta do Claude."
            )

        return text[
            start:end
        ]