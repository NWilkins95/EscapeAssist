import streamlit as st
import asyncio
import time
from dotenv import load_dotenv

load_dotenv()

from workflows.V1workflow import run_workflow, WorkflowInput


def extract_reply(result: dict) -> str:
    # Normal assistant output
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    # Guardrail failure
    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    # Unknown failure
    return "I couldn't process that request. Please try again."


st.image("assets/IMG_4865.jpeg")
st.header("Welcome to EscapeAssist V1!")
st.markdown("My knowledge is based on the raw-preprocessed 2022 Ford Escape Owner's Manual.")
st.markdown("Ask me anything about your 2022 Ford Escape, and I'll do my best to assist you!")

if "messages_v1" not in st.session_state:
    st.session_state.messages_v1 = []

if "conversation_history_v1" not in st.session_state:
    st.session_state.conversation_history_v1 = []

# Display chat history
for msg in st.session_state.messages_v1:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask about your Ford Escape...")

if prompt:
    st.session_state.messages_v1.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pass the previous conversation history (as plain dicts) to the workflow
    workflow_input = WorkflowInput(
        input_as_text=prompt,
        conversation_history=st.session_state.conversation_history_v1 or None
    )
    result = asyncio.run(run_workflow(workflow_input))

    # Store the updated conversation history from the workflow response
    if "conversation_history" in result:
        st.session_state.conversation_history_v1 = result["conversation_history"]

    reply = extract_reply(result)

    st.session_state.messages_v1.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        with st.spinner("EscapeAssist is thinking..."):
            result = asyncio.run(run_workflow(workflow_input))
    
        reply = extract_reply(result)
    
        placeholder = st.empty()
        typed = ""
        for char in reply:
            typed += char
            placeholder.markdown(typed)
            time.sleep(0.01)