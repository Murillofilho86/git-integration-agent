from pathlib import Path
import subprocess


class GitFileReader:

    def read(
        self,
        repository: str,
        branch: str,
        file_path: str
    ) -> str | None:

        repository_path = Path(
            repository
        )

        result = subprocess.run(
            [
                "git",
                "-C",
                str(
                    repository_path
                ),
                "show",
                f"{branch}:{file_path}"
            ],
            capture_output=True
        )

        if result.returncode != 0:

            return None

        for encoding in (
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin-1"
        ):

            try:

                return result.stdout.decode(
                    encoding
                )

            except UnicodeDecodeError:

                continue

        raise RuntimeError(
            (
                "Não foi possível decodificar "
                f"'{file_path}' da branch "
                f"'{branch}'."
            )
        )