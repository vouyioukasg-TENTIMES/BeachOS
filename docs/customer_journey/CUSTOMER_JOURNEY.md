# BeachOS Customer Journey

## Purpose and authority

This document describes the complete operational journey from the moment a guest
party enters the Venue until the guests physically depart and the operation has a
safe, truthful understanding of what remains.

It is governed by:

- the BeachOS Operational Intelligence Framework;
- the approved Guest Arrival Capability;
- the Domain Model;
- the Domain Events catalogue;
- the Customer Group Lifecycle;
- the Decision Log;
- the Project Glossary;
- approved operational workflows and product requirements.

It does not define software, screens, interfaces, storage, or new business rules.
Where the repository has not yet approved a rule, actor, condition, or sequence,
the uncertainty is stated explicitly.

## Journey boundaries

Before the Responsible Waiter intentionally opens official service, the people
are an **arriving guest party**. They are not yet an active Customer Group.

After opening, the **Customer Group** is the primary operational entity. It owns
the Service Location, Responsible Waiter, Orders, optional Bill, Payments through
that Bill, and History until completion.

The accepted Customer Group lifecycle contains only:

1. **Active**
2. **Completed**

Ordering, preparation, transfer, handover, Payment, and a fully paid Bill are
conditions or workflows within Active service. They do not create new Customer
Group lifecycle states.

Physical guest departure does not automatically complete the Customer Group.
Payment, zero Balance, or Bill closing also does not automatically complete it.
The exact completion conditions, authority, sequence, and Service Location
release relationship remain unresolved Product Owner decisions.

## Journey reasoning

At every stage, BeachOS should ask:

1. What decision is the responsible person trying to make?
2. What current facts are required?
3. Is the operation ready?
4. Is BeachOS confident enough to advise?
5. What deserves attention?
6. What safe human action follows?
7. Is the outcome confirmed, rejected, or uncertain?

# Stage 1 — Guest Arrival

## Purpose

Ensure the arriving party is noticed and enters a clear hospitality process
without creating an operational or financial commitment.

## Primary Decision

Can the Venue begin normal arrival for this party, and who is taking human
responsibility for welcoming them?

## Responsible Human

The Host or approved arrival responsibility.

The act of noticing and acknowledging the guests remains human. BeachOS has no
approved automatic arrival-detection capability.

## Operational Readiness

- The Venue is officially open for the current Business Date.
- Guest arrivals are permitted.
- A Host or approved arrival responsibility is present.
- Manual operational continuity is available if current BeachOS context cannot
  be used.

The Host may still welcome guests respectfully when normal arrival is not ready,
but must not proceed into normal seating or Customer Group opening.

## Operational Confidence

BeachOS can advise confidently only when the Venue, Business Date, and official
opening state are current and confirmed.

BeachOS must remain uncertain when opening state, arrival responsibility, or the
current Venue context cannot be confirmed.

## Attention

- **Immediate action:** Guests are entering before the Venue is officially open.
- **Action required:** No Host has clear ownership of the arriving party.
- **Monitor:** The Host is welcoming the party normally and no conflict is
  present.

No greeting-time threshold or automatic arrival alert is approved.

## Advice

BeachOS may confirm whether normal arrival may proceed and identify missing
operational readiness.

BeachOS must not decide how to greet the party, infer why they arrived, or
present an unseen arrival as a confirmed fact.

## Human Decision

The Host decides how to acknowledge the guests, take clear ownership, and begin
the conversation.

## Outcome

- The party is welcomed and proceeds to needs assessment.
- Normal arrival pauses because the Venue is not ready.
- The party leaves before the arrival conversation continues.
- Arrival responsibility remains uncertain and requires human coordination.

# Stage 2 — Welcome and Needs Understanding

## Purpose

Understand the minimum practical information needed to provide appropriate
hospitality without making assumptions or collecting unnecessary personal
information.

## Primary Decision

What does this party need from the Venue right now, and which needs are
requirements rather than preferences?

## Responsible Human

The Host.

## Operational Readiness

- The party has been acknowledged.
- The Host has clear ownership of the conversation.
- The Host can communicate sufficiently to understand party size and immediate
  practical needs.
- Approved Venue constraints can be consulted where relevant.

## Operational Confidence

