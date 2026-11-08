export function MerchantAlternatives({ merchants, onSelect }: { merchants: string[]; onSelect: (merchant: string) => void }) {
  return <section className="card alternatives-card"><span className="card__eyebrow">Try another merchant</span><div className="merchant-list">{merchants.slice(0, 3).map((merchant) => <button key={merchant} onClick={() => onSelect(merchant)} type="button">{merchant}</button>)}</div></section>;
}
