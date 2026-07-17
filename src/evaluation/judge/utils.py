import json
from pathlib import Path


GOLDEN_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "golden.jsonl"


def load_golden_data() -> list[dict]:
    """
    Load the golden dataset from disk.

    Returns:
        A list of dictionaries, one per JSONL line in the golden dataset.
    """
    golden_data = []
    with open(GOLDEN_DATA_PATH, "r", encoding="utf-8") as f:
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


def write_jsonl(rows: list[dict], output_path: Path) -> None:
    """
    Write a list of dictionaries to a JSONL file.

    Args:
        rows: List of dicts to write.
        output_path: Destination file path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")