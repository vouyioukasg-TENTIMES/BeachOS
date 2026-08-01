# BeachOS Explainability Engine

## Purpose

The BeachOS Explainability Engine defines the business obligation to explain
every important operational fact to a human.

It is not Artificial Intelligence, a chatbot, a reporting feature, or a
technical mechanism. It is a standard for honest operational meaning.

BeachOS should never present an important statement as a conclusion that people
must simply trust. It should be possible to understand what is true, the
evidence supporting it, the responsible source, the approved business meaning,
the remaining uncertainty, and the human decision that still follows.

Explainability protects the relationship between the real operation and the
Operational Digital Twin. It allows staff, managers, owners, testers, designers,
and future product teams to distinguish reliable operational truth from an
assumption, recommendation, historical pattern, or incomplete situation.

# What Every Important Fact Must Explain

For every consequential operational fact, BeachOS should be able to answer:

1. **What is true?** State the business fact precisely and name its scope.
2. **How do we know it?** Identify the supporting current evidence.
3. **Who confirmed it?** Name the responsible human, department, or approved
   business outcome that established it.
4. **When was it confirmed?** Give the relevant Business Date and time or
   historical period.
5. **Which Product Decision allows this fact to exist?** Connect the statement
   to its approved business authority.
6. **Which Capability produced it?** Name the operational capability whose
   approved outcome created the fact.
7. **Which Domain Events support it?** Identify the completed business facts in
   its history. If no Domain Event is appropriate, say so.
8. **Which uncertainty still exists?** State what the fact does not prove, what
   may be stale, and what remains unknown.
9. **What human decision is still required?** Explain who remains responsible
   for the next judgment or action.

A fact is not fully explained if it answers only “what” while hiding “why,”
“who,” “when,” or “what remains unresolved.”

# Core Concepts

## Operational Fact

An Operational Fact is a business statement that BeachOS may responsibly treat
as true within a defined scope and time.

Examples include:

- the Bar declared `BLOCKED` for this Venue opening;
- the Venue opened for this Business Date;
- this Customer Group is active at Beach A12;
- this Order Round was accepted;
- Kitchen acknowledged this Kitchen Ticket;
- this Payment was recorded against this Bill.

An Operational Fact must not be created from expectation, probability, silence,
elapsed time, visual convenience, or repeated historical behavior.

## Supporting Evidence

Supporting Evidence is the confirmed material that justifies an Operational
Fact.

Evidence may include:

- a declaration made by the responsible person;
- an approved intentional business action and its outcome;
- a permanent Order, Ticket, Bill, Payment, or Opening Report;
- related Domain Events;
- a required Activity Log;
- approved configuration relevant to the fact;
- current context that establishes Venue, Business Date, responsibility, and
  scope;
- confirmed historical facts used for an Operational Learning explanation.

Evidence must be relevant and sufficient for the exact statement. Evidence that
supports a weaker fact must not be used to claim a stronger one. For example, a
Ticket acknowledgment supports “the department recognized the work,” not “the
work is ready.”

## Business Explanation

A Business Explanation describes why the fact is valid in the official language
of the business.

It connects:

- the approved definition;
- the Product Decision;
- the responsible Capability;
- the required conditions;
- the completed outcome;
- its consequences and limits.

A Business Explanation is precise enough for product governance, operational
review, testing, and audit. It must not rely on technical terminology.

## Human Explanation

A Human Explanation expresses the same truth in calm, direct language suited to
the person making the next operational decision.

It should answer:

- what happened or is true now;
- why BeachOS can say it;
- what it means for this person;
- what BeachOS still does not know;
- what decision remains theirs.

A Human Explanation should not overwhelm people with every historical detail.
It should allow deeper evidence to be examined when needed without concealing
the essential reason.

## Explainability Chain

The Explainability Chain is the complete connection from a BeachOS statement
back to its approved meaning and forward to the remaining human decision.

```text
Operational statement
→ scope and current fact
→ supporting evidence
→ responsible confirmer
→ confirmation time
→ Product Decision
→ Capability
→ Domain Events and relevant history
→ remaining uncertainty
→ next responsible human decision
```

