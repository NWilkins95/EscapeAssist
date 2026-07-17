# Run Report - iter-004 - 2026-07-07

- Run ID: iter-004
- Date: 2026-07-07
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: 2026-07-04 instruction tightening remained in effect; low-grounding rows across factual, warning-light, maintenance, and invalid questions now point to both source-quote gaps and true refusal failures

---

## Executive Summary

This run is still roughly flat at the metric level, but the question-by-question story is more important than the averages. V0 gained grounding while correctness slipped very slightly and hallucination stayed flat. V1 lost a little grounding but also reduced hallucination a bit. V2 kept correctness flat, gained a small amount of grounding, and increased hallucination slightly.

The 2026-07-04 instruction update is visible in the answers: they are tighter and more constrained to the retrieved text than before. The remaining issue is not one single failure mode. Some rows are still true unsupported-spec prompts and need a direct refusal, especially horsepower, firmware, and the manual override row. Other rows are simply under-grounded even when the answer is not fully wrong. The low-grounding set is broader than snow chains: in V0 and V1, questions like child seating, seatbelt reminder, fuel gauge, battery warning, door ajar, powertrain fault, Auto Hold, the oil-life monitor, and the automatic transmission fluid interval still land at grounding 3 or less; in V2, the same pattern shows up on the warning-light, maintenance, and oil-capacity rows as well. The snow-chain questions still look like benchmark/source-quote mismatches because the manual has general snow-chain guidance, but the current gold rows still treat them as trim-specific invalids with N/A source quotes.

Q59 is no longer uniform across versions. V0 and V2 now return the safety-filter fallback, but V1 still falls through into a procedural answer. That makes it a guardrail problem, not a cleanly solved invalid row.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|----|
| Correctness (raw avg) | 4.28 | 4.33 | 4.26 |
| Correctness (normalized) | 0.86 | 0.87 | 0.85 |
| Grounding (raw avg) | 3.81 | 3.75 | 3.72 |
| Grounding (normalized) | 0.76 | 0.75 | 0.74 |
| Hallucination True Rate | 17% | 12% | 20% |

### Key Takeaways

- V0 gained grounding but lost a little correctness, while hallucination held flat.
- V1 lost grounding slightly, but hallucination improved slightly.
- V2 stayed flat on correctness, gained a little grounding, and picked up a small hallucination increase.
- The answer text is tighter to source quotes, but several rows are still under-grounded at 3 or below, including factual, warning-light, maintenance, and invalid questions.
- Snow-chain rows are still a clear source-quote mismatch, but they are only part of the broader low-grounding pattern.

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|-------|
| factual | 23 | 0.83 | 0.83 | 0.81 | Still the weakest category because answers keep elaborating beyond the retrieved text, even when the wording is tighter. Representative rows include child seating, seatbelt reminder, fuel gauge, battery warning, and the oil-life monitor. |
| procedural | 10 | 1.00 | 0.98 | 0.98 | Procedural rows remain the strongest category and continue to show zero hallucinations across all versions. |
| table | 21 | 0.89 | 0.93 | 0.84 | V1 is the strongest table run here; V2 is still the most volatile, so table cleanup remains relevant but is no longer the main story. |
| invalid | 15 | 0.76 | 0.76 | 0.85 | This bucket mixes true refusal failures with rows that should probably be re-baselined because the manual has relevant general guidance, especially the snow-chain questions. |

---

## Stability Review

- Answer text changed on 13/69 V0 questions, 17/69 V1 questions, and 20/69 V2 questions compared with the previous run.
- The clearest score shifts are V0's grounding gain, V1's slight grounding/hallucination loss, and V2's slight grounding/hallucination gain.
- Q59 is still not uniform: V0 and V2 return the safety-filter fallback, but V1 still produces a procedural answer.
- The low-grounding set is wider than the snow-chain family. Warning-light, maintenance, and factual rows also remain at 3 or below in multiple versions, so the next pass should not focus only on invalid prompts.

### Deviations Beyond Normal Noise

- V0's grounding gain is real, but the run still has a horsepower hallucination plus several grounded-at-3 rows in the factual and warning-light clusters.
- V1's q59 regression is the clearest guardrail failure in this run.
- V2 is the closest to the manual on the snow-chain row, which suggests the current source quote is too thin for that question, but V2 also still has several 3-or-below grounding rows in the oil-capacity, warning-light, and towing categories.
- q51 still looks like a genuinely brittle factual row because the automatic-transmission-fluid interval answer swings across runs.

---

## Failure Analysis

### Top Failure Categories

1. **Low-grounding rows that are only partially supported by the retrieved text**
   - Examples: Q2, Q6, Q7, Q8, Q9, Q29, Q31, Q32, Q34, Q36, Q41, Q43, Q44, Q48, Q49, Q51, Q52, Q64, Q67
   - Description: The latest run shows a broad cluster of rows at grounding 3 or below, including child seating, seatbelt reminder, fuel gauge, warning lights, Auto Hold, oil-life monitoring, maintenance intervals, and the snow-chain questions. Some of these are true refusal failures, but several are better described as answers that went beyond the source quote or were scored against an underspecified gold row.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Review the retrieved chunks for each low-grounding row, separate true unsupported-spec cases from mixed-support manual guidance, and update the golden dataset source_quote/truth where the manual actually contains relevant general guidance.

2. **True unsupported-spec refusal failures**
   - Examples: Q58, Q59, Q61
   - Description: Horsepower, manual override, and firmware remain genuinely unsupported. V0 still hallucinates horsepower, V1 still falls through on Q59, and firmware still fails across versions.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: Keep the direct refusal rule strict and keep trim-related follow-up language out of the unsupported-spec path.

3. **Factual elaboration beyond the retrieved text**
   - Examples: Q2, Q7, Q21, Q36, Q49
   - Description: The answers are tighter than before, but several factual rows still add context that is not in the source quote.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: After the benchmark split is cleaned up, keep tightening source-only paraphrase and rerun.

---

## Per-Version Summary

**V0:** Grounding improved the most of the three versions, but correctness slipped a bit and hallucination held flat. The weak rows are spread across factual, warning-light, maintenance, and invalid categories, with horsepower still a true unsupported failure and snow chains still a source-quote mismatch.

**V1:** Slightly weaker on grounding and slightly better on hallucination. Q59 is still the clearest problem row because it falls through into a procedural answer instead of refusing, but the broader low-grounding set is not confined to invalid prompts.

**V2:** Flat correctness, a small grounding gain, and a small hallucination increase. It is the closest to the manual on the snow-chain row, which is a strong hint that the current gold row is under-specified, but V2 also still has several other 3-or-below grounding rows.

---

## Recommendations for Next Iteration

1. **Rebaseline the low-grounding rows whose answers still go beyond the source quote.** Review every latest-run question at grounding 3 or below, identify which ones need source-quote or truth updates, and expand the benchmark where the manual already provides relevant general guidance.
2. **Keep the unsupported-spec refusal path strict for truly absent details.** Horsepower, firmware, and manual override questions should remain direct refusal cases, with no trim-related follow-up language added back in.
3. **Rerun after the benchmark split is cleaned up, then revisit the remaining factual and table drift.** Once the mixed-support rows are corrected, check whether the tighter instruction set holds and whether the factual and table rows still need another pass.
