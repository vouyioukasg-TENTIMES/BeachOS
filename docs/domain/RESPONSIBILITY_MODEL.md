# BeachOS Responsibility Model

## Purpose

This document investigates whether the approved BeachOS business model is
fundamentally state driven or responsibility driven.

It examines approved Product Decisions, capabilities, workflows, Domain Events,
the Customer Journey, Operational Intelligence, Operational Learning, and the
First Operational Day. It ignores current implementation, interfaces, and
technical delivery.

It does not create a new Product Decision. Where responsibility is unresolved,
the uncertainty remains explicit.

# Conclusion

## BeachOS is fundamentally responsibility driven

BeachOS uses states, but states are not its organizing purpose.

The approved product repeatedly asks:

- Who is responsible now?
- What decision belongs to that person or department?
- What confirmed facts allow that person to act?
- Has responsibility been knowingly accepted?
- Has responsibility ended, or does outstanding work remain?
- Who must receive the next handoff?

Operational states such as `READY`, `BLOCKED`, `ACTIVE`, `NEW`,
`ACKNOWLEDGED`, `OPEN`, and `CLOSED` make responsibility understandable. They
describe facts that constrain action. They do not replace accountable humans or
decide hospitality work by themselves.

A purely state-driven interpretation would make progress primarily a sequence
of status changes. That would be inconsistent with the approved model because:

- a department’s readiness must be declared by its responsible person;
- the Host coordinates Venue Opening but cannot replace department ownership;
- the Host coordinates Guest Arrival but cannot open the Customer Group;
- the Responsible Waiter must knowingly accept responsibility;
- Roles describe responsibilities while Capabilities authorize actions;
- Kitchen and Bar acknowledge only their own confirmed work;
- a zero Bill Balance does not automatically close the Bill;
- historical facts may inform advice but never override current facts or human
  authority;
- several future states remain intentionally unavailable until their ownership
  and business meaning are approved.

The strongest description is therefore:

> BeachOS is a responsibility-driven hospitality operating system whose states
> provide evidence, constraints, continuity, and accountability for human
> decisions.

# What Is Operational Responsibility?

Operational responsibility is the business expectation that a known human,
department, or explicitly approved operational function will understand a
defined situation, make or coordinate the decisions that belong to it, and
carry the work until an approved outcome or accepted handoff occurs.

Operational responsibility has several dimensions:

- **scope** — the guest, Customer Group, department, Ticket, Bill, Payment, or
  operational period concerned;
- **purpose** — what the responsible party is expected to protect or achieve;
- **authority** — which actions the person is permitted to perform through
  Capabilities;
- **current facts** — what is known, unknown, ready, blocked, active, or
  completed;
- **continuity** — responsibility remains visible while work is outstanding or
  its outcome is uncertain;
- **acceptance** — a handoff must not silently make another person responsible;
- **ending condition** — responsibility ends only when the approved outcome or
  handoff has been confirmed;
- **history** — consequential responsibility changes remain explainable.

Responsibility is not identical to Role, Capability, task assignment, physical
location, custody, blame, or system access.

# Who Owns Responsibility?

The approved model supports different owners at different scopes.

## Individual responsibility

A Staff Member may own an operational responsibility personally:

- a department’s responsible person owns its opening-readiness declaration;
- the Host owns coordination of Venue Opening and the arrival experience;
- the Responsible Waiter owns the active Customer Group’s service context;
- an authorized Cashier may own a Payment-recording action when that capability
  is later implemented.

The Staff Member’s Role describes the responsibility. A Capability separately
authorizes protected action. Neither alone proves that a specific responsibility
has been accepted in the current situation.

## Department responsibility

Kitchen and Bar own separate destination-specific work. A concrete Ticket makes
that scope visible. Department responsibility does not merge because both
Tickets originate from one Order.

## Coordinating responsibility

The Host may own coordination without owning every specialist verification or
action. This is a genuine responsibility, not a weaker substitute for execution.
The Host protects continuity, visibility, and escalation while department owners
retain their own truth.

## Product and business responsibility

