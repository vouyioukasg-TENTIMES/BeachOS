import { renderToStaticMarkup } from 'react-dom/server';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { HostWorkspaceView, type HostWorkspaceState } from './HostWorkspace';
import {
  getVenueContext,
  openVenue,
  type OpeningReport,
  type VenueContext,
} from './venueOpeningApi';

const readiness = {
  department_id: 'kitchen',
  responsible_person_id: 'staff-kitchen',
  declared_by_id: 'staff-kitchen',
  status: 'READY',
  declared_at: '2026-07-26T07:55:00Z',
  reason: null,
  comment: null,
};

const report: OpeningReport = {
  venue_id: 'venue-1',
  business_date: '2026-07-26',
  opened_at: '2026-07-26T08:00:00Z',
  host_id: 'development-host',
  department_readiness: [readiness],
  declaration_history: [readiness],
  delays: [],
  blocking_issues: [],
};

const readyContext: VenueContext = {
  venue_id: 'venue-1',
  venue_name: 'Emerald Beach Club',
  business_date: '2026-07-26',
  opening_status: 'CLOSED',
  opening_report: null,
  department_readiness: [
    {
      department_id: 'kitchen',
      name: 'Kitchen',
      responsible_person_id: 'staff-kitchen',
      current_readiness: readiness,
    },
  ],
  outstanding_departments: [],
  attention_queue: [
    {
      code: 'READY_TO_OPEN',
      importance: 'ACTION_REQUIRED',
      message: 'Every mandatory department is READY. The Venue can be opened.',
      department_id: null,
    },
  ],
};

function renderState(state: HostWorkspaceState): string {
  return renderToStaticMarkup(
    <HostWorkspaceView
      state={state}
      onRetry={() => undefined}
      onRequestOpen={() => undefined}
      onConfirmOpen={() => undefined}
      onCancelOpen={() => undefined}
    />,
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('Host Workspace', () => {
  it('shows an explicit loading state while context is retrieved', () => {
    const markup = renderState({ status: 'loading' });

    expect(markup).toContain('Loading Host Workspace');
    expect(markup).toContain('confirming the current Venue and Business Date');
    expect(markup).toContain('role="status"');
  });

  it('shows authoritative Venue state, readiness, and attention', () => {
    const context: VenueContext = {
      ...readyContext,
      department_readiness: [
        ...readyContext.department_readiness,
        {
          department_id: 'bar',
          name: 'Bar',
          responsible_person_id: 'staff-bar',
          current_readiness: null,
        },
      ],
      outstanding_departments: ['bar'],
      attention_queue: [
        {
          code: 'MISSING_DECLARATION',
          importance: 'ACTION_REQUIRED',
          message: 'Bar has not declared readiness.',
          department_id: 'bar',
        },
      ],
    };

    const markup = renderState({
      status: 'ready',
      context,
      opening: { status: 'idle' },
    });

    expect(markup).toContain('Emerald Beach Club');
    expect(markup).toContain('Venue closed');
    expect(markup).toContain('Operational Readiness');
    expect(markup).toContain('NOT READY');
    expect(markup).toContain('Blocking items');
    expect(markup).toContain('Estimated readiness');
    expect(markup).toContain('Not available');
    expect(markup).toContain('Kitchen');
    expect(markup).toContain('Bar');
    expect(markup).toContain('PENDING');
    expect(markup).toContain('Bar has not declared readiness');
    expect(markup).toContain('disabled');
  });

  it('offers opening only when every mandatory department is ready', () => {
    const markup = renderState({
      status: 'ready',
      context: readyContext,
      opening: { status: 'confirming' },
    });

    expect(markup).toContain('READY');
    expect(markup).toContain('You can safely open the Venue');
    expect(markup).toContain('Opening is available');
    expect(markup).toContain('Open Venue');
    expect(markup).toContain('Open Emerald Beach Club?');
    expect(markup).toContain('Confirm Open Venue');
  });

  it('shows success and the current Opening Report after opening', () => {
    const markup = renderState({
      status: 'ready',
      context: {
        ...readyContext,
        opening_status: 'OPEN',
        opening_report: report,
        attention_queue: [],
      },
      opening: { status: 'success' },
    });

    expect(markup).toContain('Venue opened successfully');
    expect(markup).toContain('Opening Report');
    expect(markup).toContain('development-host');
    expect(markup).toContain('No confirmed action required');
    expect(markup).toContain('does not mean the operation is perfect');
  });

  it('shows context and opening errors without inventing success', () => {
    const contextFailure = renderState({
      status: 'error',
      message: 'The current Business Date cannot be confirmed.',
    });
    const openingFailure = renderState({
      status: 'ready',
      context: readyContext,
      opening: {
        status: 'error',
        message: 'every mandatory department must be READY before opening',
      },
    });

    expect(contextFailure).toContain('Host Workspace could not load');
    expect(contextFailure).toContain('The current Business Date cannot be confirmed');
    expect(openingFailure).toContain('Venue was not opened');
    expect(openingFailure).not.toContain('Venue opened successfully');
  });

  it('disables the action while opening is processed', () => {
    const markup = renderState({
      status: 'ready',
      context: readyContext,
      opening: { status: 'processing' },
    });

    expect(markup).toContain('Opening…');
    expect(markup).toContain('disabled');
  });
});

describe('Host Workspace API', () => {
  it('retrieves context from the real endpoint contract', async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify(readyContext), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);

    await expect(getVenueContext('venue-1')).resolves.toEqual(readyContext);
    expect(fetchMock).toHaveBeenCalledWith('/venue/context?venue_id=venue-1', {
      headers: { Accept: 'application/json' },
      signal: undefined,
    });
  });

  it('submits opening to the existing real endpoint contract', async () => {
    const response = { request_id: 'request-1', report };
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify(response), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });

    await expect(openVenue('venue-1')).resolves.toEqual(response);
    expect(fetchMock).toHaveBeenCalledWith('/venue/open', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ request_id: 'request-1', venue_id: 'venue-1' }),
      signal: undefined,
    });
  });

  it('uses a safe fallback for an unexpected context response', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn<typeof fetch>().mockResolvedValue(new Response('unavailable', { status: 500 })),
    );

    await expect(getVenueContext('venue-1')).rejects.toThrow(
      'BeachOS could not load the current Venue context. Please try again.',
    );
  });
});
