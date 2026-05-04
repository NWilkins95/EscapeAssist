from docling.document_converter import DocumentConverter
from pathlib import Path

# Define the source PDF document and initialize the converter
try:
    source = Path(__file__).resolve().parent.parent / "documentation" / "data" / "2022-ford-Escape.pdf"
    converter = DocumentConverter()
except Exception as e:
    print(f"Error initializing converter: {e}")

# Create output directories if they don't exist and define output paths
OUTPUT_DIR_V1 = Path(__file__).resolve().parent.parent / "preprocessing" / "v1_raw"
OUTPUT_DIR_V1.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR_V2 = Path(__file__).resolve().parent.parent / "preprocessing" / "v2_sections"
OUTPUT_DIR_V2.mkdir(parents=True, exist_ok=True)

# Process the PDF document for version 1 (raw text)
def process_v1_raw():
    try:
        # Convert the PDF document to a structured format
        result = converter.convert(source)
        doc = result.document
    
        # Export raw markdown
        raw_md = doc.export_to_markdown()
        (OUTPUT_DIR_V1 / "2022-ford-Escape-raw.md").write_text(raw_md, encoding="utf-8")

        print(f"Version 1 (raw text) processed and saved to {OUTPUT_DIR_V1}")
    except Exception as e:        
        print(f"Error processing version 1 (raw text): {e}")

def process_v2_sections():
    print("Implementation will come later")

def main():
    process_v1_raw()

# run the main function to execute the preprocessing    
if __name__ == "__main__":
    main()