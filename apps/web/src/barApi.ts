export interface BarTicketItem {
  order_item_id: string;
  name: string;
  quantity: number;
  note: string | null;
}
export interface BarTicket {
  ticket_id: string;
  order_id: string;
  customer_group_id: string;
  venue_id: string;
  submission_service_location_id: string;
  current_service_location_id: string;
  responsible_service_staff_id: string;
  submitted_at: string;
  items: BarTicketItem[];
  status: 'NEW' | 'ACKNOWLEDGED' | 'READY' | 'COLLECTED' | 'DELIVERED';
  acknowledged_by_id: string | null;
  acknowledged_at: string | null;
  ready_by_id: string | null;
  ready_at: string | null;
  collected_by_id: string | null;
  collected_at: string | null;
  delivered_by_id: string | null;
  delivered_at: string | null;
  current_responsibility: string;
  current_responsible_person_id: string;
  next_action: 'ACKNOWLEDGE' | 'MARK_READY' | 'COLLECT' | 'DELIVER' | 'NONE';
}
export interface BarContext {
  venue_id: string;
  awaiting_acknowledgement_count: number;
  tickets: BarTicket[];
}
export class BarApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'BarApiError';
    this.status = status;
  }
}
async function request<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(url, init);
  } catch {
    throw new BarApiError(
      'BeachOS cannot confirm the current Bar result. Check the connection before continuing.',
      0,
    );
  }
  if (!response.ok) {
    let message = 'Bar Operations is temporarily unavailable.';
    try {
      const body = (await response.json()) as { error?: { message?: string } };
      message = body.error?.message ?? message;
    } catch {
      // Keep the safe operational message.
    }
    throw new BarApiError(message, response.status);
  }
  return (await response.json()) as T;
}
export function getBarContext(venueId: string, signal?: AbortSignal) {
  return request<BarContext>(`/bar/context?${new URLSearchParams({ venue_id: venueId })}`, {
    signal,
  });
}
export function acknowledgeBarTicket(ticketId: string) {
  return request<{ request_id: string; ticket: BarTicket }>(
    `/bar/tickets/${encodeURIComponent(ticketId)}/acknowledge`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: crypto.randomUUID() }),
    },
  );
}

export function progressBarTicket(ticketId: string, action: string) {
  return request<{ request_id: string; ticket: BarTicket }>(
    `/bar/tickets/${encodeURIComponent(ticketId)}/${action.toLowerCase()}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: crypto.randomUUID() }),
    },
  );
}
