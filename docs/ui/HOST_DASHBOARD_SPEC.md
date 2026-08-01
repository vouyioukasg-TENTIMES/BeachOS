# BeachOS MVP — Host Dashboard Specification

## Status and scope

This document defines the first implementable Host Dashboard for the BeachOS MVP.

Its primary question is:

> **What requires the Host’s attention right now?**

The Dashboard is a focused operational workspace. It is not a generic reporting page, a complete Venue administration area, an unrestricted Audit Trail, or a menu of every product capability.

This specification defines functional content and behavior only. It does not define visual styling, application code, components, APIs, data structures, or implementation architecture.

Authoritative sources:

- `docs/DECISIONS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/DOMAIN_EVENTS.md`;
- `docs/PROJECT_GLOSSARY.md`;
- `docs/PRODUCT_REQUIREMENTS.md`;
- `framework/FRAMEWORK_PRINCIPLES.md`;
- `framework/03 Roles/HOST.md`;
- `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`;
- `framework/04 Workflows/GUEST_ARRIVAL_WORKFLOW.md`;
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`.

## Product boundary

The Dashboard may present confirmed information, enforce accepted business rules, and support actions already allowed by approved responsibility and Capability.

It must not:

- make human hospitality decisions;
- infer unapproved operational meaning;
- turn a Role into authority;
- allow the Host to open a Customer Group;
- make Service Location identification perform an operational or financial action;
- expose unapproved financial or personal information;
- treat an unresolved business lifecycle as implemented.

When this document says information is “shown,” it means the information is functionally available in the Dashboard. It does not prescribe a particular visual component.

# 1. Dashboard purpose

## Why the Dashboard exists

The Host coordinates the transition from operational readiness to guest service and maintains live awareness of the parts of the Venue that affect arrival, seating, responsibility, and continuity.

Without one focused operational view, the Host may need to ask several departments for readiness, rely on memory for Service Location availability, miss an unresolved opening blocker, or discover too late that the physical and digital operation no longer agree.

The Dashboard exists to reduce that uncertainty.

## Operational problems it solves

The MVP Dashboard helps the Host:

- understand whether the Venue is eligible to open;
- see which mandatory Operational Department has not declared readiness;
- understand why a department is NOT READY or BLOCKED;
- perform OPEN VENUE only when authorized and eligible;
- confirm the official opening outcome;
- understand current Service Location availability and occupancy;
- locate and identify the correct Service Location;
- understand the current Customer Group and Responsible Waiter context where authorized;
- recognize confirmed operational conditions requiring immediate follow-up;
- see current Bar and Kitchen work pressure without inventing prediction or performance judgment;
- distinguish confirmed state from stale, pending, failed, or unavailable information;
- recover operational awareness after a connection interruption.

## Action-oriented workspace

Every primary item must answer at least one of these questions:

- What needs attention?
- Why does it need attention?
- Who owns the next action?
- What can the Host do now?
- What is confirmed?
- What remains uncertain?

Information that does not help the Host act, coordinate, or understand current operational state belongs outside the primary Dashboard.

The Dashboard must not prioritize historical totals, broad reports, employee comparison, configuration, or general business analysis over live operational work.

## Trusted operational mirror

The Dashboard must reflect the central system’s latest confirmed Venue state.

It must:

- label information that is not current;
- never present a pending action as completed;
- never imply that cached information is authoritative after connectivity is lost;
- resynchronize after missed live updates;
- make mismatches and uncertainty visible rather than silently choosing a preferred version;
- preserve the distinction between physical observation and confirmed digital state.

# 2. User and device context

## Primary user

The primary user is the **Host**.

The Host:

- coordinates Venue opening;
- receives department readiness information;
- welcomes and seats guests;
- identifies Service Locations;
- coordinates handoff to the Responsible Waiter;
- maintains operational awareness;
- escalates confirmed problems to the responsible person;
- does not personally verify every department;
- does not officially open a Customer Group.

The Dashboard must use Host language and priorities rather than presenting a reduced Manager, Cashier, or Waiter interface.

## Identity and session context

- The user is one signed-in individual Staff Member.
- Shared anonymous Host access is not acceptable.
- The signed-in person’s Venue context must be clear.
- The Dashboard must distinguish the Host Role from the person’s granted Capabilities.
- A person may perform a protected action only when both the business responsibility and required Capability conditions are satisfied.
- A changed or revoked Capability must affect future actions promptly.

## Primary devices

Primary devices are:

- tablet;
- desktop computer.

These devices support the Host’s need to monitor readiness, compare Service Location states, and coordinate several operational areas.

## Secondary supported device

A mobile phone is a supported secondary device.

Mobile support must preserve:

- critical blockers;
- actions requiring the Host;
- Venue opening eligibility;
- Service Location lookup and identification;
- connection status;
- essential current operational context.

Mobile adaptation must not hide critical information merely because less space is available.

## Interaction context

The Dashboard must support:

- touch-first interaction;
- large, practical touch targets;
- one-handed use for essential mobile actions where practical;
- bright outdoor conditions;
- fast visual scanning;
- interruptions and return to context;
- rapid use during arrival pressure;
- safe repeated interaction when connection response is delayed;
- desktop pointer and keyboard use without weakening touch behavior.

This specification does not prescribe colors, typography, spacing values, or component styling.

# 3. Dashboard operating modes

The Dashboard has three operational modes determined by confirmed Venue and connection state.

## A. Before Venue opening

### Primary purpose

Operational Readiness.

### Required information

The Dashboard must provide:

- current Venue;
- current Business Date;
- whether the Venue is not yet open;
- planned opening time only if an approved, confirmed planned time exists for the current Business Date;
- opening delay derived from that confirmed planned time, where available;
- every mandatory Operational Department;
- responsible person for each department;
- current declaration: READY, NOT READY, BLOCKED, or missing;
- mandatory reason for NOT READY or BLOCKED;
- current comments relevant to opening;
- unresolved missing declarations;
- unresolved NOT READY departments;
- unresolved BLOCKED departments;
- whether the signed-in Host satisfies the Host responsibility;
- whether the signed-in Host holds the required Venue-opening Capability;
- whether every business condition for OPEN VENUE is satisfied;
- whether OPEN VENUE is unavailable, eligible, pending, succeeded, or failed.

### Opening rule

OPEN VENUE must remain unavailable until:

- every mandatory Operational Department has a current READY declaration;
- no mandatory declaration is missing;
- the signed-in Staff Member satisfies the Host responsibility;
- the signed-in Staff Member holds the required Venue-opening Capability;
- authoritative state confirms all opening rules.

The passage of planned opening time never makes the Venue eligible automatically.

### Actions

The Host may:

- review readiness;
- inspect reasons and comments;
- follow up with the responsible person through the Venue’s human communication practice;
- retry retrieval of current state;
- execute OPEN VENUE when eligible and authorized.

The Dashboard must not:

- let the Host declare READY for another department;
- remove a mandatory department;
- bypass NOT READY, BLOCKED, or missing status;
- create the Opening Report independently;
- allow guest arrivals, new Customer Groups, or Orders before successful Venue opening.

## B. Venue open — normal operation

### Primary purpose

Live operational awareness.

### Required information

The Dashboard must provide:

- confirmation that the Venue is open;
- official opening time;
- current Business Date;
- current connection freshness;
- total Service Locations in the active Venue context;
- counts of Available, Occupied, and Unavailable Service Locations;
- Service Location overview grouped or filtered by Area and current Zone;
- stable visible name or number;
- Service Location type;
- current occupancy state;
- active Customer Group context where the Host is authorized to see it;
- current Responsible Waiter context where the Host is authorized to see it;
- counts of current Bar and Kitchen Tickets using only approved Ticket states;
- oldest confirmed outstanding Ticket time as a factual indicator, without declaring it delayed;
- confirmed rejected protected actions directly relevant to the signed-in Host’s current work;
- confirmed integrity or state errors that prevent safe Host action;
- limited recent important activity relevant to Host responsibility.

### Preparation pressure boundary

The Dashboard may summarize:

- created Tickets awaiting acknowledgement;
- acknowledged Tickets;
- ready Tickets awaiting the next approved service step;
- factual submission or status times.

The Dashboard must not:

- label a Ticket “late” without an approved threshold;
- estimate preparation completion;
- predict guest waiting time;
- score Bar or Kitchen Staff;
- assume the meaning of Ticket completion beyond approved definitions;
- invent delivery state.

### Financial boundary

Financial totals, Payment amounts, Bill Lines, sales, and Cashier information are excluded from the default Host Dashboard.

The Host may receive only a minimal Bill or Payment state where:

- it is necessary for an approved Host responsibility;
- the signed-in Staff Member holds the required Capability;
- the information is permitted by the current business rule.

No such expanded financial Host responsibility is approved for the base MVP. The default MVP therefore hides financial details.

### Operational mismatch boundary

The Host may physically observe that the real Venue does not match the digital state. No approved general mismatch-reporting lifecycle currently exists.

For the MVP:

- the Service Location context must make verification possible;
- uncertain state must block unsafe Host action;
- the Host follows the approved human escalation practice;
- no general issue record, complaint record, or automatic correction is created.

## C. Degraded connectivity

### Primary purpose

Protect operational truth and prevent false action confirmation while connectivity is unreliable.

### Required information

The Dashboard must provide:

- a persistent connection-status indication;
- the time of the last confirmed authoritative synchronization;
- whether displayed information is current, reconnecting, or safely cached;
- which actions are unavailable because confirmation cannot be guaranteed;
- a clear manual operational fallback reminder.

### Cached information

Safely cached information may be used read-only where approved and clearly labeled.

Cached information must:

- show its last confirmed time;
- never appear equal to current authoritative state;
- never authorize OPEN VENUE;
- never prove that a Service Location is still available;
- never confirm a protected action;
- never overwrite newer central information after reconnection.

The exact categories of information approved for caching require later technical and security design. The MVP functional rule is conservative: uncertain state is read-only and cannot support consequential action.

### Actions

While authoritative confirmation is unavailable:

- OPEN VENUE is unavailable;
- a protected state-changing action is unavailable or remains clearly pending until its outcome is known;
- Service Location information may support manual awareness but not a claim of safe current availability;
- the Host uses the Venue’s manual fallback;
- the Host must not repeat an uncertain action merely to force a visible result.

### Reconnection

On reconnection, the Dashboard must:

1. identify that reconnection is in progress;
2. retrieve authoritative current state;
3. resolve pending action outcomes before enabling repetition;
4. replace stale cached values with confirmed state;
5. identify any material conflict requiring human follow-up;
6. record the new confirmed synchronization time;
7. return to the correct before-opening or Venue-open mode.

Full offline operation is excluded from the MVP.

# 4. Information hierarchy

The Dashboard must prioritize information in this order:

1. **Critical blockers and safety-related matters**
2. **Actions required from the Host**
3. **Venue opening or live operational status**
4. **Service Location availability and occupancy**
5. **Department or preparation pressure**
6. **Secondary metrics and history**

## Critical blockers and safety-related matters

This level contains only confirmed conditions that make normal Host action unsafe or forbidden, including:

- degraded connection preventing authoritative confirmation;
- a mandatory department BLOCKED before opening;
- an invariant violation such as an Active Customer Group without clear responsible service ownership;
- an authoritative state conflict that prevents safe Service Location use;
- a protected action with an uncertain outcome.

An Active Customer Group without exactly one Responsible Waiter is invalid under the current domain. It is not a permitted lifecycle state or ordinary queue item. If detected, it is treated as a critical integrity error requiring escalation.

The Dashboard does not create safety assessments from weather, emotion, personal data, or prediction.

## Actions required from the Host

This level includes:

- missing readiness declarations;
- NOT READY or BLOCKED departments needing human follow-up;
- OPEN VENUE when eligible and authorized;
- a rejected protected action initiated by or directly coordinated by the Host that requires a next step;
- a connection or state problem requiring manual fallback.

## Venue status

This level answers:

- Is the Venue open?
- For which Business Date?
- When did it open?
- Is current information authoritative?

## Service Location state

This level supports arrival and seating:

- Available;
- Occupied;
- Unavailable;
- Area;
- Zone;
- visible identity;
- current Customer Group and Responsible Waiter context where authorized.

## Department and preparation pressure

Before opening, department readiness is live and actionable.

After opening, opening readiness becomes historical. Current preparation pressure may use only accepted Bar and Kitchen Ticket facts. There is no general post-opening department-health lifecycle in the MVP.

## Secondary metrics and history

Only concise, role-relevant facts belong here. Historical exploration and unrestricted reporting are outside the Dashboard.

## Visibility rule

The highest-priority current item must be available without navigating away from the primary Dashboard.

Lower-priority detail may require deliberate expansion, but critical status and required Host action must never depend on hidden navigation.

# 5. Dashboard sections

## Opening Readiness Panel

### Purpose

Give the Host one trustworthy view of daily opening readiness and the only eligible path to OPEN VENUE.

### Information displayed

- Venue and Business Date.
- Official status: not open, eligible, opening pending, or open.
- Planned opening time only when already approved and confirmed.
- Derived opening delay where a planned time exists.
- Mandatory Operational Departments.
- Responsible person for each declaration.
- READY, NOT READY, BLOCKED, or missing.
- Required reason for NOT READY or BLOCKED.
- Opening comments.
- Count and identity of unresolved blockers.
- Signed-in Host responsibility status.
- Required Venue-opening Capability status.
- OPEN VENUE eligibility.

### Allowed actions

- Review all readiness declarations.
- Inspect a department’s reason and comments.
- Follow up through the human operational process.
- Retry authoritative state retrieval.
- Execute OPEN VENUE when eligible and authorized.

The Host cannot declare or change another department’s readiness from this section.

### Required Capability

- Viewing readiness requires signed-in Host operational access for the Venue.
- OPEN VENUE requires the approved Venue-opening Capability; its final official Capability name remains a Product Owner decision.
- The Host Role alone does not authorize the action.

### Empty state

If mandatory departments have not been configured or none are available for the Business Date, the Venue is not eligible to open. The section must state that opening setup is incomplete and direct the Host to the responsible Manager or Master process.

It must not treat an empty department list as “all ready.”

### Error state

If current readiness cannot be confirmed:

- OPEN VENUE remains unavailable;
- the last confirmed state is labeled with its time;
- missing authoritative information is explicit;
- the Host is directed to manual coordination and retry.

### Refresh or live-update behaviour

- Department declarations update promptly after confirmation.
- Eligibility is recalculated from authoritative state.
- A missed live update is corrected by resynchronization.
- The Panel must not infer READY from silence, elapsed time, or a previous Business Date.

### Mobile adaptation

- Current blockers, missing declarations, Capability status, and OPEN VENUE eligibility remain available first.
- Department detail may be opened one department at a time.
- The complete set and unresolved count remain clear.
- OPEN VENUE must not become easier to trigger accidentally on a smaller device.

### Related Decisions and Domain Events

- DEC-038
- DEC-039
- `Department Readiness Declared`
- `Venue Opened for Business Date`
- `Activity Logged`

## Attention Queue

### Purpose

Present the smallest current set of confirmed matters that require Host attention.

It is not a general issue-management, complaint-management, task-management, or staff-monitoring module.

### Information displayed

Allowed MVP attention items are:

- missing readiness declaration before opening;
- mandatory department NOT READY before opening;
- mandatory department BLOCKED before opening;
- degraded connection or stale authoritative state;
- OPEN VENUE eligible and awaiting the authorized Host;
- directly relevant rejected protected action requiring Host follow-up;
- uncertain outcome of a protected action;
- confirmed invariant violation preventing safe Host work.

The queue may identify the affected:

- Operational Department;
- Service Location;
- Customer Group;
- Responsible Waiter;
- protected action;
- connection state.

Each item must include:

- importance level;
- confirmed fact;
- reason it matters;
- affected operational context;
- available next action or escalation;
- time the fact was confirmed.

Excluded from the MVP queue:

- Service Location mismatches without an approved reporting source;
- Customer Group without Responsible Waiter as a normal state;
- Ticket delay without an approved threshold;
- complaints;
- VIP arrivals;
- waiting parties;
- weather;
- predicted pressure;
- staff performance.

### Allowed actions

- Open the affected operational context.
- Acknowledge awareness without concealing unresolved mandatory state.
- Follow up through approved human communication.
- Retry a safe state retrieval.
- Execute an already approved protected action only when the Host holds the Capability and all rules pass.

The queue does not create new issue records or assign work automatically.

### Required Capability

- Viewing an item depends on the Host’s operational access to the affected context.
- Any protected follow-up action requires its own Capability.
- Dismissing an informational item requires no new business authority.
- A mandatory blocker cannot be dismissed while unresolved.

### Empty state

State that no confirmed item currently requires Host attention.

The empty state must not imply:

- that every guest is satisfied;
- that no physical problem exists;
- that preparation has no delay;
- that the Venue is operating perfectly.

It means only that the approved information sources contain no current Host-attention item.

### Error state

If the queue cannot be refreshed:

- do not show “no issues”;
- label the queue unavailable or stale;
- preserve last confirmed items with their timestamp where safe;
- direct the Host to physical observation and manual coordination.

### Refresh or live-update behaviour

- Items appear, change importance, or resolve after confirmed source facts change.
- Duplicate items for the same fact and context are combined.
- An item does not disappear merely because it was viewed.
- Mandatory opening items resolve only when a new valid readiness declaration changes the condition.
- Rejected actions remain visible long enough for the Host to understand the outcome; retention duration requires later interaction design.

### Mobile adaptation

- Critical and Action required items appear before Awareness only.
- Each item retains context, reason, and next action.
- The count of unresolved higher-priority items remains visible.
- Lower-priority history does not displace current action.

### Related Decisions and Domain Events

- DEC-008
- DEC-010
- DEC-011
- DEC-038
- DEC-039
- `Department Readiness Declared`
- `Order Submission Rejected`
- `Transfer Rejected`
- `Payment Rejected` only if explicitly authorized and relevant
- `Activity Logged`

## Service Location Overview

### Purpose

Help the Host locate, verify, and coordinate current Service Locations for arrival and seating.

### Information displayed

- Stable visible name or number.
- Service Location type.
- Physical Area.
- Current operational Zone, where assigned.
- Available, Occupied, or Unavailable.
- Current Customer Group context where authorized.
- Current Responsible Waiter where authorized.
- Last confirmed state time.
- Whether the current view is authoritative or cached.
- Manual identification by visible name or number.
- NFC identification entry point on supported devices.

Financial totals, Bill Lines, Payment amounts, guest profiles, and personal details are excluded.

### Allowed actions

- Filter or group by Area.
- Filter or group by current Zone.
- Locate by visible name or number.
- Open the current Service Location context.
- Identify through NFC.
- Use manual lookup.
- Review current Customer Group and Responsible Waiter context where authorized.
- Coordinate with the Responsible Waiter through the Venue’s human practice.

Identification must not:

- open a Customer Group;
- create a Bill;
- create a charge;
- create an Order;
- perform a transfer;
- record a Payment;
- grant authority.

### Required Capability

- Viewing general Service Location operational state requires signed-in Venue access appropriate to the Host.
- Customer Group or Responsible Waiter detail requires approved operational need.
- Any protected action reached from the location context requires its own Capability.
- Identification itself grants no Capability.

### Empty state

If no Service Locations exist in the selected Area or Zone, state that the filter has no matching locations and allow the Host to clear it.

If the Venue has no configured Service Locations, identify incomplete Venue setup rather than presenting the Venue as full or unavailable.

### Error state

If state cannot be confirmed:

- do not label a location safely Available;
- show the last confirmed state and time where safe;
- block consequential action based on uncertain state;
- keep manual identification and physical escalation guidance available;
- distinguish “not found” from “temporarily unavailable.”

### Refresh or live-update behaviour

Update promptly after:

- `Service Location Made Available`;
- `Service Location Made Unavailable`;
- `Customer Group Opened`;
- `Transfer Completed`;
- `Customer Group Completed`;
- `Service Location Reassigned to Zone`;
- `Responsible Waiter Assigned`;
- `Responsible Waiter Changed`.

`Customer Group Completed` and `Responsible Waiter Changed` are Command gated; live support must not imply their Commands are approved before open decisions are resolved.

A missed notification must be corrected through authoritative resynchronization.

### Mobile adaptation

- Search or direct location lookup takes priority over broad overview.
- Area and Zone context remain available.
- Visible name, state, Customer Group presence, and Responsible Waiter remain scannable.
- NFC and manual fallback are both reachable.
- Filters must not conceal that a critical location error exists outside the current filtered subset.

### Related Decisions and Domain Events

- DEC-011
- DEC-012
- DEC-030
- DEC-031
- DEC-032
- DEC-035
- DEC-038
- `Service Location Made Available`
- `Service Location Made Unavailable`
- `Service Location Reassigned to Zone`
- `Customer Group Opened`
- `Responsible Waiter Assigned`
- `Responsible Waiter Changed`
- `Transfer Completed`
- `Transfer Rejected`
- `Customer Group Completed`

## Live Operation Summary

### Purpose

Provide a compact current summary of the Venue operation without becoming a reporting dashboard.

### Information displayed

- Venue-open confirmation.
- Business Date.
- Official opening time.
- Last confirmed synchronization time.
- Available Service Location count.
- Occupied Service Location count.
- Unavailable Service Location count.
- Active Customer Group count.
- Current Bar Ticket counts by accepted state.
- Current Kitchen Ticket counts by accepted state.
- Oldest confirmed outstanding Bar and Kitchen Ticket submission time.
- Count of current Critical and Action required attention items.

Excluded:

- sales;
- revenue;
- Payment totals;
- average staff performance;
- guest satisfaction score;
- waiting predictions;
- occupancy forecasts;
- historical comparison.

### Allowed actions

- Open the filtered Service Location Overview.
- Open the current Bar or Kitchen operational context only if the Host has approved access.
- Open the Attention Queue.
- Review official opening time and Opening Report summary.

The summary must not allow correction, deletion, financial action, or staff scoring.

### Required Capability

- General Host operational access permits non-sensitive counts.
- Detailed Customer Group or preparation context requires the relevant approved operational access.
- No financial Capability is assumed.

### Empty state

If the Venue is open but has no Active Customer Groups or Tickets, state that no current service activity is confirmed.

Zero is valid only after authoritative state is received. Before that, use loading or unavailable state.

### Error state

- Preserve last confirmed counts with timestamp where safe.
- Do not replace unavailable values with zero.
- Do not calculate pressure from incomplete data.
- Direct the Host to the relevant detailed context or manual fallback.

### Refresh or live-update behaviour

Update promptly from confirmed:

- Venue opening;
- Service Location state changes;
- Customer Group opening and completion;
- transfer completion;
- Bar and Kitchen Ticket creation and accepted status changes.

Counts must be recalculated from authoritative current state after reconnection.

### Mobile adaptation

- Venue status and attention count remain first.
- Location counts remain available as direct entry points.
- Preparation counts remain factual and compact.
- Secondary details may be opened deliberately.

### Related Decisions and Domain Events

- DEC-008
- DEC-011
- DEC-013
- DEC-031
- DEC-039
- `Venue Opened for Business Date`
- `Customer Group Opened`
- `Customer Group Completed`
- `Transfer Completed`
- `Kitchen Ticket Created`
- `Bar Ticket Created`
- `Kitchen Ticket Acknowledged`
- `Bar Ticket Acknowledged`
- `Kitchen Ticket Ready`
- `Bar Ticket Ready`

## Department Status

### Purpose

Before opening, provide actionable department readiness. After opening, preserve the distinction between historical opening readiness and current live operational facts.

### Information displayed

Before opening:

- same current declaration facts used by the Opening Readiness Panel;
- missing, READY, NOT READY, and BLOCKED;
- reasons and comments;
- responsible person.

After opening:

- department readiness at the official opening time;
- opening delays and blocking issues preserved in the Opening Report;
- clear label that these are historical opening facts;
- current confirmed Bar and Kitchen Ticket facts through the preparation summary;
- current Service Location availability facts where relevant to Beach Operations.

The MVP does not define a general post-opening Department status of healthy, degraded, blocked, or closed.

### Allowed actions

Before opening:

- review and follow up;
- open the relevant readiness context;
- execute OPEN VENUE when eligible and authorized.

After opening:

- review the opening snapshot;
- review currently confirmed operational facts already supported elsewhere;
- coordinate manually with the department.

The Host cannot:

- alter another department’s opening declaration;
- suspend or close the Venue automatically;
- create a post-opening incident from this section;
- rewrite the Opening Report.

### Required Capability

- Host operational access permits readiness review.
- OPEN VENUE requires the Venue-opening Capability.
- Historical Opening Report access is limited to the Host’s operational need.
- Sensitive correction requires separately approved authority; none is defined for MVP.

### Empty state

Before opening, no configured mandatory department is a blocking setup error, not a successful empty state.

After opening, if the Opening Report is unavailable, state that historical opening facts cannot be confirmed and escalate the integrity issue.

### Error state

- Do not infer current department condition from missing data.
- Do not change Venue-open state automatically.
- Label historical and live data separately.
- Provide last confirmed time and manual follow-up guidance.

### Refresh or live-update behaviour

- Before opening, declarations update promptly.
- At opening, the current declaration set becomes the permanent opening snapshot.
- After opening, later operational problems do not rewrite the snapshot.
- Current supported operational facts continue to update in their own domain contexts.

### Mobile adaptation

- Before opening, unresolved departments remain first.
- After opening, the historical snapshot is secondary to current attention and Service Location state.
- Reasons and comments remain readable on demand.

### Related Decisions and Domain Events

- DEC-039
- `Department Readiness Declared`
- `Venue Opened for Business Date`
- `Kitchen Ticket Created`
- `Bar Ticket Created`
- accepted Ticket status events

## Recent Important Activity

### Purpose

Provide limited, role-relevant recent context so the Host can understand important changes without becoming an unrestricted Activity Log or Audit Trail viewer.

### Information displayed

Only recent facts relevant to Host coordination:

- Venue opened for the Business Date;
- department readiness declarations during opening;
- Service Location made Available or Unavailable;
- Service Location reassigned to Zone;
- Customer Group opened;
- Responsible Waiter assigned;
- approved Responsible Waiter change;
- Transfer completed or rejected;
- important rejected action initiated by or directly affecting the Host’s work;
- role-relevant Activity Log entries.

Financial information is excluded by default.

Each item includes:

- official event name;
- time;
- affected operational context;
- actor where operationally appropriate and permitted;
- concise business result.

### Allowed actions

- Open the affected operational context.
- Review permitted detail.
- Return to current live state.

The Host cannot:

- edit history;
- delete an event;
- view unrestricted staff activity;
- search all financial history;
- use the section as an employee-monitoring tool.

### Required Capability

- Signed-in Host operational access.
- Event detail is filtered by Venue, Role responsibility, privacy, and Capability.
- Sensitive financial or staff information requires separately approved access and is absent from the base MVP.

### Empty state

State that no recent role-relevant important activity is available.

Do not imply that no business activity occurred; only that none qualifies for this limited view.

### Error state

- Current operational sections remain independent where possible.
- The section states that recent history is unavailable.
- It must not present partial history as complete.
- The error must not remove an unresolved mandatory Attention item sourced from current state.

### Refresh or live-update behaviour

- New permitted events appear promptly after confirmation.
- Ordering follows confirmed business time.
- Duplicate notifications do not create duplicate activity entries.
- Resynchronization restores missed recent events within the approved review window.
- The exact recent-history window requires later interaction design but must remain deliberately limited.

### Mobile adaptation

- Show a short recent list.
- Preserve event name, time, and affected context.
- Detailed history requires deliberate access.
- Recent activity never displaces Critical or Action required content.

### Related Decisions and Domain Events

- DEC-010
- DEC-012
- DEC-031
- DEC-032
- DEC-035
- DEC-038
- DEC-039
- `Activity Logged`
- `Venue Opened for Business Date`
- `Service Location Made Available`
- `Service Location Made Unavailable`
- `Service Location Reassigned to Zone`
- `Customer Group Opened`
- `Responsible Waiter Assigned`
- `Responsible Waiter Changed`
- `Transfer Completed`
- `Transfer Rejected`

# 6. Primary actions

The MVP Host Dashboard supports these actions:

## Review department readiness

The Host can understand every mandatory department’s current declaration, responsible person, reason, comments, and effect on opening eligibility.

## Follow up on missing or blocked readiness

The Dashboard identifies the affected department and responsible person. Follow-up occurs through the Venue’s human operational communication. No task or incident record is created.

## Execute OPEN VENUE

The action is available only when:

- all mandatory departments are READY;
- the signed-in person satisfies Host responsibility;
- the required Venue-opening Capability is present;
- authoritative state confirms eligibility.

The action is consequential and requires a clear intentional confirmation. While the outcome is pending, repetition must not produce a second opening.

Successful completion results in:

- `Venue Opened for Business Date`;
- official Opening Report;
- enabled guest arrivals, new Customer Groups, and Orders;
- live-operation Dashboard mode.

## Locate a Service Location

The Host may find a location using its stable visible name or number and may narrow current context by Area or Zone.

## Identify a Service Location

The Host may use:

- NFC as the preferred initial method;
- manual lookup as a permanent fallback.

Identification retrieves current context only.

## View current location and Customer Group context

The Host may review current occupancy and responsible service context needed for arrival, seating, and coordination.

## Coordinate with the Responsible Waiter

The Dashboard provides confirmed responsibility context. Communication, judgment, and handoff remain human.

## Initiate another protected action

The Host may initiate only a protected action that:

- is already approved for the product;
- belongs to the person’s current business responsibility;
- is authorized by an explicit Capability;
- satisfies all business rules;
- is not prohibited elsewhere in this specification.

The base MVP does not add new Host Capabilities.

## Explicitly prohibited primary actions

The Host Dashboard must not allow:

- Host-created Customer Group;
- Host-created Bill or charge;
- Order creation through Service Location identification;
- transfer through identification;
- Payment through identification;
- deletion of operational or financial history;
- forced department READY status;
- forced Venue opening;
- automatic Responsible Waiter assignment;
- Customer Group completion, cancellation, or reopening;
- Bill reopening;
- Venue closing.

# 7. Attention and notification rules

## Attention levels

### Critical

Use only when immediate Host awareness is necessary to prevent unsafe, forbidden, or untrustworthy action.

MVP examples:

- mandatory department BLOCKED before opening;
- authoritative state unavailable for a consequential action;
- protected action outcome is uncertain;
- confirmed invariant violation prevents safe Service Location or Customer Group coordination.

Critical does not mean an employee performed badly.

### Action required

Use when the Host has a clear next step.

MVP examples:

- missing mandatory readiness declaration;
- mandatory department NOT READY;
- Venue eligible and awaiting OPEN VENUE by an authorized Host;
- directly relevant rejected protected action requiring follow-up;
- manual fallback required after NFC failure.

### Awareness only

Use for current confirmed information that may affect coordination but requires no immediate action.

MVP examples:

- Venue successfully opened;
- Service Location became Unavailable;
- Zone reassignment affecting the Host’s current context;
- current factual Ticket pressure without an approved delay threshold.

## Notification requirements

Every notification must be:

- based on confirmed information;
- relevant to Host responsibility;
- actionable or explicitly informational;
- explainable in business language;
- associated with an affected operational context;
- deduplicated by business fact and context;
- time-stamped by confirmed business time;
- cleared by a new confirmed fact, not merely by being viewed.

## Dismissal

- Awareness-only information may be dismissed from the current view.
- An Action required item may be acknowledged, but acknowledgment must not imply resolution.
- A Critical item may not be dismissed if doing so would hide an unresolved mandatory condition.
- Opening blockers resolve only through valid Department Readiness declarations.
- Connection risk resolves only after authoritative resynchronization.
- An invariant violation remains visible until authoritative state is valid or the Host leaves that unsafe context.

## Noise control

- Do not repeat the same fact through several sections as separate notifications.
- Combine related opening blockers by department while preserving individual reasons.
- Do not notify the Host about normal activity that requires no Host awareness.
- Do not alert on raw elapsed time without an approved threshold.
- Do not use employee scoring, blame language, emotional inference, or behavioral judgment.
- Do not create alerts from personal, health, VIP, or financial data outside approved responsibility.

# 8. Live-update behaviour

## Facts that update promptly

The Dashboard should receive or retrieve current confirmed changes to:

- Department Readiness declarations;
- Venue opening;
- Service Location availability and occupancy;
- Customer Group opening;
- initial Responsible Waiter assignment;
- approved Responsible Waiter change;
- Zone reassignment;
- Bar Ticket creation and accepted state changes;
- Kitchen Ticket creation and accepted state changes;
- transfer completion or rejection where relevant;
- confirmed Payment or Bill state only when the Host is explicitly authorized and the information is operationally necessary.

The base MVP does not display financial detail, so financial updates must not leak through counts, notifications, or recent activity.

## Source of truth

The central system remains the authoritative source.

Live notification is a prompt that state changed; it is not a second source of truth. The Dashboard must be able to retrieve the current authoritative state independently.

## Missed updates

A missed, delayed, duplicated, or out-of-order live notification must not create permanent inconsistency.

The Dashboard must:

- deduplicate repeated facts;
- avoid applying an older fact over newer confirmed state;
- resynchronize after reconnection;
- resynchronize when state appears inconsistent;
- preserve pending action identity until outcome is known;
- never claim an action succeeded based only on a notification.

## Freshness

The Dashboard must make clear:

- current authoritative state;
- last confirmed synchronization time;
- reconnecting state;
- cached read-only state;
- unknown state.

No predetermined refresh interval is defined by this product specification. Performance targets belong to later technical design and approval.

# 9. Interaction rules

1. **Use the minimum practical number of interactions.** Common Host work must remain direct.
2. **Use large touch targets.** Essential actions must be practical on tablets and phones.
3. **Never hide critical status.** Critical and Action required conditions remain available from the primary Dashboard.
4. **Never show ambiguous success.** Pending, succeeded, rejected, and failed outcomes must be distinct.
5. **Confirm only consequential actions.** OPEN VENUE requires intentional confirmation; ordinary viewing and filtering do not.
6. **Separate advice, warning, mandatory rule, and completed fact.**
   - Advice suggests a human option.
   - Warning explains risk.
   - Mandatory rule states what is forbidden or required.
   - Completed fact states what already happened.
7. **Preserve manual NFC fallback.** A failed NFC interaction must not trap the Host.
8. **No destructive action from the main Dashboard.** No delete, irreversible correction, history rewrite, or broad deactivation belongs here.
9. **Do not rely on color alone.** Every state has a clear word or equivalent non-color indicator.
10. **Support bright sunlight and fast scanning.** Current status, context, and action meaning must remain discernible under outdoor use.
11. **Preserve context after interruption.** Returning to the Dashboard must not silently reset an unfinished review or conceal that state changed.
12. **Prevent unsafe repeated action.** A second interaction while OPEN VENUE is pending must not create duplicate opening.
13. **Keep filter effects clear.** The Host must know when an Area or Zone filter hides other Service Locations.
14. **Do not make empty look healthy.** Missing or unavailable data is not zero and is not “all clear.”
15. **Use official vocabulary.** Service Location, Customer Group, Responsible Waiter, Zone, Capability, Activity Log, and Domain Event retain their agreed meanings.

# 10. Permissions and privacy

## Role and Capability

- Host describes business responsibility.
- Host Role alone grants no protected action.
- Capability authorizes a defined action in an approved context.
- Business rules still apply after Capability is confirmed.
- The required Venue-opening Capability’s official catalogue name remains to be approved.

## Enforcement

Authorization and business rules must be enforced centrally.

The Dashboard must not rely on:

- hidden actions;
- disabled controls alone;
- client-side checks alone;
- a Role label alone;
- possession of an NFC tag;
- cached information.

## Minimum necessary information

The Host may see only information needed for:

- Venue opening;
- arrival and seating;
- Service Location awareness;
- Responsible Waiter coordination;
- relevant preparation awareness;
- safe escalation;
- limited operational continuity.

## Restricted information

The base MVP Host Dashboard excludes:

- Bill totals;
- Payment amounts;
- detailed financial history;
- payment credentials or secrets;
- personal customer profiles;
- VIP status;
- unnecessary guest identity;
- health information beyond immediate human communication needed for safe service;
- unrestricted staff records;
- Capability administration;
- employee scoring;
- unrestricted Activity Logs or Audit Trails.

## Activity Logs

Activity Logs support accountability and operational understanding.

The Dashboard:

- provides only role-relevant recent activity;
- does not expose unrestricted staff monitoring;
- does not rank or score employees;
- does not infer intent;
- does not use Activity Logs as blame indicators;
- preserves the distinction between a Domain Event and an Activity Log.

# 11. Acceptance criteria

## Opening readiness

- **AC-01:** A signed-in Host can identify the current Venue and Business Date.
- **AC-02:** Before opening, every mandatory Operational Department is present with its responsible person and current declaration.
- **AC-03:** A missing readiness declaration is clearly distinguishable from READY, NOT READY, and BLOCKED.
- **AC-04:** NOT READY and BLOCKED cannot appear as valid declarations without a reason.
- **AC-05:** Current reasons and comments are available to the Host.
- **AC-06:** OPEN VENUE remains unavailable while any mandatory department is missing, NOT READY, or BLOCKED.
- **AC-07:** OPEN VENUE remains unavailable to a Host who lacks the required Capability.
- **AC-08:** The Host Role alone does not authorize OPEN VENUE.
- **AC-09:** An eligible authorized Host can intentionally execute OPEN VENUE.
- **AC-10:** While opening is pending, the Dashboard does not show the Venue as open and prevents unsafe duplicate execution.
- **AC-11:** Successful opening produces the accepted `Venue Opened for Business Date` outcome and official Opening Report.
- **AC-12:** Failed opening leaves the Venue unopened and provides a clear, non-technical outcome.
- **AC-13:** After confirmed success, the Dashboard changes to Venue-open mode.

## Service Location and Customer Group safety

- **AC-14:** Venue-open mode provides current counts of Available, Occupied, and Unavailable Service Locations.
- **AC-15:** Each Service Location has its stable visible name or number, type, Area, Zone context, and current state where available.
- **AC-16:** An Occupied or Unavailable Service Location never appears as safely Available from the same confirmed state.
- **AC-17:** The Host can locate a Service Location manually by visible name or number.
- **AC-18:** Supported devices can begin NFC identification.
- **AC-19:** NFC failure leaves manual lookup available.
- **AC-20:** NFC and manual identification resolve to the same enduring Service Location.
- **AC-21:** Identification retrieves context but creates no Customer Group, Bill, charge, Order, transfer, or Payment.
- **AC-22:** Identification grants no Capability.
- **AC-23:** The Host Dashboard provides no action allowing the Host to open a Customer Group.
- **AC-24:** Current Customer Group and Responsible Waiter context is available only where authorized.
- **AC-25:** A detected invariant violation does not appear as a normal permitted Customer Group state.

## Attention and operational awareness

- **AC-26:** Critical, Action required, and Awareness only are distinguishable without relying on color alone.
- **AC-27:** Every Attention item identifies its confirmed fact, reason, affected context, and available next step.
- **AC-28:** Duplicate notifications for the same fact and context do not create repeated queue items.
- **AC-29:** An unresolved mandatory blocker cannot be dismissed as resolved.
- **AC-30:** Ticket pressure uses only accepted factual states and times.
- **AC-31:** No Ticket is labeled delayed without a separately approved threshold.
- **AC-32:** Recent Important Activity is limited to Host-relevant permitted events and Activity Logs.
- **AC-33:** The Dashboard does not expose unrestricted financial, personal, or staff information.

## Connectivity and truth

- **AC-34:** Connection status is continuously available when state may be degraded.
- **AC-35:** Degraded mode provides the last confirmed synchronization time.
- **AC-36:** Cached information is clearly distinguished from authoritative current state.
- **AC-37:** Consequential actions cannot be confirmed from stale cached information.
- **AC-38:** No uncertain action outcome is presented as success.
- **AC-39:** On reconnection, the Dashboard resynchronizes from central authoritative state.
- **AC-40:** Missed or duplicated live notifications do not create permanent inconsistent state.
- **AC-41:** After resynchronization, the Dashboard returns to the correct operating mode.

## MVP boundaries

- **AC-42:** No digital waiting list or predictive waiting time is exposed.
- **AC-43:** No reservation, Guest Profile, VIP intelligence, or automatic recognition is exposed.
- **AC-44:** No automatic Responsible Waiter assignment is exposed.
- **AC-45:** No complaint or incident-management module is exposed.
- **AC-46:** No employee score, ranking, blame indicator, or emotional inference is exposed.
- **AC-47:** No weather integration or automatic weather decision is exposed.
- **AC-48:** No Venue Closing Workflow or unapproved Customer Group lifecycle state is exposed.
- **AC-49:** No AI-generated operational decision is exposed.
- **AC-50:** The primary Dashboard remains focused on current Host attention rather than general reporting or administration.

# 12. Screen-state catalogue

The states below define functional content, not visual designs.

## Initial loading

### Meaning

The Dashboard is retrieving identity, Capability, Venue, Business Date, Venue-open state, and current authoritative operational context.

### Required content

- Loading state.
- Current signed-in identity when already known.
- No operational zero values.
- No OPEN VENUE or other consequential action.

### Exit

Move to the confirmed before-opening, Venue-open, degraded-connection, no-authorized-action, or error state.

## Before opening — declarations pending

### Meaning

The Venue is not open and at least one mandatory department is missing or NOT READY.

### Required content

- Business Date.
- All mandatory departments.
- Missing and NOT READY facts.
- Reasons for NOT READY.
- Responsible people.
- OPEN VENUE unavailable.
- Required Host follow-up.

### Exit

Confirmed declarations change the state to blocked, eligible, or remain pending.

## Before opening — blocked department

### Meaning

The Venue is not open and at least one mandatory department is BLOCKED.

### Required content

- Critical opening blocker.
- Affected department.
- Responsible person.
- Mandatory reason.
- Relevant comment and confirmation time.
- OPEN VENUE unavailable.
- Human escalation requirement.

### Exit

The responsible person makes a later valid readiness declaration. Viewing or acknowledging the blocker does not resolve it.

## Before opening — eligible to open

### Meaning

Every mandatory department is READY.

### Required content

- All-ready confirmation.
- Signed-in Host responsibility status.
- Venue-opening Capability status.
- OPEN VENUE available only if authorized.
- Consequence summary: official Business Date start, guest arrivals and new Customer Groups allowed, Opening Report created.

### Exit

The Host executes OPEN VENUE, a department submits a new non-READY declaration, authority changes, connection degrades, or state retrieval fails.

## Opening in progress

### Meaning

The authorized Host has intentionally requested opening and the final outcome is not yet confirmed.

### Required content

- Pending state.
- No success statement.
- No enabled duplicate OPEN VENUE action.
- Connection and authoritative confirmation status.
- Clear instruction not to repeat the action while outcome is uncertain.

### Exit

Move to Opening succeeded, return to the appropriate before-opening state after clear rejection, or enter degraded/uncertain state.

`Venue Opening Started` is not a Domain Event. This is an interaction state only.

## Opening succeeded

### Meaning

`Venue Opened for Business Date` is confirmed.

### Required content

- Confirmed success.
- Official opening time.
- Business Date.
- Host.
- Opening Report availability.
- Clear transition to live-operation mode.

### Exit

Move promptly to Venue open — normal or Venue open — attention required.

## Venue open — normal

### Meaning

The Venue is open, connection is authoritative, and no approved Critical or Action required item exists.

### Required content

- Venue-open confirmation.
- Official opening time.
- Current Service Location summary.
- Active Customer Group count.
- Factual Bar and Kitchen Ticket pressure.
- Awareness-only information.
- Empty Attention Queue wording that does not claim operational perfection.

### Exit

Confirmed attention item, connection degradation, authorization change, or unexpected error.

## Venue open — attention required

### Meaning

The Venue is open and at least one confirmed current item requires Host attention.

### Required content

- Highest-priority item first.
- Importance, reason, affected context, and next step.
- Venue status remains open.
- Current Service Location and preparation context remain available.

### Exit

The source business fact resolves, connection degrades, or another item changes priority.

A post-opening department problem does not automatically close or suspend the Venue.

## Connection degraded

### Meaning

The Dashboard cannot guarantee that displayed state is current.

### Required content

- Persistent degraded status.
- Last confirmed synchronization time.
- Cached information labeled read-only where available.
- Consequential actions unavailable.
- Manual fallback guidance.
- Reconnection status.

### Exit

Authoritative resynchronization succeeds or an unexpected error prevents recovery.

## Connection restored

### Meaning

Connectivity has returned but current state is still being reconciled.

### Required content

- Reconnection confirmation.
- Resynchronization in progress.
- Pending action outcome resolution.
- No premature claim that state is current.

### Exit

After authoritative state is confirmed, move to the correct before-opening or Venue-open state.

## No authorized Host action

### Meaning

The signed-in person can view permitted operational context but lacks the Capability for the current protected action, or does not satisfy Host responsibility.

### Required content

- Clear view-only or limited-access explanation.
- Current operational facts allowed by responsibility.
- No protected action control that appears usable.
- Direction to the appropriate authorized person.

### Exit

Authority changes and is confirmed, the user signs in under their own correct account, or the operational context changes.

## Unexpected error

### Meaning

The Dashboard cannot establish a safe known operating state due to an unexpected problem.

### Required content

- Clear statement that current state cannot be confirmed.
- No false zero or success.
- Consequential actions unavailable.
- Last confirmed time and state where safe.
- Retry option where safe.
- Manual fallback and escalation guidance.

### Exit

Successful authoritative reload, confirmed degraded mode, or sign-in recovery.

# 13. MVP exclusions

## Digital waiting list

Excluded because no waiting-list entity, lifecycle, priority rule, or privacy policy is approved. The Host follows the manual waiting process.

## Predictive waiting times

Excluded because no approved thresholds, prediction basis, or operational promise exists.

## Reservations

Excluded from first-version boundaries. Reservation, deposit, arrival, and Service Location-hold rules are not approved.

## Guest Profiles

Excluded because the initial product does not require individual customer identity and no profile lifecycle is approved.

## VIP intelligence

Excluded because VIP identity, recognition, ranking, priority, and privacy rules are not approved. Human recognition remains operational practice.

## Automated customer recognition

Excluded because it is unnecessary for the approved workflow and creates identity and privacy risks.

## AI-generated operational decisions

Excluded because the Framework requires explainable advice and human judgment, and no AI decision capability is approved.

## Complaint-management module

Excluded because complaint, incident, resolution, remedy, and escalation lifecycles are not approved.

## General issue-management module

Excluded because the Attention Queue may contain only derived current facts. It must not create a separate issue entity or lifecycle.

## Staff performance scoring

Excluded because operational information supports coaching rather than automatic judgment, ranking, or blame.

## Automatic Responsible Waiter assignment

Excluded because assignment and handover require clear human responsibility and the exact handover process remains unresolved.

## Ticket delay alerts

Excluded until the Product Owner approves delay thresholds, scope, and expected action. Raw state and time may be shown without declaring delay.

## Preparation prediction

Excluded because no approved estimate or predictive model exists.

## Weather integration

Excluded because no weather source, safety rule, or automated response has been approved.

## Equipment monitoring

Excluded because equipment and maintenance lifecycles are not part of the approved MVP domain.

## Venue Closing Workflow

Excluded because no daily Venue closing event, Command, report, or workflow has been approved.

## Customer Group completion, cancellation, or reopening action

Excluded because exact completion authority and rules are unresolved, while cancellation and reopening are not approved.

## Bill reopening

Excluded because `Bill Reopened` is explicitly unavailable until a future accepted exception exists.

## Financial dashboard

Excluded because the Host’s base responsibility does not justify financial totals, Payments, sales, or detailed Bill information.

## Full offline operation

Excluded because safe offline operation and conflict resolution require a separate approved design.

## Service Location mismatch case management

Excluded because the reporting, ownership, correction, and closure lifecycle for a mismatch is not approved. The Host uses manual escalation.

## Zone Templates

Excluded because the capability is future approved and outside the first version.

## Venue administration

Excluded because configuring departments, Service Locations, Areas, Zones, Roles, Capabilities, menus, and prices belongs outside the Host’s primary live Dashboard.

## Unrestricted Activity Log or Audit Trail

Excluded because the Host needs limited role-relevant context, not broad employee, financial, security, or administrative history.

# 14. Traceability matrix

| Dashboard behavior | Framework responsibility | Workflow step | Domain Concept | Domain Event | Decision ID | Acceptance criterion |
|---|---|---|---|---|---|---|
| Identify current Business Date and Venue state | Coordinate daily Venue opening | Venue Opening: establish opening scope | Venue, Business Date | None until opening succeeds | DEC-039 | AC-01 |
| Present every mandatory department and declaration | Review opening readiness | Venue Opening: departments declare readiness | Operational Department, Department Readiness | Department Readiness Declared | DEC-039 | AC-02–AC-05 |
| Keep OPEN VENUE unavailable while any mandatory department is unresolved | Protect opening integrity | Venue Opening: Venue becomes eligible | Venue, Department Readiness | None; rule evaluation | DEC-039 | AC-06 |
| Enforce Host responsibility and Capability for OPEN VENUE | Role does not grant authority | Venue Opening: Host opens Venue | Host, Capability, Venue | Venue Opened for Business Date | DEC-038, DEC-039 | AC-07–AC-09 |
| Distinguish pending opening from success | No false confirmation | Venue Opening: Host opens Venue | Venue, Opening Report | Venue Opened for Business Date | DEC-008, DEC-039 | AC-10–AC-12 |
| Change to live-operation mode after successful opening | Maintain operational awareness | Venue Opening completed | Venue, Business Date | Venue Opened for Business Date | DEC-039 | AC-13 |
| Summarize Available, Occupied, and Unavailable locations | Check current availability | Guest Arrival: availability check | Service Location, Customer Group | Service Location Made Available / Unavailable | DEC-011, DEC-031 | AC-14–AC-16 |
| Locate by visible name or number | Reach physical context quickly | Guest Arrival: Service Location identification | Service Location, Digital Identity | No Domain Event | DEC-030 | AC-17 |
| Support NFC with manual fallback | Physical context opens digital context | Guest Arrival: Service Location identification | Service Location Digital Identity | No Domain Event | DEC-030 | AC-18–AC-20 |
| Ensure identification has no business side effect | Preserve intentional human action | Guest Arrival: Service Location identification | Service Location, Customer Group | No Domain Event | DEC-030, DEC-035 | AC-21–AC-22 |
| Prevent Host from opening Customer Group | Preserve service responsibility | Guest Arrival: Responsible Waiter opens group | Host, Responsible Waiter, Customer Group | Customer Group Opened | DEC-035, DEC-038 | AC-23 |
| Present authorized current Customer Group and responsibility | Coordinate handoff and live operation | Guest Arrival: Responsible Waiter introduction | Customer Group, Responsible Waiter | Responsible Waiter Assigned | DEC-031, DEC-035 | AC-24–AC-25 |
| Classify attention without blame | Coaching before judging | Host monitoring and issue escalation | Attention level, Activity Log | Related confirmed event | DEC-010 | AC-26–AC-29 |
| Present factual preparation pressure only | Maintain awareness without prediction | Host operational monitoring | Bar Ticket, Kitchen Ticket | Ticket Created / Acknowledged / Ready | DEC-013 | AC-30–AC-31 |
| Limit recent activity to Host relevance | Accountability without surveillance | Host operational monitoring and handover | Activity Log, Domain Event, Audit Trail | Activity Logged | DEC-010 | AC-32–AC-33 |
| Expose degraded connection and last confirmation | Protect operational continuity | Manual operational fallback | Central source of truth | No new Domain Event | DEC-007, DEC-008 | AC-34–AC-38 |
| Resynchronize authoritative state after reconnection | Technology reduces uncertainty | Return from manual fallback | Venue operational state | Existing confirmed events | DEC-007, DEC-008 | AC-39–AC-41 |
| Exclude waiting, VIP, recognition, assignment, complaints, scoring, weather, closing, and AI decisions | Keep MVP focused and human-led | Boundaries across Host workflows | Future or undefined concepts | No current Domain Events | DEC-003, DEC-020, DEC-031, DEC-038 | AC-42–AC-50 |

## Specification conclusion

The MVP Host Dashboard is intentionally small.

Before opening, it is a readiness and opening workspace.

After opening, it is a live operational awareness workspace centered on Service Locations, Customer Groups, Responsible Waiter context, factual preparation pressure, and a narrow Attention Queue.

During degraded connectivity, it protects truth by becoming conservative, read-only where appropriate, and explicit about uncertainty.

The Dashboard succeeds when the Host can answer what requires attention now without searching through reports, exposing unnecessary information, or being invited to perform an unapproved action.
