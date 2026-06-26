from agents.git_file_reader import (
    GitFileReader
)


class FileSnapshotBuilder:

    def __init__(
        self
    ):

        self._git_reader = (
            GitFileReader()
        )

    def build(
        self,
        repository: str,
        source_branch: str,
        target_branch: str,
        task: dict
    ) -> dict:

        snapshot = {
            "files": []
        }

        for file_path in task[
            "files"
        ]:

            source_content = (
                self._git_reader.read(
                    repository,
                    source_branch,
                    file_path
                )
            )

            target_content = (
                self._git_reader.read(
                    repository,
                    target_branch,
                    file_path
                )
            )

            snapshot[
                "files"
            ].append(
                {
                    "path": file_path,
                    "source": source_content,
                    "target": target_content
                }
            )

        return snapshot