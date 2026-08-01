# BeachOS MVP Sprint Plan

## Purpose

This plan organizes the MVP into outcome-based Sprints. Sprint numbers describe
dependency order, not duration. The team must estimate each Sprint only after its
entry decisions are accepted and the work is refined.

Sprint 1 is intentionally narrow:

> An authorized Host can successfully open a Venue.

It contains no Guest Arrival, Service Location identification, Customer Group,
Order, preparation, Bill, Payment, Manager Dashboard, or general post-opening Host
Dashboard feature.

## Sprint governance

- No Sprint begins without Product Owner approval under DEC-016.
- A Sprint may implement only accepted business behavior.
- Command-gated behavior stays out until its blocking rules are approved.
- Every protected action is tested independently from Role.
- Every Sprint includes applicable rule, authorization, failure, retry, activity
  history, responsive-use, and accessibility checks.
- “Done” means a complete reviewed business outcome, not merely merged code.
- Production deployment is not implied by Sprint completion.

# Sprint 1 — Venue Opening

## Objective

Deliver the minimum complete vertical slice in which:

1. responsible people declare Operational Department readiness;
2. the Host sees the complete current readiness picture;
3. OPEN VENUE becomes eligible only when every mandatory department is READY;
4. an authorized Host intentionally opens the Venue for the Business Date;
5. the permanent Opening Report and required Activity Log are preserved;
6. success, rejection, failure, repetition, and uncertainty remain safe and clear.

## Deliverables

### Foundation required by this slice

- Approved source and module boundaries for the minimum web and server applications.
- Approved local dependency resolution and lockfiles.
- Minimum application entry points needed for this slice.
- Minimum database migration mechanism and development/test database workflow.
- Minimum signed-in Staff Member and session behavior.
- Minimum Role and explicit Capability evaluation needed for department declaration
  and Venue opening.
- Minimum test fixtures for one Organization, one Venue, one Business Date,
  mandatory Operational Departments, responsible people, one Host, and relevant
  Capabilities.

These are enabling parts of Venue Opening, not reusable-platform speculation.

### Venue Opening business behavior

- Current Venue and Business Date context.
- Mandatory Operational Department and responsible-person context.
- `Declare Department Readiness`.
- Validation of READY, NOT READY, and BLOCKED.
- Mandatory reason validation.
- `Department Readiness Declared`.
- Opening Readiness views for declarations pending, blocked, and ready to open.
- Derivation of opening eligibility.
- OPEN VENUE confirmation.
- `Open Venue for Business Date`.
- Pending outcome handling and duplicate protection.
- `Venue Opened for Business Date`.
- Permanent Opening Report.
- Required `Activity Logged`.
- Opening success feedback and minimal confirmation that Venue state is now open.
- Unauthorized, stale, degraded, rejected, and unexpected-error behavior necessary
  to protect opening.

### Verification

- Unit tests for readiness validation and eligibility.
- Authorization tests proving Role and Capability are separate.
- Integration tests for declaration history, atomic opening, Opening Report, and
  Activity Log.
- Concurrency and repeated-request test proving one daily opening.
- End-to-end tests for pending, blocked, authorized success, unauthorized attempt,
  changed readiness, retry, and uncertain outcome.
- Manual acceptance on one supported tablet or desktop context with an experienced
  Host and representative department responsible person.

## Dependencies

- Accepted DEC-007, DEC-010, DEC-014, DEC-017, DEC-018, DEC-019, DEC-038, DEC-039.
- Venue Opening Workflow.
- Domain Event engineering contract for Venue Opening.
- Functional opening wireframes.
- Acceptance Criteria E1.F1 through E1.F5 in `docs/MVP_BACKLOG.md`.
- Resolution of every “Must Decide Before Development” item in
  `docs/TECHNICAL_FOUNDATION.md`.
- Human approval of the official Venue-opening Capability name and initial
  Capability assignments.
- Approved minimum device/browser target for Sprint acceptance.

## Definition of Done

1. The current Venue and Business Date are never ambiguous.
2. Every mandatory department and responsible person is present.
3. Department declarations accept only approved values.
4. NOT READY and BLOCKED without a reason are rejected.
5. The Host cannot declare another department READY.
6. OPEN VENUE remains unavailable until every mandatory department is READY.
7. Host Role without the required Capability cannot open the Venue.
8. The authorized Host performs one intentional confirmation.
9. The opening Command is safe against repeated interaction and concurrent
   attempts.
