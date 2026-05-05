from docling.document_converter import DocumentConverter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

####################################################################
# Preprocessing Script for 2022 Ford Escape PDF
# V1: Basic Docling extraction to Markdown
# V2: Docling extraction + LLM cleanup (TOC removal, table repair)
####################################################################

# Load environment variables from .env and initialize OpenAI client
load_dotenv()

# Initialize OpenAI client with API key from environment
_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if _OPENAI_API_KEY:
    client = OpenAI(api_key=_OPENAI_API_KEY)
else:
    client = None
    print("WARNING: No OpenAI API key found. LLM cleanup will not run.\n" \
          "Either export OPENAI_API_KEY in your shell, source the .env file, or add the key to ~/.zshrc.")

####################################################################
# Setup and Initialization   
####################################################################

try:
    source = (
        Path(__file__).resolve().parent.parent
        / "documentation"
        / "data"
        / "2022-ford-Escape.pdf"
    )
    converter = DocumentConverter()
except Exception as e:
    print(f"Error initializing converter: {e}")

OUTPUT_DIR_V1 = Path(__file__).resolve().parent.parent / "preprocessing" / "v1_raw"
OUTPUT_DIR_V1.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR_V2 = Path(__file__).resolve().parent.parent / "preprocessing" / "v2_cleaned"
OUTPUT_DIR_V2.mkdir(parents=True, exist_ok=True)


####################################################################
# LLM Cleanup Helpers
####################################################################

def chunk_text(text: str, max_chars: int = 8000):
    """
    Split text into chunks without breaking Markdown tables.
    
    Rules:
    - Never split inside a table (lines starting with '|' or containing '|').
    - If a table is larger than max_chars, allow it to be its own chunk.
    - Otherwise, accumulate lines until adding another would exceed max_chars.
    """
    lines = text.splitlines(keepends=True)
    current_chunk = []
    current_length = 0
    inside_table = False

    def is_table_line(line: str) -> bool:
        stripped = line.strip()
        return stripped.startswith("|") or ("|" in stripped and "---" not in stripped)

    for line in lines:
        line_is_table = is_table_line(line)

        # Detect entering or exiting a table block
        if line_is_table and not inside_table:
            inside_table = True
        elif not line_is_table and inside_table:
            inside_table = False

        # If adding this line exceeds the limit AND we're not inside a table, start a new chunk
        if current_length + len(line) > max_chars and not inside_table:
            yield "".join(current_chunk)
            current_chunk = []
            current_length = 0

        current_chunk.append(line)
        current_length += len(line)

    # Yield the final chunk
    if current_chunk:
        yield "".join(current_chunk)


def llm_cleaning(raw_md: str) -> str:
    """
    Cleans Docling V2 Markdown using an LLM:
    - Removes Table of Contents
    - Fixes broken tables
    - Normalizes headings/lists
    - Preserves all real content
    """
    if client is None:
        raise RuntimeError("OpenAI client not configured. Set OPENAI_API_KEY or source .env before running.")

    cleaned_chunks = []

    for chunk in chunk_text(raw_md):
        prompt = f"""
            You are cleaning Markdown extracted from a PDF.

            Rules:
            1. Remove any Table of Contents sections. A TOC contains page numbers, dot leaders, or section listings.
            2. Fix broken tables. A valid Markdown table must have:
               - A header row
               - A separator row with dashes
               - Consistent column counts
            3. Preserve all real content. Do NOT remove warnings, notes, steps, lists, or headings.
            4. Do not rewrite or summarize. Only clean structure.
            5. Return ONLY cleaned Markdown with no explanations.

            Here is the Markdown to clean:
            {chunk}
            """

        response = client.responses.create(
            model="gpt-4o",
            input=prompt,
            temperature=0,
            max_output_tokens=3000
        )

        cleaned_chunks.append(response.output_text)
        print("Chunk cleaned and added to output.")

    print("All chunks processed. Combining cleaned Markdown.")

    return "\n".join(cleaned_chunks)


####################################################################
# Preprocessing Functions
####################################################################

def process_v1_data():
    """
    Extracts the PDF using Docling and saves the raw Markdown output.
    """
    try:
        result = converter.convert(source)
        doc = result.document

        raw_md = doc.export_to_markdown()

        output_path = OUTPUT_DIR_V1 / "2022-ford-Escape-raw.md"
        output_path.write_text(raw_md, encoding="utf-8")

        print(f"Version 1 (raw markdown) processed and saved to {OUTPUT_DIR_V1}")

    except Exception as e:
        print(f"Error processing version 1 (raw markdown): {e}")


def process_v2_data():
    """
    Runs Docling extraction, then cleans the Markdown using an LLM.
    Saves the cleaned output into v2_cleaned.
    """
    try:
        result = converter.convert(source)
        doc = result.document

        raw_md = doc.export_to_markdown()

        print("\nRunning LLM cleanup on extracted Markdown...")
        cleaned_md = llm_cleaning(raw_md)

        output_path = OUTPUT_DIR_V2 / "2022-ford-Escape-cleaned.md"
        output_path.write_text(cleaned_md, encoding="utf-8")

        print(f"Version 2 (LLM-cleaned markdown) saved to {output_path}")

    except Exception as e:
        print(f"Error processing version 2 (LLM-cleaned markdown): {e}")


####################################################################
# Main Execution Function
####################################################################

def main():
    """
    Runs the preprocessing pipeline.
    """
    while True:
        print("\n=== EscapeAssist Preprocessing Pipeline ===")
        print("1. Run Raw Extraction (V1)")
        print("2. Run LLM Cleaned Extraction (V2)")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ")

        if choice == "1":
            process_v1_data()
        elif choice == "2":
            process_v2_data()
        elif choice == "3":
            print("\nExiting program.\n")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()