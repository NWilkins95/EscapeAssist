import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# Path Setup & Client Initialization
# =========================================================
SRC_DIR = Path(__file__).resolve().parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

load_dotenv()
client = OpenAI()

from evaluation.judge.judge_instructions import get_judge_instructions
from evaluation.judge.judge_runner import (OUTPUTS_DIR, WORKFLOWS, extract_reply, load_golden_data) 
from user_interface.async_runner import run_async 

DEFAULT_SAMPLE_SIZE = 15
DEFAULT_SEED = 42
VERSIONS = ("V0", "V1", "V2")

# =========================================================
# Sampling & File Helpers
# =========================================================
def pick_sample(golden_data: list[dict], sample_size: int, seed: int) -> list[dict]:
    if sample_size > len(golden_data):
        raise ValueError(
            f"Requested sample size {sample_size} exceeds the golden dataset size of {len(golden_data)}."
        )

    sampled = random.Random(seed).sample(golden_data, sample_size)
    return sorted(sampled, key=lambda item: item["id"])


def write_jsonl(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


# =========================================================
# Judge LLM Helper Functions
# =========================================================
def save_answers(selected_version: str, answers: list[tuple], output_path: Path) -> None:
    rows = []
    for i, (question_id, question, model_answer, truth, source_quote, question_type) in enumerate(answers, start=1):
        rows.append(
            {
                "id": f"{selected_version}-answer-{i:04d}",
                "question_id": question_id,
                "question": question,
                "model_answer": model_answer,
                "truth": truth,
                "source_quote": source_quote,
                "type": question_type,
            }
        )

    write_jsonl(rows, output_path)


def save_eval(selected_version: str, evaluations: list[dict], output_path: Path) -> None:
    rows = []
    for i, evaluation in enumerate(evaluations, start=1):
        rows.append(
            {
                "id": f"{selected_version}-eval-{i:04d}",
                **evaluation,
            }
        )

    write_jsonl(rows, output_path)


def gather_answers(selected_version: str, sampled_cases: list[dict], output_path: Path) -> list[tuple]:
    workflow_fn, workflow_input_cls = WORKFLOWS[selected_version]

    answers = []
    for case in sampled_cases:
        workflow_input = workflow_input_cls(
            input_as_text=case["question"],
            conversation_history=None,
        )

        result = run_async(workflow_fn(workflow_input))
        model_answer = extract_reply(result)

        answers.append((case["id"], case["question"], model_answer, case["truth"], case["source_quote"], case["type"]))

    save_answers(selected_version, answers, output_path)
    return answers

# =========================================================
# Judge LLM Evaluation Function
# =========================================================
def run_judge(answers: list[tuple]) -> list[dict]:
    judge_instructions = get_judge_instructions()
    evaluation_results = []

    for answer in answers:
        question_id, question, model_answer, truth, source_quote, question_type = answer

        case_input = f"""
        Question: {question}
        Model Answer: {model_answer}
        Ground Truth: {truth}
        Source Quote: {source_quote}
        Question Type: {question_type}
        """

        response = client.responses.create(
            model="gpt-4o",
            instructions=judge_instructions,
            input=case_input,
            max_output_tokens=400,
            temperature=0.0,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "judge_output",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "correctness": {"type": "integer", "minimum": 0, "maximum": 5},
                            "grounding": {"type": "integer", "minimum": 0, "maximum": 5},
                            "hallucination": {"type": "boolean"},
                            "reasoning": {"type": "string", "minLength": 1},
                        },
                        "required": ["correctness", "grounding", "hallucination", "reasoning"],
                        "additionalProperties": False,
                    },
                }
            },
        )

        judge_result = json.loads(response.output_text)
        evaluation_results.append(
            {
                "question_id": question_id,
                "question": question,
                "model_answer": model_answer,
                "truth": truth,
                "source_quote": source_quote,
                "type": question_type,
                "judge_result": judge_result,
            }
        )

    return evaluation_results


# =========================================================
# Main
# =========================================================
def main() -> None:
    golden_data = load_golden_data()
    sampled_cases = pick_sample(golden_data, sample_size=DEFAULT_SAMPLE_SIZE, seed=DEFAULT_SEED)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_root = OUTPUTS_DIR / "judge_calibration" / run_id

    manifest = {
        "run_id": run_root.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": DEFAULT_SEED,
        "sample_size": DEFAULT_SAMPLE_SIZE,
        "versions": list(VERSIONS),
        "sampled_question_ids": [case["id"] for case in sampled_cases],
    }

    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_jsonl(sampled_cases, run_root / "sample.jsonl")

    for version in VERSIONS:
        version_root = run_root / version
        answers = gather_answers(version, sampled_cases, version_root / "answers.jsonl")
        evaluations = run_judge(answers)
        save_eval(version, evaluations, version_root / "judge_results.jsonl")

    print(f"Calibration run complete. Results saved to: {run_root}")


if __name__ == "__main__":
    main()