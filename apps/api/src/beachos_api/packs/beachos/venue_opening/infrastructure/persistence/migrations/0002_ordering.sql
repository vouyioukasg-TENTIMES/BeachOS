CREATE TABLE ordering_customer_groups (
    customer_group_id text PRIMARY KEY,
    venue_id text NOT NULL,
    service_location_id text NOT NULL,
    responsible_waiter_id text NOT NULL,
    status text NOT NULL CHECK (status IN ('ACTIVE', 'COMPLETED')),
    stream_version bigint NOT NULL DEFAULT 0 CHECK (stream_version >= 0)
);

CREATE TABLE ordering_menu_items (
    venue_id text NOT NULL,
    menu_item_id text NOT NULL,
    category_name text NOT NULL,
    category_order integer NOT NULL CHECK (category_order >= 0),
    item_name text NOT NULL,
    item_order integer NOT NULL CHECK (item_order >= 0),
    unit_price numeric NOT NULL CHECK (unit_price >= 0),
    currency text NOT NULL,
    destination text NOT NULL
        CHECK (destination IN ('BAR', 'KITCHEN', 'NO PREPARATION')),
    available boolean NOT NULL,
    PRIMARY KEY (venue_id, menu_item_id),
    UNIQUE (venue_id, category_order, item_order)
);

CREATE TABLE ordering_events (
    customer_group_id text NOT NULL,
    sequence bigint NOT NULL CHECK (sequence > 0),
    event_type text NOT NULL CHECK (
        event_type IN (
            'ORDER_SUBMITTED',
            'KITCHEN_TICKET_CREATED',
            'BAR_TICKET_CREATED',
            'FINANCIAL_OBLIGATION_CREATED',
            'BILL_CREATED',
            'BILL_LINE_ADDED'
        )
    ),
    event_data jsonb NOT NULL,
    occurred_at timestamp with time zone NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_group_id, sequence),
    FOREIGN KEY (customer_group_id)
        REFERENCES ordering_customer_groups (customer_group_id)
        ON DELETE RESTRICT
);

CREATE TABLE ordering_command_receipts (
    request_id text PRIMARY KEY,
    customer_group_id text NOT NULL,
    result_data jsonb NOT NULL,
    recorded_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER protect_ordering_events
BEFORE UPDATE OR DELETE ON ordering_events
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();

CREATE TRIGGER protect_ordering_command_receipts
BEFORE UPDATE OR DELETE ON ordering_command_receipts
FOR EACH ROW
EXECUTE FUNCTION beachos_reject_immutable_history_change();
