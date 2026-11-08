# Agentic Workflow

## Tools and workflow

- Used the Specify constitution, specification, planning, task-generation, and implementation
  workflows to establish separate API, agent, and UI artifacts.
- Used local shell commands to inspect source, run UV/Pytest/Ruff and npm/Vitest/ESLint/Vite checks,
  start the local API/UI, and exercise HTTP flows.
- Used headless Chrome through the Chrome DevTools protocol to inspect the default, transaction,
  triage, and confirmed-case UI states.

## Decomposition and steering

Work was separated into three component scopes: `src/api`, `src/agent`, and `src/ui`, with shared
mock data at project level. Representative steering constraints were:

- “100% Mocked Architecture” and no external LLM or banking integration.
- “Immutable Verdict” requiring a manual confirmation control.
- “Specifications should always be generated per component.”
- “Every session should have a log file with a correlation ID.”

## Human interventions and review

I reviewed the generated and existing code against the component contracts, then directed focused
refinements: nine-character alphanumeric case IDs, a confirmation button that disables after case
creation, top-level session logs, mock user ID 599, and logging of triage answers and case IDs. For
each refinement, I reviewed the resulting diff and source paths, ran or reviewed the relevant tests
and lint/build checks, exercised the API flow, and visually inspected the affected UI state where
applicable. Further, apart from a code review, I supplied precise instructions to specify on the use case and the flow reviewing each step of the generated output.
