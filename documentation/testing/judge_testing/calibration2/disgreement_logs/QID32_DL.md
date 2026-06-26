# Judge vs. Human Disagreement Log

## Run Metadata
- Date: 06/13/2026
- EscapeAssist versions: V0, V1, V2
- Question ID: 32
- Question: What should you do if the engine coolant temperature warning light illuminates?
- Golden dataset reference: Ford Escape 2022 Owner’s Manual — Engine Coolant Temperature Warning Light
- Judge run IDs: V0-eval-20260609, V1-eval-20260609, V2-eval-20260609

## Judge Output (Summary Across Versions)
- Correctness scores (judge): V0: 3, V1: 3, V2: 3
- Grounding scores (judge): V0: 3, V1: 3, V2: 2
- Hallucination flag (judge): V0: false, V1: false, V2: true
- Judge reasoning:
  The Model Answers include additional procedural steps beyond the Ground Truth (stop, switch off, get checked). Some added steps (checking coolant, adding coolant, restarting engine, leaving engine running) are either unsupported or potentially unsafe. The judge treats the answers as partially correct with reduced grounding; for V2 the judge set hallucination=true due to explicitly unsafe advice.

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
  - Same dangerous hallucinations as V0; invented steps are not in the manual.
  - Contradicts Ford safety guidance.

### Version V2
- Correctness: 1
- Grounding: 1
- Hallucination: 4
- Notes:
  - V2 recommends leaving the engine running, which contradicts the manual and is explicitly unsafe.
  - Invents coolant inspection/refill steps; high‑severity hallucination.

## Disagreement Summary
- Match status: partial (all versions)
- Main disagreement types:
  - Correctness severity (judge is more permissive)
  - Grounding severity (judge reduces grounding less than human)
  - Hallucination handling differences (judge boolean vs. human severity scale)
- Why the human grade differs:
  - The judge treats unsupported additions as lower‑severity grounding issues in some cases, while the human grader distinguishes benign unsupported details from **dangerous, safety‑critical hallucinations** that should trigger stronger penalties.
  - The invented steps materially alter the recommended action and introduce potential safety risks; humans penalize these more heavily.

## Suggested Judge Prompt Changes
- Add explicit instruction: if the Model Answer includes **unsafe mechanical advice** or contradicts safety instructions in the source, treat this as a **high‑severity hallucination**. When hallucination is recorded as a boolean, still reduce correctness and grounding more aggressively for unsafe additions and document the internal severity.

## Final Decision
- Accept judge as-is for these samples: No
- Correction note:
  The judge should be adjusted to differentiate between benign unsupported additions and dangerous hallucinations — unsafe additions should reduce both correctness and grounding more strongly and, when possible, set hallucination=true.
