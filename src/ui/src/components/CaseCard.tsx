export function CaseCard({ caseId, nextSteps }: { caseId?: string; nextSteps: string[] }) {
  return <section className="card case-card"><span className="card__eyebrow">{caseId ? "Mock case created" : "Next steps"}</span>{caseId && <strong>{caseId}</strong>}<ul>{nextSteps.map((step) => <li key={step}>{step}</li>)}</ul></section>;
}
