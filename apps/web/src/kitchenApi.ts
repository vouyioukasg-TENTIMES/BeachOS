export interface KitchenTicketItem {
  order_item_id: string;
  name: string;
  quantity: number;
  note: string | null;
}

export interface KitchenTicket {
  ticket_id: string;
  order_id: string;
  customer_group_id: string;
  venue_id: string;
  submission_service_location_id: string;
  current_service_location_id: string;
  responsible_service_staff_id: string;
  submitted_at: string;
  items: KitchenTicketItem[];
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

export interface KitchenContext {
  venue_id: string;
  awaiting_acknowledgement_count: number;
  tickets: KitchenTicket[];
}

export class KitchenApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'KitchenApiError';
    this.status = status;
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(url, init);
  } catch {
    throw new KitchenApiError(
      'BeachOS cannot confirm the current Kitchen result. Check the connection before continuing.',
      0,
    );
  }
  if (!response.ok) {
    let message = 'Kitchen Operations is temporarily unavailable.';
    try {
      const body = (await response.json()) as { error?: { message?: string } };
      message = body.error?.message ?? message;
    } catch {
      // Keep the safe operational message.
    }
    throw new KitchenApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export function getKitchenContext(venueId: string, signal?: AbortSignal) {
  const query = new URLSearchParams({ venue_id: venueId });
  return request<KitchenContext>(`/kitchen/context?${query.toString()}`, { signal });
}

export function acknowledgeKitchenTicket(ticketId: string) {
  return request<{ request_id: string; ticket: KitchenTicket }>(
    `/kitchen/tickets/${encodeURIComponent(ticketId)}/acknowledge`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: crypto.randomUUID() }),
    },
  );
}

export function progressKitchenTicket(ticketId: string, action: string) {
  return request<{ request_id: string; ticket: KitchenTicket }>(
    `/kitchen/tickets/${encodeURIComponent(ticketId)}/${action.toLowerCase()}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: crypto.randomUUID() }),
    },
  );
}