If one link is missing, the explanation should identify the gap rather than
silently bridge it.

## Evidence Chain

The Evidence Chain shows how individual confirmed facts support a conclusion.

For Venue readiness, for example:

```text
Mandatory department configuration
→ latest attributable declaration for each department
→ every mandatory department is READY
→ Venue is eligible to be opened
```

The Evidence Chain must preserve counterevidence, superseded facts, and scope.
An earlier `BLOCKED` declaration remains history even when a later `READY`
declaration becomes current. Yesterday’s evidence does not prove today’s truth.

## Responsibility Chain

The Responsibility Chain shows who owned each relevant responsibility, whether
it was accepted, how it changed, and who owns the next decision.

For Guest Arrival:

```text
Host owns arrival coordination
→ eligible Responsible Waiter reviews the handoff
→ Responsible Waiter explicitly accepts
→ Customer Group opens
→ Responsible Waiter owns active service
```

Responsibility must not be inferred from Role, Capability, physical presence,
message receipt, or another person’s assignment alone.

## Decision Chain

The Decision Chain connects Product Governance to the operational outcome.

```text
Approved Product Decision
→ official business rule and concept
→ approved Capability
→ authorized human intention
→ completed Domain Event
→ current Operational Fact
→ next human decision
```

The Decision Chain prevents implementation, habit, or technical convenience from
quietly becoming product authority.

# Explainability Levels

## Immediate explanation

The smallest useful explanation for live operations:

> The Venue cannot open because Maintenance is BLOCKED. Nikos confirmed an
> electrical issue at 08:14. Maintenance must declare READY before the Host can
> decide to open.

## Operational detail

The evidence relevant to coordination:

- current and earlier declarations;
- required department status;
- responsible person;
- Business Date and time;
- blocking reason;
- current responsible next step.

## Governance detail

The authority required for review:

- Product Decision;
- Capability definition;
- Domain Event meaning;
- related business rules;
- Activity Log or Audit Trail where required;
- known unresolved Product Decisions.

The levels differ in depth, not truth. A short explanation must never contradict
the complete explanation.

# Explainability Examples

The examples below describe the explanation each operational fact requires.
They do not claim that every capability is currently implemented.

## Venue Opening

### What is true?

The Venue is officially open for the named Business Date.

### How do we know it?

Every mandatory department had a current `READY` declaration, an authorized
Host intentionally opened the Venue, and the permanent Opening Report confirms
the outcome.

### Who confirmed it?

Each department owner confirmed their own readiness. The Host confirmed the
opening decision.

### When was it confirmed?

At the opening time recorded for the Venue and Business Date.

### Which Product Decision allows this fact to exist?

DEC-039 establishes the Venue Opening workflow and its responsibility boundary.
DEC-038 separates Role responsibility from Capability authority.

### Which Capability produced it?

Venue Opening.

### Which Domain Events support it?

`Department Readiness Declared`, `Venue Opened for Business Date`, and
`Activity Logged` where required.

### Which uncertainty still exists?

Opening proves eligibility was confirmed at that moment. It does not prove that
no later operational problem occurred or that every Service Location is ready
for every guest.

### What human decision is still required?

The Host and responsible departments continue monitoring current conditions and
decide how to respond to changes.

### Human explanation

> Emerald opened for 1 August at 08:30. Every mandatory department had declared
> READY, and the Host completed the opening. Current issues after 08:30 still
> require review; opening does not guarantee that every later condition remains
> ready.

## Department Readiness

### What is true?

One department is currently `READY`, `NOT READY`, or `BLOCKED` for Venue
Opening.

### How do we know it?

The configured responsible person made the latest declaration for the current
Venue and Business Date. A reason accompanies `NOT READY` or `BLOCKED`.

### Who confirmed it?

The department’s responsible person—not the Host.

### When was it confirmed?

At the time of the latest declaration. Earlier declarations remain historical
evidence.

### Which Product Decision allows this fact to exist?

DEC-039 approves department-owned readiness declarations and Host coordination.

### Which Capability produced it?

Department Readiness Declaration within Venue Opening.

### Which Domain Events support it?

`Department Readiness Declared`.

