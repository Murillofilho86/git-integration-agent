from pathlib import Path
import subprocess
import re


class DependencyConflictAnalyzer:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def analyze(
        self,
        target_ref: str,
        summary: list[str]
    ) -> list[dict]:

        results = []

        for item in summary:

            if not item.startswith(
                "Nova dependência:"
            ):
                continue

            dependency = (
                item.replace(
                    "Nova dependência:",
                    ""
                )
                .strip()
            )

            result = self._inspect_dependency(
                target_ref,
                dependency
            )

            results.append(
                result
            )

        return results

    def _inspect_dependency(
        self,
        target_ref: str,
        dependency: str
    ) -> dict:

        dependency_name = (
            dependency.split(".")
            [-1]
        )

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "grep",
            dependency_name,
            target_ref
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if not result.stdout:

            return {
                "dependency": dependency_name,
                "status": "MISSING"
            }

        occurrences = len(
            result.stdout.splitlines()
        )

        if occurrences > 20:

            return {
                "dependency": dependency_name,
                "status": "AMBIGUOUS",
                "occurrences": occurrences
            }

        return {
            "dependency": dependency_name,
            "status": "FOUND",
            "occurrences": occurrences
        }