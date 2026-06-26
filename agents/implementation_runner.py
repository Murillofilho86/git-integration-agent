from agents.file_snapshot_builder import (
    FileSnapshotBuilder
)

from agents.implementation_prompt_generator import (
    ImplementationPromptGenerator
)

from agents.claude_cli_runner import (
    ClaudeCliRunner
)


class ImplementationRunner:

    def __init__(
        self
    ):

        self._snapshot_builder = (
            FileSnapshotBuilder()
        )

        self._prompt_generator = (
            ImplementationPromptGenerator()
        )

        self._runner = (
            ClaudeCliRunner()
        )

    def run(
        self,
        repository: str,
        workspace: str,
        source_branch: str,
        target_branch: str,
        task: dict
    ) -> str:

        snapshot = (
            self._snapshot_builder.build(
                repository,
                source_branch,
                target_branch,
                task
            )
        )

        self._prompt_generator.generate(
            workspace,
            task,
            snapshot
        )

        return (
            self._runner.run(
                workspace,
                prompt_file="implementation-prompt.md",
                response_file="implementation-response.json",
                session_file="implementation-session.md"
            )
        )