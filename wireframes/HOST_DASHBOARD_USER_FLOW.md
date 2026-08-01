# BeachOS Host Dashboard — Functional User Flow

## Document purpose

This document defines navigation and state transitions for the first Host Dashboard
functional prototype. It describes operational triggers, business safeguards,
Business Commands, Domain Events, affected Domain Concepts, failure outcomes, and
user feedback.

It does not define software screens beyond their functional relationships. It does
not create a Command, Domain Event, Capability, lifecycle state, or business rule.

## Flow notation

- **Screen state** is written as a named step.
- **Human operational step** is written in parentheses.
- **Business Command** is named only when it already appears in
  `docs/DOMAIN_EVENTS.md`.
- **No Command** means the transition is viewing, navigation, human work, or
  retrieval rather than an intent to change business state.
- **No Domain Event** means the transition does not produce an approved meaningful
  business fact.
- “Updated” means the current view or relationship changes. It does not imply any
  technical storage design.

# 1. Top-level navigation map

```text
Loading
  |
  +--> Before Opening — Declarations Pending
  |       |
  |       +--> Before Opening — Blocked Department
  |       |       |
  |       |       +--> Before Opening — Declarations Pending
  |       |       +--> Before Opening — Ready to Open
  |       |
  |       +--> Before Opening — Ready to Open
  |               |
  |               +--> Opening Confirmation
  |                       |
  |                       +--> Cancel --> Before Opening — Ready to Open
  |                       |
  |                       +--> Opening in Progress
  |                               |
  |                               +--> Venue Open
  |                               +--> Before Opening
  |                               +--> Connection Degraded
  |                               +--> Unexpected Error
  |
  +--> Venue Open
  |       |
  |       +--> Venue Open — Attention Required
  |       |
  |       +--> Service Location Selection
  |               |
  |               +--> NFC Identification
  |               |       |
  |               |       +--> Service Location Context
  |               |       +--> Manual Identification
  |               |
  |               +--> Manual Identification
  |                       |
  |                       +--> Service Location Context
  |
  |   Service Location Context
  |       |
  |       +--> (Host escorts guests)
  |       +--> (Host introduces Responsible Waiter)
  |       +--> (Responsible Waiter accepts responsibility)
  |       +--> (Responsible Waiter opens Customer Group in authorized service context)
  |       +--> Host Dashboard receives confirmed live context
  |
  +--> Connection Degraded
  |       |
  |       +--> Retry --> Connection Restored
  |                       |
  |                       +--> correct authoritative state
  |
  +--> Unauthorized Host
  |
  +--> Unexpected Error
          |
          +--> Retry --> Loading
```

“Before Opening” after a rejected action means whichever of Declarations Pending,
Blocked Department, or Ready to Open matches the newly confirmed authoritative
state.

# 2. Initial state routing

## Transition 1 — Entry to Loading

### From and to

Application entry or Dashboard navigation → Loading.

### Trigger

The signed-in person enters or returns to the Host Dashboard.

### Business rule

No operational value or protected action may be presented as current until identity,
Venue, Business Date, Capabilities, connection, and authoritative Venue state are
established.

### Command

No Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None. The Dashboard retrieves permitted current context for Staff Member, Role,
Capability, Venue, and Business Date.

### Possible failures

- Session is absent or expired.
- Venue context is unavailable.
- Capability state cannot be confirmed.
- Central state cannot be reached.
- Retrieved facts are inconsistent.

### User feedback

Show loading, never zero or success. Route to the correct confirmed state,
Connection degraded, Unauthorized Host, or Unexpected error.

## Transition 2 — Loading to a before-opening state

### Trigger

Authoritative state confirms that the Venue is not open for the Business Date.

### Business rule

Before daily opening, guest arrivals, new Customer Groups, and Orders are forbidden.
Current department declarations determine which before-opening state applies.

### Command

No Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None. Venue, Business Date, Operational Department, Department Readiness, Staff
Member, and Capability are read.

### Possible failures

- Mandatory department setup is missing.
- A declaration is invalid.
- Current state becomes unavailable.

### User feedback

- Missing or NOT READY → Declarations Pending.
- Any BLOCKED → Blocked Department.
- Every mandatory department READY → Ready to Open.
- Setup or integrity failure → Critical feedback with no opening action.

