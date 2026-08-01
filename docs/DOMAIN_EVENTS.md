# BeachOS Domain Events

## 1. Purpose and authority

This document defines the official business events of the current BeachOS domain.

A **Domain Event** is a meaningful business fact that has already happened. It describes an outcome the business may rely upon, such as a Venue opening, an Order being accepted, or a Payment being confirmed as received.

A Domain Event:

- records a completed business fact;
- uses official business language;
- describes what happened, not how software handled it;
- may result from a human decision, a business rule, or both;
- does not authorize an action;
- does not prove that the actor had authority unless the event definition requires that authority as a precondition;
- does not replace a Command, business rule, Activity Log, Audit Trail, or operational workflow;
- does not imply event sourcing or any particular technical architecture.

A **Command** expresses an intention to perform an action. A Domain Event states that the intended outcome, rejection, correction, or reversal has already occurred.

A **business rule** decides whether an action is permitted and what consequences follow. An event records the result after those rules have been applied.

An **Activity Log** is the accountable record of one sensitive or exceptional action. A Domain Event describes the business fact itself. One business outcome may produce both a Domain Event and an Activity Log.

An **Audit Trail** is the connected chronological history assembled from relevant Domain Events, Activity Logs, and preserved business records. It is not a single event.

This catalogue is governed by:

