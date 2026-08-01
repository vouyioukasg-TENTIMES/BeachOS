ALTER TABLE kitchen_events DROP CONSTRAINT kitchen_events_event_type_check;
ALTER TABLE kitchen_events ADD CONSTRAINT kitchen_events_event_type_check CHECK (
    event_type IN (
        'KITCHEN_TICKET_ACKNOWLEDGED',
        'KITCHEN_TICKET_READY',
        'KITCHEN_TICKET_COLLECTED',
        'KITCHEN_TICKET_DELIVERED'
    )
);

ALTER TABLE bar_events DROP CONSTRAINT bar_events_event_type_check;
ALTER TABLE bar_events ADD CONSTRAINT bar_events_event_type_check CHECK (
    event_type IN (
        'BAR_TICKET_ACKNOWLEDGED',
        'BAR_TICKET_READY',
        'BAR_TICKET_COLLECTED',
        'BAR_TICKET_DELIVERED'
    )
);
