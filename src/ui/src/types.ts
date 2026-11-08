export type ResponseType = "transaction_matches" | "not_found" | "redirection" | "error";
export type Outcome = "fraud_scam" | "dispute" | "merchant_refund_guidance";
export type Question = "merchant_known" | "merchant_refund_agreed" | "customer_made_purchase";

export interface Transaction {
  transaction_id: string;
  customer_id: string;
  merchant: string;
  amount: string;
  transaction_date: string;
  description: string;
}

export interface ApiMessageResponse {
  correlation_id: string;
  message: string;
  response_type: ResponseType;
  transactions: Transaction[];
  alternative_merchants: string[];
}

export interface ApiSubmissionResponse {
  correlation_id: string;
  outcome: Outcome;
  message: string;
  next_steps: string[];
  case_id: string | null;
}

export type Card =
  | { type: "transaction"; transaction: Transaction }
  | { type: "question"; question: Question }
  | { type: "proposal"; outcome: Outcome; nextSteps: string[] }
  | { type: "case"; caseId?: string; nextSteps: string[] }
  | { type: "alternatives"; merchants: string[] };

export interface ChatEntry {
  id: string;
  role: "customer" | "assistant";
  content: string;
  card?: Card;
}

export interface TriageAnswers {
  merchantKnown?: boolean;
  merchantRefundAgreed?: boolean;
  customerMadePurchase?: boolean;
}
