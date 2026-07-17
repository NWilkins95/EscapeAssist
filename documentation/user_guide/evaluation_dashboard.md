# EscapeAssist Evaluation Dashboard Guide

This guide explains how to use the Streamlit evaluation dashboard for EscapeAssist.

## What The Dashboard Does

The dashboard lets you inspect saved evaluation runs for V0, V1, and V2. It loads the answer files and Judge LLM output files for each run, joins them by timestamp, and displays summary metrics, charts, and per-question details.

## How The Data Is Organized

Evaluation artifacts are stored as separate timestamped JSONL files:

- Answers: `src/evaluation/outputs/answers/{V0,V1,V2}/`
- Evaluations: `src/evaluation/outputs/evaluations/{V0,V1,V2}/`

Each run uses the same timestamp in the answer and evaluation filenames so the dashboard can match them reliably.

## Launching The Dashboard

Open the Streamlit app and select the Evaluation Dashboard page:

```bash
streamlit run src/user_interface/app.py
```

The dashboard is one of the pages exposed by the app navigation.

## Dashboard Layout

### Overall Tab

The Overall tab shows:

- Run buttons for V0, V1, and V2
- A summary table for the latest saved run in each version
- A run history table for older runs
- Trend charts across runs
- Question-type comparison charts

### Version Tabs

Each version tab shows:

- A run button for that version
- A dropdown for selecting any saved run
- The key summary metrics for the selected run
- A question-type filter
- A per-question inspector with the question, model answer, judge scores, and judge reasoning
- CSV and JSON export controls

## Reading The Metrics

The dashboard shows both raw averages and normalized averages for correctness and grounding.

- Raw scores are on the judge’s 0-5 scale.
- Normalized scores are on a 0-1 scale and are computed as `raw_score / 5`.
- Hallucination is shown as a true-rate percentage.

Use the normalized metrics when comparing runs, because they are easier to compare across versions and are the values used in the system testing reports.

## Typical Workflow

1. Select a version tab and run the latest evaluation.
2. Pick a saved run from the dropdown.
3. Review the summary metrics and per-question entries.
4. Use the question-type filter to focus on a category such as factual, procedural, table, or invalid.
5. Export the run if you want to review the results outside Streamlit.

## Troubleshooting

- If no saved runs appear, confirm that the answer and evaluation JSONL files exist for the same timestamp.
- If the metrics look wrong, verify that both the answers and evaluations directories contain matching files for the selected version.
- If a question row is missing judge scores, check the evaluation JSONL file for that run.