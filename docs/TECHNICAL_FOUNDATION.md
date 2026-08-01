# BeachOS Technical Foundation Decisions

## Purpose

This document identifies technical decisions that still require explicit approval
before implementation. It does not select a technology, approve a Proposed
Decision, define application architecture beyond the existing repository, or
resolve a business rule.

The existing direction is:

- one mobile-first responsive web application;
- one shared codebase for supported devices and Roles;
- a modular single application;
- a central PostgreSQL database;
- server-enforced authentication, Capabilities, and business rules;
- live notices with central state remaining authoritative;
- separate development, test, and production environments.

Those directions come from Accepted Decisions. Repository scaffolding additionally
contains React, FastAPI, Docker Compose, PostgreSQL, pnpm, uv, and GitHub Actions
proposals. DEC-021 through DEC-029 still say **Proposed**. Existing files do not
silently convert those proposals into Accepted Decisions.

# Must Decide Before Development

These decisions block any responsible Sprint 1 coding.

## 1. Status of the engineering proposals

### Decision required

Accept, reject, supersede, or revise DEC-021 through DEC-029 individually:

- pnpm workspace;
- Python 3.13, uv, and pyproject-based backend;
- React 19, TypeScript, Vite, ESLint, Prettier, and Vitest;
- FastAPI, Uvicorn, Ruff, mypy, and pytest;
- Docker Compose for local PostgreSQL;
- environment-variable configuration;
- GitHub Actions;
- test placement;
- proprietary repository status.

### Why Sprint 1 needs it

The repository already references these tools, but dependency installation,
lockfiles, entry points, and test execution cannot begin while their Decision Log
status remains Proposed.

### Approval outcome needed

The Decision Log must show the approved status and any replacement Decisions before
the affected implementation is created.

## 2. Dependency authorization and lockfile baseline

### Decision required

- Which currently declared dependencies and versions are approved?
- Is dependency installation authorized?
- Which lockfiles are mandatory?
- Who reviews licensing, maintenance, and vulnerability results?
- What is the update and pinning policy for the first implementation Sprint?

### Why Sprint 1 needs it

There is no installed dependency set or lockfile. Builds and tests would otherwise
be non-reproducible.

## 3. Minimum source and module layout

### Decision required

- Where do the web and backend entry points live within the existing `apps/web` and
  `apps/api` boundaries?
- What are the initial module boundaries for identity and authorization, Venue
  Opening, operational history, and shared contracts?
- What may enter `packages/shared` and what must remain owned by an application?
- How are dependency directions enforced so the domain does not depend on delivery
  or storage details?

### Why Sprint 1 needs it

The repository intentionally contains no application entry point or source layout.
Beginning without a reviewed boundary risks coupling the first workflow to
framework or database details.

## 4. Individual identity and sign-in

### Decision required

- What sign-in method is approved for Staff Members in the first release?
- What credentials or identity proof are used?
- How are credentials created, changed, recovered, disabled, and protected?
- How are shared devices handled without shared anonymous accounts?
- What sign-in and failed-access facts require Activity Logs or security logs?

### Why Sprint 1 needs it

DEC-014 requires authentication. Venue Opening must attribute declarations and the
opening action to individual people. No authentication exists, and the accepted
business documents do not define account governance.

### Product boundary

This decision must not change the definitions of Staff Member, Role, Capability, or
Host.

## 5. Session and browser security

### Decision required

- What server-controlled session model is used?
- What are session lifetime, inactivity, renewal, revocation, and sign-out rules?
- What happens when a session expires during OPEN VENUE?
- What protections are required for browser requests and session credentials?
- Which security events are recorded, retained, and reviewable?

### Why Sprint 1 needs it

A protected action cannot rely on an unverified or stale browser identity.
Uncertain action outcomes must survive safe sign-in recovery without being
repeated.

## 6. Capability catalogue name and governance

### Decision required

- What is the official name of the Capability required to open a Venue?
- Which Capability authorizes `Declare Department Readiness`, if it is not governed
  by another approved responsibility rule?
- Who grants and revokes these Capabilities?
- What is their Organization or Venue scope?
- How are conflicts, temporary assignments, and revocation during a pending action
  handled?
- Which changes require `Activity Logged`?

### Why Sprint 1 needs it

DEC-038 requires explicit Capabilities, and DEC-039 requires one for Venue opening.
The official name and governance remain unresolved. Role cannot be substituted.

### Authority boundary

This is partly a Product Owner decision. Engineering must not invent it.

## 7. Business Date determination

### Decision required

- What local time and boundary determine the Business Date for a Venue?
- Who configures and approves that rule?
- What happens across midnight, daylight-saving changes, and an application
  restart?
- Can one Venue open more than once on one Business Date?
- How is an already-open Business Date recovered after a restart?

### Why Sprint 1 needs it

`Open Venue for Business Date` and the Opening Report cannot be made unique or
reliable without an unambiguous Business Date.

### Authority boundary

The timezone and business-day rule require Product Owner approval. Engineering may
then decide representation and enforcement.

## 8. Sprint 1 configuration ownership

### Decision required

