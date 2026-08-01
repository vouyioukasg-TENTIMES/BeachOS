CREATE TABLE payment_streams (
    bill_id text PRIMARY KEY,
    customer_group_id text NOT NULL,
    stream_version bigint NOT NULL CHECK (stream_version >= 0)
);
CREATE TABLE payment_events (
    bill_id text NOT NULL REFERENCES payment_streams(bill_id) ON DELETE RESTRICT,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL CHECK (event_type IN ('PAYMENT_RECORDED','BILL_FULLY_PAID')),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (bill_id, sequence)
);
CREATE TABLE payment_command_receipts (
    request_id text PRIMARY KEY, bill_id text NOT NULL,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE payment_activity_log (
    request_id text PRIMARY KEY, payment_id text NOT NULL UNIQUE, bill_id text NOT NULL,
    customer_group_id text NOT NULL, actor_id text NOT NULL,
    action_name text NOT NULL CHECK (action_name='PAYMENT_RECORDED'),
    amount numeric NOT NULL CHECK (amount > 0), currency text NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER protect_payment_events BEFORE UPDATE OR DELETE ON payment_events
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_payment_receipts BEFORE UPDATE OR DELETE ON payment_command_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_payment_activity BEFORE UPDATE OR DELETE ON payment_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
