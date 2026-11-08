import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { TriageQuestionCard } from "../src/components/TriageQuestionCard";
import { TransactionCard } from "../src/components/TransactionCard";

describe("transaction and triage cards", () => {
  it("selects a transaction and sends only the selected question answer", () => {
    const select = vi.fn();
    const answer = vi.fn();
    render(<><TransactionCard onSelect={select} transaction={{ transaction_id: "txn-001", customer_id: "mock-customer-001", merchant: "Woolworths", amount: "50.00", transaction_date: "2026-10-01", description: "Groceries" }} /><TriageQuestionCard onAnswer={answer} question="merchant_known" /></>);
    fireEvent.click(screen.getByText("Review this transaction"));
    fireEvent.click(screen.getByText("No"));
    expect(select).toHaveBeenCalledOnce();
    expect(answer).toHaveBeenCalledWith(false);
  });
});
