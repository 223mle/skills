# Artifact agent examples

Use these examples to identify a useful model/tool boundary. Adapt the components and constraints to the product rather than imposing a universal template.

## Slides

**Repeated mechanics:** the model writes coordinates, font sizes, colors, and spacing for every slide, then repairs similar layout failures repeatedly.

**Structural improvement:** provide layout components such as title plus three-to-five bullets, a comparison, or an asymmetric text-and-chart layout. The model selects a component and supplies its semantic content; the renderer owns geometry and typography.

An illustrative input:

```json
{
  "layout": "title-bullets",
  "title": "Quarterly priorities",
  "bullets": [
    "Standardize recurring layouts",
    "Validate rendered outputs",
    "Review the narrative"
  ]
}
```

Back the input with a schema that validates layout IDs, required fields, allowed properties, bullet counts, and appropriate text limits. Keep colors, fonts, and spacing in the template, with explicit options where users need variation. Reject unsupported fields rather than silently ignoring them.

Define overflow handling in the component: choose a suitable supported variant, request shorter content, or split into another slide where appropriate. Do not silently discard content or shrink text below the product's readability threshold. Character limits alone do not guarantee fit across fonts, scripts, or renderers.

**Remaining checks:** render the target artifact and inspect clipping, unintended overlaps, missing elements, and data/chart consistency. When editing an existing deck, verify preservation of content and features outside the requested change. Separate mechanical checks from probabilistic visual or semantic review.

**Remaining judgment:** audience, narrative, evidence, emphasis, and component selection. Freeform work may need a different supported workflow; a constrained component library should not erase an explicitly requested design.

## Spreadsheets and Excel

**Repeated mechanics:** the model reconstructs cell addresses, formula ranges, number formats, and chart references for each task.

**Structural improvement:** expose operations over typed tables and stable column IDs. For recurring reports, the model selects grouping dimensions, measures, filters, and an output layout. Tool code resolves ranges, generates formulas, applies formats, and preserves unrelated content.

An illustrative input after the source table has been bound to a workbook:

```json
{
  "operation": "aggregate",
  "tableId": "sales",
  "groupBy": ["month", "department"],
  "measures": [{ "columnId": "revenue", "function": "sum" }],
  "outputLayout": "summary-table"
}
```

Validate identifiers and compatible operations against the actual table schema, not just the JSON shape. Make null handling, duplicate treatment, filters, units, and destination explicit or apply documented defaults suited to the task. Custom analyses may require controlled formula generation instead of a fixed aggregation component.

For file editing, use a working copy and inspect the resulting changes. For a live workbook, bind the workbook, sheet, and allowed write ranges, check for relevant concurrent changes, and avoid duplicating rows or sheets on retries. These boundaries belong in the editing tools.

**Remaining checks:** recalculate with an engine that supports the required workbook features, inspect calculated values, and compare counts or totals with an independently derived expectation. Writing a formula or reading a cached result does not establish that calculation succeeded. No error cells does not establish that the aggregation includes the right rows. Check preservation of formulas and workbook features relevant to the requested edit.

**Remaining judgment:** metric definitions, appropriate aggregation, exceptional data, and interpretation of results. Inspect business assumptions before encoding them in a reusable component.

## Improving a skill itself

If a skill repeatedly instructs the model to reconstruct the same layout or command sequence, extract the stable part into a template or helper that the skill actually invokes. Keep task-dependent choices in the instructions. Add a schema or narrow interface where it removes demonstrated ambiguity, and a relevant check for the behavior that remains uncertain.

Do not create an unused script, empty schema, or asset folder merely to satisfy this hierarchy. Validate the proposed helper on a representative case and confirm that the workflow uses it. Record remaining judgment rather than claiming the new structure guarantees all output quality.
