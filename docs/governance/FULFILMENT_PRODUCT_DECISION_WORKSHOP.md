# Fulfilment Product Decision Workshop

## Purpose

This workshop prepares the Product Owner decisions required to define the
business meaning of `Ticket Ready`, `Ticket Completed`, and `Item Delivered`.

It does not approve an answer. It does not modify the Domain, create an event,
or authorize implementation. Every option and question below remains open until
the Product Owner records an approved Product Decision.

## Current Approved Boundary

BeachOS currently knows these confirmed facts:

- a submitted Order may create one Kitchen Ticket and one Bar Ticket;
- each Ticket contains only work for its named department;
- Kitchen and Bar acknowledgement means that the department has recognized its
  Ticket as active work;
- acknowledgement does not mean ready, completed, handed over, or delivered;
- Kitchen and Bar remain separate business capabilities;
- original submission context remains history while the current Service
  Location must remain discoverable;
- humans decide, and BeachOS must not manufacture certainty from elapsed time;
- `Kitchen Ticket Ready`, `Bar Ticket Ready`, `Kitchen Ticket Completed`, and
  `Bar Ticket Completed` are recognized names, but their Commands are gated;
- `Item Delivered` is not an approved Domain Event or current Domain rule.

The repository does not approve preparation priority, partial readiness,
department handoff, Runner responsibility, delivery confirmation, or the effect
of cancellation, correction, transfer, and unavailable items on fulfilment.

## Workshop Method

For every proposed meaning, the Product Owner should identify:

1. the observable real-world fact;
2. the human who is responsible for confirming it;
3. the responsibility that begins and ends;
4. the next permitted business action;
5. the exceptions that prevent the fact from being true;
6. whether the fact applies to a whole Ticket or individual items;
7. what BeachOS may say with confidence after confirmation.

The workshop must avoid choosing interface controls, database structures, API
shapes, notifications, or automation.

# 1. Ticket Ready

## Current language

The event catalogue currently describes Kitchen or Bar Ticket Ready as the
department declaring that approved Ticket work is ready for the next service
step. The exact readiness meaning and partial-readiness rules are unresolved.

## Kitchen

### Who performs it?

Unresolved. The existing catalogue points to authorized Kitchen Staff, but it
does not decide whether any Kitchen Staff Member, the person preparing the work,
a station lead, or a Kitchen lead may confirm readiness.

### What business fact becomes true?

Only the broad statement “Kitchen work is ready for the next service step” is
currently recognized. The next step, required condition, and scope of “work”
are not defined.

Possible meanings requiring a Product Owner choice include:

- every Kitchen item on the Ticket is physically ready to leave Kitchen;
- one approved subset is ready while the Ticket remains partly outstanding;
- Kitchen has finished preparation but a final quality or handoff check remains;
- the work has been placed at an agreed collection point.

None of these meanings is approved today.

### What responsibility begins?

Unresolved. Possible new responsibility could belong to a Runner, Responsible
Service Staff, or a department handoff role. The current repository does not
assign it.

### What responsibility ends?

Unresolved. Readiness may end preparation responsibility, may retain Kitchen
responsibility until collection, or may create shared responsibility during
handoff.

### What can happen next?

Undecided. Candidate next actions are collection, explicit handoff, delivery,
continued waiting, or correction of the readiness declaration.

### What cannot happen yet?

BeachOS cannot claim collection, delivery, Ticket completion, or an ended
Kitchen responsibility merely because readiness was declared.

## Bar

### Who performs it?

Unresolved. The catalogue points to authorized Bar Staff but does not decide
whether readiness is confirmed by the person supplying the item, any Bar Staff
Member, a station lead, or a Bar lead.

### What business fact becomes true?

Only the broad statement “Bar work is ready for the next service step” is
recognized. The meaning may differ for prepared drinks, packaged drinks, and
items handed directly to Responsible Service Staff, but no distinction is
approved.

### What responsibility begins?

Unresolved. Runner or Responsible Service Staff responsibility might begin, or
Bar responsibility might continue until physical handoff.

### What responsibility ends?

Unresolved. Ready may or may not end the Bar’s active preparation or custody
responsibility.

### What can happen next?

