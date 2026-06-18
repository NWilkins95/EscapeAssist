# UI Utils Refactor Decision

- Date: June 17, 2026
- Owner: Nicholas Wilkins

## Summary

Shared helper functions for the EscapeAssist UI will live in a dedicated utils module so the dashboard and EscapeAssist Vx pages stay smaller, cleaner, and easier to maintain.

## Context

The Streamlit dashboard and the EscapeAssist V0/V1/V2 pages had repeated helper logic for loading workflows, extracting responses, reading evaluation artifacts, and rendering common UI behaviors. Keeping those functions inline made the pages harder to read and made future edits more likely to drift across files.

## Decision

Move shared UI helper functions into a dedicated utils file and have the dashboard and EscapeAssist Vx pages import those helpers instead of duplicating them.

The shared module will own the reusable logic, while each page will keep only its page-specific layout and behavior.

## Why This Was Chosen

1. It reduces duplication across the UI pages.
2. It keeps the page files focused on layout rather than helper implementation.
3. It makes future updates to shared behavior easier and less error-prone.
4. It improves readability for the dashboard and model pages.
5. It gives the UI a clearer structure for maintenance over time.

## Consequences

- Positive:
  - Less repeated code across the dashboard and Vx pages.
  - Cleaner page files with a smaller maintenance surface.
  - Shared behavior changes can be made in one place.

- Trade-offs:
  - The shared utils module becomes a central dependency for the UI pages.
  - Imports must stay consistent so the pages continue to resolve the helper module correctly.

## Follow-Up Actions

1. Keep shared UI helpers in the utils module.
2. Import the shared helpers from the dashboard and EscapeAssist Vx pages.
3. Avoid reintroducing duplicated helper functions in the page files.