Confidence comes from what the guests say, what the Host observes directly, and
approved facts about the Venue.

BeachOS must remain uncertain about needs that have not been stated or confirmed.
It must not infer accessibility needs, family requirements, preferences, status,
or identity from appearance or familiarity.

## Attention

- **Immediate action:** A stated safety or accessibility need cannot be
  understood or safely addressed.
- **Action required:** Language, capacity, or exception questions require help
  from an appropriate colleague or Manager.
- **Monitor:** Ordinary preferences that can be considered during availability
  review.

## Advice

BeachOS may provide approved facts about Service Location types, Areas, and known
Venue constraints.

BeachOS should remain silent about personal suitability when the necessary human
conversation has not happened. It must not rank or profile guests.

## Human Decision

The Host decides what to ask, how to listen, what to clarify, and when to seek
help.

## Outcome

- The Host understands enough to review suitable availability.
- Essential needs remain unclear and the conversation continues.
- The Host escalates an exception or safety question.
- The guests choose not to continue.

# Stage 3 — Availability, Waiting, or Seating Choice

## Purpose

Offer only suitable Service Locations whose current availability can be trusted,
or provide an honest manual waiting path when no suitable location is available.

## Primary Decision

Can the Host offer a suitable, currently available Service Location, or should
the party wait, consider another option, or leave?

## Responsible Human

The Host. A Manager supports unresolved exceptions, conflict, safety, and
unapproved priority requests.

## Operational Readiness

A Service Location is ready to be offered when:

- its identity and current availability are confirmed;
- it is not occupied, unavailable, or retired;
- its physical condition does not conflict with the current operational state;
- the Host judges it suitable from direct observation and the guests’ stated
  needs;
- no approved rule prevents its use.

Waiting remains a manual operational process. No digital waiting lifecycle,
priority rule, reservation relationship, or queue order is approved.

## Operational Confidence

Confidence requires agreement between current central operational truth and the
physical situation.

BeachOS must remain uncertain when:

- availability may be stale;
- the physical and operational states conflict;
- another party may be using the same location;
- capacity or accessibility suitability is unclear;
- waiting order, reservation status, or exception authority is unclear.

## Attention

- **Immediate action:** Two parties are being directed to one Service Location,
  or physical occupancy conflicts with the current state.
- **Action required:** No suitable location is available, the guests need a
  waiting update, or an exception requires Manager judgment.
- **Monitor:** A suitable location remains available while the party considers
  it.

## Advice

BeachOS may identify confirmed available and unavailable Service Locations and
explain known reasons.

It must not:

- promise a waiting time;
- create an unofficial reservation;
- choose priority between parties;
- infer VIP entitlement;
- call a location “best” without approved facts and human judgment.

## Human Decision

The Host decides which suitable options to present. The guests decide whether to
accept, wait through the approved manual process, consider another option, or
leave.

## Outcome

- The guests accept a confirmed Service Location.
- The guests enter manual waiting.
- The guests choose another suitable option.
- The guests leave.
- The decision pauses because availability or suitability cannot be confirmed.

# Stage 4 — Escort and Service Location Identification

## Purpose

Bring the guests to the accepted physical location and confirm that it resolves
to the correct enduring Service Location and current operational context.

## Primary Decision

Are the guests at the correct, still-available Service Location?

## Responsible Human

The Host.

## Operational Readiness

- The guests accepted the location.
- The location remains confirmed available.
- The Host knows the correct physical destination.
- The physical route appears safe and practical through human observation.
- NFC or manual lookup can resolve the Service Location Digital Identity.

## Operational Confidence

Confidence requires agreement among:

- the visible location name or number;
- the Service Location Digital Identity;
- the current operational state;
- the physical condition.

NFC success identifies the location only. It does not establish availability,
suitability, authority, or permission to open a Customer Group.

## Attention

- **Immediate action:** The identity resolves to the wrong location, the location
  becomes occupied or unavailable, or the physical condition is unsafe.
- **Action required:** NFC fails and manual lookup is needed.
- **Monitor:** The accepted location remains available during escort.

## Advice

BeachOS may advise manual lookup when NFC fails and may explain a confirmed
location-state change.

BeachOS must not advise the Host to guess, continue despite a mismatch, or treat
identification as an operational action.

