# EscapeAssist Preprocessing Pipeline — User Guide

Welcome to the EscapeAssist preprocessing pipeline! This guide walks you through using the tool to extract and clean PDF documentation into organized Markdown files.

---

## Table of Contents

1. [What This Tool Does](#what-this-tool-does)
2. [Prerequisites](#prerequisites)
3. [How to Run the Pipeline](#how-to-run-the-pipeline)
4. [Pipeline Versions](#pipeline-versions)
5. [Output Files](#output-files)
6. [Uploading Files to OpenAI Agent Dashboard](#uploading-files-to-openai-agent-dashboard)
7. [Troubleshooting](#troubleshooting)

---

## What This Tool Does

The EscapeAssist preprocessing pipeline takes a PDF document (currently the 2022 Ford Escape manual) and extracts it into clean, organized Markdown format. The pipeline offers two versions:

- **V1 (Raw Extraction):** Extracts the PDF to Markdown with minimal processing
- **V2 (LLM-Cleaned + Reorganized):** Uses OpenAI's LLM to clean up formatting, remove Table of Contents, fix broken tables, and reorganize content into logical sections

Both versions produce human-readable Markdown files that can be used as knowledge bases for agents or other applications.

---

## Prerequisites

Before running the pipeline, ensure you have:

1. **Python 3.10+** installed (this project uses Python 3.14.4)
2. **Required dependencies** installed:
   ```bash
   pip install docling openai python-dotenv
   ```
3. **OpenAI API Key** (for V2 processing):
   - Create an account at [OpenAI](https://openai.com)
   - Generate an API key from your account settings
   - Store it in a `.env` file in the repository root:
     ```
     export OPENAI_API_KEY=sk-your-key-here
     ```
4. **Source PDF** placed at:
   ```
   documentation/data/2022-ford-Escape.pdf
   ```

---

## How to Run the Pipeline

### Step 1: Navigate to the Repository Root

```bash
cd /path/to/EscapeAssist
```

### Step 2: Load Environment Variables

Load your `.env` file with the OpenAI API key:

```bash
set -a
source .env
set +a
```

Alternatively, you can run the script directly and it will auto-load the `.env` file using `python-dotenv`.

### Step 3: Run the Pipeline

```bash
python preprocessing/preprocess.py
```

### Step 4: Select a Version

You'll see an interactive menu:

```
=== EscapeAssist Preprocessing Pipeline ===
1. Run Raw Extraction (V1)
2. Run LLM Cleaned + Organized Extraction (V2)
3. Exit

Select an option (1-3):
```

- **Choose 1** for raw extraction (faster, no API calls)
- **Choose 2** for LLM-cleaned extraction (slower, requires OpenAI API key, produces better-organized output)

### Step 5: Processing

The pipeline will:
- Extract the PDF using Docling
- For V2: split content into chunks, clean and reorganize each chunk using OpenAI's API, then combine results
- Save the output to the appropriate folder

---

## Pipeline Versions

### Version 1 (Raw Extraction)

**Location:** `preprocessing/v1_raw/`

**Output:** `2022-ford-Escape-raw.md`

**Features:**
- Direct PDF-to-Markdown extraction using Docling
- Fast (no LLM processing)
- Preserves original PDF structure
- May contain formatting issues, Table of Contents, or broken tables

**Use case:** Quick preview, or when you don't have an OpenAI API key

### Version 2 (LLM-Cleaned + Organized)

**Location:** `preprocessing/v2_cleaned/`

**Output:** `2022-ford-Escape-organized.md`

**Features:**
- Two-pass LLM processing:
  - **Pass 1 (Cleaning):** Removes Table of Contents, fixes broken tables, normalizes formatting
  - **Pass 2 (Reorganization):** Groups related content under logical headings
- Chunks processed in parallel (up to 8 concurrent API calls)
- Preserves all original content (no information lost)
- Much more readable and structured output

**Use case:** Production-quality documentation for knowledge bases and agent training

**Note:** Requires an OpenAI API key and costs money (typically a few dollars per document)

---

## Output Files

After running the pipeline, you'll find:

```
preprocessing/
├── v1_raw/
│   └── 2022-ford-Escape-raw.md
└── v2_cleaned/
    └── 2022-ford-Escape-organized.md
```

Both files are standard Markdown (.md) and can be opened in any text editor or Markdown viewer.

---

## Uploading Files to OpenAI Agent Dashboard

Once you've generated your Markdown files, you can upload them to OpenAI to train your agents.

### Steps to Upload:

1. **Log into OpenAI Platform**
   - Go to [https://platform.openai.com](https://platform.openai.com)
   - Sign in with your account

2. **Navigate to Your Project**
   - Click on your project from the dashboard
   - Find the "Agents" or "Files" section (exact location may vary based on OpenAI updates)

3. **Upload the Markdown File**
   - Click "Upload" or "Add File"
   - Select your generated Markdown file:
     - `preprocessing/v1_raw/2022-ford-Escape-raw.md` (for raw output), or
     - `preprocessing/v2_cleaned/2022-ford-Escape-organized.md` (recommended)
   - Confirm the upload

4. **Associate File with Agent**
   - After uploading, attach the file to your agent's knowledge base
   - This enables the agent to reference the Ford Escape manual when answering user queries

5. **Test Your Agent**
   - Ask the agent questions about the Ford Escape
   - Verify that it correctly references information from the uploaded file

### Best Practices:

- **Use V2 output** (`v2_cleaned`) for best results — the organized structure helps agents understand content better
- **Keep file names descriptive** — include the document title and version
- **Test after upload** — verify your agent can access and reference the content
- **Update regularly** — if you have new or corrected source PDFs, regenerate and re-upload

---

## Troubleshooting

### Error: "No OpenAI API key found"

**Solution:** Ensure your `.env` file exists in the repository root and contains:
```
export OPENAI_API_KEY=sk-your-actual-key
```

Then source it before running:
```bash
set -a
source .env
set +a
python preprocessing/preprocess.py
```

### Error: "PDF file not found"

**Solution:** Verify the source PDF is at:
```
documentation/data/2022-ford-Escape.pdf
```

If it's in a different location, update the `source` path in `preprocessing/preprocess.py` (around line 32).

### V2 Processing is Very Slow

**Reason:** LLM API calls take time (5–20 seconds per chunk). The pipeline processes up to 8 chunks in parallel.

**Mitigation:**
- Be patient — a typical document takes 2–5 minutes for V2 processing
- Reduce the number of parallel workers in `preprocessing/preprocess.py` if you hit rate limits (change `max_workers=8` to a lower number)

### Blank or Corrupted Output File

**Cause:** The LLM may have had issues processing a specific chunk.

**Solution:**
- Try running again (LLM responses can vary)
- If persistent, try V1 extraction first to ensure the PDF is readable
- Check your OpenAI account for API errors at [https://platform.openai.com/account/usage/overview](https://platform.openai.com/account/usage/overview)

---

## Questions?

For more information about the preprocessing code, see `preprocessing/preprocess.py` (well-commented) or contact the project maintainer.

Happy preprocessing! 🎉