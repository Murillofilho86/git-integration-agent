from pathlib import Path


class AnalysisSummaryGenerator:

    @staticmethod
    def generate(
        output_path: Path,
        source: str,
        target: str,
        commits: int,
        files_changed: int,
        age_days: int,
    ):

        risk = "BAIXO"

        if age_days > 90:
            risk = "ALTO"
        elif age_days > 30:
            risk = "MÉDIO"

        content = f"""# Git Integration Analysis

## Context

Source:
{source}

Target:
{target}

## Metrics

- Commits exclusivos: {commits}
- Arquivos alterados: {files_changed}
- Idade da referência: {age_days} dias

## Risk Assessment

Nível de risco: {risk}

## Observações

Este arquivo é apenas um resumo inicial.

A classificação final deverá ser realizada pelo agente de IA utilizando:

- metadata.json
- commits.txt
- files.txt
- diff.patch
- range-diff.txt

## Próximos Passos

1. Executar classificação da integração
2. Identificar conflitos potenciais
3. Definir estratégia:
   - Merge
   - Rebase
   - Cherry Pick
   - Reimplementação
"""

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content)