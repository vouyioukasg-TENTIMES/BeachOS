# Sprint 1 Technical Decision Recommendations

## 1. Purpose

This document classifies every unresolved engineering decision identified in
`docs/TECHNICAL_FOUNDATION.md`.

It separates decisions into:

1. **MUST DECIDE BEFORE CODING**
2. **CAN DECIDE DURING SPRINT 1**
3. **CAN WAIT**

Recommendations are architecture proposals for Product Owner and engineering
approval. They are not Accepted Decisions. Approval must be recorded through the
repository authority model before implementation.

## 2. Classification rule

### MUST DECIDE BEFORE CODING

A choice belongs here when the first implementation would otherwise:

- use an unapproved technology;
- create an irreversible or expensive boundary;
- weaken authentication, authorization, history, or business truth;
- make tests or dependencies non-reproducible;
- require a developer to invent a Product Owner rule;
- create code that cannot be placed within an approved dependency structure.

### CAN DECIDE DURING SPRINT 1

A choice belongs here when:

- coding can begin behind an explicit port or temporary local boundary;
- the decision must be approved before the related story is Done or merged;
- it does not change the Domain or public business behavior;
- delay will not force a rewrite of the core business rules.

### CAN WAIT

A choice belongs here when Sprint 1 excludes the related capability or when it is
required only before staging, production, or a later roadmap phase.

# MUST DECIDE BEFORE CODING

## M01 — Engineering proposal status

### Decision

Accept, reject, supersede, or revise DEC-021 through DEC-029 individually.

### Why

The repository contains configuration for pnpm, Python 3.13, React, FastAPI, Docker
Compose, environment variables, GitHub Actions, testing placement, and proprietary
licensing. The Decision Log still marks all nine decisions Proposed. Creating source
or lockfiles would otherwise treat proposals as approval.

### Recommended solution

Review DEC-021 through DEC-029 as one engineering-foundation approval meeting, but
record an individual status for each Decision. Accept those still matching the
approved product direction. Supersede any that require changed versions, naming, or
scope with new Decision IDs rather than rewriting history.

The recommended initial implementation baseline is the one already prepared by the
repository:

- pnpm workspace;
- Python 3.13 with uv and pyproject;
- React with TypeScript, Vite, ESLint, Prettier, and Vitest;
- FastAPI with Uvicorn, Ruff, mypy, and pytest;
- Docker Compose for local PostgreSQL only;
- environment-variable configuration with no committed secrets;
- GitHub Actions;
- tests beside their owner plus root cross-system tests;
- proprietary repository.

### Trade-offs

- Approval preserves the existing foundation and minimizes rework.
- Revising now costs little compared with changing after source and lockfiles exist.
- Approving the group quickly risks insufficient review of versions, licensing, or
  operational ownership.

### Risks

- Framework versions may have changed since the proposal.
- Tool compatibility may fail after real dependency resolution.
- Proprietary licensing needs final legal-owner confirmation.
- Treating all nine as one binary decision would weaken historical clarity.

## M02 — Dependency authorization and lockfile baseline

### Decision

Approve declared dependencies, authorize installation, define mandatory lockfiles,
and name dependency reviewers.

### Why

No dependencies are installed and no lockfiles exist. The same repository state
could resolve differently on two machines. Sprint 1 cannot build or test
reproducibly.

### Recommended solution

After M01:

1. Review every currently declared direct dependency.
2. Remove any dependency not required by the approved Sprint 1 foundation.
3. Authorize one controlled resolution for the pnpm workspace and one for the uv
   backend environment.
4. Commit both reviewed lockfiles.
5. Record license and vulnerability results.
6. Require all later direct dependencies to include purpose, owner, license,
   maintenance, and security review.
7. Pin runtime major versions through the existing tool-version policy.

### Trade-offs

- Strict review slows the first setup but creates reproducibility and supply-chain
  visibility.
- Broad version ranges make updates easier but produce more resolution variation.
- Exact direct pins improve predictability but increase deliberate update work.

### Risks

- Initial resolution may expose incompatible declared versions.
- Transitive dependencies may introduce licensing or vulnerability concerns.
- Lockfiles can create false confidence if review and updates are neglected.

## M03 — Source namespace and Clean Architecture layout

### Decision

Approve the production source roots, package namespace, Feature Pack structure, and
dependency direction.

