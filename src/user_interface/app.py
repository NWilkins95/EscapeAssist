import streamlit as st
import asyncio
from dotenv import load_dotenv

load_dotenv()

from workflows.V0workflow import run_workflow, WorkflowInput


def extract_reply(result: dict) -> str:
    # Normal assistant output
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    # Guardrail failure
    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    # Unknown structure
    return "I couldn't process that request. Please try again."


st.title("EscapeAssist")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about your Ford Escape...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    workflow_input = WorkflowInput(input_as_text=prompt)
    result = asyncio.run(run_workflow(workflow_input))

    reply = extract_reply(result)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
