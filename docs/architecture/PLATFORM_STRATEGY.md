# BeachOS Platform Strategy

## Purpose

This document defines the internal platform strategy of BeachOS.

It classifies the product’s existing parts by their architectural purpose and
proposes future platform boundaries. It does not replace the Mission, Product
Philosophy, Operational Intelligence Framework, Domain Model, Decision Log, or
approved software architecture.

This is a strategic classification, not an implementation plan. It introduces
no source structure, API, database design, deployment model, or new business
rule.

## Why Classification Matters

BeachOS is becoming more than a collection of features. Without clear
classification, several forms of confusion become likely:

- product purpose may be treated as software policy;
- Operational Intelligence may start changing business truth;
- a capability may become a dependency of unrelated capabilities;
- shared code may become a hidden generic Domain;
- infrastructure may acquire business decisions;
- a platform may become a large miscellaneous module;
- common vocabulary may expand into a tightly coupled global model.

Classification establishes what each part owns, what it may depend on, and what
it must never decide.

# Classification Model

Every existing part has one **primary classification** in this strategy. A part
may influence or support other classifications, but it must have one clear
architectural purpose.

## Mission

Mission explains why BeachOS exists, what success means, and which values guide
decisions.

Mission governs every other classification but contains no executable business
rules. Product and technical work must be evaluated against it; software must
not depend on Mission documents at runtime.

## Operational Intelligence

Operational Intelligence defines how BeachOS turns confirmed business facts
into readiness, confidence, attention, advice, and honest uncertainty.

It does not own the facts, authorize actions, or create outcomes. It interprets
current facts for a specific human decision while preserving the authority of
the responsible person.

## Capability

A Capability is a coherent business outcome BeachOS enables for a particular
operational purpose.

A Capability owns its commands, business policy, concrete events, user
conversation, and acceptance criteria. It may use Platforms and the Shared
Kernel but must not reach through another Capability’s internal layers.

## Platform

A Platform is a stable internal product boundary that enables several
Capabilities through governed contracts, shared operational mechanics, and
consistent guarantees.

A Platform is not merely code used twice. It exists when multiple Capabilities
need the same durable service and one accountable owner must protect its
contract.

A Platform must not erase concrete business language or become a universal
workflow engine.

## Infrastructure

Infrastructure provides technical adapters and operating environments:
persistence, network delivery, runtime configuration, migrations, containers,
deployment, and automation.

Infrastructure implements inward-facing contracts. It never owns business
meaning, authorization policy, operational advice, or the approved lifecycle of
a Domain concept.

## Shared Kernel

The Shared Kernel is the smallest jointly governed set of stable business
semantics that several Domains must interpret identically.

It is not a general utility library and not a copy of the entire Domain Model.
Every addition creates coordination cost and therefore requires strong evidence
that different Domains cannot safely interpret the concept differently.

## Core Domain

The Core Domain contains the business meaning that makes BeachOS a Hospitality
Operating System: the trusted model of what is happening in the real operation,
what work exists, who is responsible, what money is owed or received, and what
requires attention.

It deserves the strongest product ownership and must not be delegated to a
generic technology model.

## Supporting Domain

A Supporting Domain is necessary for BeachOS operations but does not by itself
define the product’s primary differentiation.

It supports Core Domain decisions and may contain important venue-specific
rules. It should remain explicit rather than being hidden inside configuration
or infrastructure.

## Generic Domain

A Generic Domain solves a common problem that is not distinctive to
hospitality.

BeachOS should use clear internal boundaries and established approaches for
these concerns rather than inventing proprietary business meaning. Generic
Domains still require security, reliability, and ownership.

# Classification of Existing BeachOS Parts

## Repository Governance and Documentation

