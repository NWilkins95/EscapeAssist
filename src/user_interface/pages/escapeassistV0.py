import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()

from async_runner import run_async
from workflows.V0workflow import run_workflow, WorkflowInput


def extract_reply(result: dict) -> str:
    """
    Extract the assistant's output text from a workflow result.

    This function inspects the workflow response payload and returns the
    assistant's generated text when available. If the result indicates a
    safety‑filter trigger, a user‑friendly message is returned instead.
    Otherwise, a generic fallback message is provided.

    Args:
        result: The workflow result dictionary returned by a workflow run.

    Returns:
        The assistant's output text, a safety‑filter message, or a fallback
        error message when no valid output is present.
    """
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    return "I couldn't process that request. Please try again."


# ========================================================
# Cache the workflow 
# ========================================================
@st.cache_resource
def load_workflow():
    """
    Cache the V0 workflow function for Streamlit.
    """
    return run_workflow


workflow = load_workflow()


# ========================================================
# UI Setup
# ========================================================
st.image("assets/IMG_4865.jpeg")
st.header("Welcome to EscapeAssist V0!")
st.markdown("My knowledge is based on the auto-ingested 2022 Ford Escape Owner's Manual.")
st.markdown("Ask me anything about your 2022 Ford Escape, and I'll do my best to assist you!")

if "messages_v0" not in st.session_state:
    st.session_state.messages_v0 = []

if "conversation_history_v0" not in st.session_state:
    st.session_state.conversation_history_v0 = []


# Chat history
for msg in st.session_state.messages_v0:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================================================
# Handle new user input
# =========================================================
prompt = st.chat_input("Ask about your Ford Escape...")

if prompt:
    # Add user message to UI
    st.session_state.messages_v0.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build workflow input
    workflow_input = WorkflowInput(
        input_as_text=prompt,
        conversation_history=st.session_state.conversation_history_v0 or None
    )

    # Run workflow using shared async loop
    with st.chat_message("assistant"):
        with st.spinner("EscapeAssist is thinking..."):
            result = run_async(workflow(workflow_input))

        reply = extract_reply(result)

        # Typewriter effect
        placeholder = st.empty()
        typed = ""
        for char in reply:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.01)

    # Update conversation history
    if "conversation_history" in result:
        st.session_state.conversation_history_v0 = result["conversation_history"]

    # Add to UI history
    st.session_state.messages_v0.append({"role": "assistant", "content": reply})