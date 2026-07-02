# Change Decision - Instructions - Unsupported Spec Refusal

- Date: 2026-07-01
- Owner: Nicholas Wilkins
- Iteration: iter-1
- Affected Version(s): V0, V1, V2
- Category: instructions

---

## Summary

Add a more explicit refusal rule for trim features, capacities, firmware, and other unsupported spec questions when the manual does not provide a direct answer.

---

## Context

The baseline run showed that invalid and out-of-scope questions were the main hallucination driver, especially for unsupported feature and spec lookups.

This affected questions such as horsepower, firmware, snow chains, and trim-specific capability comparisons.

---

## Change

Update the agent grounding instructions so the model refuses unsupported spec questions instead of guessing.

Proposed wording to be added:

- If the user asks for trim-specific features, capacities, firmware, exact specs, or other details not directly stated in the manual, respond: "The manual does not provide this information."
- Do not infer or estimate from related trims, model years, or general automotive knowledge.
- Do not expand beyond the retrieved source.
- Offer a clarifying question or suggest checking the manual or service documentation.

---

## Why This Change

This is the simplest way to reduce hallucinations without changing the preprocessing pipeline.
It directly targets the highest-frequency failure pattern in the baseline.

---

## Expected Outcome

- Lower hallucination rate on invalid questions
- Fewer zero-score answers on unsupported spec prompts
- Better consistency across V0, V1, and V2

---

## Next Step

Test the instruction update against the golden dataset and compare hallucination rate plus invalid-question scores.