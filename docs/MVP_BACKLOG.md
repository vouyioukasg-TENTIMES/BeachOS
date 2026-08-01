# BeachOS MVP Backlog

## Purpose

This backlog decomposes the approved MVP into Epics, Features, User Stories, and
Acceptance Criteria. It is ordered by business dependency rather than estimated
delivery date.

Backlog items do not approve an unresolved rule. An item marked **Blocked** cannot
enter implementation until its referenced Product Owner or technical decision is
Accepted. Acceptance Criteria supplement, but never replace, the authoritative
Decision, Workflow, Domain Model, or Domain Event definition.

## Status terms

- **Ready for refinement** — approved business behavior exists; technical or
  delivery detail may still need team refinement.
- **Blocked** — a named decision or contract is still missing.
- **Future approved** — accepted as a future concept but outside the first MVP
  implementation.

# Epic E1 — Daily Venue Opening

## Epic outcome

An authorized Host opens the Venue for the Business Date only after every mandatory
Operational Department is READY.

## Authority

- DEC-007, DEC-010, DEC-014, DEC-017, DEC-018, DEC-038, DEC-039.
- Venue Opening Workflow.
- `Declare Department Readiness`.
- `Department Readiness Declared`.
- `Open Venue for Business Date`.
- `Venue Opened for Business Date`.
- `Activity Logged`.

## Feature E1.F1 — Opening context

### User Story E1.F1.US1 — Establish current opening scope

**As a Host, I want to see the current Venue, Business Date, mandatory departments,
and responsible people so that I coordinate the correct opening.**

#### Acceptance Criteria

1. The current Venue and Business Date are explicit.
2. Every mandatory Operational Department is present.
3. Every mandatory department has one responsible person.
4. Optional departments do not block opening unless already made mandatory through
   an approved process.
5. Missing configuration is shown as a blocking setup error, not an empty healthy
   state.
6. Data from another Venue or Business Date is never mixed into the opening.

**Status:** Ready for refinement, subject to technical foundation gates.

## Feature E1.F2 — Department readiness declarations

### User Story E1.F2.US1 — Declare readiness

**As an Operational Department responsible person, I want to declare my
department’s current readiness so that the Host can coordinate from confirmed
facts.**

#### Acceptance Criteria

1. Allowed values are exactly READY, NOT READY, and BLOCKED.
2. NOT READY and BLOCKED require a reason.
3. READY does not accept a hidden known blocker.
4. The actor, department, Venue, Business Date, status, reason where required,
   comment where provided, and confirmed time are attributable.
5. Success produces `Department Readiness Declared`.
6. A rejected declaration does not change the current declaration.
7. A later declaration preserves historically relevant opening context.

### User Story E1.F2.US2 — Protect department ownership

**As a department responsible person, I want my declaration to remain my
responsibility so that the Host coordinates rather than verifies my department.**

#### Acceptance Criteria

1. The Host cannot declare READY on another department’s behalf.
2. Role or interface visibility alone does not authorize declaration.
3. A declaration from the wrong person, Venue, department, or Business Date is
   rejected.
4. Rejection never appears as a confirmed declaration.

**Status:** Blocked by identity, session, and Capability-governance technical
decisions.

## Feature E1.F3 — Opening Readiness

### User Story E1.F3.US1 — See unresolved readiness

**As a Host, I want missing, NOT READY, and BLOCKED declarations prioritized so that
I know what requires follow-up.**

#### Acceptance Criteria

1. Missing, READY, NOT READY, and BLOCKED are distinct in words.
2. NOT READY and BLOCKED show the approved reason.
3. The responsible person is clear.
4. BLOCKED is Critical; missing and NOT READY are Action required.
5. Viewing or acknowledging an item does not resolve it.
6. A blocker clears only after a later valid declaration changes the source fact.
7. The interface uses no employee scoring or blame language.

### User Story E1.F3.US2 — Derive eligibility

**As a Host, I want the system to state whether the Venue is eligible to open so
that I do not rely on memory.**

#### Acceptance Criteria

1. Eligibility is true only when every mandatory department is READY.
2. Missing, NOT READY, or BLOCKED makes eligibility false.
3. Eligibility does not mean that the Venue is already open.
4. The passage of time never opens the Venue.
5. Stale or unavailable state never authorizes opening.

