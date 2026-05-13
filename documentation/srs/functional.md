## Section 2a: Must Have Requirements

**FR‑1** The system shall preprocess the 2022 Ford Escape Owner’s Manual into a raw cleaned text version.

**FR‑2** The system shall preprocess the manual into a cleaned and LLM‑organized version that preserves section structure.

**FR‑3** The system shall ingest three versions of the manual into OpenAI’s retrieval system:
- the baseline auto‑ingested version,
- the raw preprocessed version,
- the cleaned and LLM‑organized version.

**FR‑4** The system shall allow users to ask natural‑language questions about the 2022 Ford Escape.

**FR‑5** The system shall retrieve relevant manual content and generate grounded answers based solely on retrieved information.

**FR‑6** The system shall support powertrain‑specific queries, including Hybrid, PHEV, EcoBoost, and AWD/FWD information.

**FR‑7** The system shall allow the user to select which agent configuration (baseline, raw‑preprocessed, cleaned‑organized) is used during a session.

**FR‑8** The system shall provide a Streamlit‑based chat interface that displays user queries and system responses.

**FR‑9** The system shall maintain chat history for the duration of a user session.

**FR‑10** The system shall include a golden question dataset covering major manual categories (warnings, towing, hybrid behavior, safety, maintenance, etc.).

**FR‑11** The system shall run an automated evaluation harness that sends each golden‑set question to all three agents and collects their responses.

**FR‑12** The system shall use a judge LLM to score each response for accuracy, grounding, and hallucination.

**FR‑13** The system shall store evaluation results in a structured format such as JSON or CSV.

**FR‑14** The system shall provide a dashboard that visualizes accuracy, hallucination rate, and category‑level performance for all three agents.

**FR‑15** The system shall allow filtering or sorting of evaluation results in the dashboard.

## Section 2b: Stretch Requirements

**SR-1** The system shall use a sliding context window to keep only the last 5 messages within context.
