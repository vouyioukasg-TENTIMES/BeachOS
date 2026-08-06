import { useEffect, useMemo, useState } from 'react';
import { BarWorkspace } from './BarWorkspace';
import { BillingWorkspace } from './BillingWorkspace';
import { CustomerGroupCompletionWorkspace } from './CustomerGroupCompletionWorkspace';
import { DepartmentReadinessWorkspace } from './DepartmentReadinessWorkspace';
import { FulfilmentWorkspace } from './FulfilmentWorkspace';
import { GuestArrivalWorkspace } from './GuestArrivalWorkspace';
import { GuestDepartureWorkspace } from './GuestDepartureWorkspace';
import { HostWorkspace } from './HostWorkspace';
import { KitchenWorkspace } from './KitchenWorkspace';
import { OrderingWorkspace } from './OrderingWorkspace';
import { OverviewDashboard, type Workspace } from './OverviewDashboard';
import { VenueClosingWorkspace } from './VenueClosingWorkspace';
import { getVenueContext, type VenueContext } from './venueOpeningApi';
import './app.css';

type Role = 'Host' | 'Responsible Waiter' | 'Kitchen' | 'Bar' | 'Cashier' | 'Manager';

const roles: Role[] = ['Host', 'Responsible Waiter', 'Kitchen', 'Bar', 'Cashier', 'Manager'];

const navigation: { id: Workspace; label: string; roles: Role[] }[] = [
  { id: 'overview', label: 'Overview', roles },
  { id: 'opening', label: 'Opening', roles: ['Host', 'Manager'] },
  { id: 'arrival', label: 'Guest Arrival', roles: ['Host', 'Responsible Waiter', 'Manager'] },
  {
    id: 'groups',
    label: 'Customer Groups',
    roles: ['Host', 'Responsible Waiter', 'Cashier', 'Manager'],
  },
  { id: 'orders', label: 'Orders', roles: ['Responsible Waiter', 'Manager'] },
  { id: 'kitchen', label: 'Kitchen', roles: ['Kitchen', 'Manager'] },
  { id: 'bar', label: 'Bar', roles: ['Bar', 'Manager'] },
  { id: 'billing', label: 'Billing', roles: ['Responsible Waiter', 'Cashier', 'Manager'] },
  { id: 'closing', label: 'Closing', roles: ['Host', 'Manager'] },
];

const roleIdentity: Record<Role, string> = {
  Host: 'development-host',
  'Responsible Waiter': 'staff-waiter-1',
  Kitchen: 'staff-kitchen',
  Bar: 'staff-bar',
  Cashier: 'development-host',
  Manager: 'development-host',
};

function statusLabel(status: VenueContext['opening_status'] | undefined) {
  if (!status) return 'Status unavailable';
  if (status === 'CLOSED_FOR_BUSINESS_DATE') return 'Closed for day';
  return status === 'OPEN' ? 'Open' : 'Before opening';
}

function DemoLauncher({ onStart }: { onStart: () => void }) {
  const [open, setOpen] = useState(false);
  if (!import.meta.env.DEV) return null;
  return (
    <div className="demo-launcher">
      <button
        className="demo-trigger"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
      >
        Demo Day <span>Development only</span>
      </button>
      {open && (
        <section className="demo-popover" aria-label="Demo Day launcher">
          <strong>Representative operational day</strong>
          <p>Start or resume using the configured local Venue and Customer Group.</p>
          <button
            className="primary-action"
            onClick={() => {
              onStart();
              setOpen(false);
            }}
          >
            Start or resume Demo Day
          </button>
          <button disabled title="No approved data-reset capability exists">
            Reset operational data
          </button>
          <small>
            Reset is unavailable until an approved development-data reset exists. No production
            workflow is affected.
          </small>
        </section>
      )}
    </div>
  );
}

function CustomerGroupsWorkspace({ customerGroupId }: { customerGroupId: string }) {
  return (
    <div className="combined-workspace">
      <header className="combined-heading">
        <p className="eyebrow">Customer Group lifecycle</p>
        <h1>Complete service, then confirm departure</h1>
        <p>
          Completion ends service. Departure is a separate action that releases the Service
          Location.
        </p>
      </header>
      <CustomerGroupCompletionWorkspace customerGroupId={customerGroupId} />
      <GuestDepartureWorkspace customerGroupId={customerGroupId} />
    </div>
  );
}

function OrdersWorkspace({
  customerGroupId,
  venueId,
}: {
  customerGroupId: string;
  venueId: string;
}) {
  return (
    <div className="combined-workspace">
      <OrderingWorkspace customerGroupId={customerGroupId} />
      <section className="journey-divider">
        <p className="eyebrow">After preparation</p>
        <h2>Collect and deliver confirmed Tickets</h2>
      </section>
      <FulfilmentWorkspace venueId={venueId} />
    </div>
  );
}

