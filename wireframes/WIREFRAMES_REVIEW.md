# Host Dashboard Functional Wireframes — Review

## 1. Review outcome

The Host Dashboard is ready for a **constrained low-fidelity clickable prototype**.

The prototype can demonstrate:

- opening-readiness review;
- blocking and pending declarations;
- the intentional OPEN VENUE confirmation;
- pending, successful, rejected, and uncertain opening outcomes;
- transition to live Venue operation;
- current Host Attention;
- Service Location selection;
- NFC identification with manual fallback;
- the boundary between Host handoff and Responsible Waiter action;
- degraded connection and authoritative recovery;
- authorization and unexpected-error behavior.

It is not ready to become an implementation specification. Several Product Owner
decisions and later technical designs remain deliberately unresolved.

## 2. Files created

- `wireframes/HOST_DASHBOARD_WIREFRAMES.md`
- `wireframes/HOST_DASHBOARD_USER_FLOW.md`
- `wireframes/WIREFRAMES_REVIEW.md`

No existing documentation or implementation file was changed.

## 3. Authority reviewed

The complete repository was reviewed before creating the wireframe documents. The
functional decisions were traced principally to:

- `docs/DECISIONS.md`;
- `docs/DOMAIN_MODEL.md`;
- `docs/DOMAIN_EVENTS.md`;
- `docs/PRODUCT_REQUIREMENTS.md`;
- `docs/PROJECT_GLOSSARY.md`;
- `framework/03 Roles/HOST.md`;
- `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`;
- `framework/04 Workflows/GUEST_ARRIVAL_WORKFLOW.md`;
- `framework/04 Workflows/CUSTOMER_GROUP_LIFECYCLE.md`;
- `docs/ui/HOST_DASHBOARD_SPEC.md`;
- `docs/ui/HOST_DASHBOARD_REVIEW.md`.

Repository governance, architecture, planning, Framework, engineering-foundation,
configuration, application placeholders, infrastructure, scripts, and testing
documents were also reviewed to confirm scope and prevent implementation work.

## 4. Missing decisions

The wireframes preserve the following unanswered Product Owner questions:

1. What is the official name of the Capability required to open a Venue?
2. Who may grant and revoke that Capability?
3. Where does a planned opening time come from?
4. May planned opening time vary by Business Date, season, or event?
5. Which department declarations and comments remain visible to the Host after
   opening, and for how long?
6. Which Host-relevant events belong in Recent Important Activity?
7. What is the approved retention window for that recent activity?
8. Which rejected protected actions should appear in the Host Attention Queue?
9. Which Customer Group details are necessary and permitted for Host coordination?
10. May the Host see Bill or Payment state without amounts?
11. Which exact Bar and Kitchen Ticket states belong in the first release?
12. What do Ticket readiness and completion mean operationally?
13. May the Host see the oldest outstanding Ticket time?
14. What threshold, if any, makes preparation work “delayed”?
15. Which facts may be safely cached during degraded connectivity?
16. How old may a confirmed fact become before a consequential action is blocked?
17. What manual process applies when current Service Location state cannot be
    retrieved?
18. What is the approved business process for a physical and digital Service
    Location mismatch?
19. What are the exact Responsible Waiter assignment and acceptance steps?
20. Who may change the Responsible Waiter, through which Capability, and how is the
    handover accepted?
21. Which devices and browsers must support NFC at launch?
22. What notification acknowledgment and retention rules apply?
23. Which person or function is the correct escalation destination when the Host
    lacks the required opening authority?
24. What language should distinguish a confirmed business rejection from a
    technical failure where no official rejection Domain Event exists?

The wireframe documents do not answer these questions.

## 5. UX risks

### Opening confirmation adds a thirteenth functional moment to the earlier catalogue

The approved Host Dashboard specification listed an Opening succeeded state but did
not list a separate Opening confirmation state. The present brief requires Opening
confirmation and lists 12 screens by omitting Opening succeeded.

The wireframes preserve both meanings without adding a thirteenth screen:

- Opening confirmation is a required screen.
- Opening success is explicit outcome feedback at the transition into Venue Open,
  including official opening time and Opening Report availability.

Risk: a prototype may make success feedback too brief or visually indistinct. The
designer must make the confirmed outcome perceivable without turning it into an
additional required screen.

