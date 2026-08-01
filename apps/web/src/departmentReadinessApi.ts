import {
  VenueOpeningApiError,
  type DepartmentContext,
  type DepartmentReadiness,
} from './venueOpeningApi';

export type ReadinessStatus = 'READY' | 'NOT READY' | 'BLOCKED';

export function readinessRequiresReason(status: ReadinessStatus): boolean {
  return status !== 'READY';
}

export interface DepartmentOwnerContext {
  venue_id: string;
  venue_name: string;
  business_date: string;
  opening_status: 'CLOSED' | 'OPEN';
  departments: DepartmentContext[];
  declaration_history: DepartmentReadiness[];
}

export interface DeclareReadinessInput {
  venueId: string;
  departmentId: string;
  actorId: string;
  status: ReadinessStatus;
  reason: string | null;
  comment: string | null;
}

interface ErrorBody {
  error?: { message?: string };
}

async function errorMessage(response: Response, fallback: string): Promise<string> {
  try {
    const body = (await response.json()) as ErrorBody;
    return body.error?.message ?? fallback;
  } catch {
    return fallback;
  }
}

export async function getDepartmentOwnerContext(
  venueId: string,
  actorId: string,
  signal?: AbortSignal,
): Promise<DepartmentOwnerContext> {
  const query = new URLSearchParams({ venue_id: venueId });
  const response = await fetch(`/venue/department-readiness/context?${query.toString()}`, {
    headers: {
      Accept: 'application/json',
      'X-BeachOS-Development-Actor': actorId,
    },
    signal,
  });
  if (!response.ok) {
    throw new VenueOpeningApiError(
      await errorMessage(response, 'BeachOS could not confirm your department.'),
      response.status,
    );
  }
  return (await response.json()) as DepartmentOwnerContext;
}

export async function declareDepartmentReadiness(
  input: DeclareReadinessInput,
  signal?: AbortSignal,
): Promise<DepartmentReadiness> {
  const response = await fetch(
    `/venue/departments/${encodeURIComponent(input.departmentId)}/readiness`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-BeachOS-Development-Actor': input.actorId,
      },
      body: JSON.stringify({
        request_id: crypto.randomUUID(),
        venue_id: input.venueId,
        status: input.status,
        reason: input.reason,
        comment: input.comment,
      }),
      signal,
    },
  );
  if (!response.ok) {
    throw new VenueOpeningApiError(
      await errorMessage(response, 'BeachOS could not save the readiness declaration.'),
      response.status,
    );
  }
  const result = (await response.json()) as { declaration: DepartmentReadiness };
  return result.declaration;
}
