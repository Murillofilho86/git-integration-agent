import re


class ChangeSummarizer:

    def summarize(
        self,
        change_result: dict
    ) -> list[str]:

        summary = []

        additions = change_result.get(
            "additions",
            []
        )

        removals = change_result.get(
            "removals",
            []
        )

        for line in additions:

            content = line.lstrip("+").strip()

            if content.startswith(
                "using "
            ):

                dependency = (
                    content
                    .replace(
                        "using ",
                        ""
                    )
                    .replace(
                        ";",
                        ""
                    )
                )

                summary.append(
                    f"Nova dependência: {dependency}"
                )

            elif "app.MapGet" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Novo endpoint GET: {route}"
                )

            elif "app.MapPost" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Novo endpoint POST: {route}"
                )

            elif "app.MapPut" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Novo endpoint PUT: {route}"
                )

            elif "app.MapDelete" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Novo endpoint DELETE: {route}"
                )

            elif (
                content.startswith(
                    "public "
                )
                and "{ get; set; }"
                in content
            ):

                summary.append(
                    f"Nova propriedade: {content}"
                )

            elif (
                "Task<"
                in content
                or content.startswith(
                    "private "
                )
                or content.startswith(
                    "public "
                )
            ) and "(" in content:

                summary.append(
                    f"Novo método: {content}"
                )

        for line in removals:

            content = line.lstrip("-").strip()

            if "app.MapGet" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Endpoint removido: {route}"
                )

            elif "app.MapPost" in content:

                route = self._extract_route(
                    content
                )

                summary.append(
                    f"Endpoint removido: {route}"
                )

        return list(
            dict.fromkeys(
                summary
            )
        )

    def _extract_route(
        self,
        line: str
    ) -> str:

        match = re.search(
            r'"([^"]+)"',
            line
        )

        if match:

            return match.group(
                1
            )

        return "rota não identificada"