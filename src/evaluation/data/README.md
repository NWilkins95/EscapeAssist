# Golden Dataset (evaluation/data)

## Purpose

This directory contains the canonical (golden) dataset used by the EscapeAssist
evaluation harness. The golden dataset provides ground-truth question/answer
pairs that the judge LLM uses to compute metrics and compare system outputs across
experiments and versions.

## File format

- Store data as newline-delimited JSON (`.jsonl`). Each line must be a single
	valid JSON object.

## Record fields

Each JSON object (one line) should include at least:

- `id` (int): stable unique identifier for the case.
- `question` (string): the prompt presented to the agent.
- `truth` (string): canonical/golden answer used for scoring.
- `source_quote` (string): supporting excerpt(s)
- `type` (string): one of `factual`, `procedural`, `table`, or `invalid`.


## Example line

{"id": 2, "question": "Where should children 12 years old and under be seated?", "truth": "Children 12 years old and under should be properly secured in a rear seating position whenever possible.", "source_quote": "Properly secure children 12 years old and under in a rear seating position whenever possible.", "type": "factual"}

## Invalid / refusal cases

If a question should not be answered (e.g. off-topic, unsafe, unverifiable, not in knowledge base),
set `"type": "invalid"` and `truth` as an empty string or a short canonical refusal message.


## Usage notes (Streamlit / UI)

- Resolve paths relative to the code file using `Path(__file__).resolve()` to
	avoid broken paths when Streamlit changes the working directory.
