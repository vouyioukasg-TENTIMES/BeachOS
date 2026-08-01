# Guest Arrival Capability

## Capability status

This document defines the first product capability for Guest Arrival.

It is governed by the BeachOS Operational Intelligence Framework and remains
subordinate to the Domain Model, Decision Log, Project Glossary, Guest Arrival
Workflow, Host Operational Playbook, and approved business rules.

This capability describes hospitality operations and BeachOS reasoning. It does
not define screens, implementation, data structures, interfaces, automation, or
new business rules.

# 1. Purpose

The Guest Arrival Capability helps the Host turn an arriving guest party into a
welcomed, honestly informed, safely seated party with a clear handoff to the
Responsible Waiter.

The capability begins when a guest party enters the Venue. It ends when one of
the following is clear:

- the Responsible Waiter intentionally opens the Customer Group at the confirmed
  Service Location;
- the party enters the approved manual waiting process;
- the party chooses another available option;
- the party leaves before service begins;
- the arrival pauses because a safe next step cannot be confirmed.

BeachOS supports operational awareness, but hospitality remains human. It does
not notice the guest, choose how to greet them, infer their needs, promise a
location, assign importance to them, or open their Customer Group automatically.

# 2. Primary Decision

The Host’s primary decision is:

> Can I confidently guide this arriving party to a suitable, currently available
> Service Location and complete a clear handoff to the Responsible Waiter?

This decision contains three connected questions:

1. Is the Venue ready to receive the party?
2. Is there a suitable Service Location whose current availability can be
   trusted?
3. Can an eligible Responsible Waiter accept the handoff and decide whether to
   open the Customer Group?

The Host decides how to welcome, assess, propose, wait, escort, and coordinate.
The Host does not decide the official Customer Group opening. Only the
Responsible Waiter may intentionally open the Customer Group while holding the
required Capability.

# 3. Operational Scope

## Begins

The capability begins at the exact moment a guest party enters the Venue. Human
awareness may follow, but a delayed acknowledgment does not move the true start
of the arrival experience.

## Includes

- noticing and acknowledging the party;
- greeting;
- understanding the minimum practical needs;
- checking current Service Location availability;
- deciding whether to offer seating or the approved manual waiting process;
- proposing an appropriate available Service Location;
- escorting the party;
- identifying the Service Location through NFC or manual lookup;
- confirming that physical and operational context agree;
- introducing the Responsible Waiter;
- supporting the Responsible Waiter’s intentional Customer Group opening;
- communicating a clear confirmed, declined, paused, or uncertain outcome.

## Ends

The normal successful scope ends when the Responsible Waiter has intentionally
opened exactly one Customer Group at the confirmed Service Location and the
outcome is known.

## Outside the current scope

- digital waiting-list management;
- reservation management;
- automated arrival detection;
- automatic seating or Service Location assignment;
- automatic Responsible Waiter selection;
- predicted waiting or release times;
- customer profiles;
- VIP identification, ranking, or automatic priority;
- facial recognition or personal inference;
- route guidance;
- weather or crowd detection;
- Customer Group transfer after opening;
- Order taking;
- preparation, billing, Payment, or Customer Group completion beyond the
  immediate approved Beach Sunbed opening consequence.

Waiting remains a manual operational process. Any future digital waiting,
reservation, recognition, or recommendation capability requires separate Product
Owner approval.

# 4. Actors

## Guest party

The people arriving to receive hospitality. Before official service begins, the
capability refers to them as the arriving party, not as an active Customer Group.
Individual identity is not required.

The guests decide whether to accept a proposed Service Location, wait, consider
another option, or leave.

## Host

The Host welcomes the party, understands practical needs, checks availability,
proposes options, escorts the guests, verifies the physical context, and
coordinates the handoff.

The Host remains responsible for the arrival experience until the handoff is
clear. The Host does not officially open the Customer Group and must not declare
another person responsible without their acceptance.

## Responsible Waiter

The Responsible Waiter confirms the party and Service Location, accepts service
responsibility, reviews any immediate Beach Sunbed Financial Obligation, and
intentionally decides whether to open the Customer Group.

The Responsible Waiter must be eligible for the responsibility and hold the Open
Customer Group Capability. Role alone does not authorize the action.

## Manager

