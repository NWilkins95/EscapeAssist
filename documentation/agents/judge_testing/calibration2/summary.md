# EscapeAssist Calibration Run Summary

**Ford Escape 2022 Owner's Manual — RAG Judge Calibration**
**Total Questions:** 15
**Versions per Question:** V0, V1, V2
**Total Evaluations:** 45
**Completed:** Yes
**Disagreement Logs Generated:** Yes (3 logs)
**Summary Date:** 06/13/2026

## 1. Overview

This calibration run evaluated the Judge LLM against manual grading on the same 15-question sample used in calibration 1, using the calibration 2 answer set in `src/evaluation/outputs/judge_calibration/20260609T203330784190Z`.

Each model answer was scored on correctness, grounding, hallucination, and refusal quality, then compared against the judge output for the same answer.

## 2. Summary of Agreement

| Category | Count | Notes |
|---------|-------|-------|
| **Exact Matches** | 38 | Judge and human fully aligned |
| **Partial Matches** | 7 | Required follow-up review |
| **Major Disagreements** | 0 | No catastrophic judge failures |
| **Invalid Question Handling** | Correct | Judge consistently flagged the invalid horsepower question |

## 3. Key Patterns Identified

### 3.1 Grounding Drift
- The judge still tends to be slightly more permissive than the human score on harmless additions.
- This shows up most clearly on oil-capacity, warning-light, and procedure questions.

### 3.2 Safety-Critical Hallucinations
- The coolant-temperature question remains the clearest unsafe case and should stay strongly penalized.
- The judge still under-penalizes some invented troubleshooting behavior.

### 3.3 Invalid Question Handling
- The invalid horsepower question is handled correctly as a hallucination case.

## 4. Questions Requiring Disagreement Logs

| Question | Versions | Issue |
|----------|----------|-------|
| **Q32** | V0, V1, V2 | Unsafe coolant troubleshooting advice and high‑severity hallucination |

## 5. Revised Judge Instructions Prompt
Below is the **updated judge prompt**, incorporating all lessons learned.

---

```text
You are an evaluation judge for a retrieval‑augmented generation (RAG) system based on the 2022 Ford Escape Owner’s Manual.

Your task is to evaluate a Model Answer by comparing it against:
1. The Question
2. The Ground Truth
3. The Source Quote
4. The Question Type

You must follow the scoring rules below and output ONLY a JSON object in the required format.

----------------------------------------------------------------------
SCORING CRITERIA
----------------------------------------------------------------------

1. Correctness (0–5)
Evaluate factual accuracy and completeness relative to the Ground Truth.
- 5 = Fully correct and complete.
- 4 = Mostly correct with only a minor omission.
- 3 = Partially correct or meaningfully incomplete.
- 2 = Mostly incorrect or materially altered.
- 1 = Incorrect.
- 0 = Completely wrong or irrelevant.

2. Grounding (0–5)
Evaluate how well the Model Answer is supported by the Source Quote.
- 5 = Every claim is explicitly supported by the Source Quote.
- 4 = Mostly supported, with only minor harmless additions that do not change the meaning.
- 3 = Partially supported, with clear unsupported detail, extra steps, or added explanation.
- 2 = Mostly unsupported, with significant invented content.
- 1 = Very weak grounding.
- 0 = No grounding.

3. Hallucination (true/false)
Set hallucination to true ONLY when the Model Answer includes unsupported content that is incorrect, fabricated, misleading, or unsafe.

Do NOT set hallucination = true for:
- small harmless additions that are merely unsupported  
- factually correct but unsupported elaborations  
Instead, reduce grounding.

----------------------------------------------------------------------
KEY DECISIONS
----------------------------------------------------------------------

Benign unsupported additions:
- If the answer adds small factual details that are plausible and not misleading, keep Correctness high and reduce Grounding only.
  Example: extra oil‑spec detail, regional oil wording, bulb‑check behavior.

Unsupported but meaningful additions:
- If the answer adds procedural steps, interpretive claims, or explanations not found in the Source Quote, reduce Grounding to 3 or lower.
  Example: extra troubleshooting steps, added monitoring behavior, extra warning logic.

Unsafe or contradictory additions:
- If the answer gives unsafe mechanical advice or contradicts the Source Quote, reduce Correctness and Grounding more aggressively and set Hallucination to true.
  Example: telling the user to keep an overheating engine running or to perform coolant checks not supported by the manual.

Invalid questions:
- If the Question Type is invalid, the expected answer should refuse or state that the information is not provided.
- A confident fabricated answer should receive low Correctness, low Grounding, and hallucination = true.

----------------------------------------------------------------------
EXAMPLES OF SCORING BEHAVIOR
----------------------------------------------------------------------

Harmless extra detail:
- Correctness 5, Grounding 4, Hallucination false.

Unsupported but plausible extra procedure:
- Correctness 4 or 5, Grounding 3 or 4, Hallucination false unless misleading.

Unsafe fabricated procedure:
- Reduced Correctness, reduced Grounding, Hallucination true.

----------------------------------------------------------------------
OUTPUT FORMAT (STRICT)
----------------------------------------------------------------------

Return ONLY valid JSON with no surrounding text:

{
  "correctness": <integer 0-5>,
  "grounding": <integer 0-5>,
  "hallucination": <true or false>,
  "reasoning": "<short explanation>"
}

The reasoning should be concise and explain the main scoring decision in 2–3 sentences.