### Which uncertainty still exists?

The declaration may later become stale if reality changes. It does not prove
the physical condition through independent observation.

### What human decision is still required?

The responsible department person decides when a new declaration is justified;
the Host decides whether to open only after the complete gate is satisfied.

### Human explanation

> Bar is BLOCKED. Eleni confirmed at 08:12 that the ice machine failed. Bar must
> reassess and declare a new status; the Host cannot replace that declaration.

## Guest Arrival

### What is true?

The arriving party has either remained in human arrival coordination or become
an active Customer Group through an accepted Responsible Waiter handoff.

### How do we know it?

The Venue was open, a Service Location was confirmed, an eligible Responsible
Waiter accepted responsibility, and the waiter intentionally opened the
Customer Group.

### Who confirmed it?

The Host confirms arrival coordination and physical context through human
practice. The Responsible Waiter confirms acceptance and official service
opening.

### When was it confirmed?

At the attributable handoff and Customer Group opening time. BeachOS does not
invent an arrival time from automatic detection.

### Which Product Decision allows this fact to exist?

DEC-031 makes Customer Group the primary operational entity. DEC-035 requires
the Responsible Waiter to open it. DEC-030 governs Service Location Digital
Identity. DEC-034 governs the Beach Sunbed opening obligation.

### Which Capability produced it?

Guest Arrival and Customer Group Opening.

### Which Domain Events support it?

`Responsible Waiter Assigned`, `Customer Group Opened`, and, for a Beach Sunbed,
`Financial Obligation Created`, `Bill Created`, and `Bill Line Added`.

### Which uncertainty still exists?

BeachOS does not prove that the guest was greeted, understood, satisfied, or
physically seated merely from identification or opening. Waiting, VIP,
accessibility, and capacity rules remain incomplete.

### What human decision is still required?

The Host decides how to coordinate arrival; the Responsible Waiter decides
whether to accept responsibility and begin service.

### Human explanation

> This party became Customer Group CG-24 at Beach A12 when Maria accepted
> responsibility and opened service at 09:08. The NFC identification only found
> Beach A12; it did not open the group or create the charge by itself.

## Customer Group

### What is true?

One Customer Group is active at a confirmed Service Location with exactly one
Responsible Waiter and its continuing Orders, optional Bill, Payments, and
History.

### How do we know it?

The group was intentionally opened and no approved completion has occurred.
Every accepted Order and financial fact remains attached to the same identity.

### Who confirmed it?

The Responsible Waiter confirmed opening. Other authorized humans confirm later
facts within their narrower responsibilities.

### When was it confirmed?

At opening, with later current facts attributed to their own times.

### Which Product Decision allows this fact to exist?

DEC-011 limits one active Customer Group per Service Location. DEC-031 makes the
Customer Group primary. DEC-033 allows it to exist without a Bill. DEC-035 owns
opening responsibility. DEC-036 permits multiple Orders.

### Which Capability produced it?

Customer Group Opening, followed by approved service capabilities.

### Which Domain Events support it?

`Customer Group Opened`, `Responsible Waiter Assigned`, and all later approved
events connected to the group.

### Which uncertainty still exists?

Active does not prove that guests are still physically present, every item was
delivered, or the group is ready to complete. Completion rules are unresolved.

### What human decision is still required?

The Responsible Waiter continues service decisions. Future authorized humans
must decide transfer, handover, financial closure, and completion under approved
rules.

### Human explanation

> CG-24 remains active at Beach A12 under Maria’s responsibility. It has two
> Order Rounds and one running Bill. BeachOS has no confirmed completion or
> departure fact.

## Service Location

### What is true?

The named Service Location has one stable identity and a current confirmed
operational status and Customer Group relationship.

### How do we know it?

Its permanent business identity and visible name are approved configuration.
Its current occupancy follows confirmed Customer Group opening, transfer, or
completion facts.

### Who confirmed it?

Authorized business setup establishes identity. Responsible staff confirm the
operational actions that change occupancy. NFC or manual lookup only identifies
the location.

### When was it confirmed?

Identity is enduring. Current state is confirmed at the latest relevant
operational event and must be reconsidered if physical reality conflicts.