### The post-opening Attention Queue is intentionally sparse

No complaint, incident, equipment, weather, waiting-list, or general issue
lifecycle is approved. The queue can show only confirmed accepted facts, invariant
risk, connection risk, directly relevant rejection, manual NFC fallback, and
factual preparation pressure.

Risk: stakeholders may expect a broader “operations control center” and ask the
designer to invent alerts. Those requests require new product decisions.

### The Host-to-Responsible-Waiter handoff has limited digital behavior

The operation requires a clear human introduction and acceptance, but the exact
assignment and handover Command rules remain open.

Risk: a prototype may accidentally give the Host an “Assign” or “Open Customer
Group” action. The clickable Host path must stop at introduction and confirmed
context unless a later approved design provides the waiter-side interaction.

### Empty and unavailable are easy to confuse

Valid zero Active Customer Groups or Tickets is different from failed retrieval,
unknown state, or no configured Service Locations.

Risk: a conventional dashboard layout may show all four as an empty card. Each must
have distinct functional wording.

### Degraded connectivity can create false confidence

Exactly which data can be cached is unresolved.

Risk: visually complete cached content may look current even with a timestamp. The
prototype must make uncertainty persistent and must keep consequential actions
unavailable.

### Mobile hierarchy may hide context

The Host needs critical status, fallback, location identity, and connection
freshness on a smaller screen.

Risk: collapsing sections can hide a blocker or active filter. Critical and Action
required information must remain directly reachable and cannot depend on a hidden
summary count.

### Attention language may feel punitive

Department blockers and operational pressure describe conditions, not individual
performance.

Risk: names, ranking, timing, or wording may be interpreted as blame. The prototype
must use factual language and support coordination.

## 6. Business risks

### A Host action could accidentally begin service

The most serious prototype risk is merging seating, identification, Responsible
Waiter introduction, assignment, and Customer Group opening into one apparent
action.

Required protection:

- Host seating has no business effect.
- identification has no business effect;
- only the Responsible Waiter opens the Customer Group;
- Beach Sunbed financial consequences follow that intentional waiter action, never
  Host interaction.

### A stale all-ready view could appear to authorize opening

All mandatory departments must still be READY at action acceptance. Host
responsibility and current Capability must also be confirmed.

The prototype must not imply that entering Ready to Open reserves eligibility.

### Retry could duplicate a consequential action

After OPEN VENUE submission, Retry must retrieve the result. It must never submit a
second opening intention.

### Service Location ambiguity could cause duplicate occupancy

NFC and manual lookup must resolve to the same enduring Service Location. Ambiguous
or mismatched identity cannot be silently resolved. One Service Location may have
at most one Active Customer Group.

### A normal-looking “unassigned group” would weaken a core invariant

Every Active Customer Group has exactly one Responsible Waiter. A missing
Responsible Waiter is an integrity violation, not a supported workload state.

### Financial information could leak through operational summaries

The base Host Dashboard excludes totals, Payment amounts, and detailed Bill
information. Indirect counts or alerts must not reveal financial activity without
an approved need and Capability.

### Opening success could imply broader authority

Venue opening enables guest arrivals and permits later Customer Groups and Orders
under their own rules. It does not create them and does not grant the Host authority
to perform them.

## 7. Contradictions and source tensions

### Screen-state catalogue and current brief use different opening-state breakdowns

`HOST_DASHBOARD_SPEC.md` defines:

- Opening in progress;
- Opening succeeded.

The current brief requires:

- Opening confirmation;
- Opening in progress;

and then Venue Open.

This is a screen-catalogue tension, not a business-rule contradiction. The
wireframes retain intentional confirmation and express confirmed success during the
transition to Venue Open. Product Owner approval is recommended before the final
Figma screen inventory is locked.

### “Guest Arrival” is both enabled after opening and mostly human

DEC-039 and the Venue Opening Workflow say guest arrivals become available after
opening. The Guest Arrival Workflow states that noticing, greeting, assessing,
waiting, and escorting are human steps without Domain Commands or Events.

There is no business contradiction. The phrase “Guest Arrival available” must not
be interpreted as a digital Guest Arrival record or action.

### Responsible Service Staff and Responsible Waiter remain terminologically split

