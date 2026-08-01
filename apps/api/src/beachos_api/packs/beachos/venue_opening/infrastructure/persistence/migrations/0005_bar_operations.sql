CREATE TABLE bar_ticket_streams (
    ticket_id text PRIMARY KEY,
    stream_version bigint NOT NULL DEFAULT 0 CHECK (stream_version >= 0)
);
CREATE TABLE bar_events (
    ticket_id text NOT NULL,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL CHECK (event_type IN ('BAR_TICKET_ACKNOWLEDGED')),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ticket_id, sequence),
    FOREIGN KEY (ticket_id) REFERENCES bar_ticket_streams(ticket_id) ON DELETE RESTRICT
);
CREATE TABLE bar_command_receipts (
    request_id text PRIMARY KEY,
    ticket_id text NOT NULL,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER protect_bar_events BEFORE UPDATE OR DELETE ON bar_events FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_bar_command_receipts BEFORE UPDATE OR DELETE ON bar_command_receipts FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
