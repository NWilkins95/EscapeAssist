# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V2
- Question ID: 15
- Question: Why is it important to use the correct engine oil specification?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 5
- Grounding score: 4
- Hallucination flag: false
- Judge reasoning:
  The Model Answer is fully correct and complete, matching the Ground Truth. It covers all key points: component protection, warranty, performance, emissions, and fuel economy. However, the Source Quote does not explicitly mention warranty coverage, so grounding is slightly reduced.

## Human Grade
- Correctness score: 4
- Grounding score: 4
- Hallucination score: 0
- Refusal quality: N/A
- Human notes:
  - Core reasons are present and correct.
  - The extra explanations are reasonable extrapolations, not hallucinations.
  - Still slightly less grounded than the source because of the added detail.

## Disagreement Summary
- Match status: partial
- Main disagreement type: correctness
- Why the human grade differs:
  The answer is fully correct, but the extra wording is still unsupported by the retrieved quote and should not be treated as fully grounded.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Reduce grounding for the unsupported elaboration; do not treat the answer as fully grounded.