| Existing part                                                                                           | Primary classification | Why                                                                                                                                                                                             |
| ------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DECISIONS.md`                                                                                          | Mission                | Governs why material choices were made and prevents later work from silently changing approved direction. It contains decisions across categories, but its architectural purpose is governance. |
| `PRODUCT_REQUIREMENTS.md`, MVP Backlog, Sprint Plan, and Implementation Roadmap                         | Capability             | Define concrete outcomes, acceptance expectations, scope, and delivery sequence for business capabilities.                                                                                      |
| `DOMAIN_MODEL.md`, `DOMAIN_EVENTS.md`, and Project Glossary                                             | Core Domain            | Are the authoritative expression of BeachOS business truth and official language. Individual concepts are further classified below.                                                             |
| Product, Domain, glossary, mission, NFC, framework, and implementation review reports                   | Mission                | Provide governance evidence, consistency findings, and review outcomes. They do not own runtime behavior.                                                                                       |
| Engineering Architecture, Application Structure, Technical Foundation, and ADRs                         | Platform               | Define system-wide engineering boundaries and recommended contracts used across capabilities. Infrastructure-specific decisions inside them remain implemented by Infrastructure.               |
| Development Plan and engineering setup documentation                                                    | Platform               | Establish common delivery and repository practices for all capabilities.                                                                                                                        |
| Host Dashboard specification, wireframes, and UX specification                                          | Capability             | Describe the concrete Host experience and its operational decisions rather than a universal UI platform.                                                                                        |
| `framework/03 Roles`                                                                                    | Capability             | Defines executable responsibility in named operational contexts. Role documents do not grant permissions.                                                                                       |
| `framework/04 Workflows`                                                                                | Capability             | Defines approved human operational sequences and outcomes.                                                                                                                                      |
| Empty Framework sections for Playbooks, Coaching, Knowledge, Decision Engine, and Operational Standards | Mission                | Are reserved Operational Framework governance areas, not implemented software modules or accepted automated behavior.                                                                           |
| `README.md`, `CONTRIBUTING.md`, Code of Conduct, Security policy, and bootstrap/setup reports           | Platform               | Govern the shared engineering environment, contribution process, and project operation.                                                                                                         |
| License and repository meta-files                                                                       | Generic Domain         | Provide standard legal and engineering-tool configuration unrelated to hospitality behavior.                                                                                                    |

Review reports inherit the authority of their source documents only when their
findings are approved. A review does not create a business rule by itself.

## Repository Structure

| Existing part                                  | Primary classification | Why                                                                                                                                           |
| ---------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `apps/web`                                     | Platform               | Is the shared delivery shell hosting concrete capability workspaces. Individual workspace modules remain Capabilities.                        |
| `apps/api` application shell                   | Platform               | Hosts composition, delivery, and capability feature packs without owning their Domain policy.                                                 |
| `apps/api/.../venue_opening`                   | Capability             | Contains the concrete Venue Opening vertical slice.                                                                                           |
| `apps/api/.../ordering`                        | Capability             | Contains the concrete Ordering vertical slice.                                                                                                |
| `apps/api/.../kitchen`                         | Capability             | Contains the concrete Kitchen Operations vertical slice.                                                                                      |
| Infrastructure subfolders inside feature packs | Infrastructure         | Implement capability-owned ports through PostgreSQL and other technical adapters. Their location does not give them Domain authority.         |
| `packages/config`                              | Platform               | Is reserved for governed shared engineering configuration.                                                                                    |
| `packages/shared`                              | Shared Kernel          | Is reserved for deliberately approved shared semantics; its existence must not justify adding general utilities or capability policy.         |
| `infrastructure`                               | Infrastructure         | Is reserved for deployment and runtime environment concerns.                                                                                  |
| `scripts`                                      | Platform               | Provides repository-wide engineering and local-development operations. Scripts must not become a hidden business command path.                |
| Root `tests` structure                         | Platform               | Provides cross-capability quality organization. Tests inside a concrete feature remain owned by that Capability.                              |
| `docs`                                         | Mission                | Is the primary governance library for product truth and decisions, although individual documents receive more specific classifications above. |
| `framework`                                    | Mission                | Defines technology-independent operational direction. Individual role and workflow playbooks are classified as Capabilities.                  |
| `ux` and `wireframes`                          | Capability             | Describe concrete approved user journeys and functional interactions.                                                                         |
| `.github`                                      | Infrastructure         | Runs repository automation and quality gates.                                                                                                 |

## Mission

| Existing part                                                                      | Primary classification | Why                                                                                                                                                |
| ---------------------------------------------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MISSION_AND_VALUES.md`                                                            | Mission                | Defines why the company and product exist, the product promise, measures of success, and the decision test.                                        |
| `PRODUCT_VISION.md`                                                                | Mission                | Describes the business destination, target market, long-term direction, and success from the owner’s perspective.                                  |
| `PRODUCT_PHILOSOPHY.md`                                                            | Mission                | Provides timeless principles for deciding what deserves to exist in the product.                                                                   |
| `MASTER_BLUEPRINT.md`                                                              | Mission                | Acts as the enduring product and architectural constitution. Its detailed rules influence other categories, but its primary purpose is governance. |
| Framework Vision and Philosophy material                                           | Mission                | Explains what outstanding hospitality operation should achieve independently of software.                                                          |
| `FRAMEWORK_INTRODUCTION.md`, `FRAMEWORK_PRINCIPLES.md`, and `FRAMEWORK_ROADMAP.md` | Mission                | Establish the Operational Framework’s purpose, principles, and strategic reach across hospitality industries.                                      |

These documents must guide priorities and reviews. They must not become runtime
configuration or be translated directly into automatic system decisions.

## Operational Intelligence

