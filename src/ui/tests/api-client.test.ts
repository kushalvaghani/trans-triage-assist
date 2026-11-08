import { describe, expect, it, vi } from "vitest";
import { sendMessage } from "../src/api/client";

describe("API client", () => {
  it("sends the correlation ID with a customer message", async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ correlation_id: "id", message: "Found", response_type: "transaction_matches", transactions: [], alternative_merchants: [] }) });
    vi.stubGlobal("fetch", fetchMock);
    await sendMessage("Report $50 at Woolworths", "id");
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining("/message"), expect.objectContaining({ body: expect.stringContaining('"correlation_id":"id"') }));
  });
});
