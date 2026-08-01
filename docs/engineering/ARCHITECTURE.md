# BeachOS Software Architecture

## 1. Purpose and authority

This document defines the target software boundaries for BeachOS and its future
industry products. It prepares Sprint 1 implementation without creating source
code, database design, transport contracts, or new business rules.

It is subordinate to the accepted:

- Decision Log;
- Domain Model;
- Domain Events;
- Product Requirements;
- Master Blueprint;
- Framework and Workflows;
- MVP Backlog;
- Sprint Plan.

When technology and the business disagree, the approved business model wins.
Technology may be replaced. Business meaning must remain stable.

Recommendations that still require approval are listed in
`SPRINT1_TECHNICAL_DECISIONS.md`. Their presence here does not mark them Accepted.

## 2. Architectural goals

The architecture must:

- support one responsive staff web application;
- keep one central source of operational and financial truth;
- enforce authentication, Capabilities, and business rules on the server;
- deliver Sprint 1 as a small complete vertical slice;
- remain a modular single application until measured needs justify separation;
- keep Domain Concepts independent from frameworks and storage;
- support tablet, desktop, and mobile from one product;
- protect complete, atomic, retry-safe business actions;
- preserve sensitive and financial history;
- support BeachOS, future RestaurantOS, HotelOS, and other industry packs;
- support future plugins without giving them uncontrolled access to core data;
- allow individual modules to evolve without turning the repository into unrelated
  applications;
- remain understandable and maintainable over a ten-year horizon.

## 3. High-level architecture

BeachOS is a modular web platform with these runtime responsibilities:

1. **Staff Web Application**
   - One responsive application used by supported Roles and devices.
   - Presents task-focused experiences.
   - Sends intentions and retrieves current state.
   - Treats live notices as prompts to reload authoritative state.
   - Never becomes the final enforcement boundary.

2. **Application Server**
   - Authenticates the Staff Member.
   - Establishes Organization and Venue context.
   - Authorizes protected actions through explicit Capabilities.
   - Executes Application use cases.
   - Enforces Domain rules.
   - Coordinates atomic persistence.
   - Creates required Activity Logs.
   - Returns explicit success, business rejection, authorization denial, or
     unexpected failure.

3. **Central Relational Database**
   - Holds authoritative operational, financial, identity, authorization, and
     accountability state.
   - Supports transactional integrity and essential uniqueness.
   - Preserves history.
   - Does not define the business language by itself.

4. **Live Notice Boundary**
   - Notifies connected clients that relevant confirmed state changed.
   - Carries enough identity to prompt safe refresh.
   - Is never a second source of truth.
   - May be replaced without changing Domain behavior.

5. **Operational Adapters**
   - Connect approved infrastructure concerns such as time, identifiers, secrets,
     monitoring, future external systems, and plugin execution.
   - Implement interfaces owned by inner layers.

The initial deployment remains one backend application and one central database.
Module boundaries are logical and enforced in the codebase. They are not separate
network services.

## 4. Clean Architecture dependency rule

Dependencies point inward:

> Delivery and infrastructure → Application → Domain

The Domain depends on no framework, transport, database, web application, or
external provider.

The Application layer depends on:

- the Domain;
- ports it owns for persistence, identity context, time, transaction handling,
  Activity Logs, live notices, and other external effects.

Infrastructure depends on:

- Application ports;
- Domain types only where required to translate persisted or external values.

Delivery layers depend on:

- Application use-case contracts;
- delivery-specific presentation or transport models.

Inner layers never import outer layers. Cross-feature calls use explicit
Application contracts or approved shared Domain concepts, not another feature’s
database or delivery implementation.

## 5. Platform composition

The long-term platform has four composition levels.

### 5.1 Hospitality Core

Shared business capabilities proven to apply across hospitality products, such as:

- Organization;
- Venue;
- Staff Member;
- Role;
- Capability;
- Business Date;
- Activity Log;
- shared operational identity and history concepts.

