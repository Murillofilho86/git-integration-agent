import subprocess

from agents.dependency_conflict_analyzer import DependencyConflictAnalyzer


def fake_run_factory(occurrences_by_name: dict):
    def _fake_run(command, **kwargs):
        # command looks like ["git", "-C", repo, "grep", name, ref]
        name = command[4]
        count = occurrences_by_name.get(name, 0)
        stdout = "\n".join(f"file{i}.txt:match" for i in range(count))
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    return _fake_run


class TestDependencyConflictAnalyzer:

    def test_missing_dependency(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", fake_run_factory({}))

        analyzer = DependencyConflictAnalyzer(repo_path="/unused")
        results = analyzer.analyze("target", ["Nova dependência: System.Text.Json"])

        assert results == [{"dependency": "Json", "status": "MISSING"}]

    def test_found_dependency(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", fake_run_factory({"Json": 3}))

        analyzer = DependencyConflictAnalyzer(repo_path="/unused")
        results = analyzer.analyze("target", ["Nova dependência: System.Text.Json"])

        assert results == [
            {"dependency": "Json", "status": "FOUND", "occurrences": 3}
        ]

    def test_ambiguous_dependency_above_threshold(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", fake_run_factory({"Json": 25}))

        analyzer = DependencyConflictAnalyzer(repo_path="/unused")
        results = analyzer.analyze("target", ["Nova dependência: System.Text.Json"])

        assert results[0]["status"] == "AMBIGUOUS"
        assert results[0]["occurrences"] == 25

    def test_ignores_items_that_are_not_dependencies(self, monkeypatch):
        monkeypatch.setattr(subprocess, "run", fake_run_factory({}))

        analyzer = DependencyConflictAnalyzer(repo_path="/unused")
        results = analyzer.analyze(
            "target",
            ["Novo endpoint GET: /users", "Nova propriedade: Name"],
        )

        assert results == []

    def test_react_summary_with_no_dependency_items_yields_empty_results(
        self, monkeypatch
    ):
        # React/TS source produces no "Nova dependência:" items at all
        # (see test_change_summarizer.py), so analyze() must simply
        # return an empty list without ever calling git.
        calls = []
        monkeypatch.setattr(
            subprocess, "run", lambda *a, **k: calls.append(a) or fake_run_factory({})(*a, **k)
        )

        analyzer = DependencyConflictAnalyzer(repo_path="/unused")
        results = analyzer.analyze("target", [])

        assert results == []
        assert calls == []
