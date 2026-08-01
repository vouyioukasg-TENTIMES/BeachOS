# Customer Group Lifecycle

## Purpose

This document defines the operational states and permitted state transitions of a Customer Group.

It is a lifecycle reference, not a description of software screens or technical storage. It uses only business rules already present in the Domain Model and accepted Decisions.

The governing decisions are:

- DEC-011 — one active Customer Group per Service Location;
- DEC-012 — preserve Customer Group identity during transfer;
- DEC-013 — route submitted items by preparation destination;
- DEC-030 — Service Location identification performs no operational or financial action;
- DEC-031 — Customer Group is the primary operational entity;
- DEC-033 — create a Bill only when a Financial Obligation exists;
- DEC-034 — Beach Sunbed opening creates the immediate approved obligation;
- DEC-035 — only the Responsible Waiter opens a Customer Group;
- DEC-036 — each submitted Order is one Order Round;
- DEC-038 — Capabilities authorize protected actions;
- DEC-039 — the Venue must be officially open before new Customer Groups are allowed.

## Lifecycle boundary

A Customer Group begins only when the Responsible Waiter intentionally completes the official opening action.

Before that moment, guests may have entered the Venue, spoken with the Host, waited, accepted a Service Location, been escorted, and had the location identified. None of those facts creates a Customer Group. **Not Yet Opened** is therefore a precondition, not a Customer Group state.

The accepted domain supports two durable Customer Group lifecycle states:

1. **Active**
2. **Completed**

The following are not separate Customer Group lifecycle states:

- with no Bill;
- with an open Bill;
- Bill fully paid;
- payment requested;
- waiting for preparation;
- preparation ready;
- transfer in progress;
- Responsible Waiter handover in progress;
- physically moving between Service Locations.

These are financial conditions, operational conditions, or workflows involving an Active Customer Group. Treating them as separate lifecycle states would incorrectly prevent the group from continuing to own its Service Location, Orders, optional Bill, Payments, Responsible Waiter, and History.

Cancellation is not currently an available lifecycle state. The Domain Model allows it only under a future approved exceptional rule, and no such rule has been accepted.

Reopening a Completed Customer Group is not approved.

---

# State 1 — Active

## Business meaning

Active means official service has begun and the Customer Group remains the primary operational entity for the party.

While Active, the Customer Group:

- occupies exactly one Service Location;
- has exactly one Responsible Waiter;
- owns zero or more Orders;
- may have no Bill or one Bill;
- owns any Payments through its Bill;
- preserves its complete History;
- may continue across Staff Shifts;
- may move to another approved available Service Location without changing identity.

## Entry conditions

All of the following must be true:

1. The Venue is officially open for the current Business Date under DEC-039.
2. The guests are at an approved available Service Location.
3. The Service Location does not already have an active Customer Group under DEC-011.
4. The Service Location has been correctly identified.
5. One eligible Staff Member has accepted the Responsible Waiter responsibility.
6. That Responsible Waiter holds Open Customer Group.
7. The Responsible Waiter intentionally performs the official opening action under DEC-035.
8. Every required business check succeeds as one complete outcome.
9. If the Service Location is a Beach Sunbed, the Responsible Waiter confirms the applicable approved Beach Sunbed charge under DEC-034.

NFC or manual Service Location identification does not satisfy the opening action and cannot enter the Customer Group into Active state (DEC-030).

## Exit conditions

An Active Customer Group may exit to Completed only when the approved completion conditions are satisfied.

The accepted Domain Model establishes that:

- any Bill must satisfy its approved closing conditions;
- all outstanding operational work must satisfy the approved completion rules;
- a Customer Group that never received a Financial Obligation may complete without ever having a Bill.

The exact completion authority, final completion sequence, and relationship between Bill closing and Customer Group completion remain open Product Owner decisions. Until those rules are accepted, implementation must not assume that full Payment, zero Balance, Bill closing, departure, or elapsed time alone automatically completes the Customer Group.

## Automatic actions

### On successful entry

- The Customer Group becomes Active.
- The selected Service Location becomes occupied by that Customer Group.
- The Responsible Waiter is recorded.
- The opening time and Venue context become part of History.
- The Customer Group becomes the owner of its Service Location, future Orders, optional Bill, Payments through that Bill, Responsible Waiter, and History under DEC-031.