A concept enters Hospitality Core only when its cross-industry meaning is stable.
Beach Club assumptions must not be generalized prematurely.

### 5.2 Industry Packs

An Industry Pack defines business capabilities for one operating context:

- BeachOS pack;
- future RestaurantOS pack;
- future HotelOS pack;
- future ResortOS or Events pack if approved.

An Industry Pack may:

- define industry-specific Domain policies;
- contribute Application use cases;
- contribute web feature packs;
- provide industry-specific configuration and navigation;
- map shared core concepts into approved industry workflows.

An Industry Pack may not:

- fork the Hospitality Core;
- redefine an existing official concept silently;
- bypass central authorization or Activity Logs;
- access another pack’s persistence directly;
- make technology-specific concepts part of the Domain.

BeachOS is the first Industry Pack. It owns beach-specific meaning such as Beach
Sunbed obligations and the current Responsible Waiter rule where that meaning is
not yet proven universal.

### 5.3 Modular Feature Packs

A Feature Pack is a cohesive vertical business capability inside a platform or
Industry Pack. Initial feature boundaries include:

- Identity and Access;
- Venue Opening;
- Venue and Service Locations;
- Customer Groups;
- Menus;
- Orders;
- Preparation;
- Billing;
- Payments;
- Operational History;
- Reporting.

Each Feature Pack contains only the layers it needs:

- Domain policy or concepts;
- Application use cases and ports;
- Infrastructure adapters;
- API delivery;
- Web experience;
- tests.

Feature Packs are compile-time modules inside the modular application. They are not
independent deployments or runtime plugins.

### 5.4 Future Plugins

Plugins are optional extensions installed or enabled through an approved lifecycle.
They are not required for Sprint 1.

Plugins interact only through versioned extension contracts. They never receive
unrestricted access to the Domain, database, authentication material, or internal
module code.

## 6. Frontend architecture

### Responsibilities

The frontend:

- provides one responsive staff application;
- composes Role-focused routes and Feature Pack experiences;
- renders current information in official business language;
- captures user intentions;
- maintains temporary presentation state;
- presents loading, empty, disabled, pending, success, rejection, degraded, and
  failure states;
- prevents obvious invalid interaction for usability;
- receives live notices and retrieves authoritative state;
- preserves safe pending-request identity across refresh and reconnect;
- adapts layout to tablet, desktop, and mobile;
- applies accessibility and localization conventions.

### Frontend boundaries

The frontend is divided into:

- **Application Shell**
  - session bootstrap;
  - Venue context;
  - navigation;
  - common error and connection state;
  - industry-pack and Feature Pack registration.

- **Feature Experiences**
  - Venue Opening;
  - later Host Dashboard, Guest Arrival, and other capabilities.
  - Each experience owns its screens, interaction state, delivery models, and
    feature-level tests.

- **Shared Presentation**
  - genuinely reusable interaction patterns;
  - accessibility behavior;
  - formatting of approved common concepts;
  - no business decisions.

- **Client Delivery Adapters**
  - communication with the API;
  - session-aware request behavior;
  - live-notice connection;
  - no Domain rule enforcement.

### Frontend dependency rule

Feature experiences may depend on:

- shell contracts;
- approved shared presentation;
- generated or manually governed public API contracts;
- common business vocabulary types that contain no behavior.

They may not depend on:

- backend source;
- database models;
- another feature’s internal state;
- infrastructure details;
- plugin internals;
- Role names as authorization proof.

### State ownership

- Server business state remains authoritative.
- Temporary input, focus, dialog, and disclosure state belongs to the frontend.
- Pending business actions have one stable client-visible request identity.
- Cached server data is presentation support only.
- Connection state and business state are separate.
- Live notices invalidate or prompt refresh; they do not directly establish
  completed truth unless the approved contract explicitly confirms it and the
  authoritative state can be reconciled.

### Sprint 1 frontend boundary

Sprint 1 includes only the Host Venue Opening experience:

