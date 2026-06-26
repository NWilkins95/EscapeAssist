# Baseline Run Analysis

- Run ID: baseline-001
- Date: YYYY-MM-DD
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: None (frozen baseline)

---

## Executive Summary

[One paragraph summarizing the baseline performance across all three versions. Highlight which version performs best, which struggles most, and what the primary failure categories are.]

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|-----|
| Correctness (raw avg) | TBD | TBD | TBD |
| Correctness (normalized) | TBD | TBD | TBD |
| Grounding (raw avg) | TBD | TBD | TBD |
| Grounding (normalized) | TBD | TBD | TBD |
| Hallucination True Rate | TBD | TBD | TBD |

### Key Observations

**Strongest Version:** [V0 / V1 / V2] at TBD normalized correctness

**Weakest Version:** [V0 / V1 / V2] at TBD normalized correctness

**Hallucination Leader:** [V0 / V1 / V2] with TBD hallucination rate

**Grounding Leader:** [V0 / V1 / V2] at TBD normalized grounding

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Best Version | Notes |
|---------------|-------|-------|-------|-------|-------|-------|
| factual | TBD | TBD | TBD | TBD | TBD | TBD |
| procedural | TBD | TBD | TBD | TBD | TBD | TBD |
| table | TBD | TBD | TBD | TBD | TBD | TBD |

### Category Insights

**Factual Questions:**
- [Which version is strongest and why?]
- [Common failure patterns?]

**Procedural Questions:**
- [Which version is strongest and why?]
- [Common failure patterns?]

**Table Questions:**
- [Which version is strongest and why?]
- [Common failure patterns?]

---

## Failure Analysis

### Top Failure Categories

Ranked by frequency (total failures across all versions):

1. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: [What does this failure look like?]
   - Affected Versions: V0 / V1 / V2
   - Root Cause: [Is it preprocessing, instruction-related, or retrieval?]
   - Suggested Fix: TBD

2. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: TBD
   - Affected Versions: V0 / V1 / V2
   - Root Cause: TBD
   - Suggested Fix: TBD

3. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: TBD
   - Affected Versions: V0 / V1 / V2
   - Root Cause: TBD
   - Suggested Fix: TBD

### Per-Version Failure Summary

**V0 (OpenAI Auto-Ingestion):**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD
- Unique weaknesses (not shared with V1/V2): TBD

**V1 (Pure Docling):**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD
- Unique weaknesses (not shared with V0/V2): TBD

**V2 (Docling + Cleanup):**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD
- Unique weaknesses (not shared with V0/V1): TBD

---

## Question-Level Details

### Top Performers

Questions with perfect or near-perfect scores across all versions (these are the "easy" baseline):

| Q# | Question | V0 | V1 | V2 | Reason These Work |
|----|----------|----|----|-----|-------|
| TBD | TBD | 5/5 | 5/5 | 5/5 | [Straightforward factual, clear grounding, etc.] |
| TBD | TBD | 5/5 | 5/5 | 5/5 | TBD |
| TBD | TBD | 5/5 | 5/5 | 5/5 | TBD |

### Consistent Failures

Questions that all three versions struggle with equally (likely source data or conceptual difficulty):

| Q# | Question | V0 | V1 | V2 | Likely Cause |
|----|----------|----|----|-----|-------|
| TBD | TBD | 1/5 | 1/5 | 1/5 | [Missing source / Ambiguous / Hallucination trap] |
| TBD | TBD | 2/5 | 2/5 | 2/5 | TBD |

### Version Differences

Questions where one version significantly outperforms the others (these highlight preprocessing or instruction effects):

| Q# | Question | V0 | V1 | V2 | Winner | Why This Version Won |
|----|----------|----|----|-----|--------|--------|
| TBD | TBD | 2/5 | 5/5 | 3/5 | V1 | [Docling extraction was cleaner / V0 missing context / V2 cleanup broke something] |
| TBD | TBD | 4/5 | 2/5 | 5/5 | V2 | [Cleanup script fixed missing or garbled section] |
| TBD | TBD | 5/5 | 3/5 | 3/5 | V0 | [Raw output was better; preprocessing introduced errors] |

---

## Hallucination Analysis

### Hallucination Instances by Type

| Q# | Question | Version | Hallucination | Truth | Category | Likely Cause |
|----|----------|---------|---------------|-------|----------|-------|
| TBD | TBD | V0 | [Made-up metric] | [Actual metric] | Metric/Confidence | Model confidence without source text |
| TBD | TBD | V1 | TBD | TBD | Feature/Instruction | Model added feature not in manual |
| TBD | TBD | V2 | TBD | TBD | TBD | TBD |

### Hallucination Patterns

**Most Common Type:** [Metric / Feature / Instruction / Confidence]

**Affected Versions:** [Which versions hallucinate most?]

**Trigger Pattern:** [What question types or topics trigger hallucinations?]

