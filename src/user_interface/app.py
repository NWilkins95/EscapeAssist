import streamlit as st

# Define pages
home = st.Page("home.py", title="Home", icon="🏠")
escapeassistV0 = st.Page("escapeassistV0.py", title="EscapeAssist V0", icon="🚗")
escapeassistV1 = st.Page("escapeassistV1.py", title="EscapeAssist V1", icon="🚓")
escapeassistV2 = st.Page("escapeassistV2.py", title="EscapeAssist V2", icon="🚙")

# Navigation
nav = st.navigation([home, escapeassistV0, escapeassistV1, escapeassistV2])
nav.run()