## Human Decision

The Host decides whether the escort remains safe, whether the physical context
matches, and whether to continue, reassess availability, or explain a change to
the guests.

## Outcome

- The guests reach the correct identified Service Location.
- The Host returns to availability review because the location changed.
- Identity remains uncertain and the journey pauses.
- The guests change their mind before official service begins.

No Customer Group transfer exists at this stage because no Customer Group has
opened.

# Stage 5 — Service Handoff and Customer Group Opening

## Purpose

Establish exactly one accountable Responsible Waiter and intentionally begin
official service at the correct Service Location.

## Primary Decision

Can the Responsible Waiter safely and intentionally open the Customer Group?

## Responsible Human

The Host coordinates the handoff.

The eligible Responsible Waiter accepts responsibility and alone decides whether
to perform the official Customer Group opening while holding the required
Capability.

## Operational Readiness

- The Venue remains officially open.
- The party is at the correct identified Service Location.
- The Service Location remains available.
- No active Customer Group already occupies it.
- One eligible Responsible Waiter accepts responsibility.
- The Responsible Waiter holds Open Customer Group.
- The approved Beach Sunbed Financial Obligation can be confirmed where
  applicable.
- The complete opening outcome can be confirmed safely.

## Operational Confidence

Confidence requires current agreement about the party, Service Location,
availability, Responsible Waiter, Capability, and any immediate Beach Sunbed
obligation.

BeachOS must remain uncertain when an opening may have completed but its outcome
cannot be confirmed.

## Attention

- **Immediate action:** Duplicate occupancy, wrong location, unauthorized actor,
  unavailable location, or uncertain opening outcome.
- **Action required:** No eligible Responsible Waiter has accepted the handoff.
- **Monitor:** A clear handoff is progressing normally.

## Advice

BeachOS may explain the approved opening consequences and identify a missing
condition.

BeachOS must not:

- open the Customer Group automatically;
- let the Host open it;
- treat Role alone as authority;
- repeat an opening while its outcome is uncertain;
- create a Bill unless an approved Financial Obligation exists.

## Human Decision

The Host decides how to complete the hospitality handoff. The Responsible Waiter
decides whether to accept responsibility and intentionally open the Customer
Group.

## Outcome

- Exactly one active Customer Group opens with one Responsible Waiter.
- At a Beach Sunbed, the approved Financial Obligation, Bill, and Bill Line arise
  as part of the same complete outcome.
- At another Service Location type, the Customer Group may open without a Bill.
- Opening is rejected and no Customer Group opens.
- Opening remains uncertain and must be reconciled before repetition.

# Stage 6 — Active Service and Guest Care

## Purpose

Maintain one clear operational context for the party while service continues.

## Primary Decision

What does this active Customer Group need next, and who is accountable for
coordinating it?

## Responsible Human

The Responsible Waiter is the one Staff Member accountable for coordinating
service for the active Customer Group.

Other authorized Staff Members may perform approved work. The exact boundary
between Responsible Waiter coordination and other service responsibilities is
not fully defined beyond accepted actions.

## Operational Readiness

- The Customer Group is Active.
- It occupies exactly one Service Location.
- It has exactly one Responsible Waiter.
- Current Service Location and responsibility can be confirmed.
- Any action follows its Capability and business rules.

## Operational Confidence

Confidence requires the current physical operation to match the Customer Group,
Service Location, and Responsible Waiter context.

BeachOS must remain uncertain when responsibility, location, an earlier action,
or the party’s current need cannot be confirmed.

## Attention

- **Immediate action:** The physical party and active Customer Group context do
  not match, or the Customer Group has no clear Responsible Waiter.
- **Action required:** A guest request, delay, complaint, transfer need, or
  responsibility change needs human coordination.
- **Monitor:** Ordinary ongoing service with clear responsibility.

No complaint, incident, request, or service-delivery lifecycle is currently
approved. BeachOS must not invent one.

## Advice

BeachOS may show confirmed current context and direct the responsible person
toward approved work.

It should remain silent about ordinary hospitality choices that require direct
observation, conversation, or empathy. It must not score staff or infer guest
satisfaction.

## Human Decision

