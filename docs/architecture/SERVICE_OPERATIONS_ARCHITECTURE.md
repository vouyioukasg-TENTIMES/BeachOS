# Service Operations Architecture Review

## Purpose

This review determines how BeachOS should structure Kitchen Operations and Bar
Operations before Bar implementation begins.

It does not change the approved Domain Model, Domain Events, APIs, or current
Kitchen implementation. It compares two architectural directions and recommends
how future implementation can reduce duplication without combining business
concepts that the Domain keeps separate.

## Authoritative Constraints

The frozen product foundation establishes the following boundaries:

- `Kitchen Ticket` and `Bar Ticket` are separate official business concepts.
- `Kitchen Ticket Created` and `Bar Ticket Created` are separate official Domain
  Events.
- `Kitchen Ticket Acknowledged` and `Bar Ticket Acknowledged` are separate
  official Domain Events.
- Kitchen Staff and Bar Staff recognize responsibility for their own confirmed
  work.
- Each Ticket belongs to one Order and contains only items for its configured
  destination.
- A Ticket is operational work, not another Order, Bill, or financial charge.
- Original submission context remains historical truth; current Service
  Location context must remain discoverable.
- Ready and Completed events exist in the approved vocabulary but their commands
  remain gated because their exact business rules are unresolved.
- Preparation priority, estimates, delays, stations, partial readiness,
  delivery, cancellation effects, and offline behavior must not be inferred.
- Capability checks remain independent from Role names.
- Operational Intelligence must identify the decision, use confirmed facts,
  preserve uncertainty, and leave the human decision with the responsible
  authorized person.

These constraints mean reuse is permitted only when it preserves concrete
Kitchen and Bar language, event ownership, capability boundaries, and future
independent evolution.

# Option A — Independent Kitchen and Bar Implementations

## Description

Kitchen and Bar would each have a complete feature pack with its own Domain
types, Application services, ports, infrastructure mappings, event stream,
delivery adapters, frontend workspace, and tests.

The Bar implementation would copy the structural approach already used by
Kitchen Operations and replace Kitchen-specific concepts with Bar-specific
ones.

## Domain Boundaries

This option makes the boundary immediately obvious. Kitchen concepts cannot
accidentally appear in Bar behavior, and Bar concepts cannot alter Kitchen
behavior.

The cost is duplication of rules that are currently identical:

- confirmed work originates from one destination-specific Ticket;
- the Ticket references one Order and one Customer Group;
- original and current Service Location context remain distinguishable;
- acknowledgement is intentional and cannot be repeated;
- history is append-only;
- command retries are idempotent;
- uncertain outcomes are not reported as success.

If the duplicated implementations later evolve differently by accident, the
same approved business meaning could behave inconsistently.

## Event Ownership

Ownership is simple:

- Ordering owns `Kitchen Ticket Created` and `Bar Ticket Created`.
- Kitchen owns Kitchen acknowledgement and later approved Kitchen events.
- Bar owns Bar acknowledgement and later approved Bar events.

Separate mappings and streams make ownership visible, but duplicate event-store
mechanics and receipt handling.

## Aggregate Ownership

Kitchen owns a `KitchenTicket` aggregate. Bar owns a `BarTicket` aggregate.

This strongly protects aggregate language and invariants. It also produces two
nearly identical aggregate implementations for the currently approved
acknowledgement lifecycle.

## Capability Isolation

Isolation is strong and straightforward:

- Acknowledge Kitchen Ticket is checked only by Kitchen Application behavior.
- Acknowledge Bar Ticket is checked only by Bar Application behavior.

There is little risk of authorizing a Bar action through a Kitchen capability,
provided copied code is updated correctly. Copying itself creates a review risk:
a missed name, capability, event, or error message can silently cross the
boundary.

## Operational Intelligence Alignment

Each workspace can use department-specific language and facts without
translation.

However, duplicated reasoning code may eventually classify equivalent
uncertainty or attention differently. Kitchen and Bar could then communicate
the same operational condition inconsistently without an approved business
reason.

## Future Extensibility

Independent packs make department-specific evolution easy:

- Kitchen stations, courses, and food-safety concerns can remain in Kitchen.
- Bar stations, immediate fulfillment, cocktail preparation, and Bar-specific
  handoff can remain in Bar.

Adding another preparation destination would require another full
implementation, even when most mechanics are shared.

## Maintenance Cost

Initial implementation is familiar but expensive over time. Every correction to
event replay, optimistic concurrency, command receipts, uncertainty handling,
or context reconstruction must be applied and tested in both packs.

The same cost repeats for each later service department.

## Risk of Accidental Coupling

Direct coupling between Kitchen and Bar is low.

Indirect coupling through copied code is significant. The implementations may
look independent while sharing assumptions that are changed in one copy and
missed in another. Copy-and-rename errors also risk publishing the wrong
concrete event or checking the wrong capability.

# Option B — Shared Service Operations Architecture

