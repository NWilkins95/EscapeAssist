# AI Platform Change Decision

- Date: May 4, 2026
- Owner: Nicholas Wilkins

## Summary

On May 4, 2026, the project decision was made to move from Microsoft Foundry to the OpenAI Platform Agent Builder.

## Context

The original plan used Microsoft Foundry for the AI workflow. During implementation, several blockers made that path unreliable for this project timeline and maintainability goals.

## Decision Drivers

1. Azure billing issues created operational friction and uncertainty.
2. An expired tenant hard-locked access to both the project and the Azure portal.
3. Microsoft support was unable to provide a workable recovery path in time.
4. Foundry did not provide the level of control needed for chunking behavior (chunk size, chunk overlap, and related preprocessing settings).
5. OpenAI Platform offers a simpler integration path with Streamlit.
6. The project is already planning to use the OpenAI Platform API for both the preprocessing pipeline and the Judge LLM, so aligning platforms reduces complexity.

## Decision

Adopt OpenAI Platform Agent Builder as the primary platform for agent development and orchestration, replacing Microsoft Foundry.

## Consequences

- Positive:
  - Removes dependency on the blocked Azure tenant and billing constraints.
  - Improves implementation speed through easier Streamlit integration.
  - Aligns platform usage across Agent Builder, preprocessing pipeline, and Judge LLM API calls.
  - Reduces configuration mismatch risk by standardizing on a single AI platform.

- Trade-offs:
  - Requires migration effort from any Foundry-specific assumptions or setup.
  - Team workflows and documentation need to stay aligned with OpenAI Platform updates.

## Follow-Up Actions

1. Update architecture and implementation docs to reflect OpenAI Platform Agent Builder as the system of record.
2. Confirm preprocessing pipeline controls for chunking and overlap in the OpenAI-based flow.
3. Verify Streamlit integration end-to-end with the new platform.
4. Remove or archive Foundry-specific setup notes that are no longer applicable.
