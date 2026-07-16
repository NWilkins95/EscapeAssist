# Run Report - iter-005 - 2026-07-11

- Run ID: iter-005
- Date: 2026-07-11
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: corrected golden dataset remained in effect; this run validates the benchmark cleanup and shows the current ceiling of the black-box retrieval setup

---

## Executive Summary

This run is the clearest sign yet that the corrected golden dataset helped. All three versions improved over the baseline on normalized correctness and grounding, and hallucination is down overall across the run set. The strongest version is still V1 on correctness, while V0 and V2 are essentially tied on grounding. V2 shows the largest total lift from baseline, especially on grounding and the invalid-question bucket.

The main story is no longer one dominant failure mode. The benchmark cleanup has removed a lot of noise from the mixed-support invalid rows, especially the snow-chain rows and the old Q59 guardrail probe. What remains is a smaller set of true unsupported-spec failures plus a broader retrieval-bound ceiling on factual and table questions. In other words, the system is now limited more by what the retrieval layer gives it than by the prompt or the benchmark wording.

At this point, further accuracy gains would require influence over retrieval. With the current black-box retrieval boundary, this looks like the practical plateau for instruction and preprocessing work alone.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|----|
| Correctness (raw avg) | 4.35 | 4.43 | 4.30 |
| Correctness (normalized) | 0.87 | 0.89 | 0.86 |
| Grounding (raw avg) | 3.90 | 3.87 | 3.91 |
| Grounding (normalized) | 0.78 | 0.77 | 0.78 |
| Hallucination True Rate | 16% | 13% | 17% |

### Key Takeaways

- V1 is the strongest version on correctness and hallucination rate.
- V0 and V2 are effectively tied on grounding, with V2 slightly ahead in raw precision but rounding to the same 0.78.
- Compared with iter-004, all three versions gained on correctness and grounding overall.
- Hallucination moved down overall versus the baseline, even though the per-version story is mixed.
- The corrected golden dataset did real work here: the invalid bucket is now a cleaner refusal test and no longer dominated by benchmark/source-quote mismatch noise.

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|-------|
| factual | 23 | 0.89 | 0.88 | 0.83 | Still the weakest broad category because answers often stay close to the source but add a little extra context. |
| procedural | 10 | 0.98 | 1.00 | 0.96 | Procedural rows remain the strongest category and still have zero hallucinations across all versions. |
| table | 21 | 0.88 | 0.89 | 0.83 | V1 leads the table category; V2 is still the most brittle on exact-value and comparison rows. |
| invalid | 15 | 0.76 | 0.83 | 0.88 | This is the clearest sign of benchmark cleanup. The invalid bucket is now much cleaner, with V2 leading after the snow-chain and guardrail rows were rebaselined. |

### Category Insights

**Factual Questions:**
- The answers are tighter than earlier runs, but some rows still drift just beyond the quoted source.
- The remaining losses are mostly small grounding penalties rather than outright wrong answers.

**Procedural Questions:**
- These remain the most stable rows in the benchmark.
- V1 is now effectively perfect here, and V0/V2 are only a small step behind.

**Table Questions:**
- V1 is still the best version for table-heavy questions.
- V2 is less brittle than before, but it still drops more points than V1 on comparison-heavy rows.

**Invalid Questions:**
- The invalid bucket now looks like a real refusal test again rather than a mixed-support catchall.
- Q59 is stable in all three versions.
- The snow-chain rows are now much better separated from the true unsupported-spec failures.

---

## Stability Review

- Q59 is now stable across all three versions and no longer distorts the run.
- The biggest gain versus iter-004 is V2 grounding, which improved materially once the benchmark cleanup took effect.
- V0 improved the most on correctness relative to the previous run, while V1 recovered on correctness but gave back a little hallucination rate.
- The overall lift from baseline is real, but the run also shows a plateau: the remaining misses are mostly source-coverage and retrieval-bound.

### Deviations Beyond Normal Noise

- V0’s correctness and grounding gains are meaningful, but the version still leaks on unsupported-spec questions more often than the other two.
- V1 is the best balanced version overall, but its invalid bucket still needs cleaner refusal behavior on the last few unsupported rows.
- V2 now benefits the most from the benchmark correction, especially on the invalid bucket, but it still trails V1 on factual and table stability.