## Transition 3 — Loading to Venue Open

### Trigger

Authoritative state confirms `Venue Opened for Business Date`.

### Business rule

The Venue-open state must be based on the confirmed daily opening fact, not an
expected time, cached assumption, or Role.

### Command

No Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None. Venue, Business Date, Opening Report, Service Locations, Customer Groups,
Responsible Waiters, accepted preparation state, and permitted recent history are
read.

### Possible failures

- Opening Report cannot be confirmed.
- Current Venue state and opening history disagree.
- Authorization changes while loading.

### User feedback

Proceed to Venue Open or Venue Open — Attention Required according to current
confirmed facts. An integrity conflict becomes Critical or Unexpected error; it is
not silently reconciled.

# 3. Venue-opening flow

## Transition 4 — Department declaration changes readiness

### From and to

Declarations Pending or Blocked Department → the applicable before-opening state.

### Trigger

The responsible person for an Operational Department makes a new current
declaration.

### Business rule

The responsible person verifies their own department. The status is READY, NOT
READY, or BLOCKED. NOT READY and BLOCKED require a reason. The Host cannot declare
for the department.

### Command

`Declare Department Readiness`.

This Command belongs to the department’s responsible person, not to the Host
Dashboard flow.

### Produced Domain Events

- `Department Readiness Declared`.

A separate Activity Log is not currently required for every ordinary declaration.
The declaration remains attributable in the Opening Report history.

### Updated Domain Concepts

- Operational Department.
- Department Readiness.
- Staff Member responsible for the declaration.
- Opening Report preparation context.
- Venue opening eligibility as a derived current condition.

### Possible failures

- Invalid readiness value.
- Missing reason for NOT READY or BLOCKED.
- Unknown or unauthorized responsible person.
- Declaration applies to the wrong Venue or Business Date.
- Connection or authoritative state is unavailable.

### User feedback

Update the affected department promptly. Re-evaluate the whole mandatory set:

- any BLOCKED → Blocked Department;
- otherwise any missing or NOT READY → Declarations Pending;
- all READY → Ready to Open.

Viewing or acknowledging a declaration produces no state change.

## Transition 5 — Declarations Pending to Blocked Department

### Trigger

A confirmed current declaration for any mandatory department is BLOCKED.

### Business rule

BLOCKED requires a reason and prevents opening. It does not judge the responsible
person.

### Command

No Host Command. The source transition follows `Declare Department Readiness`.

### Produced Domain Events

No additional Domain Event beyond `Department Readiness Declared`.

### Updated Domain Concepts

No additional update. Attention classification changes from the confirmed
Department Readiness fact.

### Possible failures

- Reason absent.
- Duplicate or out-of-order live notice.
- Older declaration appears after a newer declaration.

### User feedback

Present the blocker as Critical, name the department and responsible person, retain
OPEN VENUE as unavailable, and retrieve current authoritative state when ordering
is uncertain.

## Transition 6 — Blocked Department to Declarations Pending

### Trigger

No mandatory department remains BLOCKED, but at least one current declaration is
missing or NOT READY.

### Business rule

A resolved blocker does not automatically produce READY. The responsible person
must intentionally make a new valid declaration.

### Command

No Host Command. The source change follows `Declare Department Readiness`.

### Produced Domain Events

No additional Domain Event.

### Updated Domain Concepts

Attention classification and opening eligibility reflect the new confirmed
declarations.

### Possible failures

- The old BLOCKED fact remains authoritative.
- Another department becomes BLOCKED.
- Declaration conflict.

### User feedback

Remove the Critical blocker only after the new fact is confirmed. Continue to show
remaining Action required declarations.

## Transition 7 — Pending or Blocked to Ready to Open

### Trigger

Authoritative state confirms that every mandatory Operational Department is READY.

### Business rule

All READY creates eligibility only. It does not open the Venue. Host responsibility
and the required Capability are separately required for the opening action.

### Command

No Command. This is a derived eligibility transition.

### Produced Domain Events

None beyond the declarations that established READY.

### Updated Domain Concepts

Venue opening eligibility is now true as a derived condition. Venue remains closed.

### Possible failures

- A declaration changes before action.
- Capability cannot be confirmed.
- A mandatory department is missing from the set.
- Connection becomes degraded.

### User feedback

