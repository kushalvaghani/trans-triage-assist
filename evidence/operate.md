# Operate

## Run locally

```bash
# API dependencies (Westpac index/certificates required in this environment)
UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/api --extra dev

uv run --directory src/api uvicorn api.app:app --host 127.0.0.1 --port 8765

# Separate terminal: UI
npm install --prefix src/ui
npm run dev --prefix src/ui -- --host 127.0.0.1 --port 5173
```

The Vite proxy forwards the API prefix to `http://127.0.0.1:8765`. The API exposes `POST`
`/exp-digiServicing-transctiontraige/v1/message` and `/submission`.

## Logs, status, and configuration

- Logs: `logs/<correlation-id>.jsonl`; each event contains the correlation ID and mock `user_id: 599`.
- Submission logs record triage answers, confirmation, final outcome, and generated case ID.
- `VITE_API_BASE_URL` can override the UI's same-origin API base; no secrets are required or stored.
- Static fixtures are in `sample_data/transactions.json`; logs, virtual environments, and UI build
  output are ignored by Git.

## Failure and rollback/degrade approach

- Invalid requests return safe customer messages and an associated correlation ID. 
- Unmatched searches return other merchant alternatives; merchant-refund outcomes do not create a case. 
- If the API is unavailable, the UI displays a safe processing error and creates no case. 
- Roll back by restoring the previous local revision and restarting the API/UI; no remote state or migrations exist.

## Local-to-cloud considerations

Before any cloud deployment, 
1. Replace mock user identity and fixtures with authenticated, authorised
systems. Integrate with PING or ISAM for user authentication
2. Package and deploy the UI, API and agent in Westpac controlled environment using the patterns. This can include Mesh or Next. Agents can live in AKS, Azure AI foundry or Google Agent Engine. Also using an agent framework like LangChain OR Googles ADK or Microsoft MAF will be ideal.
3. Add secure configuration/secrets management. For example triggering a LLM call or API to agent authentication.
4. Scale the API layers after understanding the user volume and growth in terms of TPS
5. Perform SIT, SVP and other testing to ensure the functionality works as expected. If LLM is used, perform evalautions.
6. Follow Westpac standard for encrypted central logging and retention rules,
observability, rate limiting, durable idempotency keys, health checks, and CI/CD controls.
7. If a controlled rollout of the feature is needed, then can use something like LaunchDarkly to rollout the feature
8. Work with stakeholders to validate the business process and functionality.
9. Triage questions can be implemented as a workflow agent with questions controlled in a workflow like Elsa
