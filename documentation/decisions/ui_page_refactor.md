# UI Page Refactor Decision

- Date: June 17, 2026
- Owner: Nicholas Wilkins

## Summary

The EscapeAssist Streamlit UI pages will use shared helper functions from one utils module so the page files stay clean, focused, and easier to maintain.

## Context

The dashboard and EscapeAssist Vx pages had repeated UI logic for chat rendering, evaluation loading, metrics, exports, and run controls. Keeping that logic directly in each page made the files harder to scan and increased the chance of inconsistent updates.

## Decision

Refactor the Streamlit UI so that reusable functions live in a single utils module and the individual page files only import and call those shared functions.

The pages will keep their page-specific text and setup, while the common behavior stays centralized.

## Why This Was Chosen

1. It removes duplicated code from the UI pages.
2. It keeps the page files small and easier to read.
3. It makes shared behavior easier to update in one place.
4. It reduces maintenance cost as the UI grows.
5. It keeps the Streamlit pages focused on presentation instead of helper implementation.

## Consequences

- Positive:
  - Cleaner UI page files.
  - Shared logic is easier to test and reuse.
  - Future UI changes are less likely to drift across pages.

- Trade-offs:
  - The utils module becomes the central place for UI behavior.
  - Page imports must stay aligned with the shared helper API.

## Follow-Up Actions

1. Keep shared UI functions in the utils module.
2. Import shared helpers from the dashboard and EscapeAssist Vx pages.
3. Avoid reintroducing page-local copies of the shared UI logic.