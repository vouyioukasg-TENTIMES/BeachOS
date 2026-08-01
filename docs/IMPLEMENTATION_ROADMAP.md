# BeachOS Implementation Roadmap

## Purpose

This roadmap turns the approved Product Foundation into an implementation sequence
for a professional delivery team. It describes outcomes and gates, not dates,
estimates, application structure, or new business rules.

The sequence follows the operational dependency chain:

> Open the Venue → understand the live operation → receive guests → open Customer
> Groups → take Orders → prepare items → manage Bills → record Payments → provide
> management oversight.

Each phase is a reviewable vertical increment. A phase is complete only when its
accepted business behavior works across the required user journey, server-enforced
rules, durable history, failure handling, and tests. Later phases must not weaken
earlier invariants.

## Delivery rules

- Accepted Decisions, Domain Model, Domain Events, Product Requirements, Framework
  workflows, and approved functional specifications remain authoritative.
- A Role never directly authorizes an action. Protected actions require explicit
  Capabilities and all applicable business rules.
- The central system remains the source of operational and financial truth.
- A Command is not successful until its approved business outcome is confirmed.
- Sensitive actions create the required Activity Logs.
- A Product Owner decision that is still open remains a delivery blocker for the
  affected behavior.
- Every phase requires human acceptance before the next major implementation phase
  begins, in accordance with DEC-016.
- Phase completion does not authorize production release. Deployment, security,
  recovery, legal, and operational-readiness gates remain separate.

# Phase 1 — Venue Opening

## Objective

Deliver the smallest complete workflow in which an authorized Host can open one
Venue for one Business Date after every mandatory Operational Department has
declared READY.

## Business capabilities

- Establish the signed-in Staff Member, current Venue, Business Date, Host
  responsibility, and current Capabilities.
- Present every mandatory Operational Department and its responsible person.
- Allow each department’s responsible person to intentionally declare READY, NOT
  READY, or BLOCKED.
- Require a reason for NOT READY and BLOCKED.
- Preserve current and historically relevant declarations for the Opening Report.
- Show missing, NOT READY, and BLOCKED conditions to the Host.
- Derive opening eligibility only when every mandatory department is READY.
- Allow OPEN VENUE only to a Host holding the required Venue-opening Capability.
- Require intentional confirmation and prevent unsafe repeated execution.
- Produce `Department Readiness Declared`.
- On successful opening, produce `Venue Opened for Business Date` and the required
  `Activity Logged`.
- Make the permanent Opening Report official as part of the successful opening.
- Confirm failure, rejection, pending, and uncertain outcomes without false success.

Sprint 1 does not include the full post-opening Host Dashboard. It needs only the
minimum interaction required to complete and verify Venue Opening.

## Dependencies

- DEC-007, DEC-010, DEC-014, DEC-017, DEC-018, DEC-019, DEC-038, and DEC-039.
- Venue, Business Date, Operational Department, Department Readiness, Host, Staff
  Member, Role, Capability, Opening Report, and Activity Log definitions.
- `Declare Department Readiness` and `Open Venue for Business Date` contracts in
  `docs/DOMAIN_EVENTS.md`.
- Venue Opening Workflow.
- The relevant Loading, pending, blocked, ready, confirmation, in-progress,
  unauthorized, degraded, and error wireframe behavior.
- Human approval of the Sprint 1 blockers listed in
  `docs/TECHNICAL_FOUNDATION.md`.
- Approved minimum test identities and one deterministic Venue-opening fixture.

## Completion criteria

- Every mandatory department has exactly one current declaration for the Business
  Date.
- Invalid values and missing required reasons are rejected.
- The Host cannot declare another department READY.
- OPEN VENUE remains unavailable while any mandatory declaration is missing, NOT
  READY, or BLOCKED.
- Host Role alone cannot open the Venue.
- An authorized Host can intentionally open only after all mandatory departments
  are READY.
- A repeated or uncertain request cannot create a second opening.
- Successful opening has one official time, one Host, one Opening Report, the
  opening readiness snapshot, and required Activity Log.
- Opening creates no Customer Group, Bill, Financial Obligation, Order, transfer,
  or Payment.
- Before opening, new Customer Groups and Orders remain forbidden at the business
  boundary even though those features are not yet implemented.
- Current state can be retrieved after refresh or missed live notice.
- Automated tests cover the rules, success path, rejection paths, concurrency or
  repeated submission, authorization, and durable history.
- The Product Owner and an experienced Host accept the workflow.

# Phase 2 — Host Dashboard

## Objective

Extend the Venue Opening slice into the approved Host operational workspace that
answers: “What requires the Host’s attention right now?”

## Business capabilities