- loading;
- declarations pending;
- blocked department;
- ready to open;
- limited access;
- confirmation;
- opening in progress;
- success;
- Opening Report;
- minimal Venue-open destination;
- degraded, restored, and error states.

It does not include department declaration editing in the Host experience.

## 7. Backend architecture

### Responsibilities

The backend:

- verifies the authenticated identity;
- establishes Organization, Venue, and Business Date scope;
- evaluates explicit Capabilities;
- invokes one Application use case per intention;
- loads authoritative state through ports;
- executes Domain rules;
- coordinates transactions;
- protects uniqueness and concurrency;
- writes permanent business facts and required Activity Logs;
- publishes post-commit live notices;
- exposes current-state queries;
- returns stable outcome categories;
- records operational diagnostics without exposing secrets.

### Modular monolith

The backend begins as one deployable application with strong internal modules.

This is preferred because:

- Sprint 1 has one team and one tightly related transaction boundary;
- operational and Activity Log consistency is easier to protect;
- local development, testing, deployment, and recovery remain simpler;
- module extraction can occur later from evidence.

No module may be separated into a service merely to mirror an organization chart or
future possibility. Separation requires a recorded reason such as independent
scaling, reliability isolation, ownership, compliance, or deployment cadence.

### Backend boundaries

Each Feature Pack exposes:

- public Application commands and queries;
- public outcome contracts;
- published confirmed events or notices intended for other modules;
- no direct repository or table access.

Internal Domain entities, persistence mappings, and helper services remain private.

## 8. Shared packages

Shared packages reduce duplication only when a stable shared responsibility exists.

### Allowed shared responsibilities

- code-quality and build configuration;
- public API contract descriptions;
- stable value representations that cross delivery boundaries;
- shared testing utilities without business behavior;
- accessible presentation primitives;
- observability conventions;
- plugin contract definitions after plugin architecture approval.

### Forbidden shared responsibilities

- a generic “utils” dumping ground;
- mutable global application state;
- database models shared with the web application;
- Domain entities serialized directly as API contracts;
- business rules copied into frontend packages;
- feature-specific behavior generalized after one use;
- imports that allow Feature Packs to bypass public contracts.

Shared packages are owned explicitly. A package without an owner or clear consumers
should not exist.

## 9. Domain layer

### Responsibilities

The Domain layer expresses business truth:

- official business concepts;
- invariants;
- lifecycle rules;
- value meaning;
- decisions made from business facts;
- Domain Events describing completed facts;
- Domain services only when a rule does not naturally belong to one concept.

### Domain layer properties

- framework independent;
- database independent;
- transport independent;
- synchronous in reasoning even if outer delivery is asynchronous;
- deterministic when provided time, identity, and approved external facts;
- testable without web, database, network, or filesystem;
- uses official vocabulary.

### What the Domain layer does not do

- authenticate a browser session;
- parse an HTTP request;
- execute database queries;
- publish a network message;
- write technical logs;
- choose a UI state;
- read environment variables;
- call plugins directly;
- decide an unresolved Product Owner rule.

### Domain Events

Domain Events:

- state completed business facts;
- are created only from approved business outcomes;
- are not transport messages by definition;
- do not authorize actions;
- do not imply event sourcing;
- remain distinct from Activity Logs.

For Sprint 1, the relevant official events are:

- `Department Readiness Declared`;
- `Venue Opened for Business Date`;
- `Activity Logged`.

There is no Sprint 1 `Venue Opening Started`, `Opening Report Created`, or accepted
`Venue Opening Rejected` Domain Event.

## 10. Application layer

### Responsibilities

The Application layer coordinates one business intention or query.

It:

- accepts an authenticated actor context from the delivery boundary;
- confirms Organization and Venue scope;
- requests authorization through an Application port;
- loads required Domain state;
- invokes Domain behavior;
- coordinates transaction boundaries;
- persists changed authoritative state;
- requests the required Activity Log;
- publishes live notices only after successful commit;
- returns an explicit outcome;
- protects safe retry and request identity.

### Commands and queries

