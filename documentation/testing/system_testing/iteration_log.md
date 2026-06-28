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
| iter-001 | YYYY-MM-DD | V0 / V1 / V2 | preprocessing / instructions / fallback | TBD |

**Baseline Comparison:**
- V0 Correctness (norm): TBD → TBD (Δ TBD)
- V1 Correctness (norm): TBD → TBD (Δ TBD)
- V2 Correctness (norm): TBD → TBD (Δ TBD)

**Change Decision:** `decisions/YYYY-MM-DD_change_{category}_{description}.md`

**Qualitative Observations:**
- TBD

**Next Iteration:** TBD

---

## Iteration 2

| Run ID | Date | Versions | Change Category | Change Description |
|--------|------|----------|-----------------|-------------------|
| iter-002 | YYYY-MM-DD | V0 / V1 / V2 | preprocessing / instructions / fallback | TBD |

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
