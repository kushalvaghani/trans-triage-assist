# Quickstart: Transaction Triage Chat UI

## Prerequisites

- Node.js 20+ and npm
- Local API dependencies installed under `src/api/`
- API running at the UI-configured local base URL

## Run locally

```bash
cd src/ui
npm install
npm run dev
```

## Validate manually

1. Open a new chat and verify the greeting, Westpac logo, preset label, input placeholder, and restart
   action are visible.
2. Use “Report $50 at Woolworths”; verify customer and service messages appear in chronological order.
3. Select a transaction, progress through question cards, and confirm a proposal only through the
   explicit confirmation control.
4. Search an unavailable merchant; verify the exact not-found text and exactly three alternatives.
5. Restart during a pending request; verify the new greeted chat ignores the old response.
6. Narrow the chat viewport and verify the transcript remains scrollable.

## Automated checks

```bash
cd src/ui
npm test -- --run
npm run lint
npm run build
```
