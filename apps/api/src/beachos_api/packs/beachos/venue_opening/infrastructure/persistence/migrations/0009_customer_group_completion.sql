CREATE TABLE customer_group_completion_streams (
    customer_group_id text PRIMARY KEY,
    stream_version bigint NOT NULL CHECK(stream_version >= 0)
);
CREATE TABLE customer_group_completion_events (
    customer_group_id text NOT NULL REFERENCES customer_group_completion_streams(customer_group_id) ON DELETE RESTRICT,
    sequence bigint NOT NULL CHECK(sequence > 0),
    event_type text NOT NULL CHECK(event_type='CUSTOMER_GROUP_COMPLETED'),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(customer_group_id,sequence)
);
CREATE TABLE customer_group_completion_receipts (
    request_id text PRIMARY KEY, customer_group_id text NOT NULL, result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE customer_group_completion_activity_log (
    request_id text PRIMARY KEY, customer_group_id text NOT NULL, actor_id text NOT NULL,
    action_name text NOT NULL CHECK(action_name='CUSTOMER_GROUP_COMPLETED'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER protect_completion_events BEFORE UPDATE OR DELETE ON customer_group_completion_events
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_completion_receipts BEFORE UPDATE OR DELETE ON customer_group_completion_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_completion_activity BEFORE UPDATE OR DELETE ON customer_group_completion_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
