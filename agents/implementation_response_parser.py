from pathlib import Path
import json

from contracts.implementation_contract_v1 import (
    ImplementationContractV1
)


class ImplementationResponseParser:

    def __init__(
        self
    ):

        self._contract = (
            ImplementationContractV1
        )

    def _validate_contract(
        self,
        response: dict
    ) -> None:

        for field in (
            self._contract.REQUIRED_FIELDS
        ):

            if field not in response:

                raise RuntimeError(
                    f"Campo obrigatório ausente: {field}"
                )

        for field, expected_type in (
            self._contract.FIELD_TYPES.items()
        ):

            if not isinstance(
                response[field],
                expected_type
            ):

                raise RuntimeError(
                    f"Campo '{field}' deve ser do tipo "
                    f"{expected_type.__name__}."
                )

    def _validate_task_scope(
        self,
        implementation: dict,
        task: dict
    ) -> None:

        expected = set(
            task["files"]
        )

        returned = {
            item["path"]
            for item in implementation[
                "generated_files"
            ]
        }

        if expected != returned:

            missing = sorted(
                expected - returned
            )

            extra = sorted(
                returned - expected
            )

            message = [
                "A resposta do Claude não corresponde ao escopo da tarefa.",
                "",
                f"Arquivos esperados : {len(expected)}",
                f"Arquivos retornados: {len(returned)}",
                ""
            ]

            if missing:

                message.append(
                    "Arquivos ausentes:"
                )

                message.extend(
                    missing
                )

                message.append(
                    ""
                )

            if extra:

                message.append(
                    "Arquivos extras:"
                )

                message.extend(
                    extra
                )

            raise RuntimeError(
                "\n".join(
                    message
                )
            )

    def parse(
        self,
        workspace_path: str,
        task: dict
    ) -> str:

        workspace = Path(
            workspace_path
        )

        response_file = (
            workspace /
            "implementation-response.json"
        )

        if not response_file.exists():

            raise RuntimeError(
                "Arquivo implementation-response.json não encontrado."
            )

        response = json.loads(
            response_file.read_text(
                encoding="utf-8"
            )
        )

        if "result" not in response:

            raise RuntimeError(
                "Campo 'result' não encontrado."
            )

        try:

            implementation = json.loads(
                response[
                    "result"
                ]
            )

        except json.JSONDecodeError as exception:

            raise RuntimeError(
                "O campo 'result' não contém um JSON válido."
            ) from exception

        self._validate_contract(
            implementation
        )

        self._validate_task_scope(
            implementation,
            task
        )

        generated_directory = (
            workspace /
            "generated-files"
        )

        generated_directory.mkdir(
            exist_ok=True
        )

        for file in implementation[
            "generated_files"
        ]:

            output_file = (
                generated_directory /
                file[
                    "path"
                ]
            )

            output_file.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            output_file.write_text(
                file[
                    "content"
                ],
                encoding="utf-8"
            )

        return str(
            generated_directory
        )