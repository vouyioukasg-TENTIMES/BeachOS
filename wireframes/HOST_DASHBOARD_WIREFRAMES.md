# BeachOS Host Dashboard — Functional Wireframes

## Document purpose

This document translates the approved Host Dashboard specification into functional
screen descriptions. It is a handoff for low-fidelity prototyping. It defines what
must be present, what may happen, and what must remain unavailable. It does not
define visual design.

The wireframes answer one operational question:

> What requires the Host’s attention right now?

The descriptions use only approved repository behavior. An unresolved decision is
identified as unresolved rather than answered here.

## Shared frame

Every Dashboard state uses the following persistent functional frame where the
information is known and authorized:

- signed-in Staff Member identity;
- current Venue;
- current Business Date;
- confirmed Venue state;
- connection and information-freshness state;
- access to the Host Dashboard home;
- a route to manual Service Location lookup when the Venue is open;
- a route to sign out;
- no financial totals, Payment amounts, personal guest profiles, VIP labels,
  employee scores, or unrestricted Activity Logs.

Critical and Action required information must remain ahead of general operational
information. State meaning must be expressed in words and must not depend on color.

The following terms in this document describe functional regions, not prescribed
visual components:

- **status context** — identity, Venue, Business Date, operating state, and
  connection state;
- **attention summary** — the highest-priority confirmed fact requiring awareness
  or action;
- **content section** — a bounded group of related operational information;
- **action** — an available human intention, subject to Capability and business
  rules;
- **disabled action** — a visible action that cannot currently be performed, with
  its reason;
- **unavailable action** — an action that must not be offered at all.

## Shared interaction constraints

- OPEN VENUE is the only consequential primary action defined for the Host
  Dashboard itself.
- OPEN VENUE requires Host responsibility, the required Venue-opening Capability,
  every mandatory Operational Department to be READY, current authoritative
  state, and intentional confirmation.
- The official name of the Venue-opening Capability remains unresolved. Prototype
  copy must say “required Venue-opening Capability” or use a visibly marked
  placeholder; it must not invent a permanent Capability name.
- The Host may locate and identify a Service Location. Identification retrieves
  context only.
- NFC or manual identification never creates a Customer Group, Bill, Financial
  Obligation, Order, transfer, or Payment and never grants authority.
- The Host Dashboard provides no action for the Host to open a Customer Group.
- The Responsible Waiter intentionally opens the Customer Group in their authorized
  service context, not from a Host action disguised as a handoff.
- Cached information is never treated as current authority for a consequential
  action.
- Empty, loading, stale, unavailable, failed, rejected, and successful states must
  remain distinct.
- The prototype must not invent waiting-list, reservation, VIP, complaint,
  incident, weather, prediction, employee-scoring, Venue-closing, Customer Group
  completion, or Bill-reopening functionality.

# 1. Loading

## Screen title

Host Dashboard

## Screen objective

Establish the signed-in identity, Venue, Business Date, Capabilities, Venue-opening
state, connection state, and current operational context before displaying any
actionable result.

## User Goal

Reach a trustworthy current operating state without interpreting missing
information as “all clear.”

## Visible sections

1. Status context.
2. Loading explanation.
3. Connection check.

Operational Dashboard sections are represented only as unresolved loading regions.
They must not show zero values or empty-state messages while their state is unknown.

## Primary information

- “Loading current Venue state.”
- Known signed-in identity, if already confirmed.
- Known Venue, if already confirmed.
- Connection check in progress.

## Secondary information

- Business Date retrieval in progress.
- Capability retrieval in progress.
- Last confirmed synchronization time only if an earlier safe session context is
  available.

## Available actions

- None while initial authoritative state is being established.

## Disabled actions

- OPEN VENUE.
- Service Location identification.
- Manual Service Location lookup.
- Any other protected or consequential action.

The reason is that operating state and authority are not yet confirmed.

## Empty states

There is no valid empty state. Missing information remains loading, unavailable, or
failed; it is never displayed as zero.

## Error states

- Identity cannot be established: continue to Unauthorized Host or the approved
  sign-in recovery path.
- Connection cannot establish current state but safe prior context exists: continue
  to Connection degraded.
