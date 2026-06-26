from pathlib import Path
import typer

from agents.change_extractor import ChangeExtractor
from agents.change_summarizer import ChangeSummarizer
from agents.conflict_detector import ConflictDetector
from agents.dependency_conflict_analyzer import DependencyConflictAnalyzer
from agents.execution_navigator import ExecutionNavigator
from agents.file_action_classifier import FileActionClassifier
from agents.implementation_planner import ImplementationPlanner
from agents.integration_scope_builder import IntegrationScopeBuilder
from agents.plan_importer import PlanImporter
from agents.repository_explorer import RepositoryExplorer
from agents.target_validator import TargetValidator
from agents.task_tracker import TaskTracker
from analyzers.git_analyzer import GitAnalyzer
from classifiers.integration_classifier import IntegrationClassifier
from generators.analysis_package_generator import AnalysisPackageGenerator
from agents.change_inspector import ChangeInspector
from agents.instruction_generator import InstructionGenerator
from agents.integration_guide_generator import  IntegrationGuideGenerator
from agents.implementation_plan_generator import ImplementationPlanGenerator
from agents.prompt_generator import PromptGenerator
from agents.claude_cli_runner import ClaudeCliRunner
from agents.claude_response_parser import ClaudeResponseParser

app = typer.Typer()


@app.command()
def analyze(
    repo: str = typer.Option(..., "--repo", help="Caminho do repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch ou referência de origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch ou referência de destino"),
):
    git = GitAnalyzer(repo)

    if not git.branch_exists(from_ref):
        raise typer.BadParameter(f"Referência não encontrada: {from_ref}")

    if not git.branch_exists(to_ref):
        raise typer.BadParameter(f"Referência não encontrada: {to_ref}")

    commits = git.count_commits(from_ref, to_ref)
    files = git.changed_files(from_ref, to_ref)
    age = git.age_days(from_ref)

    generator = AnalysisPackageGenerator(git)
    analysis_dir = generator.generate(from_ref, to_ref)

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
    workspace: str = typer.Option(..., "--workspace", help="Diretório da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    classifier = IntegrationClassifier()
    result = classifier.classify(workspace)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CLASSIFICATION")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Strategy  : {result['strategy']}")
    typer.echo(f"Confidence: {result['confidence']}")
    typer.echo("")
    typer.echo("Reasons:")

    for reason in result["reasons"]:
        typer.echo(f"- {reason}")

    typer.echo("")


