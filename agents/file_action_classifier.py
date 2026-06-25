from pathlib import Path
import subprocess


class FileActionClassifier:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def classify(
        self,
        source_ref: str,
        target_ref: str,
        files: list[str]
    ) -> dict:

        result = {
            "create": [],
            "update": [],
            "validate": []
        }

        for file in files:

            file_lower = file.lower()

            if (
                file_lower.startswith(
                    "test/"
                )
                or "/test/" in file_lower
            ):

                result["validate"].append(
                    file
                )

                continue

            source_exists = (
                self._file_exists(
                    source_ref,
                    file
                )
            )

            target_exists = (
                self._file_exists(
                    target_ref,
                    file
                )
            )

            if (
                source_exists
                and not target_exists
            ):

                result["create"].append(
                    file
                )

            elif (
                source_exists
                and target_exists
            ):

                result["update"].append(
                    file
                )

        return result

    def _file_exists(
        self,
        git_ref: str,
        file_path: str
    ) -> bool:

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "cat-file",
            "-e",
            f"{git_ref}:{file_path}"
        ]

        result = subprocess.run(
            command,
            capture_output=True
        )

        return result.returncode == 0