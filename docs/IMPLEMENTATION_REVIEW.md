# BeachOS Implementation Readiness Review

## Executive conclusion

**Sprint 1 is not ready to begin coding.**

The Sprint 1 business outcome is ready:

> An authorized Host can successfully open a Venue after every mandatory
> Operational Department is READY.

The repository defines that outcome unusually well. Its business rules, Role
boundaries, Commands, Domain Events, operational workflow, functional states,
failure behavior, and acceptance expectations are sufficient for engineering
refinement.

The technical execution foundation is not yet approved or complete. Starting code
now would force developers to decide identity, sessions, Capability governance,
Business Date handling, persistence, Command semantics, concurrency, live updates,
test strategy, and dependency status without authority.

The correct next step is a short human technical-decision gate, not application
implementation.

# Is Sprint 1 ready?

## Product and domain readiness

**Yes, with two narrow Product Owner decisions still required for implementation
language and governance.**

The approved repository clearly establishes:

- a Venue cannot open before every mandatory Operational Department is READY;
- department responsible people declare their own readiness;
- READY, NOT READY, and BLOCKED are the only statuses;
- NOT READY and BLOCKED require a reason;
- the Host coordinates and does not verify every department;
- Host Role alone grants no authority;
- OPEN VENUE requires an explicit Capability;
- opening is intentional and never time-triggered;
- successful opening creates the official operational start, Opening Report,
  `Venue Opened for Business Date`, and required Activity Log;
- opening creates no Customer Group, Bill, Financial Obligation, Order, transfer,
  or Payment;
- an uncertain outcome cannot be shown as success or blindly repeated.

The remaining narrow Product Owner decisions that directly affect Sprint 1 are:

1. the official name and governance of the Venue-opening Capability;
2. the implementable Business Date rule, including its Venue boundary.

Opening Report history, responsible-person configuration, and declaration authority
also need an explicit approved Sprint 1 interpretation if not already covered by
the two decisions above.

## Interaction readiness

**Mostly yes.**

The repository provides:

- pending declarations;
- blocked departments;
- ready-to-open state;
- intentional confirmation;
- opening in progress;
- success feedback;
- degraded connection;
- restored reconciliation;
- unauthorized access;
- unexpected error;
- Back, Cancel, Retry, refresh, session-expiration, and Capability-change behavior.

One screen-catalogue tension remains: the Host Dashboard Specification treats
Opening succeeded as a screen, while the wireframe brief requires Opening
confirmation and expresses success during the transition to Venue Open. Sprint 1
can preserve the accepted business outcome either way, but the Product Owner should
approve the final interaction inventory before implementation.

## Engineering readiness

**No.**

The repository is a prepared scaffold, not an executable application:

- no dependencies are installed;
- no lockfiles exist;
- DEC-021 through DEC-029 remain Proposed;
- no application entry points exist;
- no authentication or session handling exists;
- no database tables or migrations exist;
- no API or Command transport exists;
- no live-update implementation exists;
- no application tests exist;
- frontend and backend CI jobs remain gated.

# What still blocks implementation?

## Blocking governance decisions

1. Accept, reject, or supersede DEC-021 through DEC-029.
2. Authorize dependency installation and lockfile creation.
3. Approve the official Venue-opening Capability name.
4. Approve Capability grant, revocation, and Venue-scope governance.
5. Approve department declaration authority and responsible-person setup.
6. Approve the Business Date boundary.
7. Approve Opening Report history, access, and Sprint 1 correction boundary.
8. Confirm the final opening-confirmation and opening-success interaction treatment.

## Blocking engineering decisions

1. Source and module layout.
2. Individual identity and sign-in method.
3. Session security, expiration, revocation, and shared-device behavior.
4. Persistence and migration mechanism.
5. Test database isolation and deterministic fixture setup.
6. Command contracts for readiness declaration and Venue opening.
7. Atomicity, uniqueness, repeated-request, and concurrency strategy.
8. Time source, timezone, and timestamp handling.
9. Web-to-server contract style and error categories.
10. Live-notice mechanism and authoritative recovery.
11. Freshness and degraded-state rules.
12. Unit, integration, browser end-to-end, and concurrency test tooling.
13. Required continuous-integration checks.
14. Reproducible local development workflow.
15. Minimum observability and uncertain-outcome ownership.
16. Secrets and synthetic non-production data handling.

Each item is described in `docs/TECHNICAL_FOUNDATION.md`.

## Blocking implementation inputs

- one approved Organization and Venue fixture;
- one Business Date scenario;
- the mandatory Operational Department set;
- one responsible person per mandatory department;
- one Host with and one Host without the required Capability;
- approved test cases for READY, NOT READY, BLOCKED, changed declaration, concurrent
  opening, duplicate submission, session expiration, and connection loss;
- a Product Owner and operational Host named for acceptance.

# What repository strengths reduce implementation risk?

## Clear authority model

The repository distinguishes:

- business responsibility from authority;
- Role from Capability;
- Command from Domain Event;
- Domain Event from Activity Log;
- Activity Log from Audit Trail;
- central truth from live notice;
- operational workflow from interface behavior.

These separations prevent common security and architecture errors.

## Strong Venue Opening invariant

DEC-039 and the Venue Opening Workflow give Sprint 1 one precise gate:

> Every mandatory Operational Department is READY.