The Responsible Waiter decides how to coordinate ordinary service within
approved rules. Guests decide what to request and whether their needs have been
understood.

## Outcome

- Active service continues.
- The Customer Group begins an Order Round.
- A transfer or Responsible Waiter handover is considered.
- A guest concern requires human escalation.
- Service context becomes uncertain and consequential actions pause.

# Stage 7 — Order Round

## Purpose

Turn a reviewed guest request into one safely accepted and preserved Order Round
without changing earlier Orders.

## Primary Decision

Can this reviewed collection of Order Items be safely submitted as one Order for
the active Customer Group?

## Responsible Human

The Responsible Waiter or another Staff Member authorized to submit the Order
under applicable business rules.

The exact limits on which other Staff Members may submit for the Customer Group
require capability-specific design.

## Operational Readiness

- The Customer Group is Active.
- The correct Customer Group, Service Location, and responsible service context
  are confirmed.
- Each requested Menu Item is available in the applicable Menu and Venue
  context.
- Quantity, price, preparation destination, and approved instructions are
  reviewed.
- The acting Staff Member has the required Capability.
- The submission can be accepted as one complete outcome.

## Operational Confidence

Confidence requires the reviewed request to match the guest’s intention and the
current approved Menu context.

BeachOS must remain uncertain when submission may have completed but its outcome
is unknown. A repeated attempt must not create a duplicate Order.

## Attention

- **Immediate action:** Submission outcome is uncertain, the Customer Group is no
  longer Active, or the wrong Customer Group or Service Location is selected.
- **Action required:** An item is unavailable, required information is missing,
  or the request needs clarification.
- **Monitor:** A reviewed draft is being prepared and has no financial or
  preparation effect yet.

## Advice

BeachOS may identify unavailable items, missing required information, destination
meaning, and the consequence of submission.

It must not invent an Order from conversation, treat a draft as submitted,
silently change an earlier Order, or encourage duplicate submission.

## Human Decision

The guests decide what to request. The authorized Staff Member reviews the
request and intentionally submits it.

## Outcome

- One Order is submitted as one preserved Order Round.
- Zero or one Kitchen Ticket and zero or one Bar Ticket are created according to
  the approved destinations.
- Approved Financial Obligations and Bill Lines arise.
- If this is the first Financial Obligation, the Bill is created.
- Submission is rejected with no confirmed preparation or financial effect.
- Submission outcome remains uncertain and must be reconciled.

The Customer Group remains Active. Later requests become new Orders rather than
updates to the earlier Order.

# Stage 8 — Bar and Kitchen Preparation

## Purpose

Allow each preparation department to understand and progress only the confirmed
work for which it is responsible.

## Primary Decision

For each department: what confirmed preparation work requires attention next?

## Responsible Human

Kitchen Staff are responsible for Kitchen Ticket work.

Bar Staff are responsible for Bar Ticket work.

The exact assignment within each department, partial preparation, runner, and
delivery responsibilities are unresolved.

## Operational Readiness

- A confirmed Order created the relevant Kitchen Ticket or Bar Ticket.
- The Ticket contains only items for that preparation destination.
- The originating Order, Customer Group, and service context remain clear.
- The department can confirm the approved next preparation status.

Exact meanings for acknowledgement, ready, completion, partial readiness, and
delivery still require Product Owner approval.

## Operational Confidence

Confidence requires each Ticket to match the accepted Order and the department’s
responsibility.

BeachOS must remain uncertain when:

- the Ticket and Order conflict;
- the Customer Group has transferred and current delivery context is unclear;
- preparation status meaning is not approved;
- completion or delivery has not been confirmed by the responsible people.

## Attention

- **Immediate action:** Preparation work conflicts with the accepted Order, or a
  consequential correction is uncertain.
- **Action required:** A known Blocker, delay, unavailable item, or changed
  delivery context requires coordination.
- **Monitor:** Confirmed work is progressing normally.

No approved delay thresholds or preparation priority rules exist in the current
repository.

## Advice

BeachOS may separate Bar and Kitchen responsibility, preserve the connection to
the Order, and state confirmed preparation facts.

It must not invent preparation priority, declare work ready through elapsed time,
or judge staff performance.

## Human Decision

Bar and Kitchen Staff decide how to perform and confirm their approved
preparation responsibilities. Service staff coordinate with guests and
departments through approved human practice.

