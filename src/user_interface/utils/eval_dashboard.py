import pandas as pd
import streamlit as st

from user_interface.utils.eval_charts import show_question_type_bar_charts, show_trend_charts
from user_interface.utils.eval_data import (
    build_question_type_frame,
    build_trend_frame,
    hallucination_rate,
    list_runs,
    load_run,
    metric_value,
    normalized_metric_value,
)

from evaluation.judge.judge_runner import run_selected_version


def run_version(version):
    """
    Run one workflow version through the evaluation harness.

    Args:
        version: Workflow version key.
    """
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
    json_data = export_frame.to_dict(orient="records")

    col1, col2 = st.columns(2)
    col1.download_button("Download CSV", csv_data, file_name=f"{version}_{run_id}.csv", mime="text/csv")
    col2.download_button("Download JSON", pd.Series(json_data).to_json(orient="records", force_ascii=False).encode("utf-8"), file_name=f"{version}_{run_id}.json", mime="application/json")


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

    nav_key = f"question_index_{version}_{run_id}"
    if nav_key not in st.session_state:
        st.session_state[nav_key] = 0

    st.markdown("---")
    st.subheader("Filters")

    available_types = sorted(frame['type'].unique()) if 'type' in frame.columns else []
    selected_types = st.multiselect(
        "Filter by question type",
        available_types,
        default=available_types,
        key=f"filter-{version}-{run_id}",
    )

    if selected_types:
        filtered_frame = frame[frame['type'].isin(selected_types)].reset_index(drop=True)
    else:
        filtered_frame = frame.reset_index(drop=True)

    if nav_key in st.session_state and st.session_state[nav_key] >= len(filtered_frame):
        st.session_state[nav_key] = 0

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
            st.metric("Correctness", f"{correctness} / {float(correctness) / 5:.2f}")

        if pd.notna(grounding):
            st.metric("Grounding", f"{grounding} / {float(grounding) / 5:.2f}")

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


def show_version_charts(version, title, answers_dir, evaluations_dir):
    """
    Render version-specific trend and question-type charts.

    Args:
        version: Workflow version key.
        title: Section title for the version chart block.
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
    """
    st.subheader(title)

    trend_frame = build_trend_frame(answers_dir, evaluations_dir, [version])
    show_trend_charts(trend_frame, [version])

    question_type_frame = build_question_type_frame(answers_dir, evaluations_dir, [version])
    show_question_type_bar_charts(question_type_frame, [version])


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
        show_version_charts("V0", "V0 Charts", answers_dir, evaluations_dir)
        show_version_tab("V0", answers_dir, evaluations_dir)

    with v1_tab:
        show_version_charts("V1", "V1 Charts", answers_dir, evaluations_dir)
        show_version_tab("V1", answers_dir, evaluations_dir)

    with v2_tab:
        show_version_charts("V2", "V2 Charts", answers_dir, evaluations_dir)
        show_version_tab("V2", answers_dir, evaluations_dir)