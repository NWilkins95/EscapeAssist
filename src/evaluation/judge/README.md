# Judge Evaluation Prompt

This folder contains the prompt used by the Judge LLM to evaluate model answers in the EscapeAssist evaluation harness.

## What It Does

The judge compares three things:

- the user question
- the model answer
- the source quote from the dataset

It then returns structured scores for:

- correctness
- grounding
- hallucination

## Why the Rubric Is Multi-Point

A binary score was too coarse for consistent evaluation. A 0-5 rubric gives the Judge LLM more room to separate:

- fully correct answers
- partially correct answers
- answers with unsupported extra details
- clearly incorrect or fabricated answers

## How Extra Information Is Handled

The judge does not automatically penalize an answer for adding extra information. If the extra detail is plausible and consistent with the manual, correctness can stay high.

Grounding is reduced when the answer includes details that are not supported by the source quote. Hallucination is marked true only when the extra information is likely incorrect or fabricated.

## Normalization

The judge outputs are normalized to a 0-1 scale after the Judge LLM finishes scoring.

Use this formula for each numeric score:

`normalized_score = raw_score / 5`

Examples:

- `0 -> 0.0`
- `3 -> 0.6`
- `5 -> 1.0`

## Reference

The prompt implementation lives in [judge_prompt.py](judge_prompt.py).