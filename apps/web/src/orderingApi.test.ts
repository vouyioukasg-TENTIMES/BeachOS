import { afterEach, describe, expect, it, vi } from 'vitest';
import { getOrderingContext, OrderingApiError, submitOrder } from './orderingApi';

afterEach(() => vi.unstubAllGlobals());

describe('Ordering API', () => {
  it('loads the real Ordering context contract', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            customer_group_id: 'group-1',
            venue_id: 'venue-1',
            service_location_id: 'B-12',
            responsible_waiter_id: 'waiter-1',
            status: 'ACTIVE',
            orders: [],
            bill: null,
            menu_items: [],
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getOrderingContext('group-1')).service_location_id).toBe('B-12');
  });

  it('submits a reviewed order round', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ request_id: 'r', order: {}, tickets: [], bill: null }), {
          status: 200,
        }),
      ),
    );
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });
    const result = await submitOrder('group-1', [{ menu_item_id: 'coffee', quantity: 1 }]);
    expect(result.request_id).toBe('r');
  });

  it('preserves the backend business message', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ error: { message: 'Customer Group is completed' } }), {
          status: 409,
        }),
      ),
    );
    await expect(getOrderingContext('group-1')).rejects.toMatchObject({
      message: 'Customer Group is completed',
      status: 409,
    });
  });

  it('marks an unconfirmed network outcome distinctly', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));
    await expect(submitOrder('group-1', [])).rejects.toBeInstanceOf(OrderingApiError);
    await expect(submitOrder('group-1', [])).rejects.toMatchObject({ status: 0 });
  });
});
