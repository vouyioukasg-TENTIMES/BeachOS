ALTER TABLE venue_opening_venues
DROP CONSTRAINT venue_opening_venues_opening_status_check;

ALTER TABLE venue_opening_venues
ADD CONSTRAINT venue_opening_venues_opening_status_check CHECK (
    opening_status IN ('CLOSED','OPEN','CLOSED_FOR_BUSINESS_DATE')
);

CREATE FUNCTION beachos_require_open_venue_for_customer_group()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM venue_opening_venues
        WHERE venue_id=NEW.venue_id AND opening_status='OPEN'
    ) THEN
        RAISE EXCEPTION 'a Customer Group requires an OPEN Venue Business Date';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER require_open_venue_for_customer_group
BEFORE INSERT ON ordering_customer_groups
FOR EACH ROW EXECUTE FUNCTION beachos_require_open_venue_for_customer_group();

CREATE TABLE venue_closing_events (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    event_type text NOT NULL CHECK(event_type='VENUE_CLOSED'),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(venue_id,business_date),
    FOREIGN KEY(venue_id,business_date)
        REFERENCES venue_opening_venues(venue_id,business_date) ON DELETE RESTRICT
);

CREATE TABLE venue_closing_reports (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    closed_at timestamp with time zone NOT NULL,
    closed_by_id text NOT NULL,
    active_customer_groups integer NOT NULL CHECK(active_customer_groups=0),
    occupied_service_locations integer NOT NULL CHECK(occupied_service_locations=0),
    open_bills integer NOT NULL CHECK(open_bills=0),
    unresolved_operational_work integer NOT NULL CHECK(unresolved_operational_work=0),
    PRIMARY KEY(venue_id,business_date),
    FOREIGN KEY(venue_id,business_date)
        REFERENCES venue_opening_venues(venue_id,business_date) ON DELETE RESTRICT
);

CREATE TABLE venue_closing_receipts (
    request_id text PRIMARY KEY,
    venue_id text NOT NULL,
    business_date date NOT NULL,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(venue_id,business_date)
        REFERENCES venue_opening_venues(venue_id,business_date) ON DELETE RESTRICT
);

CREATE TABLE venue_closing_activity_log (
    request_id text PRIMARY KEY,
    venue_id text NOT NULL,
    business_date date NOT NULL,
    actor_id text NOT NULL,
    action_name text NOT NULL CHECK(action_name='VENUE_CLOSED'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(venue_id,business_date)
        REFERENCES venue_opening_venues(venue_id,business_date) ON DELETE RESTRICT
);

CREATE TRIGGER protect_venue_closing_events BEFORE UPDATE OR DELETE ON venue_closing_events
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_venue_closing_reports BEFORE UPDATE OR DELETE ON venue_closing_reports
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_venue_closing_receipts BEFORE UPDATE OR DELETE ON venue_closing_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_venue_closing_activity BEFORE UPDATE OR DELETE ON venue_closing_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