**Status:** Ready for refinement, subject to technical foundation gates.

## Feature E1.F4 — Authorized Venue opening

### User Story E1.F4.US1 — Confirm OPEN VENUE

**As an authorized Host, I want to review and intentionally confirm OPEN VENUE so
that the Business Date begins only by deliberate action.**

#### Acceptance Criteria

1. The confirmation identifies Venue, Business Date, Host, and all-ready state.
2. Host responsibility and the required Venue-opening Capability are both required.
3. The Host Role alone is insufficient.
4. Business rules are rechecked when the Command is accepted.
5. Cancel before submission creates no business fact.
6. The required Capability’s official name is not invented in implementation.
7. Selecting confirmation proceeds to a pending state without claiming success.

### User Story E1.F4.US2 — Prevent duplicate opening

**As a Host, I want uncertain or repeated interaction handled safely so that one
Business Date is not opened twice.**

#### Acceptance Criteria

1. OPEN VENUE is disabled while the outcome is pending.
2. A repeated request cannot create a second daily opening.
3. Retry retrieves authoritative outcome rather than resubmitting the Command.
4. A lost response is neither success nor failure until reconciled.
5. Refresh and session recovery preserve the pending outcome identity.

### User Story E1.F4.US3 — Confirm successful opening

**As a Host, I want authoritative confirmation of opening so that I know guest
service may begin.**

#### Acceptance Criteria

1. Success produces `Venue Opened for Business Date`.
2. Success produces the required `Activity Logged`.
3. The permanent Opening Report becomes official as part of the same successful
   outcome.
4. Official opening time, Business Date, Host, and department readiness snapshot
   are available.
5. Guest arrivals, new Customer Groups, and Orders become allowed only under their
   own rules.
6. Opening creates no Customer Group, Bill, Financial Obligation, Order, transfer,
   or Payment.
7. No success is displayed before durable confirmation.

### User Story E1.F4.US4 — Understand rejection or failure

**As a Host, I want a clear non-technical outcome when opening does not complete so
that I do not assume the Venue is open.**

#### Acceptance Criteria

1. A definitive rejection leaves the Venue closed.
2. No unapproved `Venue Opening Rejected` Domain Event is invented.
3. A technical failure is not misrepresented as a business rejection.
4. An uncertain outcome blocks unsafe repetition and requires authoritative
   retrieval.
5. The current confirmed readiness state determines the next screen.

**Status:** Blocked by the official Venue-opening Capability decision and technical
identity, session, persistence, concurrency, and Command-contract decisions.

## Feature E1.F5 — Opening Report

### User Story E1.F5.US1 — Preserve the opening record

**As a Manager or authorized reviewer, I want one permanent Opening Report so that
the conditions of daily opening remain explainable.**

#### Acceptance Criteria

1. Exactly one official Opening Report exists for the completed opening.
2. It contains Venue, Business Date, opening time, Host, every mandatory department,
   readiness at opening, delays, blocking issues, reasons, and comments.
3. It shows every mandatory department was READY at opening.
4. It does not claim that the Host verified other departments.
5. It cannot be silently deleted or rewritten.
6. Access follows approved responsibility and Capability rules.

**Status:** Ready for refinement, subject to retention and access technical
decisions.

# Epic E2 — Host Operational Dashboard

## Epic outcome

The Host can identify current operational attention without using a generic report
or receiving unapproved access.

## Authority

- Host Operational Playbook.
- `docs/ui/HOST_DASHBOARD_SPEC.md`, AC-01 through AC-50.
- Host Dashboard functional wireframes and user flow.
- DEC-003, DEC-007, DEC-010, DEC-017, DEC-018, DEC-038, DEC-039.

## Feature E2.F1 — Dashboard operating modes

### User Story E2.F1.US1 — See the correct operating mode

**As a Host, I want the Dashboard to distinguish before opening, Venue open, and
degraded connectivity so that I do not act on the wrong context.**

#### Acceptance Criteria

1. Mode follows authoritative Venue and connection state.
2. Loading never appears as operational zero.
3. Opening success transitions to live operation.
4. Degraded state shows last confirmed time and disables consequential actions.
5. Restored transport is reconciled before state is called current.

