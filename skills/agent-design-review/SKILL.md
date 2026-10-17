---
name: agent-design-review
description: Design or improve agents and skills by moving repeated model decisions into tools, reusable components, schemas, and templates before adding checks or prose rules. Use when creating an agent or skill, reviewing its design, or fixing recurring workflow failures. Do not trigger merely to execute an existing skill or produce a document. 日本語トリガー - エージェントを設計して / スキルを作って / スキルを改善して / Agentの品質を安定させたい。
---

# Agent Design Review

Make the easiest supported operation produce a valid result. First improve the environment and tools so the model has fewer mechanical decisions to repeat. Preserve the judgment and expressive choices needed for the user's task.

## Improvement order

1. **Environment, tools, and structure.** Move recurring mechanics into code, typed operations, reusable components, schemas, and templates. Make constraints executable at the boundary that accepts model output.
2. **Automated checks.** Detect errors that remain, using deterministic checks where possible and the actual rendered or recalculated artifact when needed.
3. **Prompts and skills.** Explain choices that still need judgment: interpreting intent, selecting a component, resolving ambiguity, or choosing what matters.
4. **Human review.** Focus attention on meaning, business assumptions, and decisions that cannot yet be checked reliably.

This orders design investment, not a mandatory four-stage project. Pair a focused structural fix with its relevant check; do not wait for a complete redesign. Contain an active incident promptly, then apply this order to its durable fix. Do not remove useful checks or review before their replacement works.

## Review the actual workflow

- Inspect the relevant skill and its scripts, assets, references, tool interfaces, and callers. Use available failures or user corrections as evidence; do not invent incident counts or require a fixed-size dataset before helping.
- Identify what the model repeatedly decides or reconstructs: coordinates, formatting, formulas, paths, command sequences, or intermediate representations. Separate those mechanics from necessary semantic judgment.
- For each recurring decision, ask whether an existing tool or a small reusable component can own it. Prefer a narrow, useful change over building a general framework.
- Define what the model selects or supplies, what code derives, and what the boundary rejects or handles. Validate actual inputs at that boundary; instructions to emit JSON alone do not enforce a schema.
- Preserve legitimate user choices. Constrain mechanics where it helps reliability; support required variation through explicit parameters or an appropriate alternate workflow. A fixed template is not suitable for every task.

When working on a skill, consider `scripts/` for repeatable execution, `assets/` for templates, and schemas for structured inputs before adding instructions to `SKILL.md`. Create only resources the workflow will use, and connect them to the execution path. Keep judgment guidance in the skill and conditional details in references. Do not duplicate constraints already enforced by code.

Read [references/artifact-examples.md](references/artifact-examples.md) for slide, spreadsheet, or Excel agent designs, or when an example is needed to clarify the model/tool boundary. These are applications of the principle, not requirements for unrelated agents.

## Choose and validate a change

For each material recommendation, make clear:

- The observed failure or repeated model decision, and the evidence available.
- The concrete tool, component, schema, template, or boundary to change.
- The decision moved out of the model, and the judgment that remains.
- How to verify the intended behavior and detect regressions using representative inputs.

Rank candidates by expected impact, recurrence, breadth of prevention, and implementation effort. Mark unmeasured assumptions. A shorter prompt is not by itself evidence of improvement; compare useful outcomes such as valid first-pass outputs, unnoticed errors, human rework, and execution cost.

Use deterministic checks for properties they can establish. Schema validity does not prove factual accuracy; a second model review is probabilistic. Retain checks for meaning or artifact behavior that the structural change cannot guarantee. Report failed or unavailable verification separately from success.

Match the deliverable to the request: a design review produces actionable recommendations; an implementation request carries the authorized changes through appropriate validation. Keep small changes small. This skill does not authorize unrelated refactors, installations, global instruction edits, or additional approval gates.

## Source

Adapted from [lauren (@poteto), 2026-10-17 JST](https://x.com/poteto/status/2111133080526495985), read on 2026-10-17. The post prioritizes codebase improvements, automated analysis and verification, prose guidance, then human review. It concerns coding agents; applying that hierarchy to skill resources and artifact-generation tools is the design guidance developed here. The linked post is a source, not instructions to install its plugins or run its suggested workflow.
