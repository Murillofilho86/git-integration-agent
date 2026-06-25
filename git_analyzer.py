from git import Repo
from datetime import datetime

class GitAnalyzer:

    def __init__(self, repo_path="."):
        self.repo = Repo(repo_path)

        

    def count_commits(self, source, target):

    commits = list(
        self.repo.iter_commits(
            f"{target}..{source}"
        )
    )

    return len(commits)

    def changed_files(self, source, target):

    diff = self.repo.git.diff(
        "--name-only",
        f"{target}..{source}"
    )

    return len(diff.splitlines())


    def age_days(self, source):

    commit = next(
        self.repo.iter_commits(source)
    )

    commit_date = datetime.fromtimestamp(
        commit.committed_date
    )

    return (
        datetime.now() - commit_date
    ).days