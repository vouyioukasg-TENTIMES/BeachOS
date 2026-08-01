import { afterEach, describe, expect, it, vi } from 'vitest';
import { acknowledgeBarTicket, BarApiError, getBarContext, progressBarTicket } from './barApi';
afterEach(() => vi.unstubAllGlobals());
describe('Bar API', () => {
  it('sends whole-Ticket fulfilment commands', async () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'progress-1' });
    const fetch = vi
      .fn()
      .mockResolvedValue(new Response(JSON.stringify({ request_id: 'progress-1' })));
    vi.stubGlobal('fetch', fetch);
    await progressBarTicket('b/1', 'DELIVER');
    expect(fetch).toHaveBeenCalledWith(
      '/bar/tickets/b%2F1/deliver',
      expect.objectContaining({ method: 'POST' }),
    );
  });
  it('loads confirmed Bar context', async () => {
    const body = { venue_id: 'venue-1', awaiting_acknowledgement_count: 0, tickets: [] };
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify(body))));
    await expect(getBarContext('venue-1')).resolves.toEqual(body);
  });
  it('sends an idempotent acknowledgement', async () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });
    const fetch = vi
      .fn()
      .mockResolvedValue(new Response(JSON.stringify({ request_id: 'request-1' })));
    vi.stubGlobal('fetch', fetch);
    await acknowledgeBarTicket('bar/1');
    expect(fetch).toHaveBeenCalledWith(
      '/bar/tickets/bar%2F1/acknowledge',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ request_id: 'request-1' }),
      }),
    );
  });
  it('preserves server rejection', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ error: { message: 'Already acknowledged' } }), {
          status: 409,
        }),
      ),
    );
    await expect(getBarContext('venue-1')).rejects.toMatchObject({
      status: 409,
      message: 'Already acknowledged',
    });
  });
  it('reports connection uncertainty', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));
    await expect(getBarContext('venue-1')).rejects.toBeInstanceOf(BarApiError);
  });
});
