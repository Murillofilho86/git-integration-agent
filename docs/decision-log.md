# Decision Log

This document records the most important architectural decisions made during the development of the Git Integration Agent.

Its purpose is to explain *why* the architecture evolved, not only *how* it works.

---

# ADR-001

## Decision

Separate planning from execution.

## Motivation

Planning is deterministic.

Implementation requires semantic reasoning.

Keeping them independent improves reproducibility and debugging.

---

# ADR-002

## Decision

Execute features as independent tasks.

## Motivation

Large prompts reduce AI response quality.

Task decomposition provides:

- smaller prompts
- resumable execution
- easier debugging

---

# ADR-003

## Decision

Store every execution artifact.

## Motivation

Execution history allows:

- auditing
- debugging
- reproducibility

---

# ADR-004

## Decision

Use explicit AI contracts.

## Motivation

AI responses must be deterministic enough to be validated automatically.

---

# ADR-005

## Decision

Normalize AI responses before parsing.

## Motivation

Transport artifacts should be removed before contract validation.

This keeps the parser focused on business validation.

---

# ADR-006

## Decision

Use complete file generation.

## Motivation

Partial snippets increase ambiguity and complicate integration.

Every generated file must be complete.

---

# ADR-007

## Decision

Keep deterministic orchestration outside the LLM.

## Motivation

The language model should perform semantic reasoning only.

Planning, orchestration and validation remain deterministic.

---

# ADR-008

## Decision

Maintain an isolated workspace.

## Motivation

Generated artifacts should never modify the repository directly.

This enables review before integration.

---

# ADR-009

## Decision

Design every pipeline stage with a single responsibility.

## Motivation

Small components are easier to:

- test
- replace
- evolve

without affecting the remaining architecture.

---

# Future Decisions

Future architectural decisions should follow the same structure.

Each new decision should document:

- context
- decision
- motivation
- consequences
