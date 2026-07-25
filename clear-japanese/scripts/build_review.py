#!/usr/bin/env python3
"""レビュー指摘の JSON からレビュー結果 HTML を生成する。

使い方:
    python3 build_review.py <review-data.json> <output.html>

JSON のスキーマは references/html-report.md を参照。
"""
import json
import pathlib
import sys

TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "assets" / "review-template.html"
SEVERITIES = {"高", "中", "低"}
LAYERS = {"語彙", "文", "構造", "AIっぽさ"}
REQUIRED = ["id", "severity", "layer", "title", "before", "after", "reason"]


def fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) != 3:
        fail("使い方: build_review.py <review-data.json> <output.html>")
    data_path, out_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])

    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        fail(f"{data_path} を読めません: {e}")

    if "doc" not in data:
        fail('トップレベルに "doc"（対象文書のパス）が必要です')
    findings = data.get("findings")
    if not isinstance(findings, list):
        fail('"findings" は配列である必要があります')
    for i, f in enumerate(findings):
        for key in REQUIRED:
            if key not in f:
                fail(f'findings[{i}] に "{key}" がありません')
        if f["severity"] not in SEVERITIES:
            fail(f'findings[{i}].severity は 高/中/低 のいずれか（実際: {f["severity"]}）')
        if f["layer"] not in LAYERS:
            fail(f'findings[{i}].layer は 語彙/文/構造/AIっぽさ のいずれか（実際: {f["layer"]}）')

    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("__REVIEW_DATA__", payload, 1)
    out_path.write_text(html, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
