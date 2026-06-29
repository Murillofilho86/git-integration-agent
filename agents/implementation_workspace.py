from pathlib import Path


class ImplementationWorkspace:

    def __init__(
        self,
        workspace: str
    ):

        self._workspace = Path(
            workspace
        )

    def history_directory(
        self
    ) -> Path:

        directory = (
            self._workspace /
            "implementation-history"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return directory

    def task_directory(
        self,
        task_id: int
    ) -> Path:

        directory = (
            self.history_directory() /
            f"task-{task_id:03d}"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return directory

    def generated_files_directory(
        self,
        task: dict
    ) -> Path:

        directory = (
            self.task_directory(
                task
            ) /
            "generated-files"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return directory

    def prompt_file(
        self,
        task: dict
    ) -> Path:

        return (
            self.task_directory(
                task
            ) /
            "implementation-prompt.md"
        )

    def response_file(
        self,
        task: dict
    ) -> Path:

        return (
            self.task_directory(
                task
            ) /
            "implementation-response.json"
        )

    def session_file(
        self,
        task: dict
    ) -> Path:

        return (
            self.task_directory(
                task
            ) /
            "implementation-session.md"
        )

    def execution_file(
        self,
        task: dict
    ) -> Path:

        return (
            self.task_directory(
                task
            ) /
            "execution.json"
        )