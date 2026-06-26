# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/06/2026
- EscapeAssist versions: V0, V1, V2
- Question ID: 36
- Question: What does the oil pressure warning light indicate?
- Golden dataset reference: Ford Escape 2022 Owner’s Manual — Oil Pressure Warning Light
- Judge run IDs: V0-eval-0007, V1-eval-0007, V2-eval-0007

## Judge Output (Summary Across Versions)
- Correctness scores: 5 (all versions)
- Grounding scores: 4 (all versions)
- Hallucination flag: false (all versions)
- Judge reasoning:
  The Model Answers correctly identify that the oil pressure warning light indicates low engine oil pressure. The judge considers the additional procedural steps (checking oil, adding oil, stopping safely) reasonable and not hallucinations, and therefore assigns high grounding.

## Human Grade (Summary Across Versions)
### Version V0
- Correctness: 5
- Grounding: 2
- Hallucination: 0
- Notes:
  - Core meaning is correct.
  - Adds multi-step troubleshooting not present in the source.
  - Steps are safe and true → no hallucination.
  - Grounding reduced because the manual only states the meaning of the light, not what to do.

### Version V1
- Correctness: 5
- Grounding: 3
- Hallucination: 0
- Notes:
  - Less verbose than V0 but still adds unsupported procedural steps.
  - Steps are safe and true → no hallucination.
  - Grounding reduced because the manual does not provide any procedural instructions.

### Version V2
- Correctness: 5
- Grounding: 2
- Hallucination: 0
- Notes:
  - Adds speculative causes (“malfunction in the oil pressure system”) not in the source.
  - Adds procedural steps not in the manual.
  - Still safe and true → no hallucination.
  - Grounding reduced due to unsupported additions.

## Disagreement Summary
- Match status: partial (all versions)
- Main disagreement type: grounding strictness
- Why the human grade differs:
  - The judge treats the procedural steps as acceptable elaboration and assigns grounding = 4.
  - The human rubric requires grounding = 5 **only when every claim is explicitly supported** by the retrieved chunk.
  - The manual does **not** provide:
    - instructions to check oil,
    - instructions to add oil,
    - instructions to stop safely,
    - speculative causes of low pressure.
  - Therefore grounding must be reduced.

- Additional note on hallucination scoring:
  - The judge uses a **boolean** hallucination flag.
  - The human rubric uses a **0–5 severity scale**.
  - In this case, the additions are true and safe → hallucination = 0, but grounding must still be penalized.

- Suggested judge prompt change:
  Add explicit guidance:
  “If the model includes **procedural steps, troubleshooting actions, or speculative causes** that are not present in the source quote, reduce grounding accordingly even if the additions are true. Only assign grounding = 5 when **all** statements are directly supported by the source.  
  Use the hallucination flag only for **false or misleading** additions, not for true-but-unsupported elaborations.”

## Final Decision
- Accept judge as-is for these samples: No
- Correction note:
  The judge should reduce grounding to 2–3 depending on version, because the procedural steps and speculative causes are not supported by the source. Correctness remains 5 and hallucination remains false/0.