- No safe state can be established: continue to Unexpected error.

## Navigation options

- Sign out, when a known session exists.
- No navigation into operational detail until safe context is known.

## Primary CTA

None.

## Secondary CTA

Sign out, when available.

## Possible mistakes

- Treating an unresolved department count as zero.
- Showing Venue open before authoritative confirmation.
- Briefly exposing an action before Capabilities load.
- Redirecting to the previous state without checking the current Business Date.

## System feedback

- State retrieval is visibly in progress.
- No success language appears.
- The next confirmed screen replaces Loading only after its required context is
  known.

## Required permissions

A valid signed-in Staff Member session is required to proceed to permitted Host
operational information. Loading itself grants no authority.

# 2. Before Opening — Declarations Pending

## Screen title

Opening Readiness

## Screen objective

Show why the Venue is not yet eligible to open and make the Host’s coordination
work clear without transferring department verification to the Host.

## User Goal

Identify every missing or NOT READY mandatory department and follow up with the
correct responsible person.

## Visible sections

1. Status context: Venue closed for the Business Date.
2. Attention Queue.
3. Opening Readiness Panel.
4. Department Status.
5. Recent Important Activity, limited to permitted opening facts.

Service Location Overview and Live Operation Summary are not active operational
sections before opening.

## Primary information

- Every mandatory Operational Department.
- Each responsible person.
- Current declaration: READY, NOT READY, or missing.
- Mandatory reason for every NOT READY declaration.
- Opening eligibility: not eligible.
- Highest-priority Action required items.

## Secondary information

- Declaration confirmation time.
- Approved comments.
- Count of mandatory departments by current status.
- Relevant recent `Department Readiness Declared` facts.
- Planned opening comparison only if an already approved and confirmed planned
  opening time exists. The screen must not create or infer one.

## Available actions

- Review a department’s readiness detail.
- Identify the responsible person for human follow-up.
- Acknowledge an Action required item without marking it resolved.
- Return to the complete department list.
- Refresh or resynchronize current state.

Follow-up remains human operational communication. No task, message, or incident
record is implied.

## Disabled actions

- OPEN VENUE, with the reason that one or more mandatory declarations are missing or
  NOT READY.
- Changing another department’s declaration.
- Marking a department READY on its behalf.
- Guest Arrival, new Customer Group, and Order actions.

## Empty states

- No mandatory departments configured is a setup error, not an eligible or healthy
  state.
- No recent relevant activity may be stated as such without claiming that no
  opening activity occurred.

## Error states

- A NOT READY declaration without a reason is invalid and cannot satisfy readiness.
- A missing responsible person is a blocking setup problem.
- If current readiness cannot be confirmed, opening remains unavailable and the
  state moves to Connection degraded or Unexpected error as appropriate.

## Navigation options

- Open a department’s permitted detail.
- Return to Dashboard summary.
- Sign out.

## Primary CTA

Review unresolved readiness.

## Secondary CTA

Refresh current state.

## Possible mistakes

- Assuming no response means READY.
- Treating a reason as optional.
- Allowing the Host to edit the department’s declaration.
- Hiding READY departments so completely that the full opening picture cannot be
  checked.
- Treating acknowledgment as resolution.

## System feedback

- Every unresolved department is named.
- OPEN VENUE explains why it is unavailable.
- A new declaration updates the current status promptly.
- An item clears only after a new valid declaration changes the source fact.

## Required permissions

- Signed-in Host operational access to view opening readiness.
- No Capability is implied for changing department declarations.
- OPEN VENUE remains subject to the separate unresolved-name Venue-opening
  Capability and all opening rules.

# 3. Before Opening — Blocked Department

## Screen title

Opening Blocked

## Screen objective

Make a confirmed mandatory blocker impossible to overlook and direct the Host
toward human coordination and escalation.

## User Goal

Understand the blocker, its owner, and the required human follow-up while keeping
the Venue closed.

## Visible sections

1. Status context: Venue closed.
2. Critical Attention item.
3. Opening Readiness Panel.
4. Department Status.
5. Recent Important Activity.

## Primary information

- BLOCKED status.
- Affected mandatory Operational Department.
- Responsible person.
- Mandatory blocker reason.
- Confirmation time.
- Opening eligibility: not eligible.

