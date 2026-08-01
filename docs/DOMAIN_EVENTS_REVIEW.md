# Domain Events Review

## 1. Outcome

`DOMAIN_EVENTS.md` now defines the official business-event language for the current BeachOS domain.

The catalogue:

- uses completed business facts rather than technical interactions;
- preserves current Domain Model and Decision Log authority;
- separates Domain Events, Commands, business rules, Activity Logs, and Audit Trails;
- evaluates suggested event names rather than accepting them automatically;
- defines workflow engineering contracts for Venue Opening and Guest Arrival;
- introduces no API, database, message broker, queue, event-sourcing, or infrastructure design.

No existing file was modified.

## 2. Files reviewed

The complete repository was reviewed, with particular attention to:

- `docs/DECISIONS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/PROJECT_GLOSSARY.md`;
- `docs/PRODUCT_REQUIREMENTS.md`;
- `docs/MASTER_BLUEPRINT.md`;
- `docs/PRODUCT_PHILOSOPHY.md`;
- `docs/MISSION_AND_VALUES.md`;
- `docs/DOMAIN_REVIEW_REPORT.md`;
- `docs/PRODUCT_REVIEW_UPDATE_REPORT.md`;
- `docs/GLOSSARY_REVIEW.md`;
- `framework/FRAMEWORK_INTRODUCTION.md`;
- `framework/FRAMEWORK_PRINCIPLES.md`;
- `framework/03 Roles/HOST.md`;
- `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`;
- `framework/04 Workflows/GUEST_ARRIVAL_WORKFLOW.md`;
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`;
- repository governance, engineering foundation, application placeholders, infrastructure configuration, scripts, tests, and GitHub collaboration files.

## 3. Event counts

- **Accepted current events:** 56
- **Future approved events:** 1
- **Future approved event:** `Zone Template Applied`
- **Existing Domain Model names excluded from the accepted catalogue:** 2
  - `Transfer Started` — excluded because it describes an incomplete process rather than a completed business fact.
  - `Bill Reopened` — excluded because the Domain Model explicitly forbids it until a future accepted exception exists.
- **Additional accepted event made explicit from accepted decisions:** 1
  - `Financial Obligation Created` — supported by DEC-033 and DEC-034 and required to distinguish the reason money becomes owed from the resulting Bill and Bill Line.

Several current events are marked **Command gated**. Their completed meaning is supported, but Command design must wait for unresolved authority, lifecycle, correction, or completion rules.

## 4. Rejected or misleading event names

The catalogue rejects or restricts these names:

- Button Clicked
- NFC Scanned
- Service Location Identified
- API Called
- Database Updated
- Record Inserted
- Sync Completed
- Table Opened
- Visit Created
- Order Saved
- Order Updated
- Order Item Routed
- Preparation Ticket Created
- Preparation Started
- Preparation Completed
- Item Delivered
- Customer Group Transferred
- Customer Group Moved
- Department Readiness Changed
- Opening Report Created
- Payment Attempted
- Payment Confirmed
- Bill Corrected
- Bill Reopened
- Customer Group Reopened
- Guest Token Issued
- VIP Recognized
- Waiting List Entry Created
- Staff Performance Scored

Some are prohibited because they are technical rather than business language. Others duplicate an accepted event, describe an incomplete interaction, or depend on an unapproved lifecycle.

## 5. Contradictions and inconsistencies discovered

### Transfer Started conflicts with the completed-fact definition

The Domain Model lists `Transfer Started` as an optional Domain Event but explicitly states that it is not yet a completed business fact and must not imply movement.

The new catalogue excludes it from official Domain Events. It may later be defined as a workflow status, attempt record, or another concept if the Product Owner approves that distinction.

### Bill Reopened is named but forbidden

The Domain Model lists `Bill Reopened`, then states that it is forbidden until a future approved exception exists.

The catalogue treats it as unavailable, not current or future approved.

### Product Requirements imply reopening more broadly

Product Requirements state that a closed group cannot accept new Orders unless a Manager reopens it and list Reopen Bill among example Capabilities. The Domain Model forbids Bill reopening until a future rule is accepted, and Customer Group reopening is not approved.

The stricter Domain Model and Decision Log boundary should govern until the Product Owner resolves the inconsistency.

### Responsible Waiter and Responsible Service Staff differ

The Domain Model and accepted DEC-035 use Responsible Waiter. The Project Glossary defines Responsible Service Staff as the official venue-neutral concept while preserving the current waiter-specific rule.

The event catalogue retains the existing Domain Model event names to avoid silently changing DEC-035. Cross-industry event naming needs a controlled terminology decision.

### Payment Recorded and Payment Confirmed differ

The Domain Model event is `Payment Recorded`, while the requested examples and business wording naturally suggest `Payment Confirmed`.

Because the Project Glossary defines a Payment as value confirmed as received, both phrases point to the same concept. The catalogue keeps `Payment Recorded` as the existing official event name and rejects a second synonym pending approved alignment.

### Opening Report Created is not separately defined

DEC-039 and the Venue Opening Workflow make the permanent Opening Report an outcome of opening. They do not define an independent Command or event for creating it.

The catalogue treats the report as an atomic result of `Venue Opened for Business Date`.

### Completion events exist before completion rules

The Domain Model contains:

- `Customer Group Completed`;
- `Kitchen Ticket Completed`;
- `Bar Ticket Completed`;
- `Bill Closed`.

The repository also records that exact completion and closing rules remain unresolved. The event meanings are retained, but their Commands are gated.

### Shift events exist while first-version Shift scope remains open

`Shift Started`, `Shift Ended`, and `Shift Handover Completed` exist in the Domain Model. Product review still asks whether Shift belongs in the first version and how handover works.

The events remain current domain vocabulary but are Command gated.

## 6. Unresolved business decisions

Command design remains blocked or partial for:

1. Guest Token lifecycle.
2. Customer Group completion.
3. Customer Group cancellation and reopening.
4. Bill closing and reopening.
5. Bill correction and reversal.
6. Partial and split Payments.
7. Payment allocation, overpayment, change, tips, refunds, and reversal.
8. Transfer eligibility and charging consequences.
9. Responsible Service Staff handover.
10. Bar and Kitchen readiness, completion, and delivery.
11. Shift scope, start, end, and handover.
12. Venue closing.
13. Service Location state correction.
14. Zone overlap.
15. Zone Template lifecycle beyond application.
16. Complaint and incident lifecycle.
17. Operational coaching records.
18. Guest Profile and VIP lifecycle.
19. Digital waiting-list lifecycle.
20. Organization and Venue deactivation.
21. Menu and price governance.
22. Capability grant and revocation governance.

The catalogue does not resolve any of these matters.

## 7. Documents that may require later alignment

After Product Owner approval, consider aligning:

- `docs/DOMAIN_MODEL.md`
  - remove or reclassify `Transfer Started`;
  - keep `Bill Reopened` outside the event catalogue until approved;
  - add `Financial Obligation Created` if it is accepted as a first-class Domain Event;
  - clarify which completion events are semantic placeholders versus executable current outcomes.
- `docs/PRODUCT_REQUIREMENTS.md`
  - remove or qualify Manager reopening language until Bill and Customer Group reopening are approved.
- `docs/PROJECT_GLOSSARY.md`
  - add official Domain Event and Command definitions;
  - decide Responsible Waiter versus Responsible Service Staff event naming;
  - decide Payment Recorded versus Payment Confirmed.
- `docs/DECISIONS.md`
  - record future decisions for completion, closing, corrections, refunds, handovers, Shift, and Venue closing.
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`
  - align exact completion transitions after owner decisions.
