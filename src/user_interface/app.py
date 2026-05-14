import streamlit as st

# Pages
home = st.Page("pages/home.py", title="Home", icon="🏠")
escapeassistV0 = st.Page("pages/escapeassistV0.py", title="EscapeAssist V0", icon="🚗")
escapeassistV1 = st.Page("pages/escapeassistV1.py", title="EscapeAssist V1", icon="🚓")
escapeassistV2 = st.Page("pages/escapeassistV2.py", title="EscapeAssist V2", icon="🚙")
evaluation_dashboard = st.Page("pages/evaluation_dashboard.py", title="Evaluation Dashboard", icon="🧪")

# Navigation
nav = st.navigation([home, escapeassistV0, escapeassistV1, escapeassistV2, evaluation_dashboard])
nav.run()
