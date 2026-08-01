# BeachOS Sprint 1 — Venue Opening UX Specification

## 1. Specification status

This is the implementation-ready interaction specification for the Sprint 1 Host
experience.

It defines behavior for:

- tablet-first use;
- desktop compatibility;
- supported mobile use;
- the journey from application entry to confirmed Venue opening;
- failure, authorization, connectivity, refresh, and recovery states.

It does not define visual styling, components, code, data structures, APIs, or
unapproved business behavior.

## 2. Sprint 1 experience boundary

Sprint 1 begins when a signed-in Host enters BeachOS and ends when the Venue is
authoritatively confirmed open for the Business Date.

The experience includes:

- current Venue and Business Date;
- mandatory Operational Departments;
- department responsible people;
- current readiness declarations;
- opening eligibility;
- authorization to open;
- intentional confirmation;
- processing;
- definitive success or safe recovery;
- the official Opening Report outcome.

The experience does not include:

- declaring readiness on behalf of a department;
- configuring departments or responsible people;
- Guest Arrival;
- Service Location lookup or NFC;
- Customer Groups;
- Responsible Waiter assignment;
- Orders;
- Kitchen or Bar operation;
- Billing or Payments;
- Venue closing;
- a full post-opening Host Dashboard.

After successful opening, Sprint 1 displays a minimal Venue-open destination. Later
operational sections are not represented as fake or inactive features.

## 3. User and device context

### Primary user

The Host coordinates readiness and intentionally opens the Venue.

The Host:

- sees the declarations made by department responsible people;
- follows up with those people through normal human communication;
- cannot submit or edit another department’s declaration;
- cannot bypass a blocker;
- can execute OPEN VENUE only with the required Capability;
- does not open a Customer Group.

### Tablet-first behavior

- The current opening state, highest-priority unresolved condition, and primary
  action are visible without leaving the main opening context.
- The Host can scan the complete mandatory department list quickly.
- Touch is the primary interaction.
- Accidental repeated interaction with OPEN VENUE is prevented.

### Desktop compatibility

- The same information and actions remain available.
- Keyboard focus order follows the content priority.
- Enter or Space may activate the focused control, but OPEN VENUE still requires the
  confirmation step.
- Escape closes the confirmation only before submission.

### Mobile support

- Critical blocker, Action required information, Venue, Business Date, connection
  state, and OPEN VENUE eligibility remain immediately available.
- Department entries follow operational priority rather than being hidden behind a
  summary.
- Details may open sequentially, but the user can always return to the complete
  readiness list.
- No critical meaning depends on hover or a wide layout.

## 4. Shared application frame

The following information persists across Sprint 1 screens whenever confirmed:

- application name: BeachOS;
- signed-in Staff Member name;
- current Role context: Host;
- Venue name;
- Business Date;
- current Venue state: Closed, Opening in progress, or Open;
- connection state when not fully current;
- sign-out action.

### Shared behavior

- The frame never shows the Venue as Open until success is authoritative.
- Business Date is always displayed with the Venue.
- A changed or unknown Venue or Business Date stops any opening action.
- The Host Role label never implies authorization.
- The connection state becomes prominent whenever information may be stale.
- Sign out is unavailable only while it could obscure an unresolved submitted
  opening outcome; in that case, the interface explains why.

## 5. Information priority

The screen reading order is:

1. Venue, Business Date, and Venue state.
2. Connection and freshness.
3. Highest-priority opening condition.
4. Opening eligibility and Host authorization.
5. Mandatory Operational Departments.
6. Reasons, comments, responsible people, and confirmation times.
7. Recent readiness changes relevant to this opening.

Within the department list:

1. BLOCKED.
2. NOT READY.
3. Missing declaration.
4. READY.

This ordering helps coordination. It does not rank employees.

## 6. Readiness vocabulary

Only these labels are used:

- **READY** — the responsible person confirms the department can perform its opening
  responsibilities.
- **NOT READY** — preparation is incomplete; a reason is mandatory.
- **BLOCKED** — the department cannot become ready until a blocker is resolved; a
  reason is mandatory.
- **NO DECLARATION** — the responsible person has not yet made a current declaration.

The interface does not use Pending as a department declaration. “Declarations
pending” describes the screen state, not a fourth declaration value.

# 7. Screens

## Screen 1 — Application Entry and Loading

### Purpose

Establish the signed-in person, Host context, Venue, Business Date, Capabilities,
Venue state, mandatory departments, readiness declarations, and authoritative
connection before showing an operational conclusion.

### Visible information

- Screen title: “Opening”.
- “Loading current Venue opening status.”
- Signed-in Staff Member, only if already confirmed.
- Venue, only if already confirmed.
- Connection check in progress.

No readiness count, department status, eligibility, or empty state appears before it
is known.

### Primary Action

None.

### Secondary Actions

- Sign out, if the session is known and no submitted opening outcome is pending.

### Validation

Before leaving Loading, the experience validates that:

