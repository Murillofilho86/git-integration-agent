import re


class TaskBreakdown:

    VALID_EXTENSIONS = {
        "cs",
        "csproj",
        "json",
        "xml",
        "config",
        "yml",
        "yaml",
        "sql",
        "sln"
    }

    def _extract_files(
        self,
        line: str
    ) -> list[str]:

        matches = re.findall(
            r'([\w\-/\.]+)',
            line
        )

        files = []

        for match in matches:

            if "/" not in match:
                continue

            filename = (
                match
                .split("/")
                [-1]
            )

            if "." not in filename:
                continue

            extension = (
                filename
                .split(".")
                [-1]
                .lower()
            )

            if extension not in self.VALID_EXTENSIONS:
                continue

            files.append(
                filename
            )

        return files

    def _resolve_action(
        self,
        context: str
    ) -> str:

        context = context.upper()

        if "NOVOS" in context:
            return "Criar"

        if "ALTO RISCO" in context:
            return "Revisar"

        if "CRÍTICO" in context:
            return "Revisar Criticamente"

        if "MÉDIO RISCO" in context:
            return "Alterar"

        return "Analisar"

    def expand_group(
        self,
        plan: list[str],
        current_index: int
    ) -> list[str]:

        if current_index >= len(plan):
            return []

        result = []

        current_action = "Analisar"

        for index in range(
            current_index + 1,
            len(plan)
        ):

            line = plan[index]

            if line.startswith(
                "GRUPO "
            ):
                break

            if (
                "[NOVOS" in line
                or "[ALTO RISCO" in line
                or "[MÉDIO RISCO" in line
                or "[CRÍTICO" in line
            ):

                current_action = (
                    self._resolve_action(
                        line
                    )
                )

            files = self._extract_files(
                line
            )

            for file in files:

                result.append(
                    f"{current_action} {file}"
                )

        return result