---
name: fresh-review
description: Verification gate before declaring work done. Use after completing any non-trivial implementation (multi-file change, new feature, or any logic change), before reporting completion, opening a PR, or accepting a worker's result — even when nobody asked for a review. Claude applies this autonomously. 日本語トリガー - レビューして / 検証して / セルフレビュー / 深くレビュー・徹底レビュー（Workflow 段） / 完了報告・PR作成の前。
---

# fresh-review

**Core principle:** An agent that implemented something cannot objectively evaluate it — its prior reasoning biases it toward confirming what it already did. Verification therefore runs in fresh contexts that never saw the implementation happen. Reviewers report; they never fix.

Copy this checklist and work through it:

```
- [ ] 1. Scale gate: does this change need lens review at all?
- [ ] 2. Deterministic checks pass (lint / types / tests)
- [ ] 3. Lens reviewers launched in parallel (fresh context; transcript only to the transcript lens) — or the Workflow tier for the deepest reviews
- [ ] 4. Findings triaged; fixes applied; deterministic checks re-run
- [ ] 5. Completion report includes findings and dispositions
```

## 1. Scale gate

- **Trivial** (single file, no logic change — typo, comment, config value): deterministic checks + re-read your own diff. Stop here; lenses would be overkill.
- **Standard** (feature work, multi-file): 1 lens (diff).
- **High-stakes** (design change, security-sensitive area, pre-release, integrating delegated work): 2–4 lenses in parallel. Diff is always included; add **codebase** when the change lands in an unfamiliar or convention-heavy area, add **spec** when a spec or explicit requirements exist, add **transcript** when integrating delegated work (a worker transcript exists). Design changes and pre-release get all applicable lenses. When the change deserves going deeper still, propose the **Workflow tier** (§3 — its gate defines when to ask).

## 2. Deterministic checks first

Machines are cheaper than LLM reviewers; never show an LLM what a linter would catch.

Discover the project's checks in this order — use the first that exists:
1. A project verification skill (e.g. `/verify`) or commands named in CLAUDE.md
2. `package.json` scripts (`lint`, `typecheck`, `test`), `Makefile`, `justfile`
3. CI config (`.github/workflows/`) — run what CI runs

Failures found here get fixed **before** launching reviewers. Report failures honestly; never reclassify a failing check as "minor, still done."

## 3. Launch lens reviewers

Each lens is a fresh-context subagent. Decorrelated viewpoints stack — two reviewers with the same inputs find the same bugs; two with different inputs don't. No single lens catches everything; lenses with different inputs and models fail differently, and that is what compounds.

| Lens | Reviewer receives | Catches | Model |
|---|---|---|---|
| **diff** | The diff only | Logic errors, edge cases, off-by-ones | sonnet |
| **codebase** | Diff + repo read access | Convention violations, duplicated abstractions, missed call sites | sonnet |
| **spec** | Diff + spec (`/spec-first`) or original request | Intent mismatch, unmet requirements, unrequested work | inherit main model |
| **transcript** | Implementation transcript + diff — **only this lens sees the transcript** | Wrong assumptions carried through, tests weakened or skipped to pass, misread instructions, errors observed but not reported | inherit main model (long-context tolerance) |

Reviewer prompt template:

```
Review this change. You did not write it and have no stake in it.
Inputs: <diff / file paths / spec path / transcript path — per lens table>
Report findings only — do not edit any file.
For each finding: severity (high = incorrect behavior / medium = deviates from
spec or conventions / low = quality), the location, and a concrete failure
scenario (inputs → wrong outcome). 
If you find nothing, say "no findings" — do not invent issues to seem useful.
```

For the transcript lens, additionally instruct: "Look for wrong assumptions the author carried, tests weakened or disabled to make them pass, instructions misread, and errors that were observed but never reported."

Hard rules:
- **The implementation transcript goes to the transcript lens only.** Passing it — or your reasoning, or your excuses — to the diff/codebase/spec lenses makes them inherit the author's bias; their independence is what lets a transcript lens exist at all. The transcript lens catches process errors, not product errors; its verdict never substitutes for the artifact lenses.
- **Reviewers report, they don't fix.** A reviewer that edits destroys both accountability and its own independence.

### Workflow tier (deep review)

For changes that deserve the deepest pass — design changes, pre-release, security-sensitive areas — run the lenses plus adversarial verification as a single Workflow. Verification kills plausible-but-wrong findings the same way lens diversity kills blind spots: refuters with distinct viewpoints fail differently.

**Gate:** ask the user first, one line — 「Workflow 段まで回しますか？（レンズ + 反証で最大〜22エージェント消費）」. Skip the question only when the user explicitly asked for a deep review (「深くレビュー」「徹底レビュー」) — the explicit request is itself the consent. Never auto-launch.