10. Success is shown only after authoritative durable confirmation.
11. Successful opening produces one `Venue Opened for Business Date`, one official
    Opening Report, and the required Activity Log.
12. Opening creates no Customer Group, Bill, Financial Obligation, Order, transfer,
    or Payment.
13. A rejected or failed attempt leaves the Venue closed.
14. An uncertain result blocks repetition until authoritative state is recovered.
15. Refresh and missed live notice recover the current central state.
16. Tests pass in the approved continuous-integration path.
17. No secrets, production personal data, or unrelated feature work is present.
18. Product Owner and operational Host acceptance is recorded.
19. Relevant documentation and traceability are updated as part of the future
    implementation change, without rewriting historical decisions.

## Known Risks

- DEC-021 through DEC-029 remain Proposed despite the engineering foundation later
  being described as approved.
- The Venue-opening Capability has no official approved name.
- Identity, sign-in, session, account lifecycle, and Capability governance are not
  sufficiently decided.
- Business Date boundary and rollover behavior are not fully approved.
- The source and lifecycle of mandatory departments and responsible-person
  assignment require an explicit Sprint fixture or approved administration
  boundary.
- Opening Report correction and retention rules are incomplete.
- Exact safe caching and freshness rules are unresolved.
- No approved official Domain Event represents Venue-opening rejection.
- The product brief and prior screen catalogue differ on whether Opening success is
  a separate screen or transition feedback.
- The repository has no lockfiles, application entry points, migrations,
  authentication, database models, APIs, or implemented test harness.

# Sprint 2 — Host Dashboard Core

## Objective

Turn the Sprint 1 opening slice into the approved Host attention workspace without
adding later operational capabilities.

## Deliverables

- Before-opening and Venue-open Dashboard modes.
- Loading, Attention, connection-degraded, restored, unauthorized, and error states.
- Opening Readiness, Attention Queue, Department Status, and permitted Opening
  Report history.
- Valid empty states for Service Location, Customer Group, Kitchen, and Bar data not
  yet implemented.
- Live-notice reconciliation with authoritative reload.
- Tablet, desktop, and essential mobile hierarchy.

## Dependencies

- Sprint 1.
- Host Dashboard Specification and wireframes.
- Approval of Host-relevant recent activity, notification retention, safe caching,
  and opening-success screen treatment.

## Definition of Done

- Current Host attention is the first operational priority.
- Critical and Action required facts cannot be hidden by a valid empty section.
- Live notices never become a second source of truth.
- Financial, personal, waiting-list, VIP, issue-management, prediction, and
  employee-scoring information is absent.
- Supported loading, stale, error, empty, zero, pending, and success states are
  tested and distinct.
- Product Owner and Host accept the functional hierarchy.

## Known Risks

- Post-opening Attention sources remain deliberately limited.
- Cached-field classification is unresolved.
- Recent Important Activity scope is unresolved.
- Later phase sections may be mistaken for incomplete implementation rather than
  valid staged delivery.

# Sprint 3 — Guest Arrival and Service Location Identification

## Objective

Allow the Host to reach a correct, current Service Location context through manual
lookup or NFC and complete the human handoff to the Responsible Waiter.

## Deliverables

- Current Service Location Overview.
- Manual lookup by visible name or number.
- NFC identification on approved supported devices.
- Stable Service Location Digital Identity resolution.
- Available, Occupied, and Unavailable safeguards.
- Manual fallback and mismatch-safe behavior.
- Host-to-Responsible-Waiter handoff boundary.

## Dependencies

- Sprints 1 and 2.
- Approved device/browser policy.
- Approved physical marker provisioning, replacement, and support process.
- Approved mismatch escalation or an explicit manual-only boundary.
- Venue and Service Location setup data.

## Definition of Done

- NFC and manual lookup reach the same location.
- Identification reads current central state and changes no Domain Concept.
- NFC produces no official Domain Event.
- Identification grants no authority and creates no Customer Group or financial
  action.
