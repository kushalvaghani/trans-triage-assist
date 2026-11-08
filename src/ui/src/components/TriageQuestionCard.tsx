import type { Question } from "../types";

const prompts: Record<Question, string> = {
  merchant_known: "Is the merchant known to you?",
  merchant_refund_agreed: "Did you contact the merchant and did they agree to refund?",
  customer_made_purchase: "Did you make the purchase?",
};

export function TriageQuestionCard({ question, onAnswer }: { question: Question; onAnswer: (answer: boolean) => void }) {
  return <section className="card question-card" aria-label="Triage question">
    <span className="card__eyebrow">A quick question</span>
    <strong>{prompts[question]}</strong>
    <div className="card__actions"><button onClick={() => onAnswer(true)} type="button">Yes</button><button className="button--secondary" onClick={() => onAnswer(false)} type="button">No</button></div>
  </section>;
}