The business owns definitions, standards, and approved operational truth.
BeachOS records facts, enforces approved constraints, explains uncertainty, and
advises. It does not become the human owner of hospitality decisions.

# How Is Responsibility Transferred?

The approved model establishes one clear transfer pattern during Guest Arrival:

1. the Host owns arrival coordination;
2. the Host introduces the relevant context and proposed Service Location;
3. an eligible Responsible Waiter reviews the context;
4. the Responsible Waiter explicitly accepts service responsibility;
5. the Responsible Waiter intentionally opens the Customer Group;
6. exactly one Responsible Waiter becomes accountable for ongoing service;
7. the Host can return attention to arrival coordination once the handoff is
   clear.

This proves that an approved transfer requires more than changing an assigned
name. It requires clear scope, an eligible receiver, acceptance, and a confirmed
business outcome.

Other transfers remain incomplete:

- waiter handover is recognized but its acceptance conditions are unresolved;
- Kitchen/Bar readiness, collection, Runner handoff, and delivery are
  unresolved;
- transfer of a Customer Group between Service Locations preserves the same
  Responsible Waiter unless a separate approved handover changes responsibility;
- Cashier, payment, Bill-closing, departure, and Venue-closing handoffs lack
  complete approved lifecycles.

No general transfer rule should be inferred from the one approved Guest Arrival
pattern. Each future transfer must define what moves, what remains, who accepts,
and what fact confirms continuity.

# How Is Responsibility Accepted?

Acceptance is an intentional human acknowledgment that a defined responsibility
is understood and taken on.

Approved examples differ in meaning:

- a department readiness declaration confirms the responsible person’s current
  assessment; it does not transfer the Host’s coordination responsibility;
- Responsible Waiter acceptance is required before the Customer Group opens;
- Kitchen Ticket Acknowledged means Kitchen recognizes its confirmed work;
- Bar Ticket Acknowledged means Bar recognizes its confirmed work.

Acceptance cannot be inferred from:

- a Role assignment alone;
- possession of a Capability;
- viewing a screen or Ticket;
- physical presence;
- NFC or manual identification;
- elapsed time;
- another person assigning responsibility without receiver acceptance;
- a message being sent or technically delivered.

The exact evidence required for future waiter handover, Runner handoff, payment
ownership, and departure remains unresolved.

# Responsibility and Physical Custody

## Can responsibility exist without physical custody?

Yes. This is already fundamental to the approved model.

- The Host owns arrival coordination without possessing a guest, location, or
  department’s work.
- The Responsible Waiter owns the Customer Group’s service context while food
  or drinks remain physically with Kitchen or Bar.
- A department owner declares readiness without physically holding every object
  involved in Venue Opening.
- The Cashier may become responsible for recording a Payment without physical
  custody of every ordered item.

Responsibility may concern awareness, decision, coordination, verification, or
accountability rather than possession.

## Can physical custody exist without responsibility?

Potentially, but the current approved model does not define a general custody
lifecycle.

A Staff Member may physically carry or hold work while broader service
responsibility remains with another person. However, BeachOS currently has no
approved facts for collection, Runner custody, handoff, or Item Delivered.
Therefore it cannot reliably identify custody or use it to infer responsibility.

Future product design must distinguish:

- holding an item;
- being accountable for its safe and correct handoff;
- owning preparation work;
- owning the Customer Group relationship;
- confirming delivery.

# Can Responsibility Be Shared?

Different responsibilities may operate concurrently around the same guest
journey:

- the Host coordinates arrival;
- the Responsible Waiter owns service for the Customer Group;
- Kitchen owns Kitchen Ticket work;
- Bar owns Bar Ticket work;
- a Cashier may later own an authorized payment action.

This is coordinated responsibility, not ambiguous shared ownership of one
undivided obligation.

The approved model favors one clear owner for a defined scope:

- one responsible person per opening department;
- one Responsible Waiter at a time per Customer Group;
- concrete Kitchen and Bar responsibility rather than generic preparation
  ownership.

