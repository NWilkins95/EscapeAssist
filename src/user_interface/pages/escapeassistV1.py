from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from user_interface.utils import render_escapeassist_page
from workflows.V1workflow import WorkflowInput


render_escapeassist_page(
    "V1",
    "My knowledge is based on the raw-preprocessed 2022 Ford Escape Owner's Manual.",
    WorkflowInput,
)