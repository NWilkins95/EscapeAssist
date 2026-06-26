# UI Utils Folder Split Decision

- Date: June 24, 2026
- Owner: Nicholas Wilkins

## Summary

The EscapeAssist UI helper code will be split from a single large utils file into a utils folder with smaller, task-specific modules so the codebase is easier to maintain and reason about.

## Context

The UI layer had grown beyond a single flat helper file. It contained data loading, chart rendering, dashboard layout, chat workflow helpers, and async execution logic in one place. That made the module harder to navigate, increased the chance of unrelated edits affecting each other, and made the separation between data prep, rendering, and page behavior less clear.

## Decision

Move the UI helper code into a dedicated utils package with individual files organized by responsibility.

The new structure will keep related functions together, such as evaluation data helpers, chart rendering helpers, dashboard orchestration, chat helpers, and async runner support. Page files will import from the relevant module instead of relying on one large shared file.

## Why This Was Chosen

1. It improves separation of concerns by grouping related logic together.
2. It makes the code easier to find and understand.
3. It reduces the size and complexity of any single module.
4. It makes future maintenance and targeted edits less risky.
5. It supports cleaner imports and a more obvious UI module structure.

## Consequences

- Positive:
  - Smaller modules with clearer responsibilities.
  - Easier maintenance for charts, data loading, dashboard behavior, and chat behavior.
  - Less chance of accidental coupling between unrelated UI concerns.

- Trade-offs:
  - More files to manage.
  - Imports need to stay aligned with the folder structure.
  - A compatibility layer may be needed during the transition so existing callers keep working.

## Follow-Up Actions

1. Keep the UI helper modules split by concern.
2. Update page imports to use the new package modules.
3. Avoid reintroducing new unrelated helpers into a single monolithic UI file.