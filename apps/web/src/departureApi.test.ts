import { afterEach, describe, expect, it, vi } from 'vitest';
import { departCustomerGroup, getDepartureContext } from './departureApi';

afterEach(() => vi.unstubAllGlobals());

describe('Guest Departure API', () => {
  it('loads the completed group and occupied location facts', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            customer_group_id: 'group-1',
            customer_group_status: 'COMPLETED',
            departure_status: 'NOT_DEPARTED',
            service_location_id: 'location-1',
            service_location_name: 'Upper Table 1',
            service_location_status: 'OCCUPIED',
            can_depart: true,
            next_action: 'DEPART_CUSTOMER_GROUP',
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getDepartureContext('group-1')).can_depart).toBe(true);
  });

  it('confirms departure and immediate availability', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            request_id: 'request-1',
            customer_group_id: 'group-1',
            customer_group_status: 'COMPLETED',
            departure_status: 'DEPARTED',
            service_location_id: 'location-1',
            service_location_name: 'Upper Table 1',
            service_location_status: 'AVAILABLE',
            departed_by_id: 'staff-1',
            departed_at: '2026-08-01T18:10:00Z',
          }),
          { status: 200 },
        ),
      ),
    );
    const result = await departCustomerGroup('group-1', 'request-1');
    expect(result.departure_status).toBe('DEPARTED');
    expect(result.service_location_status).toBe('AVAILABLE');
  });

  it('preserves the backend rejection explanation', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ error: { message: 'only a COMPLETED Customer Group may depart' } }),
            { status: 409 },
          ),
        ),
    );
    await expect(departCustomerGroup('group-1', 'request-1')).rejects.toThrow('COMPLETED');
  });
});