## Description

Kitchen and Bar remain separate business capabilities, with concrete names,
events, permissions, workspaces, and future rules. They use a small internal
Service Operations architecture for mechanics and policies that are genuinely
identical.

This option must not create one generic business concept called “Service
Ticket” that replaces Kitchen Ticket or Bar Ticket. `Preparation Ticket`
remains a general business phrase; the current official concepts and events are
concrete.

The shared architecture is therefore an internal reuse boundary, not a new
Domain decision.

## Domain Boundaries

The business boundary remains explicit:

- Kitchen code speaks about Kitchen Tickets and Kitchen Staff.
- Bar code speaks about Bar Tickets and Bar Staff.
- Concrete capability modules own business commands and policy.
- Shared code contains only department-neutral mechanics whose meaning is
  already identical.

This preserves Domain language while preventing mechanical duplication.

The design becomes unsafe if generic abstractions start deciding preparation
rules, defining a universal lifecycle, or forcing Kitchen and Bar to evolve
together.

## Event Ownership

Concrete event ownership remains unchanged:

- Ordering owns the two concrete Ticket Created events.
- Kitchen owns concrete Kitchen operational events.
- Bar owns concrete Bar operational events.

A shared event-store adapter may persist and replay concrete events, but it does
not rename them, merge their streams, or decide which events a capability may
emit.

Event type registration must be explicit. A department identifier must never be
used to manufacture an event name dynamically without a concrete registered
mapping.

## Aggregate Ownership

Kitchen and Bar retain concrete aggregate ownership.

They may compose a small reusable event-sourced acknowledgement mechanism, or
conform to a narrow internal contract required by shared persistence. The shared
mechanism may protect only already-common invariants:

- an acknowledgement belongs to the correct Ticket;
- the actor and time are present and valid;
- acknowledgement cannot be repeated;
- replay emits no new events;
- aggregate version follows accepted events.

It must not own readiness, completion, priority, cancellation, delivery, or
station rules.

If later approved rules diverge, the concrete aggregate must be able to replace
or extend the shared mechanism without migration of unrelated capability code.

## Capability Isolation

Commands, capability checks, and Application services stay concrete:

- `AcknowledgeKitchenTicket` requires its Kitchen capability.
- `AcknowledgeBarTicket` requires its Bar capability.

The shared architecture may coordinate a command only after receiving a
concrete capability policy and concrete event factory. It must never accept a
generic “acknowledge any service work” permission.

Separate dependency-injection registrations and separate HTTP delivery
boundaries remain appropriate.

## Operational Intelligence Alignment

Shared operational reasoning can keep equivalent handling consistent:

- confirmed versus uncertain outcomes;
- new work awaiting acknowledgement;
- safe retry through a command receipt;
- reload guidance after an unknown result;
- distinction between original and current Service Location;
- neutral presentation of work without inferred priority.

Concrete modules still supply department language, responsible people, allowed
actions, and approved advice. Shared code must not assume that Kitchen and Bar
have the same readiness, completion, urgency, or service-handoff rules.

## Future Extensibility

A bounded shared architecture supports future concrete capabilities such as a
new approved preparation destination without copying storage and orchestration
mechanics.

It also allows Kitchen and Bar to diverge where hospitality operations demand
it. New abstractions should be introduced only after at least two concrete
capabilities demonstrate the same approved need.

This follows the BeachOS industry-pack philosophy: share a stable Core Platform
while keeping operational packs specific.

## Maintenance Cost

Shared mechanics reduce repeated work in:

- event stream loading and append;
- optimistic concurrency;
- idempotent command receipts;
- source Ticket reconstruction;
- transaction boundaries;
- common result uncertainty;
- standard context queries and paging when later approved;
- contract tests for infrastructure guarantees.

The architecture has an initial design and migration cost. That cost is
justified only if the shared boundary stays smaller than the concrete
capabilities.

## Risk of Accidental Coupling

The main risk is creating a premature generic model that forces Kitchen and Bar
into one lifecycle.

Controls are required:

- concrete events and commands must remain outside the shared kernel;
- no shared enum may define unapproved preparation states;
- no shared policy may decide readiness, completion, priority, or delay;
- capability checks must be injected as concrete policies;
- Kitchen must not import Bar, and Bar must not import Kitchen;
- shared code must not import either capability;
- shared persistence must use explicit event registrations;
- department-specific tests must remain mandatory;
- a shared change must not silently alter a concrete business outcome.

With these controls, accidental coupling is lower than with copied
implementations because common behavior has one tested implementation while
business behavior remains isolated.

# Comparison

