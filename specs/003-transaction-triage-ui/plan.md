# Implementation Plan: Transaction Triage Chat UI

**Branch**: `003-transaction-triage-ui` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-transaction-triage-ui/spec.md`

## Summary

Build a React TypeScript chat widget under `src/ui` that calls only the local transaction-triage API.
The UI begins with a greeting, Westpac logo, and report preset; it renders messages chronologically,
uses transcript cards for transactions/questions/proposals/cases, supports scrolling and restart, and
requires an explicit confirmation before a case submission.

## Technical Context

**Language/Version**: TypeScript 5+ with React 18+

**Primary Dependencies**: Vite, React, React DOM, Vitest, React Testing Library, ESLint

**Storage**: Browser-only transcript/session state; correlation ID stored in session state and sent to
the local API; no direct mock-data access

**Testing**: Vitest, React Testing Library, and a browser smoke test against the local API

**Target Platform**: Modern desktop and mobile browsers served by a local Vite development server

**Project Type**: React single-page chat widget

**Performance Goals**: Render each transcript entry immediately and auto-scroll new content into view
without removing prior messages

**Constraints**: No live banking/cloud/LLM services; only the documented local API; no automatic case
submission; all structured content remains inside chat transcript cards

**Scale/Scope**: One local customer journey, two API POST paths, greeting/search/triage/preview/
confirmation/case/restart/error states

## Constitution Check

**Pre-design gate: PASS with an API integration dependency.**

- The UI is React-only, relies on the local API, and does not read `sample_data` or agent code.
- Greeting, Westpac branding, cards, scrollable transcript, preset, redirection, and restart are
  explicit UI states.
- A proposal is visualized before its distinct confirmation action; the UI never submits a case on
  its own.
- The UI passes a correlation ID and renders customer-safe failures.
- The current API needs agent integration or a compatible session contract before it can return the
  specified transaction-selection and sequential-triage states. This is a delivery dependency, not a
  reason to bypass the API.

**Post-design gate: PASS.** The adapter contract isolates this dependency and preserves the API-only
architecture.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/ui/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── styles.css
│   ├── api/client.ts              # Local API adapter; correlation propagation
│   ├── types.ts                   # API and chat-state contracts
│   ├── components/
│   │   ├── ChatWidget.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── TransactionCard.tsx
│   │   ├── TriageQuestionCard.tsx
│   │   ├── ProposalCard.tsx
│   │   ├── CaseCard.tsx
│   │   └── MerchantAlternatives.tsx
│   └── assets/westpac-logo.svg    # Local brand asset or approved text mark
└── tests/
    ├── chat-widget.test.tsx
    ├── transaction-cards.test.tsx
    ├── confirmation.test.tsx
    ├── merchant-alternatives.test.tsx
    └── api-client.test.ts
```

**Structure Decision**: Keep the UI independently runnable in `src/ui`; put all transport in one API
client so components never contact mock data or agent code directly.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations require justification.