- the session belongs to one current Staff Member;
- the Staff Member can access the Venue context;
- Venue and Business Date are known;
- current Venue state is known;
- Capability state is known;
- mandatory department context can be retrieved;
- the displayed data is authoritative or explicitly degraded.

### Success

Route without intermediate choice:

- Venue closed with missing or NOT READY declarations → Declarations Pending.
- Venue closed with any BLOCKED department → Opening Blocked.
- Venue closed and all mandatory departments READY → Ready to Open.
- Venue already open → Venue Open.
- signed-in person lacks permitted Host context → Limited Access.

### Failure

- No current state and no safe previous context → Current State Unavailable.
- Connection unavailable with safe last-confirmed context → Connection Degraded.
- Session expired → Session Expired blocking message.

### Empty state

None. Missing data is Loading, unavailable, or an error, never a valid zero.

### Loading

- One persistent page-level progress indicator.
- Loading text names the task: “Loading current Venue opening status.”
- The indicator does not reset or flash as individual requests complete.
- If loading exceeds the normal response period, the message changes to:
  “Still checking the current Venue status.”
- No manual Retry appears until the retrieval is known to have failed.

### Permissions

No action is authorized during Loading. Permission controls are not briefly exposed
before Capability state is known.

### Navigation

- Automatic transition to the correct current screen.
- No Back route into unconfirmed operational state.

## Screen 2 — Opening Readiness: Declarations Pending

### Purpose

Show every missing or NOT READY declaration and help the Host identify the correct
person for human follow-up.

### Visible information

- Screen title: “Opening Readiness”.
- Venue and Business Date.
- Venue state: “Closed”.
- Opening state: “Waiting for department readiness”.
- Summary:
  - number READY;
  - number NOT READY;
  - number with NO DECLARATION;
  - number BLOCKED, which is zero in this screen.
- Every mandatory Operational Department.
- For each department:
  - official department name;
  - current readiness label;
  - responsible person;
  - reason for NOT READY;
  - approved comment, if present;
  - confirmation time for the current declaration;
  - “No declaration received” when missing.
- Instruction:
  “Department responsible people update their own readiness. Follow up directly
  with the person shown.”
- Last confirmed update time when useful.

### Primary Action

“Review unresolved departments.”

This moves focus to the first unresolved department and then through the unresolved
set. It does not create a task, message, or escalation record.

### Secondary Actions

- Open one department’s detail.
- “Show all departments.”
- “Refresh current status.”
- Sign out.

### Validation

- A NOT READY declaration must have a reason.
- A responsible person must be known for every mandatory department.
- A current declaration belongs to this Venue and Business Date.
- OPEN VENUE eligibility is recalculated from the entire current mandatory set.

### Success

This screen itself does not complete Venue opening.

Incoming confirmed declarations cause:

- any BLOCKED → Opening Blocked;
- all mandatory departments READY → Ready to Open;
- otherwise remain on this screen with the changed department announced.

### Failure

- Invalid NOT READY declaration: show that the declaration cannot be confirmed and
  keep the department unresolved.
- Missing responsible person: show a blocking setup message for that department.
- Refresh failure: preserve confirmed information only if it remains labeled with
  its confirmation time; disable OPEN VENUE.
- Authoritative state unavailable: Connection Degraded or Current State Unavailable.

### Empty state

- No mandatory departments: “Opening cannot continue because no mandatory
  departments are configured.” This is a blocking setup error.
- No unresolved departments: automatically transition to Ready to Open.

### Loading

- Initial screen load uses the page-level Loading screen.
- Refresh keeps existing confirmed content visible, marks refresh in progress, and
  does not replace it with zero.
- A single department update shows a local “Updating current status” indicator only
  while authoritative state is being retrieved.

### Permissions

- Host may view permitted readiness information.
- Host cannot edit, create, or submit a declaration for a department.
- Host cannot mark follow-up complete in BeachOS.
- OPEN VENUE is disabled because the readiness rule is not satisfied, regardless of
  Capability.

### Navigation

- Dashboard home is this screen for the current closed Venue.
- Department detail returns to the same list and review position.
- Back must not leave the Venue and Business Date context silently.

## Screen 3 — Opening Blocked

### Purpose

Make every mandatory BLOCKED declaration impossible to overlook and give the Host
the facts needed for human coordination.

### Visible information

- Screen title: “Opening Blocked”.
- Venue and Business Date.
- Venue state: “Closed”.
- Blocking summary:
  “The Venue cannot open while a mandatory department is BLOCKED.”
- Each BLOCKED department before all other departments.
- For each blocker:
  - department;
  - responsible person;
  - mandatory reason;
  - approved comment;
  - confirmation time.
- Other NOT READY or missing declarations after blockers.
- READY departments in the complete readiness list.
- OPEN VENUE disabled with an explicit reason.

### Primary Action

“Review blocking issue.”

This opens the first blocker’s complete permitted detail.

### Secondary Actions

- Review the next blocker.
- Show all departments.
- Refresh current status.
- Sign out.