| Criterion                    | Option A: Independent Implementations                  | Option B: Shared Architecture with Separate Capabilities  |
| ---------------------------- | ------------------------------------------------------ | --------------------------------------------------------- |
| Domain clarity               | Very high initially                                    | High if concrete language remains authoritative           |
| Event ownership              | Explicit but duplicated mechanically                   | Explicit concrete ownership with shared mechanics         |
| Aggregate ownership          | Fully separate                                         | Separate aggregates using narrow reusable mechanics       |
| Capability isolation         | Strong                                                 | Strong when commands and policies remain concrete         |
| Operational Intelligence     | Easy to tailor; consistency may drift                  | Consistent uncertainty mechanics with concrete advice     |
| Future divergence            | Easy                                                   | Easy only if the shared boundary remains small            |
| New destination support      | Requires copying a complete pack                       | Reuses mechanics while adding a concrete capability       |
| Maintenance cost             | High and grows per destination                         | Lower after a controlled initial extraction               |
| Copy-and-rename risk         | High                                                   | Low                                                       |
| Premature abstraction risk   | Low                                                    | Medium; requires strict controls                          |
| Accidental business coupling | Low through imports, medium through copied assumptions | Medium without controls, low with the proposed boundaries |

# Recommended Architecture

Adopt **Option B: a shared Service Operations architecture with separate Kitchen
and Bar capabilities**.

The recommendation is not to merge Kitchen and Bar into one feature pack. The
recommended structure is:

```text
service_operations/
  shared mechanics and internal contracts only

kitchen/
  Kitchen Domain language
  Kitchen commands and capabilities
  Kitchen events
  Kitchen Application policy
  Kitchen delivery and workspace

bar/
  Bar Domain language
  Bar commands and capabilities
  Bar events
  Bar Application policy
  Bar delivery and workspace
```

Kitchen and Bar should be independently deployable modules inside the modular
monolith, even though they are not separate services.

## Reusable Abstractions

The following abstractions are recommended for later design. Their names are
descriptive, not accepted code names.

### Confirmed Work Source

A read-only internal contract that reconstructs destination-specific work from
the concrete Ticket Created event owned by Ordering.

It supplies:

- Ticket identity;
- originating Order and Customer Group;
- Venue;
- original Service Location;
- current Service Location;
- Responsible Service Staff;
- submission time;
- confirmed items, quantities, and notes;
- concrete destination identity.

It does not decide whether the work is Kitchen or Bar; the concrete source
mapping does.

### Event-Sourced Acknowledgement

A narrow mechanism for the invariant shared by the two approved
acknowledgement events:

- one intentional acknowledgement;
- one actor;
- one time;
- no repeated acknowledgement;
- replay without new events;
- aggregate version preservation.

Concrete aggregates provide and own the concrete event.

### Concrete Event Registration

An explicit registry connecting:

- a concrete capability;
- its concrete event type;
- serialization and restoration;
- its stream identity.

Registration must reject unknown events and must not infer event names from
strings.

### Service Work Repository Contract

A persistence-neutral contract for:

- loading one concrete Ticket;
- listing concrete work within an authorized Venue scope;
- appending concrete events with an expected version.

The contract does not expose SQL, rows, JSON, or a shared business aggregate.

### Idempotent Operational Command Receipt

A shared transactional mechanism that records a confirmed command result and
prevents a repeated request from creating another event.

The concrete result retains Kitchen or Bar terminology.

### Operational Uncertainty Result

A delivery-independent distinction among:

- confirmed success;
- confirmed business rejection;
- unknown outcome requiring current-context reload.

It must not introduce retry rules that could duplicate consequential work.

### Service Operations Infrastructure Contract Tests

Reusable tests for:

- append-only history;
- replay;
- optimistic concurrency;
- rollback;
- command receipt atomicity;
- unknown event rejection;
- isolation by Venue and concrete capability.

Concrete Kitchen and Bar tests remain required for business language, event
type, permission, and outcome.

## Explicitly Not Shared

The following must remain concrete:

- Domain Event names and meanings;
- commands;
- capabilities;
- aggregate public language;
- preparation readiness rules;
- completion rules;
- priority and delay policy;
- station and assignment behavior;
- delivery and handoff behavior;
- cancellation and correction effects;
- operational advice;
- API routes and external contracts;
- frontend workspaces and department conversation.

## Adoption Sequence

1. Treat the approved Kitchen slice as the first concrete reference.
2. Design the Bar capability from approved Bar rules before extracting code.
3. Compare the two concrete designs.
4. Extract only proven identical mechanics.
5. Keep the Kitchen behavior and current API unchanged during any later
   refactoring.
6. Run shared infrastructure contract tests and both concrete capability suites.
7. Record any future business-level unification as a Product Owner decision
   before implementation.

# Final Recommendation

Use a **shared Service Operations internal architecture with independent Kitchen
and Bar feature capabilities**.

This provides reuse where BeachOS already has identical technical and
operational guarantees, while preserving the frozen Domain’s concrete Tickets,
events, responsibilities, capabilities, and future freedom to diverge.

Do not create one generic preparation aggregate, one generic permission, or one
shared workflow state model. The architecture should share certainty,
event-stream, transaction, and reconstruction mechanics—not unapproved
hospitality rules.
