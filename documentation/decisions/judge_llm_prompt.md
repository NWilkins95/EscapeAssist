# Judge LLM Prompt and Rubric Decision

- Date: May 23, 2026
- Owner: Nicholas Wilkins

## Summary

The Judge LLM will use a structured prompt with a fixed scoring rubric for evaluating model answers against the dataset ground truth and a supporting source quote.

## Context

The prompt in [src/evaluation/judge/judge_instructions.py](../../src/evaluation/judge/judge_instructions.py) is the reference implementation for the current rubric wording and output format.
## Decision

Use a multi-point judge rubric rather than a binary one. The judge prompt asks for separate scores for correctness, grounding, and hallucination judgement, with the scoring scale expressed as a 0-5 range so the model has enough room to distinguish partial credit from clear failures.

Downstream evaluation code will normalize the judge outputs to a 0-1 scale after the Judge LLM returns its response by dividing each numeric score by 5.

## Rubric Behavior

1. Correctness reflects whether the answer matches the ground truth in meaning and completeness.
2. Grounding reflects whether the answer is supported by the provided source quote.
3. Hallucination is marked true only when the judge believes unsupported content is likely incorrect or fabricated.
4. Correct additional information should not reduce correctness if it is still plausible and consistent with the manual.
5. Grounding should be reduced when extra information is not supported by the source quote, even if the answer is otherwise correct.
6. Normalize raw numeric scores with `normalized_score = raw_score / 6`.

## Consequences

- Positive:
  - Gives the Judge LLM more room to distinguish near-misses from fully incorrect answers.
  - Makes scoring more stable and repeatable than a binary rubric.
  - Preserves useful distinctions between correctness and grounding.
  - Lets the evaluation pipeline convert results to a normalized 0-1 score later.

- Trade-offs:
  - The rubric is slightly more complex to explain and interpret.
  - Downstream code must normalize the judge output before aggregation.

## Follow-Up Actions
1. Keep `judge_instructions.py` aligned with the final rubric wording.
3. Reuse the same rubric wording in any evaluation dashboards or reports.