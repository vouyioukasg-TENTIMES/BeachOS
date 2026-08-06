import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { App } from './App';
import { getOperationalOverview } from './operationalOverviewApi';

afterEach(() => vi.unstubAllGlobals());

describe('BeachOS operational shell', () => {
  it('provides accessible global context and role-aware primary navigation', () => {
    const markup = renderToStaticMarkup(<App />);

    expect(markup).toContain('Skip to workspace');
    expect(markup).toContain('aria-label="Main navigation"');
    expect(markup).toContain('aria-label="BeachOS Overview"');
    expect(markup).toContain('Business Date');
    expect(markup).toContain('Development only');
    expect(markup).toContain('Overview');
    expect(markup).toContain('Opening');
    expect(markup).toContain('Guest Arrival');
    expect(markup).toContain('Customer Groups');
    expect(markup).toContain('Closing');
    expect(markup).not.toContain('>Kitchen</button>');
  });

  it('labels the Demo Day launcher as a development control', () => {
    const markup = renderToStaticMarkup(<App />);

    expect(markup).toContain('Demo Day');
    expect(markup).toContain('Development only');
  });
});

describe('operational overview API', () => {
  it('combines existing real endpoint contracts', async () => {
    const responses = [
      {
        venue_id: 'venue-1',
        venue_name: 'Emerald Beach Club',
        business_date: '2026-08-02',
        opening_status: 'OPEN',
        opening_report: null,
        department_readiness: [],
        outstanding_departments: [],
        attention_queue: [],
      },
      {
        venue_id: 'venue-1',
        venue_name: 'Emerald Beach Club',
        business_date: '2026-08-02',
        venue_open: true,
        operational_confidence: 'CONFIRMED',
        locations: [],
      },
      { venue_id: 'venue-1', awaiting_acknowledgement_count: 0, tickets: [] },
      { venue_id: 'venue-1', awaiting_acknowledgement_count: 0, tickets: [] },
      null,
      {
        customer_group_id: 'group-1',
        status: 'ACTIVE',
        bill_status: null,
        can_complete: true,
        next_action: 'COMPLETE',
        service_location_status: 'OCCUPIED',
      },
      {
        customer_group_id: 'group-1',
        customer_group_status: 'ACTIVE',
        departure_status: 'NOT_DEPARTED',
        service_location_id: 'location-1',
        service_location_name: 'A1',
        service_location_status: 'OCCUPIED',
        can_depart: false,
        next_action: 'COMPLETE_CUSTOMER_GROUP',
      },
      {
        venue_id: 'venue-1',
        business_date: '2026-08-02',
        status: 'OPEN',
        readiness: {
          active_customer_groups: 1,
          occupied_service_locations: 1,
          open_bills: 0,
          unresolved_operational_work: 0,
        },
        blockers: ['Active Customer Groups: 1'],
        can_close: false,
        closing_report: null,
      },
    ];
    const fetchMock = vi.fn<typeof fetch>();
    responses.forEach((body) => {
      fetchMock.mockResolvedValueOnce(
        new Response(JSON.stringify(body), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      );
    });
    vi.stubGlobal('fetch', fetchMock);

    const overview = await getOperationalOverview('venue-1', 'group-1');

    expect(overview.venue.opening_status).toBe('OPEN');
    expect(overview.closing?.readiness.active_customer_groups).toBe(1);
    expect(overview.unavailable).toEqual([]);
    expect(fetchMock).toHaveBeenCalledTimes(8);
  });

  it('requires Venue context but keeps secondary failures explicitly uncertain', async () => {
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            venue_id: 'venue-1',
            venue_name: 'Emerald Beach Club',
            business_date: '2026-08-02',
            opening_status: 'OPEN',
            opening_report: null,
            department_readiness: [],
            outstanding_departments: [],
            attention_queue: [],
          }),
          { status: 200, headers: { 'Content-Type': 'application/json' } },
        ),
      )
      .mockResolvedValue(new Response('unavailable', { status: 503 }));
    vi.stubGlobal('fetch', fetchMock);

    const overview = await getOperationalOverview('venue-1', 'group-1');

    expect(overview.unavailable).toHaveLength(7);
    expect(overview.kitchenTickets).toBeNull();
    expect(overview.bill).toBeUndefined();
  });
});
