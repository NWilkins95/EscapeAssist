import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


# =========================================================
# Workflow Helpers
# =========================================================
def extract_reply(result: dict) -> str:
    """
    Extract the assistant's output text from a workflow result.

    Args:
        result: The workflow result dictionary.

    Returns:
        The assistant's output text, a safety-filter message, or a fallback message.
    """
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    return "I couldn't process that request. Please try again."


def load_workflow(version: str) -> callable:
    """
    Return the requested workflow function.

    Args:
        version: Workflow version key.

    Returns:
        The run_workflow callable for the requested version.
    """
    from workflows.V0workflow import run_workflow as run_v0
    from workflows.V1workflow import run_workflow as run_v1
    from workflows.V2workflow import run_workflow as run_v2

    workflows = {
        "V0": run_v0,
        "V1": run_v1,
        "V2": run_v2,
    }
    return workflows[version]


# =========================================================
# Evaluation Helpers
# =========================================================
def read_jsonl(path):
    """
    Read a JSONL file into a list of dictionaries.

    Args:
        path: Path to the JSONL file.

    Returns:
        A list of parsed JSON objects.
    """
    rows = []
    if not path.exists():
        return rows

    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    return rows


def list_runs(version, answers_dir, evaluations_dir):
    """
    Return the shared run ids that exist for both answers and evaluations.

    Args:
        version: Workflow version key.
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.

    Returns:
        A sorted list of shared run ids.
    """
    answer_dir = answers_dir / version
    eval_dir = evaluations_dir / version
    if not answer_dir.exists() or not eval_dir.exists():
        return []

    answer_runs = set()
    for path in answer_dir.glob(f"{version}_answers-*.jsonl"):
        answer_runs.add(path.stem.replace(f"{version}_answers-", ""))

    eval_runs = set()
    for path in eval_dir.glob(f"{version}_eval-*.jsonl"):
        eval_runs.add(path.stem.replace(f"{version}_eval-", ""))

    return sorted(answer_runs & eval_runs)


def load_run(version, run_id, answers_dir, evaluations_dir):
    """
    Load and merge answer and evaluation rows for one run.

    Args:
        version: Workflow version key.
        run_id: Shared timestamp run id.
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.

    Returns:
        A merged dataframe for the selected run.
    """
    answer_path = answers_dir / version / f"{version}_answers-{run_id}.jsonl"
    eval_path = evaluations_dir / version / f"{version}_eval-{run_id}.jsonl"

    answer_frame = pd.DataFrame(read_jsonl(answer_path))
    eval_frame = pd.DataFrame(read_jsonl(eval_path))

    if answer_frame.empty or eval_frame.empty:
        return pd.DataFrame()

    answer_frame = answer_frame.reset_index().rename(columns={"index": "row"})
    eval_frame = eval_frame.reset_index().rename(columns={"index": "row"})

    if "evaluation" in eval_frame.columns:
        score_frame = pd.json_normalize(eval_frame["evaluation"])
        eval_frame = pd.concat([eval_frame[["row"]], score_frame], axis=1)

    return answer_frame.merge(eval_frame, on="row", how="left")


def normalize_score(raw_score):
    """
    Normalize a raw judge score (0-5) to a 0-1 range by dividing by 6.

    Args:
        raw_score: Raw score from the judge (0-5).

    Returns:
        Normalized score (0-1), or None if raw_score is None/NaN.
    """
    if pd.isna(raw_score):
        return None
    return raw_score / 5


def metric_value(frame, column):
    """
    Compute the mean value for a numeric column.

    Args:
        frame: DataFrame containing the metric column.
        column: Metric column name.

    Returns:
        The mean value, or 0.0 when unavailable.
    """
    if frame.empty or column not in frame.columns:
        return 0.0
    return float(pd.to_numeric(frame[column], errors="coerce").mean())


