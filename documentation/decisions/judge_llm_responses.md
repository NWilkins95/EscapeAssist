# Judge LLM Responses API Instructions and Structured Output Decision

- Date: May 27, 2026
- Owner: Nicholas Wilkins

## Summary

The Judge LLM implementation now uses the OpenAI Responses API `instructions` field for the judge prompt and a strict JSON schema for the output format.

## Context

The evaluation harness needs the Judge LLM to behave consistently and return machine-readable results that can be stored, normalized, and consumed by the evaluation dashboard. Early versions of the runner passed the judge prompt as part of the user input and relied on parsing free-form text responses, which made the output harder to control and more fragile to consume.

## Decision

The implementation in [src/evaluation/judge/judge_runner.py](../../src/evaluation/judge/judge_runner.py) now sends the judge instructions separately from the case input and requires structured JSON output with the fields `correctness`, `grounding`, `hallucination`, and `reasoning`.
## Why This Was Chosen

1. Separating instructions from the case data better matches the Responses API design and reduces prompt confusion.
2. Keeping the judge prompt in `instructions` makes the request clearer and easier to maintain.
3. A strict JSON schema guarantees that downstream code receives predictable output.
4. Structured output removes the need to parse extra text or strip markdown fences.
5. The dashboard and artifact pipeline can now consume judge results directly without extra cleanup.

## Consequences

- Positive:
  - More reliable judge responses.
  - Cleaner separation between prompt policy and evaluation input.
  - Guaranteed JSON output for downstream parsing.
  - Less brittle post-processing code.

- Trade-offs:
  - The runner must stay aligned with the exact JSON schema.
  - Any schema change requires updating both the request and the parsing code.

## Follow-Up Actions

1. Keep `judge_runner.py` aligned with the Responses API schema used by the judge.
2. Preserve the judge instructions in [src/evaluation/judge/judge_instructions.py](../../src/evaluation/judge/judge_instructions.py) as the canonical prompt text.
3. Keep evaluation output parsing minimal since the response is now guaranteed to be valid JSON.
4. Reuse the same structured output shape in the evaluation dashboard and any future reporting tools.