| Existing part                                                 | Primary classification   | Why                                                                                                                                   |
| ------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/framework/OPERATIONAL_INTELLIGENCE.md`                  | Operational Intelligence | Defines the reasoning sequence from decision and facts through readiness, confidence, attention, advice, human decision, and outcome. |
| Operational Readiness presentation in the Host Workspace      | Operational Intelligence | Interprets confirmed department declarations for the Host’s opening decision without replacing the opening rule or Host choice.       |
| Attention Queue behavior in the Host Workspace                | Operational Intelligence | Focuses confirmed operational facts that need awareness; it is not a second source of business truth.                                 |
| Uncertain-outcome guidance in Ordering and Kitchen workspaces | Operational Intelligence | Distinguishes an unknown result from success or failure and directs the person to re-establish current truth.                         |
| Guest Arrival Capability reasoning sections                   | Operational Intelligence | Apply readiness, confidence, attention, blockers, advice, and human decision to the Guest Arrival decision.                           |
| Customer Journey decision structure                           | Operational Intelligence | Frames each journey stage by operational decision and confidence while leaving business outcomes to approved capabilities.            |

Operational Intelligence may consume facts from many Platforms. It must not
write Orders, acknowledge Tickets, open Venues, record Payments, grant
Capabilities, or infer states whose rules are unresolved.

## Capabilities

| Existing part                                                                | Primary classification | Why                                                                                                                                           |
| ---------------------------------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Venue Opening                                                                | Capability             | Enables an authorized Host to open one Venue for one Business Date after approved readiness conditions are satisfied.                         |
| Host Workspace                                                               | Capability             | Enables the Host to understand current opening and operational context and make the next human decision.                                      |
| Guest Arrival                                                                | Capability             | Defines the operation from arrival through the Responsible Service Staff intentionally opening the Customer Group.                            |
| Customer Group Lifecycle                                                     | Capability             | Describes official service from intentional opening through active service and future completion, while preserving unresolved transitions.    |
| Ordering                                                                     | Capability             | Enables an authorized Staff Member to submit one reviewed Order Round and produce approved preparation and financial consequences atomically. |
| Kitchen Operations                                                           | Capability             | Enables Kitchen Staff to view confirmed Kitchen work and intentionally acknowledge it under the currently approved event model.               |
| Venue Opening frontend, Ordering workspace, and Kitchen workspace            | Capability             | These are concrete user experiences for their respective operational outcomes, not general UI platforms.                                      |
| FastAPI Venue Opening, Ordering, and Kitchen delivery routes                 | Capability             | Each route is an external delivery boundary for one concrete application capability.                                                          |
| Capability-specific tests                                                    | Capability             | Verify concrete business language, rules, events, authority, delivery behavior, and recovery.                                                 |
| Host Playbook and Venue Opening, Guest Arrival, and Customer Group workflows | Capability             | Define executable human operations and responsibility for particular outcomes.                                                                |

The Bar capability does not yet exist. The approved Service Operations review is
a platform strategy input, not an implemented Bar capability.

## Current Platform Parts

BeachOS does not yet have fully separated internal Platforms. The following
existing parts already perform platform-like responsibilities and should be
treated as seeds, not as permission to refactor immediately.

| Existing part                                       | Primary classification | Why                                                                                                                                    |
| --------------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| One shared web application shell                    | Platform               | Hosts several capability workspaces on supported device sizes and provides one product entry point. It must not own capability policy. |
| Backend composition root                            | Platform               | Connects capability ports to adapters at the application boundary. It is the governed wiring point, not a business service.            |
| FastAPI application shell and common error envelope | Platform               | Hosts capability delivery adapters and provides consistent delivery behavior without deciding business outcomes.                       |
| Approved Service Operations Architecture            | Platform               | Defines the future shared mechanics boundary for Kitchen and Bar while preserving separate concrete capabilities.                      |
| Modular feature-pack convention                     | Platform               | Provides a stable way to add BeachOS and future industry capabilities without cross-importing internal layers.                         |
| Shared local development and quality commands       | Platform               | Give every capability a consistent engineering path for build, lint, type checking, testing, and packaging.                            |

The current application shell is intentionally small. Navigation does not make
the web application the owner of Host, Ordering, or Kitchen behavior.

## Infrastructure

| Existing part                                                 | Primary classification | Why                                                                                                                                         |
| ------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| PostgreSQL 17 persistence                                     | Infrastructure         | Stores authoritative state, event streams, reports, receipts, and history through explicit adapters. PostgreSQL does not define the Domain. |
| Psycopg adapters                                              | Infrastructure         | Translate persistence records to and from Domain and Application contracts. Psycopg types stay outside inner layers.                        |
| Versioned SQL migrations                                      | Infrastructure         | Evolve storage structures and preserve committed history. They must not contain Domain behavior.                                            |
| Unit of Work implementations                                  | Infrastructure         | Provide transaction boundaries and rollback for application operations. They do not decide what a valid business transaction means.         |
| Event serialization mappings                                  | Infrastructure         | Preserve concrete Domain Events in storage without owning their meaning or allowed sequence.                                                |
| Optimistic concurrency storage checks                         | Infrastructure         | Enforce expected event-stream versions as a technical integrity guarantee. Aggregate invariants remain in the Domain.                       |
| Append-only database protections                              | Infrastructure         | Prevent technical rewriting of permanent history. The Domain determines which facts require permanence.                                     |
| Command receipt storage                                       | Infrastructure         | Supports safe repetition of consequential commands. It does not decide whether an action is authorized or valid.                            |
| `infrastructure/docker` and deployment placeholders           | Infrastructure         | Belong to runtime and deployment concerns, not product behavior.                                                                            |
| `.github` workflows                                           | Infrastructure         | Automate quality gates and build verification. They do not change acceptance criteria.                                                      |
| Environment-variable handling                                 | Infrastructure         | Supplies deployment-specific configuration through controlled boundaries.                                                                   |
| Vite, React runtime, FastAPI runtime, and server entry points | Infrastructure         | Execute delivery experiences and APIs. Frameworks remain replaceable.                                                                       |
| Root and capability test database setup                       | Infrastructure         | Provides isolated verification against PostgreSQL without becoming production business state.                                               |

## Shared Kernel

The current repository has an authoritative vocabulary but does not yet have a
formal Shared Kernel package. The strategy classifies the following semantics as
Shared Kernel candidates because several Domains must interpret them
identically.

| Existing semantic                                                                                                           | Primary classification | Why                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stable identities for Organization, Venue, Service Location, Customer Group, Staff Member, Order, Ticket, Bill, and Payment | Shared Kernel          | Cross-Domain references are unsafe if identity meaning changes by capability. The Shared Kernel owns identity semantics, not aggregate behavior.                                             |
| Venue scope                                                                                                                 | Shared Kernel          | Every operational and authorization boundary must agree which Venue a fact belongs to.                                                                                                       |
| Business Date                                                                                                               | Shared Kernel          | Venue Opening, operations, reporting, shifts, and financial views must refer to the same operational date meaning.                                                                           |
| Exact Money value and Currency identity                                                                                     | Shared Kernel          | Ordering, Billing, and Payments must agree on exact amount and currency semantics. Financial rules remain in Financial Operations.                                                           |
| Capability identity                                                                                                         | Shared Kernel          | Authorization requests need one stable name for an approved action. Permission policy and assignment do not belong in the kernel.                                                            |
| Actor identity and occurred-at time semantics                                                                               | Shared Kernel          | Permanent events across Domains must consistently identify who acted and when the fact occurred.                                                                                             |
| Domain Event envelope semantics                                                                                             | Shared Kernel          | Event identity, aggregate identity, version, occurrence time, and correlation meaning must be consistent across event-sourced Domains. Concrete event payloads remain owned by capabilities. |
| Official project vocabulary and glossary governance                                                                         | Shared Kernel          | One concept must keep one official name across Product, Design, Engineering, Testing, and AI collaboration.                                                                                  |

The Shared Kernel must not contain:

- Customer Group lifecycle policy;
- Venue opening rules;
- Order submission rules;
- Kitchen or Bar Ticket states;
- Bill closing rules;
- Payment acceptance rules;
- Role-to-Capability policy;
- operational attention or advice;
- framework, database, or delivery types.

## Core Domain

The Core Domain is the connected operational model that fulfills BeachOS’s
mission of being a trusted mirror of real hospitality.

| Existing Domain part                         | Primary classification | Why                                                                                                                                   |
| -------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Customer Group                               | Core Domain            | It is the primary operational entity and owns the connected history of location, responsibility, Orders, Bill, Payments, and service. |
| Service Location and its Digital Identity    | Core Domain            | Connect the physical venue to trusted digital context without making the business dependent on NFC or another technology.             |
| Responsible Service Staff                    | Core Domain            | Makes current human responsibility explicit and supports handovers without confusing Role with authority.                             |
| Order and Order Round                        | Core Domain            | Preserve each confirmed customer request and its operational and financial consequences.                                              |
| Order Item                                   | Core Domain            | Preserves the exact confirmed item, quantity, price, destination, and instruction accepted by the business.                           |
| Kitchen Ticket and Bar Ticket                | Core Domain            | Represent confirmed department-specific service work connected to the guest, location, Order, and responsible service team.           |
| Financial Obligation                         | Core Domain            | Explains why the Customer Group owes an exact amount and connects service actions to financial truth.                                 |
| Bill and Bill Line                           | Core Domain            | Maintain one explainable running financial view of the Customer Group without rewriting history.                                      |
| Payment                                      | Core Domain            | Represents confirmed value received and protects owner confidence in the financial mirror.                                            |
| Domain Events for the above concepts         | Core Domain            | Preserve meaningful business facts and make current state, history, and uncertainty explainable.                                      |
| Movement of a Customer Group and its context | Core Domain            | Keeps physical and digital operations aligned when service moves between locations.                                                   |
| Responsibility handover                      | Core Domain            | Preserves service continuity and accountability as staff responsibility changes.                                                      |

Core Domain behavior must remain explicit and concrete. Platform reuse may
support it but must never generalize away its hospitality meaning.

## Supporting Domain

| Existing Domain part                            | Primary classification | Why                                                                                                                            |
| ----------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Organization                                    | Supporting Domain      | Establishes commercial ownership and multi-venue scope but is not the live service operation itself.                           |
| Venue                                           | Supporting Domain      | Provides the operational boundary and context in which Core Domain work occurs.                                                |
| Area                                            | Supporting Domain      | Describes stable physical layout needed to understand Service Locations.                                                       |
| Zone and Zone Template                          | Supporting Domain      | Support daily operational grouping and staffing without changing Service Location identity.                                    |
| Operational Department                          | Supporting Domain      | Establishes departmental responsibility used by Venue Opening and later operational coordination.                              |
| Opening Report                                  | Supporting Domain      | Preserves daily readiness and official opening history that enables safe service.                                              |
| Staff Member                                    | Supporting Domain      | Represents a person who performs work; concrete operational responsibility belongs to capabilities.                            |
| Role                                            | Supporting Domain      | Groups business responsibilities without granting authority by itself.                                                         |
| Shift                                           | Supporting Domain      | Provides the work-period context for staffing and handover.                                                                    |
| Menu, Menu Category, and Menu Item              | Supporting Domain      | Define current offerings, prices, and destinations used by Ordering, while submitted Order Items preserve Core Domain history. |
| Payment Method                                  | Supporting Domain      | Describes the approved way value may be received. Payment confirmation remains Core Domain behavior.                           |
| Activity Log                                    | Supporting Domain      | Provides operational accountability around sensitive actions without replacing Domain history.                                 |
| Venue Opening rules and department declarations | Supporting Domain      | Enable safe operation but support rather than define the full guest-service value stream.                                      |

Supporting does not mean unimportant. These Domains require clear ownership and
may contain significant business rules.

## Generic Domain

| Existing part                                                    | Primary classification | Why                                                                                                                                |
| ---------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Temporary development identity provider                          | Generic Domain         | Identity resolution is a common software concern. The fake adapter is explicitly temporary and not production authentication.      |
| Future authentication and session management boundary            | Generic Domain         | Verifies who is using the system; it is not distinctive hospitality behavior.                                                      |
| Technical authorization evaluation mechanism                     | Generic Domain         | Evaluating granted capabilities and Venue access is common. The business names and requirements of capabilities remain outside it. |
| Health endpoint                                                  | Generic Domain         | Reports technical service availability and carries no hospitality meaning.                                                         |
| Technical logging and observability                              | Generic Domain         | Support operation of software rather than Venue operations.                                                                        |
| Notification delivery mechanisms                                 | Generic Domain         | Deliver messages through channels. Business rules decide whether a notification is warranted.                                      |
| Generic report rendering and export                              | Generic Domain         | Format and distribute approved read models without owning their business interpretation.                                           |
| CI tooling, linting, formatting, type checking, and test runners | Generic Domain         | Standard engineering capabilities that support quality but do not distinguish BeachOS.                                             |

# Current Dependency Direction

The strategic dependency direction is:

```text
Mission
  governs all decisions

