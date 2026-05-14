from agents import (
    FileSearchTool,
    Agent,
    ModelSettings,
    TResponseInputItem,
    Runner,
    RunConfig,
    trace,
)
from openai import AsyncOpenAI
from types import SimpleNamespace
from guardrails.runtime import (
    load_config_bundle,
    instantiate_guardrails,
    run_guardrails,
)
from pydantic import BaseModel
from typing import Optional, List, Any

MAX_HISTORY_MESSAGES = 5

# =========================================================
# Tool Definitions
# =========================================================
file_search = FileSearchTool(vector_store_ids=["vs_69f97188bd308191b44186b3fec46237"])

# Shared client for guardrails and file search
client = AsyncOpenAI()
ctx = SimpleNamespace(guardrail_llm=client)

# =========================================================
# Guardrails Configuration
# =========================================================
guardrails_config = {
    "guardrails": [
        {
            "name": "Jailbreak",
            "config": {
                "model": "gpt-4.1-mini",
                "confidence_threshold": 0.7
            }
        },
        {
            "name": "NSFW Text",
            "config": {
                "model": "gpt-4.1-mini",
                "confidence_threshold": 0.7
            }
        },
        {
            "name": "URL Filter",
            "config": {
                "url_allow_list": [],
                "allowed_schemes": ["https"],
                "block_userinfo": True,
                "allow_subdomains": False
            }
        },
        {
            "name": "Prompt Injection Detection",
            "config": {
                "model": "gpt-4.1-mini",
                "confidence_threshold": 0.7
            }
        },
        {
            "name": "Moderation",
            "config": {
                "categories": [
                    "sexual/minors",
                    "hate/threatening",
                    "harassment/threatening",
                    "self-harm/instructions",
                    "violence/graphic",
                    "illicit/violent"
                ]
            }
        },
        # FIXED: Removed deprecated field: detect_encoded_pii=True
        {
            "name": "Contains PII",
            "config": {
                "block": False,
                "entities": [
                    "CREDIT_CARD",
                    "US_BANK_NUMBER",
                    "US_PASSPORT",
                    "US_SSN"
                ]
            }
        }
    ]
}

# =========================================================
# Cached Guardrail Instances
# =========================================================
ALL_GUARDRAILS = instantiate_guardrails(load_config_bundle(guardrails_config))
PII_ONLY_CONFIG = {
    "guardrails": [
        next(
            g for g in guardrails_config["guardrails"]
            if g["name"] == "Contains PII"
        )
    ]
}
PII_GUARDRAILS = instantiate_guardrails(load_config_bundle(PII_ONLY_CONFIG))

# =========================================================
# Helper Functions
# =========================================================
def guardrails_has_tripwire(results):
    return any(
        (
            hasattr(r, "tripwire_triggered")
            and (r.tripwire_triggered is True)
        )
        for r in (results or [])
    )

def get_guardrail_safe_text(results, fallback_text):
    for r in (results or []):
        info = (r.info if hasattr(r, "info") else None) or {}
        if isinstance(info, dict) and ("checked_text" in info):
            return info.get("checked_text") or fallback_text
    pii = next(
        (
            (r.info if hasattr(r, "info") else {})
            for r in (results or [])
            if isinstance(
                (r.info if hasattr(r, "info") else None) or {},
                dict
            )
            and (
                "anonymized_text"
                in ((r.info if hasattr(r, "info") else None) or {})
            )
        ),
        None
    )
    if isinstance(pii, dict) and ("anonymized_text" in pii):
        return pii.get("anonymized_text") or fallback_text
    return fallback_text

async def scrub_conversation_history(history, config):
    try:
        guardrails = (config or {}).get("guardrails") or []
        pii = next(
            (
                g for g in guardrails
                if (g or {}).get("name") == "Contains PII"
            ),
            None
        )
        if not pii:
            return
        for msg in (history or []):
            content = (msg or {}).get("content") or []
            for part in content:
                if (
                    isinstance(part, dict)
                    and part.get("type") == "input_text"
                    and isinstance(part.get("text"), str)
                ):
                    res = await run_guardrails(
                        ctx,
                        part["text"],
                        "text/plain",
                        PII_GUARDRAILS,
                        suppress_tripwire=True,
                        raise_guardrail_errors=True
                    )
                    part["text"] = get_guardrail_safe_text(res, part["text"])
    except Exception:
        pass