### When opening at a Beach Sunbed

- The approved Beach Sunbed Financial Obligation arises immediately.
- A Bill is created because the first Financial Obligation exists.
- The applicable charge becomes a preserved financial fact.

These actions follow the Responsible Waiter’s intentional opening decision. NFC identification, Host seating, or the passage of time cannot trigger them.

### When opening at another Service Location type

- No Bill is created merely because the Customer Group opened.
- The Customer Group remains Active without a Bill until its first approved Financial Obligation exists.

### When the first Financial Obligation arises

- A Bill is created if none exists.
- The Bill becomes the single running financial obligation for the Customer Group under the current approved model.

### When an Order is submitted

- The submitted Order becomes one preserved Order Round under DEC-036.
- Its approved financial effect contributes to the Customer Group’s Bill.
- If it creates the first Financial Obligation, the Bill is created.
- Bar and Kitchen work is separated by the configured preparation destination under DEC-013.
- A later Order does not overwrite an earlier Order.

### When a transfer completes

- The same Customer Group moves to the approved available destination Service Location.
- The old Service Location is released.
- The destination becomes occupied.
- Orders, optional Bill, Payments, Responsible Waiter, and History remain with the same Customer Group under DEC-012.
- The transfer becomes part of History.

Transfer does not create a new Customer Group and does not change the lifecycle state from Active.

### When the Responsible Waiter changes

- The Customer Group remains Active.
- Exactly one new Responsible Waiter becomes accountable.
- The previous and new responsibility become part of History.

The exact handover and acceptance process remains an open business decision.

### When Payment is recorded

- The confirmed Payment reduces the Bill’s remaining Balance.
- The Customer Group remains Active unless separately approved completion conditions are satisfied.
- A zero Balance does not itself bypass Bill closing or Customer Group completion requirements.

## Human actions

While the Customer Group is Active, authorized people may perform only the actions allowed by their Capabilities and the applicable business rules.

Accepted human actions include:

- the Responsible Waiter intentionally opening the Customer Group;
- the Responsible Waiter or another authorized Staff Member submitting separate Order Rounds;
- an authorized Staff Member requesting or performing an allowed complete transfer;
- an authorized Staff Member changing the Responsible Waiter under the future approved handover rules;
- Bar and Kitchen Staff progressing their own preparation work;
- an authorized Cashier or Staff Member recording a confirmed Payment;
- an authorized Staff Member closing the Bill only when its approved closing conditions are satisfied;
- authorized correction, cancellation, or reversal actions where their specific rules allow them.

The following human actions are not authorized merely by the Customer Group being Active:

- the Host opening the Customer Group;
- creating a second active Customer Group at the same Service Location;
- deleting the Customer Group;
- silently changing submitted Orders or financial History;
- splitting or combining Customer Groups;
- reopening a closed Bill without a future approved exception;
- completing the Customer Group through an undefined shortcut.

## Allowed transitions

### Not Yet Opened → Active

Allowed only through the Responsible Waiter’s intentional and successful Customer Group opening action.

Not Yet Opened is the pre-lifecycle context, not a stored Customer Group state.

### Active → Active

The Customer Group remains Active when:

- another Order Round is submitted;
- its first Financial Obligation creates the Bill;
- further Financial Obligations or Bill Lines are added;
- a Payment is recorded;
- the Bill becomes fully paid but completion has not occurred;
- preparation work changes status;
- the Responsible Waiter changes;
- the Customer Group transfers to another approved available Service Location;
- a Staff Shift changes;
- an authorized correction or cancellation preserves the group’s continuing service.

These are changes within the Active state, not lifecycle transitions to new Customer Groups.

### Active → Completed

Allowed only after the approved completion conditions are satisfied.

The Domain Model permits the transition, but the repository still requires Product Owner decisions defining:

- the exact conditions that complete service;
- who may confirm completion;
- whether Bill closing and Customer Group completion are one action or separate actions;
- when the Service Location is released if operational work remains;
- how a no-Bill Customer Group is completed;
- which exceptional conditions may prevent or delay completion.

Until these decisions are accepted, the transition must not be implemented through assumed rules.

## Invalid transitions

