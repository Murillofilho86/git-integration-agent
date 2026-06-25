from pathlib import Path
import subprocess


class TargetValidator:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def validate(
        self,
        target_ref: str,
        file_path: str,
        summary: list[str]
    ) -> list[dict]:

        target_content = self._load_file(
            target_ref,
            file_path
        )

        results = []

        for item in summary:

            exists = self._exists_in_target(
                item,
                target_content
            )

            results.append(
                {
                    "item": item,
                    "already_exists": exists
                }
            )

        return results

    def _load_file(
        self,
        target_ref: str,
        file_path: str
    ) -> str:

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "show",
            f"{target_ref}:{file_path}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        return result.stdout

    def _exists_in_target(
        self,
        item: str,
        target_content: str
    ) -> bool:

        if "endpoint" in item.lower():

            parts = item.split(
                ":",
                maxsplit=1
            )

            if len(parts) == 2:

                route = parts[1].strip()

                return (
                    route
                    in target_content
                )

        if "dependência" in item.lower():

            parts = item.split(
                ":",
                maxsplit=1
            )

            if len(parts) == 2:

                dependency = (
                    parts[1]
                    .strip()
                    .split(".")
                    [-1]
                )

                return (
                    dependency
                    in target_content
                )

        return False