Whether one exact responsibility may be jointly owned is not generally
approved. Future capabilities should prefer separate, explicit scopes and a
named coordinating responsibility. Shared ownership should require a Product
Decision because it can make acceptance, escalation, completion, and audit
meaning ambiguous.

# Can Responsibility Be Temporarily Delegated?

Ordinary teamwork can include assistance, but formal temporary delegation is
not yet an approved general Domain behavior.

The repository distinguishes assistance from changed responsibility:

- the Host may coordinate without taking over a department’s verification;
- another Staff Member may help without becoming the Responsible Waiter;
- a Role or Capability grant does not automatically change current ownership;
- responsible waiter handover is recognized as a future business event but its
  workflow is gated.

Any formal delegation model must later decide:

- the delegator and receiver;
- whether acceptance is required;
- which responsibilities and Capabilities are included;
- start and end conditions;
- whether the original owner remains accountable;
- how revocation and uncertain outcomes work;
- what history must be preserved.

Until those decisions exist, BeachOS must not silently model assistance as
delegation or delegation as permanent transfer.

# Responsibility Across Capabilities

## Venue Opening

**Responsibility structure:** Department owners verify and declare their own
readiness. The Host coordinates the whole opening and performs `OPEN VENUE` only
after every mandatory department is Ready.

**State relationship:** `READY`, `NOT READY`, and `BLOCKED` communicate each
owner’s current fact. The Venue’s opening state constrains guest operations but
does not erase the underlying human declarations.

**Transfer and acceptance:** Department responsibility is configured before the
workflow. The Host receives declarations but does not take ownership of their
truth. No general opening-responsibility handover is approved.

**Unresolved boundary:** Venue Closing ownership and any formal substitute for
an absent department owner remain unresolved.

## Guest Arrival

**Responsibility structure:** The Host owns arrival recognition, honest
coordination, seating guidance, and continuity until a clear handoff. The
Responsible Waiter owns the decision to start service.

**State relationship:** Venue openness and Service Location availability make
the handoff possible but do not perform it. Identification supplies context; it
does not authorize action.

**Transfer and acceptance:** This is the clearest approved transfer: Host to an
eligible Responsible Waiter through explicit acceptance and intentional
Customer Group opening.

**Unresolved boundary:** Formal Host-to-Host arrival handover, waiting ownership,
automatic waiter selection, VIP handling, and capacity or accessibility
responsibility remain unresolved.

## Customer Group

**Responsibility structure:** The Customer Group is the primary operational
entity and has exactly one Responsible Waiter at a time. It carries Service
Location, Orders, optional Bill, Payments, and History as one continuing
service context.

**State relationship:** `ACTIVE` indicates that service may continue under
approved rules. A Customer Group can exist without a Bill. State does not
replace the named Responsible Waiter.

**Transfer and acceptance:** Service Location transfer preserves Customer Group
identity and existing responsibility. Responsible Waiter change is recognized,
but its handover and acceptance rules remain gated.

**Unresolved boundary:** Customer Group completion, no-Bill completion,
reopening, cancellation, and responsibility after departure are unresolved.

## Ordering

**Responsibility structure:** Authorized service staff review and submit one
Order Round for the active Customer Group. The Responsible Waiter remains part
of the preserved service context. Ordering creates concrete downstream Kitchen
and Bar work without transferring the whole Customer Group responsibility.

**State relationship:** Submission turns a reviewed intention into a permanent
Order. Later rounds are new Orders, not mutations of earlier responsibility or
history.

**Transfer and acceptance:** `Kitchen Ticket Created` and `Bar Ticket Created`
establish department-specific confirmed work. Department acknowledgment later
confirms recognition; Ticket creation alone must not be treated as human
acceptance.

**Unresolved boundary:** Cancellation, correction, unavailable items, and their
downstream responsibility effects remain gated.

## Kitchen

**Responsibility structure:** Kitchen owns only Kitchen-destination work from
its concrete Ticket. Acknowledgement confirms that Kitchen recognizes this work
as active.

**State relationship:** `NEW` and `ACKNOWLEDGED` distinguish unrecognized from
recognized work. Acknowledgement does not mean preparation started, Ready,
Completed, collected, or delivered.

