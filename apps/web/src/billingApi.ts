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
  version: number;
}

export async function getRunningBill(customerGroupId: string): Promise<RunningBill | null> {
  const response = await fetch(
    `/api/billing/customer-groups/${encodeURIComponent(customerGroupId)}`,
  );
  if (!response.ok) throw new Error('The running Bill could not be loaded.');
  return (await response.json()) as RunningBill | null;
}
