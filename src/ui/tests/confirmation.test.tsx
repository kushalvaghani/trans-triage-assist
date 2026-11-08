import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CaseCard } from "../src/components/CaseCard";
import { ProposalCard } from "../src/components/ProposalCard";

describe("confirmation cards", () => {
  afterEach(cleanup);

  it("requires an explicit confirm click and renders local case details", () => {
    const confirm = vi.fn();
    render(<><ProposalCard nextSteps={["Review details"]} onConfirm={confirm} outcome="dispute" /><CaseCard caseId="MOCK-DISPUTE-TXN-001" nextSteps={["Keep this ID"]} /></>);
    expect(confirm).not.toHaveBeenCalled();
    fireEvent.click(screen.getByText("Confirm and create mock case"));
    expect(confirm).toHaveBeenCalledOnce();
    expect(screen.getByText("MOCK-DISPUTE-TXN-001")).toBeInTheDocument();
  });

  it("shows merchant-refund guidance without a confirmation control", () => {
    render(<CaseCard nextSteps={["Contact the merchant about the agreed refund."]} />);
    expect(screen.getByText("Next steps")).toBeInTheDocument();
    expect(screen.queryByText("Confirm and create mock case")).not.toBeInTheDocument();
  });
});
