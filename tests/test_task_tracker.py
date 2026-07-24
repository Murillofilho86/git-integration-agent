import json

from core.task_tracker import TaskTracker


class TestTaskTracker:

    def test_load_state_creates_default_when_missing(self, tmp_path):
        state = TaskTracker().load_state(str(tmp_path))

        assert state == {"current": 0, "completed": []}
        assert (tmp_path / "task-state.json").exists()

    def test_save_and_load_round_trip(self, tmp_path):
        tracker = TaskTracker()
        tracker.save_state(str(tmp_path), {"current": 2, "completed": [0, 1]})

        state = tracker.load_state(str(tmp_path))

        assert state == {"current": 2, "completed": [0, 1]}

    def test_reset_state_overwrites_existing_progress(self, tmp_path):
        tracker = TaskTracker()
        tracker.save_state(str(tmp_path), {"current": 5, "completed": [0, 1, 2, 3, 4]})

        tracker.reset_state(str(tmp_path))

        state = json.loads((tmp_path / "task-state.json").read_text())
        assert state == {"current": 0, "completed": []}

    def test_complete_current_task_advances_and_marks_completed(self, tmp_path):
        write_two_task_plan(tmp_path)

        tracker = TaskTracker()
        result = tracker.complete_current_task(str(tmp_path))

        assert result == {"completed": True, "finished": False}
        state = tracker.load_state(str(tmp_path))
        assert state == {"current": 1, "completed": [0]}

    def test_complete_current_task_reports_finished_on_last_task(self, tmp_path):
        write_two_task_plan(tmp_path)

        tracker = TaskTracker()
        tracker.complete_current_task(str(tmp_path))
        result = tracker.complete_current_task(str(tmp_path))

        assert result == {"completed": True, "finished": True}

    def test_complete_current_task_noop_when_already_finished(self, tmp_path):
        write_two_task_plan(tmp_path)

        tracker = TaskTracker()
        tracker.complete_current_task(str(tmp_path))
        tracker.complete_current_task(str(tmp_path))
        result = tracker.complete_current_task(str(tmp_path))

        assert result == {"completed": False, "finished": True}


def write_two_task_plan(tmp_path):
    plan = {
        "current": 0,
        "tasks": [
            {"id": 1, "title": "A", "files": ["a.py"]},
            {"id": 2, "title": "B", "files": ["b.py"]},
        ],
    }
    (tmp_path / "task-plan.json").write_text(json.dumps(plan))