async def scrub_workflow_input(workflow, input_key, config):
    try:
        guardrails = (config or {}).get("guardrails") or []
        pii = next(
            (
                g for g in guardrails
                if (g or {}).get("name") == "Contains PII"
            ),
            None
        )
        if not pii:
            return
        if not isinstance(workflow, dict):
            return
        value = workflow.get(input_key)
        if not isinstance(value, str):
            return
        res = await run_guardrails(
            ctx,
            value,
            "text/plain",
            PII_GUARDRAILS,
            suppress_tripwire=True,
            raise_guardrail_errors=True
        )
        workflow[input_key] = get_guardrail_safe_text(res, value)
    except Exception:
        pass

async def run_and_apply_guardrails(input_text, config, history, workflow):
    results = await run_guardrails(
        ctx,
        input_text,
        "text/plain",
        ALL_GUARDRAILS,
        suppress_tripwire=True,
        raise_guardrail_errors=True
    )
    has_tripwire = guardrails_has_tripwire(results)
    safe_text = get_guardrail_safe_text(results, input_text)
    fail_output = build_guardrail_fail_output(results or [])
    pass_output = {"safe_text": (get_guardrail_safe_text(results, input_text) or input_text)}
    return {
        "results": results,
        "has_tripwire": has_tripwire,
        "safe_text": safe_text,
        "fail_output": fail_output,
        "pass_output": pass_output
    }

def build_guardrail_fail_output(results):
    def _get(name: str):
        for r in (results or []):
            info = ((r.info if hasattr(r, "info") else None) or {})
            gname = (
                info.get("guardrail_name")
                if isinstance(info, dict)
                else None
            ) or (
                info.get("guardrailName")
                if isinstance(info, dict)
                else None
            )
            if gname == name:
                return r
        return None

    pii, mod, jb, hal, nsfw, url, custom, pid = map(
        _get,
        [
            "Contains PII",
            "Moderation",
            "Jailbreak",
            "Hallucination Detection",
            "NSFW Text",
            "URL Filter",
            "Custom Prompt Check",
            "Prompt Injection Detection"
        ]
    )

    def _tripwire(r):
        return bool(r.tripwire_triggered) if r else False

    def _info(r):
        return r.info if r else {}

    jb_info, hal_info, nsfw_info, url_info, custom_info, pid_info, mod_info, pii_info = map(
        _info,
        [jb, hal, nsfw, url, custom, pid, mod, pii]
    )

    detected_entities = (
        pii_info.get("detected_entities")
        if isinstance(pii_info, dict)
        else {}
    )

    pii_counts = []
    if isinstance(detected_entities, dict):
        for k, v in detected_entities.items():
            if isinstance(v, list):
                pii_counts.append(f"{k}:{len(v)}")

    flagged_categories = (
        mod_info.get("flagged_categories")
        if isinstance(mod_info, dict)
        else None
    ) or []

    return {
        "pii": {
            "failed": ((len(pii_counts) > 0) or _tripwire(pii)),
            "detected_counts": pii_counts
        },
        "moderation": {
            "failed": (_tripwire(mod) or (len(flagged_categories) > 0)),
            "flagged_categories": flagged_categories
        },
        "jailbreak": {
            "failed": _tripwire(jb)
        },
        "hallucination": {
            "failed": _tripwire(hal),
            "reasoning": (hal_info.get("reasoning") if isinstance(hal_info, dict) else None),
            "hallucination_type": (hal_info.get("hallucination_type") if isinstance(hal_info, dict) else None),
            "hallucinated_statements": (hal_info.get("hallucinated_statements") if isinstance(hal_info, dict) else None),
            "verified_statements": (hal_info.get("verified_statements") if isinstance(hal_info, dict) else None)
        },
        "nsfw": {
            "failed": _tripwire(nsfw)
        },
        "url_filter": {
            "failed": _tripwire(url)
        },
        "custom_prompt_check": {
            "failed": _tripwire(custom)
        },
        "prompt_injection": {
            "failed": _tripwire(pid)
        },
    }