### Why

The current backend metadata references one placeholder source namespace, while the
target product language is BeachOS. No entry points or source folders exist.
Changing namespaces and module boundaries after migrations, contracts, and tests
exist creates avoidable churn.

### Recommended solution

Adopt `docs/engineering/APPLICATION_STRUCTURE.md` as the target structure, with:

- one `apps/web` frontend;
- one `apps/api` backend;
- backend Clean Architecture inside modular Feature Packs;
- a Hospitality Core;
- a BeachOS Industry Pack;
- Venue Opening as the first vertical Feature Pack;
- inward dependency enforcement;
- no empty future pack folders in Sprint 1.

Approve one stable backend source namespace before creating the entry point. Align
project metadata, imports, tests, and build configuration to that namespace in the
same foundation change.

### Trade-offs

- Feature-centered Clean Architecture uses more explicit boundaries than a small
  flat application.
- It improves long-term ownership and testing but can become ceremonial if every
  trivial function receives an unnecessary abstraction.
- A product-oriented namespace supports future packs but requires updating current
  placeholder metadata.

### Risks

- Over-engineering Sprint 1 with empty layers.
- A shared-domain folder becoming a dumping ground.
- Circular dependencies hidden behind convenience imports.
- Prematurely generalizing BeachOS rules into Hospitality Core.

## M04 — Individual identity and sign-in method

### Decision

Define how a Staff Member proves identity, how credentials are issued and recovered,
and how accounts are disabled.

### Why

Department declarations and Venue opening must be attributed to an individual.
DEC-014 requires authentication. No account lifecycle or sign-in implementation
exists.

### Recommended solution

For the first release, use individual first-party Staff Member accounts with a
simple credential sign-in backed by the central application. Store only a modern
one-way credential verifier, never readable credentials. Require:

- one person per account;
- no shared Host account;
- manager-controlled or otherwise approved account activation and deactivation;
- an explicit recovery process;
- rate limiting and security recording for suspicious failures;
- synthetic accounts only outside production.

Keep the Domain dependent only on authenticated Staff Member identity, not on the
credential mechanism. This preserves future replacement by an external identity
provider.

### Trade-offs

- First-party credentials are simpler for one internal Venue but create password
  lifecycle and support responsibility.
- An external identity provider could reduce credential handling but introduces
  dependency, cost, connectivity, and account-mapping complexity before it is
  required.
- Very short sign-in flows help shared devices but may weaken assurance if not
  designed carefully.

### Risks

- Shared credentials despite policy.
- Weak recovery becoming an account takeover path.
- Staff turnover leaving active accounts.
- Login friction leading to unsafe workarounds.
- Personal data retained without an approved lifecycle.

## M05 — Server-controlled session model

### Decision

Define session representation, browser protection, lifetime, inactivity, renewal,
revocation, sign-out, and pending-Command recovery.

### Why

The server must establish the current actor on every protected action. Venue
opening may remain pending across refresh, connectivity loss, or session expiry.

### Recommended solution

Use a server-controlled session referenced by a secure browser credential. The
browser stores no authoritative Capability set. Recommend:

- secure transport in every non-local environment;
- browser credential unavailable to application scripts where the chosen mechanism
  supports it;
- strict same-site request behavior appropriate to the approved deployment;
- explicit request-forgery protection;
- central revocation;
- idle and maximum lifetime;
- session rotation after sign-in and sensitive changes;
- re-authentication after expiry;
- pending opening request identity stored independently from page memory so the
  outcome can be retrieved after sign-in.

### Trade-offs

- Server-controlled sessions make revocation and shared-device safety clearer but
  require central session storage and cleanup.
- Self-contained browser credentials reduce server lookup but make immediate
  revocation and stale Capability control harder.
- Short lifetimes reduce exposure but increase interruptions during operations.

### Risks

- Session fixation or request forgery.
- One Staff Member leaving a shared tablet signed in.
- Capability changes not taking effect promptly.
- Expiry after submission causing duplicate opening.
- Sensitive session material appearing in logs.

## M06 — Sprint 1 Capability catalogue and governance

### Decision

Approve:

- the official Capability name for opening a Venue;
- the authority needed to declare department readiness;
- grant and revocation ownership;
- Organization and Venue scope;
- temporary coverage and revocation behavior;
- Activity Log requirements.