If several departments are BLOCKED, all remain accessible and the summary states
the number affected without ranking employees.

## Secondary information

- Approved department comment.
- Other missing or NOT READY declarations.
- READY departments.
- Related declaration history permitted for the opening context.

## Available actions

- Review blocker detail.
- Identify the responsible person.
- Review other unresolved departments.
- Acknowledge that the Host has seen the item without changing its status.
- Refresh or resynchronize.

Escalation is a human action under Venue practice. No digital escalation workflow is
created.

## Disabled actions

- OPEN VENUE.
- Dismiss blocker as resolved.
- Override BLOCKED.
- Declare READY for the department.
- Begin Guest Arrival or Customer Group work.

## Empty states

This state cannot have an empty blocker. If no current mandatory department is
BLOCKED, transition to the appropriate pending or ready state.

## Error states

- BLOCKED without a reason is invalid.
- Unknown department owner is a setup blocker.
- Conflicting declaration state requires authoritative resynchronization and no
  opening action.

## Navigation options

- Department detail.
- Complete Opening Readiness.
- Dashboard summary.
- Sign out.

## Primary CTA

Review blocking issue.

## Secondary CTA

Review all unresolved departments.

## Possible mistakes

- Using blame language.
- Allowing acknowledgment to clear the blocker.
- Automatically changing BLOCKED to READY when an issue appears resolved.
- Showing an opening-time target as authority to bypass readiness.

## System feedback

- The blocker remains visible until the responsible person makes a later valid
  declaration.
- A changed declaration returns the user to blocked, pending, or ready state based
  on the complete current readiness set.
- No elapsed time automatically changes the status.

## Required permissions

Signed-in Host operational access permits review. The Host has no implied authority
to declare for another department or bypass DEC-039.

# 4. Before Opening — Ready to Open

## Screen title

Ready to Open

## Screen objective

Confirm that every mandatory department is READY and distinguish opening
eligibility from the Host’s authority to execute OPEN VENUE.

## User Goal

Review the complete readiness picture and, if authorized, intentionally begin the
Venue-opening action.

## Visible sections

1. Status context: Venue closed, eligible to open.
2. Opening Readiness Panel.
3. Department Status.
4. Authorization status.
5. Consequence summary.
6. Recent Important Activity.

## Primary information

- All mandatory departments are READY.
- Responsible person for every declaration.
- Current confirmation times.
- Venue remains closed until intentional opening succeeds.
- Whether the signed-in person satisfies Host responsibility.
- Whether the signed-in person holds the required Venue-opening Capability.

## Secondary information

- Approved comments.
- Business Date.
- Planned opening comparison only when an approved, confirmed value already exists.
- The opening consequences:
  - official operational start;
  - guest arrivals allowed;
  - new Customer Groups allowed under their own rules;
  - Orders allowed under their own rules;
  - daily operational timers and measures begin;
  - permanent Opening Report becomes official.
- Explicit statement that opening creates no Customer Group, Bill, Financial
  Obligation, Order, transfer, or Payment.

## Available actions

- OPEN VENUE, only for the authorized Host under authoritative current state.
- Review complete readiness.
- Refresh current state.

## Disabled actions

- OPEN VENUE when Host responsibility or the required Capability is absent.
- OPEN VENUE when state becomes stale or any department changes away from READY.
- Changing department declarations.
- Guest Arrival, Customer Group, and Order actions before confirmed opening.

## Empty states

There is no valid empty readiness state. Every mandatory department must be shown
and READY.

## Error states

- Capability cannot be confirmed: OPEN VENUE unavailable.
- Readiness changed during review: return to pending or blocked.
- Current state cannot be confirmed: Connection degraded or Unexpected error.

## Navigation options

- Review department detail.
- Dashboard summary.
- Sign out.

## Primary CTA

OPEN VENUE.

## Secondary CTA

Review readiness.

## Possible mistakes

- Treating eligibility as automatic opening.
- Treating the Host Role as sufficient authority.
- Hiding the fact that the Venue is still closed.
- Letting a stale all-ready snapshot authorize opening.
- Assigning the unresolved Capability a new official name.