Show all-ready confirmation, Venue still closed, authority status, consequences,
and OPEN VENUE only when all action conditions are current.

## Transition 8 — Ready to Open to Opening Confirmation

### Trigger

An eligible and authorized Host selects OPEN VENUE.

### Business rule

OPEN VENUE is intentional and consequential. The Host Role alone is insufficient.
Every mandatory department must remain READY.

### Command

No Command yet. Selecting the action opens confirmation; it is not the business
intention’s accepted execution.

### Produced Domain Events

None.

### Updated Domain Concepts

None.

### Possible failures

- Host lacks responsibility.
- Required Capability is absent or revoked.
- Readiness changes.
- State is stale.

### User feedback

Show Venue, Business Date, all-ready summary, Host identity, and consequences.
Disable or exit confirmation if any condition changes.

## Transition 9 — Opening Confirmation cancelled

### From and to

Opening Confirmation → Ready to Open or the newly applicable before-opening state.

### Trigger

The Host cancels or uses Back before submission.

### Business rule

Cancellation before the Command is accepted performs no business action. Current
readiness must be retrieved or retained as confirmed, not assumed.

### Command

No Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None.

### Possible failures

- Readiness changes while confirmation is open.
- Session expires.
- Connection degrades.

### User feedback

Return to the current authoritative state. Do not show an opening success or
failure message.

## Transition 10 — Opening Confirmation to Opening in Progress

### Trigger

The Host deliberately confirms OPEN VENUE and the intention is accepted for
evaluation.

### Business rule

At acceptance time:

- every mandatory department is READY;
- the actor satisfies Host responsibility;
- the actor holds the required Venue-opening Capability;
- the Venue is not already open for the Business Date;
- central authoritative state is available.

The official Capability name remains unresolved and is not invented here.

### Command

`Open Venue for Business Date`.

### Produced Domain Events

None while the final outcome remains pending.

`Venue Opening Started` is explicitly not an official Domain Event.

### Updated Domain Concepts

No completed business concept changes while the result is unknown. The interaction
retains the intended Venue, Business Date, Host, and request identity for safe
outcome checking.

### Possible failures

- A business rule rejects the intention.
- Duplicate interaction.
- Session expires.
- Connection is lost before the outcome reaches the Host.
- Outcome is unknown.

### User feedback

Show Opening in Progress, disable duplicate submission, and never claim success
until authoritative confirmation.

## Transition 11 — Opening succeeds

### From and to

Opening in Progress → Venue Open or Venue Open — Attention Required.

### Trigger

The central system confirms successful completion of Open Venue for Business Date.

### Business rule

All mandatory departments were READY and the actor had both Host responsibility and
the required Capability. Opening is one intentional completed outcome.

### Command

The completed outcome of `Open Venue for Business Date`.

### Produced Domain Events

- `Venue Opened for Business Date`.
- `Activity Logged` for the Capability-protected opening action.

The Opening Report becomes official as part of `Venue Opened for Business Date`.
There is no separate `Opening Report Created` event.

### Updated Domain Concepts

- Venue is open for the Business Date.
- Business Date has an official operational start.
- Opening Report becomes permanent.
- Host is recorded as the actor.
- Operational Department readiness at opening is preserved.
- Activity Log records the sensitive action.
- Guest arrivals, new Customer Groups, and Orders become allowed under their own
  separate rules.
- Daily operational timers and measures begin.

No Customer Group, Bill, Financial Obligation, Order, transfer, or Payment is
created by this transition.

### Possible failures

- Success notification is missed or duplicated.
- Opening Report is unavailable after claimed success.
- Current state conflicts with the event.

### User feedback

Confirm official opening time, Venue, Business Date, Host, and Opening Report
availability. Then show the correct Venue-open state. Retrieve authoritative state
if live notification and current state disagree.

## Transition 12 — Opening is rejected

### From and to

Opening in Progress → applicable Before Opening state or Unauthorized Host.

### Trigger

The opening intention is definitively rejected before Venue opening occurs.

### Business rule

The Venue remains closed. No accepted `Venue Opening Rejected` Domain Event exists
in the current catalogue, so the prototype must not name one.

### Command

Rejected `Open Venue for Business Date` intention.

### Produced Domain Events

No approved Venue-opening rejection Domain Event.

A security-relevant or accountability-relevant failed action may require logging
under approved rules, but this flow does not invent that outcome.

