from pathlib import Path


class InstructionGenerator:

    def generate(
        self,
        file_path: str,
        detected_items: list[str]
    ) -> dict:

        instructions = []

        for item in detected_items:

            instructions.append(
                f"Adicionar implementação de {item}"
            )

        return {
            "file": file_path,
            "instructions": instructions
        }