Undecided. Collection, handoff, direct delivery, or continued holding are
possible operational paths requiring approval.

### What cannot happen yet?

BeachOS cannot treat Bar readiness as collection, delivery, or completion. It
cannot assume the same physical handoff used by Kitchen.

## Runner

### Who performs it?

The Runner role and its authority are not yet formally defined for this
workflow. The Product Owner must decide whether Runner is a Role, a temporary
operational responsibility, or not required.

### What business fact becomes true?

Ticket Ready is not currently a Runner fact. It may become the condition that
makes work available for collection, but that relationship is unapproved.

### What responsibility begins?

Unresolved. Possible responsibility is to collect the correct work and preserve
its correct Customer Group and current Service Location context.

### What responsibility ends?

Not applicable until Runner responsibility is approved. A future decision must
also define whether responsibility ends at handoff to service staff or delivery
to guests.

### What can happen next?

No Runner action is approved from Ticket Ready today.

### What cannot happen yet?

BeachOS cannot assign, notify, time, judge, or hold a Runner accountable.

## Responsible Service Staff

### Who performs it?

The existing Responsible Service Staff attached to the Customer Group is known,
but their role in accepting ready work is unresolved.

### What business fact becomes true?

No additional fact about Responsible Service Staff becomes true merely because
a department declares a Ticket Ready.

### What responsibility begins?

Unresolved. The Product Owner must decide whether readiness creates collection,
guest communication, or delivery responsibility for Responsible Service Staff.

### What responsibility ends?

None is approved to end at readiness.

### What can happen next?

Only human coordination under current venue practice. BeachOS cannot prescribe
the next operational action yet.

### What cannot happen yet?

The system cannot state that Responsible Service Staff accepted the work or
that the guest was served.

# 2. Ticket Completed

## Current language

The event catalogue says completion ends the named department’s responsibility
for the Ticket under an approved workflow. The required workflow and completion
conditions do not yet exist.

## Kitchen

### Who performs it?

Unresolved. The catalogue indicates authorized Kitchen Staff, but authority and
whether another human must first accept handoff are undecided.

### What business fact becomes true?

The only recognized meaning is that Kitchen no longer owns outstanding work for
the Ticket. It is unknown whether this means preparation finished, work was
collected, custody transferred, or all items were delivered.

### What responsibility begins?

Unresolved. Completion may begin Runner or Responsible Service Staff
responsibility, or it may occur only after that responsibility has already
begun.

### What responsibility ends?

Kitchen responsibility ends, but the exact boundary and treatment of
exceptions, missing items, remakes, and rejected handoffs require approval.

### What can happen next?

Unresolved. Potential next facts include handoff, transit, delivery, remake, or
no further preparation action.

### What cannot happen yet?

Completion cannot prove delivery, guest acceptance, complete fulfilment of the
Order, or eligibility to close the Bill or Customer Group.

## Bar

### Who performs it?

Unresolved. Authorized Bar Staff are the current event’s intended actors, but
the required handoff confirmation is unknown.

### What business fact becomes true?

Bar no longer owns outstanding work for the Ticket. Whether packaged and
prepared items complete at the same moment is undecided.

### What responsibility begins?

Unresolved. It may transfer to Runner or Responsible Service Staff, or may
already have transferred through a separate future handoff fact.

### What responsibility ends?

Bar responsibility ends only under conditions still requiring approval.

### What can happen next?

Collection, transit, delivery, or exception handling may follow, but none is an
approved automatic consequence.

### What cannot happen yet?

BeachOS cannot infer that completed Bar work reached the guests or that every
Bar item in the Order was fulfilled.

## Runner

### Who performs it?

Unresolved. Ticket Completed is currently a department event, not a Runner
action.

### What business fact becomes true?

No Runner fact is currently created. If completion represents physical
collection, this would introduce Runner meaning that requires an explicit
Product Decision.

### What responsibility begins?

Unresolved. Possible custody responsibility cannot be assumed.

### What responsibility ends?

No approved Runner responsibility can end through Ticket completion.

### What can happen next?

Nothing prescribed by BeachOS until handoff and delivery responsibilities are
approved.

### What cannot happen yet?