### Updated Domain Concepts

No Venue-opening business state changes.

### Possible failures

- Readiness changed.
- Venue was opened by another authorized Host.
- Capability was revoked.
- Request was duplicated.
- Technical failure is confused with business rejection.

### User feedback

Explain in non-technical language that the Venue was not opened. Retrieve
authoritative state and route accordingly. Do not invite a blind repeat.

## Transition 13 — Opening outcome becomes uncertain

### From and to

Opening in Progress → Connection Degraded or Unexpected Error.

### Trigger

The Dashboard loses the ability to determine whether opening completed.

### Business rule

An uncertain outcome is neither success nor failure. The same opening intention must
not be repeated until authoritative state is known.

### Command

No new Command.

### Produced Domain Events

None asserted by the Dashboard.

### Updated Domain Concepts

None asserted until reconciliation.

### Possible failures

- Connection loss.
- Session expiration.
- Response lost after successful completion.
- Partial operational information.

### User feedback

Show the pending outcome, last confirmed time, and disabled consequential actions.
Retry retrieves current authoritative state; it does not resubmit OPEN VENUE.

# 4. Venue-open operational flow

## Transition 14 — Venue Open to Attention Required

### Trigger

A confirmed current fact meets the approved Critical or Action required criteria.

### Business rule

Attention is derived from approved current facts. It cannot create a new issue,
complaint, weather, prediction, or employee-performance concept.

### Command

No Command.

### Produced Domain Events

No additional Domain Event. The source may be an existing event such as:

- `Service Location Made Unavailable`;
- `Service Location Reassigned to Zone`;
- `Transfer Rejected`;
- a relevant existing rejected action;
- an accepted current preparation event.

An invariant violation or connection risk may require attention without a new
Domain Event.

### Updated Domain Concepts

No additional business update. Attention classification and the affected permitted
context change in the Dashboard.

### Possible failures

- Duplicate or out-of-order notification.
- Source fact no longer current.
- Detail not permitted to the Host.
- An unapproved threshold is used to label work delayed.

### User feedback

Place the highest-priority item first; identify fact, reason, context, time, and next
human step. Retrieve current state before keeping an uncertain alert.

## Transition 15 — Attention Required to Venue Open

### Trigger

Authoritative state confirms that no Critical or Action required item remains.

### Business rule

Viewing or acknowledging an item does not resolve it. Resolution follows a new
confirmed source fact. Awareness only information may remain.

### Command

No Host Command unless the source workflow separately defines one. The Dashboard
does not invent a resolution Command.

### Produced Domain Events

Only the existing source workflow event, if any. No generic `Attention Resolved`
event exists.

### Updated Domain Concepts

Attention classification changes. The underlying Domain Concept changes only
through its own approved workflow.

### Possible failures

- Item was merely dismissed or acknowledged.
- Source state is stale.
- Several related facts were incorrectly treated as one resolution.

### User feedback

Return to Venue Open only after confirmed resolution. The empty queue says no
confirmed Host action currently requires attention, not that the operation is
perfect.

## Transition 16 — Venue Open to Service Location Selection

### Trigger

The Host chooses to locate or identify a Service Location during arrival, seating,
or operational coordination.

### Business rule

The Venue is open. Selection is context retrieval, not occupancy, reservation,
assignment, or Customer Group opening.

### Command

No Command for browsing or filtering.

### Produced Domain Events

None.

### Updated Domain Concepts

None. Current Service Location identity, type, Area, Zone, and state are read.

### Possible failures

- Filter hides relevant locations.
- Current state is unavailable.
- A location appears physically different from the central state.
- No Service Locations are configured.

### User feedback

Show active filters, current confirmation state, and Available, Occupied, and
Unavailable in official language. Never infer availability from appearance.

## Transition 17 — Selection to NFC Identification

### Trigger

On a supported device, the Host intentionally begins NFC identification at a
physical Service Location.

### Business rule

The tag contains only a stable non-sensitive identifier or secure application link.
It grants no Capability and contains no changing operational or financial data.

### Command

`Identify Service Location`.

This business-facing Command produces no official Domain Event.

### Produced Domain Events

None.

`NFC Scanned` and `Service Location Identified` are not official Domain Events.

### Updated Domain Concepts

