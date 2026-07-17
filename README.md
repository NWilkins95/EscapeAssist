# EscapeAssist

EscapeAssist is a senior project focused on building a retrieval-augmented assistant for the 2022 Ford Escape owner’s manual. The repository includes the preprocessing pipeline, the Streamlit chat application, the evaluation harness, and the system-testing documentation used to compare versions over time.

## What’s In The Project

### Preprocessing

The preprocessing pipeline extracts the manual into Markdown in two forms:

- V1: raw Docling extraction
- V2: cleaned and reorganized output

See [documentation/user_guide/preprocessing.md](documentation/user_guide/preprocessing.md) for the full pipeline guide.

### Streamlit Application

The UI in `src/user_interface/` exposes:

- Home
- EscapeAssist V0
- EscapeAssist V1
- EscapeAssist V2
- Evaluation Dashboard

Use [documentation/user_guide/streamlit_ui.md](documentation/user_guide/streamlit_ui.md) for navigation and page-level guidance.

### Evaluation Harness

The evaluation pipeline stores answer outputs and Judge LLM outputs as separate timestamped JSONL artifacts. The dashboard and system-testing reports use those artifacts to compare runs.

See [documentation/user_guide/judge_llm_evaluation.md](documentation/user_guide/judge_llm_evaluation.md) and [documentation/user_guide/evaluation_dashboard.md](documentation/user_guide/evaluation_dashboard.md).

## Quick Start

1. Install the project dependencies for preprocessing, evaluation, and Streamlit.
2. Run the preprocessing pipeline if you need fresh manual outputs.
3. Launch the app with `streamlit run src/user_interface/app.py`.
4. Open the Evaluation Dashboard page to inspect saved runs and compare V0, V1, and V2.

## Repository Layout

```text
README.md
documentation/
	user_guide/
		preprocessing.md
		judge_llm_evaluation.md
		streamlit_ui.md
		evaluation_dashboard.md
	testing/
		system_testing/
			run_reports/
			decisions/
			iteration_log.md
src/
	preprocessing/
	evaluation/
	user_interface/
```

## Key Paths

- Preprocessing script: `src/preprocessing/preprocess.py`
- Streamlit entry point: `src/user_interface/app.py`
- Evaluation outputs: `src/evaluation/outputs/answers/` and `src/evaluation/outputs/evaluations/`
- Golden dataset: `src/evaluation/data/golden.jsonl`
- System testing reports: `documentation/testing/system_testing/run_reports/`
- System testing decisions: `documentation/testing/system_testing/decisions/`

## Documentation

Start with the user guide index at [documentation/user_guide/README.md](documentation/user_guide/README.md).

For evaluation work, the most useful references are:

- [documentation/user_guide/preprocessing.md](documentation/user_guide/preprocessing.md)
- [documentation/user_guide/judge_llm_evaluation.md](documentation/user_guide/judge_llm_evaluation.md)
- [documentation/user_guide/evaluation_dashboard.md](documentation/user_guide/evaluation_dashboard.md)
- [documentation/user_guide/streamlit_ui.md](documentation/user_guide/streamlit_ui.md)

## System Testing

The system-testing history is documented in `documentation/testing/system_testing/`. It includes run reports, decision notes, and the iteration log that tracks how the preprocessing and benchmark changes affected correctness, grounding, and hallucination over time.