The Manager supports exceptions, conflict, safety questions, unclear capacity,
priority requests, unresolved responsibility, and other matters that require
approved oversight.

This capability does not assume that Manager responsibility bypasses any
business rule or automatically grants a Capability.

## Other operational staff

Other Hosts, service leaders, and responsible staff may provide current
operational facts or accept a clear handoff within their approved
responsibilities.

## BeachOS

BeachOS provides current business context, identifies uncertainty, protects
approved rules, focuses attention, and offers grounded advice.

BeachOS does not greet the guest, observe physical suitability, make promises,
decide hospitality exceptions, infer personal needs, or replace the Host or
Responsible Waiter.

# 5. Business Concepts

This capability uses only approved business concepts:

- **Venue** — the physical hospitality operation receiving the party.
- **Business Date** — the current Venue operating day.
- **Host** — the Staff Member responsibility coordinating arrival.
- **Staff Member** — the person acting in an approved business capacity.
- **Role** — the person’s business responsibility, which does not itself grant
  authority.
- **Capability** — explicit authority for a protected action.
- **Area** — the permanent physical section of the Venue.
- **Zone** — the dynamic operational grouping that may support current service
  coordination but does not define physical geography.
- **Service Location** — the identifiable place that may receive one active
  Customer Group.
- **Available** — the Service Location is eligible to receive a Customer Group.
- **Occupied** — the Service Location already has an active Customer Group.
- **Unavailable** — the Service Location cannot receive a new Customer Group.
- **Service Location Digital Identity** — the stable identity resolving the
  physical place to its current central context.
- **Responsible Waiter** — the one eligible Staff Member who accepts
  responsibility and intentionally opens the Customer Group.
- **Customer Group** — the primary operational entity created only when the
  Responsible Waiter officially begins service.
- **Financial Obligation** — an approved reason the Customer Group owes an exact
  amount.
- **Bill** — created only when the first approved Financial Obligation exists.
- **Beach Sunbed** — the Service Location type whose Customer Group opening
  creates the approved immediate Beach Sunbed Financial Obligation.

The capability does not introduce an Arrival, Visit, Waiting Entry, Seating
Reservation, VIP Profile, or Handoff as a new business concept.

# 6. Preconditions

## Venue preconditions

- The Venue has been officially opened for the current Business Date.
- Guest arrivals are permitted.
- The Venue and Business Date can be confirmed.
- Normal operational responsibility and manual continuity arrangements are in
  place.

## Host preconditions

- A Host or approved arrival responsibility is present.
- The Host understands the current Venue arrangement and known constraints.
- The Host knows how to escalate to the Manager and relevant operational leaders.
- The Host understands that the Responsible Waiter alone opens the Customer
  Group.

## Service Location preconditions

- Current Service Location state can be confirmed from the central source of
  operational truth.
- The Host can compare the current state with the physical situation.
- Occupied, unavailable, and retired locations are excluded.
- NFC identification has a manual lookup fallback using the visible name or
  number.

## Responsibility preconditions

- An eligible Responsible Waiter can be confirmed before Customer Group opening.
- The Responsible Waiter can explicitly accept responsibility.
- The Open Customer Group Capability can be confirmed.

## Business-rule preconditions

- One active Customer Group per Service Location remains protected.
- Service Location identification performs no operational or financial action.
- The Customer Group does not exist merely because the guests arrived, were
  greeted, accepted a location, or were escorted.
- A Bill is not created unless a Financial Obligation exists.
- Opening at a Beach Sunbed creates the approved immediate Financial Obligation.

If a precondition cannot be confirmed, BeachOS must describe the uncertainty and
must not present the affected next step as ready.

# 7. Operational Readiness

Guest Arrival does not have one permanent readiness score. Readiness is evaluated
for each decision in the arrival journey.

## Ready to begin normal arrival

Normal arrival is ready to proceed when:

- the Venue is officially open for the current Business Date;
- arrival responsibility is present;
- current Venue and Service Location context can be confirmed;
- a safe manual continuity path exists if direct digital support is unavailable.

The Host can still welcome a guest respectfully when normal arrival is not ready.
Welcoming the guest does not authorize seating or Customer Group opening.

## Ready to offer a Service Location

A Service Location is ready to be offered when:

