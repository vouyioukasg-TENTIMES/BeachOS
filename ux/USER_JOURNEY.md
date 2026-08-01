# BeachOS Sprint 1 — Host Opens a Venue

## Journey scope

This is one complete successful Host journey from entering BeachOS until the Venue
is authoritatively confirmed open.

The journey uses:

- one signed-in Host;
- one Venue;
- one Business Date;
- six mandatory Operational Departments:
  - Kitchen;
  - Bar;
  - Beach Operations;
  - Cleaning;
  - Maintenance;
  - Cashier;
- one responsible person per department;
- current authoritative connectivity;
- the Host’s required Venue-opening Capability.

The Host never declares readiness for a department. Department responsible people
update their own statuses.

# Journey

## Step 1 — The Host enters BeachOS

The Host opens BeachOS on a tablet.

BeachOS displays:

- “Opening”;
- “Loading current Venue opening status”;
- the Host’s name when confirmed;
- the Venue when confirmed.

No readiness totals or opening action appear yet.

### Host understanding

BeachOS is checking the correct person, Venue, Business Date, authorization, and
current opening state.

### System requirement

No missing information is shown as zero, READY, or Closed by assumption.

## Step 2 — BeachOS establishes the opening context

BeachOS confirms:

- the individual signed-in Staff Member;
- Host responsibility;
- the required Venue-opening Capability;
- the Venue;
- the current Business Date;
- the Venue is Closed;
- the six mandatory Operational Departments;
- each responsible person;
- the current declaration from each department.

BeachOS opens the Opening Readiness screen.

### Host understanding

The Host is looking at the current opening for the correct Venue and Business Date.

## Step 3 — The Host sees declarations pending

The screen shows:

- Kitchen — READY;
- Bar — NO DECLARATION;
- Beach Operations — READY;
- Cleaning — NOT READY;
- Maintenance — READY;
- Cashier — READY.

Cleaning shows:

- responsible person;
- reason: “Beach cleaning is still in progress”;
- confirmation time.

Bar shows:

- responsible person;
- “No declaration received.”

The screen states:

- Venue: Closed;
- “Waiting for department readiness”;
- Open Venue is disabled;
- “One department is NOT READY”;
- “One readiness declaration is missing.”

### Host action

The Host selects “Review unresolved departments.”

BeachOS moves focus first to Cleaning and then Bar.

### Host understanding

The Host knows exactly who needs follow-up and why. The Host does not have an action
to edit either declaration.

## Step 4 — The Host coordinates human follow-up

The Host contacts the responsible people for Cleaning and Bar through normal Venue
communication.

BeachOS does not:

- create a task;
- send a message;
- create an incident;
- mark either issue resolved;
- allow the Host to declare READY.

### Host understanding

BeachOS provides confirmed operational truth. Human coordination remains the Host’s
responsibility.

## Step 5 — Bar declares READY

The Bar responsible person verifies the department and submits READY in their own
authorized context.

BeachOS receives the confirmed `Department Readiness Declared` fact.

The Host sees:

- toast: “Bar readiness updated to READY”;
- Bar updated to READY with its responsible person and confirmation time;
- the missing-declaration count removed;
- Cleaning still NOT READY;
- Open Venue still disabled.

### Host understanding

One required condition is resolved, but the Venue is not eligible to open.

## Step 6 — Cleaning declares READY

After completing the work, the Cleaning responsible person verifies readiness and
submits READY.

BeachOS receives the new confirmed `Department Readiness Declared` fact.

The Host sees:

- toast: “Cleaning readiness updated to READY”;
- all six mandatory departments marked READY;
- the screen transition to Ready to Open.

### System requirement

Cleaning does not become READY merely because time passed or because the previous
reason appears resolved. The responsible person’s new declaration creates the
change.

## Step 7 — The Host reviews Ready to Open

The screen shows:

- Venue;
- Business Date;
- Venue state: Closed;
- “All mandatory departments are READY”;
- all six mandatory departments;
- each responsible person;
- each READY confirmation time;
- “You are authorized to open this Venue”;
- enabled “Open Venue” action.

The screen explains:

- opening records the official operational start;
- opening makes the Opening Report official;
- opening allows later Guest Arrival, Customer Groups, and Orders only under their
  own rules;
- opening itself creates no Customer Group, Bill, charge, Order, transfer, or
  Payment.

### Host action

The Host reviews the complete list and selects “Open Venue.”

### System requirement

Selecting Open Venue does not yet perform the business action.

## Step 8 — The Host receives the confirmation

BeachOS opens the “Open this Venue?” confirmation.

The confirmation shows:

- Venue;
- Business Date;
- “All mandatory departments are READY”;
- the official effect of the action;
- the statement that no Customer Group or financial or ordering action will be
  created.

The available actions are:

- “Confirm Open Venue”;
- “Cancel.”

### Host action

The Host verifies the Venue and Business Date, then selects “Confirm Open Venue”
once.

### System requirement

Immediately before accepting the intention, BeachOS rechecks:

- every mandatory department remains READY;
- the Venue remains Closed;
- Venue and Business Date are unchanged;
- the Host still has Host responsibility;
- the Host still has the required Capability;
- central state is current.

All checks pass.

## Step 9 — BeachOS confirms the opening

The confirmation closes.

BeachOS displays Opening in Progress:

- “Opening Venue”;
- Venue;
- Business Date;
- Host;
- “Opening is being confirmed”;
- “Do not repeat the action.”

Open Venue is unavailable. Back and sign out cannot expose or obscure a second
opening attempt.

### Host action

The Host waits. No second action is required.

### System requirement

BeachOS processes one `Open Venue for Business Date` intention. It does not show
success optimistically and does not produce a `Venue Opening Started` Domain Event.

## Step 10 — The opening succeeds

The central system authoritatively confirms the completed outcome.

The outcome produces:

- `Venue Opened for Business Date`;
- the official Opening Report;
- the required `Activity Logged`.

BeachOS displays Opening Successful:

- “Venue Open”;
- “The Venue is open for this Business Date”;
- Venue;
- Business Date;
- official opening time;
- Host;
- “All mandatory departments were READY at opening”;
- “Official Opening Report is available.”

### Host understanding

The opening is now a confirmed business fact. It is no longer pending, assumed, or
based on a device-only state.

## Step 11 — The Host continues to the opened Venue

The Host selects “Continue to Venue.”

BeachOS displays the Sprint 1 Venue Open destination:

- Venue;
- Business Date;
- official opening time;
- opening Host;
- “Venue opening is complete”;
- “View Opening Report.”

No Open Venue action remains.

No Guest Arrival, Service Location, Customer Group, Order, preparation, Bill,
Payment, Manager Dashboard, or Venue-closing feature appears in Sprint 1.

## Successful journey outcome

The Host has:

- entered the correct Venue-opening context;
- identified unresolved departments;
- coordinated human follow-up;
- observed declarations made by the correct responsible people;
- waited until every mandatory department was READY;
- reviewed the complete readiness state;
- intentionally confirmed OPEN VENUE;
- received no false or premature success;
- received authoritative confirmation;
- reached the Venue Open state;
- gained access to the permanent Opening Report.

The Host has not:

- verified departments on their behalf;
- changed another person’s declaration;
- bypassed authorization;
- overridden a blocker;
- opened automatically because of time;
- created a Customer Group;
- created a Bill, charge, Order, transfer, or Payment;
- repeated the opening action.