## Feature E2.F2 — Attention Queue

### User Story E2.F2.US1 — Review current Host Attention

**As a Host, I want confirmed Critical, Action required, and Awareness only facts so
that I can coordinate the next human step.**

#### Acceptance Criteria

1. Every item states the fact, reason, affected context, time, and next step.
2. Duplicate notifications do not create duplicate items.
3. Acknowledgment does not imply resolution.
4. No general issue, complaint, weather, prediction, or employee-scoring lifecycle
   is invented.
5. Financial and personal data remain excluded by default.

**Status:** Blocked by decisions for event scope, retention, Host-visible detail,
safe caching, and later domain data.

# Epic E3 — Guest Arrival and Service Location Identification

## Epic outcome

The Host can guide guests to a confirmed Service Location and introduce the
Responsible Waiter without creating a Customer Group or financial action.

## Authority

- DEC-011, DEC-030, DEC-031, DEC-035, DEC-038, DEC-039.
- Guest Arrival Workflow.
- `Identify Service Location`.
- Host Dashboard user flow transitions 16 through 20.

## Feature E3.F1 — Manual Service Location lookup

### User Story E3.F1.US1 — Find by visible identity

**As a Host, I want to find a Service Location by its visible name or number so that
service continues when NFC is unavailable.**

#### Acceptance Criteria

1. Exact Service Location identity, type, Area, Zone, and current state are shown.
2. Ambiguous results require deliberate verification.
3. Occupied and Unavailable never appear safely Available.
4. Lookup retrieves current central state and performs no business action.

## Feature E3.F2 — NFC identification

### User Story E3.F2.US1 — Identify the physical location

**As a Host, I want to tap the location’s NFC marker so that I reach the correct
digital context quickly.**

#### Acceptance Criteria

1. The marker holds no changing or sensitive business information.
2. NFC and manual lookup resolve to the same enduring Service Location.
3. One active marker cannot resolve to multiple Service Locations.
4. Missing, damaged, unsupported, or replaced NFC does not change location identity
   or history.
5. Failure leaves manual lookup available.
6. Identification grants no Capability and produces no official Domain Event.
7. Identification creates no Customer Group or financial or operational action.

**Status:** Blocked by supported-device policy, marker provisioning, and mismatch
procedure.

# Epic E4 — Customer Group Lifecycle and Responsibility

## Epic outcome

The Responsible Waiter can open one Active Customer Group at an Available Service
Location, preserving its complete operational identity.

## Authority

- DEC-011, DEC-012, DEC-030 through DEC-035, DEC-038, DEC-039.
- Customer Group Lifecycle.
- `Assign Responsible Waiter`.
- `Open Customer Group`.
- `Responsible Waiter Assigned`.
- `Customer Group Opened`.

## Feature E4.F1 — Responsible Waiter assignment

### User Story E4.F1.US1 — Accept service responsibility

**As an eligible Responsible Waiter, I want responsibility to be explicit so that
one person is accountable at a time.**

#### Acceptance Criteria

1. Exactly one eligible Responsible Waiter is associated with the Active Customer
   Group.
2. Role alone does not authorize assignment or opening.
3. Assignment is traceable.
4. The Host cannot automatically assign responsibility.

## Feature E4.F2 — Customer Group opening

### User Story E4.F2.US1 — Open official service

**As the Responsible Waiter with Open Customer Group, I want to intentionally open
the group so that service begins at the confirmed location.**

#### Acceptance Criteria

1. Venue is open.
2. Location is exactly identified, Available, and has no Active Customer Group.
3. Only the Responsible Waiter performs opening.
4. Success is atomic and produces `Responsible Waiter Assigned`, `Customer Group
   Opened`, and `Activity Logged`.
5. Beach Sunbed opening also produces `Financial Obligation Created`, `Bill
   Created`, and `Bill Line Added` exactly once.
6. Another location type may remain Active without a Bill.
7. Rejection leaves no partial group, occupancy, Bill, or charge.

## Feature E4.F3 — Customer Group transfer

### User Story E4.F3.US1 — Transfer the complete group

