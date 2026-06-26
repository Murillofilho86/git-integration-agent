from pathlib import Path
import json


class TaskPlanReader:

    def load(
        self,
        workspace_path: str
    ) -> dict:

        workspace = Path(
            workspace_path
        )

        task_plan_file = (
            workspace /
            "task-plan.json"
        )

        if not task_plan_file.exists():

            raise RuntimeError(
                "Arquivo task-plan.json não encontrado."
            )

        return json.loads(
            task_plan_file.read_text(
                encoding="utf-8"
            )
        )

    def get_tasks(
        self,
        workspace_path: str
    ) -> list:

        task_plan = self.load(
            workspace_path
        )

        return task_plan.get(
            "tasks",
            []
        )

    def get_task(
        self,
        workspace_path: str,
        index: int
    ) -> dict | None:

        tasks = self.get_tasks(
            workspace_path
        )

        if index < 0:

            return None

        if index >= len(
            tasks
        ):

            return None

        return tasks[
            index
        ]

    def total_tasks(
        self,
        workspace_path: str
    ) -> int:

        return len(
            self.get_tasks(
                workspace_path
            )
        )