The Project Glossary uses Responsible Service Staff as the venue-neutral concept.
Current Beach Club decisions, Domain Model, Domain Events, and workflows use
Responsible Waiter for the approved opening rule.

The wireframes use Responsible Waiter for current BeachOS behavior and do not
generalize it to all future Venues.

### The earlier review mentions Proposed engineering decisions after foundation approval

DEC-021 through DEC-029 remain Proposed in the Decision Log even though the
engineering foundation was later described as approved. This does not prevent
documentation-only wireframing but remains a governance inconsistency before
application implementation.

### Product naming varies by document purpose

The repository uses Emerald Management System, Emerald Hospitality Operating
System, BeachOS, and the Beach Operations Framework in different contexts. HOST.md
states that BeachOS means the supporting software and does not rename the approved
product.

The wireframes use “BeachOS Host Dashboard” because that is the vocabulary of the
approved Host materials and present brief. They do not declare a product rename.

## 8. Screens still impossible to wireframe completely

No required screen is entirely impossible to wireframe at low fidelity. The
following regions must remain annotated placeholders rather than finalized
interaction decisions:

### Ready to Open

- official Venue-opening Capability label;
- planned opening time and delay, unless an approved confirmed value already
  exists.

### Venue Open and Attention Required

- exact Host-visible Customer Group detail;
- exact preparation states;
- whether oldest outstanding Ticket time is shown;
- approved recent-activity event set and retention;
- which rejected actions create Host Attention.

### Connection Degraded

- exact safely cached fields;
- approved cache age;
- detailed manual continuity process.

### Service Location Context

- mismatch reporting and correction;
- exact Responsible Waiter assignment and acceptance interaction.

### Unauthorized Host

- exact escalation contact or destination;
- final official Capability terminology.

These gaps must appear as annotations in the prototype. They must not be converted
into realistic-looking invented behavior.

## 9. Recommendations before Figma

1. Obtain Product Owner confirmation that Opening succeeded will be transition
   feedback within Venue Open rather than a separate required screen.
2. Choose the official Venue-opening Capability name.
3. Approve the minimum Host-visible Customer Group and Responsible Waiter fields.
4. Approve the first-release Bar and Kitchen states and whether factual age belongs
   in the Host view.
5. Define the permitted Recent Important Activity set and review window.
6. Define which data, if any, is safe to display from cache and how freshness is
   expressed.
7. Define the manual operating procedure when Service Location truth cannot be
   retrieved.
8. Decide whether the first prototype ends at Responsible Waiter introduction or
   includes a separately designed waiter-side opening handoff.
9. Test the low-fidelity sequence with at least one experienced Host using
   before-opening pressure, simultaneous arrivals, NFC failure, and connection-loss
   scenarios.
10. Record any resulting business choice in `docs/DECISIONS.md` before changing the
    functional prototype.

## 10. Readiness for clickable prototyping

**Ready: Yes, with explicit annotations and no invented resolutions.**

The screen goals, hierarchy, allowed actions, disabled actions, feedback, guard
conditions, error paths, and state transitions are sufficient for a low-fidelity
clickable prototype.

The prototype is suitable for:

- validating whether the Host sees the right priority;
- checking that opening feels intentional and safe;
- checking that the Host can recover from blockers and NFC failure;
- testing the distinction between current and stale information;
- validating the handoff boundary with experienced Venue staff;
- identifying which open Product Owner decisions materially affect use.

The prototype is not suitable for:

- visual brand approval;
- final content approval;
- accessibility sign-off;
- implementation estimation;
- declaring the unresolved Command and Capability contracts complete;
- application development.

## 11. Recommended next deliverable

Create one low-fidelity clickable prototype covering the 12 requested screens and
the Service Location identification subflow.

The prototype should:

- contain no application code;
- use neutral functional labels;
- annotate every unresolved field or transition;
- include tablet, desktop, and essential mobile hierarchy;
- show Opening Confirmation, pending outcome, confirmed opening feedback, NFC
  failure, manual fallback, degraded connection, restored reconciliation,
  authorization loss, and safe Retry;
- stop the Host-owned arrival flow at Responsible Waiter introduction;
- be reviewed by the Product Owner and at least one experienced Host before any
  higher-fidelity design begins.

## 12. Stop point

The functional wireframe documents are complete. No Figma artifact, mockup, image,
visual style, application code, or new business decision was created.