## Outcome

- Kitchen or Bar acknowledges, readies, or completes its Ticket under the
  approved event catalogue.
- Preparation remains in progress.
- A Blocker or delay requires coordination.
- A correction or cancellation follows its separately approved rules.
- Preparation or delivery meaning remains uncertain.

There is no approved `Item Delivered` business event. This journey must not
pretend that preparation completion proves guest delivery.

# Stage 9 — Ongoing Service, Additional Rounds, Transfer, or Handover

## Purpose

Preserve one continuous Customer Group while its needs, Service Location, Orders,
or Responsible Waiter change during service.

## Primary Decision

Can the Customer Group continue safely in its current context, or is another
Order Round, transfer, handover, or escalation required?

## Responsible Human

The Responsible Waiter coordinates service.

Authorized Staff Members may perform approved transfer or responsibility-change
actions. Exact transfer combinations, handover acceptance, authority, and
charging effects remain unresolved.

## Operational Readiness

- The Customer Group remains Active.
- Its current Service Location and Responsible Waiter are clear.
- New Order Rounds meet the Order-stage readiness conditions.
- A transfer destination is confirmed available before transfer.
- A responsibility change preserves exactly one eligible Responsible Waiter.
- Each protected action satisfies the required Capability and approved rule.

## Operational Confidence

Confidence requires one authoritative current Customer Group identity across all
changes.

BeachOS must remain uncertain when:

- transfer outcome is unknown;
- source or destination availability conflicts;
- responsibility acceptance is unclear;
- the financial effect of a move between differently priced Physical Rows or
  into a Beach Sunbed is unresolved;
- current delivery location cannot be established for existing preparation
  work.

## Attention

- **Immediate action:** Transfer outcome is uncertain, duplicate occupancy is
  possible, or the Customer Group could be left without one Responsible Waiter.
- **Action required:** Guests request a move, another Order Round, or a
  responsibility handover.
- **Monitor:** Active service continues normally at the current Service Location.

## Advice

BeachOS may advise checking destination availability, preserving Customer Group
identity, and confirming responsibility before an approved change.

It must not create a new Customer Group because of a move, split or combine
groups, invent transfer charging, or choose a Responsible Waiter automatically.

## Human Decision

Guests decide whether to request more service or a move. Authorized staff decide
whether an Order, transfer, or handover may proceed under approved rules.

## Outcome

- Another separate Order Round is submitted.
- The same Customer Group completes an approved transfer and keeps its Orders,
  optional Bill, Payments, Responsible Waiter, and History.
- Exactly one new Responsible Waiter accepts an approved handover.
- The requested action is rejected with the existing state unchanged.
- The action remains uncertain and must be reconciled.
- Active service continues without change.

# Stage 10 — Bill Review

## Purpose

Give authorized staff and the guests a clear, explainable understanding of what
the Customer Group owes before Payment and closing decisions.

## Primary Decision

Is the Bill complete and understandable enough for the guests and authorized
staff to proceed toward Payment?

## Responsible Human

The Responsible Waiter supports the guest relationship.

The Cashier has financial visibility and may perform approved financial actions
when holding the required Capability.

The exact division of responsibility for presenting, reviewing, correcting, and
approving a Bill is not fully defined.

## Operational Readiness

- A Bill exists because at least one approved Financial Obligation exists.
- Every Bill Line is explainable and connected to an approved obligation,
  adjustment, correction, or reversal.
- Submitted Order Rounds and other approved charges are represented without
  overwriting history.
- Payments already recorded are reflected.
- The current Balance can be confirmed.

A Customer Group with no Financial Obligation may have no Bill. Its completion
path is unresolved and must not invent a zero-value Bill.

## Operational Confidence

Confidence requires financial facts to be complete, current, internally
consistent, and attributable.

BeachOS must remain uncertain when an Order, Bill Line, correction, reversal, or
Payment outcome is unresolved.

## Attention

- **Immediate action:** Financial history conflicts, a consequential outcome is
  uncertain, or the guest is being asked to pay an amount that cannot be
  explained.
- **Action required:** The guest questions a line, an approved correction is
  needed, or outstanding work affects the final review.
