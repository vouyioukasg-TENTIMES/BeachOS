export interface ClosingReport {
  venue_id: string;
  business_date: string;
  closed_at: string;
  closed_by_id: string;
  active_customer_groups: number;
  occupied_service_locations: number;
  open_bills: number;
  unresolved_operational_work: number;
}

export interface ClosingContext {
  venue_id: string;
  business_date: string;
  status: 'CLOSED' | 'OPEN' | 'CLOSED_FOR_BUSINESS_DATE';
  readiness: {
    active_customer_groups: number;
    occupied_service_locations: number;
    open_bills: number;
    unresolved_operational_work: number;
  };
  blockers: string[];
  can_close: boolean;
  closing_report: ClosingReport | null;
}

export interface CloseVenueResult {
  request_id: string;
  status: 'CLOSED_FOR_BUSINESS_DATE';
  closing_report: ClosingReport;
}

export async function getClosingContext(venueId: string): Promise<ClosingContext> {
  const response = await fetch(
    `/api/venue/closing-context?venue_id=${encodeURIComponent(venueId)}`,
  );
  if (!response.ok) throw new Error('Venue Closing context could not be loaded.');
  return (await response.json()) as ClosingContext;
}

export async function closeVenue(venueId: string, requestId: string): Promise<CloseVenueResult> {
  const response = await fetch('/api/venue/close', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ request_id: requestId, venue_id: venueId }),
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as {
      error?: { message?: string };
    } | null;
    throw new Error(body?.error?.message ?? 'The Venue was not closed.');
  }
  return (await response.json()) as CloseVenueResult;
}
