import { useCallback, useEffect, useMemo, useState } from 'react';
import { getOperationalOverview, type OperationalOverview } from './operationalOverviewApi';

export type Workspace =
  | 'overview'
  | 'opening'
  | 'readiness'
  | 'arrival'
  | 'groups'
  | 'orders'
  | 'kitchen'
  | 'bar'
  | 'fulfilment'
  | 'billing'
  | 'closing';

interface Props {
  venueId: string;
  customerGroupId: string;
  role: string;
  onNavigate: (workspace: Workspace) => void;
}

interface CardProps {
  label: string;
  value: string | number;
  detail: string;
  status?: 'good' | 'attention' | 'neutral';
  onOpen: () => void;
}

function MetricCard({ label, value, detail, status = 'neutral', onOpen }: CardProps) {
  return (
    <button className={`overview-card ${status}`} onClick={onOpen}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
      <b>
        Open workspace <span aria-hidden="true">→</span>
      </b>
    </button>
  );
}

const roleAction: Record<string, { title: string; detail: string; workspace: Workspace }> = {
  Host: {
    title: 'Confirm operational readiness',
    detail: 'Review department declarations, open the Venue, and coordinate arrivals.',
    workspace: 'opening',
  },
  'Responsible Waiter': {
    title: 'Continue service for your group',
    detail: 'Open a Customer Group, submit Orders, and deliver confirmed Tickets.',
    workspace: 'arrival',
  },
  Kitchen: {
    title: 'Review Kitchen work',
    detail: 'Acknowledge confirmed Tickets and mark completed preparation READY.',
    workspace: 'kitchen',
  },
  Bar: {
    title: 'Review Bar work',
    detail: 'Acknowledge confirmed Tickets and mark completed preparation READY.',
    workspace: 'bar',
  },
  Cashier: {
    title: 'Review the current Bill',
    detail: 'Record the approved full Cash Payment and close a fully paid Bill.',
    workspace: 'billing',
  },
  Manager: {
    title: 'Review the whole operation',
    detail: 'Resolve outstanding work and confirm whether the Venue can safely close.',
    workspace: 'closing',
  },
};

