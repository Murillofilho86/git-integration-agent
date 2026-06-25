from pathlib import Path

import typer

from analyzers.git_analyzer import GitAnalyzer
from generators.analysis_package_generator import (
    AnalysisPackageGenerator
)
from classifiers.integration_classifier import (
    IntegrationClassifier
)
from agents.prompt_generator import (
    PromptGenerator
)

app = typer.Typer()


@app.command()
def analyze(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Caminho do repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch ou referência de origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch ou referência de destino"
    )
):

    git = GitAnalyzer(repo)

    if not git.branch_exists(from_ref):
        raise typer.BadParameter(
            f"Referência não encontrada: {from_ref}"
        )

    if not git.branch_exists(to_ref):
        raise typer.BadParameter(
            f"Referência não encontrada: {to_ref}"
        )

    commits = git.count_commits(
        from_ref,
        to_ref
    )

    files = git.changed_files(
        from_ref,
        to_ref
    )

    age = git.age_days(
        from_ref
    )

    generator = AnalysisPackageGenerator(
        git
    )

    analysis_dir = generator.generate(
        from_ref,
        to_ref
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("ANALYSIS")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"FROM : {from_ref}")
    typer.echo(f"TO   : {to_ref}")
    typer.echo("")
    typer.echo(f"Commits exclusivos : {commits}")
    typer.echo(f"Arquivos alterados : {files}")
    typer.echo(f"Idade da branch    : {age} dias")
    typer.echo("")
    typer.echo("Artefatos gerados em:")
    typer.echo(f"{analysis_dir.resolve()}")
    typer.echo("")


@app.command()
def classify(
    workspace: str = typer.Option(
        ...,
        "--workspace",
        help="Diretório da análise"
    )
):

    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(
            f"Workspace não encontrado: {workspace}"
        )

    classifier = IntegrationClassifier()

    result = classifier.classify(
        workspace
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CLASSIFICATION")
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Strategy  : {result['strategy']}"
    )

    typer.echo(
        f"Confidence: {result['confidence']}"
    )

    typer.echo("")

    typer.echo("Reasons:")

    for reason in result["reasons"]:
        typer.echo(
            f"- {reason}"
        )

    typer.echo("")


@app.command(name="generate-prompt")
def generate_prompt(
    workspace: str = typer.Option(
        ...,
        "--workspace",
        help="Diretório da análise"
    )
):

    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(
            f"Workspace não encontrado: {workspace}"
        )

    generator = PromptGenerator()

    output_file = generator.generate(
        workspace
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("PROMPT GENERATED")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo gerado:")
    typer.echo(output_file)
    typer.echo("")


if __name__ == "__main__":
    app()