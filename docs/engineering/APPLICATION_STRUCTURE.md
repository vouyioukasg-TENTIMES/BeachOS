# BeachOS Application Structure

## 1. Purpose

This document defines the target repository and module structure for BeachOS. It
applies Clean Architecture to a modular single application and prepares the
repository for:

- Sprint 1 Venue Opening;
- one shared responsive web application;
- modular Feature Packs;
- BeachOS and future RestaurantOS, HotelOS, and other Industry Packs;
- future plugins;
- long-term independent evolution of delivery, business rules, and infrastructure.

It describes folders and dependency rules only. It does not create the folders,
source files, components, APIs, database models, migrations, or infrastructure.

## 2. Structural principles

1. **Dependencies point inward.**
   - delivery → Application → Domain;
   - infrastructure → Application ports and Domain representations;
   - Domain → nothing outside Domain.

2. **Feature ownership is explicit.**
   - each Feature Pack owns its behavior and persistence boundary;
   - another feature uses its public Application contract.

3. **Industry variation is isolated.**
   - Hospitality Core holds proven shared concepts;
   - BeachOS holds beach-specific policy;
   - future packs do not fork the core.

4. **Shared means stable and genuinely shared.**
   - no generic utilities package;
   - no premature abstraction;
   - no business rules in presentation packages.

5. **Runtime boundaries do not dictate repository boundaries.**
   - one backend deployable can contain strongly separated modules;
   - one web application can contain Role-focused Feature Packs.

6. **Tests follow ownership.**
   - tests for one module live beside it;
   - root tests protect contracts and complete journeys.