**Transfer and acceptance:** Kitchen accepts responsibility through the approved
acknowledgement. No approved handoff from Kitchen to Runner or Responsible
Service Staff exists.

**Unresolved boundary:** Ready, partial readiness, completion, custody, Runner,
delivery, remake, and exception responsibility require Product Decisions.

## Bar

**Responsibility structure:** Bar owns only Bar-destination work from its
concrete Ticket. It remains independent from Kitchen even when both Tickets
belong to one Order.

**State relationship:** Bar acknowledgement proves recognition of active work,
not readiness or fulfilment.

**Transfer and acceptance:** Bar accepts responsibility through its concrete
acknowledgement. No physical handoff or delivery transfer is approved.

**Unresolved boundary:** The meaning may differ for packaged items, prepared
drinks, direct counter handoff, and Runner delivery. None may be inferred.

## Billing

**Responsibility structure:** The business owns financial truth. A Financial
Obligation arises only from an approved reason. The Bill aggregates those facts
for one Customer Group. Authorized humans will own corrections and closing once
their rules are approved.

**State relationship:** A Bill may be absent, open, fully paid, or later closed.
Zero Balance is a financial fact and does not automatically end operational
responsibility or close the Customer Group.

**Transfer and acceptance:** No general transfer of Bill responsibility is
approved. The running Bill remains with the Customer Group during Service
Location transfer.

**Unresolved boundary:** Closing authority, exceptions, corrections, reopening,
and the connection between outstanding fulfilment and Bill closing remain
unresolved.

## Payments

**Responsibility structure:** An authorized Staff Member confirms that the
business received an exact amount through an approved Payment Method. This is a
sensitive accountability boundary, not merely a state update.

**State relationship:** `Payment Recorded` changes Bill Balance exactly once.
`Bill Fully Paid` means zero Balance but does not prove Bill closure or guest
departure.

**Transfer and acceptance:** The current model does not define transfer of
payment handling among Responsible Service Staff, Cashier, and Manager.

**Unresolved boundary:** Partial, split, excess, reversed, refunded, cash-change,
tip, failure-recovery, and post-closing responsibility remain unresolved.

## Departure

**Responsibility structure:** The complete departure owner is not approved.
Responsible Service Staff, Cashier, Host, cleaning responsibility, and Manager
may each have distinct future scopes, but none may be merged by assumption.

**State relationship:** Physical departure, zero Balance, Bill closure, Customer
Group completion, Service Location release, and location readiness are distinct
possible facts. Their required order is unresolved.

**Transfer and acceptance:** No approved responsibility chain carries the guest
from final service through Payment, departure, location release, and reset.

**Unresolved boundary:** Departure remains a missing capability. BeachOS cannot
release the Service Location or complete the Customer Group merely because the
guest leaves physically or the Bill reaches zero.

# States as Evidence of Responsibility

BeachOS still needs states. Their proper role is to answer responsibility-driven
questions:

| State or fact                | Responsibility question it helps answer                                           |
| ---------------------------- | --------------------------------------------------------------------------------- |
| Department `READY`           | Has the responsible department owner confirmed readiness for Venue Opening?       |
| Venue `OPEN`                 | May responsible people begin guest operations for this Business Date?             |
| Service Location `AVAILABLE` | May the Host propose this context for a handoff?                                  |
| Customer Group `ACTIVE`      | Does ongoing service responsibility exist?                                        |
| Order Submitted              | Has the submission responsibility produced a permanent accepted round?            |
| Ticket `NEW`                 | Which department has confirmed work that is not yet acknowledged?                 |
| Ticket `ACKNOWLEDGED`        | Has the department recognized its work as active?                                 |
| Bill Balance zero            | Is the financial amount settled, while other closing responsibilities may remain? |

This distinction prevents status-driven shortcuts. A state permits, blocks, or
explains responsibility; it does not manufacture acceptance, authority, custody,
or completion.

# Responsibility, Operational Intelligence, and Learning