- `docs/DECISIONS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/PROJECT_GLOSSARY.md`;
- `docs/PRODUCT_REQUIREMENTS.md`;
- `framework/03 Roles/HOST.md`;
- `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`;
- `framework/04 Workflows/GUEST_ARRIVAL_WORKFLOW.md`;
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`.

No new event may be added merely because it sounds useful. It must be supported by an accepted decision, an approved workflow, or the existing Domain Model. Event names use the past tense.

## Event status terms

- **Current:** Supported by the present domain. It may be used in current workflow and Command design.
- **Current — Command gated:** The completed business fact is supported, but one or more rules governing the action are still unresolved. The event may be discussed, but the Command must not be finalized until those decisions are approved.
- **Future approved:** The concept has been accepted for a future capability but is not part of the current implementation scope.
- **Unavailable:** The event is not currently permitted or supported.

## Audit importance terms

- **Critical:** Affects money, authority, security, permanent responsibility, or another high-risk business outcome. An Activity Log is required.
- **High:** Material to live operations or permanent history. It requires durable business history; an Activity Log is required when the Domain Model or accepted audit rules classify the action as sensitive.
- **Standard:** The business record itself normally provides the required history. A separate Activity Log is not automatically required.

## 2. Event naming rules

1. **Use past tense.** Use `Order Submitted`, not `Submit Order`.
2. **Name a completed business fact.** An event states what the business may now rely upon.
3. **Use one official business name per concept.** Do not create synonyms for the same fact.
4. **Name the business outcome, not the interface interaction.** Use `Customer Group Opened`, not `Open Button Clicked`.
5. **Avoid technical language.** Do not use `API Called`, `Record Inserted`, `Database Updated`, `Message Published`, or `Sync Completed`.
6. **Separate intention from outcome.** A request or Command is not a Domain Event until a meaningful result occurs.
7. **Distinguish success and rejection.** `Order Submitted` and `Order Submission Rejected` have different business meanings.
8. **Distinguish an attempt from confirmed value.** A Payment attempt does not reduce a Bill Balance. Only a confirmed Payment does.
9. **Distinguish correction from rewriting.** Use an approved corrected or reversed fact while preserving the original.
10. **Distinguish ready from completed.** Preparation readiness and completion are not interchangeable.
11. **Do not create an event for every derived detail.** Several facts may result from one atomic business action without requiring separate Commands.
12. **Do not turn a workflow step into an event automatically.** Greeting, escorting, checking, and identifying may be important work without being Domain Events.
13. **Preserve venue-specific accepted names where required.** The current Domain Model uses `Responsible Waiter` for the Beach Club rule. Cross-industry terminology requires later alignment with `Responsible Service Staff`.
14. **Use rejection only for a completed negative outcome.** A rejected action confirms that the requested business change did not occur.

## 3. Event catalogue

The catalogue contains **56 current events** and **1 future approved event**.

Some current events are marked **Command gated** because their completed meaning is known while the authority, preconditions, or detailed workflow remains unresolved.

### 3.1 Organization, Venue, and Business Date

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Organization Established | An approved operating business has entered the Emerald domain. | Authorized business setup is approved. | The Organization has a clear identity and authorized representative. | The Organization may contain Venues and preserve Organization-level history. | Organization, Venue | DEC-001, DEC-002 | High; permanent business history | Current |
| Organization Deactivated | The Organization has stopped new operation while its history remains preserved. | Authorized leadership completes deactivation. | Active operational obligations have been resolved through an approved process. | No new ordinary activity is permitted; history remains. | Organization, Venue, History | DEC-001, DEC-009 | Critical; Activity Log required | Current — Command gated because deactivation procedure is not detailed |
| Venue Established | A physical hospitality operation has been added under an Organization and is ready for setup. | Authorized Venue setup is approved. | Parent Organization exists. | Venue configuration may begin. | Organization, Venue | DEC-001, DEC-002 | High; permanent business history | Current |
| Venue Activated | A configured Venue has been approved for live use generally. | Authorized leadership approves activation. | Essential Venue setup and operating rules are approved. | The Venue may participate in live operation, subject to daily opening. | Venue, Area, Service Location | DEC-001 | Critical; Activity Log required | Current — Command gated because activation approval is not detailed |
| Department Readiness Declared | One Operational Department’s responsible person has declared READY, NOT READY, or BLOCKED for the current opening. | The responsible person verifies the department and submits its declaration. | Venue opening is in preparation; the department and responsible person are known; NOT READY and BLOCKED include a reason. | The current readiness declaration becomes part of the opening context and later Opening Report. | Operational Department, Department Readiness, Staff Member, Opening Report | DEC-039 | High; permanent Opening Report history required | Current |
| Venue Opened for Business Date | The Venue has officially begun operation for the Business Date. | The authorized Host intentionally executes OPEN VENUE. | Every mandatory Operational Department is READY; the Host holds the required Capability. | Guest arrivals, new Customer Groups, and Orders become allowed; operational timers and daily measures begin; the Opening Report becomes official. | Venue, Business Date, Host, Opening Report, Operational Department | DEC-038, DEC-039 | Critical; Opening Report and Activity Log required | Current |
| Venue Deactivated | A Venue has stopped accepting new live activity while history remains preserved. | Authorized leadership completes deactivation. | Active operation has been resolved through an approved process. | No new live Venue activity is allowed. | Venue, Organization, History | DEC-001, DEC-009 | Critical; Activity Log required | Current — Command gated because deactivation procedure is not detailed |
| Area Established | A major physical part of a Venue has been formally recognized. | Authorized Venue setup establishes the Area. | Venue exists; the Area belongs to that Venue. | Service Locations may be organized within the physical Area. | Venue, Area, Service Location | None specific; supported by Domain Model | Standard; permanent setup history | Current |

#### Venue event evaluations

- **Venue Opening Started** is not an official event. The opening workflow may begin operationally, but no accepted decision defines that beginning as a durable business fact.
- **Department Readiness Changed** is not a separate event. A later `Department Readiness Declared` records the new declaration while the Opening Report preserves relevant declaration history.
- **Opening Report Created** is not separate from `Venue Opened for Business Date`. The report becomes official as part of that one successful business action.
- `Venue Activated` describes general permission for live use. `Venue Opened for Business Date` describes the daily operational start. They must not be confused.

### 3.2 Service Location

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Service Location Made Available | A Service Location has become eligible to receive a Customer Group or transfer. | Authorized operational action resolves any reason for unavailability. | The location exists, is not retired, and has no active Customer Group. | The Service Location may be selected under applicable rules. | Service Location, Available, Customer Group | DEC-011, DEC-030 | High when availability was manually changed; Activity Log required for sensitive correction | Current |
| Service Location Made Unavailable | A Service Location has been intentionally blocked from receiving a Customer Group or transfer. | Authorized operational action declares it unavailable. | The effect on any active Customer Group has been safely resolved. | The Service Location cannot receive new occupancy or transfer. | Service Location, Unavailable, Customer Group | DEC-011, DEC-030 | High; reason and actor should be traceable | Current — Command gated because detailed unavailability rules are open |

#### Service Location event evaluations

- **Service Location Identified** is not an official Domain Event. NFC or manual identification resolves the stable Service Location Digital Identity and retrieves current context; it performs no operational or financial action under DEC-030.
- **NFC Scanned** is a technical interaction, not a business fact.
- **Service Location State Corrected** is not currently defined. A future correction rule must state what was wrong, who may correct it, and how history is preserved.
- Zone membership events are listed under Zones.

### 3.3 Zones

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Zone Created | A new dynamic operational grouping now exists for the Venue. | A Staff Member holding Manage Zones intentionally creates it. | Venue exists; name and scope satisfy approved rules. | The Zone may group Service Locations without changing physical layout. | Zone, Venue, Capability | DEC-032, DEC-038 | High; Activity Log required | Current |
| Zone Renamed | The current operational name of a Zone has changed. | A Staff Member holding Manage Zones intentionally renames it. | Zone exists in the Venue. | The new name applies prospectively; Service Locations and history remain unchanged. | Zone, Venue, Capability | DEC-032, DEC-038 | High; old and new name must be traceable | Current |
| Service Location Reassigned to Zone | A Service Location now belongs to a different current operational Zone. | A Staff Member holding Manage Zones completes reassignment. | Zone and Service Location belong to the same Venue. | Zone membership changes; Area, identity, Customer Group, Orders, Bill, Responsible Waiter, and history do not. | Zone, Service Location, Area | DEC-032, DEC-038 | High; previous and new Zone context should be traceable | Current |
| Zone Deleted | A dynamic operational grouping has ended. | A Staff Member holding Manage Zones intentionally deletes it. | Zone exists; effects on current operations are understood. | The Zone no longer groups locations; no Service Location is deleted, moved, or renamed. | Zone, Service Location, Venue | DEC-032, DEC-038 | High; Activity Log required | Current |
| Zone Template Applied | An approved reusable plan has created the initial Zone arrangement before service. | A Master user holding Manage Zone Templates intentionally applies it. | Future capability is approved for implementation; Venue is before service; template is valid for that Venue. | Initial Zones and assignments exist; later manual reassignment remains available. | Zone Template, Zone, Service Location, Master Role, Capability | DEC-037, DEC-038 | Critical; template, actor, and resulting arrangement require history | Future approved |

#### Zone event evaluations

- **Service Location Added to Zone** and **Service Location Removed from Zone** are not separate official names in the current model. Use `Service Location Reassigned to Zone` for the accepted change of current membership.
- Whether a Service Location may belong to more than one active Zone remains unresolved. Do not invent overlapping add/remove events until that rule is approved.

### 3.4 Staff, Roles, Capabilities, and Shifts

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Staff Member Added | An individual has been recognized as an authorized Staff Member. | Authorized leadership adds the person to the Organization or Venue context. | Identity and employment authority are confirmed through approved practice. | The Staff Member may receive Roles and Capabilities. | Staff Member, Organization, Venue | DEC-014, DEC-038 | Critical; Activity Log required | Current — Command gated because account governance is not detailed |
| Staff Member Deactivated | A Staff Member has lost authority for new work while past actions remain attributed. | Authorized leadership deactivates the person. | Staff Member exists; active responsibilities are safely handed over. | New work is forbidden; history remains. | Staff Member, Role, Capability, History | DEC-010, DEC-014, DEC-038 | Critical; Activity Log required | Current — Command gated because deactivation and handover rules are not detailed |
| Role Assigned | A Staff Member has received a named business responsibility in an approved context. | Authorized leadership assigns the Role. | Staff Member and Role exist; context is valid. | Responsibility description changes; no Capability is granted automatically. | Staff Member, Role, Venue | DEC-038 | Critical; Activity Log required | Current — Command gated because Role governance is not detailed |
| Role Removed | A Staff Member’s named business responsibility has ended. | Authorized leadership removes the Role. | Staff Member currently holds the Role. | Role responsibility ends; separate Capabilities do not silently change. | Staff Member, Role, Capability | DEC-010, DEC-038 | Critical; Activity Log required | Current — Command gated because Role governance is not detailed |
| Capability Granted | A Staff Member has received explicit authority for one defined action in an approved context. | An authorized person approves the grant. | Staff Member and Capability exist; grant authority and scope are valid. | The Staff Member may attempt the protected action, subject to every business rule. | Staff Member, Capability, Role, Venue | DEC-010, DEC-014, DEC-038 | Critical; Activity Log required | Current — Command gated pending Capability governance |
| Capability Revoked | A Staff Member’s explicit authority for one defined action has ended. | An authorized person approves revocation. | The grant exists. | The Staff Member can no longer perform new actions requiring that Capability; history remains. | Staff Member, Capability, Role | DEC-010, DEC-014, DEC-038 | Critical; Activity Log required | Current — Command gated pending Capability governance |
| Shift Started | A Staff Member has begun an approved working period at a Venue. | The Staff Member or authorized leader confirms the start. | Staff Member is eligible for the Venue and working context. | The Shift becomes active. | Shift, Staff Member, Venue | None specific; supported by Domain Model | High; Shift record provides history | Current — Command gated because first-version Shift scope is unresolved |
| Shift Ended | A Staff Member’s approved working period has ended. | The Staff Member or authorized leader confirms the end. | Shift is active; unresolved responsibilities have an approved handover. | The Shift is complete; operational history remains. | Shift, Staff Member, Venue | None specific; supported by Domain Model | High; Shift record and exceptions require history | Current — Command gated because end and handover rules are unresolved |
| Shift Handover Completed | Operational responsibility has been deliberately passed between Staff Members or Shifts. | Responsible people complete and acknowledge the handover. | The handover scope and receiving responsibility are clear. | The receiving person owns the handed-over operational responsibility. | Shift, Staff Member, Responsible Service Staff, Customer Group | DEC-010; exact handover decision pending | Critical where Customer Group responsibility changes; Activity Log required | Current — Command gated because exact handover is unresolved |

Role assignment and Capability authorization are deliberately separate. One event must never imply the other.

### 3.5 Customer Group and service responsibility

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Customer Group Opened | Official service has begun for one party at one available Service Location. | The Responsible Waiter intentionally opens the group. | Venue is open; location is available and correctly identified; exactly one eligible Responsible Waiter holds Open Customer Group; all opening rules pass. | One Active Customer Group occupies the Service Location and owns its operational context. | Customer Group, Service Location, Responsible Waiter, Capability, History | DEC-011, DEC-030, DEC-031, DEC-035, DEC-038, DEC-039 | Critical; lifecycle opening and actor require Activity Log | Current |
| Responsible Waiter Assigned | One eligible Staff Member has accepted responsibility for an Active Customer Group. | Assignment is confirmed as part of opening or an approved responsibility process. | Customer Group is opening or Active; person is eligible; required authority exists. | Exactly one Responsible Waiter is accountable. | Customer Group, Responsible Service Staff, Responsible Waiter, Staff Member | DEC-031, DEC-035, DEC-038 | Critical; Activity Log required | Current |
| Responsible Waiter Changed | Responsibility for an Active Customer Group has moved to another eligible Staff Member. | An authorized handover is completed. | Customer Group is Active; new person is eligible; required Capability and handover conditions pass. | Exactly one new Responsible Waiter is accountable; previous and new responsibility remain in History. | Customer Group, Responsible Service Staff, Responsible Waiter, History | DEC-010, DEC-031, DEC-038 | Critical; Activity Log required | Current — Command gated because handover and acceptance are unresolved |
| Transfer Completed | The complete Active Customer Group has moved to another available Service Location. | An authorized Staff Member completes the transfer. | Customer Group is Active; destination is approved and available; transfer rules pass. | Old location is released; destination is occupied; Customer Group identity, Orders, optional Bill, Payments, Responsible Waiter, and History remain. | Customer Group, Transfer, Service Location, Bill, History | DEC-010, DEC-012, DEC-031, DEC-038 | Critical; Activity Log required | Current — Command gated for allowed location combinations and charging consequences |
| Transfer Rejected | A requested transfer has failed a business rule and no movement occurred. | The transfer request is evaluated and rejected. | A transfer was requested; at least one required condition failed. | Customer Group and both Service Locations remain unchanged. | Customer Group, Transfer, Service Location | DEC-012, DEC-031, DEC-038 | High; rejection reason should be traceable | Current |
| Customer Group Completed | Active service has ended after all approved financial and operational completion conditions were satisfied. | An authorized completion action succeeds. | Customer Group is Active; any Bill and all outstanding operational work satisfy approved completion rules. | Customer Group becomes Completed; location becomes available unless otherwise unavailable; ordinary activity ends; History remains. | Customer Group, Completed Customer Group, Bill, Outstanding Work, Service Location | DEC-031, DEC-033; completion decision pending | Critical; Activity Log required | Current — Command gated because exact completion conditions and authority are unresolved |

#### Customer Group event evaluations

- **Transfer Started** is not an official Domain Event in this catalogue. The Domain Model calls it optional and explicitly says it is not a completed business fact. It may be a workflow status, but it conflicts with the event rule that Domain Events record completed outcomes.
- **Customer Group Transferred** should not be introduced as a synonym. Use the accepted `Transfer Completed`.
- The Domain Model currently uses `Responsible Waiter Assigned` and `Responsible Waiter Changed`. `Responsible Service Staff` is the venue-neutral glossary concept; naming alignment requires Product Owner approval and must preserve DEC-035.
- `Customer Group Completed` is a valid business fact, but no completion Command may be finalized until the open completion decisions are resolved.

### 3.6 Menus and offerings

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Menu Activated | A reviewed Menu has become available in an approved Venue and context. | An authorized Staff Member activates it. | Menu is valid and approved for the context. | Menu Items may be selected according to availability and pricing rules. | Menu, Venue, Menu Item | DEC-009, DEC-038 | Critical where prices become effective; Activity Log required | Current — Command gated because menu governance is not detailed |
| Menu Retired | A Menu has stopped accepting new selections while past Orders remain unchanged. | An authorized Staff Member retires it. | Menu exists; effects on current service are understood. | No new selection uses the retired Menu; history remains. | Menu, Order, History | DEC-009, DEC-038 | High; Activity Log required | Current |
| Menu Item Made Available | A Menu Item has become selectable in an approved context. | Authorized menu management changes availability. | Menu Item exists with valid current configuration. | New Orders may select it. | Menu Item, Menu, Order | DEC-013, DEC-038 | High; Activity Log required when operationally sensitive | Current |
| Menu Item Made Unavailable | A Menu Item has stopped being selectable for new Orders. | Authorized menu management changes availability. | Menu Item exists. | New Orders cannot select it; past Order Items remain unchanged. | Menu Item, Menu, Order Item | DEC-009, DEC-013, DEC-038 | High; Activity Log required when operationally sensitive | Current |
| Menu Item Price Changed | A new approved selling price has taken effect prospectively. | Authorized menu management approves the price change. | Menu Item exists; price and effective context are approved. | New Order Items use the new price; old Order Items and Bill Lines remain unchanged. | Menu Item, Price, Order Item, Bill Line | DEC-009, DEC-038 | Critical; previous and new price require Activity Log | Current — Command gated because price governance is not detailed |

### 3.7 Orders and Order Rounds

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Order Submitted | One reviewed Order Round has been safely accepted for an Active Customer Group. | An authorized Staff Member submits the draft. | Venue and Customer Group are Active; items are valid and available; authority and business rules pass. | The Order is permanent; preparation and financial consequences may be created; later rounds remain separate. | Order, Order Round, Order Item, Customer Group | DEC-008, DEC-013, DEC-036, DEC-038, DEC-039 | Critical operational fact; Order record is required, separate Activity Log for exceptions | Current |
| Order Submission Rejected | A proposed Order was not accepted and created no preparation or financial effect. | Submission is evaluated and a business rule fails. | A submission was attempted. | No confirmed Order, Ticket, Bill Line, or Financial Obligation results from the rejected submission. | Draft Order, Order, Customer Group | DEC-008, DEC-036 | High; rejection reason should be traceable | Current |
| Order Item Cancelled | An authorized cancellation has removed the future fulfillment and financial effect of a submitted Order Item while preserving history. | Authorized Staff Member completes cancellation. | Submitted Order Item exists; cancellation rules, Capability, reason, and downstream conditions pass. | Original remains visible; approved cancellation effect is applied. | Order Item, Order, Bill Line, Activity Log | DEC-009, DEC-010, DEC-038 | Critical; Activity Log required | Current — Command gated because cancellation authority and effects are unresolved |
| Order Item Corrected | An authorized correction has addressed an Order Item error without rewriting the original. | Authorized Staff Member completes correction. | Submitted Order Item exists; correction rules, Capability, and reason pass. | Original and correction remain explainable; financial and preparation effects follow approved rules. | Order Item, Order, Bill Line, Activity Log | DEC-009, DEC-010, DEC-038 | Critical; Activity Log required | Current — Command gated because correction workflow is unresolved |
| Kitchen Ticket Created | A submitted Order has produced confirmed Kitchen work. | `Order Submitted` includes one or more Kitchen-destination items. | Order is safely accepted; relevant items retain Kitchen destination. | A Kitchen Ticket exists for the Kitchen portion of that Order Round. | Order, Order Item, Kitchen Ticket, Destination | DEC-008, DEC-013, DEC-036 | High; Ticket itself provides operational history | Current |
| Bar Ticket Created | A submitted Order has produced confirmed Bar work. | `Order Submitted` includes one or more Bar-destination items. | Order is safely accepted; relevant items retain Bar destination. | A Bar Ticket exists for the Bar portion of that Order Round. | Order, Order Item, Bar Ticket, Destination | DEC-008, DEC-013, DEC-036 | High; Ticket itself provides operational history | Current |

#### Order event evaluations

- **Order Item Routed** is not a separate official event. Routing is an approved consequence of Order submission and is represented by concrete `Kitchen Ticket Created` or `Bar Ticket Created` facts.
- **Preparation Ticket Created** is a useful general phrase, but the official current events are the concrete Bar and Kitchen Ticket events.
- A submitted Order is one Order Round. A later round creates another `Order Submitted`; it does not update or overwrite the earlier Order.

### 3.8 Preparation

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Kitchen Ticket Acknowledged | Kitchen Staff have recognized the Kitchen Ticket as active work. | Authorized Kitchen Staff acknowledge it. | Kitchen Ticket exists and is awaiting acknowledgement. | Kitchen responsibility for the confirmed work is visible. | Kitchen Ticket, Kitchen Staff, Order | DEC-013 | Standard; Ticket history is sufficient unless an exception occurs | Current |
| Bar Ticket Acknowledged | Bar Staff have recognized the Bar Ticket as active work. | Authorized Bar Staff acknowledge it. | Bar Ticket exists and is awaiting acknowledgement. | Bar responsibility for the confirmed work is visible. | Bar Ticket, Bar Staff, Order | DEC-013 | Standard; Ticket history is sufficient unless an exception occurs | Current |
| Kitchen Ticket Ready | Kitchen Staff have declared the approved Ticket work ready for the next service step. | Authorized Kitchen Staff confirm readiness. | Kitchen Ticket exists and the relevant work satisfies the current readiness meaning. | Kitchen work is ready for the next service step. | Kitchen Ticket, Order, Responsible Service Staff | DEC-013 | High operational history | Current — Command gated because partial readiness and exact readiness rules are unresolved |
| Bar Ticket Ready | Bar Staff have declared the approved Ticket work ready for the next service step. | Authorized Bar Staff confirm readiness. | Bar Ticket exists and the relevant work satisfies the current readiness meaning. | Bar work is ready for the next service step. | Bar Ticket, Order, Responsible Service Staff | DEC-013 | High operational history | Current — Command gated because partial readiness and exact readiness rules are unresolved |
| Kitchen Ticket Completed | The Kitchen’s responsibility for the Ticket has ended under the approved workflow. | Authorized Kitchen Staff complete the Ticket. | Kitchen Ticket exists; all approved completion conditions pass. | Kitchen no longer owns outstanding work for the Ticket; history remains. | Kitchen Ticket, Outstanding Work, Customer Group | DEC-013; completion decision pending | High; completion history required | Current — Command gated because exact completion meaning is unresolved |
| Bar Ticket Completed | The Bar’s responsibility for the Ticket has ended under the approved workflow. | Authorized Bar Staff complete the Ticket. | Bar Ticket exists; all approved completion conditions pass. | Bar no longer owns outstanding work for the Ticket; history remains. | Bar Ticket, Outstanding Work, Customer Group | DEC-013; completion decision pending | High; completion history required | Current — Command gated because exact completion meaning is unresolved |

#### Preparation event evaluations

- **Preparation Started** is not an official current event. The Domain Model uses `Kitchen Ticket Acknowledged` and `Bar Ticket Acknowledged`, which mean the department recognized active work. A separate start event requires an approved distinction.
- **Preparation Completed** is too general. Use the concrete Kitchen or Bar completion event.
- **Item Delivered** is not supported by the current Domain Model or accepted requirements.

### 3.9 Bills and Financial Obligations

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Financial Obligation Created | An approved business reason has caused the Customer Group to owe an exact amount. | An intentional approved action produces the obligation; examples are Beach Sunbed opening or an accepted Order Item. | Customer Group is Active; the charging rule and exact amount are approved. | The obligation contributes a Bill Line and creates the Bill if this is the first obligation. | Financial Obligation, Customer Group, Bill, Bill Line, Order Item, Sunbed Charge | DEC-009, DEC-033, DEC-034, DEC-036 | Critical; financial origin and amount must be permanent and explainable | Current |
| Bill Created | One Bill now exists because the Customer Group received its first approved Financial Obligation. | The first `Financial Obligation Created` occurs. | Active Customer Group has no Bill; first obligation is valid. | The Customer Group now has one running Bill. | Bill, Customer Group, Financial Obligation | DEC-009, DEC-033, DEC-034 | Critical; financial history required | Current |
| Bill Line Added | One approved financial reason has contributed an explainable amount to the Bill. | An approved Order, charge, adjustment, or correction produces the line. | Bill exists; source business fact and exact amount are valid. | Bill total and Balance reflect the new line. | Bill, Bill Line, Financial Obligation, Order | DEC-009, DEC-033, DEC-036 | Critical; source and exact amount must remain traceable | Current |
| Bill Line Reversed | An authorized financial action has offset a previous Bill Line while preserving it. | Authorized correction or reversal completes. | Original Bill Line exists; authority, reason, and reversal rules pass. | Original remains; offsetting effect changes the explainable Bill total. | Bill, Bill Line, Correction, Activity Log | DEC-009, DEC-010, DEC-038 | Critical; Activity Log required | Current — Command gated because reversal and correction rules are unresolved |
| Bill Fully Paid | Valid Payments have reduced the Bill Balance to zero. | A Payment is recorded or another separately approved financial correction produces zero Balance. | Bill exists; all considered Payments and lines are valid. | Remaining Balance is zero; no closing or Customer Group completion is implied automatically. | Bill, Balance, Payment, Customer Group | DEC-009, DEC-033 | Critical financial fact | Current |
| Bill Closed | An authorized person has confirmed that all approved Bill-closing conditions are satisfied. | Authorized Bill-closing action succeeds. | Bill exists; remaining Balance and every approved closing condition pass. | Bill stops accepting ordinary Orders, Bill Lines, and Payments; history remains. | Bill, Closed Bill, Balance, Customer Group, Capability | DEC-009, DEC-010, DEC-038; exact closing decision pending | Critical; Activity Log required | Current — Command gated because exact closing, exception, and Customer Group completion rules are unresolved |

#### Financial event evaluations

- `Financial Obligation Created` is supported by DEC-033 and DEC-034 even though the current Domain Model expresses much of its result through `Bill Created` and `Bill Line Added`. It names the business reason that makes money owed.
- **Bill Corrected** is too vague. Use the approved combination of preserved original facts, `Bill Line Reversed`, and any new explainable `Bill Line Added`.
- **Bill Reopened** is unavailable. The Domain Model explicitly forbids reopening until a future accepted exception defines authority, reason, and audit requirements.
- Bill closing does not automatically imply `Customer Group Completed`; that relationship remains unresolved.

### 3.10 Payments

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Payment Recorded | The business has confirmed receipt of an exact amount against one Bill through an approved Payment Method. | Authorized Staff Member confirms receipt after the payment action succeeds. | Bill exists and accepts Payment; amount and Payment Method are valid; Record Payments authority and rules pass. | Payment exists and reduces the Bill Balance exactly once. | Payment, Bill, Balance, Payment Method, Cashier | DEC-009, DEC-010, DEC-038 | Critical; Activity Log required | Current |
| Payment Rejected | A payment attempt was not accepted and did not reduce the Bill Balance. | The attempt fails or is refused under applicable rules. | A payment attempt occurred. | No Payment is created; Balance remains unchanged; rejection is clear. | Payment Attempt, Payment, Bill, Balance | DEC-009 | Critical where duplicate or uncertain receipt risk exists; rejection reason must be traceable | Current |
| Payment Reversed | An authorized action has reversed a previously recorded Payment while preserving history. | Authorized reversal succeeds. | Original Payment exists; reversal authority, reason, and financial rules pass. | Original remains visible; reversal changes the Bill Balance under approved rules. | Payment, Bill, Balance, Activity Log | DEC-009, DEC-010, DEC-038 | Critical; Activity Log required | Current — Command gated because reversal, refund, and post-closing rules are unresolved |

#### Payment event evaluations

- **Payment Attempted** is not an official event in the current catalogue. A Payment Attempt is a recognized concept, but its lifecycle and retention rules are not defined. A rejected attempt is represented by `Payment Rejected`.
- **Payment Confirmed** accurately describes the meaning of a Payment, but the Domain Model’s current official event name is `Payment Recorded`. Naming alignment requires an approved terminology update; do not use both names as synonyms.
- Only `Payment Recorded` reduces the Balance. A rejected or uncertain attempt does not.

### 3.11 Operational history and corrections

| Official Event Name | Business Meaning | Triggering Human or Business Action | Preconditions | Resulting Business State | Related Domain Concepts | Related Decision IDs | Audit Importance | Version |
|---|---|---|---|---|---|---|---|---|
| Activity Logged | A required Activity Log has been created for a sensitive or accountability-relevant business event. | The sensitive action succeeds or a separately approved accountability event occurs. | The event is classified as requiring an Activity Log; actor or approved origin and relevant context are known. | One protected Activity Log exists and contributes to the Audit Trail. | Activity Log, Audit Trail, Domain Event, Staff Member, History | DEC-010 | Critical; this event confirms the required accountability record itself | Current |

#### Which facts require Activity Logs

At minimum, current accepted audit principles require Activity Logs for:

- Staff Member deactivation and sensitive account changes;
- Role assignment and removal;
- Capability grant and revocation;
- Responsible Waiter changes;
- Customer Group transfers;
- Order Item cancellation and correction;
- sensitive price changes, discounts, and financial corrections;
- Bill Line reversal;
- Payment recording and reversal;
- Bill closing and any future reopening;
- other actions explicitly classified as sensitive by the Domain Model or an accepted decision.

The permanent Opening Report is required for Venue opening and department readiness. `Venue Opened for Business Date` also warrants an Activity Log because it is a Capability-protected action that changes which operations are permitted.

The following do not automatically require a separate Activity Log when their own permanent business record provides adequate ordinary history:

- normal Order submission;
- normal Bar or Kitchen Ticket acknowledgement and readiness;
- ordinary non-sensitive reference-data events.

Exceptions, corrections, unusual origins, or security-relevant activity may still require an Activity Log.

An Activity Log and a Domain Event must not be treated as interchangeable:

- `Transfer Completed` says the Customer Group moved.
- `Activity Logged` says the required accountable record of that transfer now exists.
- The Audit Trail connects those facts with the preserved Customer Group and Service Location history.

## 4. Rejected or misleading event names

| Rejected or Misleading Name | Why It Is Misleading | Correct Business Language |
|---|---|---|
| Button Clicked | Describes an interface interaction, not a completed business fact. | Use the resulting event, such as `Venue Opened for Business Date`, only after success. |
| NFC Scanned | Names a technology interaction. Identification performs no operational or financial action. | No Domain Event. Describe Service Location identification as a workflow step. |
| Service Location Identified | Identification retrieves context but does not change business state under DEC-030. | No current Domain Event. |
| API Called | Describes technical transport and says nothing about business outcome. | Use the completed or rejected business event. |
| Database Updated | Describes storage, not business meaning. | Use the relevant event, such as `Responsible Waiter Changed`. |
| Record Inserted | Describes implementation. | Use the completed business fact. |
| Sync Completed | Does not identify which business truth changed, if any. | No Domain Event unless a separate business outcome is approved. |
| Table Opened | “Table” excludes sunbeds and confuses physical location with service lifecycle. | `Customer Group Opened`. |
| Visit Created | Visit is not a core concept under DEC-031. | `Customer Group Opened`. |
| Order Saved | “Saved” could mean a draft or technical persistence. | `Order Submitted` after safe business acceptance. |
| Order Updated | Submitted Orders are preserved; later rounds are separate. | `Order Submitted` for the new Order Round, or an approved `Order Item Corrected`. |
| Order Item Routed | Routing is a consequence, not a separate accepted event. | `Kitchen Ticket Created` or `Bar Ticket Created`. |
| Preparation Ticket Created | Too general for the concrete current destinations. | `Kitchen Ticket Created` or `Bar Ticket Created`. |
| Preparation Started | No separate accepted start meaning exists. | `Kitchen Ticket Acknowledged` or `Bar Ticket Acknowledged` where that is the intended fact. |
| Preparation Completed | Does not identify which department completed responsibility. | `Kitchen Ticket Completed` or `Bar Ticket Completed`. |
| Item Delivered | Delivery lifecycle is not defined. | No current event; requires a future decision. |
| Customer Group Transferred | Creates a synonym for the accepted event. | `Transfer Completed`. |
| Customer Group Moved | Could describe physical movement before the complete transfer succeeded. | `Transfer Completed`. |
| Department Readiness Changed | A new declaration already expresses the latest completed fact. | `Department Readiness Declared`. |
| Opening Report Created | The report becomes official within Venue opening and is not an independent approved action. | `Venue Opened for Business Date`. |
| Payment Attempted | Payment Attempt retention and lifecycle are unresolved. | `Payment Rejected` for a confirmed failure, or `Payment Recorded` for confirmed receipt. |
| Payment Confirmed | Business meaning is clear, but it conflicts with the current Domain Model’s official event name. | `Payment Recorded` until an approved terminology alignment changes it. |
| Bill Corrected | Hides the original and the financial method of correction. | `Bill Line Reversed` and, where approved, `Bill Line Added`. |
| Bill Reopened | Explicitly forbidden until a future accepted exception exists. | No current event. |
| Customer Group Reopened | Reopening a Completed Customer Group is not approved. | No current event. |
| Guest Token Issued | Guest Token lifecycle is unresolved. | No event until Product Owner approval. |
| VIP Recognized | VIP identity and lifecycle are not approved BeachOS concepts. | No current event; human recognition remains operational practice. |
| Waiting List Entry Created | A digital waiting list is not approved. | No current event; waiting remains a manual operational process. |
| Staff Performance Scored | Automatic staff-performance judgment is outside the accepted product vision. | No current event. |

## 5. Event relationships

These relationships describe business order and resulting facts. They do not define technical messaging, storage, or asynchronous processing.

### Department readiness and Venue opening

`Department Readiness Declared`  
→ every mandatory Operational Department is READY  
→ `Venue Opened for Business Date`

Each mandatory department may declare more than once while conditions change. Only the current declarations at opening determine eligibility. Venue opening makes the Opening Report official as part of the same successful action; no separate `Opening Report Created` event is required.

### Service Location identification and Customer Group opening

Service Location identified through NFC or manual lookup  
→ current Service Location context retrieved  
→ eligible Responsible Waiter accepts responsibility  
→ `Responsible Waiter Assigned`  
→ `Customer Group Opened`

Service Location identification is a workflow step, not a Domain Event. It performs no operational or financial action and does not authorize the later opening.

### Beach Sunbed opening

Responsible Waiter intentionally opens the Customer Group at a Beach Sunbed  
→ `Customer Group Opened`  
→ `Financial Obligation Created`  
→ `Bill Created`  
→ `Bill Line Added`

These facts result from one intentional and atomic business action under DEC-034. If any required part fails, the complete opening outcome must fail. The sequence does not imply separate human confirmations for every resulting fact.

### Opening at another Service Location type

Responsible Waiter intentionally opens the Customer Group  
→ `Customer Group Opened`

No Bill is created merely because the group opened. Later:

first approved Financial Obligation  
→ `Financial Obligation Created`  
→ `Bill Created`  
→ `Bill Line Added`

### Order submission, preparation, and Billing

Order Round safely accepted  
→ `Order Submitted`  
→ zero or one `Kitchen Ticket Created`  
→ zero or one `Bar Ticket Created`  
→ one or more `Financial Obligation Created` and `Bill Line Added`

If no Bill exists before the first ordered Financial Obligation:

`Financial Obligation Created`  
→ `Bill Created`  
→ `Bill Line Added`

The Order, relevant Tickets, and financial facts must be mutually consistent. A rejected submission produces `Order Submission Rejected` and no confirmed preparation or financial effect.

### Preparation progression

`Kitchen Ticket Created`  
→ `Kitchen Ticket Acknowledged`  
→ `Kitchen Ticket Ready`  
→ `Kitchen Ticket Completed`

The Bar sequence is equivalent.

Exact readiness, partial completion, and completion meanings remain open. Command design for those transitions must wait for approval.

### Customer Group transfer

Authorized transfer succeeds  
→ `Transfer Completed`  
→ old Service Location becomes available  
→ destination Service Location becomes occupied

The release and occupancy changes are parts of one completed business outcome. The Customer Group remains Active and retains Orders, optional Bill, Payments, Responsible Waiter, and History.

`Transfer Rejected` means none of those changes occurred.

### Payment and Bill Balance

Confirmed value received  
→ `Payment Recorded`  
→ Bill Balance changes

If the new Balance is zero:

`Payment Recorded`  
→ `Bill Fully Paid`

Full Payment does not automatically produce `Bill Closed` or `Customer Group Completed`. Those events require additional approved conditions.

### Activity Logs and Audit Trails

Sensitive business event occurs  
→ specific Domain Event  
→ `Activity Logged`

The Audit Trail connects the specific event, its Activity Log, and the preserved business records. The Activity Log does not replace the event, and the event does not replace the Activity Log.

## 6. Open decisions and gaps

The following areas cannot receive additional official events or complete Command contracts until their business lifecycles are approved:

1. **Guest Token lifecycle:** Issuing, associating, replacing, disabling, returning, reusing, and retiring a Guest Token remain unresolved. No Guest Token events are defined.
2. **Customer Group completion:** Exact completion conditions, authority, no-Bill completion, and the relationship to Service Location release remain unresolved.
3. **Customer Group cancellation:** No exceptional cancellation state or event is approved.
4. **Customer Group reopening:** Reopening a Completed Customer Group is not approved.
5. **Bill closing:** Exact closing conditions, authority, non-zero Balance exceptions, and relationship to Customer Group completion remain unresolved.
6. **Bill reopening:** `Bill Reopened` remains forbidden until a future accepted exception defines authority, reason, consequences, and audit requirements.
7. **Bill corrections:** The allowed correction reasons, approvals, and exact combinations of reversal and replacement lines remain unresolved.
8. **Payment allocation:** Partial Payments, split Payments, overpayment, cash change, tips, and allocation rules remain unresolved.
9. **Payment reversal and refunds:** Exact authority, relationship to closed Bills, and financial consequences remain unresolved.
10. **Payment attempts:** Retention and business importance of attempted or failed external payments are not defined beyond `Payment Rejected`.
11. **Customer Group merge and unmerge:** Combining and splitting are forbidden in the initial domain. No events exist.
12. **Transfer rules:** Allowed source and destination combinations and charging effects across Physical Rows or into Beach Sunbeds remain unresolved.
13. **Preparation completion:** Exact Bar and Kitchen readiness, partial readiness, completion, delivery, and runner responsibility are unresolved.
14. **Venue closing:** No official daily Venue Closing Workflow, event, or Closing Report has been approved.
15. **Staff Shift scope:** Whether Shift belongs in the first version and the exact start, end, and handover authority remain unresolved.
16. **Responsible Service Staff handover:** Acceptance, authority, and continuity rules for changing the Responsible Waiter remain unresolved.
17. **Complaint and incident management:** No issue, complaint, escalation, resolution, or incident lifecycle is approved.
18. **Operational coaching:** Coaching is a Framework principle, not a defined transactional lifecycle. No coaching events are approved.
19. **Guest Profile and VIP lifecycle:** Customer profiles, VIP recognition, ranking, and priority are not approved.
20. **Waiting list:** A digital waiting list and its lifecycle are not approved.
21. **Service Location correction:** The business process for correcting a physical/digital state mismatch is not defined.
22. **Zone overlap:** Whether one Service Location may belong to more than one active Zone remains unresolved.
23. **Zone Templates:** `Zone Template Applied` is future approved, but template creation, approval, revision, and retirement events require later lifecycle design.
24. **Organization and Venue deactivation:** Exact preconditions, authority, and effects on unresolved live activity require approval.
25. **Menu governance:** Approval authority, effective timing, and review of Menu and price changes require detailed decisions.

These gaps must remain visible. This document does not resolve them.

## 7. Workflow engineering contracts

This appendix defines business-facing contracts only. It does not define APIs, data structures, message transport, or storage.

### 7.1 Venue Opening Workflow

#### Business Commands implied by the workflow

- **Declare Department Readiness** — the responsible person intentionally declares READY, NOT READY, or BLOCKED; NOT READY and BLOCKED include a reason.
- **Open Venue for Business Date** — the authorized Host intentionally opens after all mandatory departments are READY.

No separate `Start Venue Opening` or `Create Opening Report` Command is currently required by the approved workflow.

#### Domain Events produced after successful outcomes

- `Department Readiness Declared`
- `Venue Opened for Business Date`
- `Activity Logged` for the Capability-protected Venue-opening action

The Opening Report becomes official as part of `Venue Opened for Business Date`.

#### Domain Concepts affected

- Venue
- Business Date
- Operational Department
- Department Readiness
- Host
- Staff Member
- Capability
- Opening Report
- Activity Log

#### Important invariants enforced

- Every mandatory Operational Department has exactly one current declaration.
- The only allowed readiness values are READY, NOT READY, and BLOCKED.
- NOT READY and BLOCKED require a reason.
- Department verification belongs to its responsible person; the Host coordinates but does not replace it.
- The Host Role alone does not authorize opening.
- OPEN VENUE is forbidden until every mandatory department is READY.
- Venue opening is intentional and never occurs merely because time passed.
- Before opening, guest arrivals, new Customer Groups, and Orders are forbidden.
- Opening creates no Customer Group, Bill, Financial Obligation, Order, transfer, or Payment.
- The permanent Opening Report must reflect the readiness facts at opening and must not be silently rewritten.

#### Activity Logs required

- The authorized Host’s successful Venue-opening action.
- Any future approved sensitive correction to the official Opening Report.

Department declarations must remain permanently attributable in the Opening Report. A separate Activity Log for every ordinary declaration is not currently required by an accepted decision.

### 7.2 Guest Arrival Workflow

#### Business Commands implied by the workflow

- **Identify Service Location** — resolve the physical location through NFC or manual lookup and retrieve current context. This Command produces no official Domain Event in the current catalogue.
- **Assign Responsible Waiter** — establish the one eligible Staff Member accepting service responsibility.
- **Open Customer Group** — the Responsible Waiter intentionally begins official service.

Greeting, needs assessment, availability review, waiting, and escort are human workflow actions, not Domain Commands requiring events in the current domain.

#### Domain Events produced after successful outcomes

For every valid opening:

- `Responsible Waiter Assigned`
- `Customer Group Opened`
- `Activity Logged` for the important lifecycle opening

For a Beach Sunbed opening, the same atomic business outcome also produces:

- `Financial Obligation Created`
- `Bill Created`
- `Bill Line Added`

For another Service Location type, those financial events occur only when the first approved Financial Obligation later arises.

#### Domain Concepts affected

- Venue
- Business Date
- Host
- Service Location
- Service Location Digital Identity
- Customer Group
- Responsible Service Staff
- Responsible Waiter
- Staff Member
- Capability
- Financial Obligation
- Bill
- Bill Line
- History
- Activity Log

#### Important invariants enforced

- The Venue is officially open.
- The Service Location identity is certain and current state comes from the central system.
- NFC or manual identification performs no operational or financial action.
- Manual lookup remains available when NFC is unavailable.
- The Service Location is available and has no active Customer Group.
- At most one Active Customer Group occupies the Service Location.
- Exactly one eligible Responsible Waiter accepts responsibility.
- Only the Responsible Waiter may open the Customer Group.
- Open Customer Group Capability and all business rules are satisfied.
- The complete opening succeeds or no Customer Group is created.
- Beach Sunbed opening creates the approved immediate Financial Obligation and Bill.
- Other Service Location opening creates no Bill without a Financial Obligation.
- No false success is communicated before the outcome is safely accepted.

#### Activity Logs required

- Customer Group opening, including actor, Venue, Service Location, time, and Responsible Waiter.
- Any sensitive exception or correction affecting opening responsibility or the resulting Beach Sunbed financial fact.

Ordinary NFC or manual identification does not require an Activity Log merely because identification occurred. Security-relevant failed access or tamper concerns may require separate logging under approved security rules.

## Catalogue conclusion

The catalogue defines business meaning without selecting an event delivery mechanism. Domain Events may be represented in any responsible implementation style that preserves the approved business facts and invariants. Nothing in this document requires message brokers, queues, event sourcing, separate services, or asynchronous processing.
