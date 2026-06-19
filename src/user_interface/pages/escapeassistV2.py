from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(layout="centered")

from user_interface.utils import render_escapeassist_page
from workflows.V2workflow import WorkflowInput


render_escapeassist_page(
    "V2",
    "My knowledge is based on the cleaned, preprocessed 2022 Ford Escape Owner's Manual.",
    WorkflowInput,
)