No Domain Concept changes. The Service Location Digital Identity resolves to the
enduring Service Location, and its current context is retrieved from the central
system.

### Possible failures

- NFC unsupported.
- Tag missing, damaged, or unreadable.
- Identifier is invalid or inactive.
- Identifier does not resolve safely.
- One marker appears to resolve ambiguously.
- Connection cannot retrieve current context.
- User is signed out or lacks access.

### User feedback

- Success: show the resolved Service Location and current confirmed state, while
  stating no operational or financial action occurred.
- Failure: explain that NFC did not identify the location and keep manual lookup
  immediately available.
- Ambiguity or mismatch: do not choose a location; require manual verification and
  human escalation.

## Transition 18 — Selection to Manual Identification

### Trigger

The Host selects manual lookup initially or after NFC is unavailable or fails.

### Business rule

Manual lookup by visible name or number must reach the same enduring Service
Location as NFC. It does not weaken authentication, permissions, or business rules.

### Command

`Identify Service Location`.

### Produced Domain Events

None.

### Updated Domain Concepts

No Domain Concept changes. The chosen visible identity resolves to the Service
Location and current context is retrieved centrally.

### Possible failures

- No exact location found.
- Several possible matches.
- Location is retired or unavailable.
- Current state cannot be retrieved.
- User chooses the wrong visible name or number.

### User feedback

Require the Host to verify the exact identity and state. Do not select silently when
results are ambiguous. State that identification alone performs no business action.

## Transition 19 — Identification to Service Location Context

### Trigger

NFC or manual identification resolves exactly one Service Location and retrieves
current authoritative state.

### Business rule

- One active marker must not resolve to more than one Service Location.
- One Service Location may have at most one Active Customer Group.
- Identification does not authorize or perform an action.
- Occupied and Unavailable are not Available.

### Command

Completed outcome of `Identify Service Location`, with no official Domain Event.

### Produced Domain Events

None.

### Updated Domain Concepts

None. Permitted current context is displayed:

- Service Location;
- Service Location Digital Identity;
- Area;
- Zone;
- availability or occupancy;
- current Customer Group and Responsible Waiter only where authorized.

### Possible failures

- Physical and digital identity appear inconsistent.
- State changes during retrieval.
- Active Customer Group invariant is violated.
- Detail is not authorized.

### User feedback

Show exact visible name or number, type, Area, Zone, current state, confirmation
time, and allowed limited context. An invariant violation becomes Critical and
blocks unsafe action. A mismatch uses manual verification and escalation; no
unapproved correction workflow is offered.

# 5. Guest Arrival and Responsible Waiter boundary

The Host Dashboard supports the operational path below but does not turn every
human step into a screen or business transaction.

```text
Venue Open
  ↓
(Guest enters)
  ↓
(Host notices and greets guest)
  ↓
(Host assesses practical needs)
  ↓
(Host checks current availability)
  ↓
(Human waiting or seating decision)
  ↓
(Host escorts guests)
  ↓
NFC or Manual Service Location Identification
  ↓
(Host introduces Responsible Waiter)
  ↓
(Eligible Responsible Waiter accepts responsibility)
  ↓
(Responsible Waiter intentionally opens Customer Group in authorized context)
  ↓
Host Dashboard receives confirmed Customer Group and responsibility context
```

Greeting, needs assessment, waiting, escort, and introduction are human workflow
actions. The Dashboard must not invent a digital waiting list, guest record,
reservation, automatic assignment, or Host-owned opening action.

## Transition 20 — Service Location Context to human escort and handoff

### Trigger

The Host confirms the selected Service Location is suitable and currently
Available, escorts the guests, and introduces the intended Responsible Waiter.

### Business rule

The Host uses human judgment. Seating and introduction do not create a Customer
Group, occupy the location, assign responsibility as a completed digital fact, or
create a financial obligation.

### Command

No Host Dashboard Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None.

### Possible failures

- Location becomes unavailable or occupied during escort.
- Wrong location is identified.
- Intended Responsible Waiter is unavailable or ineligible.
- Physical and digital state disagree.
- Guest changes their mind.

### User feedback

Recheck current state before handoff. Return to Service Location Selection when the
location is no longer safe to offer. Coordinate another eligible waiter through the
approved human process; do not assign automatically.

## Transition 21 — Responsible Waiter accepts responsibility

