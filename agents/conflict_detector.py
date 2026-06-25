from pathlib import Path
import subprocess


class ConflictDetector:

    def __init__(
        self,
        repo_path: str
    ):
        self.repo_path = Path(
            repo_path
        )

    def analyze(
        self,
        target_ref: str,
        file_path: str,
        summary: list[str]
    ) -> list[dict]:

        target_content = self._load_file(
            target_ref,
            file_path
        )

        results = []

        for item in summary:

            status = self._classify(
                item,
                target_content
            )

            results.append(
                {
                    "item": item,
                    "status": status
                }
            )

        return results

    def _load_file(
        self,
        target_ref: str,
        file_path: str
    ) -> str:

        command = [
            "git",
            "-C",
            str(
                self.repo_path
            ),
            "show",
            f"{target_ref}:{file_path}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        return result.stdout

    def _classify(
        self,
        item: str,
        target_content: str
    ) -> str:

        item_lower = item.lower()

        if "endpoint" in item_lower:

            return self._analyze_endpoint(
                item,
                target_content
            )

        if "nova propriedade:" in item_lower:

            return self._analyze_property(
                item,
                target_content
            )

        if "nova dependência:" in item_lower:

            return self._analyze_dependency(
                item,
                target_content
            )

        if "novo método:" in item_lower:

            return self._analyze_method(
                item,
                target_content
            )

        return "UNKNOWN"

    def _analyze_endpoint(
        self,
        item: str,
        target_content: str
    ) -> str:

        route = (
            item
            .split(
                ":",
                maxsplit=1
            )[1]
            .strip()
        )

        if route in target_content:

            return "ALREADY_EXISTS"

        route_parts = [
            part
            for part in route.split("/")
            if part
        ]

        matches = 0

        for part in route_parts:

            if part.startswith("{"):
                continue

            if part in target_content:

                matches += 1

        if matches >= 2:

            return "CONFLICT"

        return "APPLY"

    def _analyze_property(
        self,
        item: str,
        target_content: str
    ) -> str:

        property_name = (
            item
            .replace(
                "Nova propriedade:",
                ""
            )
            .strip()
        )

        if property_name in target_content:

            return "ALREADY_EXISTS"

        property_tokens = [
            token
            for token in property_name.split()
            if len(token) > 3
        ]

        matches = sum(
            1
            for token in property_tokens
            if token in target_content
        )

        if matches >= 2:

            return "CONFLICT"

        return "APPLY"

    def _analyze_dependency(
        self,
        item: str,
        target_content: str
    ) -> str:

        dependency = (
            item
            .replace(
                "Nova dependência:",
                ""
            )
            .strip()
            .split(".")
            [-1]
        )

        if dependency in target_content:

            return "ALREADY_EXISTS"

        return "APPLY"

    def _analyze_method(
        self,
        item: str,
        target_content: str
    ) -> str:

        signature = (
            item
            .replace(
                "Novo método:",
                ""
            )
            .strip()
        )

        method_name = (
            signature
            .split("(")[0]
            .split()
            [-1]
        )

        if method_name in target_content:

            return "ALREADY_EXISTS"

        return "APPLY"