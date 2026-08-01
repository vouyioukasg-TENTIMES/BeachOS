import { useCallback, useEffect, useState } from 'react';
import { getKitchenContext, progressKitchenTicket, type KitchenTicket } from './kitchenApi';
import { getBarContext, progressBarTicket, type BarTicket } from './barApi';

type Work = (KitchenTicket | BarTicket) & { destination: 'KITCHEN' | 'BAR' };

export function FulfilmentWorkspace({ venueId }: { venueId: string }) {
  const [work, setWork] = useState<Work[]>([]);
  const [loading, setLoading] = useState(true);
  const [active, setActive] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [uncertain, setUncertain] = useState(false);
  const load = useCallback(async () => {
    setLoading(true);
    setMessage(null);
    try {
      const [k, b] = await Promise.all([getKitchenContext(venueId), getBarContext(venueId)]);
      setWork([
        ...k.tickets.map((t) => ({ ...t, destination: 'KITCHEN' as const })),
        ...b.tickets.map((t) => ({ ...t, destination: 'BAR' as const })),
      ]);
      setUncertain(false);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Fulfilment could not be confirmed.');
      setUncertain(true);
    } finally {
      setLoading(false);
    }
  }, [venueId]);
  useEffect(() => void load(), [load]);
  async function progress(item: Work) {
    setActive(item.ticket_id);
    setMessage(null);
    setUncertain(false);
    try {
      const result =
        item.destination === 'KITCHEN'
          ? await progressKitchenTicket(item.ticket_id, item.next_action)
          : await progressBarTicket(item.ticket_id, item.next_action);
      setWork((current) =>
        current.map((value) =>
          value.ticket_id === item.ticket_id && value.destination === item.destination
            ? { ...result.ticket, destination: item.destination }
            : value,
        ),
      );
      setMessage(`${item.destination} Ticket ${item.ticket_id} is now ${result.ticket.status}.`);
    } catch (error) {
      setUncertain(true);
      setMessage(error instanceof Error ? error.message : 'The outcome could not be confirmed.');
    } finally {
      setActive(null);
    }
  }
  if (loading) return <main className="kitchen-state">Loading confirmed fulfilment work…</main>;
  return (
    <main className="kitchen-workspace">
      <header className="kitchen-header">
        <div>
          <p className="eyebrow">Fulfilment</p>
          <h1>From preparation to guest delivery</h1>
          <p>Venue: {venueId}</p>
        </div>
        <div className="kitchen-summary">
          <strong>{work.filter((t) => t.status !== 'DELIVERED').length}</strong>
          <span>outstanding Tickets</span>
        </div>
      </header>
      <p className="operational-guidance">
        READY means department work is finished and available for collection. DELIVERED means the
        whole Ticket reached the correct Customer Group.
      </p>
      {message && (
        <p className={uncertain ? 'blocking-message' : 'status-message'} role="status">
          {message}
          {uncertain && ' Reload confirmed work before repeating the action.'}
        </p>
      )}
      <section aria-label="Fulfilment Tickets">
        {work.length === 0 ? (
          <div className="kitchen-empty">
            <h2>No fulfilment work</h2>
            <p>No Kitchen or Bar Tickets exist for this Venue.</p>
          </div>
        ) : (
          work.map((item) => (
            <article className="kitchen-ticket" key={`${item.destination}-${item.ticket_id}`}>
              <header>
                <div>
                  <p className="eyebrow">
                    {item.destination} · {item.ticket_id}
                  </p>
                  <h2>{item.current_service_location_id}</h2>
                  <p>Customer Group {item.customer_group_id}</p>
                </div>
                <strong>{item.status}</strong>
              </header>
              <p>Responsible service staff: {item.responsible_service_staff_id}</p>
              <p>
                <strong>Current responsibility:</strong> {item.current_responsibility} (
                {item.current_responsible_person_id}) · <strong>Next action:</strong>{' '}
                {item.next_action}
              </p>
              <ul>
                {item.items.map((i) => (
                  <li key={i.order_item_id}>
                    <strong>
                      {i.quantity} × {i.name}
                    </strong>
                    {i.note && <span> — {i.note}</span>}
                  </li>
                ))}
              </ul>
              {item.next_action !== 'NONE' && item.next_action !== 'ACKNOWLEDGE' && (
                <button
                  className="primary-action"
                  disabled={active !== null}
                  onClick={() => void progress(item)}
                >
                  {active === item.ticket_id
                    ? 'Confirming outcome…'
                    : item.next_action.replace('_', ' ')}
                </button>
              )}
            </article>
          ))
        )}
      </section>
      <button className="text-button" disabled={active !== null} onClick={() => void load()}>
        Reload confirmed work
      </button>
    </main>
  );
}
