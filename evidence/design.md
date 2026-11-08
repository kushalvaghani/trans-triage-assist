# Design

## Architecture and data flow

```diagram
[React/Vite chat UI]
        |
        | POST /message, /submission + correlation ID
        v
[FastAPI mock API] ---> [sample_data/transactions.json]
        |
        +--> [logs/<correlation-id>.jsonl]

[Deterministic Python agent] ---> [sample_data/transactions.json]
        |
        +--> [logs/<correlation-id>.jsonl]
```

- `src/ui` owns transcript state, cards, restart, and the explicit confirmation control.
- `src/api` owns HTTP validation, PII masking, matching, triage evaluation, case-ID generation, and
  API session logging.
- `src/agent` owns an independently testable deterministic reasoning state machine for a future API
  integration. It does not expose HTTP.
- `sample_data/transactions.json` is shared static fixture data; `logs/` holds ignored local JSONL
  session files.

## Key choices and trade-offs

- **Deterministic functions over LLM calls:** predictable and auditable local behaviour, at the cost
  of limited natural-language coverage.
- **Explicit confirmation:** protects against automatic case creation; the UI disables the control
  after a successful submission to prevent duplicate IDs.
- **Static JSON over a database:** simple, reproducible demonstrator; no durable uniqueness across
  process restarts or concurrent multi-instance deployment.
- **API boundary for UI:** the UI never reads sample data or imports agent code. The current API does
  not yet delegate to `transaction_agent.engine.process_interaction`; this is intentional current
  separation, not completed end-to-end agent wiring.

## Security and privacy

The API regex-masks PII before reasoning or logging. Logs include correlation ID, mock `user_id: 599`,
transaction ID, triage answers, outcome, and case ID. Logs are local, ignored from Git, and must not
be treated as a production retention solution.

## Technology and likely production shape

React/TypeScript/Vite provides the chat UI; FastAPI/Pydantic provides the API; Python/Ruff/Pytest
supports the API and agent. However, while implementing in Westpac, the below would be my considerations :

In Westpac production terms, we would host the UI inside a platform like Mesh or Next inside an MFE or presentation layer. The UI can be built in React Typescript OR NextJS. 

API can be hosted as an experience API on Mesh or Next. API would sit behind an authenticated gateway. The user would signin and a auth provider such as PING or ISAM would generate a user token. API would verify the user and start the chat flow. Although the exercise uses a REST endpoint, chat could use persistent connection such as websockets or HTTP streaming. There is a possibility of using A2UI. Logging and traceability should follow the Westpac standards such as Splunk without any PII data.

The current agent is a determinstic python function. However, as I have done in the past, this could be a real-agent deployed in Azure AI Foundy or Google Agent engine. Access to fetching transactions would be a tool call sitting behind an internal MCP server. Also tool calls would be using On-behalf-of authentication to make sure the transactions are only retrieved for the user. Further, agent intent would move from string matching to an LLM. Appropraite guardrails would be considered and in place. LLMs in future would only drive intent matching. Factual information and aggregation still comes from tool calls and APIs.


