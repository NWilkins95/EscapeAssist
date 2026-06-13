# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V1
- Question ID: 15
- Question: Why is it important to use the correct engine oil specification?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 5
- Grounding score: 5
- Hallucination flag: false
- Judge reasoning:
  The Model Answer accurately reflects the Ground Truth and is fully supported by the Source Quote. It covers all key points: component protection, engine performance, emissions control, and fuel economy. There are no unsupported or incorrect additions.

## Human Grade
- Correctness score: 5
- Grounding score: 4
- Hallucination score: 0
- Refusal quality: N/A
- Human notes:
  - Fully correct.
  - The extra environmental-regulation wording is reasonable, but the answer still adds unsupported detail.
  - No hallucinations.

## Disagreement Summary
- Match status: partial
- Main disagreement type: grounding
- Why the human grade differs:
  The answer is fully correct, but the extra wording is still unsupported by the retrieved quote and should not be treated as fully grounded.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Reduce grounding for the unsupported elaboration; do not treat the answer as fully grounded.