## System feedback

- OPEN VENUE remains clearly consequential.
- Selecting it opens the Opening confirmation state; it does not immediately claim
  success.
- Any incoming non-READY declaration removes eligibility before execution.

## Required permissions

- Host responsibility.
- Required Venue-opening Capability, official name unresolved.
- All business rules still apply.

# 5. Opening Confirmation

## Screen title

Confirm Venue Opening

## Screen objective

Require one deliberate confirmation of the consequential OPEN VENUE action while
showing its scope and consequences.

## User Goal

Verify that the intended Venue and Business Date are correct and intentionally
confirm or cancel.

## Visible sections

1. Confirmation context.
2. Readiness summary.
3. Consequence summary.
4. Authority and freshness status.

The underlying Dashboard context remains identifiable, but no unrelated action
competes with the confirmation.

## Primary information

- Venue.
- Business Date.
- All mandatory departments remain READY.
- Signed-in Host.
- Statement that the action creates the official operational start and Opening
  Report.

## Secondary information

- Official opening time will be the confirmed outcome time, not a value chosen here.
- Guest arrivals, new Customer Groups, and Orders become allowed only after
  success.
- Opening itself creates no Customer Group or financial or ordering action.

## Available actions

- Confirm OPEN VENUE.
- Cancel and return to Ready to Open.

## Disabled actions

- Confirm if current readiness, connection, Host responsibility, or Capability
  becomes unconfirmed.
- Submit repeatedly once confirmation has been accepted.
- Edit readiness from this state.

## Empty states

None. If the confirmation context is incomplete, confirmation is unavailable and
the user returns to a safe state.

## Error states

- Eligibility changed: cancel confirmation and show the new source fact.
- Capability changed: cancel confirmation and continue to Unauthorized Host or the
  permitted before-opening view.
- Connection degraded: do not submit; continue to Connection degraded.

## Navigation options

- Cancel to Ready to Open.
- Sign out only if it does not create ambiguity about a submitted action. Before
  submission, sign-out follows ordinary session behavior.

## Primary CTA

Confirm OPEN VENUE.

## Secondary CTA

Cancel.

## Possible mistakes

- Treating entry into this state as the business action.
- Using a preselected or automatic confirmation.
- Omitting Venue or Business Date.
- Allowing a double submission.
- Claiming an Opening Report exists before confirmation succeeds.

## System feedback

- Before submission: clearly states no opening has occurred.
- After submission: immediately proceeds to Opening in progress.
- No success appears until authoritative confirmation.

## Required permissions

Host responsibility and the required Venue-opening Capability, reconfirmed at the
time the action is accepted.

# 6. Opening in Progress

## Screen title

Opening Venue

## Screen objective

Protect the operation while the final outcome of Open Venue for Business Date is
unknown.

## User Goal

Understand that the request is pending and avoid unsafe repetition.

## Visible sections

1. Status context.
2. Pending action state.
3. Connection and confirmation status.

## Primary information

- OPEN VENUE is pending.
- Venue and Business Date.
- No success statement.
- Instruction not to repeat the action.

## Secondary information

- Signed-in Host.
- Readiness snapshot used for the request.
- If outcome checking is delayed, the time the intention was submitted.

## Available actions

- None that can repeat or replace the pending opening action.
- Safe outcome check may occur through Retry only after the system explicitly
  reports that it cannot determine the result; Retry means retrieve authoritative
  state, not submit OPEN VENUE again.

## Disabled actions

- OPEN VENUE.
- Back navigation that would allow a second opening request.
- Guest Arrival, Customer Group, and Order actions until success is confirmed.

## Empty states

None. A pending action must retain its known Venue and Business Date context.

## Error states

- Clear rejection: return to the appropriate before-opening state and show why no
  opening occurred.
- Uncertain outcome: continue to Connection degraded or Unexpected error with the
  pending outcome clearly unresolved.
- Session expiration after submission: require sign-in recovery, then retrieve
  authoritative state before allowing any repeat action.

## Navigation options

- No ordinary Back action while the outcome is pending.
- Sign-out must not erase the pending action context or imply cancellation.

## Primary CTA

None.

## Secondary CTA

Check current state, only when presented as safe outcome retrieval.

