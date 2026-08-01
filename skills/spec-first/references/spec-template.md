# Spec template

Copy the skeleton below. Write section content in the conversation language; keep headings.
Placeholders in `<>` state each section's pass condition — replace them, never ship them.
Delete sections that would be empty (never write "N/A"). For a small change (single file,
no design decisions) keep only: Why / Scope / Requirements / Verification / Work breakdown.

````markdown
---
id: SPEC-<slug>
status: draft            # draft → in-review → approved → implementing → reconciled
created: <YYYY-MM-DD>
targets:                 # editable range for workers; also the blast radius
  - src/<path>/
---

> **Contract.** While status is `implementing`, the body above `## Deviations` is frozen.
> Mismatches discovered during implementation are appended to `## Deviations` only.

# <The intent, stated in one line>

## Why

<One paragraph: the pain / opportunity / mandate behind this, who is affected,
and why now. Every later trade-off resolves against this paragraph.>

## Scope

**In scope**
- <what this spec builds>

**Out of scope** — minimum one item; the fence against scope creep
- <won't do: not this spec's responsibility>
- <later: deferred — name where it goes>
- <won't change: existing behavior that must survive intact (regression fence)>

## Current state

<Verified facts only — guesses belong in Assumptions.
- `path/to/file.ts:120` — <what happens today>
- <existing constraints, dependencies, callers>
Name at most ~3 paths; group by responsibility beyond that.>

## Requirements

- **REQ-1** <Intent in one sentence: "<actor> can <capability>". WHAT, not HOW.>
  - **Pass when**: <observable fact a code-blind tester could judge>
  - **Edges**: <WHEN <trigger> ... / IF <bad input> THEN ... — delete this line if none>
- **REQ-2** ...

## Decisions

- **DEC-1: <the choice, one line>**
  - Why: <the constraint/requirement/cost that forced it>
  - Rejected: <alternative> — <the concrete trade-off that killed it>
  - Visible as: <test name / measurement / greppable pattern that proves it held>

<Only decisions an implementer could plausibly make differently. If it rules
nothing out, it is not a decision — fold it into prose.>

## Verification

**Completion gates** — runnable; the work is not done until all pass
- [ ] `<command>` → <expected result>
- [ ] E2E: <shortest human-followable proof the feature works>

**Must not change** — regression fence
- [ ] <existing test/behavior that stays green>
- [ ] <files/config that stay untouched>

## Assumptions

<Defaults chosen without confirmation. Each: the assumption — why chosen — impact if wrong.>
- <assumption> — <reason> — <blast radius if it flips>

## Open Questions

<Max 3. Questions only a human can answer (preferences/trade-offs, not discoverable
facts). Each phrased as a question, with stakes and options. All must close before approval.>

- **Q1: <the question — ends with "?">**
  Why it matters: <one plain sentence on what this changes for shipping/acceptance>

  | Option | Answer | Implication |
  |---|---|---|
  | A | <option> | <scope/cost/risk impact> |
  | B | <option> | <impact> |
  | → | Recommended: A | <1–2 sentence reason> |

## Work breakdown

<Delegation units (`/plan-delegate`). [P] = parallelizable — only for tasks in
independent modules (no shared files, no imports of each other); parallel
execution additionally requires `isolation: "worktree"` per /plan-delegate.
Each line executable by a worker with no extra context. Granularity: "Add error
handling for invalid files" — good; "Create CLI tool" — too coarse.>

- [ ] T1 [REQ-1] <verb-first concrete step> — `path/to/file.ts`
- [ ] T2 [P] [REQ-1] <...> — `path/to/other.ts`
- [ ] T3 [REQ-2, DEC-1] <...> — `path/to/third.ts`

**Checkpoint**: after T1–T2, REQ-1 is independently verifiable.

## Deviations

<Append-only during implementation. Each: where reality diverged from the spec, and why.
Resolved one by one at reconcile time: fix the code, or update the spec to shipped truth.>

- (none yet)
````

## Review checklist — run before showing the user, ~2 minutes

- [ ] Why matches what was actually asked for
- [ ] Out of scope contains the "nearby things" nobody requested
- [ ] Every REQ's pass condition is judgeable without reading the code
- [ ] The case the user cares most about appears in a gate or the regression fence
- [ ] Every DEC has a rejected alternative a reviewer could disagree with
- [ ] Completion gates are commands, not sentiments
- [ ] Open Questions ≤ 3, each with options and a recommendation
- [ ] Every task cites a REQ or DEC — no work of unknown origin
- [ ] No task touches anything outside `targets`
- [ ] "If exactly this were built, and nothing more, the user would be satisfied"
