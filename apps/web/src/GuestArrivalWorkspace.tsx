import { useEffect, useMemo, useState } from 'react';
import {
  getGuestArrivalContext,
  identifyArrivalLocation,
  openArrivalCustomerGroup,
  type ArrivalLocation,
  type GuestArrivalContext,
} from './guestArrivalApi';
import { VenueOpeningApiError } from './venueOpeningApi';

export function GuestArrivalWorkspace({ venueId }: { venueId: string }) {
  const [context, setContext] = useState<GuestArrivalContext | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [identity, setIdentity] = useState('');
  const [selected, setSelected] = useState<ArrivalLocation | null>(null);
  const [waiter, setWaiter] = useState('');
  const [physical, setPhysical] = useState(false);
  const [accepted, setAccepted] = useState(false);
  const [charge, setCharge] = useState(false);
  const [opening, setOpening] = useState(false);
  const [outcome, setOutcome] = useState<string | null>(null);
  const available = useMemo(
    () =>
      context?.locations.filter(
        (item) =>
          item.status === 'AVAILABLE' &&
          item.visible_name.toLowerCase().includes(query.toLowerCase()),
      ) ?? [],
    [context, query],
  );
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    void getGuestArrivalContext(venueId, controller.signal)
      .then(setContext)
      .catch((value: unknown) => {
        if (!controller.signal.aborted)
          setError(
            value instanceof VenueOpeningApiError
              ? value.message
              : 'Current Guest Arrival facts are unavailable.',
          );
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [venueId]);
  async function identify() {
    setError(null);
    try {
      setSelected(await identifyArrivalLocation(venueId, identity));
    } catch (value) {
      setError(
        value instanceof VenueOpeningApiError
          ? value.message
          : 'The Service Location identity is uncertain.',
      );
    }
  }
  async function open() {
    if (!selected) return;
    setOpening(true);
    setError(null);
    setOutcome(null);
    try {
      const group = await openArrivalCustomerGroup({
        venueId,
        locationId: selected.service_location_id,
        waiterId: waiter,
        physicalConfirmed: physical,
        responsibilityAccepted: accepted,
        chargeConfirmed: charge,
      });
      setOutcome(`Customer Group ${group.customer_group_id} opened successfully.`);
      setContext(await getGuestArrivalContext(venueId));
      setSelected(null);
    } catch (value) {
      setError(
        value instanceof VenueOpeningApiError
          ? value.message
          : 'The opening outcome is uncertain. Confirm current facts before trying again.',
      );
    } finally {
      setOpening(false);
    }
  }
  if (loading)
    return (
      <main className="page-shell centered-state">
        <section className="state-card" role="status">
          <span className="spinner" />
          <h1>Confirming Guest Arrival</h1>
          <p>BeachOS is retrieving the Venue and Service Location facts.</p>
        </section>
      </main>
    );
  if (!context)
    return (
      <main className="page-shell centered-state">
        <section className="state-card" role="alert">
          <h1>Guest Arrival unavailable</h1>
          <p>{error}</p>
        </section>
      </main>
    );
  return (
    <main className="page-shell">
      <header className="product-header">
        <span className="wordmark">BeachOS</span>
        <span>Guest Arrival</span>
      </header>
      <div className="page-content arrival-page">
        <p className="eyebrow">{context.venue_name}</p>
        <h1>Welcome the next party</h1>
        <p className="lede">
          BeachOS confirms operational facts. The Host decides how to welcome, assess, offer, and
          escort.
        </p>
        {!context.venue_open && (
          <section className="message error-message" role="alert">
            <strong>The Venue is not open.</strong> Welcome the guests, but do not begin normal
            seating or Customer Group opening.
          </section>
        )}
        {error && (
          <p className="message error-message" role="alert">
            {error}
          </p>
        )}
        {outcome && (
          <p className="message success-message" role="status">
            {outcome}
          </p>
        )}
        <section className="workspace-panel">
          <h2>Identify the Service Location</h2>
          <p>
            NFC or a secure link supplies only the stable Digital Identity. Manual lookup remains
            available.
          </p>
          <div className="arrival-identify">
            <input
              aria-label="Digital Identity"
              value={identity}
              onChange={(e) => setIdentity(e.target.value)}
              placeholder="Digital Identity"
            />
            <button
              className="secondary-action"
              disabled={!identity.trim()}
              onClick={() => void identify()}
            >
              Identify
            </button>
          </div>
          <label>
            Manual lookup
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Visible name or number"
            />
          </label>
          <div className="arrival-locations">
            {available.length === 0 ? (
              <p>No available Service Location matches the current lookup.</p>
            ) : (
              available.map((item) => (
                <button
                  type="button"
                  key={item.service_location_id}
                  className={
                    selected?.service_location_id === item.service_location_id
                      ? 'selected-location'
                      : ''
                  }
                  onClick={() => setSelected(item)}
                >
                  <strong>{item.visible_name}</strong>
                  <span>
                    {item.location_type} · {item.status}
                  </span>
                </button>
              ))
            )}
          </div>
        </section>
        {selected && (
          <section className="workspace-panel">
            <p className="eyebrow">Confirmed central context</p>
            <h2>{selected.visible_name}</h2>
            <p>
              {selected.location_type} · {selected.status}
            </p>
            {selected.opening_charge && (
              <p>
                <strong>{selected.charge_description}:</strong> {selected.opening_charge}{' '}
                {selected.currency}
              </p>
            )}
            <p>
              The Host must confirm physical suitability. Identification alone performs no action.
            </p>
          </section>
        )}
        {selected && (
          <section className="workspace-panel arrival-handoff">
            <h2>Responsible Waiter handoff</h2>
            <label>
              Responsible Waiter identifier
              <input
                value={waiter}
                onChange={(e) => setWaiter(e.target.value)}
                placeholder="staff-waiter-…"
              />
            </label>
            <label>
              <input
                type="checkbox"
                checked={physical}
                onChange={(e) => setPhysical(e.target.checked)}
              />{' '}
              Physical and digital Service Location agree
            </label>
            <label>
              <input
                type="checkbox"
                checked={accepted}
                onChange={(e) => setAccepted(e.target.checked)}
              />{' '}
              I am the Responsible Waiter and accept responsibility
            </label>
            {selected.location_type === 'BEACH SUNBED' && (
              <label>
                <input
                  type="checkbox"
                  checked={charge}
                  onChange={(e) => setCharge(e.target.checked)}
                />{' '}
                I reviewed and confirm the Beach Sunbed charge
              </label>
            )}
            <button
              className="primary-action"
              disabled={
                opening ||
                !context.venue_open ||
                selected.status !== 'AVAILABLE' ||
                !waiter.trim() ||
                !physical ||
                !accepted ||
                (selected.location_type === 'BEACH SUNBED' && !charge)
              }
              onClick={() => void open()}
            >
              {opening ? 'Opening…' : 'Open Customer Group'}
            </button>
            <p>Only the Responsible Waiter may perform this intentional action.</p>
          </section>
        )}
      </div>
    </main>
  );
}
