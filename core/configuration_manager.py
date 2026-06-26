from pathlib import Path
import json


class ConfigurationManager:

    _instance = None

    def __new__(
        cls
    ):

        if cls._instance is None:

            cls._instance = super().__new__(
                cls
            )

            cls._instance._load()

        return cls._instance

    def _load(
        self
    ) -> None:

        self._config_file = Path(
            "config.json"
        )

        if not self._config_file.exists():

            raise RuntimeError(
                "Arquivo config.json não encontrado."
            )

        self._config = json.loads(
            self._config_file.read_text(
                encoding="utf-8"
            )
        )

    def get(
        self,
        key: str,
        default=None
    ):

        return self._config.get(
            key,
            default
        )

    def get_claude_path(
        self
    ) -> str:

        value = self.get(
            "claude_path"
        )

        if not value:

            raise RuntimeError(
                "Configuração 'claude_path' não encontrada."
            )

        return value

    def get_workspace_root(
        self
    ) -> str:

        return self.get(
            "workspace_root",
            "workspace"
        )