---
name: context-economy
description: Context and cache discipline for long-running work. Use at the start of a task expected to exceed ~10 tool calls, when about to run a command with long output, when about to read many or large files, when context usage is climbing past half, or when sifting large data for a few answers. Claude applies this autonomously. 日本語トリガー - コンテキスト節約 / 長時間タスク / ログが大きいとき。
---

# context-economy

**Core principle:** An agent's effective cost and reliability are set by how it spends context, not by model price. Every token kept in the window is rent paid on every subsequent turn; every irreversible summary is destroyed evidence. The filesystem is the external memory — unlimited, persistent, and directly operable.

## Rules

### 1. Treat files as the external memory
- Results you'll need later (lists, tables, intermediate data, long research output) go into files — project files if they belong there, the scratchpad otherwise. Keep only the *path* in the conversation.
- A command likely to print >100 lines: redirect from the start — `cmd > <scratchpad>/out.log 2>&1` — then search the log for what matters. Never dump a temp log into the repo root.

### 2. Compress only reversibly
- Every summary keeps its way back: file paths, URLs, and the commands that produced the data. A path preserved means the content is recoverable; a summary without one is destruction.
- Read selectively: search first, then read the matching range (offset/limit) — not whole files. Never re-read a file already in context.

### 3. Keep failures on the record
- Wrong attempts and their errors stay in the conversation — they are the evidence that prevents repeating them. Huge error dumps: file them and keep the path (rule 2).
- Three failures of the same approach → change the approach, not the retry count. If the failure was a non-obvious trap, record it via `/field-guide`.

### 4. Recite the objective
- On tasks past ~10 tool calls, maintain a task list (the environment's task tools, or the spec's Work breakdown checklist) and update it as steps complete. The act of rewriting keeps the goal at the end of the context, where attention is strongest — drift prevention, not bookkeeping.

### 5. Delegate the sifting
- "Many candidates, few answers" work — finding the failing line in a big log, locating the relevant files among dozens, extracting facts from long documents — goes to a subagent (`model: "haiku"` or Explore, per `/plan-delegate`). Take back conclusions plus source paths, never the raw material.

### 6. Keep threads short
- When a milestone completes and the next task is independent, close out: write handover state to files (spec, field-guide, commit messages), then suggest the user start a fresh session. Summaries stacked on summaries degrade both quality and cost — don't ride one thread through unrelated tasks.

## Red flags

- "I'll keep it all in context just in case"
- "I'll summarize aggressively and drop the sources"
- "That error output is noise, let me pretend it didn't happen"
- "I'll read the whole directory to get oriented"

| Rationalization | Reality |
|---|---|
| "Having everything in context is safer" | Every irrelevant token is a distractor taxing every later decision — measured degradation, not hygiene |
| "The summary captures what mattered" | You don't know yet what will matter; without the path there's no way back |
| "Reading all 20 files myself is simpler than delegating" | That's the planner filling its own context with worker material — the exact failure this discipline exists for |