@app.command(name="generate-prompt")
def generate_prompt(
    workspace: str = typer.Option(..., "--workspace", help="Diretório da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    generator = PromptGenerator()
    output_file = generator.generate(workspace)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("PROMPT GENERATED")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo("Arquivo gerado:")
    typer.echo(output_file)
    typer.echo("")

@app.command(name="integrate-feature")
def integrate_feature(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
):

    git = GitAnalyzer(
        repo
    )

    generator = (
        AnalysisPackageGenerator(
            git
        )
    )

    workspace = str(
        generator.generate(
            from_ref,
            to_ref
        )
    )

    classifier = (
        IntegrationClassifier()
    )

    result = (
        classifier.classify(
            workspace
        )
    )

    prompt_generator = (
        PromptGenerator()
    )

    prompt_file = (
        prompt_generator.generate(
            workspace
        )
    )

    runner = (
        ClaudeCliRunner()
    )
    
    response_file = (
        runner.run(
            workspace
        )
    )
    
    parser = (
        ClaudeResponseParser()
    )
    
    analysis_file = (
        parser.parse(
            workspace
        )    
    )   
     
    session_file = str(
        Path(
            workspace
        ) /
        "claude-session.md"
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "FEATURE INTEGRATION"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo("Workspace:")
    typer.echo(workspace)
    typer.echo("")

    typer.echo("Strategy:")
    typer.echo(
        result["strategy"]
    )
    typer.echo("")

    typer.echo("Confidence:")
    typer.echo(
        result["confidence"]
    )
    typer.echo("")

    typer.echo("Prompt:")
    typer.echo(
        prompt_file
    )
    typer.echo("")

    typer.echo("Claude Response:")
    typer.echo(
        response_file
    )
    typer.echo("")

    typer.echo("Claude Session:")
    typer.echo(
        session_file
    )
    typer.echo("")
    
    typer.echo("Integration Analysis:")
    typer.echo(analysis_file)
    typer.echo("")

@app.command(name="import-plan")
def import_plan(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
    file: str = typer.Option(..., "--file", help="JSON retornado pelo Claude"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    importer = PlanImporter()
    result = importer.import_plan(workspace, file)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("PLAN IMPORTED")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"AI Analysis : {result['analysis_file']}")
    typer.echo(f"Execution Plan : {result['execution_file']}")
    typer.echo("")


@app.command(name="show-plan")
def show_plan(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    navigator = ExecutionNavigator()
    data = navigator.get_plan(workspace)

    state = data.get("task_state", {})
    completed = state.get("completed", [])
    current = state.get("current", 0)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("EXECUTION PLAN")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Strategy  : {data.get('strategy', '-')}")
    typer.echo(f"Risk      : {str(data.get('risk', '-')).upper()}")
    typer.echo(f"Confidence: {data.get('confidence', '-')}")
    typer.echo("")
    typer.echo("Reason")
    typer.echo("-" * 50)
    typer.echo(data.get("reason", "-"))
    typer.echo("")
    typer.echo("Tasks")
    typer.echo("-" * 50)

    for index, task in enumerate(data.get("plan", [])):
        if index in completed:
            marker = "[x]"
        elif index == current:
            marker = "[>]"
        else:
            marker = "[ ]"

        typer.echo(f"{marker} {index + 1}. {task}")

    typer.echo("")


@app.command(name="next-task")
def next_task(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    navigator = ExecutionNavigator()
    result = navigator.get_next_task(workspace)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("NEXT TASK")
    typer.echo("=" * 50)
    typer.echo("")

    if not result["has_task"]:
        typer.echo("Plano concluído.")
        typer.echo("")
        return

    typer.echo(f"Tarefa #{result['index'] + 1}")
    typer.echo("")
    typer.echo(result["task"])
    typer.echo("")


@app.command(name="complete-task")
def complete_task(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    navigator = ExecutionNavigator()
    plan = navigator.get_plan(workspace)
    total_tasks = len(plan.get("plan", []))

    tracker = TaskTracker()
    result = tracker.complete_current_task(workspace, total_tasks)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("TASK COMPLETED")
    typer.echo("=" * 50)
    typer.echo("")

    if result["finished"]:
        typer.echo("Plano totalmente concluído.")
    else:
        typer.echo("Tarefa marcada como concluída.")

    typer.echo("")


@app.command(name="expand-task")
def expand_task(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    navigator = ExecutionNavigator()
    tasks = navigator.expand_current_task(workspace)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("TASK BREAKDOWN")
    typer.echo("=" * 50)
    typer.echo("")

    if not tasks:
        typer.echo("Nenhuma subtarefa encontrada.")
        typer.echo("")
        return

    for index, task in enumerate(tasks, start=1):
        typer.echo(f"{index}. {task}")

    typer.echo("")


@app.command(name="inspect-file")
def inspect_file(
    workspace: str = typer.Option(..., "--workspace", help="Workspace da análise"),
    repo: str = typer.Option(..., "--repo", help="Caminho do repositório"),
    file: str = typer.Option(..., "--file", help="Arquivo a inspecionar"),
):
    workspace_path = Path(workspace)

    if not workspace_path.exists():
        raise typer.BadParameter(f"Workspace não encontrado: {workspace}")

    explorer = RepositoryExplorer()
    result = explorer.inspect(repo, file)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("FILE INSPECTION")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo: {file}")
    typer.echo(f"Encontrado: {'Sim' if result['exists'] else 'Não'}")
    typer.echo(f"Dependentes: {result['dependent_count']}")
    typer.echo("")

    if result["dependents"]:
        typer.echo("Arquivos impactados:")
        for dependent in result["dependents"]:
            typer.echo(f"- {dependent}")
        typer.echo("")

    if result["locations"]:
        typer.echo("Localizações:")
        for location in result["locations"]:
            typer.echo(f"- {location}")

    typer.echo("")


@app.command(name="extract-change")
def extract_change(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    result = extractor.extract(from_ref, to_ref, file)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CHANGE EXTRACTION")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo: {result['file']}")
    typer.echo("")
    typer.echo(f"Adições: {result['total_additions']}")
    typer.echo(f"Remoções: {result['total_removals']}")
    typer.echo("")

    if result["additions"]:
        typer.echo("Linhas adicionadas:")
        for line in result["additions"][:20]:
            typer.echo(line)
        typer.echo("")

    if result["removals"]:
        typer.echo("Linhas removidas:")
        for line in result["removals"][:20]:
            typer.echo(line)
        typer.echo("")


@app.command(name="summarize-change")
def summarize_change(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    changes = extractor.extract(from_ref, to_ref, file)

    summarizer = ChangeSummarizer()
    summary = summarizer.summarize(changes)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CHANGE SUMMARY")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo: {file}")
    typer.echo("")

    if not summary:
        typer.echo("Nenhuma mudança semântica identificada.")
        typer.echo("")
        return

    typer.echo("Mudanças identificadas:")
    typer.echo("")

    for index, item in enumerate(summary, start=1):
        typer.echo(f"{index}. {item}")

    typer.echo("")


@app.command(name="implementation-plan")
def implementation_plan(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
    file: str = typer.Option(
        ...,
        "--file",
        help="Arquivo para análise"
    ),
):

    extractor = ChangeExtractor(
        repo
    )

    changes = extractor.extract(
        from_ref,
        to_ref,
        file
    )

    summarizer = ChangeSummarizer()

    summary = summarizer.summarize(
        changes
    )

    analyzer = (
        DependencyConflictAnalyzer(
            repo
        )
    )

    dependency_results = (
        analyzer.analyze(
            to_ref,
            summary
        )
    )

    missing_dependencies = [
        item["dependency"]
        for item in dependency_results
        if item["status"] == "MISSING"
    ]

    scope_builder = (
        IntegrationScopeBuilder(
            repo
        )
    )

    scope = scope_builder.build(
        from_ref,
        missing_dependencies,
        file
    )

    consolidated = (
        scope_builder.consolidate_scope(
            scope
        )
    )

    all_files = list(
        set(
            sum(
                (
                    category_files
                    for category_files
                    in consolidated[
                        "categories"
                    ].values()
                ),
                []
            )
        )
    )

    classifier = (
        FileActionClassifier(
            repo
        )
    )

    integration_plan = (
        classifier.classify(
            from_ref,
            to_ref,
            all_files
        )
    )

    inspector = ChangeInspector(
        repo
    )

    change_analysis = (
        inspector.inspect(
            from_ref,
            to_ref,
            file
        )
    )

    instruction_generator = (
        InstructionGenerator()
    )

    instructions = (
        instruction_generator.generate(
            file,
            change_analysis[
                "detected_items"
            ]
        )
    )

    related_files = []

    for item in change_analysis[
        "detected_items"
    ]:

        item_scope = (
            scope_builder.build(
                from_ref,
                [item],
                file
            )
        )

        for dependency in item_scope:

            related_files.extend(
                dependency["files"]
            )

    guide_generator = (
        IntegrationGuideGenerator()
    )

    guide = (
        guide_generator.generate(
            file,
            instructions[
                "instructions"
            ],
            sorted(
                list(
                    set(
                        related_files
                    )
                )
            )
        )
    )

    generator = (
        ImplementationPlanGenerator()
    )

    result = generator.generate(
        file,
        integration_plan,
        guide
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "IMPLEMENTATION PLAN"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Arquivo principal: {result['file']}"
    )

    typer.echo("")

    typer.echo("Resumo")
    typer.echo("-" * 50)

    typer.echo(
        f"Criar   : {result['summary']['create']}"
    )

    typer.echo(
        f"Alterar : {result['summary']['update']}"
    )

    typer.echo(
        f"Validar : {result['summary']['validate']}"
    )

    typer.echo("")

    if result["create"]:

        typer.echo("CRIAR")
        typer.echo("-" * 50)

        for item in result["create"]:

            typer.echo(
                f"- {item}"
            )

        typer.echo("")

    if result["update"]:

        typer.echo("ALTERAR")
        typer.echo("-" * 50)

        for item in result["update"]:

            typer.echo(
                f"- {item}"
            )

        typer.echo("")

    if result["validate"]:

        typer.echo("VALIDAR")
        typer.echo("-" * 50)

        for item in result["validate"]:

            typer.echo(
                f"- {item}"
            )

        typer.echo("")

    typer.echo("GUIA")
    typer.echo("-" * 50)

    for step in result["steps"]:

        typer.echo(
            f"{step['order']}. "
            f"{step['description']}"
        )

    typer.echo("")

@app.command(name="validate-target")
def validate_target(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    changes = extractor.extract(from_ref, to_ref, file)

    summarizer = ChangeSummarizer()
    summary = summarizer.summarize(changes)

    validator = TargetValidator(repo)
    results = validator.validate(to_ref, file, summary)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("TARGET VALIDATION")
    typer.echo("=" * 50)
    typer.echo("")

    for result in results:
        status = "JÁ EXISTE" if result["already_exists"] else "PRECISA APLICAR"
        typer.echo(f"[{status}] {result['item']}")

    typer.echo("")


@app.command(name="detect-conflicts")
def detect_conflicts(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    changes = extractor.extract(from_ref, to_ref, file)

    summarizer = ChangeSummarizer()
    summary = summarizer.summarize(changes)

    detector = ConflictDetector(repo)
    conflicts = detector.analyze(to_ref, file, summary)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CONFLICT ANALYSIS")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo: {file}")
    typer.echo("")

    for item in conflicts:
        status = item["status"]
        if status == "APPLY":
            label = "APLICAR"
        elif status == "ALREADY_EXISTS":
            label = "JÁ EXISTE"
        elif status == "CONFLICT":
            label = "CONFLITO"
        else:
            label = "DESCONHECIDO"

        typer.echo(f"[{label}] {item['item']}")

    typer.echo("")


@app.command(name="analyze-dependencies")
def analyze_dependencies(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    changes = extractor.extract(from_ref, to_ref, file)

    summarizer = ChangeSummarizer()
    summary = summarizer.summarize(changes)

    analyzer = DependencyConflictAnalyzer(repo)
    results = analyzer.analyze(to_ref, summary)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("DEPENDENCY ANALYSIS")
    typer.echo("=" * 50)
    typer.echo("")

    for result in results:
        status = result["status"]
        if status == "FOUND":
            typer.echo(f"[OK] {result['dependency']}")
        elif status == "MISSING":
            typer.echo(f"[AUSENTE] {result['dependency']}")
        elif status == "AMBIGUOUS":
            typer.echo(
                f"[AMBÍGUO] {result['dependency']} ({result['occurrences']} ocorrências)"
            )

    typer.echo("")

@app.command(name="build-scope")
def build_scope(
    repo: str = typer.Option(..., "--repo", help="Repositório Git"),
    from_ref: str = typer.Option(..., "--from", help="Branch origem"),
    to_ref: str = typer.Option(..., "--to", help="Branch destino"),
    file: str = typer.Option(..., "--file", help="Arquivo para análise"),
):
    extractor = ChangeExtractor(repo)
    changes = extractor.extract(from_ref, to_ref, file)

    summarizer = ChangeSummarizer()
    summary = summarizer.summarize(changes)

    analyzer = DependencyConflictAnalyzer(repo)
    dependency_results = analyzer.analyze(to_ref, summary)

    missing_dependencies = [
        item["dependency"]
        for item in dependency_results
        if item["status"] == "MISSING"
    ]

    builder = IntegrationScopeBuilder(repo)
    scope = builder.build(from_ref, missing_dependencies, file)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("INTEGRATION SCOPE")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivo base: {file}")
    typer.echo("")

    for item in scope:
        typer.echo(f"Dependência: {item['dependency']}")

        if not item["files"]:
            typer.echo("  Nenhum arquivo encontrado.")
            typer.echo("")
            continue

        categories = builder.categorize(item["files"])
        total = 0

        for layer, files_found in categories.items():
            if not files_found:
                continue

            total += len(files_found)
            typer.echo("")
            typer.echo(f"{layer} ({len(files_found)})")

            for found_file in files_found:
                typer.echo(f"  - {found_file}")

        typer.echo("")
        typer.echo(f"Total: {total} arquivos")
        typer.echo("")

    consolidated = builder.consolidate_scope(scope)

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo("CONSOLIDATED FEATURE SCOPE")
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(f"Arquivos únicos: {consolidated['total_unique']}")
    typer.echo("")

    for category, files in consolidated["categories"].items():
        if not files:
            continue
        typer.echo(f"{category} ({len(files)})")

    typer.echo("")

    if consolidated["shared_files"]:
        typer.echo("Arquivos compartilhados:")
        for file_name in consolidated["shared_files"]:
            typer.echo(f"- {file_name}")

    typer.echo("")

@app.command(name="build-plan")
def build_plan(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
    file: str = typer.Option(
        ...,
        "--file",
        help="Arquivo para análise"
    )
):

    extractor = ChangeExtractor(
        repo
    )

    changes = extractor.extract(
        from_ref,
        to_ref,
        file
    )

    summarizer = ChangeSummarizer()

    summary = summarizer.summarize(
        changes
    )

    analyzer = (
        DependencyConflictAnalyzer(
            repo
        )
    )

    dependency_results = (
        analyzer.analyze(
            to_ref,
            summary
        )
    )

    missing_dependencies = [
        item["dependency"]
        for item in dependency_results
        if item["status"] == "MISSING"
    ]

    builder = (
        IntegrationScopeBuilder(
            repo
        )
    )

    scope = builder.build(
        from_ref,
        missing_dependencies,
        file
    )

    consolidated = (
        builder.consolidate_scope(
            scope
        )
    )

    classifier = (
        FileActionClassifier(
            repo
        )
    )

    plan = classifier.classify(
        from_ref,
        to_ref,
        list(
            set(
                sum(
                    (
                        category_files
                        for category_files
                        in consolidated[
                            "categories"
                        ].values()
                    ),
                    []
                )
            )
        )
    )

    total_files = (
        len(plan["create"])
        + len(plan["update"])
        + len(plan["validate"])
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "INTEGRATION PLAN"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Arquivos totais: {total_files}"
    )

    typer.echo("")

    if plan["create"]:

        typer.echo(
            f"CRIAR ({len(plan['create'])})"
        )

        for file_name in plan["create"]:

            typer.echo(
                f"  - {file_name}"
            )

        typer.echo("")

    if plan["update"]:

        typer.echo(
            f"ALTERAR ({len(plan['update'])})"
        )

        for file_name in plan["update"]:

            typer.echo(
                f"  - {file_name}"
            )

        typer.echo("")

    if plan["validate"]:

        typer.echo(
            f"VALIDAR ({len(plan['validate'])})"
        )

        for file_name in plan["validate"]:

            typer.echo(
                f"  - {file_name}"
            )

        typer.echo("")

@app.command(name="inspect-change")
def inspect_change(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
    file: str = typer.Option(
        ...,
        "--file",
        help="Arquivo para análise"
    )
):

    inspector = ChangeInspector(
        repo
    )

    result = inspector.inspect(
        from_ref,
        to_ref,
        file
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "FILE CHANGE ANALYSIS"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Arquivo: {result['file']}"
    )

    typer.echo(
        f"Linhas adicionadas: {result['added_count']}"
    )

    typer.echo(
        f"Linhas removidas: {result['removed_count']}"
    )

    typer.echo("")

    if result["detected_items"]:

        typer.echo(
            "Mudanças detectadas:"
        )

        for item in result[
            "detected_items"
        ]:

            typer.echo(
                f"+ {item}"
            )

    typer.echo("")

@app.command(name="generate-instructions")
def generate_instructions(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
    file: str = typer.Option(
        ...,
        "--file",
        help="Arquivo para análise"
    )
):

    inspector = ChangeInspector(
        repo
    )

    analysis = inspector.inspect(
        from_ref,
        to_ref,
        file
    )

    generator = (
        InstructionGenerator()
    )

    result = generator.generate(
        file,
        analysis[
            "detected_items"
        ]
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "IMPLEMENTATION INSTRUCTIONS"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Arquivo: {result['file']}"
    )

    typer.echo("")

    for index, instruction in enumerate(
        result["instructions"],
        start=1
    ):

        typer.echo(
            f"{index}. {instruction}"
        )

    typer.echo("")

@app.command(name="generate-guide")
def generate_guide(
    repo: str = typer.Option(
        ...,
        "--repo",
        help="Repositório Git"
    ),
    from_ref: str = typer.Option(
        ...,
        "--from",
        help="Branch origem"
    ),
    to_ref: str = typer.Option(
        ...,
        "--to",
        help="Branch destino"
    ),
    file: str = typer.Option(
        ...,
        "--file",
        help="Arquivo para análise"
    )
):

    inspector = ChangeInspector(
        repo
    )

    analysis = inspector.inspect(
        from_ref,
        to_ref,
        file
    )

    generator = (
        InstructionGenerator()
    )

    instructions = (
        generator.generate(
            file,
            analysis[
                "detected_items"
            ]
        )
    )

    related_files = []

    scope_builder = (
        IntegrationScopeBuilder(
            repo
        )
    )

    for item in analysis[
        "detected_items"
    ]:

        scope = (
            scope_builder.build(
                from_ref,
                [item],
                file
            )
        )

        for dependency in scope:

            related_files.extend(
                dependency["files"]
            )

    guide_generator = (
        IntegrationGuideGenerator()
    )

    guide = (
        guide_generator.generate(
            file,
            instructions[
                "instructions"
            ],
            sorted(
                list(
                    set(
                        related_files
                    )
                )
            )
        )
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "FEATURE INTEGRATION GUIDE"
    )
    typer.echo("=" * 50)
    typer.echo("")

    typer.echo(
        f"Arquivo principal: {guide['file']}"
    )

    typer.echo("")

    typer.echo(
        f"Arquivos relacionados: "
        f"{len(guide['related_files'])}"
    )

    for related in guide[
        "related_files"
    ]:

        typer.echo(
            f"  - {related}"
        )

    typer.echo("")

    typer.echo("Passos:")

    for step in guide[
        "steps"
    ]:

        typer.echo(
            f"{step['order']}. "
            f"{step['description']}"
        )

    typer.echo("")

@app.command(name="run-claude")
def run_claude(
    workspace: str = typer.Option(
        ...,
        "--workspace",
        help="Diretório da análise"
    ),
):

    workspace_path = Path(
        workspace
    )

    if not workspace_path.exists():

        raise typer.BadParameter(
            f"Workspace não encontrado: {workspace}"
        )

    runner = (
        ClaudeCliRunner()
    )

    response_file = (
        runner.run(
            workspace
        )
    )

    typer.echo("")
    typer.echo("=" * 50)
    typer.echo(
        "CLAUDE EXECUTION"
    )
    typer.echo("=" * 50)
    typer.echo("")
    typer.echo(
        f"Response:"
    )
    typer.echo(
        response_file
    )
    typer.echo("")
    typer.echo(
        "Claude Response:"
    )
    typer.echo(
        response_file
    )

if __name__ == "__main__":
    app()