# EscapeAssist Agent Instruction Update Decision

- Date: June 17, 2026
- Owner: Nicholas Wilkins

## Summary

The EscapeAssist agent instructions will be updated to stop repeated retrieval retries when the manual does not contain relevant information and to return a fixed fallback response instead.

## Context

During a full evaluation pipeline run, the agent became stuck on a question where retrieval kept cycling through file search without finding any useful chunks. The flow was:

- file-search returned no useful chunks
- the agent tried again instead of stopping
- the agent never reached the fallback behavior
- the evaluation harness kept retrying because the agent never produced a final answer

Question 67 appears to be one of the cases where no chunk has even partial relevance, so the retrieval tool keeps firing without ever converging on an answer.

## Decision

Update the EscapeAssist agent instructions so that if retrieved text is irrelevant, empty, or does not answer the question, the agent must stop searching and respond with:

"The manual does not provide this information."

The instructions will explicitly say:

- Do not attempt additional searches.
- Do not guess.
- Respond with the fallback message above.

## Why This Was Chosen

1. It prevents endless retrieval loops when the manual does not contain the answer.
2. It gives the evaluation harness a final answer to record instead of waiting indefinitely.
3. It keeps the agent grounded in the source material instead of encouraging guesses.
4. It makes failure behavior explicit and consistent across missing or irrelevant retrieval results.
5. It reduces wasted time on questions that are not supported by the available files.

## Consequences

- Positive:
  - The agent will return a clear fallback when retrieval is not useful.
  - The evaluation harness will no longer hang on questions that cannot be answered from the manual.
  - The assistant behavior will be more predictable for unsupported questions.

- Trade-offs:
  - The agent will stop earlier on low-signal retrieval results.
  - Some questions may return the fallback even when a human might infer an answer from broader context, but that is preferred over guessing.

## Follow-Up Actions

1. Update the EscapeAssist agent instructions with the fallback rule.
2. Re-run the full evaluation pipeline after the instruction update.
3. Confirm that unsupported questions now terminate with the exact fallback response.
