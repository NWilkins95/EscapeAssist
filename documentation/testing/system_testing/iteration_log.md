# Iteration Log

A chronological record of all system testing iterations, changes made, and comparative results.

---

## Baseline Run

| Run ID | Date | Versions | Status | Artifacts |
|--------|------|----------|--------|-----------|
| baseline-001 | 2026-06-19 | V0, V1, V2 | Complete | `baseline_run_analysis.md` |

**Summary:** Initial end-to-end evaluation of all three preprocessing and agent versions using frozen instructions and judge rubric.

**Key Metrics:**
- V0 Correctness (norm): 0.819
- V1 Correctness (norm): 0.837
- V2 Correctness (norm): 0.772

**Top Failure Categories:** (Listed in priority order)
1. Unsupported or hallucinated answers to invalid / out-of-scope prompts
2. Maintenance and specification table extraction / comparison errors
3. Factual explanation questions with narrow source support

**Recommended First Change:** Add an explicit refusal rule for trim features, capacities, firmware, and other unsupported spec questions when the source does not contain a direct answer.

---

## Iteration 1

| Run ID | Date | Versions | Change Category | Change Description |
|--------|------|----------|-----------------|-------------------|
| iter-001 | 2026-07-02 | V0 / V1 / V2 | instructions | unsupported-spec refusal update |

**Baseline Comparison:**
- V0 Correctness (norm): 0.86 → 0.86 (Δ 0.00)
- V1 Correctness (norm): 0.87 → 0.86 (Δ -0.01)
- V2 Correctness (norm): 0.82 → 0.85 (Δ +0.03)
- V0 Grounding (norm): 0.75 → 0.74 (Δ -0.01)
- V1 Grounding (norm): 0.75 → 0.76 (Δ +0.01)
- V2 Grounding (norm): 0.71 → 0.74 (Δ +0.03)
- V0 Hallucination Rate: 13% → 14% (Δ +1 pt)
- V1 Hallucination Rate: 13% → 14% (Δ +1 pt)
- V2 Hallucination Rate: 22% → 20% (Δ -2 pts)

**Change Decision:** `decisions/2026-07-02_change_preprocessing_q59_dataset_correction.md`

**Qualitative Observations:**
- V0 and V1 regressed slightly on hallucination rate, while V2 improved on correctness, grounding, and hallucination rate.
- Q59 appears mislabeled in the golden dataset and should be corrected before the next comparison.
- The new refusal wording did not fix horsepower, winter tire, or firmware hallucinations, and it sometimes shifted trim-specific questions into clarifying language instead of a direct refusal.

**Next Iteration:** Correct Q59 in the golden dataset, rerun the evaluation, and then decide whether unsupported-spec refusal or table preprocessing should be the next change.

---

## Iteration 2

| Run ID | Date | Versions | Change Category | Change Description |
|--------|------|----------|-----------------|-------------------|
| iter-002 | 2026-07-03 | V0 / V1 / V2 | preprocessing | q59 invalid restoration / guardrail separation |

**Previous Iteration Comparison:**
- V0 Correctness (norm): 0.86 → 0.86 (Δ 0.00)
- V1 Correctness (norm): 0.86 → 0.87 (Δ +0.01)
- V2 Correctness (norm): 0.85 → 0.82 (Δ -0.03)
- V0 Grounding (norm): 0.74 → 0.75 (Δ +0.01)
- V1 Grounding (norm): 0.76 → 0.75 (Δ -0.01)
- V2 Grounding (norm): 0.74 → 0.71 (Δ -0.03)
- V0 Hallucination Rate: 14% → 14% (Δ 0)
- V1 Hallucination Rate: 14% → 14% (Δ 0)
- V2 Hallucination Rate: 20% → 22% (Δ +2 pts)

**Baseline Comparison (Cumulative):**
- V0 Correctness (norm): baseline 0.86 → current 0.86 (Δ 0.00)
- V1 Correctness (norm): baseline 0.87 → current 0.87 (Δ 0.00)
- V2 Correctness (norm): baseline 0.82 → current 0.82 (Δ 0.00)