### Why

DEC-038 makes Capability separate from Role. DEC-039 explicitly requires a
Capability to open. Engineering cannot substitute a Role name or invent the
catalogue.

### Recommended solution

Product Owner approval should define two narrow action authorities:

1. authority for the responsible person to declare readiness for one Operational
   Department in one Venue context;
2. authority for an eligible Host to execute `Open Venue for Business Date` for one
   Venue.

Use action-specific, verb-led official names consistent with the existing
Capability vocabulary. Grants are scoped, centrally evaluated on every Command, and
audited when changed. Role assignment never creates either grant automatically.

### Trade-offs

- Fine-grained Capabilities improve least privilege and audit clarity.
- They increase setup and administration compared with Role-based permissions.
- Department-specific scope is safer but requires clear temporary-coverage rules.

### Risks

- Role accidentally treated as authority.
- A broad “manage Venue” Capability granting too much.
- Missing substitute responsibility blocking opening.
- Revoked Capability remaining in browser cache.
- Product vocabulary diverging between UI, contracts, and Decision Log.

## M07 — Business Date policy

### Decision

Approve the Venue-local Business Date boundary and rules for rollover, restart, and
one opening per Business Date.

### Why

Opening uniqueness, declaration scope, Opening Report identity, and official time
all depend on one unambiguous operating day.

### Recommended solution

Define Business Date as a Venue-owned policy using the Venue’s approved IANA
timezone and one configured local rollover time. The server derives it from the
authoritative clock. Recommend:

- one current Business Date for ordinary Venue operation;
- at most one successful daily opening for the Venue and Business Date;
- restart recovery from persisted authoritative state;
- no device-clock authority;
- explicit test cases around midnight and daylight-saving change;
- any exceptional multiple opening period deferred until separately approved.

The exact rollover time is a Product Owner decision per Venue, not an engineering
default.

### Trade-offs

- A configurable rollover supports late shifts but adds setup and edge cases.
- Midnight is simpler but may split a continuing hospitality operation
  incorrectly.
- One daily opening is clear but cannot represent future split operating periods
  without a new rule.

### Risks

- Wrong Business Date at midnight.
- Daylight-saving ambiguity.
- Two server instances deriving inconsistent day context.
- Device display disagreeing with server state.
- Accidental second Opening Report after restart.

## M08 — Sprint 1 configuration ownership

### Decision

Define how Sprint 1 obtains Organization, Venue, mandatory departments, responsible
people, Roles, and Capability grants without building unapproved administration.

### Why

The workflow cannot run without these facts. Sprint 1 scope does not include Venue
configuration or account administration screens.

### Recommended solution

Use reviewed, versioned, synthetic fixtures for development and automated tests,
plus one controlled non-UI bootstrap process for the approved acceptance
environment. Treat bootstrap as environment preparation, not a business feature.

Require Product Owner sign-off on:

- the first Venue;
- mandatory department list;
- responsible people;
- test Host and authorization cases;
- Business Date policy.

Do not build general administration until its own backlog and authorization rules
are approved.

### Trade-offs

- Controlled bootstrap keeps Sprint 1 focused but is not suitable for long-term
  operational administration.
- A configuration UI would be more flexible but materially expands scope and
  security exposure.
- Versioned fixtures improve repeatability but require careful separation from
  production identities.

### Risks

- Bootstrap becoming an undocumented production backdoor.
- Fixture data leaking into production.
- Manual setup differing between developers.
- Mandatory department changes without business history.

## M09 — Persistence and migration baseline

### Decision

Confirm PostgreSQL version policy, persistence approach, migration ownership, test
database lifecycle, and history protection.

### Why

Sprint 1 creates permanent declarations, Venue opening, Opening Report, and Activity
Log facts. No persistence model or migration mechanism exists.

### Recommended solution

Use the already Accepted PostgreSQL direction and the repository’s proposed local
PostgreSQL baseline after DEC-025 approval. Select one Python persistence approach
and one versioned migration tool compatible with the approved FastAPI/uv stack.

Require:

- persistence models only in Infrastructure;
- repositories implementing Application-owned ports;
- one migration history for the backend;
- forward migration as the normal production strategy;
- safe rollback or compensating recovery planned per change;
- isolated disposable database per automated integration run or worker;
- tested upgrade from the previous supported schema;
- no destructive rewrite of Activity Logs or Opening Reports.

