# Change Decision - Preprocessing - Q59 Dataset Correction

- Date: 2026-07-02
- Owner: Nicholas Wilkins
- Iteration: iter-001
- Affected Version(s): V0, V1, V2
- Category: preprocessing

---

## Summary

Correct the golden dataset entry for Q59 so it reflects the manual park release procedure that is actually present in the source material.

---

## Context

**Problem Identified:**
Q59 is currently scored as invalid, but the manual includes a manual park release section that answers the substance of the question. This makes the current evaluation misleading for all three versions.

**Questions Affected:**
- Q59
- Broader invalid-question metrics, because the mislabeled row distorts the unsupported-prompt bucket

**Why This Approach:**
The source support is already present, so the cleanest fix is to correct the dataset instead of forcing the agents to keep failing the question.

---

## Change Details

### Category: Preprocessing

**File(s) Modified:**
- `src/evaluation/data/golden.jsonl` (proposed)

**Change:**
Update Q59 so the question, truth, and source metadata reflect the manual park release procedure instead of treating it as unsupported.

**Rationale:**
This removes a false failure and gives a cleaner read on the unsupported-spec refusal change and the remaining agent regressions.

---

## Expected Outcome

**If Successful:**
- Better correctness and grounding signal for all three versions on Q59
- Slightly improved overall metrics across the run
- Cleaner invalid-question analysis after the next rerun

**If Unsuccessful:**
- Q59 still behaves like an unsupported item after correction
- The next run continues to show the same invalid-question pattern once the dataset is fixed

---

## Decision

The current dataset label is inconsistent with the source material, so correcting Q59 is the highest-value next step before making another instruction or preprocessing change.

---

## Next Steps

Rerun the pipeline after the Q59 correction, then decide whether the unsupported-spec refusal needs a stricter fallback or whether table preprocessing is the next best place to refine.
