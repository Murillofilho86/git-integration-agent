from agents.task_plan_reader import TaskPlanReader
from agents.implementation_executor import ImplementationExecutor
from agents.implementation_workspace import ImplementationWorkspace
from agents.generated_files_merger import GeneratedFilesMerger
from core.task_tracker import TaskTracker

class ImplementationRunner:

    def __init__(
        self
    ):

        self._reader = (
            TaskPlanReader()
        )

        self._executor = (
            ImplementationExecutor()
        )

        self._merger = (
            GeneratedFilesMerger()
        )

        self._tracker = (
            TaskTracker()
        )

    def run(
        self,
        repository: str,
        workspace: str,
        source_branch: str,
        target_branch: str,
        resume: bool = False
    ) -> str:

        tasks = (
            self._reader.get_tasks(
                workspace
            )
        )

        total = len(
            tasks
        )

        if not resume:

            self._tracker.reset_state(
                workspace
            )

        state = (
            self._tracker.load_state(
                workspace
            )
        )

        implementation_workspace = (
            ImplementationWorkspace(
                workspace
            )
        )

        for index, task in enumerate(
            tasks
        ):

            if index in state["completed"]:

                print(
                    f"[{index + 1}/{total}] "
                    f"Já concluída: "
                    f"{task['title']} "
                    "(pulando)"
                )

                continue

            archived = (
                implementation_workspace.archive_task_directory(
                    task["id"]
                )
            )

            if archived is not None:

                print(
                    f"[{index + 1}/{total}] "
                    "Tentativa anterior preservada em: "
                    f"{archived}"
                )

            print(
                f"[{index + 1}/{total}] "
                f"Implementando: "
                f"{task['title']}"
            )

            self._executor.execute(
                repository=repository,
                workspace=workspace,
                source_branch=source_branch,
                target_branch=target_branch,
                task=task
            )

            print(
                f"[{index + 1}/{total}] "
                "Concluído."
            )

            state["completed"].append(
                index
            )

            state["current"] = (
                index + 1
            )

            self._tracker.save_state(
                workspace,
                state
            )

        return (
            self._merger.merge(
                workspace=workspace
            )
        )