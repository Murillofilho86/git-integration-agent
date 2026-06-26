from pathlib import Path
import json


class ImplementationPromptGenerator:

    def generate(
        self,
        workspace_path: str,
        task: dict,
        snapshot: dict
    ) -> str:

        workspace = Path(
            workspace_path
        )

        classification = (
            workspace /
            "classification.json"
        ).read_text(
            encoding="utf-8"
        )

        analysis = (
            workspace /
            "integration-analysis.json"
        ).read_text(
            encoding="utf-8"
        )

        prompt = f"""
# Branch Integration Implementation

Você é um Engenheiro de Software Sênior especialista em:

- Git
- Refatoração
- Merge Manual
- Integração de Branches
- Clean Architecture
- C#
- .NET

---

## Classificação

{classification}

---

## Análise

{analysis}

---

## Tarefa Atual

{json.dumps(
    task,
    indent=4,
    ensure_ascii=False
)}

---

## Snapshot dos Arquivos

{json.dumps(
    snapshot,
    indent=4,
    ensure_ascii=False
)}

---

## Objetivo

Implemente exclusivamente esta tarefa.

Considere:

- Branch de origem.
- Branch de destino.
- Estratégia de integração.
- Análise de riscos.
- Ordem recomendada.

---

## Regras

Utilize o conteúdo da branch de origem e da branch de destino presente no snapshot.

Compare ambos os arquivos antes de realizar qualquer alteração.

Preserve alterações existentes na branch de destino que não pertençam à branch de origem.

Implemente exclusivamente as alterações necessárias para esta tarefa.

Nunca altere arquivos que não estejam presentes no snapshot.

Caso seja necessário modificar um arquivo, gere SEMPRE o arquivo completo.

Nunca gere snippets.

Nunca utilize markdown.

Nunca utilize blocos ```.

Nunca explique a solução.

Retorne exclusivamente um JSON válido.

Formato esperado:

{{
    "generated_files": [
        {{
            "path": "",
            "content": ""
        }}
    ]
}}
"""

        output_file = (
            workspace /
            "implementation-prompt.md"
        )

        output_file.write_text(
            prompt,
            encoding="utf-8"
        )

        return str(
            output_file
        )