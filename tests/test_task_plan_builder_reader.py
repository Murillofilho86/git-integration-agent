import json

from agents.task_plan_builder import TaskPlanBuilder
from agents.task_plan_reader import TaskPlanReader


def write_analysis(tmp_path, implementation_order):
    analysis = {"ordem_recomendada_de_implementacao": implementation_order}
    (tmp_path / "integration-analysis.json").write_text(json.dumps(analysis))


class TestTaskPlanBuilder:

    def test_build_creates_task_plan_from_analysis(self, tmp_path):
        write_analysis(
            tmp_path,
            [
                {
                    "etapa": 1,
                    "lote": "Infrastructure",
                    "motivo": "base layer",
                    "arquivos_chave": ["a.py", "b.py"],
                },
                {
                    "etapa": 2,
                    "lote": "Domain",
                    "motivo": "core models",
                    "arquivos_chave": ["c.py"],
                },
            ],
        )

        output_file = TaskPlanBuilder().build(str(tmp_path))

        plan = json.loads((tmp_path / "task-plan.json").read_text())

        assert output_file == str(tmp_path / "task-plan.json")
        assert plan["current"] == 0
        assert len(plan["tasks"]) == 2
        assert plan["tasks"][0]["id"] == 1
        assert plan["tasks"][0]["title"] == "Infrastructure"
        assert plan["tasks"][0]["status"] == "pending"
        assert plan["tasks"][0]["files"] == ["a.py", "b.py"]

    def test_build_raises_when_analysis_missing(self, tmp_path):
        import pytest

        with pytest.raises(RuntimeError, match="integration-analysis.json"):
            TaskPlanBuilder().build(str(tmp_path))

    def test_build_handles_empty_implementation_order(self, tmp_path):
        write_analysis(tmp_path, [])

        TaskPlanBuilder().build(str(tmp_path))

        plan = json.loads((tmp_path / "task-plan.json").read_text())

        assert plan["tasks"] == []


class TestTaskPlanReader:

    def test_get_tasks_and_total(self, tmp_path):
        write_analysis(
            tmp_path,
            [
                {"etapa": 1, "lote": "A", "motivo": "x", "arquivos_chave": ["a.py"]},
                {"etapa": 2, "lote": "B", "motivo": "y", "arquivos_chave": ["b.py"]},
            ],
        )
        TaskPlanBuilder().build(str(tmp_path))

        reader = TaskPlanReader()

        assert reader.total_tasks(str(tmp_path)) == 2
        assert reader.get_task(str(tmp_path), 0)["title"] == "A"
        assert reader.get_task(str(tmp_path), 1)["title"] == "B"

    def test_get_task_out_of_range_returns_none(self, tmp_path):
        write_analysis(tmp_path, [])
        TaskPlanBuilder().build(str(tmp_path))

        reader = TaskPlanReader()

        assert reader.get_task(str(tmp_path), 0) is None
        assert reader.get_task(str(tmp_path), -1) is None

    def test_load_raises_when_plan_missing(self, tmp_path):
        import pytest

        with pytest.raises(RuntimeError, match="task-plan.json"):
            TaskPlanReader().load(str(tmp_path))
