---

description: "Implementation tasks for the transaction triage chat UI"
---

# Tasks: Transaction Triage Chat UI

**Input**: Design documents from `/specs/003-transaction-triage-ui/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/transaction-triage-ui-api.md`, and `quickstart.md`

**Tests**: Required by the feature success criteria. Write each test before its implementation and
confirm it fails on the preceding implementation state.

**Organization**: Tasks are grouped by user story so each increment is independently testable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the independently runnable React UI and quality tooling under `src/ui`.

- [X] T001 Create the Vite React TypeScript application manifest and scripts in `src/ui/package.json`.
- [X] T002 Create TypeScript, Vite, Vitest, and ESLint configuration in `src/ui/tsconfig.json`, `src/ui/vite.config.ts`, and `src/ui/eslint.config.js`.
- [X] T003 [P] Create the Vite HTML entry point and React bootstrap in `src/ui/index.html` and `src/ui/src/main.tsx`.
- [X] T004 [P] Add UI build/cache/environment patterns to `.gitignore` for `src/ui/node_modules/`, `src/ui/dist/`, and `src/ui/.env*`.
- [X] T005 Install and lock UI dependencies in `src/ui/package-lock.json`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Provide typed transcript state, API-only transport, safe errors, and reusable chat
layout before any user story.

**⚠️ CRITICAL**: Complete this phase before user-story work.

- [X] T006 Create typed chat session, entry, card, transaction, proposal, and API payload contracts in `src/ui/src/types.ts`, including the rule that `correlationId` is a UUID and `pendingProposal` is nullable.
- [X] T007 Create the API client in `src/ui/src/api/client.ts` for the two documented POST paths, passing `correlation_id` and mapping customer-safe errors without importing agent code or reading `sample_data`.
- [X] T008 [P] Create a local Westpac wordmark/logo asset in `src/ui/src/assets/westpac-logo.svg`.
- [X] T009 Create shared transcript, card, scroll, focus, responsive, and Westpac-themed styles in `src/ui/src/styles.css`.
- [X] T010 Verify and record the API session-contract dependency in `specs/003-transaction-triage-ui/contracts/transaction-triage-ui-api.md`; do not work around it through direct fixture or agent access.

**Checkpoint**: The UI can render typed transcript entries and call only the local API adapter.

---

## Phase 3: User Story 1 - Start a Transaction Report (Priority: P1) 🎯 MVP

**Goal**: Start a greeted chat, submit the preset or customer text, and display messages in order.

**Independent Test**: Render a new session, verify greeting/logo/preset/input/restart, use the preset,
and verify the customer text and a mocked API response appear in transcript order.

### Tests for User Story 1

- [X] T011 [P] [US1] Write greeting, Westpac logo, preset label, input placeholder, and restart tests in `src/ui/tests/chat-widget.test.tsx`.
- [ ] T013 [US1] Write chronological customer/service transcript tests in `src/ui/tests/chat-widget.test.tsx`.

### Implementation for User Story 1

- [X] T014 [US1] Implement greeted session initialization, UUID creation, restart invalidation, and append-only entries in `src/ui/src/App.tsx`.
- [X] T015 [US1] Implement the chat widget, preset “Report $50 at Woolworths”, input placeholder “Report $100 at ZeroCoffeeShop”, send action, and restart action in `src/ui/src/components/ChatWidget.tsx`.
- [X] T016 [US1] Implement role-aligned chronological chat messages in `src/ui/src/components/ChatMessage.tsx`.
- [X] T017 [US1] Connect message submission and redirection/error rendering through `src/ui/src/api/client.ts` and `src/ui/src/App.tsx`.

**Checkpoint**: A customer can start, send, see a response, and restart a transaction-report chat.

---

## Phase 4: User Story 2 - Review Transaction and Triage Cards (Priority: P2)

**Goal**: Render transaction choices, questions, proposals, confirmation, refund guidance, and case
details as transcript cards while preventing automatic submission.

**Independent Test**: Use mocked service states to select a transaction, answer questions, review a
proposal, explicitly confirm it, and observe a case card; verify merchant-refund guidance has no
confirmation control.

### Tests for User Story 2

- [ ] T018 [P] [US2] Write selectable transaction-card and scrollable-transcript tests in `src/ui/tests/transaction-cards.test.tsx`.
- [X] T019 [P] [US2] Write question-card and active-answer-only submission tests in `src/ui/tests/transaction-cards.test.tsx`.
- [X] T020 [P] [US2] Write proposal/explicit-confirmation/case-card and refund-guidance tests in `src/ui/tests/confirmation.test.tsx`.

### Implementation for User Story 2

