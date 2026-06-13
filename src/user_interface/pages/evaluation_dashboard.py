import streamlit as st
import pandas as pd

st.image("assets/IMG_4854.png")

st.title("Evaluation Dashboard")

V0_tab, V1_tab, V2_tab = st.tabs(["V0", "V1", "V2"])

with V0_tab:
    st.header("V0")
    st.write("Content for V0")

with V1_tab:
    st.header("V1")
    st.write("Content for V1")

with V2_tab:
    st.header("V2")
    st.write("Content for V2")

