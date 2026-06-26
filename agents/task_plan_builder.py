from pathlib import Path
import json


class TaskPlanBuilder:

    def build(
        self,
        workspace_path: str
    ) -> str:

        workspace = Path(
            workspace_path
        )

        analysis_file = (
            workspace /
            "integration-analysis.json"
        )

        if not analysis_file.exists():

            raise RuntimeError(
                "Arquivo integration-analysis.json não encontrado."
            )

        analysis = json.loads(
            analysis_file.read_text(
                encoding="utf-8"
            )
        )

        implementation_order = (
            analysis.get(
                "ordem_recomendada_de_implementacao",
                []
            )
        )

        tasks = []

        for item in implementation_order:

            tasks.append(
                {
                    "id": item["etapa"],
                    "title": item["lote"],
                    "status": "pending",
                    "reason": item["motivo"],
                    "files": item[
                        "arquivos_chave"
                    ]
                }
            )

        task_plan = {
            "current": 0,
            "tasks": tasks
        }

        output_file = (
            workspace /
            "task-plan.json"
        )

        output_file.write_text(
            json.dumps(
                task_plan,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return str(
            output_file
        )