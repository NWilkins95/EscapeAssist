# Run Report - iter-002 - 2026-07-03

- Run ID: iter-002
- Date: 2026-07-03
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: Q59 restored to the invalid bucket and expected to trigger a refusal or guardrail trip response.

---

## Executive Summary

This run is mostly stable at the procedural level, but it is not a clean flatline. V0 is effectively flat on correctness, V1 regains a small correctness lift, and V2 regresses back toward its baseline on correctness, grounding, and hallucination rate. The main correction is Q59: the row should stay in the invalid or blocked bucket because the manual does not explain how to override control modules, and the repeated safety-filter fallback is the expected refusal or guardrail-trip behavior for that question.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|----|
| Correctness (raw avg) | 4.29 | 4.35 | 4.09 |
| Correctness (normalized) | 0.86 | 0.87 | 0.82 |
| Grounding (raw avg) | 3.73 | 3.75 | 3.57 |
| Grounding (normalized) | 0.75 | 0.75 | 0.71 |
| Hallucination True Rate | 14% | 14% | 22% |

### Key Takeaways

- V0 is effectively flat on correctness, with a slight grounding uptick and unchanged hallucination rate.
- V1 improves slightly on correctness, slips slightly on grounding, and stays flat on hallucinations.
- V2 regresses on correctness, grounding, and hallucinations, so it is the weakest result in this run.
- Q59 belongs in the invalid or blocked bucket, not the procedural set.

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|-------|
| factual | 23 | 0.83 | 0.83 | 0.77 | Still the noisiest category; warning-light and spec-style facts drift more than procedural rows. |
| procedural | 10 | 0.89 | 0.89 | 0.89 | The most stable category, with zero hallucinations across all three versions. |
| table | 21 | 0.93 | 0.93 | 0.84 | Table rows remain sensitive to value-label pairing and unit fidelity, especially for V2. |
| invalid | 15 | 0.76 | 0.81 | 0.81 | The invalid bucket is still the main hallucination driver, and Q59 belongs here rather than in the procedural set. |

---

## Failure Analysis

### Top Failure Categories

1. **Unsupported or hallucinated answers to invalid / out-of-scope prompts**
   - Examples: Q55, Q58, Q61, Q64, Q67, Q69
   - Description: The model still invents trim-specific features, horsepower, firmware, tire, and capability details when the source does not support them.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Keep the refusal rule, but make the fallback direct and avoid trim-specific follow-up suggestions.

2. **Table structure and maintenance-spec drift**
   - Examples: Q16, Q18, Q47, Q51
   - Description: Multi-value table questions still lose attachment between labels, units, and values.
   - Affected Versions: All three versions, especially V2 on this run
   - Suggested Fix: Preserve table semantics more faithfully in preprocessing before changing the instructions again.

3. **Q59 invalid / blocked prompt behavior**
   - Examples: Q59
   - Description: The prompt asks for a control-module override that the owner's manual does not provide, so the refusal or safety-filter fallback is the expected behavior and the item should stay in the invalid bucket.
   - Affected Versions: All three versions
   - Suggested Fix: Restore Q59 to invalid and keep any guardrail-specific measurement in a separate test item.

---

## Per-Version Summary

**V0:** Correctness is flat, grounding is slightly up, and hallucination rate is unchanged. Procedural rows are still strong, but factual rows are more brittle than they were in the previous run.

**V1:** Correctness improved slightly, grounding dipped slightly, and hallucination rate stayed flat. This is the least noisy run for V1 since the baseline, but the gain is small.

**V2:** Correctness and grounding both regressed back toward the baseline, and hallucination rate increased. This is the clearest sign that the current setup is still sensitive to wording and extraction issues.

---

## Recommendations for Next Iteration

1. **Restore Q59 to the invalid bucket and rerun the comparison.** The manual does not tell users how to override control modules, so the safety-filter fallback is the correct expected behavior.
2. **Tighten unsupported-spec refusal wording.** The current instruction update did not solve horsepower, winter tire, or firmware hallucinations, and it sometimes shifts to trim-specific clarifying language instead of a direct refusal.
3. **Revisit table preprocessing only after the Q59 correction.** The table and maintenance-spec rows still look more fragile than the procedural questions, but that signal is cleaner once Q59 is fixed.