- Support before-opening, Venue-open, and degraded-connectivity modes.
- Present Opening Readiness, Attention Queue, Service Location Overview, Live
  Operation Summary, Department Status, and Recent Important Activity within their
  approved boundaries.
- Present Critical, Action required, and Awareness only facts.
- Show current Service Location availability and occupancy.
- Show limited permitted Customer Group and Responsible Waiter context.
- Show factual Bar and Kitchen preparation pressure only after those phases supply
  accepted data.
- Preserve a visible manual fallback and honest freshness state.
- Provide live notices while retrieving authoritative state independently.
- Enforce minimum necessary Host information and privacy restrictions.

Sections depending on later phases may initially have explicit valid empty or
not-yet-available states. They must not be populated with invented data.

## Dependencies

- Phase 1.
- `docs/ui/HOST_DASHBOARD_SPEC.md`.
- Host Dashboard functional wireframes and user flow.
- Product Owner decisions governing Host-visible Customer Group details, Recent
  Important Activity, notification retention, Ticket visibility, safe caching, and
  the Venue-opening Capability name.
- Service Location state from Phase 3 and preparation facts from Phases 6 and 7 for
  their eventual live summaries.

## Completion criteria

- The Dashboard satisfies AC-01 through AC-50 for the functionality available by
  that release.
- Missing, unavailable, stale, empty, zero, pending, rejected, failed, and
  successful states remain distinct.
- No unapproved financial, personal, waiting-list, VIP, complaint, incident,
  weather, predictive, scoring, Venue-closing, or AI decision behavior appears.
- Live notices cannot override central authoritative state.
- Critical information remains available on supported mobile, tablet, and desktop
  layouts.
- A Host usability review confirms that current attention is discoverable without
  general reporting or administration.

# Phase 3 — Guest Arrival

## Objective

Support the Host’s approved operational journey from a guest entering the open Venue
through correct Service Location identification and a clear handoff to the
Responsible Waiter.

## Business capabilities

- Confirm that the Venue is open before normal Guest Arrival proceeds.
- Review current Service Location availability by visible name or number.
- Find suitable current options without automating human suitability decisions.
- Identify the same enduring Service Location by NFC or manual lookup.
- Retrieve current state from the central system.
- Preserve the boundary between seating, identification, responsibility, and
  Customer Group opening.
- Provide manual continuity when NFC is missing, damaged, unsupported, or
  unavailable.
- Prevent ambiguous, occupied, unavailable, or stale location context from being
  treated as safe.

Greeting, needs assessment, waiting, escort, and introduction remain human
operational work. A digital waiting list is not part of this phase.

## Dependencies

- Phases 1 and 2.
- DEC-011, DEC-030, DEC-031, DEC-035, DEC-038, and DEC-039.
- Guest Arrival Workflow.
- Stable Service Location Digital Identity.
- Approved device and browser support, NFC behavior, manual fallback, and physical
  tag provisioning process.
- Product Owner decision for physical/digital mismatch handling if a corrective
  workflow is required.

## Completion criteria

- NFC and manual lookup resolve to the same Service Location.
- One active identification marker cannot resolve to more than one location.
- Identification grants no Capability and performs no operational or financial
  action.
- Occupied and Unavailable locations are never shown as safely Available.
- NFC failure never blocks manual identification.
- A wrong, ambiguous, stale, or unavailable location does not proceed as confirmed.
- The Host receives only approved information.
- Arrival can end with a human Responsible Waiter introduction without the Host
  opening a Customer Group.
- Staff acceptance testing covers sunlight, touch use, supported devices, failure,
  and manual fallback.

# Phase 4 — Customer Groups

## Objective

Allow the Responsible Waiter to intentionally begin and maintain one Active
Customer Group at an available Service Location while preserving its identity and
history.

## Business capabilities

- Assign exactly one eligible Responsible Waiter through an approved process.
- Allow only that Responsible Waiter with Open Customer Group to open the group.
- Enforce one Active Customer Group per Service Location.
- Make Customer Group the primary operational entity.
- Preserve current Service Location, Responsible Waiter, Orders, optional Bill,
  Payments through the Bill, and History.
- Allow a group to exist without a Bill where no Financial Obligation exists.
- Apply the immediate approved Beach Sunbed Financial Obligation atomically at
  opening.
- Support complete transfer only after open transfer and charging rules are
  approved.
- Support transition from Active to Completed only after exact completion rules are
  approved.

## Dependencies

- Phase 3.
- DEC-009 through DEC-012 and DEC-030 through DEC-035 and DEC-038.
- Customer Group Lifecycle.
- `Assign Responsible Waiter` and `Open Customer Group` contracts.
- Product Owner decisions for responsibility assignment and handover, completion,
  no-Bill completion, transfer combinations, Physical Row charge changes, and any
  cancellation exception.

