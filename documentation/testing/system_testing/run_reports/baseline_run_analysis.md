# Baseline Run Analysis

- Run ID: baseline-001
- Date: 2026-06-17 to 2026-06-19
- Versions: V0, V1, V2
- Questions Evaluated: 69
- Change(s) in This Run: None (frozen baseline)

---

## Executive Summary

This baseline is fairly strong overall, but the three versions separate cleanly once the questions move away from straightforward procedural guidance. V1 is the best performer on normalized correctness, V0 and V1 tie for the best grounding, and V2 regresses on both correctness and hallucination rate. The most reliable questions are procedural, while the biggest losses are concentrated in factual explanation questions and in invalid or out-of-scope prompts that tend to elicit unsupported guesses about trim features, specifications, or vehicle capabilities.

---

## Overall Metrics

### By Version

| Metric | V0 | V1 | V2 |
|--------|----|----|-----|
| Correctness (raw avg) | 4.3 | 4.3 | 4.1 |
| Correctness (normalized) | 0.86 | 0.87 | 0.82 |
| Grounding (raw avg) | 3.8 | 3.8 | 3.6 |
| Grounding (normalized) | 0.75 | 0.75 | 0.71 |
| Hallucination True Rate | 13% | 13% | 22% |

### Key Observations

**Strongest Version:** V1 at 0.87 normalized correctness

**Weakest Version:** V2 at 0.82 normalized correctness

**Hallucination Leader:** V2 with a 22% hallucination rate

**Grounding Leader:** V0 and V1 tie at 0.75 normalized grounding

---

## Breakdown by Question Type

| Question Type | Count | V0 Correctness (norm) | V1 Correctness (norm) | V2 Correctness (norm) | Best Version | Notes |
|---------------|-------|-----------------------|-----------------------|-----------------------|--------------|-------|
| factual | 23 | 0.800 | 0.852 | 0.783 | V1 | Weakest cluster overall; warning-light and definition questions lose grounding first. |
| procedural | 10 | 1.000 | 1.000 | 0.980 | V0/V1 tie | The most stable category; V2 only slips on a small number of answers. |
| table | 21 | 0.914 | 0.905 | 0.857 | V1 | Best category for finding preprocessing effects; V0 is slightly more grounded, but V1 wins on correctness. |
| invalid | 15 | 0.760 | 0.760 | 0.707 | V0/V1 tie | The main hallucination driver; V2 is clearly worse here. |

### Category Insights

**Factual Questions:**
- V1 is strongest overall, but the category still contains several grounding misses on explanation-style prompts such as warning lights, passive anti-theft, and oil-life logic.
- The common failure mode is adding a safe but unsupported detail that is not present in the source quote.

**Procedural Questions:**
- These are the clearest wins in the baseline. V0 and V1 are essentially perfect, and V2 only loses a little on a handful of steps.
- Failures here are rare and are usually small grounding deductions rather than full correctness misses.

**Table Questions:**
- V1 generally wins on correctness, but V0 sometimes grounds slightly better on spec-heavy entries.
- This category shows the clearest preprocessing sensitivity, especially on oil capacity, towing, and maintenance-interval tables.

---

## Failure Analysis

### Top Failure Categories

Ranked by frequency across the three runs:

1. **Unsupported or hallucinated answers to invalid / out-of-scope prompts** (9 hallucinated records in V0 and V1, 15 in V2)
   - Examples: Q58, Q61, Q64, Q67, Q68, Q69
   - Description: The model invents trim availability, horsepower, firmware, tire, or infotainment details when the question is outside the manual’s supported scope.
   - Affected Versions: V2 most strongly; V0 and V1 are tied on hallucination rate, but both still show the same pattern on the difficult invalid questions.
   - Root Cause: The results are consistent with an instruction and retrieval boundary issue. The system likely needs a firmer refusal path for unsupported specs and capabilities.
   - Suggested Fix: Add stronger refusal grounding for unsupported feature/spec questions and make the answer policy explicit for trim/capability lookups.

2. **Maintenance and specification table extraction / comparison errors** (about 6 to 8 recurring question families)
   - Examples: Q16, Q18, Q41, Q47, Q51
   - Description: Multi-value comparison questions about engine oil, transmission fluid, charging indicators, or towing rules are where small extraction errors turn into score drops.
   - Affected Versions: V2 regresses the most; V0 and V1 trade the lead depending on the specific table.
   - Root Cause: The results are consistent with preprocessing and formatting effects. Cleanup may help some rows but hurt others when table structure or labels are flattened too aggressively.
   - Suggested Fix: Preserve table structure more faithfully and avoid cleanup passes that collapse row/column relationships.

