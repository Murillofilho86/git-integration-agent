from pathlib import Path
import subprocess


class ChangeExtractor:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def extract(
        self,
        source_ref: str,
        target_ref: str,
        filename: str
    ) -> dict:

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "diff",
            target_ref,
            source_ref,
            "--",
            filename
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        diff = result.stdout

        additions = []
        removals = []

        for line in diff.splitlines():

            if line.startswith(
                "+++"
            ):
                continue

            if line.startswith(
                "---"
            ):
                continue

            if line.startswith(
                "+"
            ):
                additions.append(
                    line
                )

            elif line.startswith(
                "-"
            ):
                removals.append(
                    line
                )

        return {
            "file": filename,
            "additions": additions,
            "removals": removals,
            "total_additions": len(
                additions
            ),
            "total_removals": len(
                removals
            )
        }