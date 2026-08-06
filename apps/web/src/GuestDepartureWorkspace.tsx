import { useCallback, useEffect, useState } from 'react';
import { departCustomerGroup, getDepartureContext, type DepartureContext } from './departureApi';

export function GuestDepartureWorkspace({ customerGroupId }: { customerGroupId: string }) {
  const [context, setContext] = useState<DepartureContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [departing, setDeparting] = useState(false);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setContext(await getDepartureContext(customerGroupId));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Guest Departure is unavailable.');
    } finally {
      setLoading(false);
    }
  }, [customerGroupId]);

  useEffect(() => void load(), [load]);

  async function depart() {
    if (!context?.can_depart || departing) return;
    const stableRequestId = requestId ?? crypto.randomUUID();
    setRequestId(stableRequestId);
    setDeparting(true);
    setError(null);
    try {
      const result = await departCustomerGroup(customerGroupId, stableRequestId);
      setContext((current) =>
        current
          ? {
              ...current,
              departure_status: 'DEPARTED',
              service_location_status: 'AVAILABLE',
              can_depart: false,
              next_action: 'NONE',
            }
          : current,
      );
      setMessage(
        `${result.service_location_name} is AVAILABLE. Guest Departure was confirmed by ${result.departed_by_id}.`,
      );
      await load();
      setRequestId(null);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Departure outcome is unknown.');
    } finally {
      setDeparting(false);
    }
  }

  if (loading) return <main className="ordering-state">Loading Guest Departure…</main>;
  if (!context)
    return (
      <main className="ordering-state" role="alert">
        <h1>Guest Departure unavailable</h1>
        <p>{error}</p>
        <button onClick={() => void load()}>Retry</button>
      </main>
    );

  return (
    <main className="ordering-workspace">
      <header className="ordering-header">
        <div>
          <p className="eyebrow">Guest Departure</p>
          <h1>{context.customer_group_id}</h1>
        </div>
        <div>
          <strong>{context.departure_status}</strong>
          <p>Customer Group: {context.customer_group_status}</p>
        </div>
      </header>
      {message && (
        <p className="status-message" role="status">
          {message}
        </p>
      )}
      <section className="draft-panel">
        <h2>{context.service_location_name}</h2>
        <p>
          Service Location status: <strong>{context.service_location_status}</strong>
        </p>
        <p>
          Departure is separate from Customer Group Completion. Confirm it only after the guests
          have departed.
        </p>
        <button disabled={!context.can_depart || departing} onClick={() => void depart()}>
          {departing
            ? 'Confirming Guest Departure…'
            : context.departure_status === 'DEPARTED'
              ? 'Guest Departure confirmed'
              : 'Confirm Guest Departure'}
        </button>
        {error && (
          <p className="blocking-message" role="alert">
            {error}{' '}
            {requestId
              ? 'Reload before retrying with the same request identity.'
              : 'Reload to confirm the current authoritative state.'}
          </p>
        )}
      </section>
    </main>
  );
}