### Validation

- BLOCKED must include a reason.
- The blocker remains current only while the authoritative declaration remains
  BLOCKED.
- A Host acknowledgment never validates resolution.

### Success

A later valid declaration from the department responsible person is received:

- other blockers remain → stay on Opening Blocked;
- no blockers but missing or NOT READY remain → Declarations Pending;
- every mandatory department READY → Ready to Open.

### Failure

- BLOCKED without a reason: “This blocked declaration is incomplete. A reason is
  required before it can be confirmed.”
- Unknown responsible person: blocking setup message.
- Conflicting declaration versions: current status becomes unavailable until
  resynchronized.

### Empty state

There is no valid empty blocker state. If no current blocker exists, transition to
the correct current screen.

### Loading

- Refresh and local update behavior match Declarations Pending.
- Old blocker detail remains visibly last-confirmed during refresh; it is not
  silently removed.

### Permissions

- Host may review and coordinate.
- Host cannot dismiss the blocker as resolved.
- Host cannot change BLOCKED to READY.
- No Role or Capability provides an override under the approved Sprint 1 rules.

### Navigation

- Blocker detail → Back to Opening Blocked.
- Complete department list → same screen context.
- No route to OPEN VENUE confirmation.

## Screen 4 — Ready to Open

### Purpose

Confirm that every mandatory department is READY and let an authorized Host begin
the intentional Venue-opening action.

### Visible information

- Screen title: “Ready to Open”.
- Venue and Business Date.
- Venue state: “Closed”.
- Readiness statement: “All mandatory departments are READY.”
- Complete mandatory department list.
- For each department:
  - READY;
  - responsible person;
  - confirmation time;
  - approved comment, if present.
- Host authorization state.
- Consequence summary:
  - opens the Venue for this Business Date;
  - records official opening time and Host;
  - makes the Opening Report official;
  - allows Guest Arrival, Customer Groups, and Orders only under their own later
    rules;
  - creates no Customer Group, Bill, charge, Order, transfer, or Payment.

The Capability’s internal or official catalogue name is not shown. The interaction
uses user-facing language: “You are authorized to open this Venue” or “You are not
authorized to open this Venue.”

### Primary Action

“Open Venue”.

Available only when:

- every mandatory department is currently READY;
- Venue remains closed;
- signed-in person satisfies Host responsibility;
- signed-in person holds the required Capability;
- information is authoritative and current.

### Secondary Actions

- Review readiness.
- Refresh current status.
- Sign out.

### Validation

At display and again before opening confirmation:

- all mandatory departments are READY;
- no declaration is missing;
- Venue is still closed;
- Venue and Business Date are unchanged;
- Host responsibility and Capability remain valid;
- connection is authoritative.

### Success

Selecting “Open Venue” opens the Open Venue Confirmation dialog. It does not submit
the opening Command.

### Failure

- Readiness changes: close or prevent the confirmation, announce the changed
  department, and route to Opening Blocked or Declarations Pending.
- Capability changes: route to Limited Access.
- Connection degrades: route to Connection Degraded.
- Venue was opened elsewhere: retrieve current state and route to Venue Open.

### Empty state

None. All mandatory departments must be present and READY.

### Loading

- A current-state refresh may keep the list visible while “Checking current
  readiness” is announced.
- During refresh, Open Venue is disabled with “Checking current readiness.”

### Permissions

- Authorized Host: Open Venue enabled.
- Host without the required Capability: action disabled and Limited Access guidance
  shown.
- Capability never bypasses readiness.

### Navigation

- Open Venue → Open Venue Confirmation dialog.
- Review readiness → complete list on this screen.
- Back does not return to a stale previous readiness screen.

## Screen 5 — Limited Access

### Purpose

Explain that the Host may review permitted readiness but cannot execute OPEN VENUE.

### Visible information

- Screen title: “Opening Readiness”.
- Venue and Business Date.
- current readiness facts allowed to the signed-in person;
- statement:
  “You can review opening readiness, but you are not authorized to open this
  Venue.”
- guidance:
  “Ask an authorized Host or Venue leader to complete opening.”

The screen does not expose the person’s full Capability record or another person’s
security information.

### Primary Action

“Return to Opening Readiness.”

### Secondary Actions

- Refresh access.
- Sign out.

### Validation

- Confirm that denial is authoritative, not merely failure to load Capability
  state.
- Re-evaluate access after refresh.

### Success

- Confirmed Capability or responsibility change: route to the current appropriate
  readiness screen.
- Another Host opens the Venue: route to Venue Open after authoritative retrieval.

### Failure

- Capability state cannot be retrieved: “Authorization could not be confirmed.”
  Open Venue remains unavailable.
- Session expired: Session Expired blocking message.

### Empty state

If no operational information is permitted, show only identity, Venue context if
permitted, the access explanation, and sign-out.

### Loading

“Checking access” appears during an intentional access refresh. Open Venue is never
shown as temporarily available.

### Permissions

