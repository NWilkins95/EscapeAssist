# EscapeAssist Judge LLM Evaluation Guide

This guide explains how EscapeAssist uses a Judge LLM to score model answers during evaluation.

---

## What the Judge LLM Does

The Judge LLM compares a model answer against:

- the question
- the ground truth answer
- a source quote from the manual

It produces structured scores for correctness, grounding, and hallucination.

---

## Why the Scoring Uses Multiple Levels

A simple yes/no score is too limited for evaluation. EscapeAssist uses a 0-5 rubric so the Judge LLM can distinguish between:

- fully correct answers
- mostly correct answers
- partially correct answers
- incorrect answers

This is more consistent than asking the model to make a binary judgment.

---

## How the Judge Handles Extra Details

Sometimes a model answer may include information that is not in the exact source quote, but is still consistent with the manual.

In that case:

- correctness should not be reduced just because the answer includes a plausible extra detail
- grounding should be reduced if the extra detail is not supported by the source quote
- hallucination should only be marked true if the extra detail is likely incorrect or fabricated

This matters because the dataset quote cannot list every possible supporting passage from the manual.

---

## Normalization

The Judge LLM uses a 0-5 rubric first, then the evaluation pipeline converts the raw scores to a 0-1 scale for downstream reporting.

Use this formula:

`normalized_score = raw_score / 5`

Examples:

- `0 -> 0.0`
- `2 -> 0.4`
- `5 -> 1.0`

That gives the judge enough precision while keeping final metrics easy to compare.

---

## Where the Prompt Lives

The judge prompt is implemented in [src/evaluation/judge/judge_prompt.py](../../src/evaluation/judge/judge_prompt.py).

---

## Plain-English Example

If the source quote says the tire pressure is 32 PSI and the model answer says 32 PSI plus an extra detail that is still reasonable, the judge can keep correctness high.

If the model answer adds a detail that is not supported and seems fabricated, grounding should drop and hallucination should be marked true.