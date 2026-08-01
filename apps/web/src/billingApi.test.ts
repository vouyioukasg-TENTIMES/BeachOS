import { afterEach, describe, expect, it, vi } from 'vitest';
import { closeFullyPaidBill, getRunningBill, recordFullCashPayment } from './billingApi';

afterEach(() => vi.unstubAllGlobals());

describe('Billing API', () => {
  it('loads the authoritative running Bill', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            bill_id: 'bill-1',
            customer_group_id: 'group-1',
            currency: 'EUR',
            total: 28,
            balance: 28,
            status: 'OPEN',
            lines: [],
            payments: [],
            closed_by_id: null,
            closed_at: null,
            version: 3,
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getRunningBill('group-1'))?.total).toBe(28);
    expect(fetch).toHaveBeenCalledWith('/api/billing/customer-groups/group-1');
  });

  it('preserves the no-Bill state', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('null', { status: 200 })));
    expect(await getRunningBill('group-1')).toBeNull();
  });

  it('does not hide load failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('', { status: 503 })));
    await expect(getRunningBill('group-1')).rejects.toThrow('could not be loaded');
  });

  it('records one confirmed full Cash Payment with a stable request identity', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            request_id: 'request-1',
            payment_id: 'payment-1',
            bill_id: 'bill-1',
            customer_group_id: 'group-1',
            amount: 28,
            currency: 'EUR',
            method: 'CASH',
            recorded_by_id: 'cashier-1',
            recorded_at: '2026-08-01T18:00:00Z',
            balance: 0,
            bill_status: 'FULLY_PAID',
          }),
          { status: 200 },
        ),
      ),
    );
    const payment = await recordFullCashPayment('group-1', 28, 'EUR', 'request-1');
    expect(payment.balance).toBe(0);
    expect(fetch).toHaveBeenCalledWith(
      '/api/payments/cash',
      expect.objectContaining({ body: expect.stringContaining('request-1') }),
    );
  });

  it('closes a fully paid Bill with a stable request identity', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            request_id: 'close-1',
            bill_id: 'bill-1',
            customer_group_id: 'group-1',
            status: 'CLOSED',
            closed_by_id: 'cashier-1',
            closed_at: '2026-08-01T18:05:00Z',
            customer_group_status: 'ACTIVE',
            service_location_status: 'OCCUPIED',
          }),
          { status: 200 },
        ),
      ),
    );
    const result = await closeFullyPaidBill('group-1', 'close-1');
    expect(result.customer_group_status).toBe('ACTIVE');
    expect(result.service_location_status).toBe('OCCUPIED');
  });
});
