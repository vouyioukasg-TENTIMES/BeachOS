export interface MenuItem {
  menu_item_id: string;
  name: string;
  category_name: string;
  unit_price: number;
  currency: string;
  destination: 'BAR' | 'KITCHEN' | 'NO PREPARATION';
}

export interface OrderItem extends MenuItem {
  order_item_id: string;
  quantity: number;
  amount: number;
  note: string | null;
}

export interface Order {
  order_id: string;
  customer_group_id: string;
  submitted_at: string;
  submitted_by_id: string;
  service_location_id: string;
  responsible_waiter_id: string;
  items: OrderItem[];
}

export interface Bill {
  bill_id: string;
  currency: string;
  total: number;
  line_count: number;
}

export interface OrderingContext {
  customer_group_id: string;
  venue_id: string;
  service_location_id: string;
  responsible_waiter_id: string;
  status: 'ACTIVE' | 'COMPLETED';
  orders: Order[];
  bill: Bill | null;
  menu_items: MenuItem[];
}

export interface SubmitOrderResult {
  request_id: string;
  order: Order;
  tickets: { ticket_id: string; destination: string; item_ids: string[] }[];
  bill: Bill | null;
}

export interface DraftItem {
  menu_item_id: string;
  quantity: number;
  note?: string;
}

export class OrderingApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'OrderingApiError';
    this.status = status;
  }
}

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(url, init);
  } catch {
    throw new OrderingApiError(
      'BeachOS cannot confirm the current result. Check the connection before continuing.',
      0,
    );
  }
  if (!response.ok) {
    let message = 'Ordering is temporarily unavailable.';
    try {
      const body = (await response.json()) as { error?: { message?: string } };
      message = body.error?.message ?? message;
    } catch {
      // Keep the safe operational message.
    }
    throw new OrderingApiError(message, response.status);
  }
  return (await response.json()) as T;
}

export function getOrderingContext(customerGroupId: string, signal?: AbortSignal) {
  const query = new URLSearchParams({ customer_group_id: customerGroupId });
  return request<OrderingContext>(`/ordering/context?${query.toString()}`, { signal });
}

export function submitOrder(customerGroupId: string, items: DraftItem[]) {
  return request<SubmitOrderResult>('/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      request_id: crypto.randomUUID(),
      customer_group_id: customerGroupId,
      items,
    }),
  });
}
