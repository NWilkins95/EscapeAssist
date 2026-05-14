# Concurrency and Latency Optimization Decision

- Date: May 14, 2026
- Owner: Nicholas Wilkins

## Summary

On May 14, 2026, the project decision was made to reduce latency and token overhead by optimizing workflow execution with caching, shared async infrastructure, and duplicate-run removal.

## Context

Performance testing showed severe latency and high token usage because all three workflow/agent paths were being run together, creating repeated overhead on every prompt. This behavior increased response time and cost, and reduced scalability.

## Decision Drivers

1. Running all three workflow paths simultaneously caused unnecessary compute and token overhead.
2. Re-running workflow setup on every prompt increased latency.
3. Duplicate run commands introduced avoidable repeated execution.
4. A shared event loop model improves async execution efficiency in Streamlit workflows.
5. Caching workflow loading prevents redundant initialization work across prompts.

## Decision

Adopt a concurrency-focused optimization approach:
- Cache workflow loaders so workflows are initialized once and reused.
- Use a shared background event loop for async workflow execution.
- Remove duplicated run commands that trigger redundant processing.

## Consequences

- Positive:
  - Lower end-to-end prompt latency.
  - Reduced token usage from eliminating repeated workflow overhead.
  - Better runtime efficiency and smoother user interaction.
  - Cleaner control flow with fewer redundant execution paths.

- Trade-offs:
  - Added complexity in async lifecycle management.
  - Requires careful handling of shared loop/thread behavior.
  - Caching behavior must be monitored to avoid stale workflow state.

## Follow-Up Actions

1. Track latency and token metrics before/after optimization.
2. Periodically review execution paths to prevent duplicate runs.