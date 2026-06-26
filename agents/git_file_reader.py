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
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            return None

        return result.stdout