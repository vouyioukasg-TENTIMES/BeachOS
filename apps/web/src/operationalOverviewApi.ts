import { getBarContext, type BarTicket } from './barApi';
import { getRunningBill, type RunningBill } from './billingApi';
import { getCompletionContext, type CompletionContext } from './completionApi';
import { getDepartureContext, type DepartureContext } from './departureApi';
import { getGuestArrivalContext, type GuestArrivalContext } from './guestArrivalApi';
import { getKitchenContext, type KitchenTicket } from './kitchenApi';
import { getClosingContext, type ClosingContext } from './venueClosingApi';
import { getVenueContext, type VenueContext } from './venueOpeningApi';

export interface OperationalOverview {
  venue: VenueContext;
  arrival: GuestArrivalContext | null;
  kitchenTickets: KitchenTicket[] | null;
  barTickets: BarTicket[] | null;
  bill: RunningBill | null | undefined;
  completion: CompletionContext | null;
  departure: DepartureContext | null;
  closing: ClosingContext | null;
  unavailable: string[];
}

async function optional<T>(name: string, operation: Promise<T>, unavailable: string[]) {
  try {
    return await operation;
  } catch {
    unavailable.push(name);
    return null;
  }
}

export async function getOperationalOverview(
  venueId: string,
  customerGroupId: string,
): Promise<OperationalOverview> {
  const venue = await getVenueContext(venueId);
  const unavailable: string[] = [];
  const [arrival, kitchen, bar, bill, completion, departure, closing] = await Promise.all([
    optional('Service Locations', getGuestArrivalContext(venueId), unavailable),
    optional('Kitchen', getKitchenContext(venueId), unavailable),
    optional('Bar', getBarContext(venueId), unavailable),
    optional('Billing', getRunningBill(customerGroupId), unavailable),
    optional('Customer Group completion', getCompletionContext(customerGroupId), unavailable),
    optional('Guest departure', getDepartureContext(customerGroupId), unavailable),
    optional('Venue closing', getClosingContext(venueId), unavailable),
  ]);

  return {
    venue,
    arrival,
    kitchenTickets: kitchen?.tickets ?? null,
    barTickets: bar?.tickets ?? null,
    bill: unavailable.includes('Billing') ? undefined : bill,
    completion,
    departure,
    closing,
    unavailable,
  };
}