Operational Intelligence should advise only when the responsible human, current
facts, decision, and next authorized action are clear. Unowned work deserves
attention. Ambiguous ownership may be a Blocker when an approved operation
requires a responsible person.

Operational Learning may remember confirmed responsibility changes and compare
them with approved standards. It must not:

- infer responsibility from frequent behavior;
- turn a common informal handoff into a rule;
- judge a person without relevant operational context;
- use historical ownership to override current acceptance;
- recommend an action to someone who lacks responsibility or authority.

Responsibility history exists for continuity, explanation, coaching, and safer
operations—not punishment or surveillance.

# Domain Gaps Revealed by This Investigation

The responsibility-driven interpretation exposes Product Owner decisions still
required for:

1. Responsible Waiter handover and receiver acceptance.
2. Temporary delegation and the distinction between assistance and transfer.
3. Kitchen and Bar Ready and Completed meanings.
4. Runner identity, responsibility, custody, and handoff.
5. Item Delivered meaning and authority.
6. Order cancellation and correction responsibility across departments.
7. Billing correction, closing, and reopening responsibility.
8. Payment handling, reversal, refund, and recovery responsibility.
9. Customer Group completion, including a group without a Bill.
10. Physical departure, Service Location release, cleaning/reset, and Venue
    Closing responsibility.

These gaps are not evidence that BeachOS should become state driven. They show
that a new state must not be introduced before its responsible humans and
handoffs are understood.

# Recommended Responsibility Principles

Every future BeachOS capability should follow these principles:

1. **Name the responsibility before naming the state.** Define who owns the
   operational outcome and why before adding a status.
2. **Give each responsibility a clear scope.** State whether it concerns a
   Venue, Customer Group, Ticket, Bill, Payment, Service Location, or another
   approved concept.
3. **Separate Role, Capability, and current responsibility.** Role describes
   business responsibility, Capability authorizes action, and current ownership
   identifies who is accountable now.
4. **Require intentional acceptance for consequential handoffs.** Do not make a
   person responsible merely because another person selected their name.
5. **Preserve continuity until acceptance is confirmed.** The existing owner or
   an explicitly approved coordinating owner must remain visible during a
   handoff.
6. **Prefer one clear owner per defined responsibility.** Coordinate multiple
   scopes explicitly instead of hiding ambiguity behind shared ownership.
7. **Distinguish assistance, delegation, transfer, and custody.** They are not
   synonyms and must not silently change accountability.
8. **Do not equate physical custody with responsibility.** Define both when a
   workflow depends on possession or handoff.
9. **Make ending conditions explicit.** Responsibility ends only through an
   approved outcome, accepted transfer, or approved cancellation—not elapsed
   time or a convenient state change.
10. **Let states provide evidence, not ownership.** A state may permit, block,
    or explain action but cannot replace human authority or acceptance.
11. **Keep departmental responsibility concrete.** Kitchen and Bar may share
    mechanics but retain separate business ownership and events.
12. **Preserve uncertainty.** When ownership, custody, or outcome cannot be
    confirmed, BeachOS must say so and must not assign responsibility by
    inference.
13. **Keep financial and operational responsibility distinct.** Payment, zero
    Balance, Bill closure, Customer Group completion, and departure are separate
    facts unless a Product Decision explicitly connects them.
14. **Record consequential changes without creating surveillance.** History
    should support continuity, audit, recovery, and coaching for an approved
    purpose.
15. **Keep advice explainable and human decisions human.** BeachOS may bring the
    right facts to the responsible person; it must not silently become the owner
    of the decision.
16. **Do not learn new responsibility rules from repetition.** Operational
    Learning may reveal a pattern, but the business must approve any changed
    standard.
17. **Treat responsibility ambiguity as a product-design gap.** Do not conceal
    it with generic states, default assignments, or technical automation.
18. **Require Product Owner approval before responsibility changes become Domain
    rules.** Implementation and architecture must follow the approved business
    meaning, never create it.

Under these principles, BeachOS can remain operationally clear as it expands:
states describe what is true, while responsibility explains who must understand
that truth and carry hospitality forward.
