import json
from pathlib import Path


class PlanImporter:

    def import_plan(
        self,
        workspace: str,
        json_file: str
    ):

        workspace_path = Path(
            workspace
        )

        input_file = Path(
            json_file
        )

        if not input_file.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {json_file}"
            )

        data = json.loads(
            input_file.read_text(
                encoding="utf-8"
            )
        )

        analysis_file = (
            workspace_path /
            "ai-analysis.json"
        )

        analysis_file.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        markdown = []

        markdown.append(
            "# Execution Plan"
        )

        markdown.append("")
        markdown.append(
            "## Strategy"
        )
        markdown.append(
            str(
                data.get(
                    "strategy",
                    ""
                )
            )
        )

        markdown.append("")
        markdown.append(
            "## Confidence"
        )
        markdown.append(
            str(
                data.get(
                    "confidence",
                    ""
                )
            )
        )

        markdown.append("")
        markdown.append(
            "## Risk"
        )
        markdown.append(
            str(
                data.get(
                    "risk",
                    ""
                )
            )
        )

        markdown.append("")
        markdown.append(
            "## Reason"
        )
        markdown.append(
            data.get(
                "reason",
                ""
            )
        )

        markdown.append("")
        markdown.append(
            "## Tasks"
        )
        markdown.append("")

        for index, task in enumerate(
            data.get(
                "plan",
                []
            ),
            start=1
        ):
            markdown.append(
                f"{index}. {task}"
            )

        execution_file = (
            workspace_path /
            "execution-plan.md"
        )

        execution_file.write_text(
            "\n".join(markdown),
            encoding="utf-8"
        )

        return {
            "analysis_file": str(
                analysis_file
            ),
            "execution_file": str(
                execution_file
            )
        }