# Instruction Version Selection Decision

- Date: May 7, 2026
- Owner: Nicholas Wilkins

## Summary

On May 7, 2026, the project decision was made to adopt **Version B** as the final instruction set for the EscapeAssist AI assistant, based on comprehensive testing and evaluation of four instruction variations.

## Context

Four instruction variations (A, B, C, and D) were tested against seven use-case questions covering various vehicle manual topics, including maintenance procedures, feature explanations, warning light diagnostics, and safety refusals. Each variation employed a distinct tone and formatting approach.

## Decision Drivers

1. **Grounding Accuracy:**
   - Version B is the only version to correctly answer the wrench warning light question, indicating superior instruction clarity.
   - Versions A, C, and D all exhibited the same hallucination (TPMS confusion) on this diagnostic question.
   - This systematic difference suggests Version B's instructions provide stronger safeguards against grounding drift.

2. **User Experience & Clarity:**
   - Version B's friendly, supportive tone builds user confidence without sacrificing accuracy.
   - Additional verbosity in Version B enhances clarity and comprehension rather than introducing confusion.
   - Readability and user-friendliness rank highest for Version B (9/10 and 9/10, respectively).

3. **Safety Performance:**
   - All versions demonstrate excellent and equivalent safety behavior (10/10).
   - All correctly refuse unsafe repair requests and avoid over-confident mechanical guidance.
   - No version shows safety advantages over others.

4. **Consistency & Reliability:**
   - Version B maintains consistency scores comparable to other versions (9/10).
   - Low variability in output quality across different question types.

5. **Known Issues Across All Versions:**
   - Minor tire pressure grounding drift is present equally in all four versions.
   - This issue is addressable through instruction refinement and does not differentiate performance.

## Decision

Adopt **Version B** as the final instruction set for EscapeAssist. This version prioritizes user-friendly communication, maintains the highest grounding accuracy, and combines excellent safety behavior with superior clarity.

## Consequences

- **Positive:**
  - Users will interact with a friendly, approachable assistant that builds confidence and understanding.
  - Reduced hallucination risk compared to Versions A, C, and D due to superior grounding accuracy.
  - Verbosity is intentional and beneficial, not a flaw—it improves clarity on technical topics.
  - Maintains all safety guardrails at the highest level.
  - Establishes a clear performance baseline for future instruction iterations.

- **Trade-offs:**
  - Slightly more verbose than Version A, which may be perceived as less concise (though testing shows this improves comprehension).
  - Minor tire pressure grounding drift is present (equally in all versions; addressable separately).
  - Requires commitment to Version B's friendly tone across future updates and refinements.

## Follow-Up Actions

1. Finalize Version B as the canonical instruction set and deploy across all EscapeAssist environments.
2. Address tire pressure grounding drift by revising instructions to emphasize: "Always direct users to the Safety Compliance Certification Label; do not provide example pressures as alternatives."
3. Investigate the wrench warning light hallucination in Versions A, C, and D; apply learnings to strengthen content retrieval or hallucination prevention for diagnostic topics.
4. Archive Versions A, C, and D test notes with clear rationale for Version B selection.
5. Monitor Version B performance in production; log any grounding drift for future refinement.
6. Consider A/B testing Version B against Versions C and D in limited rollout to validate findings before full deployment.
