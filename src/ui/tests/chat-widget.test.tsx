import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "../src/App";

describe("chat widget", () => {
  it("shows greeting, branding, preset, and restart", () => {
    render(<App />);
    expect(screen.getByAltText("Westpac")).toBeInTheDocument();
    expect(screen.getByText("Report $50 at Woolworths")).toBeInTheDocument();
    expect(screen.getByText(/Hello, I can help/i)).toBeInTheDocument();
    fireEvent.click(screen.getByText("Restart"));
    expect(screen.getByText(/Hello, I can help/i)).toBeInTheDocument();
  });
});