### Not Yet Opened → Completed

Invalid. A Customer Group cannot complete if it never became Active.

### Identification → Active

Invalid. NFC or manual Service Location identification performs no opening action under DEC-030.

### Host seating → Active

Invalid. Seating and escort do not create a Customer Group. Only the Responsible Waiter opens it under DEC-035.

### Venue opening → Active

Invalid. OPEN VENUE allows new Customer Groups but does not create one under DEC-039.

### Active → Not Yet Opened

Invalid. Once official service begins, History cannot be erased by pretending the Customer Group never existed.

### Active → Deleted

Invalid. The primary operational record and its History must not be silently deleted.

### Active → New Customer Group because of transfer

Invalid. Transfer preserves Customer Group identity under DEC-012.

### Active → Two Active Customer Groups through splitting

Invalid in the initial domain. Splitting or combining Customer Groups requires a future approved rule.

### Active → Cancelled

Invalid until an exceptional cancellation rule defines conditions, authority, consequences, and History.

### Active → Completed because Balance reaches zero

Invalid as an automatic assumption. Bill Fully Paid does not bypass other closing or completion requirements.

### Active → Completed because the Bill closes

Not approved as an automatic assumption. The relationship between Bill closing, outstanding operational work, Customer Group completion, and Service Location release remains an open decision.

---

# State 2 — Completed

## Business meaning

Completed means the Customer Group’s active service has ended after its approved financial and operational completion conditions were satisfied.

The Customer Group remains a permanent historical business fact. Completion ends new ordinary activity; it does not erase the party’s service history.

## Entry conditions

The accepted Domain Model requires:

1. The Customer Group was previously Active.
2. Any Bill has satisfied the approved closing conditions.
3. All outstanding operational work has satisfied the approved completion rules.
4. The completion outcome is confirmed through an authorized and traceable process.
5. A Customer Group that never had a Financial Obligation may complete without a Bill.

The exact person, Capability, sequence, and evidence required to confirm completion are not yet approved. These conditions define the boundary but are not sufficient to invent an implementation.

## Exit conditions

Completed is a terminal Customer Group lifecycle state under the current accepted domain.

There is no approved exit from Completed.

The Customer Group remains available for authorized historical review, reporting, support, and accountability. Historical access does not make it Active again.

## Automatic actions

When the Customer Group validly becomes Completed:

- active service ends;
- the Service Location becomes available, provided it is not otherwise unavailable;
- the Customer Group stops accepting new Orders;
- ordinary financial activity stops;
- the final Service Location, Responsible Waiter, Orders, optional Bill, Payments, and relevant Activity Logs remain connected to its permanent History;
- later Menu, price, Zone, Role, or Service Location changes do not rewrite that History.

No automatic action may silently delete, anonymize, merge, split, or reactivate the Customer Group without a separate approved rule.

## Human actions

After completion, authorized people may:

- review the Customer Group’s preserved History;
- review its Orders, optional Bill, Payments, Service Location history, and responsibility history where their business responsibility permits;
- include the completed Customer Group in approved reporting;
- investigate a support, financial, security, or accountability matter;
- perform only those correction or reversal actions that have separately approved authority and rules.

Authorized people may not:

- add an ordinary new Order;
- continue ordinary Billing or Payment activity;
- transfer the Customer Group to another Service Location;
- change its Responsible Waiter as if service were continuing;
- erase or silently rewrite its History;
- reopen it through an unapproved Manager exception.

## Allowed transitions

### Completed → Completed

Historical review, reporting, and approved append-only accountability activity do not change the lifecycle state.

A permitted correction, reversal, or later explanatory Activity Log must preserve the original facts and does not automatically reactivate the Customer Group.

No other transition is currently approved.

## Invalid transitions

### Completed → Active

Invalid. Customer Group reopening has not been approved.

### Completed → Not Yet Opened

Invalid. Completion cannot erase the fact that service occurred.

### Completed → Deleted

Invalid. Completed Customer Groups and their operational and financial History are permanent.

### Completed → Transferred

Invalid. Transfer belongs to an Active Customer Group.

### Completed → New Order

Invalid. A Completed Customer Group cannot receive new ordinary Orders.

### Completed → New ordinary Payment or Financial Obligation

