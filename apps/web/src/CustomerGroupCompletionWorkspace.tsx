import { useCallback, useEffect, useState } from 'react';
import {
  completeCustomerGroup,
  getCompletionContext,
  type CompletionContext,
} from './completionApi';

export function CustomerGroupCompletionWorkspace({ customerGroupId }: { customerGroupId: string }) {
  const [context, setContext] = useState<CompletionContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [requestId, setRequestId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setContext(await getCompletionContext(customerGroupId));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Completion state is unavailable.');
    } finally {
      setLoading(false);
    }
  }, [customerGroupId]);

  useEffect(() => void load(), [load]);

  async function complete() {
    if (!context?.can_complete || completing) return;
    const stableRequestId = requestId ?? crypto.randomUUID();
    setRequestId(stableRequestId);
    setCompleting(true);
    setError(null);
    try {
      const result = await completeCustomerGroup(customerGroupId, stableRequestId);
      setContext((current) =>
        current
          ? { ...current, status: 'COMPLETED', can_complete: false, next_action: 'NONE' }
          : current,
      );
      setMessage(
        `Customer Group completed by ${result.completed_by_id}. Service Location remains occupied.`,
      );
      await load();
      setRequestId(null);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Completion outcome is unknown.');
    } finally {
      setCompleting(false);
    }
  }

  if (loading) return <main className="ordering-state">Loading Customer Group completion…</main>;
  if (!context)
    return (
      <main className="ordering-state" role="alert">
        <h1>Completion unavailable</h1>
        <p>{error}</p>
        <button onClick={() => void load()}>Retry</button>
      </main>
    );

  return (
    <main className="ordering-workspace">
      <header className="ordering-header">
        <div>
          <p className="eyebrow">Customer Group Completion</p>
          <h1>{context.customer_group_id}</h1>
        </div>
        <div>
          <strong>{context.status}</strong>
          <p>Bill: {context.bill_status ?? 'No Bill'}</p>
        </div>
      </header>
      {message && (
        <p className="status-message" role="status">
          {message}
        </p>
      )}
      <section className="draft-panel">
        <h2>End operational service</h2>
        <p>
          The Service Location remains occupied after completion. Departure and release are
          separate.
        </p>
        <button disabled={!context.can_complete || completing} onClick={() => void complete()}>
          {completing
            ? 'Completing Customer Group…'
            : context.status === 'COMPLETED'
              ? 'Customer Group completed'
              : 'Complete Customer Group'}
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