- NFC failure never blocks manual lookup.
- Ambiguous, stale, Occupied, or Unavailable context cannot proceed as safe.
- Real-device Host acceptance passes in representative outdoor conditions.

## Known Risks

- Browser/device NFC support may constrain the selected devices.
- Physical and digital mismatch correction is not defined.
- Connectivity quality may affect the practical value of physical identification.
- Waiting and suitability remain human processes and must not become shadow
  features.

# Sprint 4 — Customer Group Opening

## Objective

Allow the Responsible Waiter to intentionally open one Active Customer Group at an
Available Service Location.

## Deliverables

- Approved Responsible Waiter assignment and acceptance.
- Open Customer Group Capability.
- `Open Customer Group`.
- `Responsible Waiter Assigned`.
- `Customer Group Opened`.
- Required Activity Log.
- One Active Customer Group per Service Location.
- Exactly one Responsible Waiter per Active Customer Group.
- Beach Sunbed immediate Financial Obligation, Bill, and Bill Line.
- Valid Active-without-Bill outcome for approved other location types.

Transfer and Customer Group completion are excluded unless their open decisions
have been accepted and separately planned.

## Dependencies

- Sprint 3.
- Approved responsibility assignment and acceptance process.
- Approved Beach Sunbed Physical Row charge inputs.
- Approved minimal Bill and Financial Obligation contract required atomically by
  Beach Sunbed opening.

## Definition of Done

- Only the eligible Responsible Waiter with Open Customer Group can open.
- Host and Cashier cannot open.
- Opening at an unavailable or occupied location is rejected.
- Opening completes atomically or changes nothing.
- All required events and history are durable and attributable.
- Beach Sunbed charge occurs exactly once.
- Other approved locations can remain Active without a Bill.
- Concurrent opening tests protect Service Location occupancy.

## Known Risks

- Responsibility handover remains unresolved.
- Completion remains unresolved.
- Beach Sunbed price and effective-date governance may not be ready.
- Customer Group opening couples operational and financial integrity at Beach
  Sunbeds.

# Sprint 5 — Waiter Ordering

## Objective

Allow authorized service staff to submit multiple reliable Order Rounds for one
Active Customer Group.

## Deliverables

- Approved Menu and Menu Item reading.
- Draft Order review.
- Durable Order submission.
- Multiple independent Order Rounds.
- Price and destination snapshots.
- Duplicate-safe retry.
- Atomic downstream preparation and Billing effects.
- Clear rejection and uncertain outcome behavior.

## Dependencies

- Sprint 4.
- Approved Menu governance and initial data.
- Minimum Kitchen, Bar, No Preparation, and Billing contracts.
- Approved Order Item correction and cancellation scope, or explicit exclusion.

## Definition of Done

- Draft creates no business effect.
- Success appears only after durable acceptance.
- Retry cannot duplicate an Order.
- Submitted Orders remain permanent separate rounds.
- Mixed routing and Bill effects are consistent.
- Rejection creates no preparation or financial effect.
- Slow connection and repeated interaction tests pass.

## Known Risks

- Submission crosses Order, preparation, and Billing boundaries.
- Correction and cancellation rules remain incomplete.
- Live operational load is not yet measured.

# Sprint 6 — Kitchen Operations

## Objective

Allow Kitchen Staff to receive and progress confirmed Kitchen Tickets.

## Deliverables

- Kitchen work queue.
- Kitchen Ticket context.
- Approved acknowledgement, readiness, and completion transitions.
- Live notices and authoritative reload.
- Kitchen-specific Capability enforcement.

## Dependencies

- Sprint 5.
- Approved preparation-state meanings, partial readiness, completion, delivery, and
  runner responsibility.

## Definition of Done

- Correct Kitchen items create one Ticket exactly once.
- Non-Kitchen items never appear as Kitchen work.
- State transitions follow the approved lifecycle.
- Missed live notices recover from central state.
- No unapproved delay threshold or performance score exists.

## Known Risks

- Preparation completion language remains unresolved.
- Outdoor waiter flow and indoor preparation flow may need different device support.
- Ticket volume and concurrency are unmeasured.

# Sprint 7 — Bar Operations

## Objective

Allow Bar Staff to receive and progress confirmed Bar Tickets.

## Deliverables

