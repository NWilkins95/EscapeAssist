# Run Report – [Run ID] – [Date]

- Run ID: 
- Date: YYYY-MM-DD
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: [Brief description, or "Baseline"]

---

## Executive Summary

[One paragraph summarizing the overall results and any notable patterns or regressions.]

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

### Comparison to Previous Run

| Metric | V0 Δ | V1 Δ | V2 Δ |
|--------|------|------|------|
| Correctness (normalized) | TBD | TBD | TBD |
| Grounding (normalized) | TBD | TBD | TBD |
| Hallucination True Rate | TBD | TBD | TBD |

### Comparison to Baseline

| Metric | V0 Δ | V1 Δ | V2 Δ |
|--------|------|------|------|
| Correctness (normalized) | TBD | TBD | TBD |
| Grounding (normalized) | TBD | TBD | TBD |
| Hallucination True Rate | TBD | TBD | TBD |

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Notes |
|---------------|-------|-------|-------|-------|-------|
| factual | TBD | TBD | TBD | TBD | TBD |
| procedural | TBD | TBD | TBD | TBD | TBD |
| table | TBD | TBD | TBD | TBD | TBD |

---

## Failure Analysis

### Top Failure Categories

Ranked by frequency (total failures across all versions):

1. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: TBD
   - Affected Versions: V0 / V1 / V2
   - Suggested Fix: TBD

2. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: TBD
   - Affected Versions: V0 / V1 / V2
   - Suggested Fix: TBD

3. **[Category Name]** (TBD failures, TBD% of total)
   - Examples: Q#, Q#, Q#
   - Description: TBD
   - Affected Versions: V0 / V1 / V2
   - Suggested Fix: TBD

### Per-Version Failure Summary

**V0:**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD

**V1:**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD

**V2:**
- Total failures: TBD
- Most common failure type: TBD
- Notable strong points: TBD

---

## Question-Level Details

### Top Performers

Questions with perfect or near-perfect scores across all versions:

| Q# | Question | V0 | V1 | V2 | Notes |
|----|----------|----|----|-----|-------|
| TBD | TBD | 5/5 | 5/5 | 5/5 | Straightforward, well-grounded |
| TBD | TBD | 5/5 | 5/5 | 5/5 | TBD |

### Consistent Failures

Questions that all three versions struggle with:

| Q# | Question | V0 | V1 | V2 | Likely Cause |
|----|----------|----|----|-----|-------|
| TBD | TBD | 1/5 | 1/5 | 1/5 | [Hallucination / Refusal / Missing source / Grounding drift] |
| TBD | TBD | 2/5 | 2/5 | 2/5 | TBD |

### Version Differences

Questions where one version significantly outperforms others:

| Q# | Question | V0 | V1 | V2 | Winner | Reason |
|----|----------|----|----|-----|--------|--------|
| TBD | TBD | 2/5 | 5/5 | 3/5 | V1 | Docling handled this better; V0 missing context |
| TBD | TBD | 4/5 | 2/5 | 5/5 | V2 | Cleanup script fixed missing section |

---

## Hallucination Instances

List specific hallucinations observed:

| Q# | Question | Version | Hallucination | Truth | Category |
|----|----------|---------|---------------|-------|----------|
| TBD | TBD | V0 | TBD | TBD | [Confidence / Metric / Feature / Instruction] |
| TBD | TBD | V1 | TBD | TBD | TBD |

---

## Grounding Issues

Questions with correct answers that still scored low on grounding:

| Q# | Question | Version | Score | Grounding Notes |
|----|----------|---------|-------|-----------------|
| TBD | TBD | V0 | 4/5 | Answer is correct but pulled from multiple sources without clear attribution |
| TBD | TBD | V1 | TBD | TBD |

---

## Observations & Qualitative Notes

**What Worked Well:**
- TBD
- TBD

**What Regressed:**
- TBD
- TBD

**Edge Cases Discovered:**
- TBD
- TBD

**Unexpected Patterns:**
- TBD

---

## Recommendations for Next Iteration

**Priority 1 (Top failure category):**
- Change Type: preprocessing / instructions / fallback
- Specific Action: TBD
- Rationale: This affects TBD% of failures

**Priority 2 (Second failure category):**
- Change Type: preprocessing / instructions / fallback
- Specific Action: TBD
- Rationale: TBD

**Priority 3 (Third failure category):**
- Change Type: preprocessing / instructions / fallback
- Specific Action: TBD
- Rationale: TBD

---

## Artifacts

- **Baseline Comparison:** [Link to comparison if applicable]
- **Decision Document:** [Link to decision made for this run, if applicable]
- **Raw Exports:** Available in `evaluation/outputs/answers/` and `evaluation/outputs/evaluations/`
- **Judge Disagreements:** Checked against `evaluation/outputs/judge_calibration/` logs

---

## Appendix: Full Question-by-Question Scores

| Q# | Question | V0 Correctness | V0 Grounding | V0 Hallucination | V1 Correctness | V1 Grounding | V1 Hallucination | V2 Correctness | V2 Grounding | V2 Hallucination |
|----|----------|----------------|--------------|------------------|----------------|--------------|------------------|----------------|--------------|------------------|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