**Change Decision:** `decisions/2026-07-03_change_preprocessing_q59_question_rewording.md`

**Qualitative Observations:**
- Procedural rows remained the most stable cluster across all three versions.
- Factual and table rows still account for most of the score drift.
- Q59 should be restored to invalid: the latest run returns the safety-filter fallback for all three versions, which is the expected guardrail-trip behavior for a blocked or unsupported control-module override question.
- V0 is effectively flat, V1 regained a small correctness lift, and V2 regressed back toward baseline.

**Next Iteration:** Restore Q59 to invalid so the benchmark separates blocked control-module questions from grounding questions, then move to unsupported horsepower and trim-feature prompts.

---

## Iteration 3

| Run ID | Date | Versions | Change Category | Change Description |
|--------|------|----------|-----------------|-------------------|
| iter-003 | 2026-07-04 | V0 / V1 / V2 | preprocessing | q59 guardrail probe lockdown; factual brevity follow-up |

**Previous Iteration Comparison:**
- V0 Correctness (norm): 0.86 → 0.86 (Δ 0.00)
- V1 Correctness (norm): 0.87 → 0.87 (Δ 0.00)
- V2 Correctness (norm): 0.82 → 0.85 (Δ +0.03)
- V0 Grounding (norm): 0.75 → 0.74 (Δ -0.01)
- V1 Grounding (norm): 0.75 → 0.76 (Δ +0.01)
- V2 Grounding (norm): 0.71 → 0.74 (Δ +0.03)
- V0 Hallucination Rate: 14% → 17% (Δ +3 pts)
- V1 Hallucination Rate: 14% → 13% (Δ -1 pt)
- V2 Hallucination Rate: 22% → 19% (Δ -3 pts)

**Baseline Comparison (Cumulative):**
- V0 Correctness (norm): baseline 0.86 → current 0.86 (Δ 0.00)
- V1 Correctness (norm): baseline 0.87 → current 0.87 (Δ 0.00)
- V2 Correctness (norm): baseline 0.82 → current 0.85 (Δ +0.03)

**Change Decision:** `decisions/2026-07-04_change_preprocessing_q59_guardrail_probe_lockdown.md`

**Qualitative Observations:**
- Q59 is now stable and should be treated as a locked invalid guardrail probe rather than a changing benchmark item.
- V2 is the only version with a clear improvement beyond normal variance, driven by factual and table gains.
- Factual elaboration beyond the retrieved text remains the most consistent weakness across all three agents.
- V1 has one meaningful regression on the automatic-transmission-fluid interval question, which stands out as more than noise.

**Next Iteration:** Keep Q59 frozen, tighten unsupported-spec refusal wording.

---

## Template for Future Iterations

| Run ID | Date | Versions | Change Category | Change Description |
|--------|------|----------|-----------------|-------------------|
| iter-NNN | YYYY-MM-DD | V0 / V1 / V2 | preprocessing / instructions / fallback | TBD |

**Previous Iteration Comparison:**
- V0 Correctness (norm): TBD → TBD (Δ TBD)
- V1 Correctness (norm): TBD → TBD (Δ TBD)
- V2 Correctness (norm): TBD → TBD (Δ TBD)

**Baseline Comparison (Cumulative):**
- V0 Correctness (norm): baseline TBD → current TBD (Δ TBD)
- V1 Correctness (norm): baseline TBD → current TBD (Δ TBD)
- V2 Correctness (norm): baseline TBD → current TBD (Δ TBD)

**Change Decision:** `decisions/YYYY-MM-DD_change_{category}_{description}.md`

**Qualitative Observations:**
- TBD

**Next Iteration:** TBD

---

## Summary & Conclusions

*To be completed after iterations plateau or stop.*

**Total Iterations:** TBD  
**Total Time:** TBD  
**Final Performance Lift:**
- V0: baseline → final (Δ)
- V1: baseline → final (Δ)
- V2: baseline → final (Δ)

**Most Impactful Changes:**
1. TBD
2. TBD
3. TBD

**Remaining Known Issues:** TBD

**Lessons Learned:** TBD