- future preparation, transfer, payment, closing, and handover workflows
  - cite the official event names and preserve the Command gates in this review.

No alignment was performed in this task.

## 8. Readiness for Command design

### Ready now

The domain is ready for business Command design for:

- declaring Operational Department readiness;
- opening the Venue for a Business Date;
- identifying a Service Location as a non-event-producing lookup action;
- assigning the initial Responsible Waiter;
- opening a Customer Group;
- creating the immediate Beach Sunbed Financial Obligation and Bill;
- submitting or rejecting an Order;
- creating Bar and Kitchen Tickets;
- recording or rejecting a full Payment, subject to agreed Payment Method details;
- basic Zone creation, renaming, reassignment, and deletion, subject to the one-Zone assumption.

### Ready only after owner decisions

The domain is not ready for final Command design for:

- Customer Group completion, cancellation, or reopening;
- Bill closing exceptions, correction, or reopening;
- Payment reversal, refunds, partial Payments, split Payments, and allocation;
- Responsible Waiter changes and Shift handovers;
- transfer combinations and charging effects;
- Bar and Kitchen completion;
- Venue closing;
- Guest Token;
- waiting lists, VIP recognition, complaints, incidents, and coaching records.

## 9. Recommendation

The current domain is **partially ready for Command design**.

Venue Opening and the approved portion of Guest Arrival have sufficiently explicit actors, preconditions, outcomes, invariants, and event facts for business Command design.

The domain as a whole is not ready for complete Command design. The Product Owner should resolve the completion, financial exception, transfer, handover, preparation, and closing decisions before Commands for those areas are finalized.

## 10. Stop point

The Domain Event catalogue and review are complete. No existing documentation or implementation file was changed.
