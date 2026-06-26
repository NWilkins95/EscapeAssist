# Full System Testing Plan

- Date: June 26, 2026
- Owner: Nicholas Wilkins

## 1. Purpose

This document outlines the plan for end-to-end system testing and iterative improvement of the EscapeAssist pipeline across V0, V1, and V2 versions.

The goal is to:
- Establish a baseline evaluation across all three preprocessing and agent versions
- Identify failure patterns systematically
- Test targeted improvements one change at a time
- Document which changes improve, regress, or have no effect
- Build a clear history of what changed and why

This is distinct from instruction testing (which designed the initial instructions) and judge testing (which calibrated the judge). This plan covers the full system end-to-end.

---

## 2. Versions Under Test

Three versions of EscapeAssist will be evaluated:

- **V0**: OpenAI auto-ingestion (raw baseline, no preprocessing)
- **V1**: Pure Docling output (minimal preprocessing, Docling only)
- **V2**: Docling + custom cleanup (Docling with additional AI cleanup applied)

Each version uses the same agent instructions (Version B from instruction testing) and is evaluated with the same judge prompt and rubric.

---

## 3. Baseline Run

### 3.1 What is the Baseline?

The baseline is the first complete evaluation run across all three versions using:
- All 69 questions from the final golden dataset
- The current preprocessing pipelines as-is (V0, V1, V2)
- The frozen agent instructions (Version B)
- The frozen judge prompt and scoring rubric

### 3.2 Baseline Goals

The baseline establishes:
- The absolute performance level for each version at the start
- The main failure categories and their frequency
- Which version performs better on which question types
- Which kinds of errors are most common (hallucination, refusal, grounding drift, etc.)

### 3.3 Baseline Artifacts

After the baseline run completes, generate:
- Overall metrics summary (correctness, grounding, hallucination rate per version)
- Per-question-type breakdown
- Failure analysis by category
- Run report in `run_reports/baseline_run.md`

---

## 4. Change Categories

After analyzing the baseline, improvements are grouped into three independent categories:

### 4.1 Preprocessing Changes (V0 → V1 → V2)

Preprocessing changes affect the source text before the agent sees it.

Examples:
- Docling extraction tuning
- Cleanup script improvements
- Field extraction or section reorganization
- Malformed text fixes
- Duplicate removal or merging

**When to make:** When failures are caused by missing, incomplete, or poorly structured source text.

### 4.2 Agent Instruction Changes

Agent instruction changes modify the system prompt.

Examples:
- Clarifying grounding requirements
- Adding examples or formatting instructions
- Refining refusal conditions
- Emphasizing particular content sections
- Adding step-by-step reasoning guidance

**When to make:** When failures are caused by the agent not interpreting instructions correctly, hallucinating despite good source text, or refusing correctly grounded questions.

### 4.3 Fallback Response Rules

Fallback rules add deterministic post-processing to catch predictable failures.

Examples:
- Detecting known bad phrases and replacing with fallback text
- Reformatting malformed structured responses
- Detecting and converting over-confident refusals to uncertain responses
- Replacing hallucinated metric values with "consult the manual"

**When to make:** Only as a last resort when a specific, repeatable failure pattern would take longer to fix at the instruction level.

---

## 5. Iteration Workflow

### 5.1 Before Each Iteration

1. Review the latest run report and failure analysis
2. Identify the top failure pattern that affects the most questions
3. Determine which category it falls into: preprocessing, instructions, or fallbacks
4. Document the proposed change in a decision file
5. Make exactly one change (one preprocessing commit, one instruction edit, or one fallback rule)

### 5.2 During Each Iteration

1. Run the full pipeline for the affected version(s)
2. Generate a new run report
3. Compare the new results to the previous run and the baseline
4. Log the result in `iteration_log.md`

### 5.3 After Each Iteration

1. If the change improved results or helped specific question types, keep it
2. If the change had no effect or regressed overall performance, revert it
3. If the change helped one version but hurt another, document that as a tradeoff and decide whether to keep it
4. Move on to the next iteration

---

## 6. Comparing Runs

When comparing a new run to a previous run:

- Report changes in overall metrics (e.g., correctness went from 0.68 to 0.71)
- Report changes in per-version metrics
- Report changes in per-question-type metrics
- Identify which specific questions changed (improved or regressed)
- Note whether improvements are consistent or only affect specific categories
- Flag any new failure patterns that did not appear in previous runs

---

## 7. Success Criteria

An iteration is successful if:

- At least one metric improves for at least one version
- No other metric regresses significantly for any version (regressions < 5% of the improvement)
- The improvement is attributable to the change made (not random variation)

An iteration is inconclusive if:

- Metrics stay the same or change by less than 2%
- Some metrics improve while others regress by similar amounts

An iteration is unsuccessful if:

- Overall metrics regress for any version
- The change introduces new failure patterns

---

## 8. Stopping Criteria

Stop iterating when:

- Overall metrics plateau (gains less than 2% per iteration for three consecutive iterations)
- All three versions have similar performance and further improvements would require major architectural changes
- Time or computational budget is exhausted
- I am satisfied with the performance level

---

## 9. Documentation Requirements

### 9.1 Per-Run Artifacts

For each run, create:
- `run_reports/{date}_{version}.md` with full metrics and per-question breakdown
- Log entry in `iteration_log.md`

### 9.2 Per-Change Artifacts

For each targeted change, create:
- `decisions/{date}_change_{category}_{description}.md` with rationale and results

### 9.3 Comparison Artifacts

After every third iteration or when making a major decision:
- Brief summary comparison of baseline vs. latest run
- Summary of all changes made to date and their cumulative effect

---

## 10. Tools Available

- **Evaluation dashboard** (`src/user_interface/pages/evaluation_dashboard.py`): View metrics, trends, and per-run details
- **Run comparison**: Manually compare CSV exports of two runs
- **Judge calibration data**: Disagreement logs to refine scoring if needed
- **Test notes**: Manual per-run observations for qualitative drift analysis

---

## 11. Timeline and Pacing

Recommended pace:
- Baseline run: 1 full day
- Baseline analysis: 1 day
- First iteration cycle: 2–3 days per iteration (1 day to change, 1 day to run, 1 day to analyze)
- Subsequent iterations: 2–3 days per iteration until plateau

Total estimated time: 2 weeks

---

## 12. What This Plan Is Not

This plan is not:

- A specification for the golden dataset (see `documentation/srs/` and `documentation/data/`)
- A specification for the judge scoring rubric (see `documentation/testing/judge_testing/`)
- A guide to designing agent instructions (see `documentation/testing/instruction_testing/`)
- A production runbook or deployment guide

It only covers systematic end-to-end evaluation and iteration.
