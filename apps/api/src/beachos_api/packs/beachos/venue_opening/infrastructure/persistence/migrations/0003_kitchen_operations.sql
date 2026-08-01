CREATE TABLE kitchen_ticket_streams (
    ticket_id text PRIMARY KEY,
    stream_version bigint NOT NULL DEFAULT 0 CHECK (stream_version >= 0)
);

CREATE TABLE kitchen_events (
    ticket_id text NOT NULL,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL CHECK (
        event_type IN ('KITCHEN_TICKET_ACKNOWLEDGED')
    ),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ticket_id, sequence),
    FOREIGN KEY (ticket_id)
        REFERENCES kitchen_ticket_streams (ticket_id)
        ON DELETE RESTRICT
);

CREATE TABLE kitchen_command_receipts (
    request_id text PRIMARY KEY,
    ticket_id text NOT NULL,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER protect_kitchen_events
BEFORE UPDATE OR DELETE ON kitchen_events
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();

CREATE TRIGGER protect_kitchen_command_receipts
BEFORE UPDATE OR DELETE ON kitchen_command_receipts
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();