- A Command expresses an intention to change business state.
- A Query retrieves current or historical information without changing business
  state.
- A Command has one responsible Application handler.
- A Query does not reuse a Command as a shortcut.
- Validation failure, authorization denial, business rejection, conflict, unknown
  outcome, and unexpected technical failure remain distinguishable.

### Application ports

Ports are owned by the Application layer and describe capabilities required from
outer layers, including:

- current authenticated actor;
- Capability evaluation;
- Unit of Work or transaction boundary;
- repositories for authoritative Feature Pack state;
- authoritative clock;
- request identity and safe retry store;
- Activity Log writer;
- live-notice publisher;
- diagnostic event sink.

Ports describe responsibilities, not technologies.

### Sprint 1 use cases

The Sprint 1 Application surface is limited to:

- retrieve current Venue Opening context;
- declare department readiness;
- retrieve current readiness;
- evaluate opening eligibility;
- open Venue for Business Date;
- retrieve the authoritative opening outcome;
- retrieve the Opening Report.

The Host experience uses the retrieval and opening use cases. The declaration use
case belongs to the department responsible person’s separate authorized context.

## 11. Infrastructure layer

### Responsibilities

Infrastructure implements Application ports:

- relational persistence;
- transaction handling;
- identity/session provider integration;
- Capability storage and evaluation support;
- authoritative time;
- identifier generation;
- live-notice transport;
- Activity Log persistence;
- operational logging and metrics;
- environment configuration;
- future external integrations;
- future plugin hosting.

### Infrastructure rules

- Infrastructure translates; it does not redefine business rules.
- Adapter failure is translated into an Application outcome category.
- Secrets remain outside source code and business records.
- External provider identifiers do not replace internal business identity.
- A technology adapter may be replaced without changing Domain behavior.
- Infrastructure never calls a web screen or imports frontend code.

### Transactional effects

For a sensitive business outcome, the architecture must ensure that authoritative
state and required Activity Log history cannot silently diverge.

Live notices occur after durable success. A failed notice does not roll back a
completed business fact and must be recoverable by authoritative reload.

## 12. Database layer

### Responsibilities

The Database layer:

- stores authoritative relational state;
- enforces essential uniqueness and referential integrity;
- supports atomic business transactions;
- stores applied facts and immutable history;
- supports current-state and historical queries;
- supports controlled schema evolution;
- supports backup and restoration.

### Database boundary

Persistence models are Infrastructure concerns. They are not Domain entities and are
not API models.

Only repositories and transaction adapters access persistence models.

Feature Packs own their persistence boundary. Another Feature Pack may not query or
write those tables directly. Cross-feature information is obtained through public
Application contracts or approved read models.

### Sprint 1 integrity responsibilities

Without prescribing schema, persistence must support:

- one Venue under one Organization context;
- one unambiguous Business Date;
- current mandatory Operational Departments;
- responsible-person relationship;
- current and required historical readiness declarations;
- at most one successful opening for a Venue and Business Date;
- atomic official opening state and Opening Report;
- required Activity Log attribution;
- safe repeated request recognition.

### Prohibited database behavior

- silent deletion of opening history;
- direct client access;
- authorization based only on a stored Role label;
- shared tables treated as public module APIs;
- database triggers used to invent unapproved business events;
- schema structure leaking into official business vocabulary.

## 13. API layer

### Responsibilities

The API layer is a delivery adapter between the web application and Application use
cases.

It:

- parses and validates transport shape;
- establishes authenticated session context;
- passes the actor and scoped intention to the Application layer;
- maps Application outcomes to stable delivery outcomes;
- exposes current-state and historical queries;
- never performs Domain decisions itself;
- never exposes persistence models;
- never treats a hidden frontend action as authorization.

### API contract categories

The public contract must distinguish:

- successful query;
- accepted and completed Command;
- invalid input;
- unauthenticated session;
- authenticated but unauthorized action;
- business rule rejection;
- concurrency conflict;
- request still pending or outcome unknown;
- unexpected technical failure.