No protected opening action is available. The screen has no access-request,
Capability administration, or impersonation action.

### Navigation

- Return to permitted readiness.
- Sign out.
- No route to Open Venue Confirmation.

## Screen 6 — Opening in Progress

### Purpose

Protect the operation while the final result of OPEN VENUE is unknown.

### Visible information

- Screen title: “Opening Venue”.
- Venue and Business Date.
- signed-in Host.
- message: “Opening is being confirmed.”
- instruction: “Do not repeat the action.”
- connection state.
- submitted time, if useful for support and clearly distinguished from official
  opening time.

### Primary Action

None while the result is being determined.

### Secondary Actions

None initially.

If the result check explicitly fails, a “Check current status” action may appear.
It retrieves authoritative state and never resubmits OPEN VENUE.

### Validation

- Preserve one submitted opening intention.
- Prevent a second interaction.
- Do not infer result from elapsed time.
- Do not use device state alone as success.

### Success

Authoritative `Venue Opened for Business Date` confirmation routes to Opening
Successful.

### Failure

- Definitive rejection: show the Opening Not Completed blocking message, then return
  to the current closed readiness screen.
- Connection loss or unknown result: route to Connection Degraded with the pending
  outcome preserved.
- Session expires after submission: Session Expired message explains that the
  outcome must be checked after sign-in.
- Unexpected retrieval failure: Current State Unavailable, with the submitted
  outcome identified as unknown.

### Empty state

None. Venue, Business Date, Host, and pending intention must remain known.

### Loading

- One persistent processing indicator.
- No estimated completion time.
- No progress percentage.
- No cancellation action after submission.
- If processing continues, copy changes to:
  “Still confirming the Venue opening. Do not repeat the action.”

### Permissions

The original action was accepted only after permission validation. Remaining on
this screen does not preserve authorization for future actions.

### Navigation

- Back is disabled.
- Browser or device Back must not return to an enabled Open Venue action.
- Sign out is disabled while the outcome is unresolved, with the explanation:
  “Wait until the opening result is confirmed.”

## Screen 7 — Opening Successful

### Purpose

Give an unmistakable, authoritative acknowledgement that the Venue is open and the
official Opening Report exists.

### Visible information

- Screen title: “Venue Open”.
- statement: “The Venue is open for this Business Date.”
- Venue.
- Business Date.
- official opening time.
- Host who opened the Venue.
- summary: “All mandatory departments were READY at opening.”
- Opening Report availability.

### Primary Action

“Continue to Venue.”

### Secondary Actions

- “View Opening Report.”

### Validation

This screen appears only after authoritative confirmation of:

- `Venue Opened for Business Date`;
- official opening time;
- Host;
- Opening Report availability;
- required Activity Log outcome.

### Success

Continue to the minimal Venue Open screen.

### Failure

- If the Opening Report cannot be confirmed, do not present an unqualified success.
  Show:
  “The opening result needs to be checked before service continues.”
  Then retrieve authoritative state.
- If a duplicated live notice arrives, do not repeat this acknowledgement as a new
  opening.

### Empty state

None. Official opening facts are required.

### Loading

No loading state after success is shown. If confirmation is still incomplete,
remain on Opening in Progress.

### Permissions

The Host may view permitted opening outcome information. Opening success grants no
new Capability.

### Navigation

- Continue to Venue Open.
- View Opening Report.
- Back cannot return to Ready to Open or resubmit opening.

## Screen 8 — Opening Report

### Purpose

Let the Host review the permanent operational record produced by successful opening.

### Visible information

- Screen title: “Opening Report”.
- Venue.
- Business Date.
- official opening time.
- Host.
- every mandatory Operational Department.
- readiness at opening: READY.
- responsible person for each declaration.
- relevant delays.
- earlier blocking issues relevant to the completed opening.
- reasons and approved comments.
- report status: “Official opening record.”

The report does not state that the Host personally verified departments.

### Primary Action

“Return to Venue.”

### Secondary Actions

- None in Sprint 1.

There is no edit, correct, delete, export, or print action.

### Validation

- The report belongs to the current Venue and Business Date.
- Every mandatory department was READY at opening.
- Original opening facts are not silently changed.

### Success

Report loads and can be read.

### Failure

“The Opening Report is temporarily unavailable. The current Venue state must be
confirmed before relying on this record.”

Retry retrieves the report; it does not recreate it.

### Empty state

There is no valid empty Opening Report after confirmed opening. Missing report is an
integrity error.

### Loading

“Loading official Opening Report.”

Existing Venue Open state remains visible as context only if authoritatively
confirmed.

### Permissions

Only permitted operational report information is shown. Sprint 1 does not provide
report administration.

### Navigation

- Return to Venue Open.
- Back returns to the confirmed Venue Open state, never to pre-opening.

## Screen 9 — Venue Open

### Purpose

Provide the Sprint 1 destination after opening without pretending later Host
Dashboard features exist.

### Visible information

