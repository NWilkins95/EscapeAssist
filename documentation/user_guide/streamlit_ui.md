# EscapeAssist Streamlit UI Guide

This guide explains how to use the EscapeAssist Streamlit application.

## What The App Contains

The Streamlit app includes five pages:

- Home
- EscapeAssist V0
- EscapeAssist V1
- EscapeAssist V2
- Evaluation Dashboard

The V0, V1, and V2 pages let you chat with the three workflow variants. The dashboard page lets you inspect evaluation runs and compare their metrics.

## Prerequisites

Before launching the app, make sure you have:

- Python and the project dependencies installed
- A `.env` file if you want V2 to use OpenAI-backed cleanup behavior
- The repository opened at the project root

## How To Launch The App

From the repository root, run Streamlit against the main app entry point:

```bash
streamlit run src/user_interface/app.py
```

Streamlit will open the app in your browser and show the navigation menu in the top-left corner.

## Page Overview

### Home

The Home page is a landing page with the project image and a short pointer to the navigation menu.

### EscapeAssist V0

V0 uses the auto-ingested version of the Ford Escape manual.

### EscapeAssist V1

V1 uses the raw-preprocessed manual output.

### EscapeAssist V2

V2 uses the cleaned and reorganized manual output.

### Evaluation Dashboard

The dashboard page is for reviewing evaluation outputs, not for chatting with the manual.

## Typical Workflow

1. Open the Home page and confirm the app loads correctly.
2. Open V0, V1, or V2 and ask a question about the manual.
3. Switch between versions to compare answer style and grounding.
4. Open the Evaluation Dashboard to review saved runs and exported results.

## Tips

- Use the same question across V0, V1, and V2 when comparing behavior.
- Treat V0 as the auto-ingestion baseline, V1 as the raw preprocessing version, and V2 as the cleaned preprocessing version.
- If the app does not load, check the environment setup and confirm the expected files exist under `src/user_interface/`.