Exact transport shape remains a recommended decision, not an architectural fact in
this document.

### Contract evolution

- Contracts are versioned deliberately when compatibility changes.
- Public contracts use official business language.
- Domain entities are not serialized directly.
- Delivery models may evolve independently from persistence.
- Industry packs and plugins cannot depend on private endpoints.

## 14. Authentication boundary

Authentication answers:

> Which individual Staff Member is using this session?

### Responsibilities

- verify individual identity;
- create and revoke secure sessions;
- prevent anonymous protected action;
- support shared devices without shared identities;
- provide current Staff Member identity to the Application boundary;
- expire or revoke access safely;
- record approved security-relevant facts.

### Boundary rules

- Authentication does not grant business authority.
- The frontend never asserts identity authoritatively.
- Session data does not contain mutable business truth that can outlive central
  state.
- Session expiration after a submitted Command does not erase the Command identity
  or make repetition safe.
- Authentication secrets never enter Domain entities, Activity Logs, API responses,
  or plugins.

The exact identity and session solution remains subject to approval.

## 15. Authorization boundary

Authorization answers:

> May this authenticated Staff Member attempt this protected action in this
> Organization and Venue context?

### Responsibilities

- evaluate explicit Capability grants;
- evaluate their current scope;
- distinguish Role responsibility from Capability;
- support revocation;
- deny by default when current authority cannot be confirmed;
- pass an authorization result into the Application use case;
- allow Domain rules to make the final business decision.

### Evaluation order

For every protected Command:

1. Authenticate the individual.
2. Confirm Organization and Venue context.
3. Confirm the required Capability.
4. Load authoritative Domain state.
5. Apply all business rules.
6. Execute atomically if allowed.
7. Create required Activity Log.

A Capability never overrides a Domain invariant.

### Sprint 1 boundary

Sprint 1 requires authorization for:

- department readiness declaration by the correct responsible person;
- opening the Venue by the Host with the required Capability.

The official Capability catalogue and governance remain Product Owner approval
items.

## 16. Activity Log boundary

### Purpose

The Activity Log preserves accountability for sensitive actions. It is not a
technical debug log and not employee surveillance.

### Responsibilities

For a required Activity Log, preserve:

- actor or approved origin;
- Organization and Venue context;
- time;
- affected business subject;
- official action or event;
- relevant prior and resulting facts;
- reason where required;
- request correlation needed to investigate safe retry.

### Boundary rules

- Domain Event and Activity Log remain distinct.
- A sensitive successful action cannot be reported complete if its required
  Activity Log was silently lost.
- Activity Log writing participates in the same consistency boundary as the
  sensitive authoritative outcome where required.
- Activity Logs are append-only.
- Correction adds traceable history; it does not rewrite the original.
- Access is explicit and minimum necessary.
- Technical diagnostics must not be stored as Activity Logs unless they represent
  approved business accountability.

### Sprint 1

The successful Capability-protected Venue opening requires an Activity Log.
Department declarations remain permanently attributable in the Opening Report;
ordinary declarations do not automatically require a separate Activity Log under
the current approved rules.

## 17. Live notice and synchronization boundary

### Responsibilities

- notify relevant connected clients after confirmed changes;
- identify the changed context sufficiently for a safe refresh;
- tolerate duplicate, delayed, missed, and out-of-order delivery;
- support reconnection and current-state reconciliation.

### Rules

- A notice is not authoritative state.
- A notice never confirms a Command to the initiating client by itself.
- The current database state can always be queried independently.
- A missed notice cannot cause permanent inconsistency.
- Notice publication failure is observable and recoverable.
- Full offline operation is not part of the initial release.

## 18. Future Plugin Architecture

### Purpose

Future plugins allow optional integrations and extensions without weakening the
Hospitality Core or Industry Pack boundaries.

### Plugin categories

Potential categories, subject to future approval:

- external integration adapters;
- reporting consumers;
- notification destinations;
- approved payment or fiscal connectors;
- device connectors;
- read-only operational extensions;
- Industry Pack-specific extensions.