- How are the Organization, Venue, mandatory Operational Departments, optional
  departments, responsible people, and initial Capability assignments established
  for development, testing, and the first accepted workflow?
- Is Sprint 1 using controlled fixture data only, or is an administration path
  required?
- Who approves changes to the mandatory department set for a Business Date?

### Why Sprint 1 needs it

Venue Opening needs valid source facts, but no Venue administration feature is in
Sprint 1. A deliberate fixture/configuration boundary avoids accidentally building
an unapproved administration module.

## 9. Persistence and migration baseline

### Decision required

- Confirm the PostgreSQL major-version policy proposed by the foundation.
- Select the migration and schema-change approach.
- Define how development and test databases are created, isolated, reset, and
  migrated.
- Define ownership of schema changes and rollback or forward-recovery expectations.
- Define how immutable history and correction records are protected.

### Why Sprint 1 needs it

Department declarations, Venue opening, Opening Report, and Activity Log require
durable relational state. No tables, migrations, or database integration currently
exist.

### Constraint

The implementation must enforce the approved business invariants without making
the database schema the Domain Model.

## 10. Sprint 1 Command contracts

### Decision required

For `Declare Department Readiness` and `Open Venue for Business Date`, define:

- required input facts and context;
- actor and Capability evaluation;
- authoritative validation order;
- success result;
- definitive business rejection result;
- unexpected failure result;
- safe request identity and retry behavior;
- concurrency behavior;
- externally visible error language;
- Activity Log boundary.

### Why Sprint 1 needs it

The Domain Events document defines business-facing contracts but not a transport or
implementation contract. Sprint 1 must distinguish intention, acceptance, pending,
success, rejection, and uncertainty without inventing a new Domain Event.

## 11. Atomicity, uniqueness, and concurrency

### Decision required

- How is one official opening per Venue and Business Date enforced?
- How are current declarations protected from lost updates?
- What happens when readiness changes while the Host confirms OPEN VENUE?
- How are repeated requests recognized?
- What consistency boundary creates the Venue-open fact, Opening Report, and
  Activity Log?

### Why Sprint 1 needs it

DEC-007, DEC-010, and DEC-039 require one authoritative and auditable outcome.
Interface disabling alone is insufficient.

## 12. Opening Report history and correction boundary

### Decision required

- Which declaration changes before opening remain in permanent history?
- Is every prior declaration retained or only those needed to explain delays and
  blockers?
- What is the approved retention period?
- Who may view the report?
- Are corrections allowed in Sprint 1?
- If not, how is an error escalated without rewriting the report?

### Why Sprint 1 needs it

The report must contain readiness, delays, blocking issues, reasons, and comments
and must not be silently rewritten. “Delay” and historically relevant declaration
retention need one implementable interpretation.

### Authority boundary

Product Owner and applicable legal/privacy review are required before engineering
defines storage retention.

## 13. Time handling

### Decision required

- Which time source is authoritative?
- How are Venue local time and universal time represented?
- How are opening, declarations, and Activity Log facts ordered?
- What happens when a device clock is wrong?
- What timestamp precision and display behavior are required?

### Why Sprint 1 needs it

Opening time and declaration times are permanent business facts. Device time cannot
silently become authoritative.

## 14. Interface and server contract style

### Decision required

- How does the responsive web application communicate Commands and current-state
  retrieval to the FastAPI application if DEC-024 is accepted?
- How are contract versions and compatibility handled?
- How are business rejection, validation failure, authorization denial, unknown
  outcome, and technical failure represented distinctly?
- How are generated or shared contracts governed without duplicating business
  rules?

### Why Sprint 1 needs it

No APIs currently exist. The first vertical slice should establish a deliberate
contract pattern rather than an accidental one.

## 15. Live-notice mechanism and recovery

### Decision required

- Which existing proposed live-update option will be used initially?
- Which Sprint 1 facts produce notices?
- How does the client detect missed, duplicated, delayed, or out-of-order notices?
- When does it reload authoritative state?
- What is the fallback when the live channel is unavailable but ordinary requests
  still work?

### Why Sprint 1 needs it

DEC-017 requires prompt notices while keeping the database authoritative.
Department declarations should update for the Host without creating a second source
of truth.

## 16. Freshness and degraded behavior for Sprint 1

### Decision required

- How does the client determine that opening state is current enough for OPEN
  VENUE?
- Which opening facts, if any, may be displayed from cache?
- What happens when connection is lost before confirmation, after submission, or
  during outcome retrieval?
- What manual fallback information is approved?

### Why Sprint 1 needs it

The Host must never open from stale readiness or repeat an uncertain opening.

### Constraint

Full offline operation remains excluded by DEC-018.

## 17. Test strategy and tooling approval

### Decision required

- Confirm the unit and integration tools proposed in DEC-023 and DEC-024.
- Select the browser end-to-end approach.
- Define database-test isolation and deterministic time handling.
- Define minimum coverage expectations for critical business rules.
- Define concurrency, repeated-request, session-expiry, and degraded-connection test
  methods.
- Define supported device/browser acceptance for Sprint 1.

