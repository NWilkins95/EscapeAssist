# (no external typing imports needed)

# =================================================================
# Judge prompt builder for RAG evaluation
#
# This is a reusable prompt for the Judge LLM that evaluates model answers
# against the golden dataset. It defines the evaluation criteria, scoring rules, and 
# expected output format.
#
# Usage:
#     from evaluation.judge.judge_prompt import build_judge_prompt
#     prompt = build_judge_prompt(question, model_answer, truth, source_quote, qtype)
#     # send prompt to the LLM evaluator
# =================================================================


def build_judge_prompt(question: str, model_answer: str, truth: str, source_quote: str, qtype: str) -> str:
    """Return the formatted judge prompt string

    Inputs are inserted verbatim from the golden dataset. The
    returned string is ready to send to a Judge LLM that will produce the
    JSON evaluation.
    """

    prompt = f"""
    You are an evaluation judge for a retrieval-augmented generation (RAG) system.

    Task: Compare the Model Answer to the Ground Truth and the provided Source Quote.
    Score the Model Answer using the rules below and produce ONLY a JSON object (see OUTPUT FORMAT).

    INPUTS
    - Question: {question}
    - Model Answer: {model_answer}
    - Ground Truth: {truth}
    - Source Quote: {source_quote}
    - Question Type: {qtype}

    EVALUATION RULES
    1) Correctness (0-5): judge factual accuracy and completeness relative to the Ground Truth.
       - 5: Fully correct and complete
       - 4: Mostly correct, minor omissions
       - 3: Partially correct; important information missing
       - 2: Mostly incorrect or incomplete
       - 1: Incorrect
       - 0: Completely wrong or irrelevant

    2) Grounding (0-5): judge how well the Model Answer is supported by the Source Quote.
       - 5: Fully grounded in the source
       - 4: Mostly grounded with small, acceptable additions
       - 3: Partially grounded
       - 2: Weak grounding
       - 1: Mostly hallucinated
       - 0: Completely hallucinated

    3) Hallucination (true/false): true if the Model Answer contains information that is
       unsupported by the Source Quote and is likely incorrect or fabricated.

    Special cases:
    - If Question Type == "invalid": expect the model to refuse or state the information is not provided.
      * Correct refusal: correctness=5, grounding=5, hallucination=false
      * Partial/speculative answer: correctness in 2-3, grounding low, hallucination=true
      * Confident hallucination: correctness 0-1, grounding=0, hallucination=true

    Procedural questions: verify all required steps are present and in correct order.
    Tables / structured outputs: verify all required entries and mappings are present.

    General rule: Do not require exact wording; evaluate meaning, accuracy, and completeness.

    OUTPUT FORMAT (STRICT):
    Return ONLY valid JSON (no surrounding text):
    {{ "correctness": <int 0-5>, "grounding": <int 0-5>, "hallucination": <true|false>, "reasoning": "<short explanation>" }}

    Notes on scoring:
    - An answer may be factually correct but include extra info not in the Source Quote.
      * Do NOT reduce correctness for correct additional info.
      * Reduce grounding if the extra info is unsupported by the Source Quote.
      * Set hallucination = true only if the unsupported info is likely incorrect or fabricated.

    Examples of hallucination:
    - Adding facts not present in the Source Quote that are likely incorrect or fabricated -> likely hallucination
    - Guessing specific values or specs without support -> hallucination

    When you produce the JSON, keep the reasoning concise (one or two sentences).
    """

    return prompt