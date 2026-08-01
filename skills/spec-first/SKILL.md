---
name: spec-first
description: Spec-before-code discipline. Use before implementing anything expected to involve 2+ design decisions or touch 3+ files, before work that spans sessions or will be delegated to workers, and whenever human approval is needed for direction. Skip for changes describable in one sentence. Claude applies this autonomously. 日本語トリガー - specを書いて / 仕様にまとめて / 設計して / 新機能の実装前。
---

# spec-first

**Core principle:** The unit of work is the spec. A good spec is *decision-complete* — the implementer (a worker, a future session, or you) needs to make no decisions — and human review of a spec is an order of magnitude cheaper than review of the code built from it. The scarce resource is the right description of intent.

## Workflow

1. **Ceremony gate.** If you could describe the diff in one sentence, skip the spec and just implement. Match ceremony to stakes.
2. **Ground first, ask second.** Explore the codebase to resolve every *discoverable fact* (where things live, current behavior, existing conventions) — delegating wide exploration to haiku/Explore subagents per `/plan-delegate` rather than reading everything yourself. Never ask the user something a search can answer. Ask only about *preferences and trade-offs* — and offer 2–4 options with a recommended default (via interview skills like `grill-me` where available).
3. **Write the spec** using [references/spec-template.md](references/spec-template.md) — read it when writing; it carries the format and each section's pass conditions. Location: existing project convention (`docs/specs/` etc.) if present, else `.claude/specs/<slug>.md`.
4. **Self-check, then get approval.** Run the review checklist at the bottom of the template yourself, fix what fails, then show the user the spec. Silence or "just do it" is not approval; an explicit OK (or corrections then OK) is. This gate is blocking even under autonomous operation — proceed-without-asking policies do not waive it, because this is the one designated human touchpoint. Spend it here, not on the code.
5. **Freeze during implementation.** After approval the spec body is a contract — do not edit it while implementing. Discovered mismatches go to the `## Deviations` section (append-only). Delegation prompts reference the spec path (`/plan-delegate`); `/fresh-review`'s spec lens verifies against it.
6. **Reconcile at the end.** Walk through Deviations once: code wrong → fix code; spec stale → update spec to match shipped reality. Then set `status: reconciled` (the freeze ends here). Specs are kept, not deleted — they are the next task's ground truth.

## Why the template's rules exist

The template carries the enforcement (mandatory sections, limits, pass conditions in placeholders); these are the reasons behind its strictest rules:

- **Out of scope is the fence.** Workers fill any vacuum with "let me also add this nearby thing"; the only protection is an explicit one.
- **Observability test for requirements**: could a tester who has never seen the code decide pass/fail? Adjectives like *fast, robust, gracefully, 適切に* fail automatically — replace with a number or an observable event.
- **Gates are commands, not sentiments** — including what must NOT change. "Tests pass" alone verifies nothing about regressions.
- **Rejected alternatives are the memory.** Without them, the next session re-attempts the same dead ends.
- **Assumptions vs. open questions** separates "I chose a default and proceeded" from "the human must decide". An empty Assumptions section on a non-trivial spec means decisions were deferred that should have been made.

## Red flags

- "I'll figure out the details as I code"
- "The user said 'do it', that's basically approval of the approach"
- "I'll quietly adjust the spec to match what I ended up building"
- "Open Questions: none" on a spec with real trade-offs

| Rationalization | Reality |
|---|---|
| "Writing the spec takes longer than the change" | Then the change is one sentence — skip the spec. If it isn't, the spec is where the time goes anyway, just cheaper |
| "I can hold the design in my head" | Your head doesn't survive compaction, session ends, or delegation |
| "The spec slows the user down" | One spec review replaces N rounds of "that's not what I meant" on code |