There is no approved override, automatic opening, time-based opening, or Host
verification shortcut. This makes rule implementation and testing objective.

## Defined success and non-success behavior

The repository does not stop at the happy path. It defines:

- missing declarations;
- NOT READY;
- BLOCKED;
- changed readiness;
- unauthorized Host;
- pending outcome;
- duplicate interaction;
- degraded connection;
- restored reconciliation;
- unexpected error;
- no false success.

This materially reduces ambiguity in acceptance testing.

## Event and history clarity

Sprint 1 has a small, explicit event set:

- `Department Readiness Declared`;
- `Venue Opened for Business Date`;
- `Activity Logged`.

The Opening Report becomes official with the opening event rather than through a
separate invented event. The repository also states which interaction states are
not Domain Events.

## Functional design depth

The Host Dashboard Specification and wireframes define:

- user goals;
- visible and secondary information;
- available and disabled actions;
- empty and error states;
- navigation;
- permissions;
- user mistakes;
- system feedback;
- 50 broader Host Dashboard Acceptance Criteria;
- explicit transition guards.

Engineering should not need to infer business behavior from a visual mockup.

## Deliberate scope boundaries

The repository repeatedly excludes unapproved functionality. This protects Sprint 1
from becoming a hidden “platform foundation” or full Dashboard build.

## Existing repository governance

The project already includes:

- contribution and security policies;
- Decision Log discipline;
- proposed continuous integration;
- environment separation;
- dependency review expectations;
- test placement guidance;
- human approval requirements;
- AI accountability rules.

## Safety principles

The accepted foundation prioritizes:

- no false confirmation;
- no silent operational or financial loss;
- server-side authorization;
- permanent sensitive history;
- exact financial data;
- human control;
- small milestones.

These provide useful review criteria before code exists.

# What should absolutely not be implemented yet?

## Outside Sprint 1

Do not implement:

- the full post-opening Host Dashboard;
- Guest Arrival software beyond the minimum fact that arrivals become allowed after
  confirmed opening;
- Service Location search, NFC, or manual identification;
- Guest Token;
- digital waiting list;
- reservations;
- Guest Profiles or VIP recognition;
- Customer Group opening;
- Responsible Waiter assignment or handover;
- Customer Group transfer, completion, cancellation, reopening, merge, or split;
- Menus, Draft Orders, Orders, or Order Items;
- Kitchen or Bar Tickets;
- Financial Obligations, Bills, Bill Lines, charges, discounts, tax, or corrections;
- Payments, Payment Methods, refunds, reversals, or Bill closing;
- Venue Closing Workflow;
- Manager Dashboard or reporting;
- Zone or Zone Template management;
- complaint, incident, equipment, weather, or maintenance modules;
- AI recommendations, predictions, decisions, staff scoring, or emotional inference.

## Unapproved Sprint 1 extensions

Do not implement:

- a broad account-administration product;
- Role-based authorization that bypasses Capability;
- automatic Capability assignment from Role;
- a forced readiness override;
- a Manager bypass for DEC-039;
- automatic Venue opening;
- a separate `Venue Opening Started` Domain Event;
- a separate `Opening Report Created` Domain Event;
- an invented `Venue Opening Rejected` Domain Event;
- Opening Report correction without approved rules;
- a generic issue or escalation ticket;
- planned opening scheduling without approved source and governance;
- offline Venue opening;
- cached readiness as opening authority;
- a second source of truth in the live-update mechanism;
- a broad reusable framework not required by the vertical slice;
- production deployment before hosting, security, backup, recovery, monitoring,
  support, and venue-connectivity decisions are approved.

## Premature technical additions

Do not add:

- technologies not named or approved by the repository;
- a queue, cache, separate service, native application, or offline synchronization
  architecture without an Accepted Decision;
- speculative shared packages;
- application dependencies without review and authorization;
- database abstractions or generic event infrastructure not required by Sprint 1;
- production secrets or real staff/customer data;
- implementation derived from a Proposed Decision as if it were Accepted.

# Recommended readiness sequence

## Gate 1 — Product Owner decisions

Approve:

1. Venue-opening Capability name and governance.
2. Business Date rule.
3. responsible-person and declaration authority.
4. Opening Report history and access boundary.
5. final confirmation/success interaction treatment.

Record every material decision before implementation.

## Gate 2 — Engineering decisions

Resolve the Must Decide Before Development list in
`docs/TECHNICAL_FOUNDATION.md`, beginning with DEC-021 through DEC-029, identity,
session, persistence, Command contracts, concurrency, test strategy, and CI.

## Gate 3 — Sprint refinement

- Refine only Epic E1 stories.
- Name owners.
- Define deterministic fixtures.
- Map every story to automated and human acceptance checks.
- Confirm explicit exclusions.
- Estimate only after gates 1 and 2.

## Gate 4 — Human authorization

The Product Owner explicitly authorizes Sprint 1 implementation under DEC-016.

# Final recommendation

**Do not start application coding yet.**

The business slice is ready for implementation planning, but the technical
foundation and a small number of Product Owner decisions still block safe
implementation.

Once the decision gates are complete, Sprint 1 is a strong first vertical slice:
small enough to deliver and review, important enough to validate the architecture,
and isolated from the unresolved Customer Group, preparation, Billing, and Payment
work that follows.
