import type { Outcome } from "../types";

export function ProposalCard({ outcome, nextSteps, onConfirm }: { outcome: Outcome; nextSteps: string[]; onConfirm: () => void }) {
  const label = outcome === "fraud_scam" ? "Fraud/scam" : "Dispute";
  return <section className="card proposal-card"><span className="card__eyebrow">Proposed outcome</span><strong>{label}</strong><ul>{nextSteps.map((step) => <li key={step}>{step}</li>)}</ul><button onClick={onConfirm} type="button">Confirm and create mock case</button></section>;
}