---

## Grounding Analysis

### Questions Scoring Low on Grounding (despite correct answers)

| Q# | Question | Version | Score | Grounding Issue | Root Cause |
|----|----------|---------|-------|-----------------|-------|
| TBD | TBD | V0 | 4/5 | Answer correct but pulled from multiple sources without clear attribution | [Retrieval / Formatting / Instruction] |
| TBD | TBD | V1 | TBD | TBD | TBD |

### Grounding Patterns

**Strongest Grounding:** [Which version grounds best and why?]

**Weakest Grounding:** [Which version struggles most?]

**Common Grounding Flaw:** TBD

---

## Preprocessing Impact Analysis

### V0 vs V1 (Raw vs Pure Docling)

**Questions V1 Wins on:** TBD count

**Reasons V1 Wins:** [Better extraction, cleaner structure, etc.]

**Questions V0 Wins on:** TBD count

**Reasons V0 Wins:** [Raw output was better, Docling lost context, etc.]

### V1 vs V2 (Pure Docling vs Docling + Cleanup)

**Questions V2 Wins on:** TBD count

**Reasons V2 Wins:** [Cleanup fixed garbled text, added missing sections, etc.]

**Questions V1 Wins on:** TBD count

**Reasons V1 Wins:** [Cleanup broke something, over-normalized, etc.]

---

## Observations & Qualitative Notes

**What Worked Well (across all versions):**
- TBD
- TBD

**What Consistently Failed (across all versions):**
- TBD
- TBD

**Edge Cases Discovered:**
- TBD
- TBD

**Unexpected Patterns:**
- [Any surprising performance shifts?]
- [Any version behaved counter to expectations?]

---

## Preprocessing Health Check

### V0 (OpenAI Auto-Ingestion)

- Document extraction rate: TBD%
- Parsing errors: TBD count
- Formatting issues: TBD (list)
- Missing sections: TBD (list)

### V1 (Pure Docling)

- Docling extraction success: TBD%
- Markdown quality: TBD (good / acceptable / noisy)
- Section preservation: TBD%
- Table extraction: TBD (working / inconsistent / missing)

### V2 (Docling + Cleanup)

- Cleanup script effectiveness: TBD%
- Issues introduced by cleanup: TBD (list)
- Sections fixed: TBD (list)
- Net improvement: TBD

---

## Recommendations for Iteration 1

### Priority 1: [Top Failure Category]

**Change Type:** preprocessing / instructions / fallback

**Specific Action:** [Describe the exact change to make]

**Why:** This category accounts for TBD% of all failures and affects TBD question types.

**Expected Impact:** Estimated to improve correctness by TBD across TBD version(s).

### Priority 2: [Second Failure Category]

**Change Type:** preprocessing / instructions / fallback

**Specific Action:** TBD

**Why:** TBD

**Expected Impact:** Estimated to improve correctness by TBD

### Priority 3: [Third Failure Category]

**Change Type:** preprocessing / instructions / fallback

**Specific Action:** TBD

**Why:** TBD

**Expected Impact:** Estimated to improve correctness by TBD

---

## Key Metrics Summary Table

Quick reference for future comparisons:

| Metric | V0 | V1 | V2 | Best | Gap (Best to Worst) |
|--------|----|----|-----|------|--------|
| Correctness (norm) | TBD | TBD | TBD | TBD | TBD |
| Grounding (norm) | TBD | TBD | TBD | TBD | TBD |
| Hallucination Rate | TBD | TBD | TBD | TBD | TBD |

---

## Artifacts & References

- **Evaluation Dashboard:** Available at `src/user_interface/pages/evaluation_dashboard.py`
- **Raw Exports:** 
  - Answers: `evaluation/outputs/answers/{V0,V1,V2}/`
  - Evaluations: `evaluation/outputs/evaluations/{V0,V1,V2}/`
  - Judge Calibration: `evaluation/outputs/judge_calibration/`
- **Golden Dataset:** `evaluation/data/golden.jsonl` (69 questions)
- **Judge Prompt:** `evaluation/judge/judge_instructions.py`
- **Agent Instructions:** `src/user_interface/workflows/{V0,V1,V2}workflow.py`
- **Preprocessing Code:**
  - V0: [Link to OpenAI autoingestion code]
  - V1: [Link to Docling extraction code]
  - V2: [Link to Docling + cleanup code]

---

## Appendix: Full Question-by-Question Baseline Scores

[Optional: Include full table with all 69 questions and their scores, or reference exported CSV.]

| Q# | Question | Type | V0 Corr | V0 Ground | V0 Halluc | V1 Corr | V1 Ground | V1 Halluc | V2 Corr | V2 Ground | V2 Halluc |
|----|----------|------|---------|-----------|-----------|---------|-----------|-----------|---------|-----------|-----------|
| 1 | TBD | factual | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 2 | TBD | procedural | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
