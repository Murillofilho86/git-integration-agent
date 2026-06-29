from agents.task_plan_reader import TaskPlanReader
from agents.implementation_executor import ImplementationExecutor
from agents.generated_files_merger import GeneratedFilesMerger

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

    def run(
        self,
        repository: str,
        workspace: str,
        source_branch: str,
        target_branch: str
    ) -> str:

        tasks = (
            self._reader.get_tasks(
                workspace
            )
        )

        generated_files_directory = None

        total = len(
            tasks
        )

        for index, task in enumerate(
            tasks,
            start=1
        ):

            print(
                f"[{index}/{total}] "
                f"Implementando: "
                f"{task['title']}"
            )

            generated_files_directory = (
                self._executor.execute(
                    repository=repository,
                    workspace=workspace,
                    source_branch=source_branch,
                    target_branch=target_branch,
                    task=task
                )
            )

            print(
                f"[{index}/{total}] "
                "Concluído."
            )

        return (
            self._merger.merge(
                workspace=workspace
            )
        )