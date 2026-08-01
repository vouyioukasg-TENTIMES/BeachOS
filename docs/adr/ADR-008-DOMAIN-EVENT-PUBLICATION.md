# ADR-008 — Domain Event Publication

## Status

Proposed recommendation. This ADR is not accepted.

## Context

Domain Events describe approved business facts that have already happened. They do
not imply event sourcing, a message broker, or microservices. BeachOS will
eventually need reliable post-commit reactions such as live refresh notices,
reporting updates, integrations, and future plugins.

Publishing before durable commit can announce facts that later roll back.
Publishing directly after commit can lose a notification if the process stops
between commit and delivery.

## Problem

The platform needs a publication strategy that preserves the database as
authoritative truth, avoids false events, tolerates delivery failure, and does not
couple Domain code to transports or external consumers.

## Options

1. **Transactional outbox.** Store approved publishable event records in the same
   transaction as state, then dispatch them asynchronously after commit.
2. **Immediate in-process publication before commit.** Invoke handlers as soon as
   the aggregate emits events.
3. **Best-effort publication after commit.** Publish directly to consumers once the
   transaction succeeds, without a durable handoff.
4. **Synchronous broker publication inside the transaction.** Require an external
   broker call before database commit.
5. **Event sourcing.** Make the event stream itself the authoritative persistence
   model.

## Recommended Option

Use a transactional outbox for Domain Events that have approved external or
cross-module consumers. During the Command transaction, persist the authoritative
state and an immutable outbox representation of each approved publishable event.
After commit, a dispatcher delivers versioned messages with stable event identity,
business scope, occurrence time, and schema version.

Consumers must be idempotent and must tolerate duplicates, delay, and out-of-order
delivery. Live notices should prompt authoritative refresh rather than become an
alternate source of truth. Domain code emits business events but knows nothing
about the outbox, dispatcher, broker, or plugin.

Not every internal Domain Event must be published externally. Publication requires
an approved consumer contract and data-scope review.

## Advantages

- State and publishable-event handoff are atomic.
- Delivery can recover after process or network failure.
- Domain and Application Layers remain transport-independent.
- Consumers can evolve independently through versioned contracts.
- Supports later integrations and plugins without making them part of the Command
  transaction.

## Disadvantages

- Requires outbox storage, a dispatcher, retries, monitoring, and cleanup.
- Delivery is eventually consistent.
- Consumers must handle duplicates and ordering explicitly.
- Event contract governance adds design and compatibility work.
- The pattern is more complex than direct in-process handling for a single module.

## Risks

- Publishing every internal event may expose private data or create excessive
  coupling.
- An unmonitored outbox backlog could leave consumers stale.
- Schema changes could break consumers.
- Incorrect cleanup could delete undelivered records or retain sensitive data too
  long.
- Consumers may mistakenly treat message arrival order as authoritative business
  order.
- A live notice may be mistaken for proof of committed state if contracts are
  unclear.

## Future Impact

Future Feature Packs, Industry Packs, and plugins can subscribe only to explicitly
approved, versioned public events. The primary database remains authoritative, and
consumer failure does not reverse a completed local business outcome. A message
broker may be introduced later as a dispatcher transport without changing Domain
or Application contracts; it is not required merely by this recommendation.
