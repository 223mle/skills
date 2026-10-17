# Designing a spreadsheet or Excel skill

First distinguish file generation/editing from operations on a live workbook. Use the target project's existing workbook API or engine. The calls and resource paths here are proposed interfaces, not working tools supplied by this skill.

## Caller first

For a recurring aggregation, the agent should describe the operation over inspected table/column IDs. The executor resolves physical cells and output bindings.

```json
{
  "operation": "aggregate",
  "requestId": "monthly-sales-001",
  "sourceId": "sales-source",
  "tableId": "sales",
  "groupBy": ["month", "department"],
  "measures": [{"columnId": "revenue", "function": "sum"}],
  "filters": [{"columnId": "status", "operator": "equals", "value": "paid"}],
  "nullPolicy": "skip",
  "duplicatePolicy": "keep",
  "output": {"bindingId": "monthly-summary", "layout": "summary-table", "onExisting": "reject"}
}
```

Validate it with [assets/aggregate-request.schema.json](../assets/aggregate-request.schema.json), then resolve identifiers against the bound workbook and actual table schema. The schema checks shape only; it cannot prove that `revenue` exists, is numeric, uses one currency, or is authorized for this operation. Stable IDs must come from inspection or a maintained registry, not be invented by the model.

Use these explicit starter semantics, adapting them when the product needs different behavior:

- Filters combine with AND; an empty list includes all rows. `equals` compares values of the declared column type, with no implicit string/number/boolean coercion. Strings are case-sensitive. A filter value of the wrong type is rejected before writing.
- `skip` omits missing values from a measure, not a row's values from unrelated measures. `count` counts non-null values in its column. A group with no non-null measure values yields count 0 and sum null. `reject` rejects missing measure values. Missing grouping keys are rejected in this starter contract.
- Duplicate handling runs over the filtered, normalized typed source rows, comparing all declared source columns, including columns not used by the aggregation. Compare values, not formatting or internal row IDs; missing values compare equal to missing values. `reject-exact` rejects identical rows under that definition. It does not infer a business deduplication key or compare only the grouped columns.

## Bind the target outside the semantic request

| Mode | Executor-owned binding and behavior |
|---|---|
| Create/edit a file | Source path or handle, distinct working copy/output target, engine capabilities, allowed changes, and what must survive saving. |
| Edit a live workbook | Actual workbook/sheet/table IDs, allowed write range or named output table, relevant pre-change state, and supported conflict/retry behavior. |

Bind `sourceId` and `output.bindingId` to inspected resources before allowing writes. The model chooses business intent; tool code owns cell addresses, reference generation, table placement, formats, and retry tracking.

`output.onExisting: reject` fails if the destination already contains output. `replace-bound-output` may replace only the previously bound output table/range, after checking its relevant pre-change state and write scope; it must not clear a sheet or unrelated cells. No append behavior is implied. Report the actual changed scope.

The schema's `requestId` is only a key: the executor must implement duplicate-request handling. Check it before applying the destination policy. An identical completed request returns the recorded result/evidence without another write; reuse with different input fails. A missing or ambiguous execution record requires inspecting the destination and reporting uncertainty if completion cannot be established. Merely including an ID does not make writes idempotent.

Use a revision check or compare relevant state immediately before writing if the platform supports it. A conflict requires a refreshed read and a reconsidered patch. If atomic writes or rollback are unavailable, say so and design bounded batches, backups or snapshots where possible, and post-write readback. Do not claim an unconditional transaction across a live workbook. Do not blindly repeat an operation after an ambiguous timeout; inspect whether it took effect first.

Before editing an existing workbook, inspect features needed for preservation, such as macros, pivot tables, external links, charts, or unsupported formulas. Choose a compatible engine or narrow the supported operation explicitly; avoid silently stripping features during a file round trip.

## Resources and execution

For the new skill, reuse or implement only the pieces needed for its actual operations:

| Resource | Concrete responsibility |
|---|---|
| `SKILL.md` | Interpret the request, inspect source columns and metric definitions, select operations, invoke the tool, interpret results. |
| `assets/aggregate-request.schema.json` | Validate the supported aggregation request. |
| `scripts/inspect_workbook.py` or an existing API | Discover identities, table schemas, calculation settings, write scope, and relevant engine capabilities. |
| `scripts/apply_operation.py` or an existing API | Resolve bindings, enforce preconditions, compute/write the result, track retries, and report changed scope. |
| `scripts/check_workbook.py` or an existing API | Inspect persisted values/formulas and preservation, recalculate where needed, compare independent expectations. |

Use a separate contract for operations such as updating an input table or formatting a range; do not overload the aggregation schema with arbitrary cell edits. For a custom analytical task, expose controlled formula generation where needed instead of forcing it into a fixed report component.

The implemented path is: inspect and bind → validate the request → verify schema/type/capability preconditions → prepare the patch → apply within the allowed scope → recalculate when formulas require it → read back/verify → return the artifact or changed target and evidence. Check that dates, timezone/granularity, units, nulls, duplicates, and filters have task-appropriate definitions before encoding them. Do not guess a currency or deduplication rule from appearance alone.

Examples of localized failures are `UNKNOWN_COLUMN`, `INCOMPATIBLE_TYPE`, `OUT_OF_SCOPE_WRITE`, `CONFLICT`, and `CALCULATION_UNAVAILABLE`. Report whether anything changed and what remains unverified. A recalculation flag or cached result is not evidence that an engine has evaluated the formulas. If the required engine is unavailable, leave calculation unverified rather than reporting success.

## A small aggregation fixture with known results

For the request above, use this constructed fixture. Treat the blank revenue cell as missing. Both B rows are intentionally retained by `duplicatePolicy: keep`; the pending A row is filtered out.

| month | department | revenue | status |
|---|---|---:|---|
| 2026-01 | A | 100 | paid |
| 2026-01 | A | | paid |
| 2026-01 | B | 50 | paid |
| 2026-01 | B | 50 | paid |
| 2026-01 | A | 999 | pending |

Expected output groups: **2026-01/A = 100, 2026-01/B = 100**. Their sum **200** is an independent test checksum; the request does not ask for an additional total row. If the measure is changed to `count`, the non-null counts are **A = 1, B = 2**. These are independent expected results, not values read back from the implementation under test.

| Change or failure case | Expected behavior |
|---|---|
| Reorder the physical columns | The same sums; column IDs resolve to the intended values. |
| Rename/remove a bound column without updating its mapping | Reject the unknown binding; do not substitute the neighboring column. |
| Use `nullPolicy: reject` | Reject the missing revenue instead of silently treating it as zero. |
| Use `duplicatePolicy: reject-exact` | Reject the repeated B row. |
| Filter a numeric column using the string `"100"` | Reject the incompatible filter type; do not coerce it silently. |
| Change `requestId` to an unknown field or add an arbitrary range | Schema rejects the unsupported request shape. |
| Repeat the identical request after an ambiguous timeout | Read back/consult operation state; do not append a second summary table. |
| Use a new request ID when the output already exists | With `reject`, report the collision without mutation; with `replace-bound-output`, replace only the bound output after checking its state. |
| Modify the target concurrently | Detect the conflict where supported; do not silently overwrite the newer values. |

For existing-workbook edits, also assert that unrelated values, formulas, and required features survive. Select cases relevant to the supported workflow, using real past failures when available. A green schema check, correct-looking formatting, or absence of Excel error cells cannot establish the business result.
