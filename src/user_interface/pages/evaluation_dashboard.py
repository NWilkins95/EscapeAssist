from pathlib import Path
import streamlit as st


# =========================================================
# Path Setup & Page Initialization
# =========================================================
PAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PAGE_DIR.parents[1]
import sys

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from user_interface.utils import (
    render_evaluation_dashboard,
)

OUTPUTS_DIR = SRC_DIR / "evaluation" / "outputs"
ANSWERS_DIR = OUTPUTS_DIR / "answers"
EVALUATIONS_DIR = OUTPUTS_DIR / "evaluations"
VERSIONS = ["V0", "V1", "V2"]


st.set_page_config(page_title="Evaluation Dashboard", layout="wide")
st.title("Evaluation Dashboard")

render_evaluation_dashboard(ANSWERS_DIR, EVALUATIONS_DIR, VERSIONS)