## Possible mistakes

- Displaying success optimistically.
- Making retry resubmit the command.
- Allowing navigation to Ready to Open while the outcome is unknown.
- Creating a `Venue Opening Started` Domain Event. This is only an interaction
  state.

## System feedback

- Pending status remains visible.
- On confirmed success, state proceeds directly to Venue Open with a success
  acknowledgement containing official opening time and Opening Report availability.
- On confirmed rejection, Venue remains closed.
- On uncertainty, no success or failure is invented.

## Required permissions

The submitted action required Host responsibility and the required Venue-opening
Capability. Continued display of its outcome does not itself grant authority.

# 7. Venue Open

## Screen title

Host Dashboard

## Screen objective

Provide a calm, current operational view when the Venue is open and no Critical or
Action required item exists.

## User Goal

Confirm that live service is operating normally, understand current Service
Location and preparation context, and reach the correct Service Location quickly.

## Visible sections

1. Status context: Venue open, official opening time, authoritative connection.
2. Attention Queue empty state or Awareness only items.
3. Service Location Overview.
4. Live Operation Summary.
5. Department Status.
6. Recent Important Activity.

Opening Readiness becomes historical context; it does not dominate live operation.

## Primary information

- Venue open for the Business Date.
- Current counts of Available, Occupied, and Unavailable Service Locations.
- Service Location identity, type, Area, Zone, and current state.
- Active Customer Group count.
- Current Responsible Waiter context where authorized.
- Factual Bar and Kitchen Ticket counts and accepted states.

## Secondary information

- Official opening time and Opening Report route.
- Awareness-only operational facts.
- Oldest outstanding preparation time as a fact, without “late” judgment.
- Limited Host-relevant recent events.
- Filter state and last confirmed synchronization time.

## Available actions

- Locate a Service Location manually by visible name or number.
- Identify a Service Location through NFC on a supported device.
- Filter Service Locations by Area or Zone.
- Open permitted Service Location context.
- Review current authorized Customer Group and Responsible Waiter context.
- Review permitted Opening Report and recent operational detail.
- Refresh or resynchronize.

## Disabled actions

- OPEN VENUE.
- Host opening a Customer Group.
- Automatic Responsible Waiter assignment.
- Customer Group completion, cancellation, or reopening.
- Bill or Payment actions.
- Venue closing.
- Any protected action not supported by an explicit Capability and approved rule.

## Empty states

- Attention Queue: “No confirmed Host action currently requires attention.” It must
  not say the operation is perfect.
- No Active Customer Groups: valid zero when authoritatively confirmed.
- No outstanding Bar or Kitchen Tickets: valid zero when authoritatively confirmed.
- No Service Locations configured: setup error, not a normal empty Venue.
- No recent role-relevant activity: state only that none is available in this
  limited view.

## Error states

- One section unavailable: label it unavailable without replacing missing data with
  zero; keep independent confirmed sections usable.
- Invariant violation: create Critical attention and block unsafe location work.
- State becomes stale: Connection degraded.
- Complete operating state unavailable: Unexpected error.

## Navigation options

- Service Location Overview.
- Manual Service Location lookup.
- NFC identification entry on supported devices.
- Permitted location detail.
- Permitted Opening Report.
- Permitted recent activity detail.
- Dashboard home.
- Sign out.

No waiting-list, Guest Profile, VIP, reservation, financial, complaint, or Venue
administration destination is provided.

## Primary CTA

Identify Service Location.

Manual lookup is always visible as the functional fallback.

## Secondary CTA

Find by name or number.

## Possible mistakes

- Presenting an empty Attention Queue as “everything is fine.”
- Calling factual Ticket age a delay.
- Hiding active filters.
- Exposing Bill totals or Payment information.
- Letting identification perform a business action.
- Giving the Host an Open Customer Group action.

## System feedback

- Current state updates promptly from confirmed facts.
- NFC and manual lookup resolve to the same enduring Service Location.
- Identification clearly states that context was opened and no Customer Group or
  financial action occurred.
- New confirmed Action required or Critical facts move the screen to Venue Open —
  attention required.

## Required permissions

- Signed-in Host operational access.
- Detail remains filtered by Role responsibility, Venue, privacy, and explicit
  Capability.
