from pathlib import Path


class PromptGenerator:

    def generate(
        self,
        workspace_path: str
    ) -> str:

        workspace = Path(
            workspace_path
        )

        metadata = (
            workspace /
            "metadata.json"
        ).read_text(
            encoding="utf-8"
        )

        repository_profile = (
            workspace /
            "repository-profile.json"
        ).read_text(
            encoding="utf-8"
        )

        commits = (
            workspace /
            "commits.txt"
        ).read_text(
            encoding="utf-8"
        )

        files = (
            workspace /
            "files.txt"
        ).read_text(
            encoding="utf-8"
        )

        classification_file = (
            workspace /
            "classification.json"
        )

        classification = ""

        if classification_file.exists():

            classification = (
                classification_file.read_text(
                    encoding="utf-8"
                )
            )

        prompt = f"""
# Branch Integration Analysis

Você é um especialista em:

- Git
- Refatoração
- Engenharia de Software
- Integração de Branches Legadas

---

## Repository Profile

{repository_profile}

---

## Classificação Heurística

{classification}

---

## Metadata

{metadata}

---

## Commits

{commits}

---

## Arquivos Alterados

{files}

---

## Objetivos

Determine:

1. Estratégia recomendada
2. Nível de risco
3. Possíveis conflitos
4. Complexidade
5. Plano de execução
6. Arquivos prioritários
7. Ordem recomendada de implementação

Retorne apenas JSON.
"""

        output_file = (
            workspace /
            "integration-prompt.md"
        )

        output_file.write_text(
            prompt,
            encoding="utf-8"
        )

        return str(
            output_file
        )