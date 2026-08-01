# ADR-004 — Transaction Boundary

## Status

Proposed recommendation. This ADR is not accepted.

## Context

BeachOS Commands can affect authoritative state, immutable history, Activity Logs,
request identity, and publishable Domain Events. Venue Opening must not report
success unless the Venue state, Opening Report, and required Activity Log are
consistent. Concurrent declarations and repeated opening attempts must not create a
false or duplicate result.

The Application Layer already defines a unit-of-work port so Infrastructure can
provide an atomic boundary without leaking database behavior inward.

## Problem

The platform needs a repeatable transaction rule for every Command, especially when
one business outcome touches several stored representations.

## Options

1. **One database transaction per Application Command.** Load authoritative state,
   invoke Domain behavior, stage all required writes, and commit once.
2. **One transaction per repository operation.** Each save or log write commits
   independently.
3. **Long-running transaction across user interaction.** Begin when a workflow
   screen opens and commit after the user completes several steps.
4. **Distributed transaction across multiple services or stores.** Coordinate
   every participant as one atomic operation.

## Recommended Option

Use one short database transaction per state-changing Application Command.
Re-check authoritative state inside that boundary, stage aggregate changes,
required immutable history, Activity Log records, request-id outcome, and any
transactional publication record, then commit once before returning success.

Use optimistic aggregate version checks plus essential database uniqueness
constraints. Never hold a transaction open while waiting for a person, device, or
network interaction. Queries use separate read-only boundaries appropriate to
their consistency needs.

## Advantages

- Protects business state and required accountability from partial success.
- Gives each Command one clear commit or rollback outcome.
- Supports safe concurrency and duplicate prevention.
- Keeps transaction mechanics in Infrastructure while Application owns the unit of
  work.
- Avoids long locks during human workflows.

## Disadvantages

- Commands touching several aggregates require deliberate locking and consistency
  design.
- Optimistic conflicts need explicit Application outcomes and user recovery.
- Activity Log and publication staging add work to the transaction.
- A single transaction cannot cover an unavailable external system safely.

## Risks

- Incorrect operation ordering may create deadlocks.
- Returning success before commit would create false confirmation.
- Retrying an unknown outcome without request identity may repeat an action.
- External calls inside the transaction may hold locks and reduce availability.
- Missing uniqueness constraints may allow a second successful daily opening.

## Future Impact

Every state-changing use case should declare its transaction boundary and
idempotency needs during design. Future external integrations should use local
atomic state plus recoverable asynchronous coordination rather than expanding a
database transaction across networks. Service extraction must preserve the same
business outcome guarantees through explicit consistency patterns.