Core and Supporting Domains
  define business truth

Capabilities
  perform approved business outcomes

Operational Intelligence
  interprets confirmed facts for human decisions

Platforms
  enable multiple capabilities through stable contracts

Infrastructure
  implements technical ports and runtime concerns
```

This is a direction of authority, not a proposed source-code graph.

The Shared Kernel may be used by Core, Supporting, and Generic Domains only for
the small stable semantics explicitly governed as shared.

# Future Platform Portfolio

Future Platforms should be created only when several approved Capabilities need
one durable contract and accountable ownership. A future Platform is not
automatically a separate deployable service.

## Guest Operations Platform

### Purpose

Provide stable operational coordination around a guest party from arrival
through active service and departure, centered on the Customer Group.

### Ownership

Owns shared operational contracts for:

- Customer Group identity and current lifecycle context;
- current and historical Service Location association;
- Responsible Service Staff and handover context;
- guest-facing journey continuity;
- safe movement of the whole Customer Group;
- current service context required by authorized capabilities.

It does not own Orders, preparation policy, Bills, Payments, identity, or
notifications.

### Dependencies

- Venue Operations for authoritative Venue and Service Location context.
- Identity Platform for actor and capability evaluation.
- Shared Kernel for stable identities, Venue scope, and event envelope
  semantics.

Ordering, Service Operations, and Financial Operations may reference the
Customer Group through published contracts and facts.

### Allowed Coupling

- Capabilities may request current Customer Group context through an owned
  contract.
- Guest Operations may publish concrete Customer Group and responsibility
  events.
- Read models may combine Guest Operations facts with other Platform facts
  outside authoritative write models.

### Shared Mechanics

- Customer Group context lookup;
- occupancy integrity;
- location-history preservation;
- responsibility-history preservation;
- idempotent transfer and handover command mechanics;
- current versus submission-context distinction.

### Forbidden Coupling

- Direct access to Ordering, Kitchen, Bar, Bill, or Payment persistence.
- Deciding preparation status or financial balance.
- Treating physical identification as authorization or an operational action.
- Allowing another Platform to rewrite Customer Group history.

## Service Operations Platform

### Purpose

Provide shared mechanics for concrete preparation and fulfillment capabilities
while preserving Kitchen and Bar as separate business capabilities.

### Ownership

Owns:

- confirmed work-source contracts;
- event-stream and acknowledgement mechanics proven common across service
  departments;
- current versus original location context for delivery awareness;
- safe command receipt and concurrency contracts;
- infrastructure contract tests for concrete service capabilities.

Concrete Kitchen and Bar modules own their events, commands, capabilities,
workspaces, advice, and future preparation rules.

### Dependencies

- Ordering for concrete Ticket Created facts.
- Guest Operations for current Customer Group location and responsible service
  context.
- Identity Platform for concrete capability evaluation.
- Shared Kernel for identity, Venue scope, actor, time, and event semantics.

### Allowed Coupling

- Concrete service capabilities may implement narrow Service Operations
  contracts.
- Service Operations may replay explicitly registered concrete events.
- Operational Intelligence may consume read-only service facts.

### Shared Mechanics

- source Ticket reconstruction;
- append-only event handling;
- optimistic concurrency;
- idempotent operational command receipts;
- transaction boundaries;
- confirmed, rejected, and uncertain result handling;
- reusable infrastructure contract tests.

### Forbidden Coupling

- One generic preparation aggregate replacing Kitchen Ticket and Bar Ticket.
- One generic capability authorizing all service work.
- Shared readiness, completion, priority, delay, station, cancellation,
  delivery, or handoff policy without approved identical rules.
- Kitchen importing Bar, Bar importing Kitchen, or the Platform importing
  concrete capability internals.

## Financial Operations Platform

### Purpose

Provide one trusted financial context for each Customer Group from the first
Financial Obligation through Payments and approved closing.

### Ownership

Owns shared contracts and integrity for:

- Financial Obligations;
- Bill identity and lifecycle;
- Bill Lines and their business origins;
- balance;
- Payments and Payment Method references;
- exact money;
- financial event history;
- closing eligibility once rules are approved.

It does not own Order acceptance, preparation work, sunbed occupancy, or
external accounting interpretation.

### Dependencies

- Guest Operations for Customer Group identity.
- Ordering and other charge-producing capabilities for approved Financial
  Obligation facts.
- Identity Platform for financial capabilities.
- Audit Platform for sensitive action accountability.
- Shared Kernel for Money, Currency, identity, Venue scope, actor, and time.

### Allowed Coupling

- Capabilities may request creation of an approved Financial Obligation through
  explicit contracts.
- Financial Operations may reference immutable source fact identities.
- Reporting may consume financial projections without writing them.

### Shared Mechanics

- exact arithmetic;
- one-Bill-per-Customer-Group integrity under current rules;
- source-to-Bill-Line traceability;
- payment idempotency;
- immutable financial history;
- balance calculation;
- transaction and concurrency guarantees.

### Forbidden Coupling

- Reading another Capability’s tables to infer a charge.
- Letting a Platform invent a price, discount, correction, refund, closing, or
  overpayment rule.
- Allowing reporting or accounting export to rewrite operational financial
  truth.
- Treating a payment attempt as a confirmed Payment.

## Venue Operations Platform

### Purpose

Provide stable Venue, physical layout, daily operational structure, and Business
Date context for all Venue-scoped capabilities.

### Ownership

Owns shared contracts for:

- Organization and Venue scope;
- Business Date;
- Area;
- Service Location and Digital Identity;
- dynamic Zone membership and future Zone Templates;
- Operational Departments;
- official Venue Opening context and Opening Reports.

Venue Opening remains a concrete Capability using this Platform.

### Dependencies

- Identity Platform for management and opening capabilities.
- Shared Kernel for identities, Venue scope, Business Date, actor, time, and
  event semantics.
- Audit Platform for sensitive configuration and opening actions.

### Allowed Coupling

- Other Platforms may obtain authoritative Venue, Business Date, and Service
  Location context through stable contracts.
- Venue Operations may publish location, Zone, and opening facts.
- Operational Intelligence may interpret confirmed readiness declarations.

### Shared Mechanics

- Venue-scoped lookup;
- stable Service Location Digital Identity resolution;
- physical versus dynamic grouping distinction;
- Business Date resolution;
- immutable Opening Report history;
- multi-venue isolation.

### Forbidden Coupling

- NFC, QR, or another technology becoming the Service Location identity itself.
- Zone membership changing Service Location identity or historical context.
- Venue Operations opening Customer Groups, submitting Orders, or creating
  financial effects.
- Another Platform maintaining its own conflicting Business Date.

## Identity Platform

### Purpose

Establish who is acting, which Venue scope applies, and which concrete
Capabilities have been granted.

### Ownership

Owns:

- authentication;
- session identity;
- actor identity resolution;
- Venue access;
- grants of concrete Capability identities;
- revocation and session-expiry behavior;
- secure identity evidence.

Roles remain business responsibility groupings. A Role must not directly become
permission logic.

### Dependencies

- Shared Kernel for Staff Member, Venue, Role, and Capability identities.
- Audit Platform for sensitive identity and grant changes.

It must not depend on operational Capability internals.

### Allowed Coupling

- Applications may ask whether an actor holds a named capability in a named
  scope.
- Capabilities own the meaning of the action being authorized.
- Identity may consume approved staff and role assignments.

### Shared Mechanics

- authentication protocols;
- session lifecycle;
- capability grant evaluation;
- Venue-scope checks;
- revocation;
- secure development and test identities.

### Forbidden Coupling

- Role name automatically granting an action.
- Identity deciding business preconditions.
- NFC location identification authenticating a person.
- Capability code reading identity storage directly.
- A generic “manager override” bypassing Domain rules.

## Notification Platform

### Purpose

Deliver approved operational messages reliably through future supported
channels.

### Ownership

Owns:

- delivery channel contracts;
- recipient addressing;
- delivery attempts and outcomes;
- channel availability;
- duplicate-delivery protection;
- permitted message templates and language delivery.

It does not decide that a business condition deserves a notification.

### Dependencies

- Concrete Capabilities or Operational Intelligence for an approved
  notification request.
- Identity Platform for authorized recipients and contact destinations.
- Shared Kernel for identity, Venue scope, correlation, and time.

### Allowed Coupling

- Subscribe to approved published facts or explicit notification requests.
- Report delivery success, failure, or uncertainty.
- Apply channel-specific delivery policy.

### Shared Mechanics

- channel abstraction;
- retries where safe;
- deduplication;
- delivery status;
- recipient preferences where approved;
- operational language templates.

### Forbidden Coupling

- Inferring urgency from raw database records.
- Turning every event into a notification.
- Notifications becoming the source of operational truth.
- Writing back a business status because a message was delivered.
- Exposing sensitive information through an unsuitable channel.

## Reporting Platform

### Purpose

Provide trustworthy historical and current read views for owners, managers, and
authorized operational users.

### Ownership

Owns:

- read-model contracts;
- metric definitions after business approval;
- report composition;
- time and Venue scoping;
- export and presentation of confirmed facts;
- freshness and completeness disclosure.

It does not own the source business facts.

### Dependencies

- Published facts and approved read contracts from operational Platforms.
- Identity Platform for access.
- Shared Kernel for Venue, Business Date, identity, Money, and time semantics.

### Allowed Coupling

- Build projections from concrete events.
- Join read-only facts across Platforms.
- State data freshness and uncertainty.
- Produce operational and management views without becoming a command path.

### Shared Mechanics

- projection;
- aggregation;
- date and Venue filtering;
- metric versioning;
- export;
- freshness and reconciliation checks.

### Forbidden Coupling

- Directly changing source operational state.
- Defining a metric without business ownership.
- Hiding missing or stale source facts.
- Reconstructing financial truth differently from Financial Operations.
- Using reports as an authorization mechanism.

## Audit Platform

### Purpose

Provide accountable, immutable records for sensitive actions and exceptional
changes while preserving the distinction between an Activity Log and Domain
history.

### Ownership

Owns:

- Activity Log recording contracts;
- actor, action, scope, reason, and occurrence context;
- append-only protection;
- authorized audit search;
- retention and access policy when approved.

Concrete Domains own their Domain Events. Audit records explain accountability;
they do not replace aggregate event streams.

### Dependencies

- Shared Kernel for actor, Venue, subject identity, correlation, and time.
- Identity Platform for authorized audit access.
- Concrete Capabilities for explicit accountability-relevant actions.

### Allowed Coupling

- Receive audit records in the same transaction when atomicity is required.
- Reference concrete Domain fact identities.
- Supply read-only history to authorized operational and reporting views.

### Shared Mechanics

- immutable append;
- correlation;
- actor and subject context;
- reason capture where required;
- protected search;
- retention enforcement.

### Forbidden Coupling

- Reconstructing aggregate state from Activity Logs.
- Logging every interaction without a legitimate purpose.
- Treating audit as staff surveillance.
- Allowing audit failure to be ignored when the business requires atomic
  accountability.
- Editing history to make current operations look better.

# Platform Ownership Rules

## One Accountable Owner

Each Platform requires one accountable product and engineering ownership group.
Several teams may contribute, but one owner protects the contract, terminology,
quality, and change process.

## Consumers Do Not Control the Platform

A Capability may request a Platform change but must not add a special case that
silently changes behavior for other consumers.

## Contracts Before Sharing

Sharing begins with an explicit business or application contract. Direct table
access, internal class imports, and shared mutable records are not Platform
contracts.

## Platforms Publish Facts, Not Instructions

Published Domain Events describe what happened. Consumers decide what those
facts mean inside their own approved policies. One Platform must not command
another Platform’s aggregate by writing its storage.

## Operational Intelligence Is a Consumer

Operational Intelligence may combine confirmed facts and express readiness,
confidence, attention, and advice. It remains read-oriented unless an
authorized human intentionally invokes a concrete Capability.

## Infrastructure Remains Replaceable

A Platform contract must not expose PostgreSQL rows, Psycopg connections, HTTP
framework types, React components, environment variables, or deployment
objects.

# Allowed Dependency Rules

1. Mission governs all classifications but has no runtime dependencies.
2. Capabilities may depend on their own Core or Supporting Domain behavior.
3. Capabilities may use Platform contracts and the Shared Kernel.
4. Platforms may depend on the Shared Kernel and their owned Domain concepts.
5. Platforms must not depend on concrete consumer Capabilities.
6. Infrastructure may depend inward to implement ports.
7. Domain layers must not depend on Application, Infrastructure, delivery, or
   frontend layers.
8. Operational Intelligence may consume read-only contracts and confirmed
   facts.
9. Reporting and Notification may consume published facts but must not mutate
   source Domains.
10. Generic Domains must remain isolated behind contracts and must not define
    hospitality behavior.

# Forbidden Coupling Across BeachOS

The following coupling is forbidden:

- cross-Capability database table access as a business integration contract;
- one Capability importing another Capability’s Domain internals;
- shared UI state becoming authoritative business state;
- a Platform owning a universal workflow status model;
- generic Role checks replacing concrete Capability verification;
- notifications, reports, audit records, caches, or projections becoming the
  source of truth;
- duplicated definitions of identity, Business Date, Money, Currency, or event
  version semantics;
- infrastructure exceptions leaking into Domain behavior;
- technical availability being treated as operational readiness;
- hidden synchronous dependency chains across several Platforms for one common
  staff action;
- automatic business action triggered solely by NFC or another identifier;
- a shared abstraction that introduces an unapproved business rule.

# Shared Mechanics Strategy

Mechanics may be shared when all of the following are true:

1. At least two concrete consumers demonstrate the same need.
2. The business meaning is identical, not merely similar.
3. The abstraction can be named without hiding concrete Domain language.
4. Each consumer retains its own events, commands, capabilities, and policies
   where those are business-specific.
5. The shared contract can be tested independently.
6. A consumer can evolve separately when future approved rules diverge.
7. The shared mechanism does not require direct access to another consumer’s
   persistence.

Good candidates include:

- identity and scope semantics;
- exact time and Money semantics;
- event envelope and expected-version mechanics;
- idempotent command receipt mechanics;
- transaction contracts;
- uncertainty result handling;
- append-only history protection;
- read-model freshness disclosure;
- contract-test suites.

Poor candidates include:

- preparation status;
- Customer Group lifecycle;
- Venue opening policy;
- transfer policy;
- financial correction rules;
- notification urgency;
- operational priority;
- completion conditions;
- human advice.

# Platform Evolution Principles

## Extract From Evidence

Do not create a Platform from a single Capability. Use concrete implementations
and approved business behavior to prove the shared boundary.

## Keep Platforms Smaller Than Their Consumers

If a Platform contains most of the business behavior of its consumers, the
boundary is probably hiding a Core Domain rather than enabling Capabilities.

## Prefer Stable Contracts Over Shared Storage

Shared storage creates accidental ownership. Stable contracts and published
facts allow each Platform to protect its invariants.

## Preserve Concrete Language

Internal reuse must not force staff, owners, designers, or Domain documents to
use technical generic terms.

## Make Uncertainty Part of Every Contract

Consequential operations must distinguish confirmed success, confirmed
rejection, and unknown outcome. A Platform must not create false confidence for
its consumers.

## Keep Multi-Venue Scope Explicit

Every operational Platform contract must identify Venue scope. Cross-venue
access or aggregation must be intentional and authorized.

## Avoid Premature Deployment Boundaries

A Platform is an ownership and contract boundary first. It does not require a
separate network service. The approved modular monolith remains valid until a
separate deployment has a proven operational reason.

# Recommended Platform Sequence

This is a strategic order, not a development roadmap:

1. **Venue Operations foundation** — because all work requires stable Venue,
   Business Date, and Service Location context.
2. **Guest Operations foundation** — because the Customer Group is the primary
   operational entity.
3. **Service Operations extraction** — after Kitchen and Bar concrete designs
   prove shared mechanics.
4. **Financial Operations boundary** — before expanding Billing and Payments,
   because financial truth requires one governed owner.
5. **Identity Platform** — before production authorization replaces temporary
   identity.
6. **Audit Platform** — as sensitive capabilities expand beyond the current
   Activity Log adapter.
7. **Reporting Platform** — after source Domains and metric definitions are
   sufficiently stable.
8. **Notification Platform** — only after approved operational reasons for
   interruption exist.

This order does not authorize implementation and does not override the approved
development plan.

# Final Position

BeachOS should grow as a system of:

- one enduring Mission;
- one governed Operational Intelligence model;
- concrete hospitality Capabilities;
- a small number of accountable internal Platforms;
- replaceable Infrastructure;
- a deliberately tiny Shared Kernel;
- protected Core Domains;
- explicit Supporting Domains;
- isolated Generic Domains.

The Platform strategy must reduce repeated mechanics without centralizing
business decisions. BeachOS’s Core Domain remains the trusted connection among
the real guest operation, physical location, responsible people, service work,
financial truth, and permanent history.

Platforms exist to protect that truth at scale. They must never redefine it.
