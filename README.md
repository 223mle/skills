# skills

日本語で文章を書く・レビューするための Agent Skills 集です。[Anthropic の skills リポジトリ](https://github.com/anthropics/skills)と同じ形式で、各ディレクトリが1つのスキル（`SKILL.md` + 参照ファイル）です。Claude Code のほか、Agent Skills 形式を読み込めるコーディングエージェント（Codex CLI、Cursor など）で使えます。

## 収録スキル

### [clear-japanese](clear-japanese/)

レビュワー（読み手）が一読で意味を取れる日本語を書く・レビューするスキルです。LLM の書く日本語が分かりにくくなる原因を「語彙・文・構造・AIっぽさ」の4層に分け、層ごとのルールと3つの判定テスト（復元テスト・新情報テスト・疑問応答テスト)で診断します。

- **執筆モード**: 書く前に読後アウトプット・解消したい課題・想定読者を決め、結論先行の構造で書く
- **レビューモード**: 構造 → 語彙 → 文 → AIっぽさの4パスで全文を診断する。指摘は GitHub Diff 風の HTML レポートで表示され、ユーザーは指摘ごとに採用/却下を選び、修正案をブラウザ上で直接編集できる。「結果をコピー」でチャットに貼り戻すと、エージェントが採用分だけを文書に適用する

長い文章では、観点別のサブエージェント4体に並列でレビューさせ、指摘を検証・統合する手順も含みます。

## インストール

Claude Code では、スキルを `~/.claude/skills/` に置くと読み込まれます。

```bash
git clone https://github.com/223mle/skills.git
ln -s "$(pwd)/skills/clear-japanese" ~/.claude/skills/clear-japanese
```

シンボリックリンクにしておくと、`git pull` だけで更新が反映されます。リンクの代わりにディレクトリごとコピーしても動きます。

## ライセンス

[MIT](LICENSE)