- Identification grants no Capability.

# 8. Venue Open — Attention Required

## Screen title

Host Attention Required

## Screen objective

Place the highest-priority confirmed operational fact first while preserving enough
live context for safe Host coordination.

## User Goal

Understand what needs attention, why, who or what is affected, and the approved
next human step.

## Visible sections

1. Status context: Venue remains open.
2. Attention Queue, highest importance first.
3. Affected operational context.
4. Service Location Overview.
5. Live Operation Summary.
6. Department Status.
7. Recent Important Activity.

## Primary information

Every Attention item includes:

- Critical, Action required, or Awareness only;
- confirmed business fact;
- reason;
- affected Venue, department, Service Location, Customer Group, or preparation
  context as applicable;
- confirmation time;
- available next human step;
- whether state is current.

Only accepted MVP sources may create items:

- confirmed invariant violation;
- directly relevant rejected protected action;
- manual fallback required after NFC failure;
- Service Location became Unavailable;
- Zone reassignment affecting current Host context;
- factual preparation pressure;
- opening success acknowledgement;
- authoritative-state risk.

A post-opening department problem does not automatically close or suspend the
Venue.

## Secondary information

- Related current Service Location and Responsible Waiter context.
- Factual Bar and Kitchen Ticket state and time.
- Limited related recent activity.
- Other lower-priority Attention items.

## Available actions

- Open affected permitted context.
- Acknowledge an Action required item without declaring it resolved.
- Dismiss Awareness only information from the current view.
- Use manual Service Location lookup after NFC failure.
- Coordinate with the named responsible person through human Venue practice.
- Refresh or resynchronize.

## Disabled actions

- Dismiss unresolved Critical mandatory state.
- Mark another department, Ticket, issue, or invariant as resolved.
- Automatically assign a Responsible Waiter.
- Correct a Service Location mismatch through an invented case workflow.
- Open, complete, cancel, or reopen a Customer Group.
- Perform financial actions.

## Empty states

If no Critical or Action required item remains, transition to Venue Open. Do not
hold this screen with an artificial empty alert.

## Error states

- Attention source cannot be reconfirmed: label uncertainty and resynchronize.
- Authoritative state unavailable: Connection degraded.
- Affected context cannot safely load: preserve the Attention item and show the
  partial-section error.

## Navigation options

- Affected context.
- Service Location Overview.
- Manual lookup or NFC identification.
- Permitted recent activity.
- Dashboard home.
- Sign out.

## Primary CTA

Open highest-priority context.

## Secondary CTA

Review all Attention items.

## Possible mistakes

- Inventing complaint, issue-ticket, weather, or predictive alerts.
- Using employee names as blame indicators.
- Allowing “seen” to mean “resolved.”
- Repeating one fact as several alerts.
- Hiding the Venue-open status behind the warning.

## System feedback

- Duplicate notices for the same fact and context do not create duplicate items.
- A Critical item remains until authoritative state becomes valid.
- Action required clears only through a new confirmed source fact.
- Awareness only may leave the current view when dismissed without changing
  history.

## Required permissions

Signed-in Host operational access. Each affected detail is separately limited to
the minimum information permitted for Host responsibility and Capabilities.

# 9. Connection Degraded

## Screen title

Connection Degraded

## Screen objective

Make uncertainty explicit, prevent stale information from authorizing consequential
action, and preserve safe manual continuity.

## User Goal

Understand what was last confirmed, what is now uncertain, and which manual action
can safely continue.

## Visible sections

1. Persistent degraded status.
2. Last confirmed synchronization time.
3. Known last confirmed Venue and Business Date context.
4. Safely cached read-only information, only where later approved.
5. Manual fallback guidance.
6. Reconnection status.

The exact facts that may be cached and their allowed age remain unresolved. The
prototype must label cached regions generically and must not decide that
classification.

## Primary information

- Current state cannot be guaranteed.
- Last confirmed synchronization time.
- Whether an opening action outcome is pending or uncertain.
- Consequential actions are unavailable.

## Secondary information

- Last confirmed Venue-open state, clearly labeled as historical.
- Approved cached operational context, if any.
- Human escalation or manual continuity reminder.

