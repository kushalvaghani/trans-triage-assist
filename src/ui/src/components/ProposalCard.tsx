import type { Outcome } from "../types";

export function ProposalCard({ disabled, outcome, nextSteps, onConfirm }: { disabled: boolean; outcome: Outcome; nextSteps: string[]; onConfirm: () => void }) {
  const label = outcome === "fraud_scam" ? "Fraud/scam" : "Dispute";
  return <section className="card proposal-card"><span className="card__eyebrow">Proposed outcome</span><strong>{label}</strong><ul>{nextSteps.map((step) => <li key={step}>{step}</li>)}</ul><button disabled={disabled} onClick={onConfirm} type="button">{disabled ? "Case created" : "Confirm and create case"}</button></section>;
}
