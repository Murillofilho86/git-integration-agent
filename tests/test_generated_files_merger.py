import pytest

from agents.generated_files_merger import GeneratedFilesMerger


class TestGeneratedFilesMerger:

    def test_merge_returns_empty_directory_when_no_history(self, tmp_path):
        output = GeneratedFilesMerger().merge(str(tmp_path))

        assert output == str(tmp_path / "generated-files")
        assert (tmp_path / "generated-files").exists()

    def test_merge_consolidates_files_from_multiple_tasks(self, tmp_path):
        history = tmp_path / "implementation-history"

        task1_files = history / "task-001" / "generated-files"
        task1_files.mkdir(parents=True)
        (task1_files / "a.py").write_text("task 1")

        task2_files = history / "task-002" / "generated-files"
        task2_files.mkdir(parents=True)
        (task2_files / "sub" / "b.py").parent.mkdir(parents=True)
        (task2_files / "sub" / "b.py").write_text("task 2")

        output = GeneratedFilesMerger().merge(str(tmp_path))
        output_path = tmp_path / "generated-files"

        assert output == str(output_path)
        assert (output_path / "a.py").read_text() == "task 1"
        assert (output_path / "sub" / "b.py").read_text() == "task 2"

    def test_merge_ignores_failed_history_directory(self, tmp_path):
        # Files archived by ImplementationWorkspace.archive_task_directory()
        # live in implementation-history-failed/, a sibling directory --
        # the merger must never pick those up.
        failed = tmp_path / "implementation-history-failed" / "task-001-123"
        failed.mkdir(parents=True)
        (failed / "generated-files").mkdir()
        (failed / "generated-files" / "stale.py").write_text("stale")

        output_path = tmp_path / "generated-files"
        GeneratedFilesMerger().merge(str(tmp_path))

        assert not (output_path / "stale.py").exists()

    def test_merge_raises_on_duplicate_generated_file(self, tmp_path):
        history = tmp_path / "implementation-history"

        for task_id in ("task-001", "task-002"):
            files_dir = history / task_id / "generated-files"
            files_dir.mkdir(parents=True)
            (files_dir / "same.py").write_text(task_id)

        with pytest.raises(RuntimeError, match="duplicado"):
            GeneratedFilesMerger().merge(str(tmp_path))

    def test_merge_is_technology_agnostic(self, tmp_path):
        # The merger only moves files around by path -- it must not care
        # whether the generated content is C#, TSX or Python.
        history = tmp_path / "implementation-history"
        files_dir = history / "task-001" / "generated-files"
        files_dir.mkdir(parents=True)
        (files_dir / "Component.tsx").write_text("export const X = () => null;")
        (files_dir / "Service.cs").write_text("public class Service {}")

        GeneratedFilesMerger().merge(str(tmp_path))
        output_path = tmp_path / "generated-files"

        assert (output_path / "Component.tsx").exists()
        assert (output_path / "Service.cs").exists()
