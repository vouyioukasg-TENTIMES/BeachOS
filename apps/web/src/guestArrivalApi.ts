import { VenueOpeningApiError } from './venueOpeningApi';

export interface ArrivalLocation {
  service_location_id: string;
  visible_name: string;
  digital_identity: string;
  location_type: string;
  status: string;
  active_customer_group_id: string | null;
  opening_charge: string | null;
  currency: string | null;
  charge_description: string | null;
}
export interface GuestArrivalContext {
  venue_id: string;
  venue_name: string;
  business_date: string;
  venue_open: boolean;
  operational_confidence: string;
  locations: ArrivalLocation[];
}
export interface OpenedCustomerGroup {
  customer_group_id: string;
  venue_id: string;
  service_location_id: string;
  responsible_waiter_id: string;
  opened_at: string;
  bill_id: string | null;
  opening_obligation: string | null;
  currency: string | null;
}
interface ErrorBody {
  error?: { message?: string };
}
async function errorMessage(response: Response, fallback: string) {
  try {
    const body = (await response.json()) as ErrorBody;
    return body.error?.message ?? fallback;
  } catch {
    return fallback;
  }
}
export async function getGuestArrivalContext(
  venueId: string,
  signal?: AbortSignal,
): Promise<GuestArrivalContext> {
  const query = new URLSearchParams({ venue_id: venueId });
  const response = await fetch(`/guest-arrival/context?${query}`, {
    headers: { Accept: 'application/json' },
    signal,
  });
  if (!response.ok)
    throw new VenueOpeningApiError(
      await errorMessage(response, 'BeachOS could not confirm Guest Arrival.'),
      response.status,
    );
  return (await response.json()) as GuestArrivalContext;
}
export async function identifyArrivalLocation(
  venueId: string,
  digitalIdentity: string,
  signal?: AbortSignal,
): Promise<ArrivalLocation> {
  const query = new URLSearchParams({ venue_id: venueId, digital_identity: digitalIdentity });
  const response = await fetch(`/guest-arrival/service-locations/identify?${query}`, {
    headers: { Accept: 'application/json' },
    signal,
  });
  if (!response.ok)
    throw new VenueOpeningApiError(
      await errorMessage(response, 'The Service Location could not be confirmed.'),
      response.status,
    );
  return (await response.json()) as ArrivalLocation;
}
export async function openArrivalCustomerGroup(input: {
  venueId: string;
  locationId: string;
  waiterId: string;
  physicalConfirmed: boolean;
  responsibilityAccepted: boolean;
  chargeConfirmed: boolean;
}): Promise<OpenedCustomerGroup> {
  const response = await fetch('/guest-arrival/customer-groups/open', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-BeachOS-Development-Actor': input.waiterId },
    body: JSON.stringify({
      request_id: crypto.randomUUID(),
      venue_id: input.venueId,
      service_location_id: input.locationId,
      physical_context_confirmed: input.physicalConfirmed,
      waiter_accepts_responsibility: input.responsibilityAccepted,
      opening_charge_confirmed: input.chargeConfirmed,
    }),
  });
  if (!response.ok)
    throw new VenueOpeningApiError(
      await errorMessage(response, 'The Customer Group opening outcome could not be confirmed.'),
      response.status,
    );
  const body = (await response.json()) as { customer_group: OpenedCustomerGroup };
  return body.customer_group;
}