### Trigger

One eligible Staff Member accepts the Responsible Waiter responsibility as part of
the approved opening process.

### Business rule

Exactly one eligible Responsible Waiter is required. Role alone does not authorize
the protected action. The exact standalone assignment and handover process remains
Command gated; the prototype must not invent who may assign, how acceptance is
recorded separately, or how reassignment works.

### Command

`Assign Responsible Waiter`, performed outside the Host’s protected action set.

### Produced Domain Events

On valid Customer Group opening:

- `Responsible Waiter Assigned`.

Whether assignment is separately completed before opening is not resolved here.

### Updated Domain Concepts

- Responsible Waiter relationship for the opening Customer Group context.
- Staff Member responsibility.
- History after the opening succeeds.

### Possible failures

- No eligible waiter.
- More than one waiter appears assigned.
- Capability absent.
- Assignment authority or acceptance is unclear.
- Service Location is no longer Available.

### User feedback

The Host sees only confirmed responsibility context. The Host is directed to
continue human coordination; no automatic assignment or invented assignment
control appears.

## Transition 22 — Responsible Waiter opens Customer Group

### Trigger

The eligible Responsible Waiter intentionally performs official opening at the
correct Available Service Location.

### Business rule

- Venue is officially open.
- Location identity is certain and current.
- Location is Available and has no Active Customer Group.
- Exactly one eligible Responsible Waiter accepts responsibility.
- The Responsible Waiter holds Open Customer Group.
- Only the Responsible Waiter opens the group.
- Opening succeeds completely or no Customer Group is created.
- Beach Sunbed opening creates the immediate approved Financial Obligation.
- Other location types create no Bill until a first approved Financial Obligation.

### Command

`Open Customer Group`, performed in the Responsible Waiter’s authorized service
context, not by the Host Dashboard.

### Produced Domain Events

For every valid opening:

- `Responsible Waiter Assigned`;
- `Customer Group Opened`;
- `Activity Logged`.

For a Beach Sunbed, the same atomic outcome also produces:

- `Financial Obligation Created`;
- `Bill Created`;
- `Bill Line Added`.

For other Service Location types, the financial events occur only when the first
approved Financial Obligation later arises.

### Updated Domain Concepts

- Customer Group becomes Active.
- Service Location becomes Occupied.
- Responsible Waiter is recorded.
- History begins.
- For Beach Sunbed: Financial Obligation, Bill, and Bill Line are created.
- For another type: Customer Group may remain Active without a Bill.

### Possible failures

- Venue not open.
- Service Location not Available.
- Duplicate active Customer Group.
- Wrong or uncertain location identity.
- Responsible Waiter not eligible or unauthorized.
- Open Customer Group Capability absent.
- Beach Sunbed obligation cannot be confirmed.
- Connection or durable outcome is uncertain.

### User feedback

Only the Responsible Waiter receives the actionable outcome. The Host Dashboard
updates after confirmed events to show Occupied Service Location, Active Customer
Group, and permitted Responsible Waiter context. It must not display false success
or financial detail.

## Transition 23 — Customer Group opening rejected

### Trigger

The Responsible Waiter’s intention fails a business rule.

### Business rule

No partial Customer Group, occupancy, Bill, or charge may remain. The Host does not
override the rejection.

### Command

Rejected `Open Customer Group`.

### Produced Domain Events

The current catalogue does not define `Customer Group Opening Rejected` as an
official Domain Event.

### Updated Domain Concepts

None from the rejected opening.

### Possible failures

- Location was taken by another Customer Group.
- Eligibility or Capability changed.
- Venue state changed.
- Outcome is technically uncertain rather than definitively rejected.

### User feedback

The Host sees refreshed location and responsibility facts where relevant. Return to
selection or human coordination. If outcome is uncertain, block unsafe repetition
until authoritative state is retrieved.

# 6. Connectivity transitions

## Transition 24 — Any live state to Connection Degraded

### Trigger

The Dashboard can no longer guarantee that displayed state is current.

### Business rule

The central system remains the source of truth. Cached information cannot authorize
consequential action. Full offline operation is excluded.

### Command

No Command.

### Produced Domain Events

None.

### Updated Domain Concepts

None. Connection and freshness are presentation conditions, not new business
entities or events.

### Possible failures