**As an authorized Staff Member, I want to move the complete Customer Group to an
Available Service Location so that service continuity is preserved.**

#### Acceptance Criteria

1. Destination is confirmed Available.
2. Customer Group identity, Orders, optional Bill, Payments, Responsible Waiter,
   and History are preserved.
3. Transfer succeeds completely or changes nothing.
4. `Transfer Completed` or `Transfer Rejected` accurately reflects the outcome.
5. Previous and new location and actor are auditable.

**Status:** Blocked by responsibility assignment, handover, completion, transfer,
and Physical Row charging decisions.

# Epic E5 — Waiter Ordering

## Epic outcome

Authorized service staff can submit multiple durable Order Rounds for one Active
Customer Group.

## Authority

- DEC-008, DEC-009, DEC-013, DEC-014, DEC-031, DEC-036, DEC-038.
- `Order Submitted`.
- `Order Submission Rejected`.
- Kitchen and Bar Ticket creation events.

## Feature E5.F1 — Draft and submit an Order Round

### User Story E5.F1.US1 — Submit a reviewed Order

**As authorized service staff, I want to submit one reviewed Order Round so that
preparation and Billing receive one reliable confirmed request.**

#### Acceptance Criteria

1. Draft is not an Order and creates no business fact.
2. Submitted items preserve quantity, price, destination, and approved instruction.
3. Success occurs only after durable acceptance.
4. Repeat interaction creates at most one Order.
5. Later Orders do not overwrite earlier rounds.
6. Mixed items create the appropriate separate Tickets.
7. Rejection creates no preparation or Bill effect.

**Status:** Blocked by Menu governance, correction and cancellation rules, and
downstream phase contracts.

# Epic E6 — Kitchen Preparation

## Epic outcome

Kitchen receives and progresses only confirmed Kitchen preparation work.

## Feature E6.F1 — Kitchen Ticket lifecycle

### User Story E6.F1.US1 — Progress Kitchen work

**As Kitchen Staff, I want to see and progress confirmed Kitchen Tickets so that
requested food is prepared reliably.**

#### Acceptance Criteria

1. Only Kitchen-destination items appear.
2. Ticket is created exactly once from an accepted Order.
3. Current state reloads from the central system.
4. Acknowledged, Ready, and Completed are used only after their operational meanings
   are approved.
5. No “delayed” state is inferred without an approved threshold.

**References:** DEC-008, DEC-013, DEC-017; `Kitchen Ticket Created`, `Kitchen Ticket
Acknowledged`, `Kitchen Ticket Ready`, `Kitchen Ticket Completed`.

**Status:** Blocked by preparation-state and responsibility decisions.

# Epic E7 — Bar Preparation and Fulfillment

## Epic outcome

Bar receives and progresses only confirmed Bar work.

## Feature E7.F1 — Bar Ticket lifecycle

### User Story E7.F1.US1 — Progress Bar work

**As Bar Staff, I want to see and progress confirmed Bar Tickets so that requested
drinks and fulfillment work remain reliable.**

#### Acceptance Criteria

1. Only Bar-destination items appear.
2. Ticket is created exactly once from an accepted Order.
3. Mixed Orders stay one Order Round.
4. Current state reloads from the central system.
5. Acknowledged, Ready, and Completed are used only after their operational meanings
   are approved.

**References:** DEC-008, DEC-013, DEC-017; `Bar Ticket Created`, `Bar Ticket
Acknowledged`, `Bar Ticket Ready`, `Bar Ticket Completed`.

**Status:** Blocked by preparation-state and responsibility decisions.

# Epic E8 — Billing

## Epic outcome

The Customer Group has one exact, explainable Bill only after its first Financial
Obligation.

## Feature E8.F1 — Financial Obligation and Bill creation

### User Story E8.F1.US1 — Create the Bill at the correct moment

**As the business, I want the first approved Financial Obligation to create the Bill
so that service and money owed remain distinct.**

#### Acceptance Criteria

1. A Customer Group may be Active without a Bill.
2. First obligation creates exactly one Bill.
3. Beach Sunbed opening creates the immediate approved obligation.
4. NFC, seating, and opening another Service Location type create no automatic
   Bill.
