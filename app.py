import typer

from git_analyzer import GitAnalyzer

app = typer.Typer()

@app.command()
def analyze(
    from_ref: str = typer.Option(..., "--from"),
    to_ref: str = typer.Option(..., "--to")
):

    git = GitAnalyzer()

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

    print()
    print(f"FROM: {from_ref}")
    print(f"TO: {to_ref}")
    print()
    print(f"Commits: {commits}")
    print(f"Files: {files}")
    print(f"Age: {age} days")
    print()

if __name__ == "__main__":
    app()