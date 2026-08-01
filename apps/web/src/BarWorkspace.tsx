import { useCallback, useEffect, useState } from 'react';
import {
  acknowledgeBarTicket,
  type BarContext,
  BarApiError,
  type BarTicket,
  getBarContext,
  progressBarTicket,
} from './barApi';

export function BarWorkspace({ venueId }: { venueId: string }) {
  const [context, setContext] = useState<BarContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTicketId, setActiveTicketId] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [uncertain, setUncertain] = useState(false);
  const load = useCallback(async () => {
    setLoading(true);
    setMessage(null);
    try {
      setContext(await getBarContext(venueId));
    } catch (error) {
      setContext(null);
      setMessage(error instanceof Error ? error.message : 'Bar work could not be loaded.');
    } finally {
      setLoading(false);
    }
  }, [venueId]);
  useEffect(() => void load(), [load]);
  async function acknowledge(ticket: BarTicket) {
    setActiveTicketId(ticket.ticket_id);
    setMessage(null);
    setUncertain(false);
    try {
      const result =
        ticket.status === 'NEW'
          ? await acknowledgeBarTicket(ticket.ticket_id)
          : await progressBarTicket(ticket.ticket_id, 'mark_ready');
      setContext((current) =>
        current
          ? {
              ...current,
              awaiting_acknowledgement_count: Math.max(
                0,
                current.awaiting_acknowledgement_count - 1,
              ),
              tickets: current.tickets.map((item) =>
                item.ticket_id === result.ticket.ticket_id ? result.ticket : item,
              ),
            }
          : current,
      );
      setMessage(`Bar Ticket ${ticket.ticket_id} is now ${result.ticket.status}.`);
    } catch (error) {
      setUncertain(error instanceof BarApiError && error.status === 0);
      setMessage(error instanceof Error ? error.message : 'Acknowledgement was not confirmed.');
    } finally {
      setActiveTicketId(null);
    }
  }
  if (loading) return <main className="kitchen-state">Loading confirmed Bar work…</main>;
  if (!context)
    return (
      <main className="kitchen-state" role="alert">
        <h1>Bar Operations unavailable</h1>
        <p>{message}</p>
        <button onClick={() => void load()}>Retry</button>
      </main>
    );
  return (
    <main className="kitchen-workspace">
      <header className="kitchen-header">
        <div>
          <p className="eyebrow">Bar Operations</p>
          <h1>Confirmed Bar work</h1>
          <p>Venue: {context.venue_id}</p>
        </div>
        <div className="kitchen-summary">
          <strong>{context.awaiting_acknowledgement_count}</strong>
          <span>awaiting acknowledgement</span>
        </div>
      </header>
      <p className="operational-guidance">
        Acknowledge only when the Bar has recognized the Ticket as active work. BeachOS does not
        infer preparation priority, readiness, delivery, or completion.
      </p>
      {message && (
        <p className={uncertain ? 'blocking-message' : 'status-message'} role="status">
          {message}
          {uncertain && ' Do not repeat the action until the current Bar context is reloaded.'}
        </p>
      )}
      <section aria-label="Bar Tickets">
        {context.tickets.length === 0 ? (
          <div className="kitchen-empty">
            <h2>No confirmed Bar work</h2>
            <p>No Bar Tickets currently exist for this Venue.</p>
          </div>
        ) : (
          context.tickets.map((ticket) => (
            <article className="kitchen-ticket" key={ticket.ticket_id}>
              <header>
                <div>
                  <p className="eyebrow">Ticket {ticket.ticket_id}</p>
                  <h2>{ticket.current_service_location_id}</h2>
                  {ticket.current_service_location_id !== ticket.submission_service_location_id && (
                    <p>Submitted at {ticket.submission_service_location_id}</p>
                  )}
                </div>
                <strong>{ticket.status}</strong>
              </header>
              <p>
                Submitted {new Date(ticket.submitted_at).toLocaleTimeString()} · Responsible service
                staff: {ticket.responsible_service_staff_id}
              </p>
              <ul>
                {ticket.items.map((item) => (
                  <li key={item.order_item_id}>
                    <strong>
                      {item.quantity} × {item.name}
                    </strong>
                    {item.note && <span> — {item.note}</span>}
                  </li>
                ))}
              </ul>
              {ticket.status === 'NEW' || ticket.status === 'ACKNOWLEDGED' ? (
                <button
                  className="primary-action"
                  disabled={activeTicketId !== null}
                  onClick={() => void acknowledge(ticket)}
                >
                  {activeTicketId === ticket.ticket_id
                    ? 'Confirming outcome…'
                    : ticket.status === 'NEW'
                      ? 'Acknowledge Bar Ticket'
                      : 'Mark Bar Ticket READY'}
                </button>
              ) : (
                <p>
                  {ticket.status} · Current responsibility: {ticket.current_responsibility} · Next
                  action: {ticket.next_action}
                </p>
              )}
            </article>
          ))
        )}
      </section>
      <button
        className="text-button"
        disabled={activeTicketId !== null}
        onClick={() => void load()}
      >
        Reload confirmed work
      </button>
    </main>
  );
}