- the Host has understood the minimum practical needs stated by the party;
- its current identity and availability are confirmed;
- it is not occupied, unavailable, or retired;
- the physical condition does not conflict with the confirmed operational state;
- the Host judges it suitable from direct human observation;
- no approved rule prevents its use.

The presence of an empty-looking location is not readiness. A preference is not
availability. A remembered status is not current confirmation.

## Ready to escort

Escort is ready when:

- the guests have accepted the proposed Service Location;
- the location remains confirmed available;
- the Host knows the correct physical destination;
- the route and physical situation appear suitable through human observation.

If the location changes or becomes uncertain during escort, readiness ends and
the Host returns to availability assessment.

## Ready for handoff

Handoff is ready when:

- the party is at the correct identified Service Location;
- the physical and digital Service Location context agree;
- an eligible Responsible Waiter is present or can directly accept
  responsibility;
- the guests can understand who will serve them.

## Ready for Customer Group opening

Only the Responsible Waiter evaluates and performs this final action.

Opening is ready when:

- the Venue remains officially open;
- the party and Service Location are correct;
- the Service Location remains available;
- no active Customer Group already occupies it;
- the Responsible Waiter has accepted responsibility;
- the Responsible Waiter holds the Open Customer Group Capability;
- the applicable Beach Sunbed Financial Obligation can be reviewed and confirmed
  where relevant;
- the complete outcome can be recorded safely.

Readiness makes opening eligible. It never opens the Customer Group
automatically.

# 8. Operational Confidence

## When BeachOS may advise confidently

BeachOS may confidently support seating and handoff when:

- the current Venue and Business Date are known;
- official Venue opening is confirmed;
- Service Location identity, state, and visible name agree;
- availability is current enough for the immediate decision;
- no conflicting Customer Group or location fact exists;
- the Host has supplied the practical needs learned through conversation;
- the Host confirms physical suitability;
- the Responsible Waiter and required Capability are known before opening;
- earlier actions in this arrival have known outcomes.

BeachOS may say that a location is confirmed available. It may not say that the
location is best for the guests unless an approved rule and the necessary human
information support that conclusion.

## When BeachOS must remain uncertain

BeachOS must state uncertainty when:

- the Venue opening state cannot be confirmed;
- Service Location information may be stale;
- the physical and central conditions disagree;
- NFC and manual lookup do not resolve to the same location;
- the Service Location changes state during the decision;
- another Staff Member may be seating a party at the same location;
- suitability depends on a guest need that has not been understood;
- safe capacity, accessibility, or physical condition is unclear;
- Responsible Waiter identity, acceptance, eligibility, or Capability is
  unclear;
- the applicable Beach Sunbed Financial Obligation cannot be confirmed;
- a Customer Group opening may have completed but its outcome is unknown;
- waiting order, reservation status, VIP instruction, or exception authority is
  unclear.

## Confidence boundaries

- Physical observation and central operational truth must support each other.
  BeachOS must not silently choose one when they conflict.
- NFC success identifies the Service Location; it does not prove availability,
  suitability, authority, or permission to open.
- A previous declaration or remembered location state does not establish current
  confidence.
- BeachOS must not create waiting-time estimates or suitability conclusions from
  incomplete information.
- When confidence is insufficient, the capability pauses the affected decision
  while preserving a calm guest experience.

# 9. Attention

Attention exists only when awareness or human action has practical value.

## Immediate action

The following require immediate human action:

- guests are about to be seated before the Venue is officially open;
- a proposed Service Location is physically unsafe;
- physical occupancy conflicts with the current operational state;
- two parties are being directed to the same Service Location;
- NFC or manual identification resolves to the wrong or conflicting Service
  Location;
- the Service Location becomes occupied or unavailable during escort;
- an unauthorized person attempts to open the Customer Group;
- Customer Group opening has an uncertain outcome;
- a confirmed mismatch threatens guest experience or operational truth.

## Action required

The following deserve focused attention:

- no suitable Service Location is currently available;
- the guest party is waiting and needs an honest update;
- the guests reject or reconsider an offered location;
- an eligible Responsible Waiter has not yet accepted the handoff;
- an NFC interaction fails and manual identification is required;
- an accessibility, capacity, safety, or exception question requires Manager
  confirmation;
- a recognized guest or VIP request raises an unapproved priority or exception;
- arrival pressure makes ownership between Hosts unclear.

