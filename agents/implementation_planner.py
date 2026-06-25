class ImplementationPlanner:

    def build_plan(
        self,
        file_name: str,
        summary: list[str]
    ) -> list[str]:

        plan = []

        for item in summary:

            if item.startswith(
                "Nova dependência:"
            ):

                dependency = (
                    item.replace(
                        "Nova dependência:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Adicionar import/dependência: {dependency}"
                )

            elif item.startswith(
                "Novo endpoint GET:"
            ):

                route = (
                    item.replace(
                        "Novo endpoint GET:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Adicionar endpoint GET: {route}"
                )

            elif item.startswith(
                "Novo endpoint POST:"
            ):

                route = (
                    item.replace(
                        "Novo endpoint POST:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Adicionar endpoint POST: {route}"
                )

            elif item.startswith(
                "Novo endpoint PUT:"
            ):

                route = (
                    item.replace(
                        "Novo endpoint PUT:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Adicionar endpoint PUT: {route}"
                )

            elif item.startswith(
                "Endpoint removido:"
            ):

                route = (
                    item.replace(
                        "Endpoint removido:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Remover endpoint: {route}"
                )

            elif item.startswith(
                "Nova propriedade:"
            ):

                property_name = (
                    item.replace(
                        "Nova propriedade:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Adicionar propriedade: {property_name}"
                )

            elif item.startswith(
                "Novo método:"
            ):

                method_name = (
                    item.replace(
                        "Novo método:",
                        ""
                    )
                    .strip()
                )

                plan.append(
                    f"Implementar método: {method_name}"
                )

        return plan