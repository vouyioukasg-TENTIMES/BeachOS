export interface CompletionContext {
  customer_group_id: string;
  status: 'ACTIVE' | 'COMPLETED';
  bill_status: 'OPEN' | 'FULLY_PAID' | 'CLOSED' | null;
  can_complete: boolean;
  next_action: string;
  service_location_status: 'OCCUPIED';
}

export interface CompletionResult {
  request_id: string;
  customer_group_id: string;
  status: 'COMPLETED';
  completed_by_id: string;
  completed_at: string;
  service_location_status: 'OCCUPIED';
  service_location_released: false;
}

export async function getCompletionContext(customerGroupId: string): Promise<CompletionContext> {
  const response = await fetch(
    `/api/customer-groups/${encodeURIComponent(customerGroupId)}/completion`,
  );
  if (!response.ok) throw new Error('Customer Group completion state could not be loaded.');
  return (await response.json()) as CompletionContext;
}

export async function completeCustomerGroup(
  customerGroupId: string,
  requestId: string,
): Promise<CompletionResult> {
  const response = await fetch(
    `/api/customer-groups/${encodeURIComponent(customerGroupId)}/complete`,
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
    throw new Error(body?.error?.message ?? 'Customer Group was not completed.');
  }
  return (await response.json()) as CompletionResult;
}
