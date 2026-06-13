import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# =========================================================
# Path Setup & Client Initialization
# =========================================================
SRC_DIR = Path(__file__).resolve().parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

from evaluation.judge.judge_instructions import get_judge_instructions
from user_interface.async_runner import run_async
from user_interface.workflows.V0workflow import run_workflow as run_v0, WorkflowInput as V0Input
from user_interface.workflows.V1workflow import run_workflow as run_v1, WorkflowInput as V1Input
from user_interface.workflows.V2workflow import run_workflow as run_v2, WorkflowInput as V2Input

# =========================================================
# Data Paths
# =========================================================
GOLDEN_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "golden.jsonl"
OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# Workflow Registry
# =========================================================
WORKFLOWS = {
    "V0": (run_v0, V0Input),
    "V1": (run_v1, V1Input),
    "V2": (run_v2, V2Input),
}

# =========================================================
# Judge LLM Helper Functions
# =========================================================
def load_golden_data() -> list[dict]:
    """
    Load the golden dataset from disk.

    Returns:
        A list of dictionaries, one per JSONL line in the golden dataset.
    """
    golden_data = []
    with open(GOLDEN_DATA_PATH, "r") as f:
        for line in f:
            golden_data.append(json.loads(line))

    return golden_data


def extract_reply(result: dict) -> str:
    """
    Extract the assistant's text output from a workflow result.

    Args:
        result: Workflow result dictionary.

    Returns:
        The assistant's output text, or a fallback message if unavailable.
    """
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    return "I couldn't process that request. Please try again."


def save_answers(selected_version: str, answers: list[tuple], output_path: Path) -> None:
    """
    Save model answers to a JSONL file.

    Args:
        selected_version: Workflow version key.
        answers: List of tuples containing question metadata and model answers.
        output_path: Destination file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for i, (question, model_answer, truth, source_quote, type) in enumerate(answers, start=1):
            row = {
                "id": f"{selected_version}-answer-{i:04d}",
                "question": question,
                "model_answer": model_answer,
                "truth": truth,
                "source_quote": source_quote,
                "type": type,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def save_eval(selected_version: str, evaluations: list[str], output_path: Path) -> None:
    """
    Save judge evaluation results to a JSONL file.

    Args:
        selected_version: Workflow version key.
        evaluations: List of evaluation result objects.
        output_path: Destination file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for i, eval_result in enumerate(evaluations, start=1):
            row = {
                "id": f"{selected_version}-eval-{i:04d}",
                "evaluation": eval_result,
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def gather_answers(selected_version: str, timestamp: str) -> list:
    """
    Run a workflow version across the golden dataset and collect model answers.

    Args:
        selected_version: Workflow version key.
        timestamp: Timestamp string used for output file naming.

    Returns:
        A list of tuples containing question metadata and model answers.
    """
    print(f"Gathering answers for version {selected_version}...")

    workflow_fn, workflow_input_cls = WORKFLOWS[selected_version]

    answers = []
    golden_data = load_golden_data()

    for item in golden_data:
        question = item["question"]

        workflow_input = workflow_input_cls(
            input_as_text=question,
            conversation_history=None,
        )

        result = run_async(workflow_fn(workflow_input))
        model_answer = extract_reply(result)

        answers.append((question, model_answer, item["truth"], item["source_quote"], item["type"]))

    output_path = OUTPUTS_DIR / "answers" / f"{selected_version}" / f"{selected_version}_answers-{timestamp}.jsonl"
    save_answers(selected_version, answers, output_path)

    print("Answers have been gathered. Results saved to: " + str(output_path))

    return answers


# =========================================================
# Judge LLM Function
# =========================================================
def run_judge(answers: list, selected_version: str, timestamp: str) -> list:
    """
    Evaluate model answers using the Judge LLM.

    Args:
        answers: List of tuples containing question metadata and model answers.
        selected_version: Workflow version key.
        timestamp: Timestamp string used for output file naming.

    Returns:
        A list of structured judge evaluation results.
    """
    print("Running Judge LLM on the gathered answers...")

    evaluation_results = []
    for answer in answers:
        question, model_answer, truth, source_quote, type = answer

        judge_instructions = get_judge_instructions()

        case_input = f"""
        Question: {question}
        Model Answer: {model_answer}
        Ground Truth: {truth}
        Source Quote: {source_quote}
        Question Type: {type}
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

        result = json.loads(response.output_text)
        evaluation_results.append(result)

    output_path = OUTPUTS_DIR / "evaluations" / f"{selected_version}" / f"{selected_version}_eval-{timestamp}.jsonl"
    save_eval(selected_version, evaluation_results, output_path)

    print("Evaluation complete. Results saved to: " + str(output_path))
    
    return evaluation_results

# =========================================================
# Evaluation Dashboard Judge Runner
# =========================================================
def run_selected_version(selected_version):
    """
    Run the judge evaluation for a selected version and timestamp.

    Steps:
        1. Get workflow version.
        2. Gather model answers.
        3. Run judge evaluation.
        4. Save all outputs to disk.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    answers = gather_answers(selected_version, timestamp)
    
    return run_judge(answers, selected_version, timestamp)


# =========================================================
# Main Execution Function (For Testing Purposes)
# =========================================================
def main():
    """
    Run the evaluation pipeline for a single workflow version.

    Steps:
        1. Select workflow version.
        2. Gather model answers.
        3. Run judge evaluation.
        4. Save all outputs to disk.
    """
    selected_version = "V0"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    answers = gather_answers(selected_version, timestamp)
    run_judge(answers, selected_version, timestamp)


if __name__ == "__main__":
    main()