## Monitor

The following should remain part of operational awareness without unnecessary
interruption:

- a party is being welcomed and assisted normally;
- an accepted Service Location remains available during escort;
- a clear Responsible Waiter handoff is progressing;
- arrival volume is manageable and creates no confirmed conflict;
- a guest preference is known but does not currently require action.

No automatic arrival-pressure threshold, greeting deadline, or waiting alert is
approved. BeachOS must not invent one.

## Attention rules

- Describe the guest or operational situation, not staff character.
- Do not create several Attention items from the same underlying mismatch.
- Remove current Attention when the condition is confirmed resolved, while
  preserving any required business history.
- Do not represent normal hospitality as a warning.
- An empty Attention Queue does not replace the Host’s physical observation.

# 10. Blockers

A Blocker prevents a named next operation. It must come from an approved rule or
a confirmed condition that makes the operation unsafe.

## Blockers to seating

- The Venue is not officially open.
- No suitable Service Location is confirmed available.
- The proposed Service Location is occupied, unavailable, or retired.
- The physical location and operational truth conflict.
- Service Location identity cannot be confirmed.
- A confirmed safety or suitability condition prevents use.

## Blockers to Customer Group opening

- The Venue is not officially open.
- The Service Location is no longer available.
- Another active Customer Group already occupies the Service Location.
- The Staff Member has not accepted Responsible Waiter responsibility.
- The acting person is not the Responsible Waiter.
- The Responsible Waiter lacks the Open Customer Group Capability.
- The correct Service Location cannot be confirmed.
- The applicable Beach Sunbed Financial Obligation cannot be confirmed.
- A previous opening attempt has an uncertain outcome.
- The complete opening cannot be confirmed safely.

## Conditions that are not automatically Blockers

- NFC failure when manual identification safely confirms the same Service
  Location;
- a guest preference that cannot be met when the guest accepts another suitable
  option;
- normal walking time during escort;
- an empty Attention Queue;
- a Host recommendation;
- VIP recognition by itself;
- a location being outside the Host’s preferred Area when it remains approved,
  suitable, and accepted;
- a Customer Group having no Bill at a non-Beach-Sunbed location.

When the business has not approved whether a condition blocks seating, BeachOS
must state the uncertainty and seek the appropriate human decision. It must not
invent a prohibition.

# 11. Advice

## Advice BeachOS may provide

BeachOS may:

- confirm that the Venue is open and normal arrival may proceed;
- identify which Service Locations are currently available or unavailable;
- explain a known reason a location cannot receive the party;
- advise the Host to verify a physical and operational mismatch before making a
  promise;
- advise manual lookup when NFC identification fails;
- advise returning to availability assessment when the selected location
  changes;
- advise contacting the relevant service leader when no eligible Responsible
  Waiter can accept the handoff;
- remind the Host that Service Location identification does not open a Customer
  Group;
- advise the Responsible Waiter not to repeat an opening action while its outcome
  remains uncertain;
- explain the immediate Beach Sunbed consequence before intentional opening.

## Advice BeachOS must not provide

BeachOS must not:

- tell the Host how to greet a particular guest;
- infer party needs from appearance, age, familiarity, or perceived status;
- claim that one location is best without approved facts and human input;
- promise a waiting time;
- choose a winner when two parties appear to claim one location;
- create an unofficial reservation or waiting priority;
- infer VIP status or entitlement;
- automatically select or assign the Responsible Waiter;
- advise bypassing availability, Capability, or the Responsible Waiter-only rule;
- treat NFC identification as authorization;
- encourage repeated Customer Group opening when the first outcome is unknown.

## When BeachOS should remain silent

BeachOS should remain silent when the Host has a clear normal hospitality choice
and no relevant operational meaning needs explanation. It should not narrate
every greeting, escort, or ordinary handoff.

When essential facts are uncertain, BeachOS should state the uncertainty rather
than offer unsupported advice.

# 12. Human Decisions

The following decisions always remain human:

- how and when to acknowledge the arriving party;
- how to greet and communicate;
- which practical needs to ask about;
- whether a confirmed available Service Location is physically suitable;
- which suitable options to present;
- whether and how to offer the approved manual waiting process;
- what honest estimate to communicate when current human knowledge supports one;
- whether an exception requires Manager involvement;
- how to handle a family, accessibility need, complaint, language difference,
  weather condition, or guest change of mind;
