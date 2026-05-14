# Workflow Orchestration Location Decision

- Date: May 13, 2026
- Owner: Nicholas Wilkins

## Summary

On May 13, 2026, the project decision was made to host bot orchestration/workflow logic inside the application codebase instead of relying on OpenAI Responses API orchestration.

## Context

During implementation, model access through the OpenAI Responses API did not work as expected for this project setup. Because reliable model access is required for the assistant to run, orchestration could not remain blocked on external API behavior.

## Decision Drivers

1. The current integration path could not reliably access models through the Responses API.
2. The project needed a dependable orchestration path to keep development moving.
3. Hosting orchestration in-app gives direct control over execution flow, retries, and error handling.
4. Local orchestration simplifies debugging because workflow state is visible in project code.
5. Consolidating orchestration in the app reduces dependency on unsupported or unstable API behavior.

## Decision

Implement and maintain orchestration/workflow execution within the EscapeAssist application itself as the primary runtime path.

## Consequences

- Positive:
  - Removes a critical blocker caused by model access issues.
  - Improves reliability by keeping control of orchestration in code we own.
  - Makes failures easier to diagnose and reproduce.
  - Enables faster iteration on workflow behavior.

- Trade-offs:
  - Increases maintenance responsibility for orchestration logic in the app.
  - Requires ongoing updates if API or model behavior changes.
  - Adds architectural complexity to the application layer.

## Follow-Up Actions

1. Keep orchestration modules documented.
