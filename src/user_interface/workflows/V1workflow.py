from agents import (
    FileSearchTool,
    Agent,
    ModelSettings,
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

from user_interface.workflows.escapeassist_instructions import ESCAPEASSIST_INSTRUCTIONS

MAX_HISTORY_MESSAGES = 5

# =========================================================
# Tool Definitions
# =========================================================
file_search = FileSearchTool(vector_store_ids=["vs_69f967643a9c8191ada28567bf05bb21"])

# Shared client
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
        # Deprecated field removed.
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

# =========================================================
# Helper Functions
# =========================================================
def guardrails_has_tripwire(results):
    """
    Return True when any guardrail result tripped.
    """
    return any(
        (
            hasattr(r, "tripwire_triggered")
            and (r.tripwire_triggered is True)
        )
        for r in (results or [])
    )

def get_guardrail_safe_text(results, fallback_text):
    """
    Return scrubbed text from guardrail results, or the fallback text.
    """
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

async def run_and_apply_guardrails(input_text):
    """
    Run guardrails and assemble the response payload.
    """
    results = await run_guardrails(
        ctx,
        input_text,
        "text/plain",
        ALL_GUARDRAILS,
        suppress_tripwire=True,
        raise_guardrail_errors=True
    )
    safe_text = get_guardrail_safe_text(results, input_text)
    return {
        "results": results,
        "has_tripwire": guardrails_has_tripwire(results),
        "safe_text": safe_text,
        "fail_output": build_guardrail_fail_output(results or []),
        "pass_output": {"safe_text": (safe_text or input_text)}
    }

def build_guardrail_fail_output(results):
    """
    Build the failure payload for triggered guardrails.
    """
    def _get(name: str):
        """
        Find the guardrail result for a given name.
        """
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
        """
        Return whether the result tripped.
        """
        return bool(r.tripwire_triggered) if r else False

    def _info(r):
        """
        Return the info payload for a result.
        """
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
    instructions=ESCAPEASSIST_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[file_search],
    model_settings=ModelSettings(temperature=0, top_p=1, max_tokens=2048, store=True)
)

# =========================================================
# Workflow Input
# =========================================================
class WorkflowInput(BaseModel):
    """
    Input payload for the EscapeAssist workflow.
    """
    input_as_text: str
    conversation_history: Optional[List[Any]] = None 

# =========================================================
# Main Workflow
# =========================================================
async def run_workflow(workflow_input: WorkflowInput):
    """
    Run the V1 guardrails and assistant workflow for one request.
    """
    with trace("EscapeAssist-V1"):
        workflow = workflow_input.model_dump()

        conversation_history: list[dict] = workflow.get("conversation_history") or []
        conversation_history.append({
            "role": "user",
            "content": [{"type": "input_text", "text": workflow["input_as_text"]}]
        })
        conversation_history = conversation_history[-MAX_HISTORY_MESSAGES:]
        guardrails_result = await run_and_apply_guardrails(workflow["input_as_text"])
        if guardrails_result["has_tripwire"]:
            return {
                **guardrails_result["fail_output"],
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
                    "workflow_id": "wf_69f9674bf9048190a51575109193a2ce034614341284a3a3"
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
            "guardrails": guardrails_result["pass_output"],
            "assistant": escapeassist_result,
            "conversation_history": conversation_history
        }