The specific persistence and migration libraries require separate dependency
approval.

### Trade-offs

- A mature mapping library reduces repetitive storage code but can leak persistence
  concerns into Domain models.
- Direct database access offers control but increases manual translation and
  migration burden.
- Forward-only recovery protects data better than assuming every migration is
  reversibly safe, but requires operational discipline.

### Risks

- Domain entities becoming database records.
- Migrations silently changing historical facts.
- Integration tests sharing state.
- Version mismatch between local and future production PostgreSQL.
- Missing rollback or backup path.

## M10 — Sprint 1 Command and query contracts

### Decision

Approve Application-level contracts for:

- current Venue Opening context;
- `Declare Department Readiness`;
- current readiness;
- `Open Venue for Business Date`;
- opening outcome retrieval;
- Opening Report retrieval.

### Why

The Domain Events document defines business meaning but not implementation
contracts. Without clear outcomes, UI, backend, tests, and retry behavior will
diverge.

### Recommended solution

Define one use-case contract per intention or query. Every protected Command includes
authenticated actor context, Organization, Venue, Business Date, expected current
context where required, and a stable request identity.

Use a small explicit outcome vocabulary:

- completed;
- invalid input;
- unauthenticated;
- unauthorized;
- business-rule rejected;
- conflict because authoritative state changed;
- outcome unknown;
- unexpected failure.

Keep transport and persistence models outside the Application contract. Do not add
new Domain Events to represent delivery failures.

### Trade-offs

- Explicit outcomes create more design work but prevent generic error handling.
- One contract per use case is clear but may feel repetitive.
- Optimistic current-state tokens improve conflict detection but require client
  handling.

### Risks

- Technical errors presented as business rejection.
- Request identity missing, allowing duplicate opening.
- Overloading one endpoint or handler with unrelated actions.
- API delivery models leaking into Application.
- Unapproved events created for pending or rejection states.

## M11 — Atomicity, uniqueness, and concurrency

### Decision

Define the consistency boundary for readiness changes and Venue opening.

### Why

Two Hosts may attempt opening, or a department may change away from READY during
confirmation. Interface disabling cannot enforce one valid outcome.

### Recommended solution

Use a single central database transaction for `Open Venue for Business Date` that:

1. identifies the request;
2. reloads current Venue, Business Date, all mandatory declarations, actor, and
   Capability;
3. rejects if any condition changed;
4. enforces one successful opening per Venue and Business Date with database-backed
   uniqueness;
5. records Venue-open state, official Opening Report, and required Activity Log in
   one consistency boundary;
6. commits before reporting success;
7. makes repeated requests return the already known result rather than perform the
   action twice.

Use optimistic conflict detection for readiness declaration changes plus database
constraints for essential uniqueness.

### Trade-offs

- Strong transactional consistency simplifies truth but can increase contention at
  the opening moment.
- Database constraints duplicate some Domain protection but guard every write path.
- Optimistic concurrency is efficient but requires explicit conflict UX.

### Risks

- Activity Log and opening fact diverging.
- Deadlocks or retry loops.
- A second opening after restart.
- Stale all-ready state accepted.
- An idempotency record retained for too little or too long.

## M12 — Opening Report history, access, and correction boundary

### Decision

Approve which pre-opening declarations are retained, what “delays” mean, report
access, retention, and whether Sprint 1 permits correction.

### Why

The Opening Report must preserve readiness, delays, blockers, reasons, and comments
without silent rewrite. Engineering cannot decide how much operational history is
official.

### Recommended solution

For Sprint 1:

- retain every confirmed declaration made for each mandatory department during the
  opening process;
- designate the latest valid declaration at opening as the readiness snapshot;
- derive elapsed intervals as factual timing, without inventing performance
  judgment;
- preserve blockers, reasons, comments, actor, and time;
- make the report read-only;
- provide Host access only to the current report information approved in the UX;
- defer correction to a future traceable process;
- set retention only after Product Owner and legal/privacy approval.

### Trade-offs

- Full declaration history is explainable but stores more operational and Staff
  Member data.
- Snapshot-only storage is smaller but cannot explain delays and changes.
- Read-only Sprint 1 prevents unsafe correction but requires manual escalation when
  a source fact was wrong.

### Risks