## Available actions

- Retry authoritative synchronization.
- Use approved manual operational fallback.
- Sign out if no action outcome is pending.

Manual Service Location lookup may be shown only if it can retrieve authoritative
current state; cached lookup must not imply current availability.

## Disabled actions

- OPEN VENUE.
- Any protected action based on cached state.
- Claiming a Service Location is currently Available from stale information.
- Confirming Customer Group, transfer, Order, or financial outcomes.

## Empty states

- No approved safe cache: state that current operational information is unavailable;
  do not display old or inferred values.

## Error states

- Reconnection attempt fails: remain degraded and update the attempt feedback.
- No prior safe context exists: move to Unexpected error if no useful degraded
  state can be established.
- Pending action outcome remains unknown: keep it explicitly unresolved.

## Navigation options

- Retry.
- Approved manual fallback information.
- Sign out when safe.
- No navigation into stale operational actions.

## Primary CTA

Retry connection.

## Secondary CTA

Follow manual fallback.

## Possible mistakes

- Calling cached state live.
- Hiding the timestamp.
- Letting Retry resubmit a pending Command.
- Showing old availability as safe.
- Treating restored network transport as authoritative resynchronization.

## System feedback

- Every cached fact is labeled read-only and last-confirmed.
- Retry reports reconnecting without claiming restoration.
- When transport returns, proceed to Connection restored until authoritative
  reconciliation completes.

## Required permissions

Previously permitted information remains subject to the same access boundaries.
Cached information and NFC possession never grant authority.

# 10. Connection Restored

## Screen title

Connection Restored — Checking Current State

## Screen objective

Reconcile authoritative state and any uncertain action outcome before resuming live
operation.

## User Goal

Wait for confirmation that the displayed operation now matches the central system.

## Visible sections

1. Reconnection confirmation.
2. Resynchronization progress.
3. Pending outcome reconciliation, if relevant.
4. Last confirmed state clearly separated from the state being retrieved.

## Primary information

- Connection transport is available.
- Current authoritative state is not yet confirmed.
- Consequential actions remain unavailable.

## Secondary information

- Venue and Business Date being reconciled.
- Pending Open Venue outcome, if applicable.
- Last confirmed synchronization time.

## Available actions

- None while authoritative reconciliation is actively progressing.
- Retry state retrieval only after a clear retrieval failure.

## Disabled actions

- OPEN VENUE.
- Service Location or Customer Group action using unreconciled data.
- Back navigation to a cached active screen.

## Empty states

None. If there is no recoverable operational context, proceed to Unexpected error.

## Error states

- Reconciliation fails but connection remains intermittent: return to Connection
  degraded.
- Identity or session expired: proceed through sign-in recovery, then reconcile.
- State is inconsistent: do not choose a version silently; show Unexpected error or
  the approved integrity escalation state.

## Navigation options

- No operational navigation until reconciliation finishes.
- Sign out when it cannot obscure a pending action outcome.

## Primary CTA

None.

## Secondary CTA

Retry current-state retrieval after failure.

## Possible mistakes

- Returning immediately to the last cached screen.
- Claiming success because the device is online.
- Losing the identity of a pending OPEN VENUE request.
- Applying an older fact over newer authoritative state.

## System feedback

- Resynchronization state is explicit.
- Duplicate and out-of-order notices do not create duplicate business outcomes.
- After confirmation, route to the correct pending, blocked, ready, Venue Open,
  attention, Unauthorized Host, or error state.

## Required permissions

The restored session’s identity and Capabilities must be re-established. Earlier
cached authority is not sufficient.

# 11. Unauthorized Host

## Screen title

Limited Host Access

## Screen objective

Explain that the signed-in person may view only permitted context and cannot perform
the current protected action.

## User Goal

Understand the access boundary and identify the appropriate authorized person
without being misled by a Role label.

## Visible sections

1. Signed-in identity.
2. Venue and Business Date, where permitted.
3. Clear limited-access explanation.
4. Permitted read-only operational context.
5. Direction to an appropriate authorized person.

## Primary information

- The current protected action is unavailable.
- Whether the missing condition is Host responsibility or the required Capability,
  without exposing sensitive authorization details.