- **Monitor:** The running Bill remains accurate while service continues.

## Advice

BeachOS may explain what each Bill Line represents, the confirmed Balance, and
which facts still require authorized review.

It must not hide original financial facts, invent discounts, silently edit
submitted Orders, or call a Bill final while relevant approved work remains
uncertain.

## Human Decision

The guests decide whether the Bill matches their understanding. Authorized staff
decide whether an approved correction, reversal, or next financial action is
needed.

## Outcome

- The Bill is understood and proceeds toward Payment.
- Service continues and later approved obligations may be added.
- A question or correction requires authorized resolution.
- The Bill cannot yet be relied upon.
- No Bill exists because no Financial Obligation has arisen.

# Stage 11 — Payment

## Purpose

Confirm exact value received against the Bill without confusing an attempt,
rejection, or uncertain outcome with a Payment.

## Primary Decision

Has the business safely confirmed receipt of the intended value against the
correct Bill?

## Responsible Human

An authorized Cashier or other Staff Member holding Record Payments and
satisfying the applicable business rules.

Role alone does not authorize Payment recording.

## Operational Readiness

- The correct Bill exists and accepts Payment.
- The amount and approved Payment Method are valid.
- The acting Staff Member has the required Capability.
- Earlier Payment outcomes that affect the Balance are known.
- The Payment can be confirmed exactly once.

Partial Payments, split Payments, overpayment, cash change, tips, allocation,
refunds, and detailed reversal rules remain unresolved.

## Operational Confidence

Confidence exists only when value received is authoritatively confirmed against
the intended Bill.

BeachOS must remain uncertain when an attempt may have completed but receipt
cannot be confirmed. An uncertain attempt does not reduce the Balance and must
not be repeated blindly.

## Attention

- **Immediate action:** Payment outcome is uncertain, duplicate receipt is
  possible, or the wrong Bill or amount may be affected.
- **Action required:** Payment is rejected or the approved method cannot be used.
- **Monitor:** A Payment is being attempted but has not yet been confirmed.

## Advice

BeachOS may state whether Payment was recorded, rejected, or remains uncertain
and explain the next safe confirmation step.

It must not call an attempt a Payment, reduce the Balance before confirmation,
hide a rejection, or encourage repetition while the first outcome is unknown.

## Human Decision

The guests choose an approved Payment Method. The authorized Staff Member
confirms the intended amount and decides whether to proceed, retry after a
confirmed rejection, or pause while an uncertain outcome is reconciled.

## Outcome

- `Payment Recorded`: the confirmed amount reduces the Bill Balance exactly
  once.
- `Payment Rejected`: no Payment is created and the Balance is unchanged.
- Payment outcome remains uncertain and requires reconciliation.
- A valid Payment reduces the Balance to zero and the Bill becomes fully paid.

A zero Balance does not automatically close the Bill or complete the Customer
Group.

# Stage 12 — Bill Closing and Customer Group Completion

## Purpose

End ordinary financial and operational activity only after every approved
completion condition has been satisfied.

## Primary Decision

Can the Bill be closed and can the active Customer Group be completed without
losing financial truth, outstanding work, responsibility, or History?

## Responsible Human

**Unresolved.**

The repository has not approved:

- who may confirm Customer Group completion;
- which Capability is required;
- the exact Bill-closing authority;
- whether Bill closing and Customer Group completion are one action or two.

## Operational Readiness

The accepted boundary requires:

- the Customer Group is Active;
- any Bill has satisfied its approved closing conditions;
- all outstanding operational work has satisfied approved completion rules;
- completion is authorized and traceable;
- a Customer Group with no Bill may complete through an approved no-Bill path.

The exact conditions, evidence, and sequence are unresolved. Full Payment, zero
Balance, physical departure, elapsed time, or Bill closing alone must not be
treated as sufficient.

## Operational Confidence

BeachOS cannot confidently advise completion until the Product Owner approves:

- the full completion conditions;
- the responsible person and Capability;
- the relationship between Bill closing, operational work, Customer Group
  completion, and Service Location release;
- the no-Bill completion path;
- the permitted correction, reversal, refund, and exceptional rules.

Until then, BeachOS may describe confirmed financial and operational facts but
must remain uncertain about completion eligibility.

## Attention

