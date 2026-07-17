# Run Report - iter-001 - 2026-07-02

- Run ID: iter-001
- Date: 2026-07-02
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: Unsupported-spec refusal instruction update

---

## Executive Summary

This run is mixed in terms of the results. The dashboard shows V2 improving on correctness and grounding and lowering hallucinations, while V0 and V1 both regressed on hallucination rate. The biggest remaining failure mode is still unsupported or out-of-scope prompts, but Q59 now looks like a dataset-label problem rather than an agent failure: the source contains manual park release instructions, while the golden row marks the item invalid. The new refusal wording also did not eliminate hallucinations on horsepower, winter tire, or firmware questions, and in a few trim-specific cases it shifted the answer toward a clarifying question instead of a clean refusal.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|-----|
| Correctness (raw avg) | 4.3 | 4.3 | 4.2 |
| Correctness (normalized) | 0.86 | 0.86 | 0.85 |
| Grounding (raw avg) | 3.7 | 3.8 | 3.7 |
| Grounding (normalized) | 0.74 | 0.76 | 0.74 |
| Hallucination True Rate | 14% | 14% | 20% |

### Key Takeaways

- V0 is effectively flat on correctness but weaker on grounding and worse on hallucinations.
- V1 is slightly down on correctness, slightly up on grounding, and worse on hallucinations.
- V2 is the only version that clearly improved overall, but it still has the highest remaining hallucination rate in the invalid-question set.

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|-------|
| factual | 23 | 0.85 | 0.83 | 0.82 | Still the weakest grounded category; narrow explanations keep drifting beyond the source. |
| procedural | 10 | 1.00 | 0.98 | 0.96 | Stable overall, with only small grounding loss. |
| table | 21 | 0.91 | 0.90 | 0.88 | Still sensitive to table structure; V0 remains strongest here. |
| invalid | 15 | 0.69 | 0.76 | 0.77 | Main hallucination driver; the refusal change did not fully solve unsupported spec prompts. |

---

## Failure Analysis

### Top Failure Categories

1. **Unsupported or hallucinated answers to invalid / out-of-scope prompts**
   - Examples: Q55, Q58, Q61, Q64, Q67, Q69
   - Description: The model still invents trim-specific features, horsepower, firmware, tire, and capability details when the source does not support them.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Keep the refusal rule, but make it a direct unsupported-answer fallback and avoid trim-specific follow-up suggestions.

2. **Table structure and maintenance-spec drift**
   - Examples: Q16, Q18, Q47, Q51
   - Description: Multi-value table questions still lose attachment between labels, units, and values.
   - Affected Versions: All three versions, especially V1 and V2 on this run
   - Suggested Fix: Preserve table semantics more faithfully in preprocessing before changing the instructions again.

3. **Narrow factual explanations with extra unsupported detail**
   - Examples: Q26, Q36, Q49
   - Description: Answers are directionally correct but add unsupported elaboration and lose grounding.
   - Affected Versions: All three versions
   - Suggested Fix: Bias toward quote-bound paraphrase for definition-style questions.

### Per-Version Summary

**V0:** 10 hallucinations, weaker grounding, and the largest regression in grounding. It is still strong on tables but now worse on the invalid set.

**V1:** 10 hallucinations, slight grounding improvement, and a small correctness drop. The refusal update did not materially improve the invalid questions.

**V2:** 14 hallucinations, but better correctness and grounding overall. It improved, yet remains brittle on factual and table-heavy rows.

---

## Data Issue

Q59 should be corrected before the next comparison. The golden dataset currently marks the question as invalid, but the source text and the model outputs show a manual park release procedure in the manual. That makes the current score for this item misleading for all three versions.

---

## Recommendations for Next Iteration

1. **Fix the golden dataset entry for Q59 and rerun the comparison.** This should improve the signal for all three versions and establish a cleaner baseline for the next change.
2. **Tighten unsupported-spec refusal wording.** The current instruction update did not solve horsepower, winter tire, or firmware hallucinations, and it sometimes shifts to trim-specific clarifying language instead of a direct refusal.
3. **Revisit table preprocessing only after the dataset correction.** The table and maintenance-spec rows still look more fragile than the procedural questions, but that signal is cleaner once Q59 is fixed.
