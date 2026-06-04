# EscapeAssist Judge LLM Test Plan

This document outlines the plan for testing the Judge LLM itself.

The goal is to measure how closely the Judge LLM matches my manual grading across EscapeAssist versions V0, V1, and V2 so I can refine the judge prompt and rubric.

---

## 1. Purpose

The purpose of this test plan is to:

- Evaluate whether the Judge LLM scores answers the same way I would score them manually.
- Compare judge behavior across the three EscapeAssist versions.
- Identify recurring scoring mismatches.
- Use those mismatches to improve the judge prompt and grading rubric.

This is a judge calibration workflow, not a product evaluation workflow.

---

## 2. Versions Under Test

I will run the Judge LLM on outputs from all three EscapeAssist versions:

- V0
- V1
- V2

Each version will be tested independently so I can compare judge consistency across the different pipeline outputs.

---

## 3. Sample Selection

For each EscapeAssist version, I will select 15 random questions from the golden dataset.

Selection rules:

- The questions must come from the golden dataset.
- The same 15-question sample should be used for all three versions when possible.
- The sample should include a mix of easy, medium, and harder questions.
- The sample should include grounded, partially grounded, and likely failure cases when possible.

If a question does not have a usable answer for a version, I will record that as a missing-output case.

---

## 4. Judging Workflow

For each sampled question and each EscapeAssist version, I will:

1. Run the Judge LLM on the model output.
2. Record the judge score and explanation.
3. Manually grade the same output myself.
4. Compare the judge result to my manual grade.
5. Record any disagreement and the reason for it.

This produces a paired dataset of judge judgments and human judgments.

---

## 5. Manual Grading Method

I will use my own grading as the reference standard.

For each answer, I will record:

- correctness
- grounding
- hallucination
- refusal quality, if applicable
- notes on why the score was assigned

If the judge disagrees with my score, I will note whether the issue appears to be:

- rubric interpretation drift
- too much tolerance for extra detail
- over-penalizing partial correctness
- incorrect hallucination detection
- refusal handling problems

---

## 6. Success Criteria

The judge calibration is successful if:

- the Judge LLM matches my manual scores on most samples
- disagreements are limited and explainable
- the judge behaves consistently across V0, V1, and V2
- the judge rubric can be updated with clear, testable improvements

I will treat repeated disagreement patterns as evidence that the judge prompt needs revision.

---

## 7. Expected Outputs

At the end of the test, I expect to have:

- a 15-question test set per version, or one shared 15-question sample applied to all versions
- judge outputs for all sampled answers
- manual grades for all sampled answers
- a disagreement log
- concrete prompt or rubric changes for the Judge LLM

---

## 8. What This Test Plan Is Not

This document is not:

- a golden dataset specification
- a model evaluation report
- an instruction-testing plan
- a production runbook

It only covers judge calibration against human grading.