- Loss occurs before an action.
- Loss occurs after submission but before outcome.
- Some sections update while others do not.
- Cached information exceeds an as-yet-unapproved freshness boundary.

### User feedback

Show degraded status, last confirmed time, uncertain pending outcomes, and
read-only cached content only where approved. Disable consequential actions and
provide manual fallback.

## Transition 25 — Connection Degraded to Connection Restored

### Trigger

Network transport returns or a Retry can reach the central system.

### Business rule

Connectivity alone does not prove that the operational state is current.
Authoritative resynchronization must complete.

### Command

No Command. Retry retrieves current state and pending outcomes.

### Produced Domain Events

None.

### Updated Domain Concepts

None until authoritative business facts are retrieved.

### Possible failures

- Transport is unstable.
- Session expired.
- Pending action cannot yet be resolved.
- Facts arrive duplicated or out of order.

### User feedback

Show Connection Restored — Checking Current State. Keep consequential actions
disabled.

## Transition 26 — Connection Restored to current authoritative state

### Trigger

Identity, Capabilities, Venue state, and relevant current business facts have been
reconciled with the central source.

### Business rule

Newer confirmed state wins over stale presentation. Missed or duplicated live
notices cannot create duplicate outcomes.

### Command

No new Command.

### Produced Domain Events

None produced by resynchronization. Existing confirmed events are retrieved.

### Updated Domain Concepts

No new business change is asserted. The Dashboard view is updated to the actual
current state.

### Possible failures

- Invariant conflict.
- Capability differs from the earlier session.
- Pending action succeeded while disconnected.
- Pending action failed or remains uncertain.

### User feedback

Route to the correct Loading-resolved state. If OPEN VENUE succeeded, show its
confirmed outcome once and continue to Venue Open. If authority changed, continue
to Unauthorized Host. If state remains unsafe, continue to Unexpected error.

# 7. Authorization and session transitions

## Transition 27 — Current Capability revoked or responsibility removed

### Trigger

Authoritative state confirms a Capability revocation or Role-responsibility change.

### Business rule

Roles describe responsibility and do not grant authority. Revocation prevents new
protected actions but does not rewrite history.

### Command

No Host Dashboard Command. The source governance action is outside this flow.

### Produced Domain Events

The source may produce:

- `Capability Revoked`;
- `Role Removed`;
- `Activity Logged`.

### Updated Domain Concepts

- Staff Member’s current Capability or Role relationship.
- Available Dashboard actions.

### Possible failures

- Change arrives while confirmation is open.
- Change arrives after a Command was accepted.
- Cached authority appears newer than current authority.

### User feedback

Before submission, cancel the protected action and show Limited Host Access. After
submission, preserve the pending outcome and retrieve it; revocation does not erase
an already completed fact. Never execute a queued future action.

## Transition 28 — Capability granted or responsibility restored

### Trigger

Authoritative state confirms the relevant current authority.

### Business rule

Authority permits an attempt; it does not bypass readiness or any other business
rule. A new grant never automatically performs the action.

### Command

No Host Dashboard Command. The source governance action is outside this flow.

### Produced Domain Events

The source may produce:

- `Capability Granted`;
- `Role Assigned`;
- `Activity Logged`.

### Updated Domain Concepts

- Staff Member’s current authority.
- Available actions after all rules are re-evaluated.

### Possible failures

- Capability has the wrong Venue scope.
- Host responsibility is still absent.
- Readiness is no longer all READY.

### User feedback

Refresh the permitted state. Expose OPEN VENUE only when every independent
condition is satisfied; do not resume an earlier cancelled confirmation.

## Transition 29 — Session expiration

### Trigger

The individual signed-in session is no longer valid.

### Business rule

Protected actions require an authenticated individual. Session loss cannot convert
an uncertain outcome into failure or authorize another person.

### Command

No business Command.

### Produced Domain Events

None defined by this product flow.

### Updated Domain Concepts

None.

### Possible failures

- Expiration occurs during ordinary viewing.
- Expiration occurs in confirmation before submission.
- Expiration occurs after submission while outcome is pending.

### User feedback

- Before submission: discard only the unsubmitted confirmation and require sign-in.
- After submission: retain the pending action identity, require sign-in, and retrieve
  authoritative outcome before permitting repetition.
- After recovery: reload current identity, Venue, Business Date, Capability, and
  operational state.