**Shape (one pass, no iteration):**
1. **Find** — the applicable lenses (per the lens table, each receiving only its own inputs) run in parallel with structured output.
2. **Dedup** — findings merged across lenses by file + line (plain code; the barrier is justified — the same bug found by two lenses must not be verified twice).
3. **Verify** — the top ≤6 high/medium findings are each attacked by 3 refuters with distinct viewpoints (correctness / reproduction / spec-intent), mixed models. **Refuters receive the finding plus the inputs its origin lens saw** (diff and spec always; the transcript additionally for transcript-lens findings — a refuter that cannot see what the finding is about would kill everything, including every genuine process error). The transcript-only hard rule governs the artifact *reviewers*; verifying a transcript finding necessarily reads the transcript. A finding survives on 2/3 of the votes actually returned; fewer than 2 returned votes means verification didn't run, so the finding passes through flagged `unverified` rather than dying to an infrastructure failure. Low-severity and over-cap findings skip verification and carry the same flag.
4. Survivors enter normal triage (§4). Report the killed count too; it is evidence the verification did work.

Script template — build each lens prompt from the lens table before invoking, and pass the review inputs for the refuters via `args.inputs`:

```javascript
export const meta = {
  name: 'fresh-review-deep',
  description: 'Lens reviewers + adversarial verification of each finding',
  phases: [{ title: 'Find' }, { title: 'Verify' }],
}
const FINDINGS = { type: 'object', required: ['findings'], properties: { findings: {
  type: 'array', items: { type: 'object',
    required: ['file', 'severity', 'claim', 'scenario'],
    properties: { file: { type: 'string' }, line: { type: 'number' },
      severity: { enum: ['high', 'medium', 'low'] },
      claim: { type: 'string' }, scenario: { type: 'string' } } } } } }
const VERDICT = { type: 'object', required: ['refuted', 'reason'],
  properties: { refuted: { type: 'boolean' }, reason: { type: 'string' } } }
// args: { lenses: [{ key, prompt, model? }], inputs: { diff, spec?, transcript? } }
//   lenses[].prompt はレンズ表に従い事前構築。inputs は反証者が読むパス。
const REFUTERS = [
  { lens: 'correctness', model: 'sonnet' },
  { lens: 'reproduction', model: 'sonnet' },
  { lens: 'spec-intent' },  // main model — 割り当ては変更可
]
const VERIFY_CAP = 6
const found = (await parallel(args.lenses.map(l => () =>
  agent(l.prompt, { label: `find:${l.key}`, phase: 'Find', schema: FINDINGS, model: l.model })
    .then(r => (r?.findings ?? []).map(f => ({ ...f, foundBy: l.key })))))).filter(Boolean).flat()
const seen = new Set()
const unique = found.filter(f => {
  const k = `${f.file}:${f.line ?? '?'}`
  return seen.has(k) ? false : seen.add(k)
})
const low = unique.filter(f => f.severity === 'low').map(f => ({ ...f, survives: true, unverified: true }))
const rank = { high: 0, medium: 1 }
const nonLow = unique.filter(f => f.severity !== 'low').sort((a, b) => rank[a.severity] - rank[b.severity])
const toVerify = nonLow.slice(0, VERIFY_CAP)
const overCap = nonLow.slice(VERIFY_CAP).map(f => ({ ...f, survives: true, unverified: true }))
if (overCap.length) log(`VERIFY_CAP 超過: ${overCap.length} 件は未検証フラグ付きで triage へ`)
// 反証者への入力は finding の出所レンズに合わせる（transcript finding だけが transcript を見る）
const refInputs = f => f.foundBy === 'transcript'
  ? args.inputs
  : { diff: args.inputs.diff, ...(args.inputs.spec ? { spec: args.inputs.spec } : {}) }
const verified = await parallel(toVerify.map((f, i) => () =>
  parallel(REFUTERS.map(v => () =>
    agent(`Adversarially try to REFUTE this review finding via the ${v.lens} lens.\n` +
          `Finding: ${f.claim} (${f.file}${f.line ? ':' + f.line : ''})\nScenario: ${f.scenario}\n` +
          `Inputs you may read: ${JSON.stringify(refInputs(f))}\n` +
          `Default to refuted=true if you cannot confirm the finding from those inputs.`,
      { label: `verify:${i}:${v.lens}`, phase: 'Verify', schema: VERDICT, model: v.model })))
    .then(vs => {
      const votes = vs.filter(Boolean)
      return votes.length < 2
        ? { ...f, survives: true, unverified: true }
        : { ...f, survives: votes.filter(x => !x.refuted).length >= Math.ceil(votes.length * 2 / 3) }
    })))
const all = [...verified.filter(Boolean), ...low, ...overCap]
return { survived: all.filter(f => f.survives), killed: all.filter(f => !f.survives).length }
```

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