- Screen title: “Venue Open”.
- Venue.
- Business Date.
- official opening time.
- opening Host.
- statement: “Venue opening is complete.”
- link to the Opening Report.

### Primary Action

“View Opening Report.”

### Secondary Actions

- Refresh current status.
- Sign out.

### Validation

- Venue-open state comes from the central authoritative source.
- Refresh cannot return to a closed state without a separately approved business
  outcome; no Venue closing exists in Sprint 1.

### Success

The Host can confirm that the Venue is open and review the report.

### Failure

- Current state cannot be retrieved: Connection Degraded or Current State
  Unavailable.
- Opening Report unavailable: show report-specific failure without changing the
  confirmed Venue state unless the opening itself becomes uncertain.

### Empty state

No later operational Dashboard sections are shown. Their absence is not described
as empty data.

### Loading

Refresh states “Checking current Venue status” and retains last-confirmed facts with
their time until current state is retrieved.

### Permissions

Viewing the opening outcome follows permitted Host access. No new protected action
is available.

### Navigation

- Opening Report.
- Sign out.
- No route to Guest Arrival, Customer Groups, Orders, preparation, Bills, Payments,
  Manager Dashboard, or Venue closing in Sprint 1.

## Screen 10 — Connection Degraded

### Purpose

Make uncertainty explicit and prevent stale readiness or an unknown opening outcome
from being used as authority.

### Visible information

- Screen title: “Connection Degraded”.
- Venue and Business Date when last confirmed.
- persistent message: “Current Venue status cannot be confirmed.”
- last confirmed synchronization time.
- last-confirmed Venue state, labeled “Last confirmed”.
- pending opening outcome, if one exists.
- message: “Opening actions are unavailable until current status is restored.”
- approved manual operational guidance, if supplied outside this specification.

### Primary Action

“Retry connection.”

### Secondary Actions

- Sign out only when no submitted opening outcome is unresolved.

### Validation

- Cached facts are not current authority.
- OPEN VENUE is unavailable.
- Retry retrieves current state.
- Pending action identity is preserved.

### Success

Connection transport returns → Connection Restored.

### Failure

- Retry fails: remain on this screen and show “Connection is still unavailable.”
- No safe last-confirmed context: Current State Unavailable.
- Session expired: Session Expired blocking message.

### Empty state

If no safe prior context exists:
“No confirmed Venue information is available on this device.”

Do not display zero departments or Closed/Open by assumption.

### Loading

Retry shows “Reconnecting” without removing the last-confirmed timestamp.

### Permissions

Cached identity or Capability grants no action. All protected actions are disabled.

### Navigation

- Retry.
- Safe sign-out where permitted.
- No Back route into stale readiness.

## Screen 11 — Connection Restored

### Purpose

Reconcile identity, authorization, readiness, Venue state, and any submitted opening
outcome before returning to operation.

### Visible information

- Screen title: “Connection Restored”.
- message: “Checking current Venue status.”
- Venue and Business Date being checked.
- pending opening outcome, if relevant.
- last confirmed time.

### Primary Action

None during reconciliation.

### Secondary Actions

“Retry status check” appears only after a retrieval failure.

### Validation

- Restored network access is not treated as restored operational truth.
- Current identity and Capability are rechecked.
- Missed, duplicated, or out-of-order notices do not create a second opening.

### Success

Route to the actual current state:

- Declarations Pending;
- Opening Blocked;
- Ready to Open;
- Limited Access;
- Opening Successful;
- Venue Open.

### Failure

- Reconciliation fails: return to Connection Degraded.
- State conflicts: Current State Unavailable.
- Session expired: Session Expired blocking message.

### Empty state

None.

### Loading

One page-level synchronization indicator with:
“Checking current Venue status.”

### Permissions

Earlier cached permission is ignored. Current authorization must be confirmed.

### Navigation

No operational navigation until reconciliation completes.

## Screen 12 — Current State Unavailable

### Purpose

Prevent false confidence when BeachOS cannot establish a safe current state.

### Visible information

- Screen title: “Current Venue State Unavailable”.
- message: “BeachOS cannot confirm the current opening status.”
- Venue and Business Date when safely known.
- last confirmed time and state when safely known.
- pending opening outcome, if one exists.
- statement: “Do not repeat OPEN VENUE while the result is unknown.”

Technical diagnostics are not the main user message.

### Primary Action

“Retry current status.”

### Secondary Actions

- Sign out only when no submitted outcome is unresolved.
- Follow the Venue’s approved manual escalation procedure.

### Validation

- Retry retrieves state and never repeats a Business Command.
- Missing data is not converted to zero.
- A partial response is not called complete.

### Success

Route through Loading or Connection Restored to the actual current state.

### Failure

Remain on this screen with:
“Current status is still unavailable. Follow the approved manual procedure and try
again.”

### Empty state

None. Absence of current state is the error.

### Loading

Retry uses “Checking current Venue status.”

### Permissions

No consequential action is available.

### Navigation