# =========================================================
# Agent Definition
# =========================================================
escapeassist = Agent(
    name="EscapeAssist",
    instructions="""
You are EscapeAssist, a helpful automotive assistant focused on the 2022 Ford Escape.

Your role is to give clear, accurate answers grounded in the Ford Escape Owner's Manual and any provided documentation.

Core Behavior:

- Base every answer on retrieved manual content.
- Avoid guessing or adding unsupported information.
- Ask for clarification when needed.
- Keep explanations friendly and easy to follow.
- Use short, numbered steps for procedures.
- Summarize retrieved content rather than quoting long passages.

Grounding Rules:

- Use only information found in retrieved chunks.
- If the manual does not support an answer, say:
  "The manual does not provide this information."
- Do not add extra automotive advice beyond what the manual includes.

Safety Rules:

- Do not provide mechanical diagnoses or instructions beyond the manual.
- If a request is unsafe, offer a safer alternative or recommend contacting a certified mechanic.

Tone & Style:

- Friendly, clear, and supportive.
- No emojis.
- Use simple, helpful language.
- Use bullet points and steps when appropriate.

If the manual does not contain the answer:

- Say so clearly.
- Offer a clarifying question or a safe next step.

Your Purpose:

Help Ford Escape owners understand their vehicle using manual-based, grounded information while keeping the experience approachable.
""",
    model="gpt-4o-mini",
    tools=[file_search],
    model_settings=ModelSettings(temperature=0, top_p=1, max_tokens=2048, store=True)
)

# =========================================================
# Workflow Input
# =========================================================
class WorkflowInput(BaseModel):
    input_as_text: str
    conversation_history: Optional[List[Any]] = None 

# =========================================================
# Main Workflow
# =========================================================
async def run_workflow(workflow_input: WorkflowInput):
    with trace("EscapeAssist-V2"):
        state = {}
        workflow = workflow_input.model_dump()

        # Preserve prior conversation history
        conversation_history: list[dict] = workflow.get("conversation_history") or []
        # Append the current user input as the latest message
        conversation_history.append({
            "role": "user",
            "content": [{"type": "input_text", "text": workflow["input_as_text"]}]
        })
        conversation_history = conversation_history[-MAX_HISTORY_MESSAGES:]
        guardrails_input_text = workflow["input_as_text"]
        guardrails_result = await run_and_apply_guardrails(
            guardrails_input_text,
            guardrails_config,
            conversation_history,
            workflow
        )
        guardrails_hastripwire = guardrails_result["has_tripwire"]
        guardrails_anonymizedtext = guardrails_result["safe_text"]
        guardrails_output = (
            (guardrails_hastripwire and guardrails_result["fail_output"])
            or guardrails_result["pass_output"]
        )
        if guardrails_hastripwire:
            return {
                **guardrails_output,
                "conversation_history": conversation_history,
            }
        # Use sliding window: only pass last 5 messages to agent to cap token usage
        capped_history = conversation_history[-MAX_HISTORY_MESSAGES:]
        escapeassist_result_temp = await Runner.run(
            escapeassist,
            input=[*capped_history],
            run_config=RunConfig(
                trace_metadata={
                    "__trace_source__": "agent-builder",
                    "workflow_id": "wf_69f971737c208190ac7a3919ecb3258f091e5430fee815f7"
                }
            )
        )
        escapeassist_result = {
            "output_text": escapeassist_result_temp.final_output_as(str)
        }
        conversation_history.append(
            {
                "role": "assistant",
                "content": [{"type": "output_text", "text": escapeassist_result["output_text"]}],
            }
        )
        conversation_history = conversation_history[-MAX_HISTORY_MESSAGES:]
        return {
            "guardrails": guardrails_output,
            "assistant": escapeassist_result,
            "conversation_history": conversation_history
        }
