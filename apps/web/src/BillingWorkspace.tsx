import { useEffect, useState } from 'react';
import { getRunningBill, type RunningBill } from './billingApi';

export function BillingWorkspace({ customerGroupId }: { customerGroupId: string }) {
  const [bill, setBill] = useState<RunningBill | null | undefined>();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setBill(undefined);
    setError(null);
    void getRunningBill(customerGroupId)
      .then(setBill)
      .catch((reason: unknown) =>
        setError(reason instanceof Error ? reason.message : 'Bill unavailable.'),
      );
  }, [customerGroupId]);

  if (error)
    return (
      <main className="ordering-state" role="alert">
        <h1>Billing unavailable</h1>
        <p>{error}</p>
      </main>
    );
  if (bill === undefined) return <main className="ordering-state">Loading running Bill…</main>;
  if (bill === null)
    return (
      <main className="ordering-state">
        <h1>No Bill</h1>
        <p>This Customer Group has no confirmed Financial Obligation.</p>
      </main>
    );

  return (
    <main className="ordering-workspace">
      <header className="ordering-header">
        <div>
          <p className="eyebrow">Running Bill</p>
          <h1>{bill.bill_id}</h1>
          <p>Customer Group: {bill.customer_group_id}</p>
        </div>
        <div>
          <strong>
            {bill.balance.toFixed(2)} {bill.currency}
          </strong>
          <p>{bill.status}</p>
        </div>
      </header>
      <section>
        <h2>Confirmed financial obligations</h2>
        {bill.lines.map((line) => (
          <article className="menu-row" key={line.bill_line_id}>
            <div>
              <strong>{line.description}</strong>
              <p>
                {line.quantity} × {line.unit_price.toFixed(2)} · {line.source}
              </p>
            </div>
            <span>
              {line.amount.toFixed(2)} {line.currency}
            </span>
          </article>
        ))}
      </section>
    </main>
  );
}