Invalid. Ordinary financial activity has ended. Any exceptional correction, reversal, refund, or reopened financial process requires its own approved rules and Capabilities.

### Completed → Cancelled

Invalid. Cancellation is not an approved post-completion rewrite.

---

# Financial conditions within Active

The presence and status of a Bill matter operationally, but they do not create separate Customer Group identities or lifecycle states.

## Active without Bill

This condition is valid when:

- the Customer Group has opened;
- no approved Financial Obligation has yet arisen;
- the Service Location type does not create an immediate approved obligation.

Allowed activity includes service coordination and an Order Round that may create the first obligation and Bill.

Opening at a Beach Sunbed cannot result in this condition because DEC-034 creates the immediate approved Beach Sunbed obligation.

## Active with open Bill

This condition begins when the first approved Financial Obligation creates the Bill.

The Bill aggregates approved obligations from all Order Rounds and other approved charges. Payments reduce its Balance. The Customer Group remains Active during ordinary ordering, preparation, transfer, payment, and Bill review.

## Active with fully paid Bill

This condition exists when valid Payments reduce the Bill Balance to zero but the Customer Group has not yet completed.

Bill Fully Paid is a financial fact, not Customer Group completion. Other approved Bill-closing or operational-completion conditions may remain.

## Active with closed Bill

The accepted documents do not yet fully define whether an Active Customer Group may remain temporarily active after its Bill closes or whether Bill closing and Customer Group completion occur together.

Do not implement this as a permanent state or forbid it through assumption. The Product Owner must first decide the exact completion sequence and Service Location release rule.

# Events that do not change lifecycle state

The following events may be important and auditable while the Customer Group remains Active:

- Responsible Waiter Assigned;
- Responsible Waiter Changed;
- Order Submitted;
- Order Item Cancelled;
- Order Item Corrected;
- Kitchen Ticket Created;
- Bar Ticket Created;
- preparation status changes;
- Bill Created;
- Bill Line Added;
- Bill Line Reversed;
- Payment Recorded;
- Payment Rejected;
- Payment Reversed;
- Bill Fully Paid;
- Transfer Started;
- Transfer Completed;
- Transfer Rejected;
- Shift Handover Completed;
- Activity Logged.

Some of these events depend on business rules that are still open. Their presence in the Domain Model does not grant authority or define an unapproved workflow.

# Transition summary

| From | Trigger | To | Current status |
|---|---|---|---|
| Not Yet Opened | Responsible Waiter intentionally opens at an available Service Location while authorized and all rules pass | Active | Accepted |
| Active | First approved Financial Obligation creates a Bill | Active | Accepted |
| Active | Submit another Order Round | Active | Accepted |
| Active | Complete an approved transfer | Active | Accepted, with transfer details still requiring owner decisions |
| Active | Change Responsible Waiter | Active | Accepted in principle; exact handover remains open |
| Active | Record Payment or reach zero Balance | Active | Accepted; does not itself complete the group |
| Active | Satisfy all approved completion conditions | Completed | Accepted in principle; exact completion workflow remains open |
| Completed | Review History or add separately approved accountability information | Completed | Accepted |
| Completed | Reopen ordinary service | Active | Forbidden until a future accepted decision |
| Active | Cancel through exceptional rule | Cancelled | Unavailable until a future accepted decision |

# Unresolved decisions that block a more detailed lifecycle

This lifecycle must remain deliberately simple until the Product Owner approves:

1. The exact conditions that complete a Customer Group.
2. Who may confirm Customer Group completion and which Capability is required.
3. Whether Bill closing and Customer Group completion are one action or two.
4. When the Service Location becomes available if preparation or other operational work remains.
5. How a Customer Group without a Bill completes.
6. Whether cancellation is required and, if so, its conditions, authority, consequences, and History.
7. Whether a Completed Customer Group may ever be reopened.
8. The exact Responsible Waiter handover and acceptance process.
9. The allowed transfer source and destination combinations.
10. The financial effect of transfers between differently priced Physical Rows or into a Beach Sunbed.
11. Which Payment reversals, refunds, corrections, or post-closing exceptions are allowed.

Until those decisions are accepted, BeachOS must preserve the two-state lifecycle and must not introduce hidden intermediate or exceptional states.
