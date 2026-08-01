export interface BillLine {
  bill_line_id: string;
  description: string;
  quantity: number;
  unit_price: number;
  amount: number;
  currency: string;
  source: string;
  occurred_at: string;
}

export interface RunningBill {
  bill_id: string;
  customer_group_id: string;
  currency: string;
  total: number;
  balance: number;
  status: string;
  lines: BillLine[];
  payments: Payment[];
  version: number;
}

export interface Payment {
  payment_id: string;
  amount: number;
  currency: string;
  method: 'CASH';
  recorded_by_id: string;
  recorded_at: string;
}

export interface PaymentResult extends Payment {
  request_id: string;
  bill_id: string;
  customer_group_id: string;
  balance: number;
  bill_status: string;
}

export async function getRunningBill(customerGroupId: string): Promise<RunningBill | null> {
  const response = await fetch(
    `/api/billing/customer-groups/${encodeURIComponent(customerGroupId)}`,
  );
  if (!response.ok) throw new Error('The running Bill could not be loaded.');
  return (await response.json()) as RunningBill | null;
}

export async function recordFullCashPayment(
  customerGroupId: string,
  amount: number,
  currency: string,
  requestId: string,
): Promise<PaymentResult> {
  const response = await fetch('/api/payments/cash', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      request_id: requestId,
      customer_group_id: customerGroupId,
      amount,
      currency,
    }),
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as {
      error?: { message?: string };
    } | null;
    throw new Error(body?.error?.message ?? 'The Cash Payment was not recorded.');
  }
  return (await response.json()) as PaymentResult;
}
