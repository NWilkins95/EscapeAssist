# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/06/2026
- EscapeAssist version: V2
- Question ID: 6
- Question: What does the seatbelt reminder indicator do?
- Golden dataset reference: Ford Escape 2022 Owner’s Manual — Seatbelt Reminder Indicator section
- Judge run ID or file: V2-eval-0003

## Judge Output
- Correctness score: 3
- Grounding score: 3
- Hallucination flag: true
- Judge reasoning:
  The Model Answer accurately describes the initial warning and speed-related warnings, which are supported by the Source Quote. However, it adds unsupported details about rear seatbelt monitoring and status display, which are not mentioned in the Source Quote or Ground Truth, leading to partial grounding and hallucination.

## Human Grade
- Correctness score: 4
- Grounding score: 3
- Hallucination score: 1
- Refusal quality: N/A
- Human notes:
  - Core required behavior is correct.
  - Extra details (rear monitoring, status display) are correct in the real vehicle but unsupported by the source quote.
  - These additions are not misleading → hallucination = 1, not a full hallucination.
  - Correctness should not drop below 4 because the required behavior is fully present.

## Disagreement Summary
- Match status: partial
- Main disagreement type: hallucination severity
- Why the human grade differs:
  The judge treats any unsupported detail as a full hallucination unless it is a logical conclusion, dropping correctness to 3 and marking hallucination = true.
  The human rubric distinguishes between:
  - Benign, true-but-unsupported additions → hallucination = 1
  - Incorrect or fabricated additions → hallucination = 5

  The model’s extra details were true and not misleading, so the human score is more lenient.

- Suggested judge prompt change:
  Add explicit guidance:
  “If the model adds information that is true in the real vehicle but not present in the source-quote, classify this as low-severity hallucination (hallucination = false) rather than a full hallucination. Only assign hallucination = true when the added information is false, fabricated, or misleading.”

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Judge should not treat true-but-unsupported details as full hallucinations. Correctness should remain at 4, hallucination should be false, and grounding should reflect partial support.
