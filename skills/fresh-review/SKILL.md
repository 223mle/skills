---
name: fresh-review
description: Verification gate before declaring work done. Use after completing any non-trivial implementation (multi-file change, new feature, or any logic change), before reporting completion, opening a PR, or accepting a worker's result — even when nobody asked for a review. Claude applies this autonomously. 日本語トリガー - レビューして / 検証して / セルフレビュー / 完了報告・PR作成の前。
---

# fresh-review

**Core principle:** An agent that implemented something cannot objectively evaluate it — its prior reasoning biases it toward confirming what it already did. Verification therefore runs in fresh contexts that never saw the implementation happen. Reviewers report; they never fix.

Copy this checklist and work through it:

```
- [ ] 1. Scale gate: does this change need lens review at all?
- [ ] 2. Deterministic checks pass (lint / types / tests)
- [ ] 3. Lens reviewers launched in parallel (fresh context, no transcript)
- [ ] 4. Findings triaged; fixes applied; deterministic checks re-run
- [ ] 5. Completion report includes findings and dispositions
```

## 1. Scale gate

- **Trivial** (single file, no logic change — typo, comment, config value): deterministic checks + re-read your own diff. Stop here; lenses would be overkill.
- **Standard** (feature work, multi-file): 1 lens (diff).
- **High-stakes** (design change, security-sensitive area, pre-release, integrating delegated work): 2–3 lenses in parallel. Diff is always included; add **codebase** when the change lands in an unfamiliar or convention-heavy area, add **spec** when a spec or explicit requirements exist. Design changes and pre-release get all three.

## 2. Deterministic checks first

Machines are cheaper than LLM reviewers; never show an LLM what a linter would catch.

Discover the project's checks in this order — use the first that exists:
1. A project verification skill (e.g. `/verify`) or commands named in CLAUDE.md
2. `package.json` scripts (`lint`, `typecheck`, `test`), `Makefile`, `justfile`
3. CI config (`.github/workflows/`) — run what CI runs

Failures found here get fixed **before** launching reviewers. Report failures honestly; never reclassify a failing check as "minor, still done."

## 3. Launch lens reviewers

Each lens is a fresh-context subagent. Decorrelated viewpoints stack — two reviewers with the same inputs find the same bugs; two with different inputs don't.

| Lens | Reviewer receives | Catches | Model |
|---|---|---|---|
| **diff** | The diff only | Logic errors, edge cases, off-by-ones | sonnet |
| **codebase** | Diff + repo read access | Convention violations, duplicated abstractions, missed call sites | sonnet |
| **spec** | Diff + spec (`/spec-first`) or original request | Intent mismatch, unmet requirements, unrequested work | inherit main model |

Reviewer prompt template:

```
Review this change. You did not write it and have no stake in it.
Inputs: <diff / file paths / spec path — per lens table>
Report findings only — do not edit any file.
For each finding: severity (high = incorrect behavior / medium = deviates from
spec or conventions / low = quality), the location, and a concrete failure
scenario (inputs → wrong outcome). 
If you find nothing, say "no findings" — do not invent issues to seem useful.
```

Hard rules:
- **Never pass the implementation transcript, your reasoning, or your excuses.** A reviewer that knows the story inherits the bias.
- **Reviewers report, they don't fix.** A reviewer that edits destroys both accountability and its own independence.

## 4. Triage and fix

- Triage findings yourself; you may reject false positives with a stated reason.
- After fixing: re-run deterministic checks. If any high-severity finding existed, run one more diff-lens pass over the fix.

## 5. Report

Include in the completion report: findings raised, and per finding — fixed, or rejected with reason. Never present a reviewed change as "clean" by omitting findings.

## Red flags — you are about to skip verification

- "It's a small change, the tests passing is enough"
- "I was careful while writing it, it's probably fine"
- "Spinning up a reviewer for this feels heavyweight"
- "I'm low on time, I'll report done and review later"

| Rationalization | Reality |
|---|---|
| "I re-read my own diff, that counts as review" | Self-review confirms; measured fresh reviewers find ~2 real bugs per PR that authors missed |
| "The worker said it's done and tests pass" | A worker's "done" is a claim; integrating unreviewed delegated work merges its blind spots |
| "A no-findings review would waste tokens" | "No findings" from a fresh context is information — it's the cheapest insurance you can buy |
| "I'll batch the review after a few more changes" | Findings compound; the fix cost grows with everything built on top |
