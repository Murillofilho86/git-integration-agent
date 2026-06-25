import json
from pathlib import Path


class IntegrationClassifier:

    def classify(
        self,
        workspace_path: str
    ):

        workspace = Path(workspace_path)

        metadata_file = workspace / "metadata.json"

        if not metadata_file.exists():
            raise FileNotFoundError(
                f"metadata.json não encontrado em {workspace}"
            )

        with open(
            metadata_file,
            encoding="utf-8"
        ) as file:
            metadata = json.load(file)

        commits = metadata["commits"]
        files_changed = metadata["files_changed"]
        age_days = metadata["age_days"]

        reasons = []

        strategy = "A"
        confidence = 0.60

        if age_days > 90:
            strategy = "D"
            confidence = 0.90

            reasons.append(
                "Referência possui mais de 90 dias."
            )

        if files_changed > 100:
            strategy = "D"
            confidence = 0.95

            reasons.append(
                "Mais de 100 arquivos alterados."
            )

        elif commits <= 10 and files_changed <= 20:
            strategy = "A"
            confidence = 0.90

            reasons.append(
                "Poucos commits e poucos arquivos."
            )

        elif commits <= 30 and files_changed <= 50:
            strategy = "B"
            confidence = 0.80

            reasons.append(
                "Volume moderado de alterações."
            )

        elif commits <= 50 and files_changed <= 100:
            strategy = "C"
            confidence = 0.75

            reasons.append(
                "Alterações extensas. Cherry Pick recomendado."
            )

        classification = {
            "source": metadata["source"],
            "target": metadata["target"],
            "strategy": strategy,
            "confidence": confidence,
            "reasons": reasons
        }

        classification_file = (
            workspace /
            "classification.json"
        )

        with open(
            classification_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                classification,
                file,
                indent=4,
                ensure_ascii=False
            )

        return classification