- Role alone does not authorize the action.

## Secondary information

- Current readiness or Venue-open facts only where permitted.
- Connection status.
- General instruction to contact an authorized Venue leader or Host.

## Available actions

- View permitted operational facts.
- Return to Dashboard home.
- Sign out and use the correct individual account.
- Refresh authority state.

## Disabled actions

- OPEN VENUE without all authority conditions.
- Any action hidden only through visual treatment while still functionally
  available.
- Capability administration.
- Acting as another person.

## Empty states

- If no Host operational context is permitted, show only the access explanation,
  safe navigation, and sign-out.

## Error states

- Capability state unavailable is not the same as confirmed denial; consequential
  action remains unavailable and state retrieval may be retried.
- Session invalid: continue to the approved sign-in recovery path.

## Navigation options

- Permitted Dashboard home.
- Sign out.
- No direct route to authorization administration.

## Primary CTA

Return to permitted Dashboard.

## Secondary CTA

Sign out.

## Possible mistakes

- Naming a Role as the missing permission.
- Revealing the user’s complete Capability record.
- Offering a “request access” workflow that has not been approved.
- Allowing a stale Capability to remain effective.

## System feedback

- The action is clearly unavailable and why.
- A confirmed Capability change causes fresh evaluation; it never silently performs
  the action.
- No protected action is queued for later execution.

## Required permissions

No additional permission is needed to see the minimal access explanation. All
operational detail remains limited to the person’s current confirmed access.

# 12. Unexpected Error

## Screen title

Current Venue State Unavailable

## Screen objective

Prevent false operational confidence when the Dashboard cannot establish a safe
known state.

## User Goal

Understand that no current conclusion can be trusted, retry safely, and continue
through approved manual operations or escalation.

## Visible sections

1. Clear non-technical error statement.
2. Last confirmed time and state, only when safe.
3. Consequential-action lockout.
4. Safe Retry.
5. Manual fallback and escalation guidance.

## Primary information

- Current operational state cannot be confirmed.
- No success, zero, or “all clear” is implied.
- Consequential actions are unavailable.

## Secondary information

- Last confirmed Venue, Business Date, and operating state where safe.
- Whether a prior action outcome remains uncertain.
- A concise distinction between a retryable retrieval problem, degraded connection,
  and session problem where known.

## Available actions

- Retry authoritative loading.
- Follow approved manual fallback.
- Sign out where safe.

## Disabled actions

- OPEN VENUE.
- Any protected operational or financial action.
- Repeating an action whose result is uncertain.
- Editing or correcting business state from the error screen.

## Empty states

None. Absence of current state is the error and must be stated directly.

## Error states

- Retry fails: remain in error with updated feedback; do not multiply error records
  in the user’s view.
- Connection state becomes specifically degraded: continue to Connection degraded.
- Session expired: continue through sign-in recovery before authoritative reload.

## Navigation options

- Retry.
- Manual fallback guidance.
- Sign out.
- No operational detail that could be mistaken for current truth.

## Primary CTA

Retry current state.

## Secondary CTA

Follow manual fallback.

## Possible mistakes

- Showing technical diagnostics as the main message.
- Clearing a pending action outcome.
- Displaying partial data as complete.
- Returning to a consequential screen before authority and state are confirmed.

## System feedback

- Retry visibly retrieves state rather than repeating a business Command.
- A recovered state routes to the correct current screen.
- Failure remains honest, bounded, and non-technical.

## Required permissions

Retry does not grant authority. Recovered content and actions require a valid
individual session and current Capabilities.

# Prototype fidelity rules

The UX Designer may determine grouping and low-fidelity arrangement but must not:

- add or remove a business action;
- convert a human follow-up into a software workflow;
- name the unresolved Venue-opening Capability;
- decide what cached data is approved;
- invent a planned opening-time source;
- invent Ticket delay thresholds or completion meaning;
- introduce Host financial visibility;
- turn Responsible Waiter assignment or Customer Group opening into a Host action;
- add unapproved lifecycle states;
- imply that an interaction creates a Domain Event when the event catalogue says it
  does not.

Any such need must be returned as a Product Owner question before the prototype is
treated as approved.