- Retry.
- Safe sign-out where permitted.
- No route to Ready to Open, confirmation, or processing from unconfirmed state.

# 8. Dialogs

## Dialog D1 — Open Venue Confirmation

### Trigger

The authorized Host selects “Open Venue” from Ready to Open.

### Purpose

Require deliberate confirmation of the consequential action.

### Title

“Open this Venue?”

### Information

- Venue.
- Business Date.
- “All mandatory departments are READY.”
- “Opening records the official start of this Business Date and creates the Opening
  Report.”
- “This action does not create a Customer Group, Bill, charge, Order, transfer, or
  Payment.”

### Primary Action

“Confirm Open Venue.”

### Secondary Action

“Cancel.”

### Behavior

- Primary action is not preselected.
- Confirmation is available only while current state and authorization remain
  valid.
- Confirm submits once and immediately moves to Opening in Progress.
- Cancel closes the dialog and returns to Ready to Open without a business change.
- Outside interaction and Escape may equal Cancel only before submission.
- Once submitted, the dialog closes and cannot be reopened while outcome is pending.

### Validation

Immediately before submission:

- Venue and Business Date unchanged;
- Venue still closed;
- all mandatory departments still READY;
- Host responsibility current;
- required Capability current;
- central state current.

### Validation failure

The dialog closes. The system announces the reason and routes to the correct current
screen. It never leaves the user looking at a valid-looking stale confirmation.

## No other Sprint 1 dialogs

Sprint 1 has no:

- blocker dismissal dialog;
- declaration editing dialog;
- override dialog;
- force-open dialog;
- report correction dialog;
- Venue-close dialog.

# 9. Toasts

Toasts communicate completed, low-interruption feedback. They never carry the only
copy of a critical blocker, authorization failure, uncertain outcome, or required
next action.

## Toast T1 — Readiness updated

**Message:** “[Department] readiness updated to [READY / NOT READY / BLOCKED].”

**When used:** A confirmed current declaration changes while the Host remains on
the readiness screen.

**Behavior:** The relevant department and screen state update at the same time.
Duplicate notices do not create duplicate toasts.

## Toast T2 — Current status refreshed

**Message:** “Current opening status refreshed.”

**When used:** An explicit refresh completes and the screen state does not otherwise
change.

**Do not use:** When refresh reveals a blocker, authorization loss, or Venue opening;
those changes require persistent screen feedback.

## Toast T3 — Connection restored

**Message:** “Connection restored. Current status confirmed.”

**When used:** Only after authoritative reconciliation completes.

**Do not use:** Merely because network transport returned.

## Toast T4 — Opening Report available

**Message:** “Official Opening Report is available.”

**When used:** Optional after the Opening Successful screen transitions to Venue
Open.

The report link remains persistently available; the toast is not the only route.

## Toast behavior rules

- A toast may be dismissed.
- Dismissal has no business effect.
- A toast does not clear Attention or a readiness condition.
- A toast is announced accessibly.
- A toast does not include sensitive authorization detail.
- Success toasts appear only after authoritative confirmation.

# 10. Confirmations

Sprint 1 has one business confirmation:

1. Open Venue Confirmation.

The following do not require confirmation:

- viewing department detail;
- refreshing status;
- viewing the Opening Report;
- returning to Venue Open;
- signing out when no action outcome is pending.

No second confirmation appears after “Confirm Open Venue.” Processing begins
immediately.

# 11. Blocking messages

Blocking messages remain visible until their source state changes or the user moves
to a safe recovery path.

## B1 — Mandatory department BLOCKED

**Title:** “Opening blocked”

**Message:** “[Department] is BLOCKED: [reason]. The responsible person must update
the declaration before the Venue can open.”

**Action:** “Review blocking issue.”

## B2 — Missing declaration

**Title:** “Readiness declaration required”

**Message:** “[Department] has not declared readiness. Contact [responsible person].”

## B3 — Department NOT READY

**Title:** “Department not ready”

**Message:** “[Department] is NOT READY: [reason].”

## B4 — Missing responsible person

**Title:** “Responsible person required”

**Message:** “[Department] has no confirmed responsible person for this opening.
Venue opening cannot continue.”

No configuration action is offered in Sprint 1.

## B5 — Not authorized to open

**Title:** “Opening action unavailable”

**Message:** “You can review readiness, but you are not authorized to open this
Venue. Ask an authorized Host or Venue leader.”

## B6 — Current status unavailable

**Title:** “Current status cannot be confirmed”

**Message:** “Opening actions are unavailable until BeachOS confirms the current
Venue status.”

## B7 — Opening outcome unknown

**Title:** “Opening result not confirmed”

**Message:** “Do not repeat OPEN VENUE. BeachOS must check the current Venue status
first.”

## B8 — Opening not completed

**Title:** “Venue was not opened”

**Message:** Use the approved plain-language rejection reason when available,
followed by: “The Venue remains closed.”

This message does not invent a `Venue Opening Rejected` Domain Event.

## B9 — Session expired