export function OverviewDashboard({ venueId, customerGroupId, role, onNavigate }: Props) {
  const [overview, setOverview] = useState<OperationalOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setOverview(await getOperationalOverview(venueId, customerGroupId));
    } catch (reason) {
      setOverview(null);
      setError(
        reason instanceof Error ? reason.message : 'The operational overview is unavailable.',
      );
    } finally {
      setLoading(false);
    }
  }, [customerGroupId, venueId]);

  useEffect(() => void load(), [load]);

  const facts = useMemo(() => {
    if (!overview) return null;
    const kitchenOpen = overview.kitchenTickets?.filter((ticket) => ticket.status !== 'DELIVERED');
    const barOpen = overview.barTickets?.filter((ticket) => ticket.status !== 'DELIVERED');
    const ready = [...(overview.kitchenTickets ?? []), ...(overview.barTickets ?? [])].filter(
      (ticket) => ticket.status === 'READY',
    ).length;
    return { kitchenOpen, barOpen, ready };
  }, [overview]);

  if (loading)
    return (
      <section className="shell-state" role="status">
        <span className="spinner" aria-hidden="true" />
        <h1>Building the operational picture</h1>
        <p>BeachOS is confirming the current Venue, work, service, and financial facts.</p>
      </section>
    );

  if (!overview || !facts)
    return (
      <section className="shell-state" role="alert">
        <h1>The overview could not be confirmed</h1>
        <p>{error}</p>
        <button className="primary-action" onClick={() => void load()}>
          Retry
        </button>
      </section>
    );

  const locationAvailable = overview.arrival?.locations.filter(
    (item) => item.status === 'AVAILABLE',
  ).length;
  const locationOccupied = overview.arrival?.locations.filter(
    (item) => item.status === 'OCCUPIED',
  ).length;
  const action = roleAction[role] ?? {
    title: 'Review the whole operation',
    detail: 'Resolve outstanding work and confirm whether the Venue can safely close.',
    workspace: 'closing' as const,
  };
  const closingBlockers = overview.closing?.blockers.length;

  return (
    <main className="overview-dashboard">
      <header className="overview-heading">
        <div>
          <p className="eyebrow">Live operational overview</p>
          <h1>What needs attention now?</h1>
          <p>
            Confirmed facts from the existing BeachOS workspaces. Unknown information remains
            visible.
          </p>
        </div>
        <button className="secondary-action" onClick={() => void load()}>
          Refresh overview
        </button>
      </header>

      <section className="next-action-card" aria-labelledby="next-action-title">
        <div>
          <p className="eyebrow">Next for {role}</p>
          <h2 id="next-action-title">{action.title}</h2>
          <p>{action.detail}</p>
        </div>
        <button className="primary-action" onClick={() => onNavigate(action.workspace)}>
          Continue <span aria-hidden="true">→</span>
        </button>
      </section>

      <section className="role-entry-grid" aria-labelledby="role-workspaces-title">
        <div className="section-heading">
          <p className="eyebrow">Role workspaces</p>
          <h2 id="role-workspaces-title">Enter the operation by responsibility</h2>
        </div>
        {Object.entries(roleAction).map(([name, entry]) => (
          <button key={name} onClick={() => onNavigate(entry.workspace)}>
            <strong>{name}</strong>
            <span>{entry.title}</span>
          </button>
        ))}
        <button onClick={() => onNavigate('readiness')}>
          <strong>Department Owner</strong>
          <span>Declare opening readiness</span>
        </button>
      </section>

      {overview.unavailable.length > 0 && (
        <p className="uncertainty-banner" role="status">
          <strong>Some facts are not confirmed:</strong> {overview.unavailable.join(', ')}. Their
          cards show “Unknown”; refresh before acting on them.
        </p>
      )}

      <section className="overview-grid" aria-label="Operational facts">
        <MetricCard
          label="Venue status"
          value={overview.venue.opening_status.replaceAll('_', ' ')}
          detail={`${overview.venue.outstanding_departments.length} department declaration(s) outstanding`}
          status={overview.venue.opening_status === 'OPEN' ? 'good' : 'attention'}
          onOpen={() => onNavigate('opening')}
        />
        <MetricCard
          label="Active Customer Groups"
          value={overview.closing?.readiness.active_customer_groups ?? 'Unknown'}
          detail="Confirmed Venue Closing fact"
          status={
            (overview.closing?.readiness.active_customer_groups ?? 0) > 0 ? 'attention' : 'good'
          }
          onOpen={() => onNavigate('groups')}
        />
        <MetricCard
          label="Service Locations"
          value={locationAvailable === undefined ? 'Unknown' : `${locationAvailable} available`}
          detail={
            locationOccupied === undefined
              ? 'Occupancy unavailable'
              : `${locationOccupied} occupied`
          }
          onOpen={() => onNavigate('arrival')}
        />
        <MetricCard
          label="Open Kitchen Tickets"
          value={facts.kitchenOpen?.length ?? 'Unknown'}
          detail="Not yet delivered"
          status={(facts.kitchenOpen?.length ?? 0) > 0 ? 'attention' : 'good'}
          onOpen={() => onNavigate('kitchen')}
        />
        <MetricCard
          label="Open Bar Tickets"
          value={facts.barOpen?.length ?? 'Unknown'}
          detail="Not yet delivered"
          status={(facts.barOpen?.length ?? 0) > 0 ? 'attention' : 'good'}
          onOpen={() => onNavigate('bar')}
        />
        <MetricCard
          label="Ready for collection"
          value={overview.kitchenTickets && overview.barTickets ? facts.ready : 'Unknown'}
          detail="Whole Tickets awaiting collection"
          status={facts.ready > 0 ? 'attention' : 'good'}
          onOpen={() => onNavigate('fulfilment')}
        />
        <MetricCard
          label="Current Bills"
          value={overview.closing?.readiness.open_bills ?? 'Unknown'}
          detail={
            overview.bill
              ? `${overview.bill.balance.toFixed(2)} ${overview.bill.currency} current balance`
              : overview.bill === null
                ? 'No Bill for configured group'
                : 'Current group unavailable'
          }
          onOpen={() => onNavigate('billing')}
        />
        <MetricCard
          label="Fully paid awaiting closing"
          value={
            overview.bill === undefined ? 'Unknown' : overview.bill?.status === 'FULLY_PAID' ? 1 : 0
          }
          detail="Configured Customer Group"
          status={overview.bill?.status === 'FULLY_PAID' ? 'attention' : 'neutral'}
          onOpen={() => onNavigate('billing')}
        />
        <MetricCard
          label="Completed awaiting departure"
          value={overview.departure ? (overview.departure.can_depart ? 1 : 0) : 'Unknown'}
          detail="Configured Customer Group"
          status={overview.departure?.can_depart ? 'attention' : 'neutral'}
          onOpen={() => onNavigate('groups')}
        />
        <MetricCard
          label="Venue closing blockers"
          value={closingBlockers ?? 'Unknown'}
          detail={
            closingBlockers === 0 ? 'All confirmed checks are clear' : 'Resolve before closing'
          }
          status={closingBlockers === 0 ? 'good' : 'attention'}
          onOpen={() => onNavigate('closing')}
        />
      </section>
    </main>
  );
}
