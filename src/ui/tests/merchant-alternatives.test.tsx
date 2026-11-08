import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { MerchantAlternatives } from "../src/components/MerchantAlternatives";

describe("merchant alternatives", () => {
  it("renders exactly three alternatives and makes the selected merchant actionable", () => {
    const select = vi.fn();
    render(<MerchantAlternatives merchants={["Coles", "Aldi", "ZeroCoffee", "AlphaShop"]} onSelect={select} />);
    expect(screen.getAllByRole("button")).toHaveLength(3);
    fireEvent.click(screen.getByText("Coles"));
    expect(select).toHaveBeenCalledWith("Coles");
  });
});
