
import json
from pathlib import Path


class TaskTracker:

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
    ):

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

    def complete_current_task(
        self,
        workspace: str,
        total_tasks: int
    ) -> dict:

        state = self.load_state(
            workspace
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