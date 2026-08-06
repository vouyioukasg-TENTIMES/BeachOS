export interface DepartureContext {
  customer_group_id: string;
  customer_group_status: 'ACTIVE' | 'COMPLETED';
  departure_status: 'NOT_DEPARTED' | 'DEPARTED';
  service_location_id: string;
  service_location_name: string;
  service_location_status: 'OCCUPIED' | 'AVAILABLE';
  can_depart: boolean;
  next_action: string;
}

export interface DepartureResult {
  request_id: string;
  customer_group_id: string;
  customer_group_status: 'COMPLETED';
  departure_status: 'DEPARTED';
  service_location_id: string;
  service_location_name: string;
  service_location_status: 'AVAILABLE';
  departed_by_id: string;
  departed_at: string;
}

export async function getDepartureContext(customerGroupId: string): Promise<DepartureContext> {
  const response = await fetch(
    `/api/customer-groups/${encodeURIComponent(customerGroupId)}/departure`,
  );
  if (!response.ok) throw new Error('Guest Departure context could not be loaded.');
  return (await response.json()) as DepartureContext;
}

export async function departCustomerGroup(
  customerGroupId: string,
  requestId: string,
): Promise<DepartureResult> {
  const response = await fetch(
    `/api/customer-groups/${encodeURIComponent(customerGroupId)}/depart`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: requestId }),
    },
  );
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as {
      error?: { message?: string };
    } | null;
    throw new Error(body?.error?.message ?? 'Guest Departure was not confirmed.');
  }
  return (await response.json()) as DepartureResult;
}
