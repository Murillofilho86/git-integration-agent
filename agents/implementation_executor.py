from agents.file_snapshot_builder import FileSnapshotBuilder
from agents.implementation_prompt_generator import ImplementationPromptGenerator
from agents.claude_cli_runner import ClaudeCliRunner
from agents.implementation_response_parser import ImplementationResponseParser
from agents.implementation_workspace import ImplementationWorkspace
from agents.claude_json_response_normalizer import ClaudeJsonResponseNormalizer

class ImplementationExecutor:

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

        self._normalizer = (
            ClaudeJsonResponseNormalizer()
        )

        self._parser = (
            ImplementationResponseParser()
        )
        
    def execute(
        self,
        repository: str,
        workspace: str,
        source_branch: str,
        target_branch: str,
        task: dict
    ) -> str:

        implementation_workspace = (
            ImplementationWorkspace(
                workspace
            )
        )

        task_workspace = (
            implementation_workspace.task_directory(
                task["id"]
            )
        )

        snapshot = (
            self._snapshot_builder.build(
                repository,
                source_branch,
                target_branch,
                task
            )
        )

        self._prompt_generator.generate(
           workspace_path=workspace,
           task_workspace=str(task_workspace),
           task=task,
           snapshot=snapshot
        )

        self._runner.run(
            str(
                task_workspace
            ),
            prompt_file="implementation-prompt.md",
            response_file="implementation-response.json",
            session_file="implementation-session.md"
        )

        self._normalizer.normalize(
            workspace=str(task_workspace),
            response_file="implementation-response.json",
            backup_file="implementation-response.original.json"
        )
        
        return (
            self._parser.parse(
                str(
                    task_workspace
                ),
                task
            )
        )