import { useState } from 'react';
import { HostWorkspace } from './HostWorkspace';
import { GuestArrivalWorkspace } from './GuestArrivalWorkspace';
import { DepartmentReadinessWorkspace } from './DepartmentReadinessWorkspace';
import { KitchenWorkspace } from './KitchenWorkspace';
import { OrderingWorkspace } from './OrderingWorkspace';
import { BarWorkspace } from './BarWorkspace';
import { FulfilmentWorkspace } from './FulfilmentWorkspace';
import './app.css';

export function App() {
  const venueId = import.meta.env.VITE_VENUE_ID ?? 'venue-1';
  const customerGroupId = import.meta.env.VITE_CUSTOMER_GROUP_ID ?? 'customer-group-1';
  const [workspace, setWorkspace] = useState<
    'host' | 'readiness' | 'arrival' | 'ordering' | 'kitchen' | 'bar' | 'fulfilment'
  >('host');

  return (
    <>
      <nav className="workspace-nav" aria-label="Workspaces">
        <button aria-pressed={workspace === 'host'} onClick={() => setWorkspace('host')}>
          Host
        </button>
        <button aria-pressed={workspace === 'readiness'} onClick={() => setWorkspace('readiness')}>
          Department Readiness
        </button>
        <button aria-pressed={workspace === 'arrival'} onClick={() => setWorkspace('arrival')}>
          Guest Arrival
        </button>
        <button aria-pressed={workspace === 'ordering'} onClick={() => setWorkspace('ordering')}>
          Ordering
        </button>
        <button aria-pressed={workspace === 'kitchen'} onClick={() => setWorkspace('kitchen')}>
          Kitchen
        </button>
        <button aria-pressed={workspace === 'bar'} onClick={() => setWorkspace('bar')}>
          Bar
        </button>
        <button
          aria-pressed={workspace === 'fulfilment'}
          onClick={() => setWorkspace('fulfilment')}
        >
          Fulfilment
        </button>
      </nav>
      {workspace === 'host' ? (
        <HostWorkspace venueId={venueId} />
      ) : workspace === 'readiness' ? (
        <DepartmentReadinessWorkspace venueId={venueId} />
      ) : workspace === 'arrival' ? (
        <GuestArrivalWorkspace venueId={venueId} />
      ) : workspace === 'ordering' ? (
        <OrderingWorkspace customerGroupId={customerGroupId} />
      ) : workspace === 'kitchen' ? (
        <KitchenWorkspace venueId={venueId} />
      ) : workspace === 'bar' ? (
        <BarWorkspace venueId={venueId} />
      ) : (
        <FulfilmentWorkspace venueId={venueId} />
      )}
    </>
  );
}
