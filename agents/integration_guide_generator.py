class IntegrationGuideGenerator:

    def generate(
        self,
        file_path: str,
        instructions: list[str],
        related_files: list[str]
    ) -> dict:

        steps = []

        for index, instruction in enumerate(
            instructions,
            start=1
        ):

            steps.append(
                {
                    "order": index,
                    "description": instruction
                }
            )

        return {
            "file": file_path,
            "related_files": related_files,
            "steps": steps
        }