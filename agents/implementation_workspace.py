from pathlib import Path
import shutil
import time


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

    def task_directory_has_content(
        self,
        task_id: int
    ) -> bool:

        directory = (
            self.history_directory() /
            f"task-{task_id:03d}"
        )

        if not directory.exists():

            return False

        return any(
            directory.iterdir()
        )

    def failed_history_directory(
        self
    ) -> Path:

        directory = (
            self._workspace /
            "implementation-history-failed"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        return directory

    def archive_task_directory(
        self,
        task_id: int
    ) -> Path | None:

        if not self.task_directory_has_content(
            task_id
        ):

            return None

        directory = (
            self.history_directory() /
            f"task-{task_id:03d}"
        )

        destination = (
            self.failed_history_directory() /
            f"task-{task_id:03d}-{int(time.time())}"
        )

        shutil.move(
            str(directory),
            str(destination)
        )

        return destination

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