### Which Product Decision allows this fact to exist?

DEC-011 protects one active group per location. DEC-012 preserves group identity
during transfer. DEC-030 establishes stable Digital Identity. DEC-032 keeps Zone
assignment operational and independent from location identity.

### Which Capability produced it?

Venue setup establishes identity; Guest Arrival, Customer Group Opening, and
future Transfer or Completion capabilities establish operational state.

### Which Domain Events support it?

`Customer Group Opened`, `Transfer Completed`, and future
`Customer Group Completed` where approved. Identification alone produces no
Domain Event.

### Which uncertainty still exists?

Damage, cleanliness, unreported physical occupancy, moved tags, and release
after departure may be unknown. A Digital Identity match does not prove physical
suitability.

### What human decision is still required?

The Host and responsible staff decide whether physical and digital context agree
and whether the location is suitable for the next operation.

### Human explanation

> Beach A12 is the same Service Location even though its NFC tag was replaced.
> It is shown occupied because CG-24 was opened there. Confirm the physical
> context if what you see at the beach disagrees.

## Ordering

### What is true?

One reviewed Order Round was safely accepted for an active Customer Group with
preserved items, quantities, notes, prices, and preparation destinations.

### How do we know it?

The submission succeeded as one complete business outcome. Its destination
Tickets and financial consequences agree with the accepted items.

### Who confirmed it?

The authorized submitting Staff Member confirmed the reviewed Order intention;
the accepted business outcome confirms preservation.

### When was it confirmed?

At the Order submission time.

### Which Product Decision allows this fact to exist?

DEC-008 protects orders from loss. DEC-013 governs destination routing. DEC-036
defines one Order per round and one running Bill. DEC-038 governs Capability
authority.

### Which Capability produced it?

Ordering.

### Which Domain Events support it?

`Order Submitted`, zero or one `Kitchen Ticket Created`, zero or one
`Bar Ticket Created`, related `Financial Obligation Created` and
`Bill Line Added`, and `Bill Created` only for the first obligation.

### Which uncertainty still exists?

Submission does not prove acknowledgement, preparation, readiness, delivery, or
consumption. A lost response may leave submission outcome uncertain until
current facts are reconciled.

### What human decision is still required?

Responsible service staff decide whether the draft is correct and when to
submit. Departments later decide how to perform their work.

### Human explanation

> Order O-18 was accepted at 09:27 for CG-24. Food became Kitchen Ticket K-18,
> drinks became Bar Ticket B-18, and the accepted items added €34 to the running
> Bill. This does not mean preparation is complete.

## Kitchen Ticket

### What is true?

The Kitchen Ticket contains confirmed Kitchen work, and its current approved
state is either awaiting acknowledgment or acknowledged.

### How do we know it?

An accepted Order created the concrete Ticket. Authorized Kitchen Staff may
then acknowledge that Kitchen recognizes it as active work.

### Who confirmed it?

Ordering confirms Ticket creation as a consequence of submission. Kitchen Staff
confirm acknowledgment.

### When was it confirmed?

Creation time and acknowledgment time remain separate.

### Which Product Decision allows this fact to exist?

DEC-013 approves destination-specific Kitchen work.

### Which Capability produced it?

Ordering produces the Ticket; Kitchen Operations produces acknowledgment.

### Which Domain Events support it?

`Kitchen Ticket Created` and, where completed, `Kitchen Ticket Acknowledged`.

### Which uncertainty still exists?

Acknowledgment does not prove preparation start, progress, Ready, Completed,
collection, or delivery. Those meanings remain gated.

### What human decision is still required?

Kitchen decides how to perform confirmed work. Product Owner decisions are
still required before later lifecycle confirmations exist.

### Human explanation

> Kitchen acknowledged K-18 at 09:29. This confirms Kitchen recognized the work;
> BeachOS cannot yet say it is ready or delivered.

## Bar Ticket

### What is true?

The Bar Ticket contains confirmed Bar work, and its current approved state is
awaiting acknowledgment or acknowledged.

### How do we know it?

The accepted Order created Bar-destination work, and authorized Bar Staff may
confirm recognition.