- Activity history becoming employee surveillance.
- Undefined “delay” turned into a performance score.
- Personal data retained longer than necessary.
- Errors becoming permanent without an approved explanatory correction path.

## M13 — Authoritative time handling

### Decision

Choose the time source, representation, ordering, and display translation rules.

### Why

Declaration time, official opening time, Activity Logs, Business Date, and retry
history are permanent facts. Device clocks cannot be trusted.

### Recommended solution

Use server-authoritative time for business events. Persist an unambiguous universal
instant and preserve Venue timezone context needed to explain the local Business
Date. Display in the Venue’s approved local timezone.

Recommend:

- never accepting device time as event time;
- ordering by authoritative event time plus a stable sequence where equal times
  matter;
- explicit clock port in Application and Domain tests;
- one controlled fake clock in deterministic tests;
- clock-health monitoring before production.

### Trade-offs

- Universal instants support ordering and cross-Venue operation but require local
  conversion.
- Storing local time alone is easy to read but ambiguous during timezone changes.
- Stable sequence adds complexity but avoids equal-time ordering ambiguity.

### Risks

- Incorrect Venue timezone.
- daylight-saving conversion errors;
- application instances with clock drift;
- confusing displayed Business Date after rollover;
- tests depending on real time.

## M14 — API and public contract style

### Decision

Approve the web-to-server delivery style, contract ownership, error categories, and
versioning rule.

### Why

No API exists. The first endpoints will establish patterns used by every later
Feature Pack.

### Recommended solution

Use explicit HTTPS JSON contracts through the approved FastAPI delivery adapter:

- queries retrieve current or historical representations;
- Commands express named business intentions;
- every Command uses a stable request identity;
- session identity is server controlled;
- Application outcome categories map consistently to delivery responses;
- public contracts are separate from Domain and persistence models;
- one documented compatibility policy governs changes;
- live notices carry references prompting query refresh, not full alternate state.

Do not create a generic data-access API or expose table-shaped resources.

### Trade-offs

- Explicit Command contracts are clear and auditable but less generic than automatic
  CRUD.
- Shared contract generation can reduce drift but creates tooling coupling.
- Manual contract governance is simpler initially but requires disciplined tests.

### Risks

- Domain models serialized directly.
- every failure becoming one generic error.
- breaking changes without version policy;
- generated contracts becoming a shared business-logic package;
- direct database-shaped CRUD bypassing use cases.

## M15 — Test strategy and approved test tooling

### Decision

Approve unit, frontend, backend, integration, architecture, browser end-to-end,
database isolation, deterministic time, and coverage expectations.

### Why

Sprint 1 cannot be Done without proof of authorization, readiness, atomicity,
uniqueness, retry, history, and recovery. Some tools are Proposed and browser
testing is unselected.

### Recommended solution

After M01, use the repository-proposed Vitest and pytest foundations for owned unit
and Application tests. Add only:

- one approved frontend interaction-testing approach;
- one approved browser end-to-end tool selected through a short compatibility
  review;
- real PostgreSQL integration tests with isolated disposable state;
- architecture dependency tests;
- deterministic clock and request-identity support.

Set rule-based coverage expectations rather than relying only on one percentage:

- every Domain invariant has direct tests;
- every Command has success, rejection, authorization, conflict, and retry tests;
- every persistence adapter has integration tests;
- the one Host successful journey and critical failure paths have end-to-end tests.

### Trade-offs

- Real database tests are slower than mocks but validate the most important
  constraints.
- Browser tests protect integration but can be slower and more fragile.
- High numerical coverage may encourage low-value tests.
- Architecture tests add maintenance but protect the ten-year structure.

### Risks

- Test suite too slow for frequent use.
- Mocks hiding transaction failures.
- nondeterministic time or connectivity tests;
- coverage targets becoming a substitute for meaningful cases;
- browser tool chosen without device compatibility.

## M16 — Local development and synthetic data baseline

### Decision

Approve runtime versions, local PostgreSQL use, environment validation, setup/run/
test commands, safe reset behavior, and synthetic Sprint 1 fixtures.

### Why

Developers need one reproducible workflow before source changes can be reviewed.
Current scripts only inspect the foundation.

### Recommended solution

After M01 and M02:

- use the approved versions from repository metadata;
- use the proposed loopback-only local PostgreSQL service;
- provide explicit commands for dependency sync, migration, synthetic fixture load,
  web/backend start, quality checks, and tests;
