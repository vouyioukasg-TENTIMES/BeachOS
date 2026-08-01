ALTER TABLE payment_events DROP CONSTRAINT payment_events_event_type_check;
ALTER TABLE payment_events ADD CONSTRAINT payment_events_event_type_check
CHECK (event_type IN ('PAYMENT_RECORDED','BILL_FULLY_PAID','BILL_CLOSED'));
CREATE TABLE bill_closing_receipts (
    request_id text PRIMARY KEY, bill_id text NOT NULL, result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE bill_closing_activity_log (
    request_id text PRIMARY KEY, bill_id text NOT NULL, customer_group_id text NOT NULL,
    actor_id text NOT NULL, action_name text NOT NULL CHECK(action_name='BILL_CLOSED'),
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER protect_bill_closing_receipts BEFORE UPDATE OR DELETE ON bill_closing_receipts
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
CREATE TRIGGER protect_bill_closing_activity BEFORE UPDATE OR DELETE ON bill_closing_activity_log
FOR EACH ROW EXECUTE FUNCTION beachos_reject_immutable_history_change();
