# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V1
- Question ID: 32
- Question: What should you do if the engine coolant temperature warning light illuminates?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 3
- Grounding score: 3
- Hallucination flag: false
- Judge reasoning:
  The Model Answer includes the correct initial steps of stopping the vehicle and switching off the engine, as well as seeking professional help, which aligns with the Ground Truth. However, it adds steps like contacting roadside assistance, waiting for cooling, checking coolant level, and restarting the engine, which are not mentioned in the Source Quote. These additions are not harmful but reduce grounding.

## Human Grade
- Correctness score: 2
- Grounding score: 2
- Hallucination score: 4
- Refusal quality: N/A
- Human notes:
  - The manual’s instruction is simple: stop, switch off, and get it checked.
  - The added diagnostic procedure is unsafe and not in the source.
  - Dangerous mechanical hallucination.

## Disagreement Summary
- Match status: partial
- Main disagreement type: correctness, grounding, hallucination
- Why the human grade differs:
  The coolant guidance invents unsafe troubleshooting steps that are not in the source and should be penalized more heavily.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Keep the answer strongly penalized for unsafe mechanical hallucination.