- Bar work queue.
- Bar Ticket context.
- Approved acknowledgement, readiness, and completion transitions.
- Live notices and authoritative reload.
- Bar-specific Capability enforcement.

## Dependencies

- Sprint 5.
- Approved Bar state meanings, fulfillment responsibility, and completion.

## Definition of Done

- Correct Bar items create one Ticket exactly once.
- Non-Bar items never appear as Bar work.
- Mixed Orders remain one Order Round.
- State transitions follow the approved lifecycle.
- No unapproved delay or employee judgment is introduced.

## Known Risks

- Bar may include both preparation and direct fulfillment.
- Completion and delivery ownership remain open.
- Live pressure and device placement need venue validation.

# Sprint 8 — Billing

## Objective

Maintain the Customer Group’s exact, explainable Bill across all approved Financial
Obligations.

## Deliverables

- Bill creation on first Financial Obligation.
- Bill Lines for approved Order Items and Beach Sunbed charges.
- Exact totals and Balance.
- Price and charge history.
- Approved correction or reversal only if its rules are accepted.
- Approved Bill closure only if its rules are accepted.

## Dependencies

- Sprints 4 and 5.
- Approved currency, tax, discount, charge, correction, closing, and fiscal rules.
- Legal/accounting review where necessary.

## Definition of Done

- Active Customer Group without Bill remains valid.
- One first obligation creates one Bill.
- All lines have an explainable source.
- Historical values never change with current price updates.
- Financial calculations, concurrency, and history tests pass.
- Unapproved reversal, closure, or reopening is absent.

## Known Risks

- Fiscal requirements may materially change scope.
- Transfer charging and Bill closing remain unresolved.
- Financial defects have high operational and legal impact.

# Sprint 9 — Payments

## Objective

Allow authorized staff to record confirmed Payments and close eligible Bills
without duplication or false confirmation.

## Deliverables

- Approved Payment Methods.
- Payment attempt versus confirmed Payment handling.
- `Payment Recorded` and `Payment Rejected`.
- Exact Balance updates.
- `Bill Fully Paid`.
- Approved `Bill Closed`.
- Reversal or refund only if separately approved.

## Dependencies

- Sprint 8.
- Payment allocation, split, partial, overpayment, change, tip, reversal, refund,
  terminal, receipt, and closing decisions.

## Definition of Done

- Only confirmed Payment reduces Balance.
- Repeated interaction records value at most once.
- Every sensitive outcome has required Activity Log.
- Zero Balance does not silently complete Customer Group service.
- Closing follows explicit Capability and approved rules.
- Financial reconciliation and failure tests pass.

## Known Risks

- External terminal and fiscal integrations may be required.
- Payment uncertainty can create duplicate receipt risk.
- Closing and Customer Group completion relationship is unresolved.

# Sprint 10 — Manager Dashboard and MVP Operational Review

## Objective

Provide approved management oversight and validate the connected MVP across all
implemented Roles.

## Deliverables

- Approved current operational overview.
- Opening Report review.
- Approved limited reporting.
- Permitted Activity Log and Audit Trail views.
- Cross-role end-to-end validation.
- Device, concurrency, connectivity, security, recovery, and venue-pilot readiness
  review.

## Dependencies

- Sprints 1 through 9.
- Approved Manager Capability catalogue, measures, privacy, retention, and reporting
  definitions.
- Approved deployment, monitoring, backup, restoration, and support foundation.

## Definition of Done

- Every measure has an approved definition and source.
- Manager Role alone grants no action.
- Sensitive access is explicit and audited.
- No staff surveillance, scoring, or unapproved AI decision is present.
- Complete workflows pass on approved devices under representative concurrency and
  connection conditions.
- Backup restoration and incident fallback are tested before pilot approval.
- Product Owner approves the MVP release candidate.

## Known Risks

- Reporting requirements may expand without clear operational value.
- Privacy and retention obligations require professional review.
- Pilot readiness depends on real Venue connectivity, staff availability, training,
  and support ownership.

## Scope-change rule

If a Sprint reveals a new business rule:

1. stop the affected implementation;
2. document the question;
3. obtain Product Owner approval;
4. record the Decision before implementation whenever possible;
5. update the affected backlog and acceptance criteria;
6. resume only after the new authority is clear.