**Title:** “Session expired”

**Before submission:** “Sign in again to continue.”

**After submission:** “Sign in again so BeachOS can check whether the Venue opened.
Do not repeat the action.”

## B10 — Opening Report integrity failure

**Title:** “Opening record unavailable”

**Message:** “BeachOS cannot confirm the official Opening Report. Check the current
Venue status before service continues.”

# 12. Validation messages

Validation messages explain the exact condition and next safe step.

## Readiness validation

- “A reason is required when a department is NOT READY.”
- “A reason is required when a department is BLOCKED.”
- “This readiness declaration could not be confirmed.”
- “This declaration belongs to a different Venue or Business Date.”
- “A responsible person is required for every mandatory department.”

The Host sees these messages as status integrity feedback. The Host receives no
editing field for another department.

## Opening validation

- “The Venue cannot open until every mandatory department is READY.”
- “[Department] is now NOT READY. Review the updated declaration.”
- “[Department] is now BLOCKED: [reason].”
- “[Department] no longer has a current declaration.”
- “The Venue is already open for this Business Date.”
- “You are not authorized to open this Venue.”
- “Authorization could not be confirmed. Try again when current access is
  available.”
- “Current readiness could not be confirmed. OPEN VENUE is unavailable.”
- “The Venue or Business Date changed. Review the current opening context.”

## Retry validation

- “Current status is still unavailable.”
- “The opening result is still being confirmed. Do not repeat the action.”
- “Connection is still unavailable.”

## Message rules

- Never use “Something went wrong” alone.
- Never expose internal identifiers, stack traces, database errors, or Capability
  records.
- Never use success language in a validation failure.
- Never blame a Staff Member.
- Never imply that the Host can override the condition.

# 13. Loading indicators

## L1 — Page loading

Used for initial identity and current-state retrieval.

Text:

- “Loading current Venue opening status.”
- Long-running: “Still checking the current Venue status.”

## L2 — Readiness refresh

Used while preserving current confirmed readiness.

Text:

- “Checking current readiness.”

Open Venue is disabled during this state.

## L3 — Opening processing

Used only after confirmation submission.

Text:

- “Opening is being confirmed.”
- Long-running: “Still confirming the Venue opening. Do not repeat the action.”

No percentage, cancel action, or duplicate action is shown.

## L4 — Reconnecting

Used after Retry from Connection Degraded.

Text:

- “Reconnecting.”

Last-confirmed time remains visible.

## L5 — Reconciliation

Used after transport returns.

Text:

- “Connection restored. Checking current Venue status.”

## L6 — Opening Report loading

Text:

- “Loading official Opening Report.”

## Loading rules

- Loading never replaces unknown information with zero.
- An existing confirmed value may remain visible only with its confirmation or stale
  state clear.
- One operation has one indicator.
- A loader never implies progress toward success.
- Loading cannot make a disabled consequential action available.

# 14. Disabled states

Every disabled action has a nearby reason. Disabled state is not the only
authorization control.

## Open Venue disabled reasons

Use one highest-priority reason:

1. “Opening blocked by [number] mandatory department(s).”
2. “[number] department(s) are not ready.”
3. “[number] readiness declaration(s) are missing.”
4. “You are not authorized to open this Venue.”
5. “Checking current readiness.”
6. “Current Venue status is unavailable.”
7. “Venue opening is already being confirmed.”
8. “The Venue is already open.”

If several readiness conditions exist, the screen lists all of them even though the
disabled action uses one concise reason.

## Confirm Open Venue disabled reasons

- readiness changed;
- authorization changed;
- connection no longer current;
- Venue or Business Date changed;
- submission already accepted.

The confirmation dialog closes when the condition requires a different screen.

## Back disabled

During Opening in Progress:

“Wait until the opening result is confirmed.”

## Sign out disabled

Only while an opening outcome is unresolved:

“Wait until the opening result is confirmed.”

## Department declaration controls

No disabled editing control is shown to the Host. The action does not belong to the
Host, so it is absent rather than displayed as a tempting disabled control.

# 15. Transition specification

## Transition A — Enter application

- **From:** application entry
- **To:** Loading
- **Trigger:** Host enters BeachOS
- **Feedback:** page-level Loading
**Back behavior:** no operational Back state

## Transition B — Loading to current opening state

**Trigger:** identity, authorization, Venue, Business Date, and current state are
confirmed.

**Destinations:**

- Declarations Pending;
- Opening Blocked;
- Ready to Open;
- Limited Access;
- Venue Open;
- Connection Degraded;
- Current State Unavailable.

No user choice is required.

## Transition C — Readiness changes

**Trigger:** confirmed `Department Readiness Declared`.

**Behavior:**

- update the department;
- announce the change;
- reorder the list by operational priority;
- recalculate eligibility;
- transition screens if the overall state changed;
- preserve the Host’s context where safe.

Viewing or acknowledging creates no transition.

## Transition D — User presses Open Venue

