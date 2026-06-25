from pathlib import Path

import typer

from analyzers.git_analyzer import GitAnalyzer
from generators.analysis_package_generator import (
    AnalysisPackageGenerator
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
    typer.echo(f"FROM : {from_ref}")
    typer.echo(f"TO   : {to_ref}")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Commits exclusivos : {commits}")
    typer.echo(f"Arquivos alterados : {files}")
    typer.echo(f"Idade da branch    : {age} dias")
    typer.echo("")
    typer.echo(
        f"Artefatos gerados em:"
    )
    typer.echo(
        f"{analysis_dir.resolve()}"
    )
    typer.echo("")


if __name__ == "__main__":
    app()