### Who confirmed it?

Ordering confirms creation. Bar Staff confirm acknowledgment.

### When was it confirmed?

At separate creation and acknowledgment times.

### Which Product Decision allows this fact to exist?

DEC-013 approves destination-specific Bar work.

### Which Capability produced it?

Ordering and Bar Operations.

### Which Domain Events support it?

`Bar Ticket Created` and `Bar Ticket Acknowledged` where acknowledgment
succeeded.

### Which uncertainty still exists?

BeachOS does not know whether packaged or prepared items are physically ready,
held, collected, or delivered. Direct Bar handoff remains unresolved.

### What human decision is still required?

Bar decides how to supply its work. Future approved responsibility and handoff
rules must determine later confirmations.

### Human explanation

> Bar acknowledged B-18 at 09:28. This confirms ownership of the Bar work, not
> readiness, collection, or guest delivery.

## Bill

### What is true?

The Customer Group has a running Bill composed of exact, explainable Financial
Obligations and Payments, with a current Balance.

### How do we know it?

The first approved obligation created the Bill. Every Bill Line retains its
business origin, and every valid Payment changes the Balance exactly once.

### Who confirmed it?

The responsible humans who performed the approved originating actions and the
authorized person recording each Payment or future correction.

### When was it confirmed?

Each obligation, Bill Line, Payment, and later status has its own attributable
time.

### Which Product Decision allows this fact to exist?

DEC-009 protects financial truth. DEC-033 creates a Bill only at the first
obligation. DEC-034 governs Beach Sunbed opening charges. DEC-036 aggregates
multiple Orders. DEC-038 governs financial Capabilities.

### Which Capability produced it?

Customer Group Opening, Ordering, Billing, and Payments according to the origin
of each fact.

### Which Domain Events support it?

`Financial Obligation Created`, `Bill Created`, `Bill Line Added`,
`Payment Recorded`, and `Bill Fully Paid` where applicable. Future correction
or closing events apply only after their Commands are approved.

### Which uncertainty still exists?

Zero Balance does not prove Bill closure, fulfilment, departure, or Customer
Group completion. Unapproved corrections and exceptions remain unresolved.

### What human decision is still required?

Authorized humans decide how to resolve disputes, whether approved exceptions
apply, and whether future closing conditions are satisfied.

### Human explanation

> Bill BL-24 totals €54: €20 from the confirmed Beach Sunbed opening and €34
> from Order O-18. No Payment has been confirmed. The total explains what is
> owed; it does not claim that every item was delivered.

## Payment

### What is true?

The business confirmed receipt—or confirmed rejection—of an exact payment
outcome for one Bill.

### How do we know it?

An authorized person confirmed the real payment outcome, exact amount, Payment
Method, Bill, and time. Only confirmed receipt reduces Balance.

### Who confirmed it?

The Staff Member authorized to Record Payments.

### When was it confirmed?

At the recorded receipt or rejection time, not merely when an attempt began.

### Which Product Decision allows this fact to exist?

DEC-009 requires financial integrity. DEC-010 requires auditability for
sensitive actions. DEC-038 separates financial Capabilities from Roles.

### Which Capability produced it?

Payment Recording. Other payment lifecycles remain incomplete.

### Which Domain Events support it?

`Payment Recorded`, `Payment Rejected`, `Bill Fully Paid` where the resulting
Balance is zero, and `Activity Logged` where required.

### Which uncertainty still exists?

An interrupted attempt may be neither confirmed received nor rejected.
Reversal, refund, partial, split, excess, cash-change, and tip behavior remain
unresolved.

### What human decision is still required?

The authorized person must reconcile uncertainty against the real payment
outcome and follow approved recovery practice without duplicating receipt.

### Human explanation

> €54 was recorded by Sofia as received by card at 18:42, reducing BL-24 to
> zero. Zero Balance does not automatically close the Bill or complete CG-24.

## Operational Learning

### What is true?

A confirmed historical pattern deserves human review under an approved
operational objective or standard.

### How do we know it?

Comparable confirmed facts occurred repeatedly with relevant context and known
exceptions visible. A one-time incident is kept distinct from recurrence,
seasonality, drift, or observed improvement.

