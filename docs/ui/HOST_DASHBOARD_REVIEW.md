# BeachOS MVP — Host Dashboard Review

## 1. Outcome

`HOST_DASHBOARD_SPEC.md` defines the first implementable Host Dashboard as a focused operational workspace answering:

> What requires the Host’s attention right now?

The specification contains:

- three operating modes;
- a six-level information hierarchy;
- six required Dashboard sections;
- a narrow three-level attention model;
- accepted primary actions;
- live-update and degraded-connectivity rules;
- permission and privacy boundaries;
- 50 testable acceptance criteria;
- 12 functional screen states;
- explicit MVP exclusions;
- a traceability matrix linking Framework responsibilities, workflows, Domain Concepts, Domain Events, Decisions, and acceptance criteria.

No existing file or implementation artifact was modified.

## 2. Files reviewed

The complete repository was reviewed, with particular attention to:

- `docs/DECISIONS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/DOMAIN_EVENTS.md`;
- `docs/DOMAIN_EVENTS_REVIEW.md`;
- `docs/PROJECT_GLOSSARY.md`;
- `docs/PRODUCT_REQUIREMENTS.md`;
- `docs/MASTER_BLUEPRINT.md`;
- `docs/PRODUCT_PHILOSOPHY.md`;
- `docs/MISSION_AND_VALUES.md`;
- `framework/FRAMEWORK_PRINCIPLES.md`;
- `framework/03 Roles/HOST.md`;
- `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`;
- `framework/04 Workflows/GUEST_ARRIVAL_WORKFLOW.md`;
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`;
- repository governance, architecture, development planning, engineering foundation, application placeholders, infrastructure, scripts, tests, and GitHub configuration.

## 3. Accepted Dashboard capabilities

The MVP specification accepts:

- signed-in individual Host context;
- tablet and desktop as primary devices;
- mobile phone as a supported secondary device;
- touch-first responsive behavior;
- before-opening, Venue-open, and degraded-connectivity modes;
- Business Date and Venue-open status;
- mandatory Operational Department readiness;
- READY, NOT READY, BLOCKED, and missing declaration;
- mandatory reasons for NOT READY and BLOCKED;
- responsible person for each department declaration;
- strict all-ready eligibility for OPEN VENUE;
- separate Host responsibility and Venue-opening Capability checks;
- intentional OPEN VENUE action;
- official opening time and Opening Report outcome;
- Area and Zone filtering;
- Available, Occupied, and Unavailable Service Location counts;
- stable Service Location visible identity and type;
- NFC identification with manual fallback;
- current authorized Customer Group and Responsible Waiter context;
- factual Bar and Kitchen Ticket counts and times using accepted states;
- narrow Critical, Action required, and Awareness only attention levels;
- limited role-relevant important activity;
- connection status and last confirmed synchronization time;
- conservative read-only cached state where later approved safe;
- authoritative resynchronization after reconnection;
- clear pending, succeeded, rejected, failed, stale, and unknown states;
- no false confirmation and no unsafe repeated opening action.

## 4. Excluded future capabilities

The specification explicitly excludes:

- digital waiting lists;
- waiting priority and predictive waiting time;
- reservations;
- Guest Profiles;
- VIP intelligence;
- automated customer recognition;
- AI-generated operational decisions;
- complaint or incident management;
- general issue case management;
- employee scoring, ranking, or emotional inference;
- automatic Responsible Waiter assignment;
- Ticket delay alerts without approved thresholds;
- preparation prediction;
- weather integration;
- equipment monitoring;
- Venue Closing Workflow;
- Customer Group completion, cancellation, and reopening actions;
- Bill reopening;
- financial Dashboard content;
- full offline operation;
- Service Location mismatch case management;
- Zone Templates;
- Venue administration;
- unrestricted Activity Log or Audit Trail access.

## 5. Contradictions and tensions discovered

### Venue-opening Capability has no approved official name

DEC-039 requires the Host to hold the required Capability but does not name it. The Dashboard can enforce the requirement functionally, but Command and interface terminology need Product Owner approval.

The specification uses “required Venue-opening Capability” rather than inventing a permanent name.

### Planned opening time is referenced but not fully modeled

The Venue Opening Workflow and operational KPI discussion refer to target or planned opening time and opening delay. The Domain Model does not define where that time comes from, who approves it, or whether it may vary by Business Date.

The Dashboard shows opening delay only when an approved, confirmed planned time already exists. It does not create a scheduling capability.

### Attention Queue has limited post-opening sources

The requested Dashboard should show urgent matters, but the current domain has no general incident, complaint, equipment, weather, or Service Location-mismatch lifecycle.

The MVP queue is therefore intentionally sparse after opening. It contains only confirmed state, invariant failures, connection risk, and directly relevant rejected actions. This is consistent but may feel less comprehensive than a future operational-control Dashboard.

### Service Location mismatch is operationally recognized but not a domain lifecycle

The Host workflows describe physical/digital mismatches and manual escalation. No approved Command, Event, owner, correction process, or resolution event exists.

The MVP supports verification and blocks unsafe action. It does not create mismatch cases or automatic correction.

### Customer Group without Responsible Waiter is invalid, not an attention state

The current domain requires exactly one Responsible Waiter for every Active Customer Group.

The Dashboard must not present “unassigned” as a normal workflow state. If authoritative state violates the invariant, it is a critical integrity error.

### Ticket pressure is visible but delay is undefined

Ticket creation, acknowledgement, readiness, and completion events exist, but exact readiness, partial completion, completion, delivery, and delay thresholds remain unresolved.

The Dashboard may show factual counts and times. It may not label work late or predict completion.

### Host financial visibility is not approved

Product material emphasizes shared operational truth, but the Host’s approved responsibility does not require Bill totals, Payment amounts, or detailed financial history.

The base MVP excludes financial detail. A future expansion requires explicit responsibility, Capability, and privacy approval.

### Responsible Waiter and Responsible Service Staff remain unaligned

The current Beach Club decisions and Domain Events use Responsible Waiter. The Project Glossary defines Responsible Service Staff as the cross-Venue concept.

The Dashboard uses Responsible Waiter for the current accepted BeachOS behavior while avoiding universal claims.

### Degraded cached information needs technical classification

The product requirement calls for read-only safely cached information where appropriate. Which facts are safe to cache, for how long, and under which security conditions is not yet approved.

The functional specification uses a conservative rule: cached state is read-only, timestamped, and cannot authorize consequential action.

## 6. Unresolved Product Owner decisions

Before final application implementation, the Product Owner should decide:

1. What is the official name of the Capability required to open a Venue?
2. Who grants and revokes that Capability?
3. Where does the planned opening time originate?
4. May planned opening time vary by Business Date, season, or event?
5. Which department declarations and comments may the Host see after opening, and for how long?
6. Which role-relevant recent events belong in the Host’s permitted history window?
7. What is the approved retention window for Recent Important Activity?
8. Which rejected protected actions should reach the Host Attention Queue?
9. Is a Service Location mismatch lifecycle required for MVP, and who owns correction?
10. Which exact Bar and Kitchen Ticket states are approved for the first release?
11. What do Ticket readiness and completion mean?
12. Is the oldest outstanding Ticket time appropriate for Host operational awareness?
13. May the Host see any Bill or Payment state without seeing amounts?
14. Which Customer Group details are necessary for Host coordination?
15. Which information may be safely cached during degraded connectivity?
16. How recent must state be before a consequential action is blocked?
17. What manual fallback procedure applies when authoritative Service Location state is unavailable?
18. What exact notification retention and acknowledgment rules should apply?
19. Should `Customer Group Completed` appear in the MVP live state before its completion Command is approved?
20. Which devices and browsers must support NFC for the Host at launch?

None of these questions is resolved by the specification.

## 7. Readiness for wireframing

**Ready for wireframing: Yes, with documented constraints.**

The Dashboard has enough definition for a low-fidelity functional wireframe because:

- its primary question is clear;
- operating modes are distinct;
- information priority is explicit;
- section responsibilities are bounded;
- primary actions and prohibitions are known;
- screen states and acceptance criteria are testable;
- future capabilities are excluded.

Wireframes must:

- use placeholders rather than invent answers to open Product Owner decisions;
- omit financial detail;
- keep post-opening Attention deliberately narrow;
- avoid introducing waiting, VIP, complaint, weather, prediction, or closing behavior;
- label Command-gated Domain Events appropriately;
- preserve mobile access to critical state.

## 8. Readiness for application implementation

**Ready for application implementation: No.**

Reasons:

- the task does not authorize application development;
- the Venue-opening Capability name and governance remain unresolved;
- exact preparation states and completion meanings remain unresolved;
- Host-visible Customer Group detail requires approval;
- degraded caching and freshness rules require security and technical design;
- mismatch correction has no approved lifecycle;
- Command design remains partial in several related areas;
- no wireframe or Host usability review has been approved;
- engineering decisions DEC-021 through DEC-029 remain Proposed in the Decision Log despite later foundation approval.

The core business behavior is sufficiently defined for design, but not for production implementation.

## 9. Exact next recommended deliverable

Create a **low-fidelity Host Dashboard functional wireframe and interaction-state flow**, covering exactly:

1. Initial loading.
2. Before opening — declarations pending.
3. Before opening — blocked department.
4. Before opening — eligible to open.
5. Opening in progress.
6. Opening succeeded.
7. Venue open — normal.
8. Venue open — attention required.
9. Connection degraded.
10. Connection restored.
11. No authorized Host action.
12. Unexpected error.

The deliverable should:

- contain no application code;
- contain no visual brand exploration;
- map each state to the acceptance criteria in `HOST_DASHBOARD_SPEC.md`;
- demonstrate tablet, desktop, and essential mobile hierarchy;
- be reviewed with the Product Owner and at least one experienced Host;
- record unresolved choices without silently resolving them.

Only after that review should the team create an approved interaction specification or implementation milestone.

## 10. Stop point

The Host Dashboard product-design specification and review are complete. No existing documentation or implementation file was changed.
