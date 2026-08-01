# ADR-001 — Persistence Strategy

## Status

Proposed recommendation. This ADR is not accepted.

## Context

BeachOS must preserve operational and financial truth across restarts, concurrent
users, multiple devices, and future Venues. The approved architecture begins as a
modular monolith, keeps persistence outside the Domain and Application Layers, and
identifies PostgreSQL as the initial relational database direction.

Venue Opening is the first capability that requires durable current state,
historical readiness declarations, one official Opening Report, a required Activity
Log, and safe repeated-request handling.

## Problem

The platform needs one default persistence strategy that protects consistency
without coupling business concepts to a database library or prematurely adding
multiple storage technologies.

## Options

1. **One relational system of record.** Use PostgreSQL for authoritative
   transactional state and history, with explicit mappings between persistence
   records and Domain objects.
2. **Document database as the primary store.** Persist aggregates as documents and
   coordinate cross-document consistency where required.
3. **Event sourcing as the primary persistence model.** Rebuild current state from
   a complete event stream.
4. **Polyglot persistence from the beginning.** Select different datastores for
   different modules.

## Recommended Option

Use PostgreSQL as the single authoritative transactional system of record for the
initial platform. Keep persistence models and mappings in Infrastructure, use
versioned migrations, and allow Domain and Application code to remain unaware of
the selected database and mapping library.

Do not introduce event sourcing, a document database, a cache as a source of truth,
or module-specific datastores without a later ADR supported by measured need.
Specific Python persistence and migration libraries remain separate approval
decisions.

## Advantages

- Strong transactions and relational constraints suit operational and financial
  invariants.
- One system of record simplifies backup, recovery, local development, and
  operational ownership.
- PostgreSQL supports current state, append-only history, reporting, and future
  read models without requiring several systems immediately.
- Infrastructure mappings protect the Domain from storage concerns.
- The approach fits the approved modular-monolith direction.

## Disadvantages

- Relational mapping requires deliberate translation between Domain objects and
  stored records.
- Schema evolution requires disciplined migrations.
- Some future analytical or high-volume workloads may eventually need specialized
  stores.
- A single database can become a scaling bottleneck if module ownership and query
  boundaries are ignored.

## Risks

- Persistence models may leak into Domain, API, or shared packages.
- Teams may treat database tables as cross-module public contracts.
- Reporting queries may interfere with live operations if not isolated responsibly.
- “PostgreSQL can do everything” may delay evidence-based specialization when it
  eventually becomes necessary.
- Poor migration or backup practices could weaken otherwise strong consistency.

## Future Impact

Every Feature Pack should default to the shared relational system of record while
owning its persistence boundary. Future extraction to another datastore or service
must preserve official business history and be justified by scale, reliability,
compliance, or ownership evidence. This recommendation establishes a conservative
starting point, not a permanent ban on specialized storage.
