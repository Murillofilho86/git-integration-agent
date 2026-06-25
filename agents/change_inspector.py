from pathlib import Path
import subprocess
import re


class ChangeInspector:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def inspect(
        self,
        source_ref: str,
        target_ref: str,
        file_path: str
    ) -> dict:

        command = [
            "git",
            "-C",
            str(self.repo_path),
            "diff",
            target_ref,
            source_ref,
            "--",
            file_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        diff = result.stdout

        added_lines = []
        removed_lines = []

        for line in diff.splitlines():

            if line.startswith("+++"):
                continue

            if line.startswith("---"):
                continue

            if line.startswith("+"):

                added_lines.append(
                    line[1:]
                )

            elif line.startswith("-"):

                removed_lines.append(
                    line[1:]
                )

        detected_items = self._extract_items(
            added_lines
        )

        return {
            "file": file_path,
            "added_count": len(
                added_lines
            ),
            "removed_count": len(
                removed_lines
            ),
            "detected_items": detected_items
        }

    def _extract_items(
        self,
        lines: list[str]
    ) -> list[str]:

        patterns = [
            r"public\s+.*?\s+(\w+)\s*\(",
            r"private\s+.*?\s+(\w+)\s*\(",
            r"internal\s+.*?\s+(\w+)\s*\(",
            r"class\s+(\w+)",
            r"interface\s+(\w+)"
        ]

        results = set()

        for line in lines:

            for pattern in patterns:

                match = re.search(
                    pattern,
                    line
                )

                if match:

                    results.add(
                        match.group(1)
                    )

        return sorted(
            list(results)
        )