5. Each source produces an explainable Bill Line.
6. Historical price and charge facts do not change.

## Feature E8.F2 — Bill corrections and closure

### User Story E8.F2.US1 — Preserve explainable financial history

**As an authorized financial operator, I want corrections and closure to remain
traceable so that financial truth is never silently rewritten.**

#### Acceptance Criteria

1. Original Bill Lines are preserved.
2. Any approved reversal has a reason, actor, and Activity Log.
3. Closing requires every approved condition.
4. Bill closing does not automatically imply Customer Group completion unless later
   approved.
5. Bill reopening remains unavailable.

**References:** DEC-009, DEC-010, DEC-033, DEC-034, DEC-036, DEC-038; `Financial
Obligation Created`, `Bill Created`, `Bill Line Added`, `Bill Line Reversed`, `Bill
Closed`.

**Status:** Blocked by tax, charging, correction, and closing decisions.

# Epic E9 — Payments

## Epic outcome

Authorized staff can record exact confirmed Payments without duplication and close
eligible Bills.

## Feature E9.F1 — Record Payment

### User Story E9.F1.US1 — Record confirmed value received

**As an authorized Cashier, I want to record a confirmed Payment so that Bill
Balance reflects money actually received.**

#### Acceptance Criteria

1. Attempt and confirmed Payment are distinct.
2. Only `Payment Recorded` reduces Balance.
3. A repeated request cannot reduce Balance twice.
4. `Payment Rejected` leaves Balance unchanged.
5. Payment actor, amount, method, Bill, and time are traceable.

## Feature E9.F2 — Fully paid and close

### User Story E9.F2.US1 — Close an eligible Bill

**As an authorized Cashier, I want to close a Bill only after approved conditions
are satisfied so that the financial lifecycle is trustworthy.**

#### Acceptance Criteria

1. Zero Balance produces `Bill Fully Paid`.
2. Zero Balance alone does not complete the Customer Group.
3. Close Bill requires explicit Capability and approved closing rules.
4. Success produces `Bill Closed` and required Activity Log.
5. Bill reopening remains forbidden.

**References:** DEC-009, DEC-010, DEC-014, DEC-038; `Payment Recorded`, `Payment
Rejected`, `Payment Reversed`, `Bill Fully Paid`, `Bill Closed`.

**Status:** Blocked by Payment allocation, reversal, refund, closing, fiscal, and
integration decisions.

# Epic E10 — Manager Oversight

## Epic outcome

Managers receive approved operational and reporting awareness without automatic
authority or staff surveillance.

## Feature E10.F1 — Current operational overview

### User Story E10.F1.US1 — Understand current Venue operation

**As a Manager, I want approved operational facts in one view so that I can support
teams and resolve exceptions.**

#### Acceptance Criteria

1. Every measure has an approved definition.
2. Current facts trace to authoritative Domain Concepts and Events.
3. Manager Role alone grants no protected action.
4. Financial and staff detail follows minimum necessary access.
5. No employee scoring, emotional inference, or unapproved AI decision appears.

## Feature E10.F2 — Historical operational review

### User Story E10.F2.US1 — Review explainable history

**As a Manager, I want approved Opening Reports, Activity Logs, and Audit Trails so
that recurring issues can be understood and coached.**

#### Acceptance Criteria

1. Opening Reports remain permanent.
2. Activity Log and Audit Trail retain their distinct meanings.
3. History is not silently changed.
4. Access is scoped by Venue, responsibility, and Capability.
5. Review supports coaching rather than ranking or blame.

**References:** DEC-001, DEC-010, DEC-020, DEC-038, DEC-039; Host and Framework
principles.

**Status:** Blocked by reporting definitions, Manager Capability catalogue, privacy,
retention, and earlier phase completion.

## Backlog entry rules

An item may enter a Sprint only when:

1. Its business behavior is supported by Accepted Decisions.
2. Its Commands and Domain Events are sufficiently defined for the intended scope.
3. Any Command-gated rules needed by the story are approved.
4. Required technical decisions are Accepted.
5. Acceptance Criteria include failure, authorization, audit, and retry behavior
   where relevant.
6. Test data and human acceptance ownership are identified.
7. It does not depend on a future Epic that has not supplied an approved contract.
