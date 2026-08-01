import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  acknowledgeKitchenTicket,
  getKitchenContext,
  KitchenApiError,
  progressKitchenTicket,
} from './kitchenApi';

afterEach(() => vi.unstubAllGlobals());

describe('Kitchen API', () => {
  it('sends whole-Ticket fulfilment commands', async () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'progress-1' });
    const fetch = vi
      .fn()
      .mockResolvedValue(new Response(JSON.stringify({ request_id: 'progress-1' })));
    vi.stubGlobal('fetch', fetch);
    await progressKitchenTicket('k/1', 'MARK_READY');
    expect(fetch).toHaveBeenCalledWith(
      '/kitchen/tickets/k%2F1/mark_ready',
      expect.objectContaining({ method: 'POST' }),
    );
  });
  it('loads confirmed Kitchen work', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            venue_id: 'venue-1',
            awaiting_acknowledgement_count: 0,
            tickets: [],
          }),
          { status: 200 },
        ),
      ),
    );
    expect((await getKitchenContext('venue-1')).tickets).toEqual([]);
  });

  it('acknowledges through the real API contract', async () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ request_id: 'request-1', ticket: {} }), {
          status: 200,
        }),
      ),
    );
    expect((await acknowledgeKitchenTicket('ticket-1')).request_id).toBe('request-1');
  });

  it('preserves an operational backend rejection', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ error: { message: 'Already acknowledged' } }), {
          status: 409,
        }),
      ),
    );
    await expect(getKitchenContext('venue-1')).rejects.toMatchObject({
      message: 'Already acknowledged',
      status: 409,
    });
  });

  it('marks an unknown network outcome as uncertain', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));
    await expect(acknowledgeKitchenTicket('ticket-1')).rejects.toBeInstanceOf(KitchenApiError);
    await expect(acknowledgeKitchenTicket('ticket-1')).rejects.toMatchObject({
      status: 0,
    });
  });
});
