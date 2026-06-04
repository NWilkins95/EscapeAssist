# Evaluation Artifact Separation Decision

- Date: May 28, 2026
- Owner: Nicholas Wilkins

## Summary

The evaluation pipeline will store model answers and Judge LLM evaluations as separate JSONL artifacts, linked by a shared timestamp.

## Context

The evaluation harness needs to support two related workflows: generating model answers from the golden dataset and scoring those answers with the Judge LLM. Keeping those outputs in a single file makes the pipeline harder to manage and makes manual review less convenient. In addition, the Judge LLM output should stay separate while I do my own grading so that my labels are not influenced by the model's evaluation.

## Decision

Store answer generation output and Judge LLM output in separate files under the outputs directory. Use the same timestamped run name for both files so downstream metrics code can match them reliably.

The answer file will contain the original question, model answer, ground truth, source quote, and question type. The evaluation file will contain the Judge LLM's structured score for the same item. A metrics step can then load both files, join records, and calculate aggregate results.

## Why This Was Chosen

1. Separating the artifacts keeps the workflow easier to understand and maintain.
2. Timestamped run IDs make it straightforward to match answer files with evaluation files.
3. Independent files make it easier to inspect historical runs without mixing stages together.
4. Keeping the Judge LLM output separate reduces the chance of bias when manually grading the same answers.
5. The metrics code can stay simple because it only needs to read and join two structured files.

## Consequences

- Positive:
  - Clearer organization of evaluation outputs.
  - Easier historical review of past runs.
  - Cleaner manual grading workflow.
  - Better separation between generation, judging, and metrics.

- Trade-offs:
  - The metrics step must resolve both files for each run.
  - File naming and timestamp conventions must stay consistent.
  - More than one artifact must be tracked per evaluation run.

## Follow-Up Actions

1. Keep answer files and evaluation files in separate timestamped subfolders or filenames.
2. Ensure both artifacts include a shared run identifier or timestamp.
3. Build the metrics step to join answer and evaluation records by that shared identifier.
4. Preserve the evaluation file for later comparison when manually grading the same answers.