BeachOS cannot use Ticket completion to prove Runner collection, custody, or
delivery performance.

## Responsible Service Staff

### Who performs it?

Responsible Service Staff do not currently complete Kitchen or Bar Tickets.
Whether they must accept a department handoff is unresolved.

### What business fact becomes true?

No accepted-service or delivered-service fact exists merely because the
department completes its Ticket.

### What responsibility begins?

Unresolved. Delivery or guest follow-up responsibility may begin, but must be
defined separately.

### What responsibility ends?

No current Responsible Service Staff responsibility ends at Ticket completion.

### What can happen next?

Human coordination can continue, but BeachOS cannot declare the approved next
step.

### What cannot happen yet?

The Bill, Customer Group, and Service Location cannot be closed or released on
the strength of Ticket completion alone.

# 3. Item Delivered

## Current language

`Item Delivered` is not an approved Domain Event and is not supported by the
current Domain Model. This section identifies decisions required before the
Product Owner decides whether it should become a business fact at all.

## Kitchen

### Who performs it?

Unresolved. Kitchen might never perform delivery, or direct Kitchen delivery
might exist in some venues.

### What business fact becomes true?

Undecided. Possible meanings include physical placement at the correct Service
Location, handoff to one guest, or confirmation that the Customer Group
received the item.

### What responsibility begins?

Potential guest follow-up responsibility is undefined.

### What responsibility ends?

Kitchen responsibility may already have ended or may end only at delivery. This
must not be inferred.

### What can happen next?

Guest consumption, correction, replacement, complaint, or further service are
possible, but no system consequence is approved.

### What cannot happen yet?

Delivery cannot be recorded, inferred, or used to judge Kitchen performance.

## Bar

### Who performs it?

Unresolved. Bar Staff may hand directly to guests or another responsible human,
depending on venue practice.

### What business fact becomes true?

No official meaning exists. Direct counter service and delivery to a distant
Service Location may require different operational facts.

### What responsibility begins?

Unresolved.

### What responsibility ends?

Bar responsibility might end at handoff or delivery; neither boundary is
approved.

### What can happen next?

No automatic operational or financial action is approved.

### What cannot happen yet?

BeachOS cannot equate Bar completion with Item Delivered.

## Runner

### Who performs it?

Unresolved. Runner is a likely candidate only if the Product Owner formally
defines the responsibility and required Capability.

### What business fact becomes true?

The meaning of “delivered” must be chosen: arrival at the Service Location,
physical handoff, confirmation by Responsible Service Staff, or receipt by the
guest are distinct facts.

### What responsibility begins?

Possible exception or return responsibility after a refused or incorrect
delivery is undefined.

### What responsibility ends?

Runner custody might end, but only after the delivery boundary is approved.

### What can happen next?

No approved system action follows.

### What cannot happen yet?

BeachOS cannot assign delivery responsibility, measure delivery time, or infer
delivery from movement, proximity, or Ticket status.

## Responsible Service Staff

### Who performs it?

Unresolved. Responsible Service Staff may deliver, accept a Runner handoff, or
only remain accountable for the wider Customer Group relationship.

### What business fact becomes true?

No official delivered fact exists. The Product Owner must decide whether the
confirmation applies per item, quantity, Ticket, Order Round, or whole Order.

### What responsibility begins?

Possible confirmation of correctness and guest follow-up is unresolved.

### What responsibility ends?

Delivery does not automatically end overall responsibility for the Customer
Group. Any narrower delivery responsibility must be defined.

### What can happen next?

Ongoing service and later Order Rounds remain possible. Corrections, rejected
items, and service recovery need separate approved rules.

### What cannot happen yet?

Delivery cannot automatically close a Ticket, Bill, Customer Group, or Service
Location, and it cannot create or remove a financial obligation without another
approved rule.

# Cross-Cutting Ambiguities

- Whole-Ticket versus item-level or quantity-level state.
- Whether Kitchen and Bar use identical readiness and completion meanings.
- Whether Ready means preparation finished, collection possible, or handoff
  available.
