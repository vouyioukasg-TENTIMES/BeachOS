import { afterEach, describe, expect, it, vi } from 'vitest';
import { completeCustomerGroup, getCompletionContext } from './completionApi';

afterEach(() => vi.unstubAllGlobals());

describe('Customer Group Completion API', () => {
  it('loads completion readiness including no-Bill support', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            customer_group_id: 'group-1',
            status: 'ACTIVE',
            bill_status: null,
            can_complete: true,
            next_action: 'COMPLETE_CUSTOMER_GROUP',
            service_location_status: 'OCCUPIED',
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getCompletionContext('group-1')).can_complete).toBe(true);
  });

  it('completes without releasing the Service Location', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            request_id: 'request-1',
            customer_group_id: 'group-1',
            status: 'COMPLETED',
            completed_by_id: 'staff-1',
            completed_at: '2026-08-01T18:10:00Z',
            service_location_status: 'OCCUPIED',
            service_location_released: false,
          }),
          { status: 200 },
        ),
      ),
    );
    const result = await completeCustomerGroup('group-1', 'request-1');
    expect(result.service_location_released).toBe(false);
  });

  it('preserves backend rejection messages', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ error: { message: 'Bill must already be CLOSED' } }), {
          status: 409,
        }),
      ),
    );
    await expect(completeCustomerGroup('group-1', 'request-1')).rejects.toThrow('CLOSED');
  });
});