## 3. Target repository tree

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── apps/
│   ├── api/
│   │   ├── src/
│   │   │   └── beachos/
│   │   │       ├── bootstrap/
│   │   │       ├── core/
│   │   │       │   ├── identity_access/
│   │   │       │   ├── organizations/
│   │   │       │   ├── venues/
│   │   │       │   ├── operational_history/
│   │   │       │   └── shared_domain/
│   │   │       ├── packs/
│   │   │       │   ├── beachos/
│   │   │       │   │   ├── venue_opening/
│   │   │       │   │   │   ├── domain/
│   │   │       │   │   │   ├── application/
│   │   │       │   │   │   ├── infrastructure/
│   │   │       │   │   │   └── delivery/
│   │   │       │   │   ├── service_locations/
│   │   │       │   │   ├── customer_groups/
│   │   │       │   │   ├── menus/
│   │   │       │   │   ├── orders/
│   │   │       │   │   ├── preparation/
│   │   │       │   │   ├── billing/
│   │   │       │   │   ├── payments/
│   │   │       │   │   └── reporting/
│   │   │       │   ├── restaurantos/
│   │   │       │   └── hotelos/
│   │   │       ├── delivery/
│   │   │       │   ├── api/
│   │   │       │   └── live_notices/
│   │   │       ├── infrastructure/
│   │   │       │   ├── persistence/
│   │   │       │   ├── authentication/
│   │   │       │   ├── authorization/
│   │   │       │   ├── activity_logs/
│   │   │       │   ├── time/
│   │   │       │   ├── observability/
│   │   │       │   └── configuration/
│   │   │       └── plugins/
│   │   │           ├── contracts/
│   │   │           ├── registry/
│   │   │           └── runtime/
│   │   ├── tests/
│   │   │   ├── architecture/
│   │   │   ├── integration/
│   │   │   └── support/
│   │   └── migrations/
│   └── web/
│       ├── src/
│       │   ├── app/
│       │   ├── platform/
│       │   │   ├── identity/
│       │   │   ├── venue_context/
│       │   │   ├── navigation/
│       │   │   ├── connectivity/
│       │   │   └── live_notices/
│       │   ├── packs/
│       │   │   ├── beachos/
│       │   │   │   └── features/
│       │   │   │       ├── venue_opening/
│       │   │   │       ├── host_dashboard/
│       │   │   │       ├── guest_arrival/
│       │   │   │       ├── customer_groups/
│       │   │   │       ├── waiter_operations/
│       │   │   │       ├── kitchen/
│       │   │   │       ├── bar/
│       │   │   │       ├── billing/
│       │   │   │       ├── payments/
│       │   │   │       └── manager_dashboard/
│       │   │   ├── restaurantos/
│       │   │   └── hotelos/
│       │   ├── shared/
│       │   │   ├── presentation/
│       │   │   ├── accessibility/
│       │   │   ├── formatting/
│       │   │   └── testing/
│       │   └── adapters/
│       │       ├── api/
│       │       ├── session/
│       │       └── live_notices/
│       └── tests/
│           ├── architecture/
│           └── support/
├── packages/
│   ├── api-contracts/
│   ├── config/
│   ├── plugin-contracts/
│   ├── testing/
│   ├── ui/
│   └── shared/
├── infrastructure/
│   ├── docker/
│   ├── deployment/
│   ├── monitoring/
│   └── runbooks/
├── scripts/
│   ├── development/
│   ├── quality/
│   ├── database/
│   └── release/
├── tests/
│   ├── architecture/
│   ├── contract/
│   ├── integration/
│   ├── e2e/
│   ├── unit/
│   ├── performance/
│   └── fixtures/
├── docs/
│   ├── engineering/
│   └── ui/
├── framework/
│   ├── 00 Vision/
│   ├── 01 Philosophy/
│   ├── 02 Operational Principles/
│   ├── 03 Roles/
│   ├── 04 Workflows/
│   ├── 05 Playbooks/
│   ├── 06 Coaching/
│   ├── 07 Knowledge/
│   ├── 08 Decision Engine/
│   └── 09 Operational Standards/
├── ux/
└── packages-and-workspace configuration at repository root
```

Future folders in this tree are created only when their approved phase needs them.
An empty folder is not evidence of architecture progress.

# 4. Root folders

## `.github/`

### Purpose

Repository collaboration, review templates, dependency update policy, and automated
quality workflows.

### Ownership

Engineering maintainers with security review for permissions and secrets.

### Allowed dependencies

- repository scripts;
- approved runtime metadata;
- approved test and build commands.

### Forbidden dependencies

- business logic;
- production credentials;
- undocumented deployment authority;
- workflow steps that bypass required human approval.

## `apps/`

### Purpose

Holds independently runnable delivery applications.

### Ownership

Application engineering team. Each child application has a named technical owner.

### Allowed dependencies

- approved `packages/`;
- its own internal modules;
- runtime libraries approved for that application.

### Forbidden dependencies

- another application’s private source;
- direct imports across `apps/api` and `apps/web`;
- business behavior stored only in delivery code.

## `packages/`

### Purpose

Holds small, stable, explicitly owned packages shared by more than one application
or extension boundary.

### Ownership

Platform engineering. Every package has a named owner and consumer list.

### Allowed dependencies

- another lower-level package when its public contract explicitly permits it;
- no application-private source.

### Forbidden dependencies

- imports from `apps/`;
- feature-specific persistence;
- a generic collection of unrelated helpers;
- circular package dependencies;
- Domain rules duplicated for frontend convenience.

## `infrastructure/`

### Purpose

Holds local infrastructure definitions, future deployment definitions, operational
monitoring configuration, and runbooks.

### Ownership

Platform or operations engineering with security approval.

### Allowed dependencies

- deployable artifacts;
- environment contracts;
- approved operational scripts.

### Forbidden dependencies

- Domain rules;
- application business orchestration;
- secrets;
- production changes without the release and approval process.

## `scripts/`

### Purpose

Holds safe, repeatable developer, quality, database, and release operations.

### Ownership

Engineering maintainers. Destructive or production-capable scripts require
additional review.

### Allowed dependencies

- public repository commands;
- approved environment variables;
- documented tools.

### Forbidden dependencies

- hidden business decisions;
- embedded credentials;
- silent destructive defaults;
- direct production data manipulation outside approved operational procedures.

## `tests/`

### Purpose

Holds tests that span applications, modules, or runtime boundaries.

### Ownership

Shared by engineering and quality ownership; each suite has a named maintainer.

### Allowed dependencies

- public application entry points;
- approved test support and synthetic fixtures;
- deployed or locally composed test services.

### Forbidden dependencies

- production data;
- private implementation access used merely to make a test easy;
- tests that duplicate a module-owned unit test without a cross-boundary purpose.

## `docs/`

### Purpose

Holds product, domain, architecture, engineering, governance, and implementation
planning authority.

### Ownership

Product Owner for business authority; designated engineering owner for engineering
documents.

### Allowed dependencies

- references to approved repository documents;
- links to source and test evidence after implementation.

### Forbidden dependencies

- generated runtime state treated as product authority;
- silent changes to accepted Decisions;
- technical documents redefining the Domain.

## `framework/`

### Purpose

Holds the technology-independent operational Framework.

### Ownership

Business and operational leadership.

### Allowed dependencies

- approved product and domain vocabulary.

### Forbidden dependencies

- application framework details;
- database, API, or UI implementation;
- software limitations presented as hospitality rules.

## `ux/`

### Purpose

Holds implementation-ready interaction specifications and user journeys.

### Ownership

UX leadership with Product Owner approval for behavior.

### Allowed dependencies

- approved Domain, Decisions, Workflows, and backlog.

### Forbidden dependencies

- new business rules;
- visual artifacts treated as authorization;
- source code or framework-specific behavior.

# 5. Backend application folders

## `apps/api/`

### Purpose

The single backend deployable.

### Ownership

Backend engineering lead.

### Allowed dependencies

- approved backend runtime and packages;
- `packages/api-contracts` where appropriate;
- internal modules through their public contracts.

### Forbidden dependencies

- frontend source;
- browser presentation behavior;
- direct use of another deployable’s private internals.

## `apps/api/src/`

### Purpose

Backend production source root.

### Ownership

Backend engineering.

### Allowed dependencies

- approved backend libraries;
- repository shared contracts.

### Forbidden dependencies

- tests as runtime behavior;
- migrations as Domain behavior;
- undocumented import roots.

## `apps/api/src/beachos/`

### Purpose

Namespace for the backend platform composition.

### Ownership

Backend architecture owner.

### Allowed dependencies

- its child boundaries;
- approved shared packages.

### Forbidden dependencies

- unowned global helpers;
- circular dependencies between core, packs, delivery, and infrastructure.

## `apps/api/src/beachos/bootstrap/`

### Purpose

Composition root. Creates the runtime graph, registers Industry and Feature Packs,
connects ports to adapters, and starts delivery.

### Ownership

Backend platform owner.

### Allowed dependencies

- all public module composition contracts;
- delivery and infrastructure adapters;
- configuration.

### Forbidden dependencies

- Domain decisions;
- business validation;
- feature behavior;
- direct persistence operations.

Only the composition root may know concrete adapters across all layers.

## `apps/api/src/beachos/core/`

### Purpose

Hospitality Core modules proven to be shared across Industry Packs.

### Ownership

Domain architecture group and module owners.

### Allowed dependencies

- `core/shared_domain`;
- public contracts of other core modules when explicitly approved.

### Forbidden dependencies

- BeachOS-specific policy;
- Industry Pack internals;
- delivery or concrete infrastructure;
- speculative universal concepts.

## `core/identity_access/`

### Purpose

Staff Member identity, Role responsibility, Capability authority, and approved
account/session business coordination.

### Ownership

Security and identity module owner.

### Allowed dependencies

- shared core Domain concepts;
- Application ports for authentication and authorization infrastructure.

### Forbidden dependencies

- Venue Opening business rules;
- frontend session storage;
- concrete identity provider code inside Domain or Application.

## `core/organizations/`

### Purpose

Organization boundary and multi-Venue ownership context.

### Ownership

Hospitality Core domain owner.

### Allowed dependencies

- shared core concepts.

### Forbidden dependencies

- Industry-specific operational rules;
- Venue Opening delivery.

## `core/venues/`

### Purpose

Stable shared Venue identity and approved shared Venue context, including Business
Date policy when proven core.

### Ownership

Venue core owner.

### Allowed dependencies

- Organization public contract;
- shared Domain concepts.

### Forbidden dependencies

- Beach Sunbed or other industry-specific behavior;
- Opening screen logic;
- persistence adapter imports.

## `core/operational_history/`

### Purpose

Activity Log and approved Audit Trail coordination.

### Ownership

Security, compliance, and operational history owner.

### Allowed dependencies

- shared identity and context contracts;
- Application ports for durable history.

### Forbidden dependencies

- technical logging implementation;
- employee scoring;
- direct edits to another module’s history.

## `core/shared_domain/`

### Purpose

Minimal stable Domain building blocks shared by multiple core modules and Industry
Packs.

### Ownership

Domain architecture owner.

### Allowed dependencies

- language/runtime standard facilities only.

### Forbidden dependencies

- frameworks;
- persistence;
- transport;
- feature-specific rules;
- miscellaneous utilities.

## `apps/api/src/beachos/packs/`

### Purpose

Contains Industry Packs.

### Ownership

Platform product architecture and each Industry Pack owner.

### Allowed dependencies

- Hospitality Core public contracts;
- Industry Pack-owned Feature Packs.

### Forbidden dependencies

- another Industry Pack’s private modules;
- changes to Hospitality Core by copying or shadowing it.

## `packs/beachos/`

### Purpose

Beach Club industry behavior and composition.

### Ownership

BeachOS product and engineering owners.

### Allowed dependencies

- Hospitality Core public contracts;
- its own Feature Packs.

### Forbidden dependencies

- RestaurantOS or HotelOS internals;
- beach-specific behavior added to shared core without approval.

## `packs/restaurantos/` and `packs/hotelos/`

### Purpose

Reserved future Industry Packs.

### Ownership

Future named industry teams.

### Allowed dependencies

- Hospitality Core public contracts;
- their own approved Feature Packs.

### Forbidden dependencies

- BeachOS private modules;
- existence before an approved industry roadmap phase needs them.

These folders should not be created during Sprint 1 merely as empty placeholders.

## `packs/beachos/venue_opening/`

### Purpose

Owns the complete BeachOS Venue Opening Feature Pack.

### Ownership

Sprint 1 feature team.

### Allowed dependencies

- Hospitality Core public contracts for Venue, identity, Capability, time, and
  Activity Log;
- its own inner layers.

### Forbidden dependencies

- Customer Group, Order, Billing, Payment, Guest Arrival, or later Dashboard
  internals;
- concrete web or database frameworks in Domain;
- Host UI state inside backend business rules.

## Future BeachOS Feature Pack folders

The following folders use the same ownership and boundary rules:

- `service_locations/`
- `customer_groups/`
- `menus/`
- `orders/`
- `preparation/`
- `billing/`
- `payments/`
- `reporting/`

### Purpose

Each owns one cohesive approved business capability.

### Ownership

Named Feature Pack owner.

### Allowed dependencies

- Hospitality Core public contracts;
- explicitly approved public Application contracts from another Feature Pack.

### Forbidden dependencies

- another feature’s Domain internals;
- another feature’s persistence models;
- activation before its roadmap phase.

## Feature Pack `domain/`

### Purpose

Business concepts, invariants, policies, and Domain Events owned by the feature.

### Ownership

Feature’s domain owner.

### Allowed dependencies

- stable shared Domain;
- approved core Domain contracts.

### Forbidden dependencies

- Application layer;
- API;
- persistence;
- web;
- environment;
- clocks, identifiers, or providers without abstract input.

## Feature Pack `application/`

### Purpose

Commands, queries, use-case orchestration, ports, and public outcomes.

### Ownership

Feature’s application owner.

### Allowed dependencies

- its Domain;
- approved core Application contracts;
- ports defined by this layer.

### Forbidden dependencies

- concrete database, live-notice, session, or transport implementation;
- delivery models;
- direct access to another Feature Pack’s persistence.

## Feature Pack `infrastructure/`

### Purpose

Concrete adapters for feature persistence and other outer concerns.

### Ownership

Feature owner with platform review.

### Allowed dependencies

- feature Application ports;
- feature Domain representations;
- approved infrastructure libraries.

### Forbidden dependencies

- business decisions;
- frontend source;
- adapters used directly by another Feature Pack.

## Feature Pack `delivery/`

### Purpose

Feature-specific delivery translation for public API or live-notice contracts.

### Ownership

Feature owner with API governance review.

### Allowed dependencies

- feature Application public contracts;
- shared delivery conventions.

### Forbidden dependencies

- direct repository calls;
- persistence models;
- Domain mutation outside an Application use case.

## `apps/api/src/beachos/delivery/`

### Purpose

Cross-feature server delivery composition.

### Ownership

API platform owner.

### Allowed dependencies

- Feature Pack delivery registrations;
- Application public outcomes;
- approved API contracts.

### Forbidden dependencies

- Domain decisions;
- direct persistence;
- authorization based on route visibility.

## `delivery/api/`

### Purpose

Common API behavior: session context, request parsing, outcome mapping, contract
versioning, and error conventions.

### Ownership

API platform owner.

### Allowed dependencies

- public Application contracts;
- authentication boundary;
- approved shared API contracts.

### Forbidden dependencies

- feature persistence;
- business logic;
- database models as public responses.

## `delivery/live_notices/`

### Purpose

Composes relevant confirmed post-commit notices.

### Ownership

Platform reliability owner.

### Allowed dependencies

- public confirmed notice contracts;
- live-notice infrastructure port.

### Forbidden dependencies

- authoritative state mutation;
- treating delivery success as business success;
- requiring notices for state recovery.

## `apps/api/src/beachos/infrastructure/`

### Purpose

Shared concrete adapters that serve Application-owned ports.

### Ownership

Platform engineering.

### Allowed dependencies

- Application ports;
- Domain representations required for translation;
- approved infrastructure libraries.

### Forbidden dependencies

- Feature business policy;
- UI behavior;
- direct calls from Domain.

## Infrastructure child folders

| Folder | Purpose | Owner | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|---|
| `persistence/` | Database connection, transaction, shared persistence conventions | Data/platform owner | Application repository ports, migration contract | Domain decisions, API models |
| `authentication/` | Concrete identity and session adapter | Security owner | authentication ports, approved security tooling | Capability business policy, UI state |
| `authorization/` | Concrete Capability data access and evaluator adapter | Security owner | authorization ports, identity context | Role-only authorization, feature bypass |
| `activity_logs/` | Durable Activity Log adapter | History/security owner | Activity Log port and approved context | technical logs, destructive update |
| `time/` | Authoritative clock and Venue time translation | Platform owner | time port and approved Business Date policy | device-time authority, business policy invention |
| `observability/` | technical logs, metrics, traces, health | Reliability owner | correlation and safe diagnostic contracts | Activity Log replacement, sensitive payload dumping |
| `configuration/` | validated environment-specific technical configuration | Platform owner | environment contract | secrets in source, Venue business configuration hidden here |

## `apps/api/src/beachos/plugins/`

### Purpose

Future plugin contract integration, registry, and isolated runtime.

### Ownership

Platform extension owner and security.

### Allowed dependencies

- versioned plugin contracts;
- public Application extension points.

### Forbidden dependencies

- direct database access;
- private Feature Pack imports;
- activation in Sprint 1;
- self-granted Capability;
- unreviewed third-party execution.

## Plugin child folders

- `contracts/` — backend interpretation of approved extension contracts.
- `registry/` — approved plugin identity, compatibility, and activation records.
- `runtime/` — controlled invocation and isolation.

They remain absent until plugin lifecycle and governance are approved.

## `apps/api/tests/`

### Purpose

Backend-wide tests not owned by one Feature Pack.

### Ownership

Backend quality owner.

### Allowed dependencies

- public module and application composition contracts;
- synthetic support.

### Forbidden dependencies

- production data;
- cross-layer imports that violate production architecture.

### Child folders

- `architecture/` — enforces dependency rules.
- `integration/` — backend adapter and composition boundaries.
- `support/` — deterministic builders and synthetic fixtures.

Feature-specific unit and use-case tests remain beside the Feature Pack.

## `apps/api/migrations/`

### Purpose

Versioned database evolution after the migration approach is approved.

### Ownership

Data owner and affected Feature Pack owner.

### Allowed dependencies

- approved persistence design;
- migration tooling.

### Forbidden dependencies

- business-rule explanation as executable migration logic;
- silent historical rewrite;
- application runtime imports;
- creation before the migration decision is approved.

# 6. Web application folders

## `apps/web/`

### Purpose

The single responsive staff web application.

### Ownership

Frontend engineering lead.

### Allowed dependencies

- approved frontend packages;
- public API contracts;
- shared presentation packages.

### Forbidden dependencies

- backend source;
- database models;
- separate per-Role application forks.

## `apps/web/src/`

### Purpose

Frontend production source root.

### Ownership

Frontend engineering.

### Allowed dependencies

- approved frontend libraries and public packages.

### Forbidden dependencies

- test-only behavior in production;
- hidden global business state.

## `apps/web/src/app/`

### Purpose

Frontend composition root, application lifecycle, Industry Pack registration, and
top-level route composition.

### Ownership

Frontend platform owner.

### Allowed dependencies

- public registrations from platform, packs, shared presentation, and adapters.

### Forbidden dependencies

- feature business rules;
- database concepts;
- Feature Pack internals beyond registration contracts.

## `apps/web/src/platform/`

### Purpose

Shared frontend platform behavior needed by multiple Feature Packs.

### Ownership

Frontend platform team.

### Allowed dependencies

- adapters;
- shared presentation;
- public contracts.

### Forbidden dependencies

- Industry-specific workflow behavior;
- Role-based authorization as final enforcement;
- feature-specific server state.

## Platform child folders

| Folder | Purpose | Allowed dependencies | Forbidden dependencies |
|---|---|---|---|
| `identity/` | Signed-in identity presentation and session lifecycle | session adapter, public identity contract | credential storage policy invention, Feature business rules |
| `venue_context/` | Current Organization, Venue, Business Date presentation context | API adapter, common formatting | Venue Opening rule enforcement |
| `navigation/` | Registered routes and Role-focused task navigation | Feature Pack registrations | authorization proof, feature internals |
| `connectivity/` | Online, degraded, restored, freshness presentation | API and live-notice adapters | offline business authority |
| `live_notices/` | Notice subscription and authoritative invalidation | live-notice adapter, query refresh contract | direct business mutation |

## `apps/web/src/packs/`

### Purpose

Frontend Industry Packs and their Feature Experiences.

### Ownership

Each Industry Pack frontend owner.

### Allowed dependencies

- frontend platform public contracts;
- shared presentation;
- API contracts.

### Forbidden dependencies

- another Industry Pack’s internals;
- backend or database source.

## `packs/beachos/features/venue_opening/`

### Purpose

Owns the Sprint 1 Host Venue Opening interaction.

### Ownership

Sprint 1 frontend feature team and UX owner.

### Allowed dependencies

- platform identity, Venue context, connectivity, and live-notice contracts;
- shared presentation and accessibility;
- Venue Opening API contracts.

### Forbidden dependencies

- later BeachOS Feature Packs;
- business rules as authoritative client-only logic;
- department configuration;
- Customer Group or financial behavior.

### Internal organization

When implementation begins, the feature may organize:

- screens;
- interaction state;
- queries;
- Commands;
- public route registration;
- feature-level tests.

This document does not prescribe component or file names.

## Future frontend Feature Pack folders

The target tree lists:

- `host_dashboard/`
- `guest_arrival/`
- `customer_groups/`
- `waiter_operations/`
- `kitchen/`
- `bar/`
- `billing/`
- `payments/`
- `manager_dashboard/`

### Purpose

Each owns one approved staff experience.

### Ownership

Named feature team.

### Allowed dependencies

- platform public contracts;
- shared presentation;
- its public API contracts.

### Forbidden dependencies

- another feature’s private state or screens;
- implementation before its Sprint;
- duplicated Domain rules.

## `apps/web/src/shared/`

### Purpose

Frontend-only presentation support proven reusable.

### Ownership

Frontend platform and accessibility owners.

### Allowed dependencies

- approved frontend runtime;
- public contract value representations.

### Forbidden dependencies

- Feature-specific business behavior;
- server state ownership;
- authorization decisions;
- API endpoint knowledge inside presentation primitives.

## Shared frontend child folders

- `presentation/` — reusable non-business interaction patterns.
- `accessibility/` — focus, announcements, and accessible behavior helpers.
- `formatting/` — approved date, time, quantity, and business-label formatting.
- `testing/` — frontend feature test support.

Each folder must remain cohesive. Unrelated helpers are forbidden.

## `apps/web/src/adapters/`

### Purpose

Frontend outer adapters for communication and session-aware runtime behavior.

### Ownership

Frontend platform team.

### Allowed dependencies

- public API and live-notice contracts;
- browser runtime.

### Forbidden dependencies

- Domain rules;
- UI screen ownership;
- Feature Pack private state.

## Adapter child folders

- `api/` — request and response translation.
- `session/` — frontend interaction with server-controlled session lifecycle.
- `live_notices/` — transport connection and notice translation.

## `apps/web/tests/`

### Purpose

Frontend-wide architecture and shared test support.

### Ownership

Frontend quality owner.

### Allowed dependencies

- frontend public composition;
- synthetic fixtures.

### Forbidden dependencies

- backend internals;
- production data;
- feature tests unrelated to cross-app behavior.

# 7. Shared package folders

## `packages/api-contracts/`

### Purpose

Public delivery contract descriptions shared between web and backend tooling after
the contract-governance approach is approved.

### Ownership

API governance owner.

### Allowed dependencies

- stable business vocabulary value representations;
- contract tooling.

### Forbidden dependencies

- Domain entities with behavior;
- persistence models;
- business-rule execution;
- private endpoints.

## `packages/config/`

### Purpose

Shared static tool configuration proven common across workspaces.

### Ownership

Developer-experience owner.

### Allowed dependencies

- approved tooling.

### Forbidden dependencies

- runtime business configuration;
- secrets;
- Feature Pack policy.

## `packages/plugin-contracts/`

### Purpose

Future versioned public extension contracts.

### Ownership

Plugin platform and security owners.

### Allowed dependencies

- minimal public API contract values.

### Forbidden dependencies

- private Feature Pack types;
- database models;
- runtime plugin code;
- creation before plugin governance approval.

## `packages/testing/`

### Purpose

Cross-application synthetic fixtures, contract harnesses, and test conventions.

### Ownership

Quality platform owner.

### Allowed dependencies

- public contracts;
- approved test tooling.

### Forbidden dependencies

- production data;
- business behavior that belongs in Domain tests;
- runtime application dependency.

## `packages/ui/`

### Purpose

Optional future shared presentation system for one web application and approved
extensions.

### Ownership

Frontend design-system and accessibility owners.

### Allowed dependencies

- approved frontend presentation runtime.

### Forbidden dependencies

- BeachOS business rules;
- API calls;
- authentication or authorization decisions;
- creation before repeated use proves the need.

## `packages/shared/`

### Purpose

Current reserved placeholder only.

### Ownership

Platform architecture owner.

### Allowed dependencies

None until a specific stable responsibility is approved.

### Forbidden dependencies

- miscellaneous helpers;
- a mixed frontend/backend Domain package;
- Feature Pack internals;
- business logic.

Before implementation, either give this package one precise approved responsibility
or keep it empty. Do not use “shared” as an architectural shortcut.

# 8. Infrastructure folders

## `infrastructure/docker/`

### Purpose

Approved local container infrastructure only.

### Ownership

Developer-experience and platform owners.

### Allowed dependencies

- local environment contracts;
- approved service versions.

### Forbidden dependencies

- production deployment assumptions;
- application business logic;
- secrets.

## `infrastructure/deployment/`

### Purpose

Future approved environment and deployment definitions.

### Ownership

Platform operations and security.

### Allowed dependencies

- deployable artifacts;
- approved hosting and environment decisions.

### Forbidden dependencies

- content before provider and deployment decisions;
- credentials;
- bypass of human release approval.

## `infrastructure/monitoring/`

### Purpose

Future operational monitoring and alert definitions.

### Ownership

Reliability owner.

### Allowed dependencies

- approved observability contracts.

### Forbidden dependencies

- Activity Log business history;
- staff surveillance;
- unapproved production services.

## `infrastructure/runbooks/`

### Purpose

Operational procedures for deployment, rollback, backup, restore, incident response,
and degraded operation.

### Ownership

Operations with application and security review.

### Allowed dependencies

- approved environment and support processes.

### Forbidden dependencies

- undocumented destructive actions;
- credentials;
- procedures that override business rules.

# 9. Script folders

## `scripts/development/`

Purpose: repeatable local setup and runtime actions.

Owner: developer experience.

Allowed: approved local tools and safe environment validation.

Forbidden: dependency or database mutation without clear explicit command and
documentation.

## `scripts/quality/`

Purpose: formatting, static analysis, architecture checks, and test orchestration.

Owner: quality platform.

Allowed: approved repository checks.

Forbidden: source modification hidden inside a validation-only command.

## `scripts/database/`

Purpose: approved migration, fixture, and safe local/test database operations.

Owner: data platform.

Allowed: explicit environment targeting and synthetic data.

Forbidden: broad destructive defaults, production use without a separate approved
procedure, business corrections.

## `scripts/release/`

Purpose: future repeatable release preparation and verification.

Owner: release engineering.

Allowed: approved build, verification, provenance, and deployment contracts.

Forbidden: automatic production release without approval, embedded secrets, silent
schema change.

# 10. Root test folders

## `tests/architecture/`

Purpose: enforce dependency directions, public module boundaries, and forbidden
imports.

Owner: architecture owner.

Allowed: repository structure and compiled dependency information.

Forbidden: business acceptance duplication.

## `tests/contract/`

Purpose: verify public API, Industry Pack, core, and future plugin compatibility.

Owner: API and platform owners.

Allowed: public contracts.

Forbidden: private implementation coupling.

## `tests/integration/`

Purpose: verify real boundaries across applications, modules, database, sessions,
and live notices.

Owner: quality engineering.

Allowed: test environment services and synthetic data.

Forbidden: production services and data.

## `tests/e2e/`

Purpose: protect a small set of critical staff journeys.

Owner: quality engineering with Product Owner acceptance.

Allowed: public browser and backend behavior.

Forbidden: implementation-detail assertions or exhaustive unit behavior.

## `tests/unit/`

Purpose: root-owned utility tests only.

Owner: relevant utility owner.

Allowed: root utilities.

Forbidden: Feature Pack Domain or Application tests that belong beside source.

## `tests/performance/`

Purpose: future measured load and latency verification.

Owner: reliability engineering.

Allowed: approved non-production environments and synthetic workloads.

Forbidden: unapproved production load, invented targets.

## `tests/fixtures/`

Purpose: governed synthetic cross-system fixtures.

Owner: quality and domain owners.

Allowed: approved fictional Organizations, Venues, Staff Members, and operational
facts.

Forbidden: production personal, customer, payment, or secret data.

# 11. Documentation and design subfolders

## `docs/engineering/`

Purpose: current engineering architecture and decision recommendations.

Owner: software architecture.

Allowed: references to authoritative product and implementation documents.

Forbidden: silently accepting recommendations or changing business decisions.

## `docs/ui/`

Purpose: product-level UI and Dashboard specifications.

Owner: product design.

Allowed: approved UX behavior.

Forbidden: source code and new business rules.

## Framework numbered folders

Every folder from `00 Vision/` through `09 Operational Standards/` owns its named
technology-independent operational knowledge.

Allowed dependencies: earlier approved Framework principles and official business
vocabulary.

Forbidden dependencies: application implementation, technical constraints presented
as business truth.

# 12. Sprint 1 physical folder scope

Sprint 1 should create only the subset required for Venue Opening:

- backend bootstrap;
- core identity/access, Venue context, and operational history boundaries needed by
  the slice;
- BeachOS Venue Opening Feature Pack with Domain, Application, Infrastructure, and
  Delivery layers;
- shared backend delivery and infrastructure adapters required by the slice;
- web application shell and platform identity, Venue context, connectivity, and
  live-notice boundaries;
- BeachOS frontend Venue Opening feature;
- approved migrations;
- module-owned tests;
- cross-boundary architecture, integration, and end-to-end tests;
- only the scripts required for reproducible development and quality checks.

Sprint 1 must not create empty future Feature Packs, Industry Packs, plugin runtime,
production deployment, monitoring service configuration, or generic shared
libraries.

# 13. Dependency matrix

| From | May depend on | Must not depend on |
|---|---|---|
| Backend Domain | shared Domain, approved core Domain contracts | Application, delivery, infrastructure, database, web |
| Backend Application | own Domain, approved public Application contracts, owned ports | concrete adapters, delivery, another feature’s persistence |
| Backend Infrastructure | Application ports, required Domain representations | web, business policy invention |
| Backend Delivery | public Application contracts, delivery conventions | persistence models, direct Domain mutation |
| Backend Bootstrap | public module registrations and concrete adapters | business rules |
| Web Feature | frontend platform, shared presentation, public API contracts | backend source, database, another feature’s private state |
| Web Platform | adapters, shared presentation, public contracts | Industry-specific behavior |
| Web Adapter | public transport contracts, browser runtime | business rules, feature screens |
| Shared package | lower-level public packages only | application-private source |
| Industry Pack | Hospitality Core public contracts | another Industry Pack’s internals |
| Plugin | versioned extension contracts | database, private Feature Pack or core source |
| Root tests | public boundaries and test support | production secrets or private shortcuts |

# 14. Enforcement expectations

When implementation begins, the team should enforce this structure through:

- code review ownership;
- architecture tests for forbidden dependencies;
- public module interfaces;
- restricted import paths;
- no direct database access outside persistence adapters;
- no application imports from migration or test code;
- contract tests across app, Industry Pack, and future plugin boundaries;
- Decision Log review before creating a new shared package or runtime service.

The exact enforcement tools remain subject to the approved technical stack.
