# Git Integration Agent

An intelligent branch integration assistant powered by Large Language Models (LLMs).

The Git Integration Agent was created to automate one of the most expensive activities in software development: integrating long-lived Git branches.

Instead of performing a traditional line-based merge, the agent analyzes the semantic differences between two branches, plans the integration, decomposes the work into implementation tasks and reconstructs the final code while preserving the original developer's intent.

The project combines deterministic Git analysis with AI reasoning to significantly reduce manual integration effort while keeping the process reproducible and auditable.

---

# Why this project exists

Traditional Git merge tools are excellent at detecting textual conflicts.

However, they cannot understand:

- semantic changes;
- architectural refactorings;
- renamed abstractions;
- business rule changes;
- dependency migrations;
- long-lived feature branches.

As branches become older, the probability of semantic conflicts increases dramatically.

Developers often spend hours—or even days—performing manual merges.

The Git Integration Agent was designed to solve this problem.

---

# Project Goals

The project has four primary goals.

## Preserve developer intent

Every change performed in the source branch is considered intentional.

The objective is to preserve those changes whenever technically possible.

---

## Reduce manual merge effort

Automate repetitive work involved in semantic branch integration.

---

## Produce deterministic integrations

Although an LLM is used during implementation, the overall workflow is deterministic.

Every execution produces:

- analysis;
- planning;
- implementation history;
- generated files;
- execution artifacts.

---

## Build a reusable AI integration platform

The project is designed as an extensible platform capable of supporting multiple repositories, workflows and LLM providers in the future.

---

# Features

Current capabilities include:

- Git repository analysis
- Source vs target branch comparison
- Integration strategy classification
- Semantic conflict analysis
- Automatic feature planning
- Task decomposition
- File snapshot generation
- Prompt generation
- Claude CLI integration
- AI response normalization
- AI contract validation
- Independent task execution
- Integration history
- Generated file consolidation

---

# High-Level Workflow

```
                Git Repository
                       │
                       ▼
              Repository Analysis
                       │
                       ▼
          Integration Strategy Classification
                       │
                       ▼
                Feature Planning
                       │
                       ▼
               Task Decomposition
                       │
                       ▼
             File Snapshot Generation
                       │
                       ▼
               Prompt Construction
                       │
                       ▼
                  Claude CLI
                       │
                       ▼
            Response Normalization
                       │
                       ▼
              Contract Validation
                       │
                       ▼
             Generated Source Files
                       │
                       ▼
              Final File Consolidation
```

---

# Project Architecture

```
.
├── agents/
├── analyzers/
├── classifiers/
├── contracts/
├── core/
├── docs/
├── generators/
├── implementation/
├── prompts/
├── workspace/
└── app.py
```

## Folder Overview

| Folder | Responsibility |
|----------|----------------|
| agents | Reusable AI and infrastructure components |
| analyzers | Git repository analysis |
| classifiers | Integration strategy classification |
| contracts | AI response contracts |
| core | Application orchestration |
| docs | Project documentation |
| generators | Planning and analysis generators |
| implementation | Implementation pipeline |
| prompts | Prompt templates |
| workspace | Execution artifacts |

---

# Requirements

## Operating System

Recommended:

- Linux

Supported:

- macOS
- Windows (WSL recommended)

---

## Python

Python 3.14 or newer.

Verify:

```bash
python --version
```

---

## Git

Verify:

```bash
git --version
```

---

## Claude CLI

The implementation pipeline currently depends on Claude CLI.

Verify:

```bash
claude --version
```

The Claude CLI must be authenticated before executing implementation commands.

---

# Installation

## Clone the repository

```bash
git clone <repository-url>

cd git-integration-agent
```

---

## Create a virtual environment

```bash
python -m venv .venv
```

---

## Activate the virtual environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Copy:

```text
config.example.json
```

to

```text
config.json
```

Update the configuration according to your environment.

---

# Running the Project

## Analyze a feature branch

```bash
python app.py analyze \
    --repo "<repository>" \
    --from feature \
    --to qa
```

---

## Generate an integration plan

```bash
python app.py plan-feature \
    --repo "<repository>" \
    --from feature \
    --to qa
```

---

## Execute a single task

```bash
python app.py run-task \
    --workspace workspace/<workspace> \
    --repo "<repository>" \
    --from feature \
    --to qa \
    --task 1
```

---

## Execute the complete integration

```bash
python app.py integrate-feature \
    --repo "<repository>" \
    --from feature \
    --to qa
```

---

# Workspace Structure

Every execution creates an isolated workspace.

```
workspace/

└── Repository/

    └── source_vs_target/

        ├── analysis/

        ├── implementation-history/

        │   ├── task-001/

        │   ├── task-002/

        │   └── ...

        └── generated-files/
```

This structure allows executions to be resumed and inspected without affecting previous runs.

---

# Current Project Status

Implemented:

- Repository analysis
- Integration classification
- Feature planning
- Task decomposition
- Independent task execution
- Claude integration
- Response normalization
- AI contract validation
- Generated file consolidation

The project is under active development.

---

# Documentation

Additional documentation is available inside the **docs/** directory.

| Document | Description |
|-----------|-------------|
| getting-started.md | Installation and first execution |
| architecture.md | System architecture |
| workflow.md | Complete execution workflow |
| commands.md | Command reference |
| implementation-pipeline.md | Implementation pipeline |
| prompt-engineering.md | Prompt generation strategy |
| ai-contracts.md | AI contracts |
| workspace.md | Workspace structure |
| troubleshooting.md | Known issues |
| contributing.md | Contribution guidelines |
| decision-log.md | Architectural decisions |
| roadmap.md | Project roadmap |

---

# Design Principles

The project follows a few fundamental principles.

- Single Responsibility Principle
- Deterministic execution
- Explicit AI contracts
- Complete file generation
- Semantic preservation
- Reproducible executions
- Auditability
- Small composable components

---

# Roadmap

Some planned improvements include:

- Prompt budget management
- Incremental snapshot loading
- Resume interrupted executions
- Automatic retry pipeline
- Progress reporting
- Multiple LLM providers
- Parallel task execution
- Automatic validation pipeline
- Better conflict visualization

---

# Contributing

Contributions are welcome.

Before submitting changes:

- Keep components focused on a single responsibility.
- Preserve deterministic behavior.
- Update documentation whenever architecture changes.
- Maintain compatibility with existing AI contracts.
- Prefer small incremental improvements.

---

# License

This project is released under the MIT License.
