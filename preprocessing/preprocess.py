from docling.document_converter import DocumentConverter
from pathlib import Path

####################################################################
# Preprocessing Script for 2022 Ford Escape PDF
# This script performs two stages of preprocessing on the source PDF:
# 1. Version 1 (V1): Raw Markdown extraction using Docling, with no cleanup or restructuring.
# 2. Version 2 (V2): Section-aware Markdown extraction, grouping content under detected headings.   
#################################################################### 

####################################################################
# Setup and Initialization   
####################################################################

# Attempt to locate the source PDF and initialize the Docling converter.
# Wrapping this in a try/except ensures the script fails gracefully if the file is missing
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

# Define output directories for V1 (raw extraction) and V2 (section-aware extraction).
# These directories are created if they do not already exist.
OUTPUT_DIR_V1 = Path(__file__).resolve().parent.parent / "preprocessing" / "v1_raw"
OUTPUT_DIR_V1.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR_V2 = Path(__file__).resolve().parent.parent / "preprocessing" / "v2_sections"
OUTPUT_DIR_V2.mkdir(parents=True, exist_ok=True)


#####################################################################
# Preprocessing Functions
#####################################################################

def process_v1_raw():
    """
    Extracts the PDF using Docling and saves the **raw Markdown output**.

    This represents Version 1 (V1) of the preprocessing pipeline:
    - No cleanup
    - No restructuring
    - No manual review
    - Pure Docling output

    The purpose of V1 is to serve as a baseline for comparison against:
    - V0 (Foundry extraction)
    - V2 (cleaned, section-aware extraction)
    """
    try:
        # Convert the PDF into Docling's internal structured representation.
        result = converter.convert(source)
        doc = result.document

        # Export the raw Markdown exactly as Docling produces it.
        raw_md = doc.export_to_markdown()
        (OUTPUT_DIR_V1 / "2022-ford-Escape-raw.md").write_text(raw_md, encoding="utf-8")

        print(f"Version 1 (raw markdown) processed and saved to {OUTPUT_DIR_V1}")
    except Exception as e:
        print(f"Error processing version 1 (raw markdown): {e}")


def process_v2_sections():
    """
    Extracts the PDF using Docling and restructures the output into
    **section-aware Markdown**, grouped by detected headings.

    This represents Version 2 (V2) of the preprocessing pipeline:
    - Headings are used to split the document into logical sections
    - Content under each heading is grouped together
    - Output is cleaner and more RAG-friendly than V1
    - Still automated (no manual cleanup yet)

    This version is intended to:
    - Improve retrieval quality
    - Reduce hallucinations caused by mixed or noisy chunks
    - Provide a more structured dataset for ingestion
    """
    try:
        # Convert the PDF into Docling's structured representation.
        result = converter.convert(source)
        doc = result.document

        sections = []
        current_section = None

        # Iterate through Docling items (headings, paragraphs, tables, etc.)
        # and group content under the most recent heading.
        for item in doc.iterate_items():
            if item.type == "heading":
                # When a new heading is found, store the previous section.
                if current_section:
                    sections.append(current_section)
                current_section = {"heading": item.text, "content": []}
            elif current_section is not None:
                # Append any non-heading content to the current section.
                current_section["content"].append(item.text)

        # Append the final section if one exists.
        if current_section:
            sections.append(current_section)

        # Build Markdown output: each section becomes a top-level heading
        # followed by its grouped content.
        sectioned_md = "\n\n".join(
            f"# {section['heading']}\n\n" + "\n\n".join(section["content"])
            for section in sections
        )

        (OUTPUT_DIR_V2 / "2022-ford-Escape-sections.md").write_text(
            sectioned_md, encoding="utf-8"
        )

        print(f"Version 2 (sectioned markdown) processed and saved to {OUTPUT_DIR_V2}")
    except Exception as e:
        print(f"Error processing version 2 (sectioned markdown): {e}")


#####################################################################
# Main Execution Function
#####################################################################

def main():
    """
    Runs both preprocessing stages:
    - V1: Raw Docling extraction
    - V2: Section-aware Docling extraction

    This function is the entry point for the preprocessing pipeline.
    """
    process_v1_raw()
    process_v2_sections()


# Execute the preprocessing pipeline when the script is run directly.
if __name__ == "__main__":
    main()
