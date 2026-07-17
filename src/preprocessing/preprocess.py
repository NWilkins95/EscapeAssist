from docling.document_converter import DocumentConverter
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import llm_cleaning

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
    print(
        "WARNING: No OpenAI API key found. LLM cleanup will not run.\n"
        "Either export OPENAI_API_KEY in your shell, source .env, or add the key to ~/.zshrc."
    )

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
# Preprocessing Functions
# ===================================================================

def process_v1_data():
    """
    Run Docling extraction and save the raw Markdown output (Version 1).

    Extracts the PDF, converts it to Markdown, and writes the unmodified
    Markdown to the v1_raw directory.
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
    Run Docling extraction followed by LLM cleanup and reorganization (Version 2).

    Steps:
        1. Extract raw Markdown using Docling.
        2. Clean and reorganize the Markdown using chunked LLM passes.
        3. Save the final organized Markdown to the v2_cleaned directory.
    """
    try:
        result = converter.convert(source)
        doc = result.document

        raw_md = doc.export_to_markdown()

        print("\nRunning LLM cleanup + reorganization on extracted Markdown...")
        final_md = llm_cleaning(raw_md, client)

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
    Run the preprocessing pipeline interactively.

    Allows the user to:
        1. Run raw extraction (V1)
        2. Run LLM-cleaned extraction (V2)
        3. Exit the program
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
