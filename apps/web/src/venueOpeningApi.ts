export interface DepartmentReadiness {
  department_id: string;
  responsible_person_id: string;
  declared_by_id: string;
  status: string;
  declared_at: string;
  reason: string | null;
  comment: string | null;
}

export interface OpeningReport {
  venue_id: string;
  business_date: string;
  opened_at: string;
  host_id: string;
  department_readiness: DepartmentReadiness[];
  declaration_history: DepartmentReadiness[];
  delays: DepartmentReadiness[];
  blocking_issues: DepartmentReadiness[];
}

export interface OpenVenueResult {
  request_id: string;
  report: OpeningReport;
}

export interface DepartmentContext {
  department_id: string;
  name: string;
  responsible_person_id: string;
  current_readiness: DepartmentReadiness | null;
}

export interface AttentionItem {
  code: string;
  importance: string;
  message: string;
  department_id: string | null;
}

export interface VenueContext {
  venue_id: string;
  venue_name: string;
  business_date: string;
  opening_status: 'CLOSED' | 'OPEN';
  opening_report: OpeningReport | null;
  department_readiness: DepartmentContext[];
  outstanding_departments: string[];
  attention_queue: AttentionItem[];
}

interface ApiErrorBody {
  error?: {
    message?: string;
  };
}

export class VenueOpeningApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'VenueOpeningApiError';
    this.status = status;
  }
}

async function errorMessage(response: Response, fallback: string): Promise<string> {
  try {
    const body = (await response.json()) as ApiErrorBody;
    if (body.error?.message) {
      return body.error.message;
    }
  } catch {
    // The fallback below is intentionally safe and contains no server internals.
  }
  return fallback;
}

export async function openVenue(venueId: string, signal?: AbortSignal): Promise<OpenVenueResult> {
  const response = await fetch('/venue/open', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      request_id: crypto.randomUUID(),
      venue_id: venueId,
    }),
    signal,
  });

  if (!response.ok) {
    throw new VenueOpeningApiError(
      await errorMessage(response, 'BeachOS could not open the Venue. Please try again.'),
      response.status,
    );
  }

  return (await response.json()) as OpenVenueResult;
}

export async function getVenueContext(
  venueId: string,
  signal?: AbortSignal,
): Promise<VenueContext> {
  const query = new URLSearchParams({ venue_id: venueId });
  const response = await fetch(`/venue/context?${query.toString()}`, {
    headers: { Accept: 'application/json' },
    signal,
  });

  if (!response.ok) {
    throw new VenueOpeningApiError(
      await errorMessage(
        response,
        'BeachOS could not load the current Venue context. Please try again.',
      ),
      response.status,
    );
  }

  return (await response.json()) as VenueContext;
}
