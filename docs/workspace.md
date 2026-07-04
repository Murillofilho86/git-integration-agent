# Workspace

The workspace is the execution environment used by the Git Integration Agent.

Every analysis, planning and implementation artifact is stored inside the workspace.

The workspace allows executions to be:

- reproducible;
- resumable;
- auditable;
- independent from the original repository.

Nothing stored inside the workspace should be considered source code.

Everything can be regenerated.

---

# Workspace Philosophy

The project never writes directly into the target repository.

Instead, every generated artifact is stored inside an isolated workspace.

Only after the implementation has been reviewed should the generated files be copied into the destination repository.

This minimizes risk and makes every execution inspectable.

---

# Directory Structure

A typical workspace looks like:

```
workspace/

└── Repository/

    └── source_vs_target/

        ├── analysis/

        ├── implementation-history/

        ├── generated-files/

        ├── task-plan.json

        ├── metadata.json

        └── classification.json
```

---

# analysis/

Contains every artifact produced during repository analysis.

Examples include:

- branch comparison
- metadata
- integration strategy
- detected changes

These files are deterministic.

---

# implementation-history/

Stores every implementation executed by the AI.

Example:

```
implementation-history/

    task-001/

    task-002/

    task-003/
```

Each task has its own isolated directory.

---

# Task Directory

Example:

```
task-003/

    implementation-prompt.md

    implementation-response.json

    implementation-response.original.json

    implementation-session.md

    generated-files/
```

---

# implementation-prompt.md

Prompt submitted to the language model.

Keeping the prompt allows:

- debugging
- reproducibility
- prompt evolution

---

# implementation-response.original.json

Raw response returned by the AI.

This file should never be modified.

It represents the original execution output.

---

# implementation-response.json

Normalized response after preprocessing.

This file is consumed by the parser.

---

# implementation-session.md

Execution log produced during the interaction with the AI.

Useful for debugging unexpected behavior.

---

# generated-files/

Contains the generated implementation for a single task.

Example:

```
generated-files/

src/

tests/
```

Only files belonging to that task should exist inside this directory.

---

# Root generated-files/

After all tasks finish successfully, generated files may be consolidated into:

```
generated-files/
```

This directory represents the final implementation output.

---

# Cleaning the Workspace

The workspace is disposable.

To remove every generated artifact:

```bash
rm -rf workspace
```

The next execution recreates everything.

---

# Benefits

The workspace provides:

- execution history
- debugging support
- reproducibility
- isolation
- auditing
- resumable execution

---

# Best Practices

- Never edit generated artifacts manually.
- Preserve failed executions for investigation.
- Delete the workspace only when a fresh execution is desired.
- Review generated files before copying them into the repository.

---

# Next Document

Continue with:

```
troubleshooting.md
```