- how to recognize a familiar or VIP guest discreetly;
- whether the Host should stop or change an escort based on physical conditions;
- which eligible Responsible Waiter accepts the handoff under the current
  operating arrangement;
- whether the Responsible Waiter intentionally opens the Customer Group;
- how to explain delay or uncertainty to the guests.

BeachOS may provide facts and advice. It must not impersonate these decisions.

# 13. Possible Outcomes

## Customer Group opened

The party is at the correct available Service Location, one eligible Responsible
Waiter has accepted responsibility, and exactly one Customer Group is
intentionally opened.

At a Beach Sunbed, the approved immediate Financial Obligation and Bill are
created as part of the opening outcome. At another Service Location type, the
Customer Group may exist without a Bill.

## Waiting

No suitable Service Location is currently available, or the guests choose not to
accept the current options. The party enters the approved manual waiting process.
No Customer Group, Bill, charge, Order, transfer, or Payment is created.

## Alternative accepted

The guests decline the first proposal and accept another confirmed suitable
Service Location. The capability continues through escort and handoff. This is
not a Customer Group transfer because no Customer Group has opened.

## Guest leaves

The party chooses to leave before official service begins. No Customer Group is
created. The reason may remain unknown, and BeachOS must not invent one.

## Arrival paused

The next step cannot proceed because identity, availability, suitability,
responsibility, authority, or another required condition cannot be confirmed.
The Host maintains hospitality while resolving or escalating the issue.

## Opening rejected

The Customer Group is not opened because a confirmed business rule is not
satisfied. The Service Location and any existing Customer Group remain
unchanged. The rejection must state the operational reason.

## Opening outcome uncertain

BeachOS cannot yet confirm whether the intentional opening completed. This is
neither success nor failure. The party, Service Location, responsibility, and
action identity must be reconciled before the action is repeated.

This capability does not create a separate Arrival Completed business event.

# 14. Failure Recovery

## Guest not noticed promptly

The Host acknowledges the party honestly, takes clear ownership, and resumes the
arrival conversation without blaming another person. BeachOS has no approved
automatic arrival detection.

## Venue is not open

The Host welcomes the guests but does not continue into normal seating or
Customer Group opening. The Host explains that the Venue is not ready to receive
guests and follows the approved operational escalation.

## Availability cannot be confirmed

The Host makes no promise. The physical situation and central operational truth
are reconciled through the responsible people. Another confirmed option or the
manual waiting process may be offered.

## Location becomes unavailable

Before Customer Group opening, the Host explains that the situation changed and
returns to the availability decision. No transfer is created.

## NFC fails

The Host uses manual lookup by visible name or number. If the same Service
Location cannot be confirmed, the Host stops rather than guessing.

## Wrong Service Location identified

The Host does not continue the handoff or opening. The visible location and
stable Digital Identity are checked, and any moved, damaged, or duplicated marker
is escalated through the approved process.

## No Responsible Waiter available

The Host remains responsible for coordination, informs the guests honestly, and
contacts the relevant service leader. The Host does not open the Customer Group
or create an informal responsibility assignment.

## Duplicate seating attempt

Both attempts pause. The responsible people establish the actual current
situation. No second Customer Group is opened, and the affected party receives
another confirmed option or honest waiting guidance.

## Customer Group opening rejected

BeachOS states the specific business reason. The Host and Responsible Waiter
correct or escalate that reason, then begin a new intentional decision only when
readiness and confidence are restored.

## Customer Group opening uncertain

BeachOS states what is known, what cannot be confirmed, and why repetition is
unsafe. The Responsible Waiter does not repeat the action until the authoritative
Customer Group and Service Location state is confirmed.

## Connectivity or BeachOS unavailable

The Host follows the approved manual continuity process and does not invent
central operational state. Actions whose safe completion requires authoritative
confirmation remain paused. A failed device or NFC interaction alone does not
stop identification when manual lookup can safely reach the same Service
Location.

# 15. Operational Conversation Examples

These examples demonstrate tone and reasoning. They do not define interface
copy.

## Venue not open

