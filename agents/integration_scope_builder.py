from pathlib import Path
import subprocess


class IntegrationScopeBuilder:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def build(
        self,
        source_ref: str,
        dependencies: list[str],
        root_file: str | None = None
    ) -> list[dict]:

        results = []

        root_file_name = None

        if root_file:

            root_file_name = Path(
                root_file
            ).name

        for dependency in dependencies:

            files = self._find_dependency(
                source_ref,
                dependency
            )

            if root_file_name:

                files = [
                    file
                    for file in files
                    if not file.endswith(
                        root_file_name
                    )
                ]

            results.append(
                {
                    "dependency": dependency,
                    "files": files
                }
            )

        return results

    def consolidate_scope(
        self,
        scope: list[dict]
    ) -> dict:

        unique_files = set()

        occurrences = {}

        for dependency in scope:

            for file in dependency["files"]:

                unique_files.add(
                    file
                )

                occurrences[file] = (
                    occurrences.get(
                        file,
                        0
                    ) + 1
                )

        categories = self.categorize(
            list(
                unique_files
            )
        )

        shared_files = sorted(
            [
                file
                for file, count
                in occurrences.items()
                if count > 1
            ]
        )

        return {
            "total_unique": len(
                unique_files
            ),
            "categories": categories,
            "shared_files": shared_files
        }

    def categorize(
        self,
        files: list[str]
    ) -> dict:

        categories = {
            "Api": [],
            "Application": [],
            "Domain": [],
            "Infrastructure": [],
            "Tests": [],
            "Other": []
        }

        for file in files:

            file_lower = file.lower()

            if ".api/" in file_lower:

                categories["Api"].append(
                    file
                )

            elif ".application/" in file_lower:

                categories["Application"].append(
                    file
                )

            elif ".domain/" in file_lower:

                categories["Domain"].append(
                    file
                )

            elif ".infrastructure/" in file_lower:

                categories["Infrastructure"].append(
                    file
                )

            elif (
                file_lower.startswith(
                    "test/"
                )
                or "/test/" in file_lower
            ):

                categories["Tests"].append(
                    file
                )

            else:

                categories["Other"].append(
                    file
                )

        return categories

    def _find_dependency(
        self,
        source_ref: str,
        dependency: str
    ) -> list[str]:

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "grep",
            "-l",
            dependency,
            source_ref
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        files = []

        for line in result.stdout.splitlines():

            parts = line.split(
                ":",
                maxsplit=1
            )

            if len(parts) != 2:
                continue

            files.append(
                parts[1]
            )

        return sorted(
            list(
                set(files)
            )
        )