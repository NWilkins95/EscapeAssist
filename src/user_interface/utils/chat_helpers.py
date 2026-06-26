import time

import streamlit as st

from user_interface.utils.async_runner import run_async


def extract_reply(result: dict) -> str:
    """
    Extract the assistant's output text from a workflow result.

    Args:
        result: The workflow result dictionary.

    Returns:
        The assistant's output text, a safety-filter message, or a fallback message.
    """
    if "assistant" in result and "output_text" in result["assistant"]:
        return result["assistant"]["output_text"]

    if any(key in result for key in ["nsfw", "moderation", "jailbreak", "pii", "prompt_injection"]):
        return "Your message triggered a safety filter. Please try rephrasing."

    return "I couldn't process that request. Please try again."


def load_workflow(version: str) -> callable:
    """
    Return the requested workflow function.

    Args:
        version: Workflow version key.

    Returns:
        The run_workflow callable for the requested version.
    """
    from user_interface.workflows.V0workflow import run_workflow as run_v0
    from user_interface.workflows.V1workflow import run_workflow as run_v1
    from user_interface.workflows.V2workflow import run_workflow as run_v2

    workflows = {
        "V0": run_v0,
        "V1": run_v1,
        "V2": run_v2,
    }
    return workflows[version]


def render_escapeassist_page(version, knowledge_text, workflow_input_cls):
    """
    Render one EscapeAssist chat page.

    Args:
        version: Workflow version key.
        knowledge_text: Short description of the knowledge source shown on the page.
        workflow_input_cls: WorkflowInput class for the selected version.
    """
    workflow = load_workflow(version)
    message_key = f"messages_{version.lower()}"
    history_key = f"conversation_history_{version.lower()}"

    st.image("assets/IMG_4865.jpeg")
    st.header(f"Welcome to EscapeAssist {version}!")
    st.markdown(knowledge_text)
    st.markdown("Ask me anything about your 2022 Ford Escape, and I'll do my best to assist you!")

    if message_key not in st.session_state:
        st.session_state[message_key] = []

    if history_key not in st.session_state:
        st.session_state[history_key] = []

    for msg in st.session_state[message_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about your Ford Escape...")

    if prompt:
        st.session_state[message_key].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        workflow_input = workflow_input_cls(
            input_as_text=prompt,
            conversation_history=st.session_state[history_key] or None,
        )

        with st.chat_message("assistant"):
            with st.spinner("EscapeAssist is thinking..."):
                result = run_async(workflow(workflow_input))

            reply = extract_reply(result)

            placeholder = st.empty()
            typed = ""
            for char in reply:
                typed += char
                placeholder.markdown(typed)
                time.sleep(0.01)

        if "conversation_history" in result:
            st.session_state[history_key] = result["conversation_history"]

        st.session_state[message_key].append({"role": "assistant", "content": reply})
