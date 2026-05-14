from docling.document_converter import DocumentConverter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os

# =================================================================
# Preprocessing Script for 2022 Ford Escape PDF
# V1: Basic Docling extraction to Markdown
# V2: Docling extraction + LLM cleanup + LLM reorganization (chunked)
# =================================================================

# Load environment variables from .env and initialize OpenAI client
load_dotenv()

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if _OPENAI_API_KEY:
    client = OpenAI(api_key=_OPENAI_API_KEY)
else:
    client = None
    print("WARNING: No OpenAI API key found. LLM cleanup will not run.\n"
          "Either export OPENAI_API_KEY in your shell, source .env, or add the key to ~/.zshrc.")

# ===================================================================
# Setup and Initialization   
# ===================================================================

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

# ===================================================================
# Chunking Helper
# ===================================================================

def chunk_text(text: str, max_chars: int = 8000):
    """
    Split text into chunks without breaking Markdown tables.
    This is important because LLM processing can mangle tables if they're split mid-table.
    Strategy: track whether we're inside a table, and never split while inside_table=True.
    """
    lines = text.splitlines(keepends=True)
    current_chunk = []
    current_length = 0
    inside_table = False

    def is_table_line(line: str) -> bool:
        # Treat pipe-delimited lines as table content.
        stripped = line.strip()
        return stripped.startswith("|") or ("|" in stripped and "---" not in stripped)

    for line in lines:
        line_is_table = is_table_line(line)

        if line_is_table and not inside_table:
            inside_table = True
        elif not line_is_table and inside_table:
            inside_table = False

        if current_length + len(line) > max_chars and not inside_table:
            yield "".join(current_chunk)
            current_chunk = []
            current_length = 0

        current_chunk.append(line)
        current_length += len(line)

    if current_chunk:
        yield "".join(current_chunk)

# ===================================================================
# LLM Cleanup + Reorganization (Integrated)
# ===================================================================

def llm_cleaning(raw_md: str) -> str:
    """
    Cleans and reorganizes Markdown using two LLM passes per chunk:
    1. Cleanup pass (TOC removal, table repair, normalization)
    2. Reorganization pass (grouping into logical sections)
    """

    if client is None:
        raise RuntimeError("OpenAI client not configured. Set OPENAI_API_KEY or source .env before running.")

    chunks = list(chunk_text(raw_md))
    print(f"Total chunks: {len(chunks)}")

    def process_chunk(idx, chunk):
        cleaning_prompt = f"""
            You are cleaning text extracted from a PDF.

            Rules:
            1. Remove any Table of Contents sections.
            2. Fix broken Markdown tables.
            3. Preserve ALL real content exactly as written.
            4. Do NOT interpret the text.
            5. Do NOT hallucinate or invent content.
            6. Maintain Markdown formatting.
            7. Return ONLY cleaned Markdown.
            8. Do NOT wrap the output in triple backtick code fences.

            Here is the chunk to clean:
            {chunk}
            """

        cleaning_response = client.responses.create(
            model="gpt-4o-mini",
            input=cleaning_prompt,
            temperature=0,
            max_output_tokens=3000
        )

        cleaned = cleaning_response.output_text

        reorganize_prompt = f"""
            You will reorganize a Markdown document into clean, logical sections.

            Rules:
            1. Do NOT rewrite, summarize, shorten, or expand any content.
            2. Preserve ALL text exactly as written.
            3. Group related content under consistent headings.
            4. Normalize headings if needed (e.g., use ## for major sections).
            5. Do NOT remove warnings, notes, steps, lists, or tables.
            6. Do NOT hallucinate or add new content.
            7. Maintain valid Markdown formatting.
            8. Do NOT wrap the output in triple backtick code fences.

            Here is the cleaned Markdown to reorganize:
            {cleaned}
            """

        reorganize_response = client.responses.create(
            model="gpt-4o-mini",
            input=reorganize_prompt,
            temperature=0,
            max_output_tokens=3000
        )

        organized = reorganize_response.output_text

        print(f"Chunk {idx+1}/{len(chunks)} cleaned + reorganized")
        return idx, organized

    processed_chunks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(process_chunk, idx, chunk)
            for idx, chunk in enumerate(chunks)
        ]
        for future in as_completed(futures):
            processed_chunks.append(future.result())

    processed_chunks.sort(key=lambda x: x[0])
    ordered = [c for _, c in processed_chunks]

    print("All chunks processed. Combining final Markdown.")
    return "\n".join(ordered)

# ===================================================================
# Preprocessing Functions
# ===================================================================

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
    Runs Docling extraction, then performs:
    - Chunked LLM cleanup
    - Chunked LLM reorganization
    Saves the final output into v2_cleaned.
    """
    try:
        result = converter.convert(source)
        doc = result.document

        raw_md = doc.export_to_markdown()

        print("\nRunning LLM cleanup + reorganization on extracted Markdown...")
        final_md = llm_cleaning(raw_md)

        output_path = OUTPUT_DIR_V2 / "2022-ford-Escape-organized.md"
        output_path.write_text(final_md, encoding="utf-8")

        print(f"Version 2 (LLM-cleaned + reorganized markdown) saved to {output_path}")

    except Exception as e:
        print(f"Error processing version 2 (LLM-cleaned markdown): {e}")

# ===================================================================
# Main Execution Function
# ===================================================================

def main():
    """
    Runs the preprocessing pipeline.
    """
    while True:
        print("\n=== EscapeAssist Preprocessing Pipeline ===")
        print("1. Run Raw Extraction (V1)")
        print("2. Run LLM Cleaned + Organized Extraction (V2)")
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