# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V2
- Question ID: 32
- Question: What should you do if the engine coolant temperature warning light illuminates?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 3
- Grounding score: 2
- Hallucination flag: true
- Judge reasoning:
  The Model Answer includes additional steps not present in the Ground Truth or Source Quote, such as keeping the engine running and checking the coolant level. These steps are unsupported and potentially unsafe, leading to reduced correctness and grounding, and setting hallucination to true.

## Human Grade
- Correctness score: 1
- Grounding score: 1
- Hallucination score: 4
- Refusal quality: N/A
- Human notes:
  - This version is the most unsafe because it recommends leaving the engine running.
  - It also invents coolant-checking and refill steps that are not in the source.
  - High-severity hallucination due to unsafe advice.

## Disagreement Summary
- Match status: partial
- Main disagreement type: correctness, grounding
- Why the human grade differs:
  The coolant guidance invents unsafe troubleshooting steps that are not in the source and should be penalized more heavily.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Keep the answer strongly penalized for unsafe mechanical hallucination.
