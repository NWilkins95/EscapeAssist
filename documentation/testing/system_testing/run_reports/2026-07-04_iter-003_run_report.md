# Run Report - iter-003 - 2026-07-04

- Run ID: iter-003
- Date: 2026-07-04
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: Q59 locked as an invalid guardrail probe; factual brevity remains a follow-up target

---

## Executive Summary

This run is the first one with a clear version-level gain: V2 improves on correctness, grounding, and hallucination rate in a way that is larger than normal run-to-run wobble. V0 is mostly flat with a small hallucination increase, and V1 is also mostly flat with a small grounding improvement and lower hallucination rate. Q59 is now stable across all three versions and should be treated as a locked invalid/guardrail probe rather than a moving benchmark row.

The remaining weak points are unchanged in shape, even though their severity shifted a bit. Factual rows are still the weakest category across all agents because the answers keep elaborating beyond the retrieved text, unsupported-spec invalid prompts still trigger hallucinations on horsepower, winter tire, and firmware questions, and V2 table rows still lag procedural rows even after improving this run.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|----|
| Correctness (raw avg) | 4.30 | 4.35 | 4.26 |
| Correctness (normalized) | 0.86 | 0.87 | 0.85 |
| Grounding (raw avg) | 3.71 | 3.81 | 3.71 |
| Grounding (normalized) | 0.74 | 0.76 | 0.74 |
| Hallucination True Rate | 17% | 13% | 19% |

### Key Takeaways

- V0 is effectively flat on correctness, but grounding slipped slightly and hallucination rate increased.
- V1 is also mostly flat on correctness, with a small grounding gain and a lower hallucination rate.
- V2 is the only version with a clear improvement on correctness, grounding, and hallucination rate.
- Q59 is stable now and should be treated as a locked invalid/guardrail probe rather than a comparison row.

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|-------|
| factual | 23 | 0.83 | 0.82 | 0.83 | Still the weakest category overall because all three agents tend to elaborate beyond the retrieved text. |
| procedural | 10 | 0.96 | 0.98 | 0.98 | Procedural rows remain the strongest category and continue to show zero hallucinations across all versions. |
| table | 21 | 0.92 | 0.90 | 0.88 | V2 improved, but table cleanup remains the least stable part of the pipeline after procedural rows. |
| invalid | 15 | 0.76 | 0.83 | 0.77 | Q59 is now stable and no longer distorts this bucket, but unsupported-spec prompts still drive the remaining errors. |

---

## Stability Review

- Answer text changed on 56/69 V0 questions, 57/69 V1 questions, and 54/69 V2 questions compared with the previous run.
- Score changes were smaller than the surface wording drift: 15 questions changed score in V0, 14 in V1, and 17 in V2.
- Q59 is stable for all three versions now: each agent returned the safety-filter fallback and scored 5/5, so it is no longer a moving target.
- The clearest non-noise shifts are V2’s factual and table gains, V1’s regression on the automatic-transmission-fluid interval question, and V0’s modest factual regressions on child seating and towing/carrying-load guidance.

### Deviations Beyond Normal Noise

- V2’s improvement is the only broad shift that clearly exceeds normal run-to-run variation. The gain is concentrated in factual rows like seatbelt reminder, oil specifications, and battery warning, plus a smaller table improvement.
- V1’s automatic-transmission-fluid interval question regressed sharply, from a clean answer to a hallucination. That is a real degradation rather than a rounding artifact.
- V0 had two modest regressions that are worth noting: children seating and towing/carrying-load maintenance both flipped into hallucination territory.
- Q59 is no longer a source of instability. Its stable guardrail-trip behavior should be preserved, not retuned.

---

## Failure Analysis

### Top Failure Categories

1. **Factual elaboration beyond the retrieved text**
   - Examples: Q2, Q7, Q21, Q26, Q36, Q49
   - Description: All three agents still add context, examples, or warnings that were not in the source, even when the core answer is correct.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Tighten factual prompts and postprocessing so answers stay closer to retrieved text with no extra elaboration.

2. **Unsupported-spec invalid prompts**
   - Examples: Q55, Q58, Q61, Q64, Q67, Q69
   - Description: The current instruction update still does not fully suppress hallucinations on horsepower, winter tire, and firmware questions, and it sometimes shifts to trim-specific clarifying language instead of a direct refusal.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Keep the refusal rule, but make the fallback direct and avoid trim-specific follow-up suggestions.

3. **V2 table cleanup after preprocessing**
   - Examples: Q16, Q18, Q47, Q50, Q51
   - Description: V2 table rows improved in this run, but the category is still weaker than procedural rows, which suggests the preprocessing cleanup layer is still leaking signal.
   - Affected Versions: V2 in particular
   - Suggested Fix: Revisit the post-preprocessing cleanup path after the factual prompt tightening pass.

---

## Per-Version Summary

**V0:** Essentially flat overall. The run gained a little correctness but lost a little grounding and picked up a higher hallucination rate. Procedural rows are still strong, but factual rows are more brittle than before.

**V1:** Also mostly flat overall. Grounding improved slightly and hallucination dropped slightly, but the automatic-transmission-fluid interval row regressed sharply. That makes the run mixed rather than cleanly improved.

**V2:** The clear winner in this run. It improved on correctness, grounding, and hallucination rate, driven mostly by factual rows and some table cleanup. Even so, table and unsupported-spec invalid rows remain the main unresolved weaknesses.

---

## Recommendations for Next Iteration

1. **Tighten unsupported-spec refusal wording.** The current instruction update still does not solve horsepower, winter tire, or firmware hallucinations, and it sometimes shifts to trim-specific clarifying language instead of a direct refusal.
2. **Tighten factual answers to the retrieved text only.** Factual elaboration remains the most consistent cross-agent weakness, but it should be constrained directly to the retrieved text after the refusal wording is fixed.
3. **Revisit V2 table cleanup.** The table layer improved in this run, but it still trails the other answer patterns and remains the clearest preprocessing follow-up.