- validate required environment variables at startup;
- use only `.env.example` as documentation, never real values;
- require an explicit local/test environment check before any data reset;
- make reset unavailable for production configuration;
- use the same synthetic opening fixture in local, integration, and end-to-end
  contexts where practical.

### Trade-offs

- One standard workflow reduces onboarding friction but requires maintenance across
  operating systems.
- Containers improve service consistency but add local tooling overhead.
- Automatic fixture loading is convenient but can hide setup errors if applied
  implicitly.

### Risks

- destructive reset pointed at the wrong environment;
- local setup diverging from CI;
- secrets committed in local files;
- fixture identities mistaken for real accounts;
- runtime versions drifting.

## M17 — Secrets and non-production access

### Decision

Define secret sources, environment access, synthetic data policy, and protection
against production data use.

### Why

Identity and database development require sensitive configuration. DEC-019 requires
environment separation, and repository policy forbids production personal data in
development and tests.

### Recommended solution

For local development:

- use ignored local environment files or process environment values;
- commit only safe examples;
- use generated local-only credentials;
- use synthetic Staff Members and Venue facts.

For test/staging and production, select an approved secret manager before those
environments exist. Restrict access by named individuals, rotate secrets, and keep
environment data isolated. Add automated secret scanning when the approved CI
foundation is enabled.

### Trade-offs

- Local environment files are simple but depend on developer hygiene.
- A managed secret system improves control but is premature before hosting is
  selected.
- Strict synthetic-data policy increases fixture work but reduces privacy and
  incident risk.

### Risks

- secret leakage through logs, screenshots, support messages, or AI prompts;
- shared test credentials;
- staging connected to production systems;
- copied production database used for convenience;
- unclear revocation ownership.

# CAN DECIDE DURING SPRINT 1

These decisions must be approved before the related implementation is complete or
merged. They do not need to block Domain and Application skeleton work after all
MUST items are approved.

## D01 — Live-notice mechanism and recovery

### Scope

Choose between the already proposed live-update approaches and define Sprint 1
notice identity, deduplication, reconnect, and authoritative refresh.

### Timing

Decide before the department-readiness multi-user story is Done.

### Recommended direction

Prefer the simplest one-way server-to-client notice mechanism supported by the
approved stack because Sprint 1 clients only need to learn that confirmed state
changed. Keep the mechanism behind a port so evidence can justify replacement.

## D02 — Freshness and degraded-state thresholds

### Scope

Define when readiness is current enough to open, which last-confirmed information
may remain visible, and behavior for connection loss before or after submission.

### Timing

Decide before OPEN VENUE is enabled in integrated UX.

### Recommended direction

Require an immediate authoritative validation inside the opening transaction.
Allow the browser to display last-confirmed data with its time but never use it as
opening authority. Do not promise offline action.

## D03 — Continuous-integration enforcement

### Scope

Approve required checks, merge blocking, test services, safe secrets, and result
retention.

### Timing

Decide before the first Sprint 1 implementation pull request may merge.

### Recommended direction

Enable the already proposed GitHub Actions foundation after lockfiles exist. Require
formatting, lint, type checks, architecture tests, unit tests, integration tests,
and build checks relevant to changed applications. Keep permissions read-only by
default.

## D04 — Minimum observability and error ownership

### Scope

Define technical logs, metrics, correlation, health checks, sensitive-data
redaction, and owner for failed or uncertain opening.

### Timing

Decide before integrated opening processing and error recovery are Done.

### Recommended direction

Use structured technical diagnostics with one request correlation identity across
web delivery, Application use case, persistence, and live notice. Keep Activity
Logs separate. Name an engineering owner for uncertain Sprint 1 outcomes.

## D05 — Accessibility and supported-browser verification tools

### Scope

Select the frontend accessibility testing approach and the exact supported browser
and tablet acceptance matrix.

### Timing

Decide before UX implementation is considered Done.

### Recommended direction

Use automated accessibility checks as a floor and manual tablet, keyboard, screen
reader, mobile, and outdoor-condition acceptance as required evidence.

# CAN WAIT

## W01 — Full Host Dashboard decisions

Wait until Phase 2:

