CREATE TABLE venue_business_date_policies (
    venue_id text PRIMARY KEY,
    timezone_name text NOT NULL,
    rollover_time time without time zone NOT NULL
);

CREATE TABLE venue_opening_venues (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    venue_name text NOT NULL,
    opening_status text NOT NULL
        CHECK (opening_status IN ('CLOSED', 'OPEN')),
    aggregate_version bigint NOT NULL
        CHECK (aggregate_version >= 0),
    PRIMARY KEY (venue_id, business_date)
);

CREATE TABLE venue_opening_departments (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    department_id text NOT NULL,
    display_order integer NOT NULL
        CHECK (display_order >= 0),
    department_name text NOT NULL,
    responsible_person_id text NOT NULL,
    PRIMARY KEY (venue_id, business_date, department_id),
    UNIQUE (venue_id, business_date, display_order),
    FOREIGN KEY (venue_id, business_date)
        REFERENCES venue_opening_venues (venue_id, business_date)
        ON DELETE RESTRICT
);

CREATE TABLE venue_opening_declarations (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    declaration_sequence bigint NOT NULL
        CHECK (declaration_sequence > 0),
    department_id text NOT NULL,
    responsible_person_id text NOT NULL,
    declared_by_id text NOT NULL,
    readiness_status text NOT NULL
        CHECK (readiness_status IN ('READY', 'NOT READY', 'BLOCKED')),
    declared_at timestamp with time zone NOT NULL,
    reason text,
    comment text,
    PRIMARY KEY (venue_id, business_date, declaration_sequence),
    FOREIGN KEY (venue_id, business_date, department_id)
        REFERENCES venue_opening_departments (
            venue_id,
            business_date,
            department_id
        )
        ON DELETE RESTRICT,
    CHECK (
        readiness_status = 'READY'
        OR reason IS NOT NULL
    )
);

CREATE TABLE venue_opening_reports (
    venue_id text NOT NULL,
    business_date date NOT NULL,
    opened_at timestamp with time zone NOT NULL,
    host_id text NOT NULL,
    PRIMARY KEY (venue_id, business_date),
    FOREIGN KEY (venue_id, business_date)
        REFERENCES venue_opening_venues (venue_id, business_date)
        ON DELETE RESTRICT
);

CREATE TABLE venue_opening_activity_log (
    request_id text PRIMARY KEY,
    actor_id text NOT NULL,
    venue_id text NOT NULL,
    business_date date NOT NULL,
    action_name text NOT NULL
        CHECK (action_name = 'VENUE_OPENED_FOR_BUSINESS_DATE'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (venue_id, business_date)
        REFERENCES venue_opening_venues (venue_id, business_date)
        ON DELETE RESTRICT
);

CREATE FUNCTION beachos_reject_immutable_history_change()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION 'immutable BeachOS history cannot be changed or deleted';
END;
$$;

CREATE TRIGGER protect_venue_opening_declarations
BEFORE UPDATE OR DELETE ON venue_opening_declarations
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();

CREATE TRIGGER protect_venue_opening_reports
BEFORE UPDATE OR DELETE ON venue_opening_reports
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();

CREATE TRIGGER protect_venue_opening_activity_log
BEFORE UPDATE OR DELETE ON venue_opening_activity_log
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();
