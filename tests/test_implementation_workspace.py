from agents.implementation_workspace import ImplementationWorkspace


class TestImplementationWorkspace:

    def test_task_directory_creates_expected_path(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))

        directory = ws.task_directory(3)

        assert directory == tmp_path / "implementation-history" / "task-003"
        assert directory.exists()

    def test_task_directory_has_content_false_when_missing(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))

        assert ws.task_directory_has_content(1) is False

    def test_task_directory_has_content_false_when_empty(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))
        ws.task_directory(1)

        assert ws.task_directory_has_content(1) is False

    def test_task_directory_has_content_true_when_populated(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))
        directory = ws.task_directory(1)
        (directory / "implementation-response.json").write_text("{}")

        assert ws.task_directory_has_content(1) is True

    def test_archive_task_directory_noop_when_empty(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))

        assert ws.archive_task_directory(1) is None

    def test_archive_task_directory_moves_content_out_of_history(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))
        directory = ws.task_directory(2)
        (directory / "implementation-response.json").write_text("garbage")

        archived = ws.archive_task_directory(2)

        assert archived is not None
        assert archived.exists()
        assert (archived / "implementation-response.json").read_text() == "garbage"
        assert "implementation-history-failed" in str(archived)

        # A fresh call to task_directory() must yield a clean, empty directory,
        # and the merger's "task-*" glob under implementation-history/ must
        # never see the archived (failed) attempt.
        fresh_directory = ws.task_directory(2)
        assert list(fresh_directory.iterdir()) == []
        assert not any(
            "failed" in p.name
            for p in ws.history_directory().glob("task-*")
        )

    def test_archive_is_idempotent_on_second_call(self, tmp_path):
        ws = ImplementationWorkspace(str(tmp_path))
        directory = ws.task_directory(1)
        (directory / "x.txt").write_text("data")

        first = ws.archive_task_directory(1)
        second = ws.archive_task_directory(1)

        assert first is not None
        assert second is None
