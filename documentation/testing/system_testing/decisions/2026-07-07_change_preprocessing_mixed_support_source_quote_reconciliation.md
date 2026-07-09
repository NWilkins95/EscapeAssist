# Change Decision - Preprocessing - Mixed Support Source Quote Reconciliation

- Date: 2026-07-07
- Owner: Nicholas Wilkins
- Iteration: iter-004
- Affected Version(s): V0, V1, V2
- Category: preprocessing

---

## Summary

Reconcile benchmark rows whose current source_quote and ground truth omit manual-supported general guidance, and separate those from true unsupported-spec failures.

---

## Context

The 2026-07-04 instruction update tightened answer wording, but the latest run shows that not every failing row is a pure refusal problem.

The snow-chain rows are the clearest example: the manual has general snow-chain guidance, but the current benchmark still treats these questions as trim-specific invalid prompts with N/A source quotes.

The same low-grounding pattern also shows up in factual and warning-light rows such as child seating, seatbelt reminder, fuel gauge, battery warning, door ajar, powertrain fault, Auto Hold, the oil-life monitor, and the automatic transmission fluid interval question.

True unsupported-spec prompts such as horsepower, firmware, and the manual override question still need direct refusal behavior, and Q59 remains frozen as a guardrail probe rather than a moving benchmark row.

---

## Change

Review the retrieved chunks used by the model for low-grounding rows and update the golden dataset so the source_quote and truth reflect the actual manual guidance where it exists.

Proposed updates:

- Add the manual's general snow-chain guidance to the gold rows for Q64, Q67, and similar questions instead of leaving those rows as N/A invalids.
- Review factual and warning-light rows like Q2, Q6, Q29, Q31, Q32, Q36, Q43, Q49, and Q51 to see whether the retrieved chunks support the current answer or whether the gold text needs expansion.
- Keep horsepower, firmware, and manual override rows as true unsupported-spec refusal cases.
- Preserve the strict refusal wording for rows where the manual genuinely does not provide an answer.

---

## Why This Change

This separates benchmark coverage gaps from actual hallucinations.

It also prevents the next iteration from overfitting instruction wording to rows that are really missing source coverage rather than missing refusal behavior.

---

## Expected Outcome

- The snow-chain questions are credited against the correct manual guidance instead of being treated as trim-only invalid prompts.
- Low-grounding factual and warning-light rows are either re-baselined or left in place with a clearer explanation of what the source quote supports.
- True unsupported-spec questions remain refusal tests.
- Future run comparisons separate source-quote coverage problems from instruction problems.

---

## Decision

Update the golden dataset source_quote and truth for low-grounding (raw score of 3 or less) mixed-support rows before making another instruction change.

---

## Next Step

Inspect the retrieved chunks in the response logs for Q2, Q6, Q29, Q31, Q32, Q36, Q43, Q49, Q51, Q64, Q67, and similar rows, then revise the benchmark and rerun the comparison.
