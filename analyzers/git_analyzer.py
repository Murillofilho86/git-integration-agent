from datetime import datetime
from pathlib import Path

from git import Repo


class GitAnalyzer:

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

        if not self.repo_path.exists():
            raise FileNotFoundError(
                f"Repositório não encontrado: {repo_path}"
            )

        try:
            self.repo = Repo(repo_path)
        except Exception as ex:
            raise ValueError(
                f"O diretório informado não é um repositório Git válido: {repo_path}"
            ) from ex

    def get_repository_name(self) -> str:
        return self.repo_path.name

    def get_repository_profile(self) -> dict:

        technologies = []

        if list(self.repo_path.rglob("*.csproj")):
            technologies.extend(
                [
                    "csharp",
                    ".net"
                ]
            )

        if (
            self.repo_path /
            "package.json"
        ).exists():

            technologies.append(
                "nodejs"
            )

            package_json = (
                self.repo_path /
                "package.json"
            ).read_text(
                encoding="utf-8",
                errors="ignore"
            ).lower()

            if "react" in package_json:
                technologies.append(
                    "react"
                )

            if "vue" in package_json:
                technologies.append(
                    "vue"
                )

        if (
            self.repo_path /
            "angular.json"
        ).exists():
            technologies.append(
                "angular"
            )

        return {
            "repository_name": self.get_repository_name(),
            "detected_technologies": sorted(
                list(
                    set(
                        technologies
                    )
                )
            )
        }

    def branch_exists(
        self,
        branch_name: str
    ) -> bool:
        try:
            self.repo.commit(
                branch_name
            )

            return True

        except Exception:
            return False

    def count_commits(
        self,
        source: str,
        target: str
    ) -> int:

        commits = list(
            self.repo.iter_commits(
                f"{target}..{source}"
            )
        )

        return len(
            commits
        )

    def changed_files(
        self,
        source: str,
        target: str
    ) -> int:

        diff = self.repo.git.diff(
            "--name-only",
            f"{target}..{source}"
        )

        return len(
            diff.splitlines()
        )

    def age_days(
        self,
        source: str
    ) -> int:

        commit = next(
            self.repo.iter_commits(
                source
            )
        )

        commit_date = datetime.fromtimestamp(
            commit.committed_date
        )

        return (
            datetime.now() -
            commit_date
        ).days

    def get_commit_log(
        self,
        source: str,
        target: str
    ) -> str:

        return self.repo.git.log(
            f"{target}..{source}",
            "--oneline"
        )

    def get_changed_files_list(
        self,
        source: str,
        target: str
    ) -> str:

        return self.repo.git.diff(
            "--name-only",
            f"{target}..{source}"
        )