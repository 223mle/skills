---
name: plan-delegate
description: Delegation discipline for subagent work. Use whenever about to spawn a subagent, when a task is expected to span 3+ files or 2+ independent questions, when starting a sizable implementation, refactor, or investigation where delegating part of the work is plausible, or when parallel research could shorten the critical path. Claude applies this autonomously without being asked. 日本語トリガー - 並列で / 委譲して / サブエージェントで / 大きめのタスクの開始時。
---

# plan-delegate

**Core principle:** Delegation buys context isolation and parallelism at the price of coordination. The main agent acts as planner — it decomposes, decides, integrates, and reviews. Workers execute one narrow piece with their full context. A planner that grinds through bulk reads or bulk edits itself loses the big picture; a worker that plans duplicates decisions.

## Step 1: Decide whether to delegate at all

Delegate only if at least one condition holds. Otherwise do the work directly — delegation adds coordination cost and tokens.

1. **Context isolation** — the work requires reading a lot of material whose details should not pollute the main context
2. **Parallelism** — 2+ subtasks are independent of each other
3. **Specialization** — a different lens, toolset, or clean context is required (e.g. review)

Tasks touching 1–2 files, or with strong sequential dependencies: do them yourself.

If the task also meets `/spec-first` criteria (2+ design decisions, delegation planned), check for a spec before decomposing — no spec yet means write and get it approved first. Delegating without a spec spreads design decisions across workers.

## Step 2: Respect the read/write asymmetry

- **Reads (exploration, research, verification, summarization): parallelize freely.** They cannot conflict.
- **Writes (file edits): single writer by default.** Two agents writing in parallel embed conflicting implicit decisions (style, edge-case handling) even when files don't overlap.
- Parallel writes are allowed only when BOTH hold: (a) the modules are independent — they do not import each other and share no files; (b) each worker runs with `isolation: "worktree"`. Never let two agents touch the same file.

## Step 3: Write the delegation prompt as a mini-spec

Collapse all ambiguity before handing off — the worker must not need to make any decisions ("decision complete"). Template:

```
Goal: <why this piece exists, 1–2 sentences>
Inputs: <files to read; spec path if one exists (/spec-first); relevant field-guide lines (/field-guide)>
Success criteria: <observable result; runnable check command if one exists>
Boundaries: <files/dirs the worker may touch; "report, don't fix" for anything outside>
Return: <changed-file list + summary / structured findings — not raw logs>
```

**Never delegate a design decision.** If two subtrees could answer the same question (naming, error policy, data shape), decide it in the planner and pass the answer to both. Split-brain implementations are the top failure mode of parallel work.

## Step 4: Assign models by role

| Role | Model | Examples |
|---|---|---|
| Exploration, grep-like search, file listing, mechanical transforms | `model: "haiku"` | "List every call site of this API" |
| Implementation worker, test writing, structured summarization | `model: "sonnet"` | "Implement X exactly per this spec" |
| Planning, design decisions, hard parts, final integration | (no override — inherit main model) | The decomposition itself; conflict arbitration |
| Review | Per `/fresh-review` lens table | |

Never downgrade the planner: a cheap planner writes looser instructions, and the worker fleet burns multiples of the savings downstream.

## Step 5: Manage concurrency, failure, and integration

- Default concurrency **3**, max **5**. Before adding more, ask: does this split shorten the critical path (the slowest single chain)? Wider fan-out that doesn't shorten the longest chain only adds cost.
- Worker failed or returned null → re-delegate once with a more explicit prompt, then do it yourself.
- A worker reports something that invalidates a sibling's assumptions → stop, revise the plan in the planner, re-delegate. Discoveries propagate through the planner, never agent-to-agent.
- Accept results as files + short structured reports. Do not pull worker transcripts into the main context.
- Worktree workers leave their changes on separate branches — nothing merges automatically. The planner integrates: merge each returned branch sequentially, arbitrating any conflict itself (never ask a worker to resolve a conflict with a sibling).
- After any delegated implementation, run `/fresh-review` before reporting done. A worker's "completed" is a claim, not a verification.

## Red flags — stop and re-plan

- "The workers can figure out the design details themselves"
- "Both agents editing the same area will probably not conflict"
- "A cheaper model for planning will save money"
- "More parallel agents means faster"
- "I'll just read all twenty files myself real quick"

| Rationalization | Reality |
|---|---|
| "Splitting the design question between workers is fine" | Each worker answers it differently; you merge two conflicting worldviews |
| "Parallel writes rarely collide" | Colliding writes fail silently — last writer wins with no error |
| "Planner tokens are where the cost is, cut there" | Measured result: cheap planners inflate worker tokens several-fold |
| "10 workers will be faster than 3" | Wall-clock = slowest chain; extra fan-out adds cost, not speed |
