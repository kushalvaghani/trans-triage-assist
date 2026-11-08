import { FormEvent, useState } from "react";

const PRESET = "Report $50 at Woolworths";

export function ChatWidget({ onSend, onRestart, pending }: { onSend: (message: string) => void; onRestart: () => void; pending: boolean }) {
  const [message, setMessage] = useState("");
  const submit = (event: FormEvent) => { event.preventDefault(); if (message.trim() && !pending) { onSend(message.trim()); setMessage(""); } };
  return <form className="composer" onSubmit={submit}><button className="preset" onClick={() => setMessage(PRESET)} type="button">{PRESET}</button><div className="composer__row"><label className="sr-only" htmlFor="chat-message">Transaction report</label><input id="chat-message" onChange={(event) => setMessage(event.target.value)} placeholder="Report $100 at ZeroCoffeeShop" value={message} /><button disabled={pending || !message.trim()} type="submit">Send</button><button className="button--secondary" onClick={onRestart} type="button">Restart</button></div></form>;
}
