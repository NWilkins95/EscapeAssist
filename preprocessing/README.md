## Preprocessing Overview

Two preprocessing variants are available for extracting and processing the 2022 Ford Escape manual:

### 1. Raw Extraction (V1)
**What it does:**
- Uses Docling to extract the PDF directly to Markdown format
- Minimal processing — preserves the original PDF structure
- Fast (no LLM calls required)

**Output:** `v1_raw/2022-ford-Escape-raw.md`

**When to use:**
- Quick preview of the PDF content
- When you don't have an OpenAI API key
- As a baseline for comparison with V2

**Limitations:**
- May contain Table of Contents sections
- Broken or poorly formatted tables
- Less organized structure

### 2. LLM-Cleaned + Reorganized Extraction (V2)
**What it does:**
- Uses Docling to extract the PDF to Markdown
- Chunks the content intelligently (without breaking tables)
- **Pass 1 (Cleaning):** LLM removes TOC, fixes broken tables, normalizes formatting
- **Pass 2 (Reorganization):** LLM groups related content under logical headings
- Processes chunks in parallel (up to 8 concurrent API calls for speed)
- Combines all cleaned chunks back into a single organized document

**Output:** `v2_cleaned/2022-ford-Escape-organized.md`

**When to use:**
- Production-quality documentation for knowledge bases
- Training agents with clean, well-organized content
- When you need the best possible structure and readability

**Advantages:**
- TOC automatically removed
- Tables fixed and properly formatted
- Content logically organized by topic
- All original information preserved (no content loss)
- Significantly more readable than V1

**Requirements:**
- OpenAI API key in `.env` file
- Costs a few dollars per document (gpt-4o-mini model)
- Takes 2-5 minutes to process (depending on document size)

## User Guide
- [Click here](../documentation/user_guide/preprocessing.md) for the full guide on using this pipeline.

## Notes
This repository is private and used solely for academic purposes as part of the senior project requirements.