3. **Factual explanation questions with narrow source support** (about 4 recurring question families)
   - Examples: Q26, Q32, Q36, Q49
   - Description: Definition-style questions about warning lights or vehicle systems tend to get the right general idea but lose grounding because the answer adds extra detail.
   - Affected Versions: All three versions, with V2 weakest overall and V0/V1 mostly tied.
   - Root Cause: The results suggest a grounding / instruction balance issue. The model likely knows the general automotive concept but does not always stay tightly inside the quoted source.
   - Suggested Fix: Tighten the response policy for explanation questions and bias toward quote-bound phrasing when the source is narrow.

### Per-Version Failure Summary

**V0 (OpenAI Auto-Ingestion):**
- Total failures: 6 low-low records where both correctness and grounding are at 2 or below
- Most common failure type: factual grounding misses, followed by a small number of invalid-question hallucinations
- Notable strong points: procedural questions and most straightforward table lookups
- Unique weaknesses: slightly weaker grounding than V1 on some spec-heavy questions

**V1 (Pure Docling):**
- Total failures: 6 low-low records where both correctness and grounding are at 2 or below
- Most common failure type: factual grounding misses and a few table-comparison weaknesses
- Notable strong points: best overall correctness, strong procedural performance, and the best factual category score
- Unique weaknesses: does not always improve grounding over V0 on table rows, even when correctness improves, which suggests the preprocessing change is not uniformly beneficial

**V2 (Docling + Cleanup):**
- Total failures: 10 low-low records where both correctness and grounding are at 2 or below
- Most common failure type: hallucinated invalid answers and regressions on maintenance/specification tables
- Notable strong points: still very good on procedural prompts
- Unique weaknesses: the cleanup pass is associated with weaker performance on some key table answers, which is consistent with over-normalization or other formatting loss

---

## Question-Level Details

### Top Performers

Questions that are perfect or near-perfect across all versions:

| Q# | Question | V0 | V1 | V2 | Reason These Work |
|----|----------|----|----|-----|-------------------|
| 4 | Is it dangerous to ride in a cargo area of the vehicle? | 5/5 | 5/5 | 5/5 | Direct factual safety guidance with a very clean source match. |
| 10 | Under what conditions does the gasoline engine run in a hybrid vehicle, and why? | 5/5 | 5/5 | 5/5 | A stable factual explanation that is tightly supported by the manual. |
| 19 | How do you open the hood? | 5/5 | 5/5 | 5/5 | Short procedural sequence with little ambiguity. |

### Consistent Failures

There are no exact all-three low-score failures in this baseline, but the recurring weak cluster is the same across versions: narrow explanation questions with partial source support.

| Q# | Question | V0 | V1 | V2 | Likely Cause |
|----|----------|----|----|-----|--------------|
| 26 | What is the passive anti-theft system? | 5/3 | 4/3 | 2/2 | Definition-style answer that stays too generic or too assertive. |
| 36 | What does the oil pressure warning light indicate? | 3/3 | 5/3 | 4/3 | Correct core idea, but grounding stays low because the answer adds unsupported detail. |

### Version Differences

Questions where preprocessing or cleanup makes a clear difference:

| Q# | Question | V0 | V1 | V2 | Winner | Why This Version Won |
|----|----------|----|----|-----|--------|----------------------|
| 16 | What is the engine oil capacity and recommended oil specification for the 2.0L EcoBoost engine? | 5/4 | 5/5 | 2/2 | V1 | Docling preserved the relevant spec row cleanly; V2 regressed badly after cleanup. |
| 18 | What are the differences in oil capacity and specifications among the 1.5L EcoBoost, 2.0L EcoBoost, and 2.5L hybrid engines? | 4/3 | 5/4 | 2/2 | V1 | V1 keeps the comparison structure intact better than the other two versions. |
| 51 | How does the automatic transmission fluid change interval differ across normal, towing, and severe operating conditions? | 5/5 | 1/2 | 5/4 | V0 / V2 | V1 is the clear loser here; V0 and V2 retain the table semantics better. |
| 55 | What is the maximum towing capacity of the 2022 Ford Escape in kilograms? | 5/5 | 5/5 | 0/0 | V0 / V1 | V2 drops this answer entirely, which is the clearest cleanup regression in the run. |

---

## Hallucination Analysis

### Hallucination Instances by Type

The hallucinations are concentrated in invalid/out-of-scope prompts. The repeated pattern is the model fabricating trim-specific features, exact capacities, or hardware details that are not actually supported by the source material.

| Q# | Question | Version | Hallucination | Truth | Category | Likely Cause |
|----|----------|---------|---------------|-------|----------|--------------|
| 58 | What is the exact horsepower output for each engine variant? | V0 | Yes | No exact horsepower table is present in the source set | Spec / capability | Unsupported spec lookup answered from priors. |
| 61 | How do you manually upgrade the vehicle's firmware? | V0 | Yes | No manual firmware-upgrade procedure is provided | Feature / instruction | The model answers a nonexistent maintenance workflow. |
| 64 | Can I use snow chains on the Escape Active model? | V0 | Yes | No support for this exact claim in the evaluated source set | Feature / safety | The model overextends from general vehicle knowledge. |
| 67 | Does the Escape Platinum AWD support winter tire and snow chain installation like other trims? | V0 | Yes | No exact cross-trim support is grounded in the source set | Feature / trim comparison | Cross-trim speculation without source backing. |

