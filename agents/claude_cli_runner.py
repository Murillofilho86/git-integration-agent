from pathlib import Path
import subprocess
import json

from core.configuration_manager import ConfigurationManager



class ClaudeCliRunner:

    def __init__(
        self
    ):

        self._configuration = (
            ConfigurationManager()
        )

    def _get_claude_path(
        self
    ) -> str:

        configuration = (
            self._configuration.load()
        )

        claude_path = (
            configuration.get(
                "claude_path"
            )
        )

        if not claude_path:

            raise RuntimeError(
                "Configuração 'claude_path' não encontrada."
            )

        if not Path(
            claude_path
        ).exists():

            raise RuntimeError(
                f"Claude CLI não encontrado: {claude_path}"
            )

        return claude_path

    def run(
        self,
        workspace_path: str,
        prompt_file: str = "integration-prompt.md",
        response_file: str = "claude-response.json",
        session_file: str = "claude-session.md"
    ) -> str:

        workspace = Path(
            workspace_path
        )

        prompt = (
            workspace /
            prompt_file
        )

        if not prompt.exists():

            raise RuntimeError(
                f"Prompt não encontrado: {prompt}"
            )

        claude_path = (
            self._get_claude_path()
        )

        result = subprocess.run(
            [
                claude_path,
                "--print"
            ],
            input=prompt.read_text(
                encoding="utf-8"
            ),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr
            )

        response_json = {
            "result": result.stdout
        }

        response_output = (
            workspace /
            response_file
        )

        response_output.write_text(
            json.dumps(
                response_json,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        session_output = (
            workspace /
            session_file
        )

        session_output.write_text(
            result.stdout,
            encoding="utf-8"
        )

        return str(
            response_output
        )