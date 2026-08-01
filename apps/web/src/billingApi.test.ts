import { afterEach, describe, expect, it, vi } from 'vitest';
import { getRunningBill } from './billingApi';

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
});
