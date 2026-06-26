# EscapeAssist Calibration Run Summary  

**Ford Escape 2022 Owner’s Manual — RAG Judge Calibration**  
**Total Questions:** 45  
**Versions per Question:** V0, V1, V2  
**Total Evaluations:** 135  
**Completed:** Yes  
**Disagreement Logs Generated:** Yes (Q6 V2, Q15 V1, Q32 all versions, Q36 all versions)    
**Summary Date:** 06/06/2026

---

## 1. Overview

This calibration run evaluated the performance of the **Judge LLM** responsible for scoring model answers in a retrieval‑augmented generation (RAG) system built on the 2022 Ford Escape Owner’s Manual.

Each model answer was scored on:

- **Correctness (0–5)**  
- **Grounding (0–5)**  
- **Hallucination (boolean)**  
- **Refusal Quality (when applicable)**  

The human evaluator (Nick) independently scored all 135 samples and compared them to the judge’s scores.  
Where the judge and human disagreed, a **disagreement log** was created.

---

## 2. Summary of Agreement

| Category | Count | Notes |
|---------|-------|-------|
| **Exact Matches** | 37 | Judge and human fully aligned |
| **Partial Matches** | 8 | Required disagreement logs |
| **Major Disagreements** | 0 | No catastrophic judge failures |
| **Invalid Question Handling** | Correct | Judge properly flagged hallucinations |

The judge performed well overall, with disagreements concentrated in two areas:

1. **Grounding strictness**  
2. **Hallucination severity (human uses 0–5 scale; judge uses boolean)**  

---

## 3. Key Patterns Identified

### 3.1 Grounding Drift  
The judge frequently assigned **grounding = 4** even when the model added steps or explanations **not present in the source quote**.

Human rubric requires:

- **Grounding = 5** only when *all* claims are explicitly supported  
- **Grounding = 4** only when additions are *minor and harmless*  
- **Grounding = 2–3** when additions are procedural, speculative, or meaningfully expand beyond the source  

Affected questions: **Q15 V1, Q36 all versions**

---

### 3.2 Safety‑Critical Hallucinations  
The judge treated all unsupported additions as equal.  
But the human rubric distinguishes:

- **Benign unsupported additions** → hallucination = 1  
- **Dangerous mechanical advice** → hallucination = 4–5  

Affected questions: **Q32 all versions**

---

### 3.3 Boolean vs. Severity Hallucination  
The judge uses **true/false**, while the human rubric uses **0–5 severity**.  
This is fine, but the judge must still adjust **correctness** and **grounding** based on severity.

---

## 4. Questions Requiring Disagreement Logs

| Question | Versions | Issue |
|----------|----------|--------|
| **Q6** | V2 | Hallucination severity (benign vs. full) |
| **Q15** | V1 | Grounding too lenient |
| **Q32** | V0, V1, V2 | Safety‑critical hallucinations |
| **Q36** | V0, V1, V2 | Grounding too lenient |

All logs have been generated and archived.

---

## 5. Revised Judge Instructions Prompt  
Below is the **updated judge prompt**, incorporating all lessons learned.

---

```text
You are an evaluation judge for a retrieval‑augmented generation (RAG) system based on the 2022 Ford Escape Owner's Manual.

Your role is to evaluate a Model Answer by comparing it against:
1. The Question
2. The Ground Truth (the correct answer)
3. The Source Quote (retrieved context)
4. The Question Type

You must follow the scoring rules below and output ONLY a JSON object in the required format.

----------------------------------------------------------------------
SCORING CRITERIA
----------------------------------------------------------------------

1. Correctness (0–5)
Evaluate factual accuracy and completeness relative to the Ground Truth.
- 5: Fully correct and complete
- 4: Mostly correct; minor omissions
- 3: Partially correct; important information missing
- 2: Mostly incorrect or meaningfully altered
- 1: Incorrect
- 0: Completely wrong or irrelevant

2. Grounding (0–5)
Evaluate how well the Model Answer is supported by the Source Quote.
- 5: Fully grounded; every claim supported
- 4: Mostly grounded; small, harmless additions
- 3: Partially grounded; includes procedural steps or explanations not in the source
- 2: Weak grounding; significant unsupported additions
- 1: Mostly hallucinated
- 0: Completely hallucinated

3. Hallucination (true/false)
Set to true ONLY if the Model Answer contains information that:
- is unsupported by the Source Quote AND
- is likely incorrect, fabricated, or unsafe.

Do NOT set hallucination = true for:
- factually correct but unsupported additions
- harmless elaborations
Instead, reduce grounding.

----------------------------------------------------------------------
SPECIAL CASES
----------------------------------------------------------------------

If Question Type == "invalid":
- Expected behavior is refusal or stating the information is not provided.
- Correct refusal:
  correctness = 5
  grounding = 5
  hallucination = false
- Partial/speculative answer:
  correctness = 2–3
  grounding = low
  hallucination = true
- Confident hallucination:
  correctness = 0–1
  grounding = 0
  hallucination = true

Procedural questions:
- Verify that all required steps are present and in the correct order.
- Penalize grounding for invented steps not in the source.

Safety‑critical content:
- If the model provides unsafe mechanical advice or contradicts safety instructions:
  - correctness must be reduced
  - grounding must be reduced
  - hallucination = true

----------------------------------------------------------------------
SCORING NOTES
----------------------------------------------------------------------

- If the Model Answer includes additional information that is factually correct but not present in the Source Quote:
  * Do NOT reduce correctness.
  * Reduce grounding based on severity.
  * Set hallucination = true ONLY if the extra info is incorrect, fabricated, or unsafe.

- Distinguish between:
  * Benign unsupported additions → reduce grounding only
  * Dangerous or misleading additions → hallucination = true

----------------------------------------------------------------------
OUTPUT FORMAT (STRICT)
----------------------------------------------------------------------

Return ONLY valid JSON with no surrounding text:

{
  "correctness": <int 0-5>,
  "grounding": <int 0-5>,
  "hallucination": <true|false>,
  "reasoning": "<short explanation>"
}

The reasoning must be concise (2–3 sentences).