The list does not approve any plugin or integration.

### Plugin contract

A plugin contract may expose only approved capabilities such as:

- subscribe to a versioned set of confirmed public events;
- execute an explicitly registered extension action;
- request an approved read model;
- contribute a declared navigation or presentation extension point;
- report health and version information.

### Plugin manifest responsibilities

A future plugin declares:

- identity and version;
- compatible platform and Industry Pack versions;
- requested extension points;
- requested data scopes;
- requested Capabilities;
- configuration requirements;
- operational owner;
- failure behavior;
- support and upgrade policy.

### Isolation and safety

Plugins:

- have no direct database access;
- cannot import private Feature Pack code;
- cannot authenticate users independently inside BeachOS;
- cannot grant themselves Capabilities;
- cannot bypass Domain rules;
- cannot alter historical facts;
- receive minimum necessary data;
- operate with explicit timeout and failure isolation;
- expose auditable sensitive actions;
- can be disabled without preventing core Venue operation where the plugin is
  non-essential.

### Plugin execution

Core business transactions must not depend synchronously on an optional plugin.

If a future mandatory external integration participates in a business outcome, its
failure and consistency rules require a separate accepted architectural and product
decision. It must not be treated as an ordinary optional plugin.

### Compatibility

- Extension contracts are versioned.
- Breaking changes use explicit migration and deprecation policy.
- Plugins declare compatibility before activation.
- A platform upgrade must detect incompatible plugins before deployment.
- Industry-specific plugins cannot assume they apply to another Industry Pack.

### Governance

Plugin installation, approval, configuration, data access, update, suspension, and
removal require a future governance model. No general marketplace or third-party
execution is implied.

## 19. Cross-cutting quality boundaries

### Security

- least privilege;
- secure individual sessions;
- server-side enforcement;
- secrets outside code;
- safe error disclosure;
- dependency and plugin review;
- explicit production access.

### Reliability

- atomic sensitive outcomes;
- safe retry;
- central truth;
- tested concurrency;
- explicit degraded state;
- backups and restoration before production.

### Observability

- technical logs, metrics, and traces remain distinct from Activity Logs;
- sensitive data is minimized;
- a request can be followed across delivery, Application, and Infrastructure
  boundaries;
- business outcome is visible without inspecting raw database state.

### Performance

- common operational queries have explicit targets before production;
- Feature Pack boundaries allow focused optimization;
- performance work uses measured evidence;
- caching never changes source-of-truth rules.

### Testing

- Domain rules are tested without infrastructure;
- Application use cases are tested through ports;
- adapters are integration tested;
- public API contracts are tested;
- critical staff journeys are end-to-end tested;
- industry packs have contract tests against the Hospitality Core;
- future plugins have compatibility and isolation tests.

## 20. Sprint 1 architecture slice

Sprint 1 should exercise the full architecture through one narrow vertical slice:

1. Web Host Venue Opening experience.
2. API delivery for current state, readiness declaration, opening, outcome, and
   report retrieval.
3. Authentication and authorization boundaries.
4. Venue Opening Application use cases.
5. Venue Opening Domain rules.
6. Relational persistence and transaction boundary.
7. Activity Log consistency.
8. Post-commit live notice.
9. Automated tests at each boundary.

The slice must not create generic infrastructure beyond an immediate need.
Successful Sprint 1 proves the boundaries; it does not finish the platform.

## 21. Architecture decision rules

- Record material choices before implementation.
- Keep recommendations separate from Accepted Decisions.
- Prefer one explicit dependency over implicit global access.
- Prefer an Application contract over cross-module persistence access.
- Prefer a Domain rule over duplicated frontend behavior.
- Prefer a small vertical slice over speculative platform construction.
- Extract shared behavior only after stable repeated use.
- Add a service, cache, queue, plugin, or new datastore only from demonstrated need.
- Preserve historical and security boundaries during every refactor.
- Review architecture against real hospitality operation, not framework fashion.