### Who confirmed it?

Responsible people confirmed the original operational facts. A human reviewer
confirms whether the comparison and proposed lesson are meaningful.

### When was it confirmed?

Each source fact retains its own time. The pattern explanation states the
historical period reviewed and when the review occurred.

### Which Product Decision allows this fact to exist?

The approved Operational Learning framework and the Product Decisions governing
each source fact provide authority. Historical repetition alone creates no new
Product Decision.

### Which Capability produced it?

The original operational capabilities produce the source facts. Operational
Learning produces an explainable recommendation for human review, not a new
operational fact or rule.

### Which Domain Events support it?

The relevant confirmed Domain Events and approved operational history. There is
no generic event that turns a pattern into truth or policy.

### Which uncertainty still exists?

Contexts may differ, evidence may be incomplete, causes may be unknown, and the
pattern may not continue. No prediction or staff judgment is implied.

### What human decision is still required?

The responsible business owner decides whether to investigate, coach, change an
approved habit, or make no change.

### Human explanation

> On four comparable weekend openings this month, Bar changed from NOT READY to
> READY after the planned opening time because ice preparation was incomplete.
> These confirmed declarations justify review. They do not prove the cause or
> authorize a new standard.

## Operational Digital Twin

### What is true?

The current digital view matches the collection of confirmed operational facts
within a named Venue, Business Date, and time—subject to explicitly stated
uncertainty.

### How do we know it?

Every important statement is supported by current evidence, approved business
meaning, responsibility, and a connected history. Known conflicts and stale or
missing confirmations remain visible.

### Who confirmed it?

Different responsible humans and approved business outcomes confirm different
parts. No single person or system claim proves the entire operation.

### When was it confirmed?

Each fact retains its own confirmation time. The twin’s current view must expose
when relevant evidence may no longer be current enough for a decision.

### Which Product Decision allows this fact to exist?

All Product Decisions governing the represented facts, together with the
approved Operational Digital Twin model. The twin has no authority independent
of those sources.

### Which Capability produced it?

Every approved operational capability contributes its own confirmed facts. The
Digital Twin connects them; it does not manufacture another outcome.

### Which Domain Events support it?

The complete relevant Domain Event history, permanent business records,
Activity Logs where required, and explicit non-event current facts such as
approved configuration.

### Which uncertainty still exists?

Unreported physical reality, unapproved concepts, stale confirmations,
conflicting evidence, guest experience, and incomplete capability lifecycles
remain outside confirmed truth.

### What human decision is still required?

The responsible human decides whether the evidence is sufficient for the
current operation and how to reconcile any mismatch with reality.

### Human explanation

> This is the confirmed view of Emerald for 1 August. The Venue is open, CG-24
> is active at Beach A12, its two Tickets are acknowledged, and BL-24 has zero
> Balance. BeachOS still cannot confirm fulfilment, Bill closure, guest
> departure, or Service Location release.

# Mandatory Explainability Principles

## BeachOS never asks users to trust it

Trust is an outcome of consistent, inspectable truth. “Because BeachOS says so”
is never a valid business explanation.

## BeachOS always shows why

Every consequential statement must have an accessible reason appropriate to the
person’s decision. Deeper evidence and governance authority must remain
traceable.

## BeachOS distinguishes confirmed facts from assumptions

Assumptions, expectations, estimates, missing information, and informal
practice must never be presented as completed business facts.

## BeachOS distinguishes historical evidence from current truth

History can explain context and support review. It cannot override the latest
authoritative current fact or prove that a present condition still exists.

## BeachOS never hides uncertainty

Known gaps, conflicts, potentially stale information, and unknown outcomes are
part of the explanation. Removing uncertainty from view does not remove it from
the operation.

## BeachOS explains before it advises

Advice must follow the explanation of current fact, relevant rule, responsibility,
and uncertainty. BeachOS should remain silent when it cannot explain why an
advice statement is responsible.

# Additional Explainability Rules

1. Use official business language and one name per concept.
2. Name the operational scope: Organization, Venue, Business Date, Customer
   Group, Service Location, Ticket, Bill, or Payment.