### Hallucination Patterns

**Most Common Type:** Feature / specification hallucination on invalid questions

**Affected Versions:** V2 is the weakest, but the pattern exists in all three runs

**Trigger Pattern:** Questions about unsupported trim features, exact numeric specs, or maintenance tasks that are not present in the manual

---

## Grounding Analysis

### Questions Scoring Low on Grounding (despite correct answers)

| Q# | Question | Version | Score (Correctness / Grounding) | Grounding Issue | Root Cause |
|----|----------|---------|----------------------------------|-----------------|------------|
| 1 | How do you install a child restraint using seatbelts? | V0 | 5 / 4 | The answer is correct, but it adds extra safety language not quoted directly. | Instruction / formatting |
| 14 | What is the engine oil capacity and recommended oil specification for the 1.5L EcoBoost engine? | V0 | 5 / 4 | Correct answer, but the cited support is not perfectly tight. | Retrieval / table formatting |
| 41 | What do the different convenience cord LED indicator combinations mean and what actions should be taken when charging a plug-in hybrid vehicle? | V1 | 5 / 4 | Correct answer with a small grounding penalty from extra interpretation. | Retrieval / formatting |
| 49 | How does the Intelligent Oil-Life Monitor determine when an oil change is needed? | V1 | 3 / 2 | The model is directionally right but not tightly grounded to the exact source phrasing. | Source coverage |

### Grounding Patterns

**Strongest Grounding:** V0 and V1 tie overall, with V0 sometimes preserving table context slightly better and V1 often improving correctness first

**Weakest Grounding:** V2, based on this run’s grounding scores

**Common Grounding Flaw:** The answer is often correct, but it may add safe extra detail that was not explicitly supported by the source quote

---

## Preprocessing Impact Analysis

### V0 vs V1 (Raw vs Pure Docling)

**Questions V1 Wins on:** 14

**Reasons V1 Wins:** Cleaner extraction and better document structure are consistent with improved factual and table-heavy question performance, especially on spec comparisons and explanation prompts.

**Questions V0 Wins on:** 6

**Reasons V0 Wins:** Raw ingestion occasionally preserves table context or phrasing better, so V0 can still outperform V1 on some table-grounding cases.

### V1 vs V2 (Pure Docling vs Docling + Cleanup)

**Questions V2 Wins on:** 9

**Reasons V2 Wins:** Cleanup can help when it restores a missing or cluttered section and the original extraction was noisy.

**Questions V1 Wins on:** 20

**Reasons V1 Wins:** The cleanup pass sometimes appears to over-normalize the source and damage table semantics, which is consistent with worse oil/spec and towing results.

---

## Observations & Qualitative Notes

**What Worked Well (across all versions):**
- Procedural directions with short step sequences
- Direct factual safety questions with clear source support

**What Consistently Failed (across all versions):**
- Unsupported trim/spec questions that are prone to hallucination
- Table comparisons that require retaining multiple values and labels at once

**Edge Cases Discovered:**
- Exact numeric questions such as towing capacity and oil capacity are highly sensitive to preprocessing quality
- Cross-trim feature questions are a recurring hallucination trigger

**Unexpected Patterns:**
- V0 occasionally grounds table answers slightly better than V1, even though V1 wins on overall correctness
- V2 is not uniformly worse, but it is more brittle on the maintenance/specification subset in this run

---

## Preprocessing Health Check

### V0 (OpenAI Auto-Ingestion)

- Document extraction rate: 100% of the 69 questions are represented in the baseline outputs
- Parsing errors: 0 observed in the exported runs
- Formatting issues: Slight grounding loss on some spec-heavy table rows
- Missing sections: None visible from the exported evaluation set

### V1 (Pure Docling)

- Docling extraction success: 100% of the 69 questions are represented in the baseline outputs
- Markdown quality: acceptable to good
- Section preservation: strong overall
- Table extraction: working, with a few grounding-sensitive rows still losing detail

### V2 (Docling + Cleanup)

- Cleanup script effectiveness: mixed; it improves some rows but is associated with lower overall correctness and grounding
- Issues introduced by cleanup: Table semantics appear to be flattened or partially lost on several maintenance questions
- Sections fixed: Some noisy rows are cleaner, but the overall score trend is worse than V1
- Net improvement: negative versus V1 on both correctness and hallucination rate in this run

---

## Recommendations for Iteration 1

