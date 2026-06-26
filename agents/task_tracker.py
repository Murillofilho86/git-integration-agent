import json
from pathlib import Path

from agents.task_plan_reader import (
    TaskPlanReader
)


class TaskTracker:

    def __init__(
        self
    ):

        self._reader = (
            TaskPlanReader()
        )

    def _state_file(
        self,
        workspace: str
    ) -> Path:

        return (
            Path(workspace) /
            "task-state.json"
        )

    def load_state(
        self,
        workspace: str
    ) -> dict:

        state_file = self._state_file(
            workspace
        )

        if not state_file.exists():

            state = {
                "current": 0,
                "completed": []
            }

            state_file.write_text(
                json.dumps(
                    state,
                    indent=4
                ),
                encoding="utf-8"
            )

            return state

        return json.loads(
            state_file.read_text(
                encoding="utf-8"
            )
        )

    def save_state(
        self,
        workspace: str,
        state: dict
    ) -> None:

        state_file = self._state_file(
            workspace
        )

        state_file.write_text(
            json.dumps(
                state,
                indent=4
            ),
            encoding="utf-8"
        )

    def current_task(
        self,
        workspace: str
    ) -> dict | None:

        state = self.load_state(
            workspace
        )

        return self._reader.get_task(
            workspace,
            state["current"]
        )

    def total_tasks(
        self,
        workspace: str
    ) -> int:

        return self._reader.total_tasks(
            workspace
        )

    def complete_current_task(
        self,
        workspace: str
    ) -> dict:

        state = self.load_state(
            workspace
        )

        total_tasks = (
            self.total_tasks(
                workspace
            )
        )

        current = state["current"]

        if current >= total_tasks:

            return {
                "completed": False,
                "finished": True
            }

        if current not in state["completed"]:

            state["completed"].append(
                current
            )

        state["current"] += 1

        self.save_state(
            workspace,
            state
        )

        return {
            "completed": True,
            "finished": (
                state["current"] >= total_tasks
            )
        }