- **Immediate action:** Guests are departing while financial or operational truth
  is uncertain, or a Completed Customer Group could still receive ordinary
  activity.
- **Action required:** The Bill is fully paid but other completion conditions
  remain unknown or unresolved.
- **Monitor:** Confirmed outstanding work is being resolved before completion.

No approved completion timing threshold exists.

## Advice

BeachOS may say:

- the Bill Balance is zero;
- the Bill is or is not confirmed closed;
- outstanding operational work remains;
- completion eligibility cannot yet be confirmed.

BeachOS must not advise automatic completion, reopen a Completed Customer Group,
invent a no-Bill shortcut, or release the Service Location through assumption.

## Human Decision

The final authorized human decision is unresolved and requires Product Owner
approval.

Guests may decide that they are ready to leave, but that decision does not by
itself define the business completion action.

## Outcome

- The Customer Group remains Active while approved completion conditions are
  unresolved.
- A future approved action closes the Bill.
- A future approved action completes the Customer Group.
- Completion is rejected because a required condition is not satisfied.
- Completion outcome remains uncertain and ordinary activity must not be
  repeated or ended through assumption.

The current repository accepts `Bill Closed` and `Customer Group Completed` as
business events but does not yet approve their complete workflows or exact
relationship.

# Stage 13 — Guest Departure and Operational Release

## Purpose

Conclude the human hospitality experience respectfully while ensuring physical
departure, Service Location availability, and Customer Group lifecycle are not
confused.

## Primary Decision

Have the guests physically departed, and is the business authorized to consider
their active service complete and release the Service Location?

## Responsible Human

Human hospitality at departure belongs to the Venue team.

The specific person responsible for confirming departure, Customer Group
completion, and Service Location release is **not approved**.

## Operational Readiness

The guests may physically depart whenever they choose.

Operational release is ready only after future approved rules confirm:

- any Bill satisfies closing conditions;
- outstanding operational work satisfies completion conditions;
- the Customer Group is validly completed;
- the Service Location may become available and is not otherwise unavailable.

The exact order of physical departure, Bill closing, Customer Group completion,
and Service Location release is unresolved.

## Operational Confidence

BeachOS may confidently state that the Customer Group is Completed only after an
authorized, traceable completion outcome.

Physical absence, an empty-looking location, a zero Balance, or elapsed time is
not enough.

BeachOS must remain uncertain when the guests have left but completion or release
has not been confirmed.

## Attention

- **Immediate action:** The Service Location is about to be offered to another
  party while the existing Customer Group may still be Active.
- **Action required:** Guests have departed but Bill, outstanding work,
  completion, or release remains unresolved.
- **Monitor:** A confirmed completion and normal physical reset are progressing
  under future approved Venue procedures.

Housekeeping or reset readiness is not currently a defined lifecycle and must not
be invented in this journey.

## Advice

BeachOS may distinguish:

- guests physically departed;
- Customer Group still Active;
- Customer Group Completed;
- Service Location available;
- Service Location otherwise unavailable.

It must not infer one from another.

## Human Decision

The Venue team decides how to thank and farewell the guests.

The person authorized to complete the Customer Group and release the Service
Location remains an unresolved Product Owner decision.

## Outcome

- The guests depart and the Customer Group remains Active pending approved
  completion.
- The Customer Group is validly Completed and becomes permanent History.
- The Service Location becomes available after completion, provided it is not
  otherwise unavailable.
- The Service Location remains unavailable for another confirmed operational
  reason.
- Departure or release status remains uncertain and the location must not be
  promised to another party.

Completed is terminal under the current approved lifecycle. New ordinary Orders,
Payments, transfers, or responsibility changes are forbidden. Historical review
and separately approved accountability activity may continue without
reactivating the Customer Group.

# Journey-wide Intelligence Principles

Across every stage, BeachOS must:

- begin with the responsible human’s current decision;
- keep guest experience, operational truth, and human confidence ahead of
  administration;
