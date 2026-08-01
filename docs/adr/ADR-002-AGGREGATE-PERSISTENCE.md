# ADR-002 — Aggregate Persistence

## Status

Proposed recommendation. This ADR is not accepted.

## Context

BeachOS Domain aggregates protect business invariants. The Venue aggregate
currently owns Venue Opening state, current department readiness, declaration
history, the official Opening Report, and approved Domain Events. Domain objects
are not database records and must remain usable without Infrastructure.

The platform must restore an aggregate accurately, detect conflicting changes, and
preserve immutable historical facts without requiring event sourcing.

## Problem

The Infrastructure Layer needs a consistent way to store and reconstruct
aggregates while preventing storage structure from weakening Domain boundaries or
silently rewriting history.

## Options

1. **State-based aggregate persistence with explicit mapping.** Store current
   aggregate state and required append-only history, then reconstruct the Domain
   aggregate through a mapper.
2. **Serialize the entire Domain object graph.** Store one opaque aggregate payload
   and deserialize it directly.
3. **Active Record Domain objects.** Give Domain entities database save and query
   behavior.
4. **Event-source every aggregate.** Store only Domain Events and replay them to
   reconstruct current state.

## Recommended Option

Use state-based aggregate persistence with explicit Infrastructure mappings.
Persist the authoritative current state needed to restore the aggregate, preserve
required historical facts in append-only form, and maintain an aggregate version
for optimistic conflict detection.

For Venue Opening, the latest declarations support current decisions while the
complete approved declaration history and official Opening Report remain
preserved. Reconstruction must not emit new Domain Events or re-run completed
business actions.

## Advantages

- Keeps Domain models independent from persistence libraries.
- Loads current operational state without replaying an unlimited event history.
- Preserves permanent history where the business requires it.
- Supports optimistic concurrency at the aggregate boundary.
- Allows persistence schemas to evolve independently from Domain constructors and
  public contracts.

## Disadvantages

- Requires mapping code and reconstruction tests.
- Current state and append-only history must be kept consistent.
- Aggregate schema changes need explicit migration and compatibility planning.
- Developers must distinguish restoration from new Domain behavior.

## Risks

- Hydration may bypass or accidentally trigger Domain invariants incorrectly.
- Saving a partial aggregate could lose current state or history.
- Mapping code may silently omit a new Domain field.
- Reconstructed aggregates may emit duplicate events if restoration behavior is
  not explicit.
- Large aggregate histories may require carefully designed loading boundaries.

## Future Impact

Every future aggregate should define its consistency boundary, reconstruction
requirements, version, and permanent history before its Infrastructure adapter is
built. Large histories may later be exposed through separate read models while the
aggregate loads only the facts required for decisions. Event sourcing would remain
a separate, evidence-driven architectural decision.
