import type { Transaction } from "../types";

export function TransactionCard({ transaction, onSelect }: { transaction: Transaction; onSelect: () => void }) {
  return <button className="card transaction-card" onClick={onSelect} type="button">
    <span className="card__eyebrow">Transaction</span>
    <strong>{transaction.merchant}</strong>
    <span>${transaction.amount}</span>
    <small>{transaction.description} · {transaction.transaction_date}</small>
    <span className="card__action">Review this transaction</span>
  </button>;
}
