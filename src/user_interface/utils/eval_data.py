import json

import pandas as pd


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
    Normalize a raw judge score (0-5) to a 0-1 range.

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