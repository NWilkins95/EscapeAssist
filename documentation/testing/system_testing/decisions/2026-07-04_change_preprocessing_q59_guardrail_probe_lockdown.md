# Change Decision - Instructions - Unsupported Spec Refusal

- Date: 2026-07-04
- Owner: Nicholas Wilkins
- Iteration: iter-003
- Affected Version(s): V0, V1, V2
- Category: instructions

---

## Summary

Add a stricter refusal rule for unsupported spec questions so the assistant gives a direct refusal instead of drifting into trim-specific clarifying language.

---

## Context

The baseline and later runs showed that invalid and out-of-scope questions are the main hallucination driver, especially for unsupported feature and spec lookups.

This affected questions such as horsepower, winter tire guidance, firmware, and trim-specific capability comparisons.

Q59 remains frozen as an invalid guardrail probe and is not part of this change.

---

## Change

Update the agent grounding instructions so the model refuses unsupported spec questions instead of guessing or softening into trim-related clarification.

Proposed wording to be added:

- If the user asks for trim-specific features, trim-specific capacities, anything about firmware, trim specific exact specs, anything about horsepower or torque, trim-specific winter tire and chains details, or other unsupported details that are not found in modern car owner's manuals, respond: "The manual does not provide this information."
- Do not infer or estimate from related trims, model years, or general automotive knowledge.
- Do not offer trim-related follow-up questions or "if you have any other questions" style endings for unsupported-spec requests.
- Do not suggest asking about trims or trim features as a follow-up.

---

## Why This Change

This is the simplest way to reduce hallucinations without changing the preprocessing pipeline.
It directly targets the highest-frequency failure pattern in the baseline and the remaining trim-specific clarification drift.

---

## Expected Outcome

- Lower hallucination rate on invalid questions
- Fewer zero-score answers on unsupported spec prompts
- Better consistency across V0, V1, and V2

---

## Next Step

Test the instruction update against the golden dataset and compare hallucination rate plus invalid-question scores.
