# Designing a slide skill

Design a small semantic interface over the rendering engine available in the target project. The names below are proposed interfaces, not tools supplied by this skill. Start with the layouts the intended users actually need.

## Caller first

The caller supplies a deck request to a proposed `render_deck(request, output_target)` tool. The output target is bound by the execution environment; it is not a coordinate or an arbitrary path inferred from slide content.

```json
{
  "slides": [
    {
      "layout": "title-bullets",
      "title": "今期の改善方針",
      "bullets": [
        "繰り返す配置を部品化する",
        "生成物を描画して確認する",
        "内容の判断にレビューを集中する"
      ]
    }
  ]
}
```

Validate this input with [assets/slide-deck.schema.json](../assets/slide-deck.schema.json). It is a complete starter schema for three layouts, not a universal presentation format. Its length/count limits are illustrative defaults; tune them with the actual page size, fonts, languages, and renderer. A schema-valid slide can still overflow.

## Components and ownership

| Layout ID | Model supplies | Template/renderer owns |
|---|---|---|
| `title-bullets` | Title and 3–5 bullets | Text boxes, spacing, bullet style, title/body sizes. |
| `comparison` | Title, left/right headings, 1–3 bullets per side | Column geometry, alignment, heading styles, balanced spacing. |
| `text-chart` | Title, 1–3 bullets, dataset ID and category/value column IDs | Asymmetric text/chart geometry, bar-chart style, axes, labels, number formats. |

For the comparison layout, supply `left` and `right` objects, each with `heading` and `bullets`. For the chart layout, supply `chart: {"datasetId": "sales", "categoryColumnId": "month", "valueColumnId": "revenue"}` alongside `title` and `bullets`. These identifiers must resolve to inspected data; reject unknown IDs and incompatible column types before rendering.

The model chooses message, evidence, emphasis, component, and content. Keep brand colors, fonts, default text sizes, margins, and chart styles in the template/theme. The starter schema rejects arbitrary `x`, `y`, `fontSize`, and `color` fields. Add theme or design options only when implemented and useful to the user. Derive supported layouts and schema variants from one registry where feasible, or check their consistency so accepted IDs cannot lack an implementation.

Preserve traceable data bindings: chart values and labels should come from the bound dataset, while claims requiring interpretation remain subject to semantic review. Do not silently summarize or discard supplied content to fit a component. For explicitly requested freeform work, define a supported alternative or new component; do not force all requests into these three layouts.

## Resources to build in the new skill

Use only resources the target implementation needs. Example destinations:

| Resource | Concrete responsibility |
|---|---|
| `SKILL.md` | Select a supported layout, gather missing content/data, invoke the rendering tool, interpret its result. |
| `assets/slide-deck.schema.json` | Validate the semantic request before rendering. |
| `assets/theme.json` or a native template | Store theme values and font choices supported by the engine. |
| `scripts/render_deck.py` or an existing tool | Resolve layouts/data, generate the deck, render previews, and return artifact handles and errors. |
| `scripts/check_deck.py` or an existing validator | Check actual output properties and report slide/element IDs with evidence. |

Choose the real engine and invocation before writing instructions around it. A `.pptx` template, code-based renderer, or connected presentation tool may need different resources; do not create this whole list by default. For existing-deck editing, add stable slide/element identity and preservation checks instead of rebuilding the entire deck from the sample schema.

## Execution and failures

1. Confirm the renderer, required fonts, template, data bindings, and output destination are usable.
2. Validate the request shape, then resolve layout/data IDs against the real registry.
3. Render using the selected template. Inspect the rendered output; input character limits are only an early filter.
4. If content does not fit, return a localized error such as `TEXT_OVERFLOW` with slide and element IDs. Use an implemented alternate layout or split operation, or ask the model to revise content within the user's intent. Enforce the product's minimum text size and a bounded repair budget. Never hide the error by truncating text or shrinking it indefinitely.
5. Return the actual artifact, previews, checks performed, and any unverified properties. `UNKNOWN_DATASET`, `UNSUPPORTED_LAYOUT`, and `RENDER_UNAVAILABLE` are examples of distinct failure classes, not proof these handlers already exist.

When an existing file is edited, compare changed and unchanged slides, including relevant notes, links, charts, and editable objects. Rendered images alone do not prove those features survived export.

## Representative checks

| Input or change | Expected result |
|---|---|
| The request above | Schema passes; implementation produces one readable slide containing the exact supplied title and three bullets. |
| Two bullets, an unknown layout, or a raw `fontSize` field | Schema rejects the request before rendering; return the relevant input location. |
| Valid-length Japanese text that overflows with the actual font | Output check detects overflow; supported repair preserves content or reports an unresolved failure. |
| Chart bound to categories `A, B` and values `100, 200` | Chart data and displayed labels match the binding; no invented points or units. |
| Edit only slide 2 of an existing deck | Requested change is present; unrelated content and required features are preserved. |

Record a past failed slide as a regression fixture where available. Confirm the detector catches the old failure and accepts the corrected result. For aesthetics, narrative, and whether a source supports a claim, retain an explicit semantic review; do not present schema or geometry checks as proof of those qualities.
