import type { ReactNode } from "react";

export function ChatMessage({ role, children }: { role: "customer" | "assistant"; children: ReactNode }) {
  return <article className={`message message--${role}`}>{children}</article>;
}