- exact Host-visible Customer Group fields;
- Recent Important Activity event set;
- Recent Important Activity retention window;
- rejected actions entering the Attention Queue;
- post-opening Department Status visibility;
- Ticket pressure and oldest outstanding work;
- long-term notification acknowledgment and retention;
- final broader Dashboard cache policy.

Sprint 1 includes only opening-related information.

## W02 — Opening-success presentation beyond Sprint 1

The Product Owner should confirm whether Opening Successful remains a distinct
screen or transition acknowledgement before final UX implementation. It does not
change the architecture or Domain outcome and may wait until the Sprint 1
interaction is refined, provided success remains unmistakable and authoritative.

## W03 — Service Location and NFC

Wait until Guest Arrival:

- supported NFC devices and browsers;
- physical marker provisioning and replacement;
- tag tamper and support process;
- physical/digital mismatch workflow;
- manual operation when Service Location truth is unavailable;
- Service Location cache policy;
- Guest Token lifecycle.

## W04 — Waiting, profiles, and reservations

Wait unless separately approved:

- digital waiting list;
- waiting-time prediction;
- Guest Profiles;
- VIP recognition;
- reservations;
- automated guest recognition.

These are not Sprint 1 architecture needs.

## W05 — Customer Group responsibility and lifecycle

Wait until Customer Groups:

- Responsible Waiter assignment and acceptance;
- responsibility handover;
- Shift relationship;
- completion authority and conditions;
- completion without Bill;
- cancellation;
- reopening;
- transfer combinations;
- Physical Row transfer charging;
- merge and split.

Unavailable states remain unavailable; delay does not grant permission.

## W06 — Menu and Order governance

Wait until Waiter Operations:

- Menu approval authority and effective timing;
- Menu and price change governance;
- Order Item correction;
- Order Item cancellation;
- additional preparation destinations;
- order-specific localization needs.

## W07 — Kitchen and Bar operational meaning

Wait until preparation phases:

- acknowledgement meaning;
- partial readiness;
- readiness and completion;
- delivery;
- runner responsibility;
- delay thresholds;
- preparation measures;
- preparation device placement and notifications.

## W08 — Billing decisions

Wait until Billing:

- currency and tax implementation details;
- discounts;
- minimum consumption and other obligations;
- Physical Row charging details not needed by an earlier approved Beach Sunbed
  opening fixture;
- Bill Line reversals and replacements;
- correction reasons and approvals;
- Bill closing;
- relationship to Customer Group completion;
- fiscal, receipt, accounting, export, and printing requirements;
- Bill reopening, which remains unavailable.

## W09 — Payment decisions

Wait until Payments:

- Payment Methods;
- partial and split Payments;
- tips;
- overpayment;
- cash change;
- Payment allocation;
- Payment attempt retention;
- reversals;
- refunds;
- card-terminal integration;
- receipt/fiscal integration;
- post-closing exceptions.

## W10 — Manager Dashboard and reporting

Wait until Manager Dashboard:

- Manager Capability catalogue;
- current operational measures;
- report definitions;
- export formats;
- cross-Venue oversight;
- Activity Log and Audit Trail access;
- reporting retention;
- coaching support;
- operational comparison.

## W11 — AI and predictive capabilities

Wait for separate Product Owner and AI governance:

- predictions;
- recommendations;
- automated operational decisions;
- anomaly detection;
- staff performance interpretation.

Human decision authority remains unchanged.

## W12 — Future Industry Packs

Wait until the approved Framework roadmap reaches them:

- RestaurantOS Domain policies and features;
- HotelOS Domain policies and features;
- ResortOS or Events packs;
- cross-pack configuration;
- shared-core promotion rules based on repeated evidence.

The architecture reserves boundaries but Sprint 1 creates no empty future pack.

## W13 — Future plugin governance and implementation

Wait until a real approved plugin need exists:

- plugin categories;
- manifest format;
- installation authority;
- data scopes;
- extension Capabilities;
- registry;
- isolation runtime;
- health;
- compatibility;
- upgrades;
- suspension and removal;
- marketplace or third-party distribution.

Sprint 1 creates no plugin runtime or plugin contract package.

## W14 — Production hosting and deployment

May wait for local Sprint 1 coding but must be decided before staging or production:

- hosting provider;
- region;
- deployment format;
- networking;
- DNS;
- TLS certificate operation;
- deployed secret manager;
- production process topology;
- deployment approval;
- rollback;
- environment ownership and access.

