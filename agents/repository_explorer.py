from pathlib import Path


class RepositoryExplorer:

    SKIP_DIRECTORIES = {
        "node_modules",
        ".git",
        "bin",
        "obj",
        "dist",
        "build",
        "out",
        "target",
        "__pycache__",
        ".venv",
        "venv",
        ".next",
        ".nuxt",
        ".idea",
        ".vscode"
    }

    BINARY_EXTENSIONS = {
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp",
        ".svg", ".woff", ".woff2", ".ttf", ".eot", ".otf",
        ".pdf", ".zip", ".gz", ".tar", ".7z", ".rar",
        ".exe", ".dll", ".so", ".dylib", ".pyc", ".class", ".jar",
        ".mp3", ".mp4", ".mov", ".avi", ".wav",
        ".map", ".lock"
    }

    def find_file(
        self,
        repo_path: str,
        filename: str
    ) -> list[Path]:

        repo = Path(repo_path)

        return list(
            repo.rglob(filename)
        )

    def _is_skipped(
        self,
        file: Path
    ) -> bool:

        if any(
            part in self.SKIP_DIRECTORIES
            for part in file.parts
        ):

            return True

        if file.suffix.lower() in self.BINARY_EXTENSIONS:

            return True

        return False

    def find_dependents(
        self,
        repo_path: str,
        filename: str
    ) -> list[str]:

        repo = Path(repo_path)

        target_name = Path(
            filename
        ).stem

        dependents = set()

        for file in repo.rglob("*"):

            if not file.is_file():
                continue

            if file.name == filename:
                continue

            if self._is_skipped(file):
                continue

            try:

                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                if target_name in content:

                    dependents.add(
                        file.name
                    )

            except Exception:
                continue

        return sorted(
            dependents
        )

    def inspect(
        self,
        repo_path: str,
        filename: str
    ) -> dict:

        files = self.find_file(
            repo_path,
            filename
        )

        dependents = self.find_dependents(
            repo_path,
            filename
        )

        return {
            "exists": len(files) > 0,
            "locations": [
                str(file)
                for file in files
            ],
            "dependents": dependents,
            "dependent_count": len(
                dependents
            )
        }