### Why Sprint 1 needs it

The Sprint cannot be called Done without automated proof of authorization,
readiness, atomic opening, uniqueness, durable history, and recovery.

## 18. Continuous-integration baseline

### Decision required

- Confirm DEC-027.
- Define required checks for web, backend, migrations, and tests.
- Decide whether checks block merge.
- Decide how test services and secrets are provided safely.
- Define artifact and test-result retention.

### Why Sprint 1 needs it

The existing CI jobs are gated by missing lockfiles. A repeatable quality gate must
exist before feature changes merge.

## 19. Local development workflow

### Decision required

- Confirm approved runtime versions and local PostgreSQL workflow.
- Define the supported commands for setup, migration, fixture loading, running, and
  testing.
- Define how environment variables are validated.
- Define safe reset behavior for development and test data.

### Why Sprint 1 needs it

The team needs one reproducible workflow. Current scripts only inspect the
foundation and environment.

## 20. Minimum observability and error ownership

### Decision required

- Which application, security, Command, and operational signals are recorded?
- How are request identity and actor context correlated without logging secrets?
- What information is safe in developer logs?
- Who owns investigation of failed or uncertain OPEN VENUE outcomes?
- What minimum health checks are required in development and test?

### Why Sprint 1 needs it

An uncertain opening or missing Activity Log must be diagnosable without exposing
personal or sensitive information.

## 21. Secrets and non-production data

### Decision required

- How are local, test, and future deployed secrets supplied?
- Which synthetic identities and Venue fixtures are approved?
- How is accidental use of production data prevented?
- Who may access each non-production environment?

### Why Sprint 1 needs it

DEC-019 and repository security rules require environment separation and prohibit
production personal data in development and testing.

# Can Wait

These decisions do not block Sprint 1 when the Sprint maintains their current
approved exclusions.

## Host Dashboard expansion

- Exact Host-visible Customer Group fields.
- Recent Important Activity event set and retention window.
- Which rejected actions enter the Attention Queue.
- Post-opening Department Status visibility.
- Ticket pressure and oldest outstanding work.
- Final treatment of Opening succeeded as a distinct screen or transition feedback,
  provided Sprint 1 still gives clear confirmed success.

## Guest Arrival and Service Location identification

- Supported NFC devices and browsers.
- Physical marker provisioning, replacement, tamper, and support process.
- Service Location mismatch reporting and correction.
- Manual operation when current Service Location truth is unavailable.
- Guest Token lifecycle.
- Digital waiting list, which is not approved for MVP.

## Customer Group operations

- Exact Responsible Waiter assignment and acceptance.
- Handover and Shift relationship.
- Completion authority and conditions.
- No-Bill completion.
- Cancellation and reopening, which remain unavailable.
- Transfer source and destination combinations.
- Charging effects across Physical Rows or into a Beach Sunbed.
- Customer Group merge and split, which remain forbidden.

## Menu and Orders

- Menu approval and effective-time governance.
- Exact correction and cancellation reasons and authority.
- Additional preparation destinations.
- Localization and language tooling beyond the approved initial need.

## Kitchen and Bar

- Readiness, partial readiness, completion, delivery, and runner meanings.
- Delay thresholds and service measures.
- Device placement and operational notification rules.

## Billing

- Tax, discount, minimum-consumption, and non-sunbed obligation rules.
- Bill Line reversal and replacement rules.
- Bill closing and Customer Group completion relationship.
- Fiscal, receipt, accounting, and printing obligations.
- Bill reopening, which remains unavailable.

## Payments

- Partial and split Payments.
- Tips, overpayment, and cash change.
- Reversal and refund rules.
- Card-terminal and external provider integrations.
- Payment attempt retention.

## Manager Dashboard and reporting

- Approved Manager Capability catalogue.
- Report definitions and export formats.
- Cross-Venue oversight.
- Metrics, comparison, and retention.
- Staff coaching support.
- Any AI assistance, prediction, or recommendation beyond the current human-led
  principles.

## Production infrastructure

- Hosting provider and region.
- Deployment format.
- DNS and certificate operations.
- Secret manager.
- Monitoring, logging, and alerting services.
- Availability, recovery-time, recovery-point, backup-retention, and restore-test
  targets.
- Production support and incident response times.
- Venue network and backup-connectivity design.

These infrastructure decisions may wait for local Sprint 1 development, but they
must be approved before staging or production deployment.

## Legal and commercial

- Final legal owner and licensing model.
- Data-retention periods.
- Privacy notices and lawful processing.
- Greek fiscal and receipt obligations.
- Support commitments and supported-version policy.

These may not block local Venue Opening development unless they change Sprint 1
data retention or access. They block relevant pilot or production use.

## Decision readiness rule

Before coding begins, every item in **Must Decide Before Development** must have one
of these outcomes:

1. an Accepted Decision;
2. an approved existing Decision explicitly shown to cover it;
3. an approved Sprint 1 constraint that deliberately removes the need;
4. a named Product Owner decision recorded before implementation.

Silence, repository scaffolding, a Proposed Decision, or a developer preference is
not approval.
