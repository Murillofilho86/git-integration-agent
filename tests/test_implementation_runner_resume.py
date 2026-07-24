import json

import pytest

from agents.implementation_runner import ImplementationRunner
from agents.implementation_executor import ImplementationExecutor
from agents.generated_files_merger import GeneratedFilesMerger
from core.configuration_manager import ConfigurationManager


@pytest.fixture(autouse=True)
def isolated_configuration(tmp_path_factory, monkeypatch):
    # ImplementationRunner -> ImplementationExecutor -> ClaudeCliRunner
    # all instantiate the ConfigurationManager singleton, which reads
    # ./config.json relative to the CWD. Give each test its own CWD
    # with a minimal config.json, and reset the singleton around it.
    config_dir = tmp_path_factory.mktemp("config")
    (config_dir / "config.json").write_text(
        json.dumps({"claude_path": "/usr/bin/true"})
    )
    monkeypatch.chdir(config_dir)
    ConfigurationManager._instance = None
    yield
    ConfigurationManager._instance = None


def write_task_plan(tmp_path):
    plan = {
        "current": 0,
        "tasks": [
            {"id": 1, "title": "Task A", "files": ["a.py"]},
            {"id": 2, "title": "Task B", "files": ["b.py"]},
            {"id": 3, "title": "Task C", "files": ["c.py"]},
        ],
    }
    (tmp_path / "task-plan.json").write_text(json.dumps(plan))


@pytest.fixture
def stub_merge(monkeypatch):
    monkeypatch.setattr(
        GeneratedFilesMerger, "merge", lambda self, workspace: "merged-output"
    )


class TestImplementationRunnerResume:

    def test_full_run_executes_every_task_in_order(self, tmp_path, monkeypatch, stub_merge):
        write_task_plan(tmp_path)
        calls = []

        monkeypatch.setattr(
            ImplementationExecutor,
            "execute",
            lambda self, **kwargs: calls.append(kwargs["task"]["id"]),
        )

        result = ImplementationRunner().run(
            repository="repo",
            workspace=str(tmp_path),
            source_branch="feature",
            target_branch="qa",
            resume=False,
        )

        assert calls == [1, 2, 3]
        assert result == "merged-output"

        state = json.loads((tmp_path / "task-state.json").read_text())
        assert state == {"current": 3, "completed": [0, 1, 2]}

    def test_failure_preserves_progress_for_later_resume(self, tmp_path, monkeypatch, stub_merge):
        write_task_plan(tmp_path)
        calls = []

        def fake_execute(self, **kwargs):
            task_id = kwargs["task"]["id"]
            calls.append(task_id)
            if task_id == 3:
                raise RuntimeError("simulated Claude/contract failure")

        monkeypatch.setattr(ImplementationExecutor, "execute", fake_execute)

        with pytest.raises(RuntimeError, match="simulated"):
            ImplementationRunner().run(
                repository="repo",
                workspace=str(tmp_path),
                source_branch="feature",
                target_branch="qa",
                resume=False,
            )

        assert calls == [1, 2, 3]
        state = json.loads((tmp_path / "task-state.json").read_text())
        assert state == {"current": 2, "completed": [0, 1]}

    def test_resume_skips_completed_tasks_and_retries_only_the_failed_one(
        self, tmp_path, monkeypatch, stub_merge
    ):
        write_task_plan(tmp_path)
        calls = []
        attempts_on_task_3 = {"count": 0}

        def fake_execute(self, **kwargs):
            task_id = kwargs["task"]["id"]
            calls.append(task_id)
            if task_id == 3:
                attempts_on_task_3["count"] += 1
                if attempts_on_task_3["count"] == 1:
                    raise RuntimeError("first attempt fails")

        monkeypatch.setattr(ImplementationExecutor, "execute", fake_execute)

        runner = ImplementationRunner()

        with pytest.raises(RuntimeError):
            runner.run(
                repository="repo", workspace=str(tmp_path),
                source_branch="feature", target_branch="qa", resume=False,
            )

        calls.clear()
        result = runner.run(
            repository="repo", workspace=str(tmp_path),
            source_branch="feature", target_branch="qa", resume=True,
        )

        assert calls == [3]
        assert result == "merged-output"

        state = json.loads((tmp_path / "task-state.json").read_text())
        assert state == {"current": 3, "completed": [0, 1, 2]}

    def test_non_resume_run_always_restarts_from_scratch(self, tmp_path, monkeypatch, stub_merge):
        write_task_plan(tmp_path)
        calls = []

        monkeypatch.setattr(
            ImplementationExecutor,
            "execute",
            lambda self, **kwargs: calls.append(kwargs["task"]["id"]),
        )

        runner = ImplementationRunner()
        runner.run(
            repository="repo", workspace=str(tmp_path),
            source_branch="feature", target_branch="qa", resume=False,
        )

        calls.clear()
        runner.run(
            repository="repo", workspace=str(tmp_path),
            source_branch="feature", target_branch="qa", resume=False,
        )

        assert calls == [1, 2, 3]

    def test_resume_with_no_prior_state_behaves_like_a_fresh_run(
        self, tmp_path, monkeypatch, stub_merge
    ):
        write_task_plan(tmp_path)
        calls = []

        monkeypatch.setattr(
            ImplementationExecutor,
            "execute",
            lambda self, **kwargs: calls.append(kwargs["task"]["id"]),
        )

        ImplementationRunner().run(
            repository="repo", workspace=str(tmp_path),
            source_branch="feature", target_branch="qa", resume=True,
        )

        assert calls == [1, 2, 3]

    def test_stale_failed_attempt_is_archived_before_retry(
        self, tmp_path, monkeypatch, stub_merge
    ):
        write_task_plan(tmp_path)

        # Simulate a crashed previous attempt that left files behind for
        # task 2, but never advanced task-state.json past task 1.
        (tmp_path / "task-state.json").write_text(
            json.dumps({"current": 1, "completed": [0]})
        )
        stale_dir = tmp_path / "implementation-history" / "task-002"
        stale_dir.mkdir(parents=True)
        (stale_dir / "implementation-response.json").write_text("garbage")

        monkeypatch.setattr(
            ImplementationExecutor, "execute", lambda self, **kwargs: None
        )

        ImplementationRunner().run(
            repository="repo", workspace=str(tmp_path),
            source_branch="feature", target_branch="qa", resume=True,
        )

        failed_root = tmp_path / "implementation-history-failed"
        assert failed_root.exists()
        archived = list(failed_root.glob("task-002-*"))
        assert len(archived) == 1
        assert (archived[0] / "implementation-response.json").read_text() == "garbage"
