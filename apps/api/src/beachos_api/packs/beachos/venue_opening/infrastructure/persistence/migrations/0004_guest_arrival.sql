CREATE TABLE guest_arrival_service_locations (
    service_location_id text PRIMARY KEY,
    venue_id text NOT NULL,
    visible_name text NOT NULL,
    digital_identity text NOT NULL,
    location_type text NOT NULL CHECK (location_type IN ('BEACH SUNBED', 'POOL SUNBED', 'UPPER TABLE', 'OTHER')),
    initial_status text NOT NULL CHECK (initial_status IN ('AVAILABLE', 'UNAVAILABLE', 'RETIRED')),
    stream_version bigint NOT NULL DEFAULT 0 CHECK (stream_version >= 0),
    beach_sunbed_charge numeric,
    charge_currency text,
    charge_description text,
    UNIQUE (venue_id, visible_name),
    UNIQUE (venue_id, digital_identity),
    CHECK (
        location_type <> 'BEACH SUNBED'
        OR (beach_sunbed_charge IS NOT NULL AND charge_currency IS NOT NULL AND charge_description IS NOT NULL)
    )
);

CREATE TABLE guest_arrival_events (
    service_location_id text NOT NULL REFERENCES guest_arrival_service_locations(service_location_id) ON DELETE RESTRICT,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL CHECK (event_type IN (
        'RESPONSIBLE_WAITER_ASSIGNED', 'CUSTOMER_GROUP_OPENED',
        'FINANCIAL_OBLIGATION_CREATED', 'BILL_CREATED', 'BILL_LINE_ADDED'
    )),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (service_location_id, sequence)
);

CREATE TABLE guest_arrival_command_receipts (
    request_id text PRIMARY KEY,
    service_location_id text NOT NULL REFERENCES guest_arrival_service_locations(service_location_id) ON DELETE RESTRICT,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE guest_arrival_activity_log (
    request_id text PRIMARY KEY,
    actor_id text NOT NULL,
    venue_id text NOT NULL,
    service_location_id text NOT NULL,
    customer_group_id text NOT NULL,
    action_name text NOT NULL CHECK (action_name = 'CUSTOMER_GROUP_OPENED'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER protect_guest_arrival_events BEFORE UPDATE OR DELETE ON guest_arrival_events
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_guest_arrival_receipts BEFORE UPDATE OR DELETE ON guest_arrival_command_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_guest_arrival_activity BEFORE UPDATE OR DELETE ON guest_arrival_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