## Completion criteria

- Only the eligible Responsible Waiter can open the group.
- Host seating and identification cannot open it.
- Opening either completes atomically or changes nothing.
- Successful opening produces `Responsible Waiter Assigned`, `Customer Group
  Opened`, and `Activity Logged`.
- Beach Sunbed opening also creates the approved Financial Obligation, Bill, and
  Bill Line exactly once.
- Other location types may remain Active without a Bill.
- Transfers, if included after approval, preserve one Customer Group identity and
  complete atomically.
- No unapproved Cancelled, Reopened, split, or merged state exists.
- Invariants hold under concurrent attempts and repeated requests.

# Phase 5 — Waiter Operations

## Objective

Allow the Responsible Waiter and other explicitly authorized Staff Members to
coordinate active service and submit multiple safe Order Rounds for one Customer
Group.

## Business capabilities

- Review the waiter’s current Customer Group responsibilities.
- Build and review a Draft Order without treating it as submitted.
- Submit one Order as one confirmed Order Round.
- Allow multiple Orders under one Active Customer Group.
- Preserve submitted Order Items, prices, instructions, and preparation
  destinations.
- Prevent false success, silent loss, and accidental duplicate submission.
- Apply approved corrections or cancellations only when their detailed rules are
  accepted.
- Preserve responsibility changes and Shift handover only under approved rules.

## Dependencies

- Phase 4.
- DEC-008, DEC-009, DEC-013, DEC-014, DEC-017, DEC-031, DEC-036, and DEC-038.
- Approved Menus, Menu Categories, Menu Items, prices, availability, and
  destinations.
- Approved Order correction and cancellation authority and consequences.
- Preparation and Billing contracts required for atomic submission.

## Completion criteria

- A Draft Order creates no preparation or financial fact.
- Submission is allowed only for an Active Customer Group under approved
  Capability rules.
- Success is shown only after durable acceptance.
- Repeat attempts produce at most one accepted Order.
- Every later Order remains a separate round; no prior Order is overwritten.
- `Order Submitted` and required downstream events are consistent as one business
  outcome.
- Rejection creates no Bill Line or Preparation Ticket.
- Tests cover mixed destinations, changing menu data, poor connection, retry, and
  concurrent service.

# Phase 6 — Kitchen

## Objective

Provide the Kitchen with confirmed preparation work created from Kitchen-destination
Order Items and allow it to progress through approved states.

## Business capabilities

- Create one Kitchen Ticket from the Kitchen items of a submitted Order.
- Preserve Customer Group, Service Location, Order, and Order Item context needed
  for preparation.
- Present confirmed work without Bar or No Preparation items.
- Support accepted Kitchen acknowledgement, readiness, and completion meanings.
- Provide relevant live notices without making them authoritative.

## Dependencies

- Phase 5.
- DEC-008, DEC-013, DEC-014, DEC-017, and DEC-018.
- Product Owner approval of exact Kitchen Ticket readiness, partial readiness,
  completion, delivery, and runner responsibility.
- Approved Kitchen Capabilities and information boundaries.

## Completion criteria

- Every applicable submitted Order produces the correct Kitchen Ticket exactly
  once.
- Orders without Kitchen items produce no Kitchen Ticket.
- Ticket progression follows only approved transitions.
- `Kitchen Ticket Created`, `Kitchen Ticket Acknowledged`, `Kitchen Ticket Ready`,
  and `Kitchen Ticket Completed` are produced only when their meanings are
  satisfied.
- A failed or rejected Order creates no Kitchen work.
- Current work can be reloaded authoritatively after missed live notices.

# Phase 7 — Bar

## Objective

Provide the Bar with confirmed preparation or fulfillment work created from
Bar-destination Order Items and allow it to progress through approved states.

## Business capabilities

- Create one Bar Ticket from the Bar items of a submitted Order.
- Preserve the operational context required for fulfillment.
- Present confirmed work without Kitchen or No Preparation items.
- Support accepted Bar acknowledgement, readiness, and completion meanings.
- Provide relevant live notices while retaining central authority.

## Dependencies

- Phase 5.
- DEC-008, DEC-013, DEC-014, DEC-017, and DEC-018.
- Product Owner approval of exact Bar Ticket readiness, partial readiness,
  completion, delivery, and runner responsibility.
- Approved Bar Capabilities and information boundaries.

## Completion criteria

- Every applicable submitted Order produces the correct Bar Ticket exactly once.
- Orders without Bar items produce no Bar Ticket.
- Ticket progression follows only approved transitions.
- `Bar Ticket Created`, `Bar Ticket Acknowledged`, `Bar Ticket Ready`, and `Bar
  Ticket Completed` are produced only when their meanings are satisfied.