export function App() {
  const venueId = import.meta.env.VITE_VENUE_ID ?? 'venue-1';
  const customerGroupId = import.meta.env.VITE_CUSTOMER_GROUP_ID ?? 'customer-group-1';
  const [workspace, setWorkspace] = useState<Workspace>('overview');
  const [role, setRole] = useState<Role>('Host');
  const [venue, setVenue] = useState<VenueContext | null>(null);
  const [navOpen, setNavOpen] = useState(false);

  useEffect(() => {
    void getVenueContext(venueId)
      .then(setVenue)
      .catch(() => setVenue(null));
  }, [venueId, workspace]);

  const visibleNavigation = useMemo(
    () => navigation.filter((item) => item.roles.includes(role)),
    [role],
  );

  function navigate(next: Workspace) {
    setWorkspace(next);
    setNavOpen(false);
    window.scrollTo?.({ top: 0, behavior: 'smooth' });
  }

  function changeRole(next: Role) {
    setRole(next);
    const allowed = navigation.find((item) => item.id === workspace)?.roles.includes(next);
    if (!allowed) setWorkspace('overview');
  }

  return (
    <div className="beachos-shell">
      <a className="skip-link" href="#workspace-content">
        Skip to workspace
      </a>
      <header className="shell-header">
        <div className="brand-block">
          <button
            className="mobile-menu"
            onClick={() => setNavOpen((value) => !value)}
            aria-expanded={navOpen}
            aria-controls="main-navigation"
          >
            Menu
          </button>
          <button
            className="shell-wordmark"
            onClick={() => navigate('overview')}
            aria-label="BeachOS Overview"
          >
            <span aria-hidden="true">B</span>
            <strong>BeachOS</strong>
          </button>
        </div>
        <dl className="venue-context">
          <div>
            <dt>Venue</dt>
            <dd>{venue?.venue_name ?? venueId}</dd>
          </div>
          <div>
            <dt>Business Date</dt>
            <dd>{venue?.business_date ?? 'Unconfirmed'}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd>
              <span className={`status-pill ${venue?.opening_status === 'OPEN' ? 'positive' : ''}`}>
                {statusLabel(venue?.opening_status)}
              </span>
            </dd>
          </div>
        </dl>
        <div className="identity-context">
          <div>
            <small>Acting user</small>
            <strong>{roleIdentity[role]}</strong>
          </div>
          <label>
            <span>
              Role <b>Development only</b>
            </span>
            <select value={role} onChange={(event) => changeRole(event.target.value as Role)}>
              {roles.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
        </div>
      </header>

      <div className="shell-body">
        <aside className={navOpen ? 'shell-sidebar open' : 'shell-sidebar'}>
          <nav id="main-navigation" aria-label="Main navigation">
            <p>Workspace</p>
            {visibleNavigation.map((item) => (
              <button
                key={item.id}
                aria-current={workspace === item.id ? 'page' : undefined}
                onClick={() => navigate(item.id)}
              >
                {item.label}
              </button>
            ))}
          </nav>
          <div className="role-summary">
            <span>{role} workspace</span>
            <small>
              Navigation reflects the selected development role. The backend remains the authority
              for every action.
            </small>
          </div>
          <DemoLauncher
            onStart={() => navigate(venue?.opening_status === 'OPEN' ? 'overview' : 'opening')}
          />
        </aside>

        <section className="shell-main" id="workspace-content" tabIndex={-1}>
          {workspace === 'overview' ? (
            <OverviewDashboard
              venueId={venueId}
              customerGroupId={customerGroupId}
              role={role}
              onNavigate={navigate}
            />
          ) : workspace === 'opening' ? (
            <HostWorkspace venueId={venueId} />
          ) : workspace === 'readiness' ? (
            <DepartmentReadinessWorkspace venueId={venueId} />
          ) : workspace === 'arrival' ? (
            <GuestArrivalWorkspace venueId={venueId} />
          ) : workspace === 'groups' ? (
            <CustomerGroupsWorkspace customerGroupId={customerGroupId} />
          ) : workspace === 'orders' ? (
            <OrdersWorkspace customerGroupId={customerGroupId} venueId={venueId} />
          ) : workspace === 'kitchen' ? (
            <KitchenWorkspace venueId={venueId} />
          ) : workspace === 'bar' ? (
            <BarWorkspace venueId={venueId} />
          ) : workspace === 'fulfilment' ? (
            <FulfilmentWorkspace venueId={venueId} />
          ) : workspace === 'billing' ? (
            <BillingWorkspace customerGroupId={customerGroupId} />
          ) : (
            <VenueClosingWorkspace venueId={venueId} />
          )}
        </section>
      </div>
    </div>
  );
}