- distinguish readiness from confidence;
- distinguish confirmed facts from observation, advice, and uncertainty;
- preserve one Customer Group identity throughout active service;
- preserve separate Order Rounds and permanent financial History;
- protect one active Customer Group per Service Location;
- protect exactly one Responsible Waiter at a time;
- keep Role separate from Capability;
- prevent uncertain consequential outcomes from appearing as success or failure;
- advise only when approved facts support a useful next step;
- remain silent rather than create noise during normal hospitality;
- communicate calmly and without technical language or blame;
- never infer personal identity, VIP status, satisfaction, or staff performance;
- never let technology perform a human decision merely because it can identify
  the context.

# Capability Map

This map identifies the Product Capabilities that will support each journey
stage. It is a planning view, not approval to implement them.

| Journey Stage                                  | Supporting Capability                                          | Current Capability Status                                                                | Important Boundary                                                                   |
| ---------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Venue prerequisite                             | Venue Opening                                                  | Existing approved product capability in operation; no capability document in this folder | Opening permits arrivals but creates no Customer Group                               |
| 1. Guest Arrival                               | Guest Arrival                                                  | Approved capability                                                                      | Human noticing and greeting remain human                                             |
| 2. Welcome and Needs Understanding             | Guest Arrival                                                  | Approved capability                                                                      | No personal inference or profile required                                            |
| 3. Availability, Waiting, or Seating Choice    | Guest Arrival                                                  | Approved for current availability and manual waiting boundary                            | Digital waiting, reservation, priority, capacity, and accessibility rules unresolved |
| 4. Escort and Service Location Identification  | Guest Arrival                                                  | Approved capability                                                                      | NFC identifies only; manual fallback remains                                         |
| 5. Service Handoff and Customer Group Opening  | Guest Arrival; future Customer Group Opening capability        | Guest Arrival approved; dedicated opening capability not yet defined                     | Only Responsible Waiter opens; Beach Sunbed obligation applies                       |
| 6. Active Service and Guest Care               | Future Active Service Coordination capability                  | Not yet defined                                                                          | Complaint, request, delivery, and service-quality lifecycles unresolved              |
| 7. Order Round                                 | Future Ordering capability                                     | Business concepts and events approved; capability not yet defined                        | Each submission is a separate Order Round                                            |
| 8. Bar and Kitchen Preparation                 | Future Kitchen Operations and Bar Operations capabilities      | Business concepts and event sequences approved in part                                   | Priority, partial readiness, completion, runner, and delivery meanings unresolved    |
| 9. Ongoing Service                             | Future Transfer and Responsible Waiter Handover capabilities   | Accepted in principle; detailed rules unresolved                                         | Preserve Customer Group identity and one Responsible Waiter                          |
| 10. Bill Review                                | Future Billing capability                                      | Business concepts approved; detailed correction and closing rules incomplete             | Bill begins only with first Financial Obligation                                     |
| 11. Payment                                    | Future Payments capability                                     | Core Payment facts approved; detailed allocation and exception rules unresolved          | Confirmed receipt only; uncertainty never reduces Balance                            |
| 12. Bill Closing and Customer Group Completion | Future Bill Closing and Customer Group Completion capabilities | Not ready for capability design without Product Owner decisions                          | Zero Balance and Bill closing do not automatically complete the group                |
| 13. Guest Departure and Operational Release    | Future Guest Departure and Operational Release capability      | Not defined                                                                              | Physical departure, completion, and release must remain separate until approved      |
| Whole journey                                  | Future Operational History capability                          | Activity Log, Audit Trail, and History principles approved                               | Accountability without blame; history is never silently rewritten                    |

## Capability dependencies that require Product Owner decisions

Before the full journey can progress into detailed capability design, the Product
Owner must decide:

1. digital waiting, reservation, queue order, and priority rules;
2. Service Location capacity and accessibility meaning;
3. formal Host-to-Responsible-Waiter handoff and acceptance;
4. exact Order-submission authority beyond the Responsible Waiter;
5. preparation acknowledgement, readiness, completion, partial completion,
   delivery, and runner responsibility;
6. allowed transfer combinations and financial effects;
7. Responsible Waiter handover authority and acceptance;
8. Bill correction, closing, reopening, and exception rules;
9. partial, split, excess, reversed, and refunded Payment rules;
10. exact Customer Group completion conditions, actor, Capability, and sequence;
11. the no-Bill Customer Group completion path;
12. the relationship among physical departure, Customer Group completion,
    Service Location release, and any housekeeping or reset requirement.