- Mixed Orders remain one Order Round while routing to separate destinations.
- Current work recovers correctly after reconnect or refresh.

# Phase 8 — Billing

## Objective

Maintain one exact, explainable Bill for each Customer Group that has at least one
approved Financial Obligation.

## Business capabilities

- Allow an Active Customer Group to exist without a Bill.
- Create a Bill only with the first approved Financial Obligation.
- Add explainable Bill Lines from approved Order Items, Beach Sunbed charges, and
  later approved adjustments.
- Aggregate approved obligations from every Order Round.
- Preserve price and charge history.
- Calculate exact total and Balance.
- Reverse or correct a Bill Line only after the relevant rules are approved.
- Close a Bill only after exact closing rules and authority are approved.

## Dependencies

- Phases 4 and 5.
- DEC-009, DEC-010, DEC-033, DEC-034, DEC-036, and DEC-038.
- Approved currency, tax, discount, Physical Row charging, correction, and closing
  rules.
- Legal and fiscal review for the relevant Venue context.

## Completion criteria

- Customer Group opening alone creates no Bill except for the approved Beach Sunbed
  obligation.
- First obligation creates one Bill and one explainable line atomically.
- Later Order Rounds aggregate without overwriting earlier financial facts.
- Historical amounts remain unchanged after Menu or Row price changes.
- Money is exact and no financial history is silently rewritten.
- Closing and correction behavior is absent until approved; once approved, every
  sensitive action is authorized and auditable.
- Financial calculations and concurrency paths have comprehensive automated tests.

# Phase 9 — Payments

## Objective

Allow authorized Staff Members to record confirmed value received against a Bill
and close the Bill only under approved conditions.

## Business capabilities

- Present approved Payment Methods.
- Distinguish a Payment attempt from a confirmed Payment.
- Record a confirmed Payment exactly once.
- Reduce Balance only after `Payment Recorded`.
- Produce `Payment Rejected` without reducing Balance.
- Support partial, split, overpayment, change, tips, reversals, and refunds only
  after those rules are approved.
- Produce `Bill Fully Paid` at zero Balance without assuming Customer Group
  completion.
- Close the Bill only through approved authority and conditions.

## Dependencies

- Phase 8.
- DEC-009, DEC-010, DEC-014, DEC-038, and applicable Product Requirements.
- Approved Payment Methods, allocation, duplicate protection, reversal, refund,
  closing, receipt, fiscal, and terminal-integration rules.
- Approved Record Payments and Close Bill Capabilities.

## Completion criteria

- Only confirmed Payment reduces Balance.
- A repeated attempt cannot record value twice.
- Rejection and uncertainty never appear as Payment success.
- All accepted allocations balance exactly.
- Every Payment, reversal, and Bill closure has required history and Activity Log.
- Zero Balance does not automatically complete the Customer Group.
- No Bill reopening exists without a future accepted exception.

# Phase 10 — Manager Dashboard

## Objective

Provide authorized Managers with operational oversight and approved controls without
turning accountability into surveillance or bypassing Role and Capability rules.

## Business capabilities

- Review current Venue, Service Location, Customer Group, preparation, Bill, and
  Payment conditions within approved responsibility.
- Review Opening Reports and approved operational history.
- Understand exceptions, transfers, cancellations, corrections, and responsibility
  changes only where their workflows are approved.
- Access approved daily and operational reporting.
- Perform only explicitly authorized management actions.
- Preserve coaching-before-judging and minimum-necessary-information principles.

## Dependencies

- Phases 1 through 9.
- DEC-010, DEC-014, DEC-020, DEC-031, and DEC-038.
- Approved Manager responsibilities, Capabilities, reporting definitions, privacy
  boundaries, retention, and correction workflows.
- Accepted success metrics and operational definitions.

## Completion criteria

- Every displayed measure has one approved business definition and traceable source.
- Manager Role alone grants no protected action.
- Sensitive information and actions are limited by explicit Capability and Venue
  context.
- Activity Logs support explanation, not employee scoring or blame.
- Reports do not silently disagree with operational and financial source facts.
- No unapproved AI decision, prediction, employee ranking, or cross-Venue access is
  introduced.
- Product Owner and representative Manager acceptance is complete.

## Roadmap review gates

Before starting each phase, the team must confirm:

1. Related Product Owner decisions are Accepted.
2. Commands and Domain Events are current rather than Command gated for the intended
   scope.
3. Functional interaction behavior is approved.
4. Required technical decisions are Accepted.
5. Dependencies and test data are available.
6. Security, privacy, reliability, and audit effects are understood.
7. The preceding phase meets its completion criteria.
8. An authorized human approves the phase under DEC-016.
