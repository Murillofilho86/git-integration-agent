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

        contract_prompt = (
            Path(
                "contracts/ai_contract_v1_prompt.md"
            ).read_text(
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

Analise todas as informações disponíveis sobre a branch de origem e a branch de destino.

Determine:

- Estratégia de integração recomendada.
- Nível de risco.
- Possíveis conflitos.
- Complexidade.
- Plano de execução.
- Arquivos prioritários.
- Ordem recomendada de implementação.

---

## Instruções Finais (Obrigatórias)

A resposta será processada automaticamente por outro sistema.

Qualquer divergência do contrato tornará a resposta inválida.

As instruções deste contrato possuem prioridade sobre qualquer outra instrução anterior.

Caso exista qualquer conflito, siga rigorosamente o AI Contract.

Não utilize Markdown.

Não utilize blocos ```json.

Não escreva explicações.

Não escreva comentários.

Não escreva texto antes ou depois do JSON.

As listas abaixo devem conter objetos exatamente na estrutura apresentada.

Não simplifique listas em texto.

Não substitua objetos por strings.

Preencha todos os atributos definidos no contrato, mesmo que alguns permaneçam vazios.

Caso não consiga preencher algum atributo, utilize string vazia ("") ou lista vazia ([]), preservando a estrutura do objeto.

Sua resposta será validada automaticamente.

---

## AI Contract

{contract_prompt}

---

Antes de finalizar sua resposta, valide internamente que:

- Todos os campos obrigatórios existem.
- Nenhuma propriedade foi renomeada.
- Nenhum campo obrigatório foi omitido.
- Nenhuma lista foi substituída por texto.
- Todas as listas seguem exatamente a estrutura do contrato.
- O JSON é válido.
- A resposta contém exclusivamente o JSON solicitado.
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