- **From:** Ready to Open
- **To:** Open Venue Confirmation dialog
- **Guard:** all-ready, authorized, current, Venue closed
- **Feedback:** dialog opens with Venue, Business Date, and consequences
**Business change:** none

## Transition E — User cancels confirmation

- **From:** confirmation dialog
- **To:** Ready to Open or newly current readiness screen
- **Feedback:** dialog closes
**Business change:** none

## Transition F — User confirms Open Venue

- **From:** confirmation dialog
- **To:** Opening in Progress
- **Guard:** all conditions revalidated
- **Feedback:** processing begins; duplicate action unavailable
**Business intention:** `Open Venue for Business Date`

## Transition G — Processing to success

- **From:** Opening in Progress
- **To:** Opening Successful
- **Trigger:** authoritative `Venue Opened for Business Date`
- **Feedback:** official opening time, Host, Business Date, Opening Report
**Business outcome:** Venue open; Opening Report official; required Activity Log

## Transition H — Success to Dashboard change

- **From:** Opening Successful
- **To:** Venue Open
- **Trigger:** Host selects Continue to Venue
- **Feedback:** persistent Venue-open state and Opening Report route
**Business change:** none; this is navigation

## Transition I — Processing to definitive non-success

- **From:** Opening in Progress
- **To:** blocking message, then current closed readiness screen
- **Trigger:** definitive rejection or failure before opening
- **Feedback:** “Venue was not opened. The Venue remains closed.” plus approved reason
**Business outcome:** no opening fact

## Transition J — Processing to unknown outcome

- **From:** Opening in Progress
- **To:** Connection Degraded or Current State Unavailable
- **Trigger:** result cannot be determined
- **Feedback:** do not repeat; Retry checks current status
**Business outcome:** not asserted

## Transition K — Connection restored

- **From:** Connection Degraded
- **To:** Connection Restored
- **Trigger:** transport returns
- **Feedback:** current-state reconciliation
**Business change:** none

## Transition L — Reconciliation completes

- **From:** Connection Restored
- **To:** actual current opening state
- **Trigger:** authoritative state confirmed
- **Feedback:** Connection restored toast only after confirmation
**Business change:** none; existing events are reflected

## Transition M — Session expires before submission

- **From:** any pre-submission screen
- **To:** Session Expired blocking state and sign-in recovery
- **Behavior:** unsubmitted confirmation is discarded
**Business change:** none

## Transition N — Session expires after submission

- **From:** Opening in Progress
- **To:** Session Expired blocking state and sign-in recovery
- **Behavior:** preserve pending action identity; after sign-in, retrieve outcome
**Business change:** not asserted until confirmed

# 16. Refresh, Back, and interruption behavior

## Refresh

- Retrieves authoritative current state.
- Does not resubmit a Command.
- Does not resolve a blocker.
- Does not clear the Opening Report.
- Does not convert missing data to zero.
- Preserves a pending opening identity.
- Routes to a new screen when the confirmed overall state changed.

## Back

- Department detail → current readiness list.
- Confirmation before submission → Cancel.
- Opening in Progress → disabled.
- Opening Successful or Venue Open → never returns to Ready to Open.
- Connection Restored → cannot return to stale operational state.

## App backgrounding or interruption

On return:

- recheck current state when freshness cannot be guaranteed;
- preserve the pending action identity;
- never reopen the confirmation automatically;
- never automatically submit or repeat OPEN VENUE;
- show the actual current state, including Venue Open if another authorized Host
  completed opening.

# 17. Accessibility and operational clarity requirements

- Every status is expressed in text.
- Critical information is not conveyed by color alone.
- Focus moves to a newly opened dialog and returns safely on cancellation.
- Processing and live changes are announced without repeatedly interrupting the
  Host.
- Disabled controls expose their reason.
- Touch targets support tablet and mobile operation.
- Keyboard users can complete every Host action.
- Confirmation cannot be triggered accidentally by the same interaction that opens
  the dialog.
- Error messages identify the next safe step.
- Long department names, reasons, comments, and Staff Member names remain readable.
- The screen remains understandable in bright, distracting, high-pressure
  conditions.

# 18. Lovable handoff rules

The Lovable prototype must implement the functional states and transitions in this
document without adding:

- visual design decisions to the product rules;
- department declaration editing for the Host;
- force-open or override;
- an access-request workflow;
- automatic opening;
- fake post-opening features;
- Guest Arrival or Customer Group actions;
- speculative alerts, reports, settings, or administration;
- a new Domain Event;
- a hidden success before authoritative confirmation.

Prototype data should demonstrate at minimum:

1. declarations pending;
2. one NOT READY department with reason;
3. one BLOCKED department with reason;
4. every department READY;
5. Host not authorized;
6. confirmation cancelled;
7. processing;
8. successful opening;
9. definitive non-success;
10. unknown result after connection loss;
11. restored connection and successful reconciliation;
12. Opening Report.

The final prototype must allow the complete successful journey described in
`ux/USER_JOURNEY.md`.
