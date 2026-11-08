import type { ApiMessageResponse, ApiSubmissionResponse, Outcome } from "../types";

// Vite proxies this local path during development; deployments can set a local API base URL.
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";
const PREFIX = "/exp-digiServicing-transctiontraige/v1";

interface SafeError {
  correlation_id?: string;
  message?: string;
}

async function request<T>(path: string, payload: object): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${PREFIX}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const body = (await response.json()) as T & SafeError;
    if (!response.ok) throw new Error(body.message ?? "We could not process that request.");
    return body;
  } catch (error) {
    throw new Error(error instanceof Error ? error.message : "We could not process that request.");
  }
}

export function sendMessage(message: string, correlationId: string): Promise<ApiMessageResponse> {
  return request<ApiMessageResponse>("/message", { message, correlation_id: correlationId });
}

export function submitTriage(
  transactionId: string,
  answers: { merchantKnown: boolean; merchantRefundAgreed?: boolean; customerMadePurchase?: boolean },
  confirmed: boolean,
  correlationId: string,
): Promise<ApiSubmissionResponse> {
  return request<ApiSubmissionResponse>("/submission", {
    transaction_id: transactionId,
    merchant_known: answers.merchantKnown,
    merchant_refund_agreed: answers.merchantRefundAgreed,
    customer_made_purchase: answers.customerMadePurchase,
    confirmed,
    correlation_id: correlationId,
  });
}

export function proposalOutcome(answers: {
  merchantKnown: boolean;
  merchantRefundAgreed?: boolean;
  customerMadePurchase?: boolean;
}): Outcome {
  if (!answers.merchantKnown || answers.customerMadePurchase === false) return "fraud_scam";
  if (answers.merchantRefundAgreed) return "merchant_refund_guidance";
  return "dispute";
}