---

## Failure Analysis

### Top Failure Categories

1. **Retrieval-bound factual and table elaboration**
   - Examples: Q2, Q6, Q29, Q31, Q32, Q36, Q41, Q43, Q49, Q51
   - Description: The answers are often correct, but they still add a small amount of unsupported context or miss one piece of the source quote.
   - Affected Versions: V0, V1, V2
   - Suggested Fix: This is now mostly a retrieval problem, not a prompt problem. Further lift would require better control over what the model sees.

2. **True unsupported-spec refusal failures**
   - Examples: Q58, Q61, Q64
   - Description: Horsepower and firmware remain genuinely unsupported, and the snow-chain prompt on the Active model still has a failure case in at least one version.
   - Affected Versions: Mostly V0, with residual misses in V1/V2 on the firmware and snow-chain rows
   - Suggested Fix: Keep the refusal path strict and do not reintroduce trim-capability speculation.

3. **Mixed-support benchmark cleanup that is now mostly resolved**
   - Examples: Q59, Q67
   - Description: These rows were previously noisy because the gold data did not cleanly separate unsupported trim questions from manual-supported general guidance. They now behave much more like proper benchmark rows.
   - Affected Versions: All three versions, with V2 showing the strongest benefit from the cleanup
   - Suggested Fix: Keep the corrected gold rows frozen so the next run measures model behavior rather than benchmark drift.

### Per-Version Failure Summary

**V0:**
- Still the weakest version on unsupported-spec leakage.
- Better than before on factual grounding, but it remains the most likely to overstate unsupported details.

**V1:**
- Best overall balance of correctness, grounding, and hallucination rate.
- Its main remaining weakness is the last few retrieval-bound factual/table rows.

**V2:**
- Biggest total improvement from baseline.
- The benchmark cleanup helped it a lot, especially on invalid rows, but it still trails V1 on factual and table consistency.

---

## Per-Version Summary

**V0:** Improved on correctness, grounding, and hallucination versus the previous run, but it is still the leakiest version on unsupported-spec prompts. The win is real, but the remaining ceiling is now obvious.

**V1:** The strongest overall version in this run. It recovered on correctness and grounding, and it remains the best choice if the goal is balanced performance rather than a single-category win.

**V2:** The biggest beneficiary of the corrected golden dataset. It now leads the invalid bucket and posts a strong grounding gain, but it still lags V1 on factual and table stability.

---

## Recommendations for Next Iteration

1. Freeze the corrected golden dataset and treat this run as the current benchmark state.
2. Stop expecting large gains from instruction or preprocessing alone; the remaining errors are mostly bounded by the retrieval layer.
3. If more accuracy is required, move to a workflow where retrieval can be influenced or audited directly.

---

## Key Metrics Summary Table

| Metric | V0 | V1 | V2 | Best | Gap (Best to Worst) |
|--------|----|----|-----|------|---------------------|
| Correctness (norm) | 0.87 | 0.89 | 0.86 | V1 | 0.03 |
| Grounding (norm) | 0.78 | 0.77 | 0.78 | V0 / V2 | 0.01 |
| Hallucination Rate | 16% | 13% | 17% | V1 | 4 pts |

---

## Artifacts & References

- **Evaluation Dashboard:** `src/user_interface/pages/evaluation_dashboard.py`
- **Raw Exports:**
  - Answers: `src/evaluation/outputs/answers/{V0,V1,V2}/`
  - Evaluations: `src/evaluation/outputs/evaluations/{V0,V1,V2}/`
  - Judge Calibration: `src/evaluation/outputs/judge_calibration/`
- **Golden Dataset:** `src/evaluation/data/golden.jsonl` (69 questions)
- **Judge Prompt:** `src/evaluation/judge/judge_instructions.py`
- **Agent Instructions:** `src/user_interface/workflows/{V0,V1,V2}workflow.py`
- **Preprocessing Code:**
  - V0: `src/user_interface/workflows/V0workflow.py`
  - V1: `src/user_interface/workflows/V1workflow.py`
  - V2: `src/user_interface/workflows/V2workflow.py`
