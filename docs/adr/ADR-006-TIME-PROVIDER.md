# ADR-006 — Time Provider

## Status

Proposed recommendation. This ADR is not accepted.

## Context

BeachOS timestamps are permanent operational and financial facts. Venue Opening
uses authoritative times for readiness declarations, official opening, Opening
Reports, Activity Logs, and safe request investigation. Device clocks cannot be
trusted, and Domain tests must remain deterministic.

The current Application boundary already depends on a clock interface.

## Problem

The platform needs one convention for obtaining, storing, comparing, testing, and
displaying time without allowing frameworks, clients, or database defaults to
become competing business-time authorities.

## Options

1. **Application-owned clock port backed by synchronized server time.** Generate
   timezone-aware universal instants and inject a deterministic fake in tests.
2. **Database-generated timestamps.** Use the database clock for every permanent
   time.
3. **Client-provided timestamps.** Accept the device’s reported time as the event
   time.
4. **Direct system-clock calls throughout the codebase.** Let each module call the
   language runtime independently.
5. **External time service on every Command.** Request time over the network for
   each action.

## Recommended Option

Use one Application-owned `Clock` port backed by monitored, synchronized server
time. Produce timezone-aware UTC instants for Domain actions and permanent records.
Convert to the approved Venue timezone only at presentation and Business Date
policy boundaries.

Inject controlled clocks in tests. Treat database creation times as technical
metadata unless they are explicitly supplied from the same Command context. Where
equal-time ordering matters, add a stable sequence or version rather than assuming
clock precision provides total order.

## Advantages

- One replaceable interface prevents scattered direct clock calls.
- UTC instants support comparison across Venues and timezones.
- Deterministic clocks make edge cases and tests reliable.
- Device clock manipulation cannot change official business time.
- Monitoring can detect unhealthy server time before it corrupts permanent facts.

## Disadvantages

- Application instances depend on reliable host clock synchronization.
- Display always requires timezone conversion.
- A separate sequence may be needed for events sharing the same timestamp.
- Database and application technical timestamps may differ slightly.

## Risks

- Server clock drift could misorder or misdate actions.
- Naive datetimes could enter the system through an adapter.
- Incorrect timezone conversion could confuse staff even when the stored instant is
  correct.
- Treating timestamp precision as unique ordering could create nondeterministic
  history.
- A future multi-region deployment may expose larger clock differences.

## Future Impact

Every Feature Pack should receive authoritative time through the shared
Application boundary rather than calling a framework or system clock directly.
Production readiness should include clock-health monitoring. Multi-region or
regulated workloads may later justify a stronger ordering or trusted-time
strategy, but Domain models should continue to consume explicit instants.
