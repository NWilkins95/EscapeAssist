from pathlib import Path
import sys

# =========================================================
# Path Setup
# =========================================================
SRC_DIR = Path(__file__).resolve().parents[2]
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from evaluation.judge.judge_instructions import get_judge_instructions
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

# =========================================================
# Workflow Imports
# =========================================================
from user_interface.async_runner import run_async
from user_interface.workflows.V0workflow import run_workflow as run_v0, WorkflowInput as V0Input
from user_interface.workflows.V1workflow import run_workflow as run_v1, WorkflowInput as V1Input
from user_interface.workflows.V2workflow import run_workflow as run_v2, WorkflowInput as V2Input

# =========================================================
# Data Paths
# =========================================================
GOLDEN_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "golden_v1.jsonl"

# =========================================================
# Workflow Registry
# =========================================================
WORKFLOWS = {
    "V0": (run_v0, V0Input),
    "V1": (run_v1, V1Input),
    "V2": (run_v2, V2Input),
}

# =========================================================
# Judge LLM Functions
# =========================================================
def extract_reply(result: dict) -> str:
    """
    Return the assistant text from a workflow result payload.
    """
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    return "I couldn't process that request. Please try again."

def load_golden_data() -> list[dict]:
    """
    Load the golden dataset from JSONL into a list of dictionaries.
    """
    golden_data = []
    with open(GOLDEN_DATA_PATH, "r") as f:
        for line in f:
            golden_data.append(json.loads(line))
    return golden_data

def gather_answers(selected_version: str) -> list:
    """
    Run the selected workflow over the golden dataset and collect model answers.
    """

    print(f"Gathering answers for version {selected_version}...")

    workflow_fn, workflow_input_cls = WORKFLOWS[selected_version]

    answers = []
    golden_data = load_golden_data()

    five_gathered = False

    for item in golden_data:
        question = item["question"]

        workflow_input = workflow_input_cls(
            input_as_text=question,
            conversation_history=None,
        )

        result = run_async(workflow_fn(workflow_input))
        model_answer = extract_reply(result)

        answers.append((question, model_answer, item["truth"], item["source_quote"], item["type"]))

        if len(answers) >= 5 and not five_gathered:
            print("Gathered 5 answers, stopping early for testing purposes.")
            five_gathered = True

            break

    print(f"Gathered {len(answers)} answers from the model for version {selected_version}.")

    return answers

def run_judge(answers: list) -> None:
    """
    Send each answer pair to the Judge LLM and print the structured response.
    """

    print("Running Judge LLM on the gathered answers...")

    for answer in answers:
        question = answer[0]
        model_answer = answer[1]
        truth = answer[2]
        source_quote = answer[3]
        type = answer[4]

        judge_instructions = get_judge_instructions()

        case_input = f"""
        Question: {question}
        Model Answer: {model_answer}
        Ground Truth: {truth}
        Source Quote: {source_quote}
        Question Type: {type}
        """
    
        # Send the prompt to the Judge LLM and parse the response
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
                            "reasoning": {"type": "string", "minLength": 1}
                        },
                        "required": ["correctness", "grounding", "hallucination", "reasoning"],
                        "additionalProperties": False
                    }
                }
            }
        )

        raw_text = response.output[0].content[0].text
        print(raw_text)

def main():

    selected_version = "V1"
    answers = gather_answers(selected_version)
    run_judge(answers)


if __name__ == "__main__":
    main()