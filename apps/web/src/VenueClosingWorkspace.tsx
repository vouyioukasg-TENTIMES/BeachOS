import { useCallback, useEffect, useState } from 'react';
import { closeVenue, getClosingContext, type ClosingContext } from './venueClosingApi';

export function VenueClosingWorkspace({ venueId }: { venueId: string }) {
  const [context, setContext] = useState<ClosingContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [closing, setClosing] = useState(false);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setContext(await getClosingContext(venueId));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Venue Closing is unavailable.');
    } finally {
      setLoading(false);
    }
  }, [venueId]);

  useEffect(() => void load(), [load]);

  async function confirmClose() {
    if (!context?.can_close || closing) return;
    const stableRequestId = requestId ?? crypto.randomUUID();
    setRequestId(stableRequestId);
    setClosing(true);
    setError(null);
    try {
      const result = await closeVenue(venueId, stableRequestId);
      setContext((current) =>
        current
          ? {
              ...current,
              status: 'CLOSED_FOR_BUSINESS_DATE',
              can_close: false,
              closing_report: result.closing_report,
            }
          : current,
      );
      setMessage(`Venue closed at ${new Date(result.closing_report.closed_at).toLocaleString()}.`);
      await load();
      setRequestId(null);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Venue Closing outcome is unknown.');
    } finally {
      setClosing(false);
    }
  }

  if (loading) return <main className="ordering-state">Loading Venue Closing…</main>;
  if (!context)
    return (
      <main className="ordering-state" role="alert">
        <h1>Venue Closing unavailable</h1>
        <p>{error}</p>
        <button onClick={() => void load()}>Retry</button>
      </main>
    );

  const readiness = context.readiness;
  return (
    <main className="ordering-workspace">
      <header className="ordering-header">
        <div>
          <p className="eyebrow">Venue Closing</p>
          <h1>{context.venue_id}</h1>
        </div>
        <div>
          <strong>{context.status}</strong>
          <p>{context.business_date}</p>
        </div>
      </header>
      {message && (
        <p className="status-message" role="status">
          {message}
        </p>
      )}
      <section className="draft-panel">
        <h2>Closing readiness</h2>
        <ul>
          <li>Active Customer Groups: {readiness.active_customer_groups}</li>
          <li>Occupied Service Locations: {readiness.occupied_service_locations}</li>
          <li>Open Bills: {readiness.open_bills}</li>
          <li>Unresolved operational work: {readiness.unresolved_operational_work}</li>
        </ul>
        {context.blockers.length > 0 && (
          <div className="blocking-message" role="alert">
            <strong>The Venue cannot close.</strong>
            <ul>
              {context.blockers.map((blocker) => (
                <li key={blocker}>{blocker}</li>
              ))}
            </ul>
          </div>
        )}
        <button disabled={!context.can_close || closing} onClick={() => void confirmClose()}>
          {closing ? 'Closing Venue…' : context.closing_report ? 'Venue closed' : 'Close Venue'}
        </button>
      </section>
      {context.closing_report && (
        <section className="draft-panel">
          <h2>Closing Report</h2>
          <p>Closed by {context.closing_report.closed_by_id}</p>
          <p>Closing time: {new Date(context.closing_report.closed_at).toLocaleString()}</p>
          <p>All approved closing checks were confirmed clear.</p>
        </section>
      )}
      {error && (
        <p className="blocking-message" role="alert">
          {error}{' '}
          {requestId
            ? 'Reload before retrying with the same request identity.'
            : 'Reload the closing context.'}
        </p>
      )}
    </main>
  );
}