### Priority 1: Unsupported spec / capability refusal handling

**Change Type:** instructions / fallback

**Specific Action:** Add a more explicit refusal rule for trim features, capacities, firmware, and other unsupported spec questions when the source does not contain a direct answer.

**Why:** This is the largest hallucination driver in the observed results and affects the invalid question set most heavily.

**Expected Impact:** Lower hallucination rate and fewer zero-score invalid answers across all versions, especially V2.

### Priority 2: Preserve table structure through preprocessing

**Change Type:** preprocessing

**Specific Action:** Reduce cleanup aggressiveness on spec and maintenance tables so rows, labels, and units stay attached to the correct values.

**Why:** The biggest version deltas in this run show up on oil capacity, towing, and maintenance interval comparisons.

**Expected Impact:** Better grounding and fewer incorrect table-comparison answers.

### Priority 3: Tighten source-bound phrasing for factual explanations

**Change Type:** instructions

**Specific Action:** Bias the model toward quoting or paraphrasing the source closely for warning-light and subsystem explanation questions.

**Why:** Several factual prompts are already broadly correct but lose points because they drift beyond the exact source support.

**Expected Impact:** Small but consistent improvement in grounding scores.

---

## Key Metrics Summary Table

Quick reference for future comparisons:

| Metric | V0 | V1 | V2 | Best | Gap (Best to Worst) |
|--------|----|----|-----|------|---------------------|
| Correctness (norm) | 0.86 | 0.87 | 0.82 | V1 | 0.05 |
| Grounding (norm) | 0.75 | 0.75 | 0.71 | V0 / V1 | 0.04 |
| Hallucination Rate | 13% | 13% | 22% | V0 / V1 | 9 pts |

---

## Artifacts & References

- **Evaluation Dashboard:** Available at `src/user_interface/pages/evaluation_dashboard.py`
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

---

## Appendix: Representative Question-by-Question Baseline Scores

The full 69-question export is available in the raw JSONL files above. The rows below capture the most useful examples for later comparisons.

| Q# | Question | Type | V0 Corr | V0 Ground | V0 Halluc | V1 Corr | V1 Ground | V1 Halluc | V2 Corr | V2 Ground | V2 Halluc |
|----|----------|------|---------|-----------|-----------|---------|-----------|-----------|---------|-----------|-----------|
| 4 | Is it dangerous to ride in a cargo area of the vehicle? | factual | 5 | 5 | False | 5 | 5 | False | 5 | 5 | False |
| 10 | Under what conditions does the gasoline engine run in a hybrid vehicle, and why? | factual | 5 | 5 | False | 5 | 5 | False | 5 | 5 | False |
| 16 | What is the engine oil capacity and recommended oil specification for the 2.0L EcoBoost engine? | table | 5 | 4 | False | 5 | 5 | False | 2 | 2 | True |
| 18 | What are the differences in oil capacity and specifications among the 1.5L EcoBoost, 2.0L EcoBoost, and 2.5L hybrid engines? | table | 4 | 3 | False | 5 | 4 | False | 2 | 2 | True |
| 19 | How do you open the hood? | procedural | 5 | 5 | False | 5 | 5 | False | 5 | 5 | False |
| 26 | What is the passive anti-theft system? | factual | 5 | 3 | False | 4 | 3 | False | 2 | 2 | True |
| 36 | What does the oil pressure warning light indicate? | factual | 3 | 3 | False | 5 | 3 | False | 4 | 3 | False |
| 41 | What do the different convenience cord LED indicator combinations mean and what actions should be taken when charging a plug-in hybrid vehicle? | table | 4 | 3 | False | 5 | 4 | False | 5 | 5 | False |
| 47 | What are the differences in recreational towing requirements for gasoline AWD, gasoline FWD, and hybrid vehicles? | table | 5 | 5 | False | 5 | 5 | False | 3 | 3 | True |
| 51 | How does the automatic transmission fluid change interval differ across normal, towing, and severe operating conditions? | table | 5 | 5 | False | 1 | 2 | True | 5 | 4 | False |
| 55 | What is the maximum towing capacity of the 2022 Ford Escape in kilograms? | invalid | 5 | 5 | False | 5 | 5 | False | 0 | 0 | True |
| 58 | What is the exact horsepower output for each engine variant? | invalid | 0 | 0 | True | 0 | 0 | True | 0 | 0 | True |
| 61 | How do you manually upgrade the vehicle's firmware? | invalid | 0 | 0 | True | 0 | 0 | True | 0 | 0 | True |
| 64 | Can I use snow chains on the Escape Active model? | invalid | 1 | 0 | True | 1 | 0 | True | 1 | 0 | True |
| 67 | Does the Escape Platinum AWD support winter tire and snow chain installation like other trims? | invalid | 1 | 0 | True | 1 | 0 | True | 1 | 0 | True |
