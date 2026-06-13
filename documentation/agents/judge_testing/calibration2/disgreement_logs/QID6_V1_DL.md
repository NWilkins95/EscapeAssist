# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V1
- Question ID: 6
- Question: What does the seatbelt reminder indicator do?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 3
- Grounding score: 3
- Hallucination flag: false
- Judge reasoning:
  The Model Answer correctly describes the initial warning and speed-related warnings, aligning with the Ground Truth and Source Quote. However, it includes additional details about rear seat warnings and status display, which are not supported by the Source Quote. These additions are not necessarily incorrect but reduce grounding.

## Human Grade
- Correctness score: 4
- Grounding score: 3
- Hallucination score: 1
- Refusal quality: N/A
- Human notes:
  - Core warning behavior is correct.
  - Extra rear-monitoring and status details are unsupported.
  - The unsupported additions are not clearly misleading, so hallucination is minor.

## Disagreement Summary
- Match status: partial
- Main disagreement type: correctness, hallucination
- Why the human grade differs:
  The answer keeps the core warnings right, but the unsupported rear-monitoring detail should be treated as a minor hallucination rather than a clean no-hallucination answer.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Reduce hallucination to a minor unsupported detail and keep grounding below 5.
