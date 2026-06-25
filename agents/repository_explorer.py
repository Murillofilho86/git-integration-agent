from pathlib import Path


class RepositoryExplorer:

    def find_file(
        self,
        repo_path: str,
        filename: str
    ) -> list[Path]:

        repo = Path(repo_path)

        return list(
            repo.rglob(filename)
        )

    def find_dependents(
        self,
        repo_path: str,
        filename: str
    ) -> list[str]:

        repo = Path(repo_path)

        target_name = (
            filename
            .replace(".cs", "")
            .replace(".ts", "")
            .replace(".tsx", "")
        )

        dependents = set()

        for file in repo.rglob("*"):

            if not file.is_file():
                continue

            if file.name == filename:
                continue

            if file.suffix not in {
                ".cs",
                ".ts",
                ".tsx"
            }:
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