import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  getGuestArrivalContext,
  identifyArrivalLocation,
  openArrivalCustomerGroup,
} from './guestArrivalApi';
afterEach(() => vi.unstubAllGlobals());
describe('Guest Arrival API', () => {
  it('loads current arrival facts', async () => {
    const body = {
      venue_id: 'venue-1',
      venue_name: 'Emerald',
      business_date: '2026-08-01',
      venue_open: true,
      operational_confidence: 'CONFIRMED',
      locations: [],
    };
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValue(new Response(JSON.stringify(body), { status: 200 }));
    vi.stubGlobal('fetch', fetchMock);
    await expect(getGuestArrivalContext('venue-1')).resolves.toEqual(body);
    expect(fetchMock).toHaveBeenCalledWith(
      '/guest-arrival/context?venue_id=venue-1',
      expect.anything(),
    );
  });
  it('identifies by stable identity', async () => {
    const location = { service_location_id: 'a12' };
    vi.stubGlobal(
      'fetch',
      vi
        .fn<typeof fetch>()
        .mockResolvedValue(new Response(JSON.stringify(location), { status: 200 })),
    );
    await expect(identifyArrivalLocation('venue-1', 'loc-a12')).resolves.toEqual(location);
  });
  it('opens through the responsible waiter identity', async () => {
    const group = { customer_group_id: 'group-1' };
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValue(new Response(JSON.stringify({ customer_group: group }), { status: 200 }));
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });
    await expect(
      openArrivalCustomerGroup({
        venueId: 'venue-1',
        locationId: 'a12',
        waiterId: 'staff-waiter-1',
        physicalConfirmed: true,
        responsibilityAccepted: true,
        chargeConfirmed: true,
      }),
    ).resolves.toEqual(group);
    expect(fetchMock).toHaveBeenCalledWith(
      '/guest-arrival/customer-groups/open',
      expect.objectContaining({
        headers: expect.objectContaining({ 'X-BeachOS-Development-Actor': 'staff-waiter-1' }),
      }),
    );
  });
  it('preserves backend uncertainty', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn<typeof fetch>()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ error: { message: 'The opening outcome is uncertain.' } }),
            { status: 409 },
          ),
        ),
    );
    await expect(getGuestArrivalContext('venue-1')).rejects.toThrow(
      'The opening outcome is uncertain.',
    );
  });
});