# 8. Navigation rules

## Back navigation

- From ordinary permitted detail, Back returns to the prior Dashboard context with
  filters and review position preserved where safe.
- From Opening Confirmation before submission, Back equals Cancel.
- From Opening in Progress, Back cannot expose a second OPEN VENUE action while the
  outcome is pending.
- From Connection Restored, Back cannot return to cached content as if it were
  current.
- From Service Location context, Back returns to the selection result or Dashboard
  without changing the Service Location.
- Back never performs a Business Command and produces no Domain Event.

## Cancellation

- Only an unsubmitted Opening Confirmation has a defined cancellation in this
  Dashboard.
- Cancellation creates no Venue opening and no Domain Event.
- A submitted Command cannot be “cancelled” by navigation.
- NFC identification may be abandoned before resolution without business effect.
- No cancellation control may imply Customer Group cancellation, Bill reversal, or
  another unapproved business action.

## Retry

- Retry retrieves current authoritative state or the outcome of an already
  submitted intention.
- Retry must not resubmit OPEN VENUE.
- Retry after NFC failure may start a new identification attempt or move to manual
  lookup; neither creates a Domain Event.
- Retry is unavailable when it would conceal which business intention is pending.
- Feedback distinguishes reconnecting, retrieving, rejected, failed, and confirmed.

## Lost connection

- Move to Connection Degraded when currentness cannot be guaranteed.
- Show last confirmed synchronization time.
- Clearly label any approved cache as read-only.
- Disable consequential actions.
- Continue through approved manual operational practice.
- Full offline operation is not supported.
- If a Command outcome is uncertain, preserve its identity until reconciliation.

## Session expiration

- Require the user to establish their own identity again.
- Preserve but do not expose sensitive pending context beyond the approved recovery
  boundary.
- After recovery, reload authority and business state.
- Never let another person inherit the prior person’s protected action.

## Capability changes

- Re-evaluate action availability promptly from authoritative state.
- Revocation prevents new action immediately after confirmation.
- A grant reveals an action only when all other rules pass.
- Role changes and Capability changes remain separate.
- No authority change automatically executes, retries, cancels, or reverses a
  Business Command.

## Refresh behavior

- Refresh retrieves authoritative current state; it does not clear Attention items
  by itself.
- Refresh does not generate Domain Events.
- Preserve known pending action identity across refresh.
- Do not replace unavailable data with zero.
- Deduplicate repeated events and do not apply older state over newer confirmed
  state.
- Preserve user filter context only when doing so cannot hide a changed Critical
  condition.
- If refreshed state changes the applicable screen, route to that screen and
  explain the confirmed change.

# 9. Transition guard summary

| Intended transition | Required guard | If guard fails |
|---|---|---|
| Before Opening → Opening Confirmation | Every mandatory department READY; current authoritative state; Host responsibility; required Capability | Remain closed; show the exact confirmed blocker |
| Opening Confirmation → Opening in Progress | Same guards rechecked; deliberate confirmation; no opening already completed | Do not submit; route to current safe state |
| Opening in Progress → Venue Open | `Venue Opened for Business Date` confirmed authoritatively | Never claim success; reconcile or return to closed state |
| Venue Open → Service Location Context | Venue open; exact identity resolved; current context retrieved; permitted access | Use manual fallback, retry, or block unsafe context |
| Service Location Context → Customer Group Opened | Performed by eligible Responsible Waiter with Open Customer Group; location Available; all opening rules pass | No group, occupancy, Bill, or charge is partially created |
| Any current state → Protected action | Individual signed in; explicit current Capability; business responsibility and all rules satisfied | Action unavailable; current facts remain unchanged |
| Degraded → Current state | Authoritative resynchronization complete | Remain degraded or show error |

# 10. Prototype stop boundary

The clickable prototype may end the Host-led Guest Arrival path at:

> Responsible Waiter introduced; official Customer Group opening remains a
> Responsible Waiter action.

It may also demonstrate the Host Dashboard receiving the later confirmed
`Customer Group Opened` and `Responsible Waiter Assigned` facts.

It must not design the Responsible Waiter’s opening interface, the exact standalone
assignment mechanism, Customer Group completion, a Service Location mismatch case,
or any other unresolved workflow as part of this Host Dashboard prototype.