3. Separate the current fact from its complete history.
4. Preserve superseded evidence without presenting it as current.
5. Distinguish the actor, responsible owner, authorizing Capability, and affected
   person.
6. Explain what an event proves and what it does not prove.
7. Never use a Role title as proof of Capability or current responsibility.
8. Never use a technical success as proof of a business outcome.
9. Explain rejected and uncertain outcomes as carefully as successes.
10. Make financial origins and effects exact and permanent.
11. Keep explanations proportionate to operational pressure.
12. Offer deeper evidence without forcing every person to read an audit history.
13. Protect privacy and avoid unnecessary personal detail.
14. Use accountability to support continuity and recovery, not punishment.
15. Explain corrections by preserving the original fact and the approved later
    change.
16. State when no approved Product Decision or Domain Event exists.
17. Keep the human decision and responsible person visible.
18. Ensure an explanation survives changes in technology.

# Explainability Under Uncertainty

When an outcome may have succeeded but cannot be confirmed, BeachOS should
explain:

- the intended action;
- the last confirmed state;
- why the outcome is unknown;
- which consequences must not be repeated blindly;
- which current facts must be recovered;
- who is responsible for reconciliation;
- what BeachOS will not claim until reconciliation is complete.

An uncertain outcome is not a failure, success, or empty state. It is an
operational fact about the limits of current knowledge.

# Explainability and Operational Advice

An advice statement is explainable only when BeachOS can show:

1. the decision being supported;
2. the current facts;
3. the approved rule or objective;
4. the responsible human;
5. the relevant attention or Blocker;
6. the remaining uncertainty;
7. why the proposed next step is safe and useful;
8. why the final decision remains human.

Operational Learning adds historical context only after current truth. A
recommendation based on history must name the comparable facts, period,
exceptions, and approved objective. It must never imply a hidden cause,
prediction, score, or automatic policy.

# The Explainability Contract

Every future BeachOS capability must satisfy this contract before it can be
considered complete.

## 1. Fact contract

The capability defines every important Operational Fact it may produce in
official business language, including what each fact does and does not mean.

## 2. Authority contract

Every fact identifies the Product Decision, approved business rule, Domain
concept, and Capability that authorize its existence.

## 3. Evidence contract

Every fact identifies the minimum supporting evidence, its scope, its current or
historical character, and the evidence that would contradict or supersede it.

## 4. Responsibility contract

Every consequential fact identifies who confirms it, who owns the current
responsibility, whether acceptance is required, and who owns the next human
decision.

## 5. Time contract

Every time-sensitive fact identifies when it was confirmed, the relevant
Business Date, and when it may no longer be current enough for its intended
decision.

## 6. Event contract

Every completed business outcome identifies its supporting Domain Events and
required Activity Logs. A capability must explicitly state when a current fact
is not a Domain Event.

## 7. Uncertainty contract

The capability defines missing, stale, conflicting, rejected, and unknown
outcomes. It states what BeachOS must not infer in each case and how responsible
humans can re-establish current truth.

## 8. Human explanation contract

The capability supplies calm, non-technical explanations for success,
rejection, Blockers, and uncertainty. Each explanation states the reason before
advice or action.

## 9. History contract

The capability preserves the explanation of important changes, corrections,
responsibility transfers, and financial effects without silently rewriting the
original fact.

## 10. Learning contract

If historical facts may influence review, the capability defines the approved
objective, comparable context, known exceptions, and human review authority.
History never creates a rule or current fact by repetition.

## 11. Privacy and accountability contract

The capability uses only the personal and historical detail required for an
approved operational purpose. Explainability must not become surveillance.

## 12. Completion test

Before approval, a Product Owner, operator, designer, developer, tester, or AI
agent must be able to select any important statement from the capability and
answer, without guessing:

- What is true?
- How do we know it?
- Who confirmed it?
- When was it confirmed?
- Which Product Decision allows it?
- Which Capability produced it?
- Which Domain Events support it?
- Which uncertainty remains?
- What human decision is still required?

If any answer is hidden, inferred, contradictory, or unavailable, the
capability is not explainably complete and must not present the fact as trusted
operational truth.
