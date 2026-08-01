import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  declareDepartmentReadiness,
  getDepartmentOwnerContext,
  readinessRequiresReason,
  type DepartmentOwnerContext,
} from './departmentReadinessApi';

afterEach(() => vi.unstubAllGlobals());

const context: DepartmentOwnerContext = {
  venue_id: 'venue-1',
  venue_name: 'Emerald Beach Club',
  business_date: '2026-07-26',
  opening_status: 'CLOSED',
  departments: [
    {
      department_id: 'kitchen',
      name: 'Kitchen',
      responsible_person_id: 'staff-kitchen',
      current_readiness: null,
    },
  ],
  declaration_history: [],
};

describe('Department Readiness API', () => {
  it('requires a reason only for the approved non-ready declarations', () => {
    expect(readinessRequiresReason('READY')).toBe(false);
    expect(readinessRequiresReason('NOT READY')).toBe(true);
    expect(readinessRequiresReason('BLOCKED')).toBe(true);
  });
  it('retrieves only the current owner context using temporary identity', async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify(context), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);

    await expect(getDepartmentOwnerContext('venue-1', 'staff-kitchen')).resolves.toEqual(context);
    expect(fetchMock).toHaveBeenCalledWith(
      '/venue/department-readiness/context?venue_id=venue-1',
      expect.objectContaining({
        headers: expect.objectContaining({ 'X-BeachOS-Development-Actor': 'staff-kitchen' }),
      }),
    );
  });

  it('submits an attributable declaration to the real endpoint contract', async () => {
    const declaration = {
      department_id: 'kitchen',
      responsible_person_id: 'staff-kitchen',
      declared_by_id: 'staff-kitchen',
      status: 'BLOCKED',
      declared_at: '2026-07-26T08:00:00Z',
      reason: 'Equipment issue',
      comment: null,
    };
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ declaration }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    );
    vi.stubGlobal('fetch', fetchMock);
    vi.stubGlobal('crypto', { randomUUID: () => 'request-1' });

    await expect(
      declareDepartmentReadiness({
        venueId: 'venue-1',
        departmentId: 'kitchen',
        actorId: 'staff-kitchen',
        status: 'BLOCKED',
        reason: 'Equipment issue',
        comment: null,
      }),
    ).resolves.toEqual(declaration);
    expect(fetchMock).toHaveBeenCalledWith(
      '/venue/departments/kitchen/readiness',
      expect.objectContaining({ method: 'POST' }),
    );
  });

  it('surfaces backend validation and safe unexpected errors', async () => {
    vi.stubGlobal(
      'fetch',
      vi
        .fn<typeof fetch>()
        .mockResolvedValueOnce(
          new Response(JSON.stringify({ error: { message: 'A reason is required.' } }), {
            status: 409,
          }),
        )
        .mockResolvedValueOnce(new Response('unavailable', { status: 500 })),
    );

    await expect(
      declareDepartmentReadiness({
        venueId: 'venue-1',
        departmentId: 'kitchen',
        actorId: 'staff-kitchen',
        status: 'BLOCKED',
        reason: null,
        comment: null,
      }),
    ).rejects.toThrow('A reason is required.');
    await expect(getDepartmentOwnerContext('venue-1', 'staff-kitchen')).rejects.toThrow(
      'BeachOS could not confirm your department.',
    );
  });
});
