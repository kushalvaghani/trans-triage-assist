import { useEffect, useRef, useState } from "react";
import logo from "./assets/westpac-logo.svg";
import { proposalOutcome, sendMessage, submitTriage } from "./api/client";
import { CaseCard } from "./components/CaseCard";
import { ChatMessage } from "./components/ChatMessage";
import { ChatWidget } from "./components/ChatWidget";
import { MerchantAlternatives } from "./components/MerchantAlternatives";
import { ProposalCard } from "./components/ProposalCard";
import { TriageQuestionCard } from "./components/TriageQuestionCard";
import { TransactionCard } from "./components/TransactionCard";
import type { Card, ChatEntry, Outcome, Transaction, TriageAnswers } from "./types";

const notFoundMessage = "Could not find the merchant, please search for other transactions";

function greeting(): ChatEntry {
  return { id: crypto.randomUUID(), role: "assistant", content: "Hello, I can help you report an issue with a transaction." };
}

export default function App() {
  const [entries, setEntries] = useState<ChatEntry[]>([greeting()]);
  const [correlationId, setCorrelationId] = useState(crypto.randomUUID());
  const [pending, setPending] = useState(false);
  const [selected, setSelected] = useState<Transaction>();
  const [answers, setAnswers] = useState<TriageAnswers>({});
  const [proposal, setProposal] = useState<Outcome>();
  const requestVersion = useRef(0);
  const transcript = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (transcript.current) transcript.current.scrollTop = transcript.current.scrollHeight;
  }, [entries]);

  const append = (entry: Omit<ChatEntry, "id">) => {
    setEntries((current) => [...current, { ...entry, id: crypto.randomUUID() }]);
  };

  const restart = () => {
    requestVersion.current += 1;
    setCorrelationId(crypto.randomUUID());
    setEntries([greeting()]);
    setSelected(undefined);
    setAnswers({});
    setProposal(undefined);
    setPending(false);
  };

  const report = async (message: string) => {
    append({ role: "customer", content: message });
    setPending(true);
    const version = requestVersion.current;
    try {
      const result = await sendMessage(message, correlationId);
      if (version !== requestVersion.current) return;
      append({ role: "assistant", content: result.response_type === "not_found" ? notFoundMessage : result.message });
      result.transactions.forEach((transaction) => append({ role: "assistant", content: "", card: { type: "transaction", transaction } }));
      if (result.response_type === "not_found" && result.alternative_merchants.length === 3) {
        append({ role: "assistant", content: "", card: { type: "alternatives", merchants: result.alternative_merchants } });
      }
    } catch (error) {
      if (version === requestVersion.current) append({ role: "assistant", content: error instanceof Error ? error.message : "We could not process that request." });
    } finally {
      if (version === requestVersion.current) setPending(false);
    }
  };

  const chooseTransaction = (transaction: Transaction) => {
    setSelected(transaction);
    setAnswers({});
    setProposal(undefined);
    append({ role: "customer", content: `Select ${transaction.merchant} for $${transaction.amount}` });
    append({ role: "assistant", content: "", card: { type: "question", question: "merchant_known" } });
  };

  const showProposal = (next: TriageAnswers) => {
    const outcome = proposalOutcome(next as Required<TriageAnswers>);
    setProposal(outcome);
    if (outcome === "merchant_refund_guidance") {
      append({ role: "assistant", content: "Please contact the merchant to complete the agreed refund.", card: { type: "case", nextSteps: ["Contact the merchant about the agreed refund."] } });
      return;
    }
    append({ role: "assistant", content: "", card: { type: "proposal", outcome, nextSteps: ["Review the proposed details.", "Confirm to create a mock case."] } });
  };

  const answer = (value: boolean) => {
    const next: TriageAnswers = { ...answers };
    if (answers.merchantKnown === undefined) {
      next.merchantKnown = value;
      setAnswers(next);
      append({ role: "customer", content: value ? "Yes" : "No" });
      if (!value) showProposal(next);
      else append({ role: "assistant", content: "", card: { type: "question", question: "merchant_refund_agreed" } });
      return;
    }
    if (answers.merchantRefundAgreed === undefined) {
      next.merchantRefundAgreed = value;
      setAnswers(next);
      append({ role: "customer", content: value ? "Yes" : "No" });
      if (value) showProposal(next);
      else append({ role: "assistant", content: "", card: { type: "question", question: "customer_made_purchase" } });
      return;
    }
    next.customerMadePurchase = value;
    setAnswers(next);
    append({ role: "customer", content: value ? "Yes" : "No" });
    showProposal(next);
  };

  const confirm = async () => {
    if (!selected || !proposal || proposal === "merchant_refund_guidance" || answers.merchantKnown === undefined) return;
    setPending(true);
    try {
      const result = await submitTriage(selected.transaction_id, answers as Required<TriageAnswers>, true, correlationId);
      append({ role: "assistant", content: result.message, card: result.case_id ? { type: "case", caseId: result.case_id, nextSteps: result.next_steps } : undefined });
    } catch (error) {
      append({ role: "assistant", content: error instanceof Error ? error.message : "We could not process that request." });
    } finally {
      setPending(false);
    }
  };

  const renderCard = (card?: Card) => {
    if (!card) return null;
    if (card.type === "transaction") return <TransactionCard onSelect={() => chooseTransaction(card.transaction)} transaction={card.transaction} />;
    if (card.type === "question") return <TriageQuestionCard onAnswer={answer} question={card.question} />;
    if (card.type === "proposal") return <ProposalCard nextSteps={card.nextSteps} onConfirm={confirm} outcome={card.outcome} />;
    if (card.type === "case") return <CaseCard caseId={card.caseId} nextSteps={card.nextSteps} />;
    return <MerchantAlternatives merchants={card.merchants} onSelect={(merchant) => report(`Report $50 at ${merchant}`)} />;
  };

  return <main className="app-shell"><section className="chat" aria-label="Transaction triage chat"><header className="chat__header"><img alt="Westpac" src={logo} /><span>Transaction Triage</span></header><div className="transcript" aria-live="polite" ref={transcript}>{entries.map((entry) => <ChatMessage key={entry.id} role={entry.role}>{entry.content && <p>{entry.content}</p>}{renderCard(entry.card)}</ChatMessage>)}</div><ChatWidget onRestart={restart} onSend={report} pending={pending} /></section></main>;
}
