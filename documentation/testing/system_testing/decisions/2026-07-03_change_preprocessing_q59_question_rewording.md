# Change Decision - Preprocessing - Q59 Invalid Restoration

- Date: 2026-07-03
- Owner: Nicholas Wilkins
- Iteration: iter-002
- Affected Version(s): V0, V1, V2
- Category: preprocessing

---

## Summary

Restore Q59 to the invalid bucket. The manual does not provide instructions for manually overriding the automatic transmission control module, so a refusal or safety-filter trip response is the expected behavior rather than a procedural grounding target.

---

## Context

**Problem Identified:**
Q59 was temporarily treated as a procedural grounding question, but that interpretation is incorrect. Owners manuals do not typically explain how to override control modules, and the consistent safety-filter fallback indicates the item belongs in the invalid / blocked bucket.

**Questions Affected:**
- Q59
- The invalid-question bucket, because the row should not be scored as procedural

**Why This Approach:**
The question is not a valid grounding target for the owner's manual. Restoring it to invalid preserves the benchmark's intent and keeps the refusal or guardrail-trip behavior from being misread as a retrieval failure.

---

## Change Details

### Category: Preprocessing

**File(s) Modified:**
- `src/evaluation/data/golden.jsonl` (next iteration)

**Change:**
Revert Q59 to an invalid benchmark row that expects a refusal or guardrail-trip outcome instead of a procedural answer.

**Rationale:**
This keeps the harness focused on retrieval and grounding, while preventing a non-answerable control-module override prompt from contaminating the procedural set.

---

## Expected Outcome

**If Successful:**
- Q59 scores consistently as invalid or blocked, with the refusal or guardrail-trip response preserved
- The benchmark becomes easier to interpret question by question
- The invalid-question and table-failure signals become cleaner

**If Unsuccessful:**
- Q59 continues to bounce between fallback and procedural output
- The metric trend remains dominated by a single mislabeled row

---

## Decision

Q59 should be restored to invalid before the next comparison.

---

## Next Steps

Rerun the pipeline after the Q59 rollback, then move the next iteration toward unsupported horsepower and trim-feature prompts.