- Whether Completed occurs before, during, or after physical handoff.
- Whether direct Bar supply needs a different path from prepared drinks.
- Whether a Runner is always, optionally, or never involved.
- Whether Responsible Service Staff must accept transferred responsibility.
- Whether custody and accountability can be shared during handoff.
- Current Service Location changes while work is preparing or in transit.
- Missing, unavailable, substituted, remade, cancelled, corrected, or refused
  items.
- Partial quantities and mixed readiness within one Ticket.
- Multiple Tickets from different Order Rounds ready at different times.
- Whether a Ticket may return from Ready to active work, and how correction is
  preserved without rewriting history.
- What happens after an uncertain command outcome.
- Whether readiness or completion requires an Activity Log in ordinary cases.
- Whether any timestamps become service measures and, if so, how they avoid
  punitive interpretation.
- Offline continuity and reconciliation for consequential confirmations.
- Relationship among completion, delivery, financial obligations, Bill
  closing, Customer Group completion, and Service Location release.

# Product Owner Decision Agenda

The following questions require numbered, explicit answers before
implementation:

1. What exact real-world condition makes a Kitchen Ticket Ready?
2. What exact real-world condition makes a Bar Ticket Ready?
3. May part of a Ticket become Ready, or only the entire Ticket?
4. If partial readiness is allowed, does it apply by item or by quantity?
5. Who may declare Kitchen Ticket Ready?
6. Who may declare Bar Ticket Ready?
7. Does Ready end any department responsibility? If yes, exactly which one?
8. Who becomes responsible when a Ticket becomes Ready?
9. Must another human accept the handoff before responsibility changes?
10. What exact real-world condition completes a Kitchen Ticket?
11. What exact real-world condition completes a Bar Ticket?
12. Who may complete each Ticket?
13. Can a Ticket be Completed before its work is physically collected?
14. Can a Ticket be Completed before its items reach the guests?
15. Can a Ready or Completed Ticket return to active work? Under what business
    reason and authority?
16. Is Runner an official Role, a temporary responsibility, or outside the
    first fulfilment workflow?
17. When does Runner responsibility begin and end?
18. What does Responsible Service Staff own after a Ticket becomes Ready?
19. Must Responsible Service Staff confirm collection, handoff, or delivery?
20. Should `Item Delivered` become an official business event?
21. If yes, what exact real-world fact does `Item Delivered` mean?
22. Who may confirm Item Delivered?
23. Is delivery recorded by item, quantity, Ticket, or Order Round?
24. How is direct Bar handoff different from Runner delivery, if at all?
25. What happens when the Customer Group moves before collection or delivery?
26. What happens when an item is missing, refused, incorrect, remade,
    unavailable, cancelled, or corrected?
27. Which ordinary transitions need Activity Logs in addition to Domain Events?
28. What must BeachOS communicate after an uncertain Ready, Completed, or
    Delivered attempt?
29. May any fulfilment state affect a Bill, Customer Group completion, or
    Service Location release? If yes, under which separately approved rule?
30. Must Kitchen and Bar share one lifecycle, or may their approved meanings
    differ?

# Required Decision Records

At minimum, implementation requires approved Product Decision Records for:

1. Kitchen Ticket Ready meaning and authority.
2. Bar Ticket Ready meaning and authority.
3. Kitchen Ticket Completed meaning and authority.
4. Bar Ticket Completed meaning and authority.
5. Handoff and responsibility transfer among Kitchen, Bar, Runner, and
   Responsible Service Staff.
6. Partial readiness and partial fulfilment, including quantities.
7. Delivery meaning, authority, and whether `Item Delivered` becomes an official
   Domain Event.
8. Exception and recovery behavior during fulfilment.

Only after approval should the Domain Model, Domain Events, Customer Journey,
First Operational Day, requirements, and capability documents be reviewed for
consistent updates before implementation begins.

# Workshop Exit Criteria

The workshop is complete only when every proposed event has:

- one observable and non-overlapping business meaning;
- one named responsible human or explicit authority rule;
- clear whole-Ticket, item, and quantity scope;
- explicit entry and exit conditions;
- explicit responsibility transfer;
- defined exception and uncertainty treatment;
- clear statements of what the event does not imply;
- an approved Product Decision Record.

Until then, the current acknowledgement-only model remains the authoritative
and safe product boundary.
