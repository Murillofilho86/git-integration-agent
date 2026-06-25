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

    def branch_exists(self, branch_name: str) -> bool:
        try:
            self.repo.commit(branch_name)
            return True
        except Exception:
            return False

    def count_commits(self, source: str, target: str) -> int:
        commits = list(
            self.repo.iter_commits(
                f"{target}..{source}"
            )
        )

        return len(commits)

    def changed_files(self, source: str, target: str) -> int:
        diff = self.repo.git.diff(
            "--name-only",
            f"{target}..{source}"
        )

        return len(diff.splitlines())

    def age_days(self, source: str) -> int:
        commit = next(
            self.repo.iter_commits(source)
        )

        commit_date = datetime.fromtimestamp(
            commit.committed_date
        )

        return (
            datetime.now() - commit_date
        ).days

    def get_commit_log(self, source: str, target: str) -> str:
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

    def get_diff(
        self,
        source: str,
        target: str
    ) -> str:
        return self.repo.git.diff(
            f"{target}..{source}"
        )

    def get_range_diff(
        self,
        source: str,
        target: str
    ) -> str:
        try:
            return self.repo.git.execute(
                [
                    "git",
                    "range-diff",
                    f"{target}...{source}"
                ]
            )
        except Exception:
            return "range-diff não disponível ou não suportado neste repositório."