> The Venue is not open for today’s Business Date. Welcome the guests, but do not
> begin normal seating. Confirm the opening status with the Host responsible for
> Venue Opening.

## Suitable location available

> Beach A12 is currently available. It matches the location type the guests
> requested. Confirm the physical condition with the guests before offering it.

## No suitable location confirmed

> No suitable Service Location is currently confirmed available. Explain the
> situation honestly and offer the approved manual waiting process. A waiting
> time cannot be confirmed.

## Physical mismatch

> Pool P07 is shown as available, but it appears occupied. Do not promise or use
> the location until the current situation is confirmed.

## NFC failure

> The NFC identification did not confirm this Service Location. Use the visible
> name or number to find the same location manually. Identification alone will
> not open a Customer Group.

## Location changes during escort

> Upper Table U04 is no longer available. Explain that the situation changed,
> then review another confirmed option with the guests.

## Responsible Waiter not confirmed

> No eligible Responsible Waiter has accepted this handoff. Keep the guests
> informed and contact the relevant service leader. The Host must not open the
> Customer Group.

## Ready for Responsible Waiter decision

> Beach A12 is confirmed available, and Maria has accepted responsibility as the
> Responsible Waiter. Opening the Customer Group will create the approved Beach
> Sunbed obligation. Maria must review and intentionally confirm the opening.

## Opening rejected

> The Customer Group was not opened because Beach A12 is no longer available.
> Confirm another suitable location before trying again.

## Opening outcome uncertain

> The Customer Group opening cannot yet be confirmed. Do not repeat the action.
> First confirm whether the party is already active at Beach A12.

## VIP request

> The guest is recognized, but no approved priority or exception is confirmed.
> Continue normal hospitality and ask the Manager before changing the waiting or
> seating decision.

# 16. Success Criteria

The Guest Arrival Capability is successful when:

- the guest party is acknowledged and welcomed through human hospitality;
- the Host understands the minimum practical needs without unnecessary personal
  information;
- the Venue is confirmed open before normal seating proceeds;
- every offered Service Location is currently available and physically suitable;
- the Host does not present uncertainty as a promise;
- the guests understand whether they are being seated, waiting, considering
  another option, or leaving;
- NFC and manual lookup resolve to the same enduring Service Location;
- identification performs no business or financial action;
- the Host completes a clear human handoff;
- the Responsible Waiter knowingly accepts responsibility;
- only the Responsible Waiter with the required Capability opens the Customer
  Group;
- exactly one active Customer Group occupies the Service Location;
- Beach Sunbed opening creates the approved immediate Financial Obligation and
  Bill;
- another Service Location type may begin service without a Bill;
- confirmed rejection and uncertain outcome remain distinct;
- repeated action cannot create a duplicate Customer Group;
- operational messages use calm business language and identify the next safe
  step;
- the physical operation and BeachOS’s trusted view agree at the end of the
  capability.

No numerical target for Greeting Time, seating time, waiting time, or handoff
time is approved by this capability. Those measures require approved start
points, end points, exclusions, and operating targets before they can judge
success.

# 17. Future Expansion

The following may extend this capability only after separate Product Owner
decisions:

- a digital waiting process with defined entry, order, priority, ownership, and
  exit rules;
- reservations and their relationship to availability and waiting;
- approved Service Location capacity and accessibility information;
- formal arrival ownership and Host handoff;
- multilingual operational guidance;
- approved Responsible Service Staff selection support;
- workload-aware advice that never assigns responsibility automatically;
- a privacy-conscious Guest Token journey;
- approved VIP knowledge and discreet recognition rules;
- approved guest preferences without mandatory personal identity;
- reliable arrival, greeting, seating, waiting, and handoff measures;
- weather, route, crowd, or physical-safety context;
- arrival continuity across multiple entrances;
- venue-specific Guest Arrival Frameworks for restaurants, resorts, hotels, and
  events.

Future expansion must preserve these boundaries:

- human hospitality remains human;
- Customer Group remains the primary operational entity;
- arrival and seating do not create a Customer Group;
- the Responsible Waiter intentionally opens the Customer Group;
- Role does not imply Capability;
- one active Customer Group may occupy a Service Location;
- Service Location identification never authorizes or performs an action;
- waiting, priority, suitability, and VIP rules must be approved rather than
  inferred;
- uncertainty must remain visible.
