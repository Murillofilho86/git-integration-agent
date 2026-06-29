import json
from pathlib import Path

from core.task_tracker import (
    TaskTracker
)

from agents.task_breakdown import (
    TaskBreakdown
)


class ExecutionNavigator:

    def load_analysis(
        self,
        workspace: str
    ) -> dict:

        workspace_path = Path(
            workspace
        )

        analysis_file = (
            workspace_path /
            "ai-analysis.json"
        )

        if not analysis_file.exists():
            raise FileNotFoundError(
                "ai-analysis.json não encontrado"
            )

        return json.loads(
            analysis_file.read_text(
                encoding="utf-8"
            )
        )

    def get_plan(
        self,
        workspace: str
    ) -> dict:

        data = self.load_analysis(
            workspace
        )

        tracker = TaskTracker()

        state = tracker.load_state(
            workspace
        )

        data["task_state"] = state

        return data

    def get_next_task(
        self,
        workspace: str
    ) -> dict:

        data = self.load_analysis(
            workspace
        )

        tasks = data.get(
            "plan",
            []
        )

        tracker = TaskTracker()

        state = tracker.load_state(
            workspace
        )

        current = state["current"]

        if current >= len(tasks):

            return {
                "has_task": False,
                "task": None
            }

        return {
            "has_task": True,
            "task": tasks[current],
            "index": current,
            "plan": tasks
        }

    def expand_current_task(
        self,
        workspace: str
    ) -> list[str]:

        task_info = self.get_next_task(
            workspace
        )

        if not task_info["has_task"]:
            return []

        breakdown = TaskBreakdown()

        return breakdown.expand_group(
            task_info["plan"],
            task_info["index"]
        )