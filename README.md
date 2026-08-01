# Skills

エージェントスキル集です。

## Install

```bash
npx skills@latest add 223mle/skills
```

手動でインストールする場合は、リポジトリを clone して `~/.claude/skills/` に symlink を張る:

```bash
git clone https://github.com/223mle/skills.git ~/skills
for s in ~/skills/skills/*/; do ln -sfn "$s" ~/.claude/skills/"$(basename "$s")"; done
```

## Skills

### 文章

- **clear-japanese** — 読み手が一読で意味を取れる日本語を書く・レビューする。語彙・文・構造・AIっぽさの4層で診断し、指摘は GitHub Diff 風の HTML レポートで表示。採用/却下と修正案の編集をブラウザ上で行い、結果をチャットに貼り戻して適用する。

### ハーネス(agent swarm 規律)

トップティア AI 企業(Cursor / Anthropic / OpenAI / Google / Moonshot ほか)の agent swarm 一次情報調査から抽出した「課題→工夫」を、Claude Code の運用規律に落としたスキル群。5 本で独立して使えるが、組み合わせると planner/worker 型のハーネスとして機能する。**ユーザーの明示的な指示は前提にしない** — ユーザーは目標を述べるだけで、委譲・検証・申し送りの判断はエージェントが自律的に行う(発動条件は各スキルの description に記載)。

- **plan-delegate** — planner/worker 委譲の規律。read は並列・write は single writer、委譲プロンプトは decision-complete な mini-spec、モデルは役割別(探索=haiku / 実装 worker=sonnet / 計画=メインモデル)、並列度は既定 3。
- **fresh-review** — 検証の分離。決定的チェック(lint/型/テスト)を先に通し、実装の経緯を知らないクリーンコンテキストのレビュアーを視点別(diff / codebase / spec)に並列起動する。レビュアーは指摘するが直さない。
- **spec-first** — 仕様を第一級の成果物にする。decision-complete な spec を実装前に書き、人間の承認を spec 段階に集中させる。実装中は spec を凍結し、逸脱は Deviations に追記して最後に和解する。テンプレートは `references/spec-template.md`。
- **field-guide** — エージェントが管理する申し送りファイル(`.claude/field-guide.md`、50 行 / 1 行 150 字、日付=最終検証日)。想定外の遭遇と失敗した方向だけを記録し、次のセッション・サブエージェントの回り道を減らす。
- **context-economy** — コンテキストの規律。ファイルシステムを外部記憶にする、復元可能な形でだけ圧縮する、失敗を消さない、篩い作業はサブエージェントに任せる、スレッドを短く保つ。

スキル本文は英語(トークン効率と小型モデルでの追従性のため)、description には日本語トリガー語を併記している。

推奨の組み合わせ方: 実装タスクの標準フローは `spec-first` → (必要なら `plan-delegate` で委譲) → `fresh-review` で検証。`field-guide` と `context-economy` は全フローの下敷きとして常時意識する。