- [X] T021 [US2] Implement transaction card rendering and selection callbacks in `src/ui/src/components/TransactionCard.tsx`.
- [X] T022 [US2] Implement question-card yes/no controls that submit only the active answer in `src/ui/src/components/TriageQuestionCard.tsx`.
- [X] T023 [US2] Implement proposal preview with a distinct explicit confirmation action in `src/ui/src/components/ProposalCard.tsx`.
- [X] T024 [US2] Implement merchant-refund guidance and confirmed case ID/next-step rendering in `src/ui/src/components/CaseCard.tsx`.
- [X] T025 [US2] Integrate card result mapping, current-proposal validation, stale-response rejection, and API calls in `src/ui/src/App.tsx` and `src/ui/src/api/client.ts`.

**Checkpoint**: Cards remain inside the transcript; no Fraud/scam or Dispute case can be submitted
without the current proposal's explicit confirmation.

---

## Phase 5: User Story 3 - Recover from an Unmatched Merchant (Priority: P3)

**Goal**: Display the prescribed not-found message and exactly three API-provided merchant
alternatives, then search the selected alternative.

**Independent Test**: Mock a not-found response, verify exact copy and exactly three alternatives,
select one, and verify the new API search and transaction cards.

### Tests for User Story 3

- [ ] T026 [P] [US3] Write exact not-found-copy, exactly-three-alternatives, and alternative-search tests in `src/ui/tests/merchant-alternatives.test.tsx`.
- [ ] T027 [P] [US3] Write malformed alternative-response and request-failure customer-safe error tests in `src/ui/tests/merchant-alternatives.test.tsx`.

### Implementation for User Story 3

- [X] T028 [US3] Implement API-supplied merchant alternative cards and selection callbacks in `src/ui/src/components/MerchantAlternatives.tsx`.
- [X] T029 [US3] Enforce the exact required not-found text, exactly-three presentation rule, and safe malformed-response fallback in `src/ui/src/App.tsx`.
- [X] T030 [US3] Submit selected alternatives through the API client and append resulting transaction cards in `src/ui/src/api/client.ts` and `src/ui/src/App.tsx`.

**Checkpoint**: An unavailable merchant recovers through three visible, usable alternatives without
direct sample-data access.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate visual behavior, accessibility, API integration, and quality gates.

- [X] T031 [P] Add accessible labels, keyboard focus order, live status updates, and semantic card controls in `src/ui/src/components/`.
- [ ] T032 [P] Add narrow-viewport and overflow transcript coverage in `src/ui/tests/chat-widget.test.tsx` and `src/ui/src/styles.css`.
- [X] T033 Run and correct `npm test -- --run`, `npm run lint`, and `npm run build` from `src/ui/`.
- [ ] T034 Run the live API smoke flow from `specs/003-transaction-triage-ui/quickstart.md` after the API session contract is available, capture screenshots of default and card states, and update `evidence/verify.md`.
- [X] T035 Remove unused Vite boilerplate, unsupported mock paths, and dead UI state from `src/ui/`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** starts immediately.
- **Foundational (Phase 2)** depends on setup and blocks all stories.
- **US1 (Phase 3)** depends on typed state and the API client.
- **US2 (Phase 4)** depends on US1 transcript behavior and the API session-contract dependency.
- **US3 (Phase 5)** depends on US1 response rendering but can use mocked not-found responses while API
  session integration is pending.
- **Polish (Phase 6)** depends on desired user stories and the API session contract for live validation.

### User Story Dependencies

- **US1 (P1)** is the MVP and independently delivers greeting, message submission, response display,
  and restart.
- **US2 (P2)** needs a compatible API session contract for live triage selection and questions.
- **US3 (P3)** can be implemented/tested against the API client mock after US1 and completed live once
  the API response contract supplies alternatives.

### Parallel Opportunities

- T003–T004 can run alongside T001–T002; T008 can run alongside T006–T007.
- T011 and T012 can run in parallel; T018–T020 can run in parallel; T026–T027 can run in parallel.
- T031 and T032 can run in parallel after all card components are implemented.

## Parallel Example: User Story 2

```text
Task: "T018 transaction-card tests in src/ui/tests/transaction-cards.test.tsx"
Task: "T020 confirmation tests in src/ui/tests/confirmation.test.tsx"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete setup and foundational API-only boundaries.
2. Deliver a greeted, restartable transcript with preset message submission.
3. Validate message, redirection, and error rendering with a mocked API client.

### Incremental Delivery

1. Deliver US1 chat start and transcript.
2. Add US2 cards and explicit confirmation after the API session contract is available.
3. Add US3 merchant-recovery cards.
4. Complete live browser validation, linting, build, screenshots, and evidence update.