def normalized_metric_value(frame, column):
    """
    Compute the mean normalized value (0-1) for a numeric column (0-5).

    Args:
        frame: DataFrame containing the metric column.
        column: Metric column name.

    Returns:
        The mean normalized value, or 0.0 when unavailable.
    """
    if frame.empty or column not in frame.columns:
        return 0.0
    raw_values = pd.to_numeric(frame[column], errors="coerce")
    normalized_values = raw_values.apply(normalize_score)
    return float(normalized_values.mean())


def hallucination_rate(frame):
    """
    Compute the share of rows marked with hallucination = True.

    Args:
        frame: DataFrame containing the hallucination column.

    Returns:
        The fraction of True hallucination values, or 0.0 when unavailable.
    """
    if frame.empty or "hallucination" not in frame.columns:
        return 0.0
    return float(pd.Series(frame["hallucination"]).fillna(False).map(bool).mean())


def build_trend_frame(answers_dir, evaluations_dir, versions):
    """
    Build normalized trend rows across successive runs for each version.

    Args:
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
        versions: Workflow version keys.

    Returns:
        DataFrame with normalized metrics by version and run index.
    """
    rows = []
    for version in versions:
        runs = list_runs(version, answers_dir, evaluations_dir)
        for run_index, run_id in enumerate(runs, start=1):
            frame = load_run(version, run_id, answers_dir, evaluations_dir)
            rows.append(
                {
                    "agent_version": version,
                    "run_index": run_index,
                    "run_id": run_id,
                    "correctness": normalized_metric_value(frame, "correctness"),
                    "grounding": normalized_metric_value(frame, "grounding"),
                    "hallucination": hallucination_rate(frame),
                }
            )

    return pd.DataFrame(rows)


def build_question_type_frame(answers_dir, evaluations_dir, versions):
    """
    Build normalized metric rows by question type using each version's latest run.

    Args:
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
        versions: Workflow version keys.

    Returns:
        DataFrame with normalized metrics grouped by version and question type.
    """
    rows = []
    for version in versions:
        runs = list_runs(version, answers_dir, evaluations_dir)
        if not runs:
            continue

        frame = load_run(version, runs[-1], answers_dir, evaluations_dir)
        if frame.empty:
            continue

        category_col = "type" if "type" in frame.columns else None
        if category_col is None:
            grouped = pd.DataFrame(
                [
                    {
                        "question_type": "all",
                        "correctness": normalized_metric_value(frame, "correctness"),
                        "grounding": normalized_metric_value(frame, "grounding"),
                        "hallucination": hallucination_rate(frame),
                    }
                ]
            )
        else:
            grouped = (
                frame.assign(
                    correctness_norm=pd.to_numeric(frame.get("correctness"), errors="coerce").apply(normalize_score),
                    grounding_norm=pd.to_numeric(frame.get("grounding"), errors="coerce").apply(normalize_score),
                    hallucination_norm=pd.Series(frame.get("hallucination")).fillna(False).map(bool).astype(float),
                )
                .groupby(category_col, dropna=False)
                .agg(
                    correctness=("correctness_norm", "mean"),
                    grounding=("grounding_norm", "mean"),
                    hallucination=("hallucination_norm", "mean"),
                )
                .reset_index()
                .rename(columns={category_col: "question_type"})
            )

        grouped["agent_version"] = version
        rows.append(grouped[["agent_version", "question_type", "correctness", "grounding", "hallucination"]])

    if not rows:
        return pd.DataFrame()

    output = pd.concat(rows, ignore_index=True)
    output["question_type"] = output["question_type"].astype(str)
    return output


