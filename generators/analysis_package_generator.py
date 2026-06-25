import json
from pathlib import Path

from analyzers.git_analyzer import GitAnalyzer


class AnalysisPackageGenerator:

    def __init__(self, git: GitAnalyzer):
        self.git = git

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

        workspace_dir = Path("workspace")
        workspace_dir.mkdir(exist_ok=True)

        analysis_dir = (
            workspace_dir /
            f"{source_ref}_vs_{target_ref}"
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
            analysis_dir / "metadata.json",
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
            analysis_dir / "commits.txt",
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
            analysis_dir / "files.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(
                self.git.get_changed_files_list(
                    source_ref,
                    target_ref
                )
            )

        with open(
            analysis_dir / "diff.patch",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(
                self.git.get_diff(
                    source_ref,
                    target_ref
                )
            )

        try:
            with open(
                analysis_dir / "range-diff.txt",
                "w",
                encoding="utf-8"
            ) as file:
                file.write(
                    self.git.get_range_diff(
                        source_ref,
                        target_ref
                    )
                )
        except Exception:
            pass

        return analysis_dir