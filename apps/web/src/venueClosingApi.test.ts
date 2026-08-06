import { afterEach, describe, expect, it, vi } from 'vitest';
import { closeVenue, getClosingContext } from './venueClosingApi';

afterEach(() => vi.unstubAllGlobals());

describe('Venue Closing API', () => {
  it('loads every approved readiness fact', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            venue_id: 'venue-1',
            business_date: '2026-08-01',
            status: 'OPEN',
            readiness: {
              active_customer_groups: 0,
              occupied_service_locations: 0,
              open_bills: 0,
              unresolved_operational_work: 0,
            },
            blockers: [],
            can_close: true,
            closing_report: null,
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getClosingContext('venue-1')).can_close).toBe(true);
  });

  it('returns the permanent Closing Report', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            request_id: 'request-1',
            status: 'CLOSED_FOR_BUSINESS_DATE',
            closing_report: {
              venue_id: 'venue-1',
              business_date: '2026-08-01',
              closed_at: '2026-08-01T23:30:00Z',
              closed_by_id: 'manager-1',
              active_customer_groups: 0,
              occupied_service_locations: 0,
              open_bills: 0,
              unresolved_operational_work: 0,
            },
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await closeVenue('venue-1', 'request-1')).closing_report.closed_by_id).toBe(
      'manager-1',
    );
  });

  it('preserves closing blockers returned by the backend', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ error: { message: '1 ACTIVE Customer Group(s) remain' } }),
            { status: 409 },
          ),
        ),
    );
    await expect(closeVenue('venue-1', 'request-1')).rejects.toThrow('ACTIVE Customer Group');
  });
});
