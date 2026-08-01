import { useEffect, useState } from 'react';
import { getRunningBill, recordFullCashPayment, type RunningBill } from './billingApi';

export function BillingWorkspace({ customerGroupId }: { customerGroupId: string }) {
  const [bill, setBill] = useState<RunningBill | null | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [paying, setPaying] = useState(false);
  const [paymentRequestId, setPaymentRequestId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [paymentError, setPaymentError] = useState<string | null>(null);

  useEffect(() => {
    setBill(undefined);
    setError(null);
    void getRunningBill(customerGroupId)
      .then(setBill)
      .catch((reason: unknown) =>
        setError(reason instanceof Error ? reason.message : 'Bill unavailable.'),
      );
  }, [customerGroupId]);

  async function payInCash() {
    if (!bill || bill.balance <= 0 || paying) return;
    const requestId = paymentRequestId ?? crypto.randomUUID();
    setPaymentRequestId(requestId);
    setPaying(true);
    setPaymentError(null);
    try {
      await recordFullCashPayment(customerGroupId, bill.balance, bill.currency, requestId);
      setBill(await getRunningBill(customerGroupId));
      setPaymentRequestId(null);
      setMessage('Full Cash Payment recorded. The Bill Balance is zero.');
    } catch (reason) {
      setPaymentError(reason instanceof Error ? reason.message : 'Payment outcome is unknown.');
    } finally {
      setPaying(false);
    }
  }

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
      <section className="draft-panel">
        <h2>Payment</h2>
        {message && (
          <p className="status-message" role="status">
            {message}
          </p>
        )}
        {bill.payments.length > 0 ? (
          bill.payments.map((payment) => (
            <p key={payment.payment_id}>
              {payment.amount.toFixed(2)} {payment.currency} · Cash · confirmed by{' '}
              {payment.recorded_by_id}
            </p>
          ))
        ) : (
          <p>No confirmed Payment has been recorded.</p>
        )}
        <button disabled={paying || bill.balance === 0} onClick={() => void payInCash()}>
          {paying
            ? 'Recording Cash Payment…'
            : bill.balance === 0
              ? 'Fully paid'
              : `Record full Cash Payment · ${bill.balance.toFixed(2)} ${bill.currency}`}
        </button>
        {paymentError && paymentRequestId && (
          <p className="blocking-message" role="alert">
            {paymentError} Reload the Bill before deciding whether to retry. Retrying this action
            uses the same request identity.
          </p>
        )}
      </section>
    </main>
  );
}
