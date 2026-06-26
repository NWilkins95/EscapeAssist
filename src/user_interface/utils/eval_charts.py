import altair as alt
import streamlit as st

from user_interface.utils.eval_data import build_question_type_frame, build_trend_frame


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
        chart_frame = question_type_frame[["agent_version", "question_type", metric]].dropna()
        chart_frame = chart_frame[chart_frame["agent_version"].isin(versions)]
        if chart_frame.empty:
            continue

        st.markdown(f"#### {title}")
        chart = (
            alt.Chart(chart_frame)
            .mark_bar()
            .encode(
                x=alt.X("question_type:N", title="question type"),
                xOffset=alt.XOffset("agent_version:N", scale=alt.Scale(domain=versions)),
                y=alt.Y(
                    f"{metric}:Q",
                    title="score",
                    scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(format=".0%"),
                ),
                color=alt.Color("agent_version:N", scale=alt.Scale(domain=versions), title="agent_version"),
                tooltip=[
                    alt.Tooltip("question_type:N", title="question type"),
                    alt.Tooltip("agent_version:N", title="agent_version"),
                    alt.Tooltip(f"{metric}:Q", title=title, format=".1%"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(chart, width="stretch")


def show_version_charts(version, title, answers_dir, evaluations_dir):
    """
    Render version-specific trend and question-type charts.

    Args:
        version: Workflow version key.
        title: Section title for the version chart block.
        answers_dir: Base answers directory.
        evaluations_dir: Base evaluations directory.
    """
    st.header(title)

    trend_frame = build_trend_frame(answers_dir, evaluations_dir, [version])
    show_trend_charts(trend_frame, [version])

    question_type_frame = build_question_type_frame(answers_dir, evaluations_dir, [version])
    show_question_type_bar_charts(question_type_frame, [version])
