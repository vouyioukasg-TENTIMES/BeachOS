import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  getOrderingContext,
  type MenuItem,
  OrderingApiError,
  type OrderingContext,
  submitOrder,
} from './orderingApi';

interface DraftLine {
  item: MenuItem;
  quantity: number;
  note: string;
}

export function OrderingWorkspace({ customerGroupId }: { customerGroupId: string }) {
  const [context, setContext] = useState<OrderingContext | null>(null);
  const [draft, setDraft] = useState<Record<string, DraftLine>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [uncertain, setUncertain] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setMessage(null);
    try {
      setContext(await getOrderingContext(customerGroupId));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Ordering could not be loaded.');
    } finally {
      setLoading(false);
    }
  }, [customerGroupId]);

  useEffect(() => {
    void load();
  }, [load]);

  const total = useMemo(
    () => Object.values(draft).reduce((sum, line) => sum + line.item.unit_price * line.quantity, 0),
    [draft],
  );

  function add(item: MenuItem) {
    setDraft((current) => ({
      ...current,
      [item.menu_item_id]: current[item.menu_item_id] ?? { item, quantity: 1, note: '' },
    }));
  }

  async function submit() {
    if (!context || Object.keys(draft).length === 0 || submitting) return;
    setSubmitting(true);
    setMessage(null);
    setUncertain(false);
    try {
      const result = await submitOrder(
        context.customer_group_id,
        Object.values(draft).map((line) => ({
          menu_item_id: line.item.menu_item_id,
          quantity: line.quantity,
          note: line.note || undefined,
        })),
      );
      setContext({
        ...context,
        orders: [...context.orders, result.order],
        bill: result.bill,
      });
      setDraft({});
      setMessage(`Order round submitted. ${result.tickets.length} preparation ticket(s) created.`);
    } catch (error) {
      setUncertain(error instanceof OrderingApiError && error.status === 0);
      setMessage(error instanceof Error ? error.message : 'The Order was not submitted.');
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <main className="ordering-state">Loading current Customer Group…</main>;
  if (!context)
    return (
      <main className="ordering-state" role="alert">
        <h1>Ordering unavailable</h1>
        <p>{message}</p>
        <button onClick={() => void load()}>Retry</button>
      </main>
    );

  const disabled = context.status !== 'ACTIVE';
  return (
    <main className="ordering-workspace">
      <header className="ordering-header">
        <div>
          <p className="eyebrow">Customer Group</p>
          <h1>{context.service_location_id}</h1>
          <p>Responsible service staff: {context.responsible_waiter_id}</p>
        </div>
        <div>
          <strong>{context.orders.length} order round(s)</strong>
          <p>
            Running bill: {context.bill ? `${context.bill.total} ${context.bill.currency}` : 'None'}
          </p>
        </div>
      </header>

      {disabled && (
        <p className="blocking-message">
          This Customer Group is completed. New Orders are not allowed.
        </p>
      )}
      {message && (
        <p className={uncertain ? 'blocking-message' : 'status-message'} role="status">
          {message}
          {uncertain && ' Do not repeat the action until the current Customer Group is reloaded.'}
        </p>
      )}

      <div className="ordering-columns">
        <section>
          <h2>Available menu</h2>
          {context.menu_items.length === 0 ? (
            <p>No Menu Items are currently available.</p>
          ) : (
            context.menu_items.map((item) => (
              <article className="menu-row" key={item.menu_item_id}>
                <div>
                  <strong>{item.name}</strong>
                  <p>
                    {item.category_name} · {item.destination}
                  </p>
                </div>
                <span>
                  {item.unit_price} {item.currency}
                </span>
                <button disabled={disabled} onClick={() => add(item)}>
                  Add
                </button>
              </article>
            ))
          )}
        </section>

        <section className="draft-panel">
          <h2>Current order round</h2>
          {Object.values(draft).length === 0 ? (
            <p>No items selected. Add reviewed items from the current menu.</p>
          ) : (
            Object.values(draft).map((line) => (
              <article className="draft-row" key={line.item.menu_item_id}>
                <strong>{line.item.name}</strong>
                <label>
                  Quantity
                  <input
                    aria-label={`${line.item.name} quantity`}
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={line.quantity}
                    onChange={(event) =>
                      setDraft((current) => ({
                        ...current,
                        [line.item.menu_item_id]: {
                          ...line,
                          quantity: Number(event.target.value),
                        },
                      }))
                    }
                  />
                </label>
                <label>
                  Preparation note
                  <input
                    value={line.note}
                    onChange={(event) =>
                      setDraft((current) => ({
                        ...current,
                        [line.item.menu_item_id]: { ...line, note: event.target.value },
                      }))
                    }
                  />
                </label>
                <button
                  className="text-button"
                  onClick={() =>
                    setDraft((current) => {
                      const next = { ...current };
                      delete next[line.item.menu_item_id];
                      return next;
                    })
                  }
                >
                  Remove
                </button>
              </article>
            ))
          )}
          <div className="order-total">Round total: {total.toFixed(2)}</div>
          <button
            className="primary-action"
            disabled={disabled || submitting || Object.keys(draft).length === 0}
            onClick={() => void submit()}
          >
            {submitting ? 'Submitting order round…' : 'Submit order round'}
          </button>
          <button className="text-button" disabled={submitting} onClick={() => void load()}>
            Reload current group
          </button>
        </section>
      </div>
    </main>
  );
}
