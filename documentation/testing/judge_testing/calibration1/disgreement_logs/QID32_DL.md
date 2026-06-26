# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/06/2026
- EscapeAssist versions: V0, V1, V2
- Question ID: 32
- Question: What should you do if the engine coolant temperature warning light illuminates?
- Golden dataset reference: Ford Escape 2022 Owner’s Manual — Engine Coolant Temperature Warning Light
- Judge run IDs: V0-eval-0013, V1-eval-0013, V2-eval-0013

## Judge Output (Summary Across Versions)
- Correctness scores: 3 (all versions)
- Grounding scores: 3 (all versions)
- Hallucination flag: true (all versions)
- Judge reasoning:
  The Model Answers include additional steps not present in the Ground Truth or Source Quote, such as waiting for cooling, checking coolant level, adding coolant, and restarting the engine. These unsupported additions lead to partial correctness, partial grounding, and a hallucination flag.

## Human Grade (Summary Across Versions)
### Version V0
- Correctness: 2
- Grounding: 2
- Hallucination: 4
- Notes:
  - Model invents multi-step troubleshooting not in the manual.
  - Recommending checking coolant and adding coolant is **dangerous** unless fully cooled.
  - High-severity hallucination due to unsafe mechanical advice.

### Version V1
- Correctness: 2
- Grounding: 2
- Hallucination: 4
- Notes:
  - Same dangerous hallucinations as V0.
  - None of the invented steps appear in the manual.
  - Contradicts Ford safety guidance.

### Version V2
- Correctness: 1
- Grounding: 1
- Hallucination: 4
- Notes:
  - Even more unsafe: recommends **leaving the engine running**, which directly contradicts the manual.
  - Again invents steps about checking coolant and adding coolant.
  - High-severity hallucination due to unsafe, fabricated mechanical instructions.

## Disagreement Summary
- Match status: partial (all versions)
- Main disagreement types:
  - Correctness severity
  - Grounding severity
  - Hallucination severity (judge uses boolean; human uses 0–5 scale)
- Why the human grade differs:
  - The judge treats all unsupported additions as generic hallucinations.
  - The human rubric distinguishes:
    - **Benign unsupported additions** → hallucination = 1
    - **Dangerous or safety‑critical hallucinations** → hallucination = 4–5
  - The model’s invented steps are **unsafe**, contradict Ford guidance, and meaningfully alter the required action.
  - Therefore correctness and grounding must be reduced more aggressively.

- Suggested judge prompt change:
  Add explicit guidance:
  “If the model provides **unsafe mechanical advice**, or contradicts the safety instructions in the source, treat this as a **high‑severity hallucination** and reduce correctness and grounding accordingly. Unsafe additions should not be scored the same as benign unsupported details.  
  When hallucination is boolean, still differentiate internally between *benign* and *dangerous* hallucinations for correctness and grounding scoring.”

## Final Decision
- Accept judge as-is for these samples: No
- Correction note:
  The judge should reduce correctness and grounding further and treat these as **high-severity safety hallucinations**, not generic unsupported additions.