def show_trend_charts(trend_frame, versions):
    """
    Render line charts for normalized metrics across successive runs.

    Args:
        trend_frame: DataFrame returned by build_trend_frame.
        versions: Workflow version keys.
    """
    if trend_frame.empty:
        st.info("No run trend data available yet.")
        return

    st.markdown("### Trend Charts Across Runs")
    metric_titles = {
        "correctness": "Correctness (normalized)",
        "grounding": "Grounding (normalized)",
        "hallucination": "Hallucination (normalized)",
    }

    for metric, title in metric_titles.items():
        chart_frame = trend_frame[["agent_version", "run_index", metric, "run_id"]].dropna()
        chart_frame = chart_frame[chart_frame["agent_version"].isin(versions)]
        if chart_frame.empty:
            continue

        st.markdown(f"#### {title}")
        chart = (
            alt.Chart(chart_frame)
            .mark_line(point=True)
            .encode(
                x=alt.X("run_index:Q", title="successive run"),
                y=alt.Y(f"{metric}:Q", title="score", scale=alt.Scale(domain=[0, 1])),
                color=alt.Color("agent_version:N", scale=alt.Scale(domain=versions), title="agent_version"),
                tooltip=[
                    alt.Tooltip("agent_version:N", title="agent_version"),
                    alt.Tooltip("run_index:Q", title="run_index"),
                    alt.Tooltip("run_id:N", title="run_id"),
                    alt.Tooltip(f"{metric}:Q", title=title, format=".3f"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(chart, width="stretch")


def show_question_type_bar_charts(question_type_frame, versions):
    """
    Render grouped bar charts by question type for normalized metrics.

    Args:
        question_type_frame: DataFrame returned by build_question_type_frame.
        versions: Workflow version keys.
    """
    if question_type_frame.empty:
        st.info("No question-type breakdown data available yet.")
        return

    st.markdown("### Breakdown By Question Type")
    st.caption("Uses each version's latest saved run.")

    metric_titles = {
        "correctness": "Correctness (normalized)",
        "grounding": "Grounding (normalized)",
        "hallucination": "Hallucination (normalized)",
    }

    for metric, title in metric_titles.items():
        pivot = question_type_frame.pivot(index="question_type", columns="agent_version", values=metric)
        pivot = pivot.reindex(columns=versions)
        st.markdown(f"#### {title}")
        st.bar_chart(pivot, y_label="score", x_label="question type")


# =========================================================
# Streamlit Rendering Helpers
# =========================================================
def run_version(version):
    """
    Run one workflow version through the evaluation harness.

    Args:
        version: Workflow version key.
    """
    from evaluation.judge.judge_runner import run_selected_version

    progress_text = st.empty()
    progress_bar = st.progress(0, text=f"Starting {version}")

    def update_progress(completed, total, stage):
        value = 0 if total == 0 else min(completed / total, 1.0)
        progress_bar.progress(value, text=stage)
        progress_text.caption(f"{stage}: {completed}/{total}")

    with st.spinner(f"Running {version} evaluation..."):
        run_selected_version(version, progress_callback=update_progress)

    st.success(f"Finished {version} evaluation.")
    st.rerun()


def show_exports(frame, version, run_id):
    """
    Render CSV and JSON export controls for a selected run.

    Args:
        frame: DataFrame to export.
        version: Workflow version key.
        run_id: Shared timestamp run id.
    """
    if frame.empty:
        return

    default_fields = [field for field in ["question", "model_answer", "correctness", "grounding", "hallucination", "reasoning"] if field in frame.columns]
    fields = st.multiselect("Export fields", list(frame.columns), default=default_fields, key=f"fields-{version}-{run_id}")
    export_frame = frame[fields] if fields else frame

    csv_data = export_frame.to_csv(index=False).encode("utf-8")
    json_data = json.dumps(export_frame.to_dict(orient="records"), indent=2, ensure_ascii=False).encode("utf-8")

    col1, col2 = st.columns(2)
    col1.download_button("Download CSV", csv_data, file_name=f"{version}_{run_id}.csv", mime="text/csv")
    col2.download_button("Download JSON", json_data, file_name=f"{version}_{run_id}.json", mime="application/json")


def show_run(frame, version, run_id):
    """
    Render the metrics and per-question table for one saved run.

    Args:
        frame: DataFrame for the run.
        version: Workflow version key.
        run_id: Shared timestamp run id.
    """
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Questions", len(frame))
    
    raw_correctness = metric_value(frame, 'correctness')
    norm_correctness = normalized_metric_value(frame, 'correctness')
    col2.metric("Avg Correctness", f"{raw_correctness:.1f} (norm: {norm_correctness:.2f})")
    
    raw_grounding = metric_value(frame, 'grounding')
    norm_grounding = normalized_metric_value(frame, 'grounding')
    col3.metric("Avg Grounding", f"{raw_grounding:.1f} (norm: {norm_grounding:.2f})")
    
    col4.metric("Hallucination True Rate", f"{hallucination_rate(frame):.0%}")

    show_exports(frame, version, run_id)

    if frame.empty:
        st.info("No saved results for this run.")
        return

    # Initialize session state for question navigation
    nav_key = f"question_index_{version}_{run_id}"
    if nav_key not in st.session_state:
        st.session_state[nav_key] = 0

    # Question type filtering
    st.markdown("---")
    st.subheader("Filters")
    
    available_types = sorted(frame['type'].unique()) if 'type' in frame.columns else []
    selected_types = st.multiselect(
        "Filter by question type",
        available_types,
        default=available_types,
        key=f"filter-{version}-{run_id}",
    )
    
    # Filter frame based on selected types
    if selected_types:
        filtered_frame = frame[frame['type'].isin(selected_types)].reset_index(drop=True)
    else:
        filtered_frame = frame.reset_index(drop=True)
    
    # Reset navigation index if filtered frame is smaller
    if nav_key in st.session_state and st.session_state[nav_key] >= len(filtered_frame):
        st.session_state[nav_key] = 0

    # Question navigation
    st.markdown("---")
    st.subheader("Question Details")
    
    question_num = st.selectbox(
        "Select Question",
        range(len(filtered_frame)),
        index=st.session_state[nav_key],
        format_func=lambda i: f"Question {i + 1} of {len(filtered_frame)}",
        key=f"select-{version}-{run_id}",
    )
    st.session_state[nav_key] = question_num

    # Display selected question details
    row = filtered_frame.iloc[st.session_state[nav_key]]
    
    st.markdown("### Question")
    st.write(row.get('question', 'N/A'))
    
    st.markdown("### Model Answer")
    st.write(row.get('model_answer', 'N/A'))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Judge Scores")
        correctness = row.get('correctness', '-')
        grounding = row.get('grounding', '-')
        hallucination = row.get('hallucination', '-')
        
        if pd.notna(correctness):
            norm_c = normalize_score(correctness)
            st.metric("Correctness", f"{correctness} / {norm_c:.2f}")
        
        if pd.notna(grounding):
            norm_g = normalize_score(grounding)
            st.metric("Grounding", f"{grounding} / {norm_g:.2f}")
        
        if pd.notna(hallucination):
            st.metric("Hallucination", str(bool(hallucination)).lower())
    
    with col2:
        st.markdown("### Judge Reasoning")
        st.write(row.get('reasoning', 'N/A'))


def show_version_tab(version, answers_dir, evaluations_dir):
    """
    Render the dashboard content for one workflow version.

    Args:
        version: Workflow version key.
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
    """
    st.subheader(version)

    if st.button(f"Run {version}", key=f"run-{version}"):
        run_version(version)

    runs = list_runs(version, answers_dir, evaluations_dir)
    if not runs:
        st.info("No saved runs found yet.")
        return

    run_id = st.selectbox("Saved run", runs, index=len(runs) - 1, key=f"run-select-{version}")
    frame = load_run(version, run_id, answers_dir, evaluations_dir)
    show_run(frame, version, run_id)


def render_evaluation_dashboard(answers_dir, evaluations_dir, versions):
    """
    Render the full evaluation dashboard layout.

    Args:
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
        versions: Workflow version keys.
    """
    overall_tab, v0_tab, v1_tab, v2_tab = st.tabs(["Overall", "V0", "V1", "V2"])

    with overall_tab:
        st.subheader("Overall Comparison")

        run_cols = st.columns(len(versions))
        for version, column in zip(versions, run_cols):
            with column:
                if st.button(f"Run {version}", key=f"overall-run-{version}"):
                    run_version(version)

        summary_rows = []
        history_rows = []
        for version in versions:
            runs = list_runs(version, answers_dir, evaluations_dir)
            if runs:
                latest_run = runs[-1]
                frame = load_run(version, latest_run, answers_dir, evaluations_dir)
                summary_rows.append(
                    {
                        "Version": version,
                        "Run": latest_run,
                        "Questions": len(frame),
                        "Avg Correctness (raw)": f"{metric_value(frame, 'correctness'):.1f}",
                        "Avg Correctness (norm)": f"{normalized_metric_value(frame, 'correctness'):.2f}",
                        "Avg Grounding (raw)": f"{metric_value(frame, 'grounding'):.1f}",
                        "Avg Grounding (norm)": f"{normalized_metric_value(frame, 'grounding'):.2f}",
                        "Hallucination True Rate": f"{hallucination_rate(frame):.0%}",
                    }
                )

            for run_id in runs:
                frame = load_run(version, run_id, answers_dir, evaluations_dir)
                history_rows.append(
                    {
                        "Version": version,
                        "Run": run_id,
                        "Avg Correctness (raw)": f"{metric_value(frame, 'correctness'):.1f}",
                        "Avg Correctness (norm)": f"{normalized_metric_value(frame, 'correctness'):.2f}",
                        "Avg Grounding (raw)": f"{metric_value(frame, 'grounding'):.1f}",
                        "Avg Grounding (norm)": f"{normalized_metric_value(frame, 'grounding'):.2f}",
                        "Hallucination True Rate": f"{hallucination_rate(frame):.0%}",
                    }
                )

        if summary_rows:
            st.dataframe(pd.DataFrame(summary_rows), width='stretch', hide_index=True)
        else:
            st.info("No saved runs found yet.")

        if len(history_rows) > 1:
            st.markdown("### Run History")
            st.dataframe(pd.DataFrame(history_rows), width='stretch', hide_index=True)

        trend_frame = build_trend_frame(answers_dir, evaluations_dir, versions)
        show_trend_charts(trend_frame, versions)

        question_type_frame = build_question_type_frame(answers_dir, evaluations_dir, versions)
        show_question_type_bar_charts(question_type_frame, versions)

    with v0_tab:
        show_version_tab("V0", answers_dir, evaluations_dir)

    with v1_tab:
        show_version_tab("V1", answers_dir, evaluations_dir)

    with v2_tab:
        show_version_tab("V2", answers_dir, evaluations_dir)


def render_escapeassist_page(version, knowledge_text, workflow_input_cls):
    """
    Render one EscapeAssist chat page.

    Args:
        version: Workflow version key.
        knowledge_text: Short description of the knowledge source shown on the page.
        workflow_input_cls: WorkflowInput class for the selected version.
    """
    import time

    from async_runner import run_async

    workflow = load_workflow(version)
    message_key = f"messages_{version.lower()}"
    history_key = f"conversation_history_{version.lower()}"

    st.image("assets/IMG_4865.jpeg")
    st.header(f"Welcome to EscapeAssist {version}!")
    st.markdown(knowledge_text)
    st.markdown("Ask me anything about your 2022 Ford Escape, and I'll do my best to assist you!")

    if message_key not in st.session_state:
        st.session_state[message_key] = []

    if history_key not in st.session_state:
        st.session_state[history_key] = []

    for msg in st.session_state[message_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about your Ford Escape...")

    if prompt:
        st.session_state[message_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        workflow_input = workflow_input_cls(
            input_as_text=prompt,
            conversation_history=st.session_state[history_key] or None,
        )

        with st.chat_message("assistant"):
            with st.spinner("EscapeAssist is thinking..."):
                result = run_async(workflow(workflow_input))

            reply = extract_reply(result)

            placeholder = st.empty()
            typed = ""
            for char in reply:
                typed += char
                placeholder.markdown(typed)
                time.sleep(0.01)

        if "conversation_history" in result:
            st.session_state[history_key] = result["conversation_history"]

        st.session_state[message_key].append({"role": "assistant", "content": reply})