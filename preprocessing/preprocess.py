from docling.document_converter import DocumentConverter
from pathlib import Path

####################################################################
# Preprocessing Script for 2022 Ford Escape PDF
# This script performs a single preprocessing pass on the source PDF:
# 1. Version 1 (V1): Raw Markdown extraction using Docling, with no cleanup or restructuring.
# After extraction, the user chooses whether to store the output in v1_raw or v2_sections.
#################################################################### 

####################################################################
# Setup and Initialization   
####################################################################

# Attempt to locate the source PDF and initialize the Docling converter.
# Wrapping this in a try/except keeps startup failure messages clear if the PDF is missing
# or Docling cannot initialize.
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

# Define the two available output directories.
# The user chooses which folder to save into at runtime.
OUTPUT_DIR_V1 = Path(__file__).resolve().parent.parent / "preprocessing" / "v1_raw"
OUTPUT_DIR_V1.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR_V2 = Path(__file__).resolve().parent.parent / "preprocessing" / "v2_sections"
OUTPUT_DIR_V2.mkdir(parents=True, exist_ok=True)


#####################################################################
# Preprocessing Functions
#####################################################################

def choose_output_dir():
    """
    Prompts the user to choose where the raw Markdown file should be saved.
    The labels match the existing v1_raw and v2_sections folders.

    Returns the selected output directory.
    """
    while True:
        print("\nWhere do you want to store the file?")
        print("1. v1_raw")
        print("2. v2_sections")

        choice = input("Select an option (1-2): ").strip()

        if choice == "1":
            return OUTPUT_DIR_V1
        if choice == "2":
            return OUTPUT_DIR_V2

        print("\nInvalid choice. Please try again.")


def process_raw_data():
    """
    Extracts the PDF using Docling and saves the raw Markdown output.

    This represents the preprocessing flow:
    - No cleanup
    - No restructuring
    - No manual review
    - Pure Docling output

    After extraction, the user chooses whether to save the file in v1_raw or v2_sections.
    """
    try:
        # Convert the PDF into Docling's internal structured representation.
        result = converter.convert(source)
        doc = result.document

        output_dir = choose_output_dir()

        # Export the raw Markdown exactly as Docling produces it.
        raw_md = doc.export_to_markdown()
        (output_dir / "2022-ford-Escape-raw.md").write_text(raw_md, encoding="utf-8")

        print(f"Version 1 (raw markdown) processed and saved to {output_dir}")
    except Exception as e:
        print(f"Error processing version 1 (raw markdown): {e}")


#####################################################################
# Main Execution Function
#####################################################################

def main():
    """
    Runs the raw Docling extraction and prompts for the save location.

    This function is the entry point for the preprocessing pipeline.
    """
    while True:
        print("\n=== EscapeAssist Preprocessing Pipeline ===")
        print("1. Run Raw Extraction")
        print("2. Exit")

        choice = input("\nSelect an option (1-2): ")

        if choice == "1":
            process_raw_data()
        elif choice == "2":
            print("\nExiting program.\n")
            break
        else:
            print("\nInvalid choice. Please try again.")
    


# Execute the preprocessing pipeline when the script is run directly.
if __name__ == "__main__":
    main()