## W15 — Production reliability

Must be approved before pilot or production:

- service availability target;
- recovery-time objective;
- recovery-point objective;
- backup frequency and retention;
- encrypted backup location;
- restore-test schedule;
- production monitoring and alerting services;
- support ownership;
- incident response times;
- supported-version policy.

## W16 — Venue connectivity

Must be validated before pilot:

- Wi-Fi coverage;
- internet capacity;
- backup connectivity;
- supported-device behavior at the beach, pool, bar, kitchen, and cashier;
- operational fallback.

Full offline operation remains excluded unless separately approved.

## W17 — Legal, privacy, fiscal, and commercial

Must be resolved before the affected production use:

- final legal owner and licensing model;
- privacy responsibilities and notices;
- Staff Member and Activity Log retention;
- Opening Report retention;
- Greek fiscal and receipt obligations;
- tax and accounting obligations;
- security-reporting contact;
- conduct-reporting contact;
- production support commitments.

## W18 — Advanced technical infrastructure

Wait for demonstrated need:

- microservices;
- a message queue;
- additional datastore;
- distributed cache;
- local Venue server;
- full offline synchronization;
- native applications;
- separate Role applications;
- generalized workflow engine;
- event-sourcing architecture.

No existing requirement justifies them for Sprint 1.

# 6. Complete traceability to TECHNICAL_FOUNDATION.md

| Original unresolved area | Classification here |
|---|---|
| 1. Engineering proposal status | M01 |
| 2. Dependency authorization and lockfiles | M02 |
| 3. Minimum source and module layout | M03 |
| 4. Individual identity and sign-in | M04 |
| 5. Session and browser security | M05 |
| 6. Capability catalogue and governance | M06 |
| 7. Business Date determination | M07 |
| 8. Sprint 1 configuration ownership | M08 |
| 9. Persistence and migration baseline | M09 |
| 10. Sprint 1 Command contracts | M10 |
| 11. Atomicity, uniqueness, concurrency | M11 |
| 12. Opening Report history and correction | M12 |
| 13. Time handling | M13 |
| 14. Interface and server contract style | M14 |
| 15. Live notices and recovery | D01 |
| 16. Freshness and degraded behavior | D02 |
| 17. Test strategy and tooling | M15 and D05 |
| 18. Continuous integration | D03 |
| 19. Local development workflow | M16 |
| 20. Observability and error ownership | D04 |
| 21. Secrets and non-production data | M17 |
| Host Dashboard expansion | W01 and W02 |
| Guest Arrival and Service Location identification | W03 and W04 |
| Customer Group operations | W05 |
| Menu and Orders | W06 |
| Kitchen and Bar | W07 |
| Billing | W08 |
| Payments | W09 |
| Manager Dashboard and reporting | W10 |
| Production infrastructure | W14 through W16 |
| Legal and commercial | W17 |
| Long-term platform and plugin choices identified by the approved architecture | W11 through W13 and W18 |

# 7. Recommended approval sequence

The Product Owner and technical owner should review in this order:

1. M01 — engineering proposal status.
2. M03 — architecture and source structure.
3. M06 and M07 — Capability and Business Date Product Owner decisions.
4. M04 and M05 — identity and session.
5. M08, M12, and M13 — configuration, report history, and time.
6. M09, M10, and M11 — persistence, use-case contracts, and atomicity.
7. M14 — API contract style.
8. M15, M16, and M17 — tests, local workflow, secrets, and synthetic data.
9. M02 — final dependency review and lockfile authorization after all required
   libraries are known.
10. D01 through D05 during Sprint 1 before their related stories merge.

No recommendation becomes active through this sequence alone. Each material choice
must receive explicit approval and the appropriate Decision Log entry or status
change.

# 8. Coding gate

Sprint 1 coding may begin only when:

- M01 through M17 are approved or explicitly removed from scope by an approved
  constraint;
- the Decision Log records material outcomes;
- dependency installation is authorized;
- the Venue-opening Capability and Business Date rules are approved;
- the initial synthetic Venue-opening fixture is approved;
- the Product Owner authorizes Sprint 1 implementation under DEC-016.

Items D01 through D05 must be resolved before the related integrated work is marked
Done. Items W01 through W18 remain outside Sprint 1 unless a new approved decision
changes scope.
