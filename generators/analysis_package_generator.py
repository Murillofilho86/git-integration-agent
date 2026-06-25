import json
from pathlib import Path

from analyzers.git_analyzer import GitAnalyzer


class AnalysisPackageGenerator:

    def __init__(
        self,
        git: GitAnalyzer
    ):
        self.git = git

    def sanitize_ref_name(
        self,
        ref_name: str
    ) -> str:

        return (
            ref_name
            .replace("/", "_")
            .replace("\\", "_")
            .replace(" ", "_")
            .replace(":", "_")
        )

    def generate(
        self,
        source_ref: str,
        target_ref: str
    ) -> Path:

        commits = self.git.count_commits(
            source_ref,
            target_ref
        )

        files = self.git.changed_files(
            source_ref,
            target_ref
        )

        age = self.git.age_days(
            source_ref
        )

        repository_profile = (
            self.git.get_repository_profile()
        )

        repository_name = (
            repository_profile[
                "repository_name"
            ]
        )

        workspace_dir = (
            Path("workspace") /
            repository_name
        )

        workspace_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        source_name = (
            self.sanitize_ref_name(
                source_ref
            )
        )

        target_name = (
            self.sanitize_ref_name(
                target_ref
            )
        )

        analysis_dir = (
            workspace_dir /
            f"{source_name}_vs_{target_name}"
        )

        analysis_dir.mkdir(
            exist_ok=True
        )

        metadata = {
            "source": source_ref,
            "target": target_ref,
            "commits": commits,
            "files_changed": files,
            "age_days": age
        }

        with open(
            analysis_dir /
            "metadata.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4,
                ensure_ascii=False
            )

        with open(
            analysis_dir /
            "repository-profile.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                repository_profile,
                file,
                indent=4,
                ensure_ascii=False
            )

        with open(
            analysis_dir /
            "commits.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                self.git.get_commit_log(
                    source_ref,
                    target_ref
                )
            )

        with open(
            analysis_dir /
            "files.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                self.git.get_changed_files_list(
                    source_ref,
                    target_ref
                )
            )

        return analysis_dir