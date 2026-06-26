from pathlib import Path
import json
import subprocess


class ClaudeCliRunner:

    def _get_claude_path(
        self
    ) -> str:

        config_file = Path(
            "config.json"
        )

        if not config_file.exists():

            raise RuntimeError(
                "Arquivo config.json não encontrado."
            )

        config = json.loads(
            config_file.read_text(
                encoding="utf-8"
            )
        )

        claude_path = config.get(
            "claude_path"
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
        workspace_path: str
    ) -> str:

        workspace = Path(
            workspace_path
        )

        prompt_file = (
            workspace /
            "integration-prompt.md"
        )

        if not prompt_file.exists():

            raise RuntimeError(
                "Arquivo integration-prompt.md não encontrado."
            )

        prompt = (
            prompt_file.read_text(
                encoding="utf-8"
            )
        )

        result = subprocess.run(
            [
                self._get_claude_path(),
                "-p",
                prompt,
                "--output-format",
                "json"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr
            )

        response_json = json.loads(
            result.stdout
        )

        if response_json.get(
            "is_error"
        ):

            raise RuntimeError(
                response_json.get(
                    "result",
                    "Erro desconhecido retornado pelo Claude."
                )
            )

        response_content = (
            result.stdout
        )

        response_file = (
            workspace /
            "claude-response.json"
        )

        response_file.write_text(
            response_content,
            encoding="utf-8"
        )

        session_file = (
            workspace /
            "claude-session.md"
        )

        session_file.write_text(
            f"""# Claude Session

## Prompt

{prompt}

---

## Response

{response_content}
""",
            encoding="utf-8"
        )

        return str(
            response_file
        )