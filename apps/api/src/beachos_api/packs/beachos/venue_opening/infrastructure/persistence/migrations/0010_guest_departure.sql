ALTER TABLE guest_arrival_events
DROP CONSTRAINT guest_arrival_events_event_type_check;

ALTER TABLE guest_arrival_events
ADD CONSTRAINT guest_arrival_events_event_type_check CHECK (event_type IN (
    'RESPONSIBLE_WAITER_ASSIGNED', 'CUSTOMER_GROUP_OPENED',
    'FINANCIAL_OBLIGATION_CREATED', 'BILL_CREATED', 'BILL_LINE_ADDED',
    'GUEST_DEPARTED'
));

CREATE TABLE guest_departure_receipts (
    request_id text PRIMARY KEY,
    customer_group_id text NOT NULL,
    service_location_id text NOT NULL REFERENCES guest_arrival_service_locations(service_location_id) ON DELETE RESTRICT,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE guest_departure_activity_log (
    request_id text PRIMARY KEY,
    customer_group_id text NOT NULL,
    service_location_id text NOT NULL,
    actor_id text NOT NULL,
    action_name text NOT NULL CHECK(action_name='GUEST_DEPARTED'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX one_guest_departure_per_customer_group
ON guest_arrival_events ((event_data->>'customer_group_id'))
WHERE event_type='GUEST_DEPARTED';

CREATE TRIGGER protect_guest_departure_receipts
BEFORE UPDATE OR DELETE ON guest_departure_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();

CREATE TRIGGER protect_guest_departure_activity
BEFORE UPDATE OR DELETE ON guest_departure_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
