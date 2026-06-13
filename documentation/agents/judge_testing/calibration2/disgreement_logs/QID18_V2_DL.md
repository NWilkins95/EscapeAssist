# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist version: V2
- Question ID: 18
- Question: What are the differences in oil capacity and specifications among the 1.5L EcoBoost, 2.0L EcoBoost, and 2.5L hybrid engines?
- Golden dataset reference: Ford Escape 2022 Owner's Manual
- Judge run ID or file: calibration2

## Judge Output
- Correctness score: 2
- Grounding score: 2
- Hallucination flag: true
- Judge reasoning:
  The Model Answer incorrectly specifies the oil type for the 2.0L EcoBoost engine as SAE 5W-20 instead of SAE 5W-30 and the specification as WSS-M2C960-A1 instead of WSS-M2C961-A1. These errors are not supported by the Source Quote, leading to incorrect and unsafe information.

## Human Grade
- Correctness score: 3
- Grounding score: 2
- Hallucination score: 3
- Refusal quality: N/A
- Human notes:
  - Two engine specs are correct, but the 2.0L spec is wrong.
  - The incorrect 2.0L oil type/specification is a meaningful factual error.
  - Hallucination is significant because the answer mixes correct and incorrect specs.

## Disagreement Summary
- Match status: partial
- Main disagreement type: correctness
- Why the human grade differs:
  The judge is stricter on the wrong 2.0L oil spec than the human score, but the human grade still treats the row as a partially correct mix of right and wrong engine specs.

## Final Decision
- Accept judge as-is for this sample: No
- Correction note:
  Mark the 2.0L oil specification as incorrect and lower both correctness and grounding.
