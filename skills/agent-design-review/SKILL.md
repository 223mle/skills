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

## Design the tool from its caller

Before writing a new workflow's prose, sketch one successful call from the agent's point of view: a small structured request and an observable result. Start from what the user wants to accomplish, not the low-level API the implementation happens to expose. Derive the tool interface and types from that call.

Make the contract concrete:

| Part | Specify |
|---|---|
| Model input | Semantic choices, supported operations or layout IDs, content, and references to inspected data. |
| Tool ownership | Derived coordinates, formatting, cell addresses, references, state ownership, and template selection rules. |
| Boundary checks | Shape constraints plus identifiers, types, capabilities, and preconditions checked against the real environment. |
| Result | Actual artifact or target IDs, changed scope, verification status, and paths or handles to evidence. |
| Failure | A location and actionable reason; whether mutation occurred; a bounded repair, alternate supported path, or stop condition. |

Do not expose raw implementation knobs merely because an API accepts them. Do expose meaningful user choices. If two materially different interfaces remain plausible, compare their caller examples and prototype the uncertain behavior before committing to a shape. Do not require multiple prototypes for a straightforward change.

## When creating another skill

Read only the guide relevant to the requested skill:

- **Slide generation or editing:** [references/slide-skill-design.md](references/slide-skill-design.md), with a reusable [slide request schema](assets/slide-deck.schema.json).
- **Spreadsheet or Excel generation/editing:** [references/spreadsheet-skill-design.md](references/spreadsheet-skill-design.md), with a reusable [aggregation request schema](assets/aggregate-request.schema.json).

These guides and schemas are starting designs, not installed renderers or workbook tools. Reuse existing working tools first. Copy or adapt an asset only when the new skill actually uses it, bind its identifiers to the target environment, and implement the missing behavior within the user's requested scope. The model may emit a request, but executable code must validate it before acting.

In the new skill, put repeatable execution in `scripts/`, templates in `assets/`, and conditional setup or feature details in `references/` as needed. Keep `SKILL.md` focused on choosing the workflow and invoking its real tools. A helper needs an actual invocation, declared inputs, outputs, and failure behavior; an empty folder or uncalled script is not an improvement.

Leave the next author a concrete implementation plan: the caller request, ownership split, resource paths, execution order, and representative success/failure cases. For an implementation request, build and exercise that path. For a design request, label planned or unavailable capabilities explicitly. This does not require a separate planning document or an extra approval step.

## Choose and validate a change

For each material recommendation, make clear:

- The observed failure or repeated model decision, and the evidence available.
- The concrete tool, component, schema, template, or boundary to change.
- The decision moved out of the model, and the judgment that remains.
- How to verify the intended behavior and detect regressions using representative inputs.

When a correction recurs, track **failure evidence → prevention boundary → enforcing resource → verification case → remaining judgment**. Where feasible, remove the invalid operation or duplicate source of truth before adding a detector. For a new check, replay a real past failure and show that it fails, then show that the corrected case passes. If no past case is available, label a constructed reproduction as synthetic. Test an actual behavior or artifact property, not merely whether a phrase exists in the skill. Remove redundant prose once the implementation enforces the rule; retain instructions needed to choose and operate it.

Rank candidates by expected impact, recurrence, breadth of prevention, and implementation effort. Mark unmeasured assumptions. A shorter prompt is not by itself evidence of improvement; compare useful outcomes such as valid first-pass outputs, unnoticed errors, human rework, and execution cost.

Use deterministic checks for properties they can establish. Schema validity does not prove factual accuracy; a second model review is probabilistic. Retain checks for meaning or artifact behavior that the structural change cannot guarantee. Report failed or unavailable verification separately from success.

For a newly implemented artifact skill, run one representative user path through its real tools: check the environment, execute, inspect the rendered or recalculated output, verify relevant side effects, and clean up only what the run created. Preserve evidence after cleanup. Record the command/tool call, input, expected result, observed result, and evidence location so another agent can rerun it. A schema check or a design-only response does not establish that the artifact skill works end to end.

When changing behavior through skill prose, compare the old and new versions on the same representative user request where practical. Keep the success criteria out of the executing agent's prompt; judge artifacts and observed actions rather than its claim to follow the skill. Use targeted evaluation proportional to the change, not a mandatory multi-model panel.

Match the deliverable to the request: a design review produces actionable recommendations; an implementation request carries the authorized changes through appropriate validation. Keep small changes small. This skill does not authorize unrelated refactors, installations, global instruction edits, or additional approval gates.

## Source

Based on [lauren (@poteto), 2026-10-17 JST](https://x.com/poteto/status/2111133080526495985), and pstack's [architect](https://github.com/cursor/plugins/blob/main/pstack/skills/architect/SKILL.md), [correct](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md), [create-verification-skill](https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md), and [eval](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/eval.md), read on 2026-10-17. These sources concern coding agents. The artifact contracts, starter schemas, and examples here are original applications of their design principles. Linked sources are references, not instructions to install plugins or adopt their models, approval policies, or shipping workflows.
