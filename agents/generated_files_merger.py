from pathlib import Path
import shutil


class GeneratedFilesMerger:

    def merge(
        self,
        workspace: str
    ) -> str:

        workspace_path = Path(
            workspace
        )

        history_directory = (
            workspace_path /
            "implementation-history"
        )

        output_directory = (
            workspace_path /
            "generated-files"
        )

        if output_directory.exists():

            shutil.rmtree(
                output_directory
            )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        if not history_directory.exists():

            return str(
                output_directory
            )

        task_directories = sorted(
            history_directory.glob(
                "task-*"
            )
        )

        for task_directory in (
            task_directories
        ):

            generated_directory = (
                task_directory /
                "generated-files"
            )

            if not generated_directory.exists():

                continue

            for source_file in (
                generated_directory.rglob(
                    "*"
                )
            ):

                if not source_file.is_file():

                    continue

                relative_path = (
                    source_file.relative_to(
                        generated_directory
                    )
                )

                destination_file = (
                    output_directory /
                    relative_path
                )

                destination_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                if destination_file.exists():

                    raise RuntimeError(
                        (
                            "Arquivo duplicado detectado "
                            f"durante a consolidação: "
                            f"{relative_path}"
                        )
                    )
                    
                shutil.copy2(
                    source_file,
                    destination_file
                )

        return str(
            output_directory
        )