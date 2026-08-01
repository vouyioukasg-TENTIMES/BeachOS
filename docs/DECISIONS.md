# Decision Log

This file is the permanent decision log for Emerald Management System. It records important product, business, user-experience, architecture, security, and technical decisions, together with the reasons behind them.

Its purpose is to help every future project owner, developer, designer, operator, and AI agent understand not only **what** was decided, but also **why** it was decided, which alternatives were considered, and what consequences followed.

Important decisions should be recorded here before implementation whenever possible. When an urgent decision must be made during implementation or live operation, it should be recorded as soon as practical afterward.

This log complements the project’s requirements, vision, blueprint, architecture, and development plan. Those documents describe the product and its direction; this file preserves the history and reasoning of material choices.

## Decision Template

Copy this template for each new decision:

### DEC-XXX — Short decision title

- **Decision ID:** DEC-XXX
- **Date:** YYYY-MM-DD
- **Status:** Proposed / Accepted / Rejected / Superseded
- **Category:** One or more categories from the list below
- **Decision:** A short, unambiguous statement of what is being decided.
- **Context:** The problem, need, constraints, and relevant facts at the time of the decision.
- **Alternatives Considered:** The realistic options considered, including “do nothing” where relevant.
- **Why this option was selected:** The reasoning, evidence, and trade-offs that led to this choice.
- **Consequences:** Expected benefits, costs, risks, limitations, and follow-up work.
- **Future Review Date:** Optional. Use YYYY-MM-DD or name a clear review event.

If a decision is rejected or superseded, its status changes but its original content remains. A replacement decision must receive a new Decision ID and link back to the earlier entry.

## Categories

Use one or more of these categories for every decision:

- **Product** — product direction, scope, users, or capabilities.
- **Architecture** — overall system structure and component boundaries.
- **Database** — data models, storage, history, and data lifecycle.
- **Security** — identity, permissions, privacy, protection, and audit controls.
- **Performance** — response times, capacity, reliability, and resilience.
- **UX** — user journeys, usability, accessibility, and interaction behaviour.
- **UI** — visual language, layouts, controls, and device presentation.
- **Infrastructure** — hosting, networks, environments, monitoring, and backups.
- **AI Workflow** — authorised AI use, review requirements, and collaboration practices.
- **Coding Standards** — source structure, naming, quality rules, and dependencies.
- **Business Rules** — operational or financial rules applied by the product.
- **Integrations** — external systems, providers, devices, and data exchange.
- **Deployment** — release, migration, rollback, and production-change practices.
- **Reporting** — business reports, measures, exports, and analysis.

New categories may be added when no existing category describes a decision clearly. Avoid creating near-duplicate categories.

## Initial Decisions

### DEC-001 — Design for a multi-venue future

- **Decision ID:** DEC-001
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Architecture
- **Decision:** Emerald Management System will be designed to grow into a multi-venue platform, while the first release will serve one venue.
- **Context:** The immediate need comes from one beach club, but the product vision includes other beach bars, pool clubs, resorts, and hospitality groups. Ignoring venue boundaries at the beginning could make later expansion costly or unsafe. Building full multi-venue administration immediately would add unnecessary complexity before the core operation is proven.
- **Alternatives Considered:** Build permanently for one venue; build complete multi-venue functionality in the first release; design clear venue ownership now but delay multi-venue features.
- **Why this option was selected:** Clear venue ownership preserves a practical path to growth without forcing the first release to carry features that have not yet been validated.
- **Consequences:** Core business records must have explicit venue ownership where appropriate. Access and data isolation must be designed with future venues in mind. Cross-venue administration, billing, and reporting remain future work and are not automatically part of the first release.
- **Future Review Date:** Before onboarding a second venue.

### DEC-002 — Emerald Beach Club is the first client, not the product boundary

- **Decision ID:** DEC-002
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Business Rules
- **Decision:** Emerald Beach Club in Loutraki is the first client and learning partner. Its current operation will shape the first release, but client-specific behaviour must not silently become a permanent universal product rule.
- **Context:** The product begins with a real venue and must solve its needs well. Some needs will be common to the market, while others may be unique to Emerald Beach Club.
- **Alternatives Considered:** Treat the system as custom software only for Emerald Beach Club; generalise every feature before real use; distinguish universal domain rules from venue configuration as the product evolves.
- **Why this option was selected:** Starting from real operations reduces speculation, while keeping product and client concepts separate supports future customers and avoids hard-coded assumptions.
- **Consequences:** Requirements should identify whether a rule is universal, configurable by venue, or unique to a specific integration. Generalisation must be earned through evidence rather than guessed in advance.
- **Future Review Date:** After the first live pilot and before offering the product to another venue.

### DEC-003 — Use a mobile-first responsive web application

- **Decision ID:** DEC-003
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Architecture, UX, UI
- **Decision:** The primary staff product will be a mobile-first responsive web application.
- **Context:** Waiters need to work while moving around the beach and pool, while bar staff, kitchen staff, cashiers, and managers may use tablets or desktop computers. The system must support different screen sizes without creating separate experiences that drift apart.
- **Alternatives Considered:** Separate native mobile applications; a desktop-only application; separate mobile and desktop websites; one responsive web application.
- **Why this option was selected:** A responsive web application can support the required devices from one delivery model, reduces installation effort, and allows rapid updates. Mobile-first design prioritises the most constrained and time-sensitive working environment.
- **Consequences:** All important workflows must be designed and tested first for handheld touch use, then adapted for larger screens. Browser and device support must be explicitly agreed. Native-device features or full offline use may require later additions.
- **Future Review Date:** After device and venue connectivity testing.

### DEC-004 — Maintain one codebase for supported devices and roles

- **Decision ID:** DEC-004
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Architecture, Coding Standards, UX
- **Decision:** Phones, tablets, desktop computers, and role-specific views will use one shared application codebase for the initial product.
- **Context:** The application needs different layouts and workflows for waiters, bar staff, kitchen staff, cashiers, and managers. Separate applications would duplicate business logic and increase the chance that behaviour becomes inconsistent.
- **Alternatives Considered:** A separate application for every device type; separate applications for each staff role; one shared application with responsive layouts and permission-based views.
- **Why this option was selected:** One codebase keeps domain rules, security fixes, interface patterns, and releases consistent while still allowing focused screens for each role.
- **Consequences:** The application must have clear internal modules and avoid a single overcrowded interface. Device-specific behaviour is allowed when necessary, but business rules must remain shared and server-enforced.
- **Future Review Date:** If a device or role develops requirements that the shared application cannot meet safely or effectively.

### DEC-005 — Begin with a modular single application

- **Decision ID:** DEC-005
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Architecture, Deployment, Performance
- **Decision:** The initial system will be built as one well-organised application with clear business-module boundaries, rather than as multiple independent services.
- **Context:** The first version has one product team, one first venue, and closely connected operations involving orders, tickets, bills, transfers, and payments. Independent services would create additional deployment, networking, monitoring, and data-consistency work.
- **Alternatives Considered:** Microservices from the beginning; several separately deployed applications; a modular single application with explicit internal boundaries.
- **Why this option was selected:** A modular single application is easier to build, operate, test, and change while the domain is still being learned. Clear boundaries preserve the ability to separate a module later if measured needs justify it.
- **Consequences:** Modules must not become tightly tangled. Service separation will occur only for demonstrated scale, reliability isolation, deployment independence, or team ownership needs—not for fashion.
- **Future Review Date:** When measured load or organisational growth shows the current structure no longer meets agreed targets.

### DEC-006 — Use PostgreSQL as the initial relational database

- **Decision ID:** DEC-006
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Database, Architecture
- **Decision:** PostgreSQL will be the initial central relational database.
- **Context:** The product contains strongly related records and strict rules involving locations, customer groups, orders, bills, payments, users, and audit history. Important operations must succeed completely or leave the system unchanged.
- **Alternatives Considered:** PostgreSQL; another relational database; a document database; local device storage as the main record; multiple databases from the beginning.
- **Why this option was selected:** PostgreSQL offers mature transactions, constraints, exact numeric handling, indexing, and relational integrity suited to operational and financial records. It is widely supported and provides a strong growth path.
- **Consequences:** Data models and migrations will use relational design and database constraints for essential invariants. The team must operate backups, restoration, monitoring, and safe schema changes. Additional data stores require a separate accepted decision.
- **Future Review Date:** Only if a demonstrated requirement cannot be met responsibly with PostgreSQL.

### DEC-007 — The central system is the source of truth

- **Decision ID:** DEC-007
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Architecture, Database, Business Rules
- **Decision:** The central application and database are the official source of operational and financial truth; individual devices are not.
- **Context:** Multiple staff members will work at the same time from different devices. Device-only or disconnected records could create conflicting locations, missed tickets, and inconsistent bills.
- **Alternatives Considered:** Device-local records with occasional synchronisation; a local spreadsheet or paper record as the official source; one central authoritative system with device caches only for presentation or controlled resilience.
- **Why this option was selected:** One source of truth gives all authorised roles the same state and allows critical business rules to be enforced consistently.
- **Consequences:** The first version depends on dependable connectivity to the central system. Cached information cannot silently override central records. Any future offline mode must include a separately approved conflict and synchronisation design.
- **Future Review Date:** After venue-wide connectivity testing or before approving offline operation.

### DEC-008 — Never falsely confirm or silently lose an order

- **Decision ID:** DEC-008
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Performance, UX, Business Rules
- **Decision:** The system must never show an order as successfully sent until it has been durably recorded, and it must protect submitted orders from silent loss or accidental duplication.
- **Context:** A lost or duplicated order damages guest service, creates waste, and undermines staff trust. Outdoor connectivity and repeated taps make this a realistic risk.
- **Alternatives Considered:** Optimistically show success before saving; rely on staff to notice failures; confirm only after safe storage and make submissions safe to retry.
- **Why this option was selected:** Operational trust is more important than making an uncertain action appear faster. Clear save state and safe retries protect both staff and customers.
- **Consequences:** Order submission must be durable, transactional where required, uniquely identifiable, and idempotent. The interface must clearly distinguish draft, sending, sent, and failed states. Failure testing is mandatory.
- **Future Review Date:** Review after pilot incidents and whenever order-delivery architecture changes.

### DEC-009 — Never silently lose or rewrite financial data

- **Decision ID:** DEC-009
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Database, Security, Business Rules
- **Decision:** Financial records must be durable, exact, traceable, and protected from silent deletion or historical rewriting.
- **Context:** Bills, charges, adjustments, and payments affect customer trust, daily reconciliation, and possible legal or accounting obligations. Later menu or row-price changes must not change old bills.
- **Alternatives Considered:** Recalculate old bills from current prices; allow authorised users to edit or delete records in place; preserve priced snapshots and record corrections as new traceable actions.
- **Why this option was selected:** Historical truth and explainable corrections are essential for reliable business operation and accountability.
- **Consequences:** Money uses exact currency units. Applied prices are stored as snapshots. Important financial changes use adjustments, reversals, or new history rather than destructive edits. Backups and tested restoration are required before live use.
- **Future Review Date:** Before adding fiscal, accounting, or payment-provider integrations.

### DEC-010 — Audit every sensitive action

- **Decision ID:** DEC-010
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Security, Database, Reporting
- **Decision:** Every sensitive action must create an activity record that identifies who acted, what changed, when it happened, and relevant previous and new values.
- **Context:** Transfers, responsible-waiter changes, cancellations, corrections, discounts, price changes, payments, role changes, and bill reopening can affect money or accountability. Without history, disputes and mistakes are difficult to resolve.
- **Alternatives Considered:** Log only technical errors; keep limited latest-change information; maintain an append-only business activity history for sensitive events.
- **Why this option was selected:** A clear history protects staff, owners, customers, and the integrity of the system. It supports support investigations and useful management reporting.
- **Consequences:** Sensitive-event definitions must be maintained. Activity records need access controls, retention rules, useful search, and protection from alteration. Auditability must not become unnecessary staff surveillance or collect excessive personal data.
- **Future Review Date:** Before pilot launch and during each security review.

### DEC-011 — One active customer group per service location

- **Decision ID:** DEC-011
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Business Rules, Database
- **Decision:** A service location may have at most one active customer group at a time.
- **Context:** Beach sunbed sets, pool sunbed sets, and upper tables represent places being served. Two active groups at the same location would make responsibility, orders, bills, and payment ambiguous.
- **Alternatives Considered:** Allow multiple groups and bills at one location; leave conflicts to staff; enforce one active group and add explicit bill-splitting or shared-location features later if required.
- **Why this option was selected:** The rule creates a clear operational model and prevents a serious class of billing and ownership errors.
- **Consequences:** The database and application must enforce the rule during opening, transfer, and closing. Split-party or shared-location service is outside this rule unless introduced through a new accepted decision.
- **Future Review Date:** If verified customer workflows require simultaneous independent groups at one location.

### DEC-012 — Keep customer-group identity during a transfer

- **Decision ID:** DEC-012
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Business Rules, Database, UX
- **Decision:** Moving a group changes its service location but preserves the same customer group, running bill, orders, notes, payment state, and history.
- **Context:** Customers may move between sunbed sets. Creating a new group or manually copying a bill would risk losing information, duplicating charges, or confusing staff.
- **Alternatives Considered:** Close the old bill and open a new one; copy selected items to a new group; move the complete existing group as one safe action.
- **Why this option was selected:** The visit remains the same even though its physical location changes. Preserving identity gives staff and cashiers a complete, continuous record.
- **Consequences:** Transfer must be an all-or-nothing operation and must refuse an occupied destination. Old and new locations and the actor must be audited. The charge rule for movement between differently priced rows requires its own accepted decision before implementation.
- **Future Review Date:** When the row-change charging rule is approved.

### DEC-013 — Route preparation items by configured destination

- **Decision ID:** DEC-013
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Business Rules, Architecture
- **Decision:** A submitted mixed order will be separated into preparation tickets according to each item’s configured destination, initially Bar, Kitchen, or No Preparation.
- **Context:** Drinks and food are prepared by different teams, but the waiter and customer experience them as one order and one running bill.
- **Alternatives Considered:** Send the complete order everywhere; require the waiter to submit separate orders manually; configure item destinations and separate tickets automatically.
- **Why this option was selected:** Automatic routing reduces waiter effort and prevents irrelevant items from cluttering preparation screens while keeping one coherent customer order.
- **Consequences:** Destination configuration becomes controlled business data. Order, billing, and ticket creation must remain consistent. Sent order items retain their original routing history even if later configuration changes.
- **Future Review Date:** Before adding new preparation destinations or routing rules.

### DEC-014 — Enforce permissions and business rules on the server

- **Decision ID:** DEC-014
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Security, Architecture, Coding Standards
- **Decision:** The server must authenticate users, authorise every protected action, and enforce business rules regardless of what the interface displays.
- **Context:** Interface controls improve usability but can be bypassed, become outdated, or behave differently across devices. Financial and operational rules cannot depend on hidden buttons alone.
- **Alternatives Considered:** Enforce rules only in the browser; duplicate rules independently in every interface; make the server authoritative while the interface also prevents obvious invalid actions.
- **Why this option was selected:** Central enforcement provides consistent protection for all devices and future integrations. Interface checks remain useful for guidance but are not security boundaries.
- **Consequences:** Protected server operations need explicit permission and validation tests. New interfaces and integrations must use the same central rules. Business logic should not be buried only in visual components.
- **Future Review Date:** At each security and architecture review.

### DEC-015 — Build and release iteratively in small milestones

- **Decision ID:** DEC-015
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Deployment, Coding Standards
- **Decision:** The product will be developed, demonstrated, tested, and released through small, complete milestones rather than one large implementation.
- **Context:** Real venue workflows contain details that planning alone cannot reveal. Large batches delay feedback and make defects, scope changes, and rollback harder to manage.
- **Alternatives Considered:** Build the entire planned product before staff review; organise work only by technical layer; deliver small end-to-end capabilities with acceptance checks.
- **Why this option was selected:** Small milestones create earlier evidence, reduce risk, and allow staff feedback to guide the product while changes are still affordable.
- **Consequences:** Each milestone requires a defined outcome and acceptance check. Progress is measured by safely usable workflows, not only code written. Scope may be adjusted when evidence changes priorities.
- **Future Review Date:** At the end of each major phase.

### DEC-016 — Require human approval before major implementation phases

- **Decision ID:** DEC-016
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, AI Workflow, Deployment
- **Decision:** An authorised human must review and approve requirements and outcomes before each major implementation phase begins or moves into production.
- **Context:** The project will use both human and AI assistance. Major phases can introduce business assumptions, security risk, cost, or operational disruption that cannot be delegated solely to automated tools.
- **Alternatives Considered:** Allow development or AI agents to proceed automatically from plans; request approval for every small action; use approval gates for material phases and high-risk changes.
- **Why this option was selected:** Human approval preserves product ownership and accountability without blocking routine, already-authorised work inside an approved phase.
- **Consequences:** Phase boundaries, decision owners, review material, and acceptance conditions must be clear. Approval does not replace testing or professional review. AI agents must not infer authority to start a major phase from unrelated instructions.
- **Future Review Date:** After the first full development and release cycle.

### DEC-017 — Use live updates while keeping the database authoritative

- **Decision ID:** DEC-017
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Architecture, Performance, UX
- **Decision:** Connected staff screens will receive prompt live notices of relevant changes, while the central database remains the authoritative state.
- **Context:** Bar, kitchen, waiter, and cashier screens need timely updates without constant manual refresh. Live connections can disconnect, so they cannot be the only record of an event.
- **Alternatives Considered:** Manual refresh only; periodic polling only; treat real-time messages as the official record; use live notifications that cause screens to read or apply centrally stored state.
- **Why this option was selected:** Live notices improve operational speed, and central persistence ensures a device can recover the correct state after disconnection.
- **Consequences:** Screens must reconnect and resynchronise safely. Missing a notification must not lose an order or payment. The exact live-update technology will be selected during implementation and does not require changing this decision.
- **Future Review Date:** After realistic multi-device and weak-connectivity testing.

### DEC-018 — Full offline operation is not part of the initial release

- **Decision ID:** DEC-018
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Product, Architecture, Infrastructure
- **Decision:** The initial release will require access to the central system and will not promise full offline order taking and billing.
- **Context:** Safe offline operation across several devices requires conflict resolution, synchronisation, duplicate prevention, and clear guarantees about order delivery and financial state. The venue’s actual connectivity quality has not yet justified that complexity.
- **Alternatives Considered:** Full offline-first operation from the start; no connection handling; online operation with clear disconnected states, connectivity safeguards, and a later review.
- **Why this option was selected:** The online approach keeps the first release safer and simpler while the team measures the real problem. It avoids presenting unreliable offline behaviour as protection.
- **Consequences:** Venue Wi-Fi coverage and backup connectivity must be tested and improved. The interface must clearly show disconnection and never falsely confirm unsaved work. Full offline operation requires a new decision and design.
- **Future Review Date:** After venue connectivity testing and the initial live pilot.

### DEC-019 — Use separate development, test, and production environments

- **Decision ID:** DEC-019
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** Infrastructure, Security, Deployment
- **Decision:** Development, testing or staging, and production will be separate environments with controlled access and data.
- **Context:** Features and database changes must be verified without risking live orders, bills, or staff access. Production information must not be casually copied into development.
- **Alternatives Considered:** Use one shared environment; use development and production only; maintain separate development, staging, and production purposes.
- **Why this option was selected:** Separation supports safe review, realistic acceptance testing, controlled releases, and protection of live information.
- **Consequences:** Configuration and deployment processes must be repeatable across environments. Test data should be synthetic or properly anonymised. Production access remains limited and auditable.
- **Future Review Date:** Before the first production release.

### DEC-020 — AI assistance requires human accountability

- **Decision ID:** DEC-020
- **Date:** 2026-07-20
- **Status:** Accepted
- **Category:** AI Workflow, Security, Coding Standards
- **Decision:** AI may assist throughout the project, but a human remains accountable for requirements, domain rules, security, financial behaviour, migrations, infrastructure, and production release approval.
- **Context:** AI can accelerate analysis, documentation, implementation, testing, and review, but its output may contain incorrect assumptions, insecure choices, or changes outside the intended scope.
- **Alternatives Considered:** Prohibit AI; accept AI output without additional review; use AI for scoped work under the same or stronger review and verification standards as human work.
- **Why this option was selected:** Controlled AI assistance can improve productivity while human accountability protects the product, business, staff, and customers.
- **Consequences:** AI tasks must state scope, constraints, and acceptance checks. AI-generated claims must be independently verified. Production secrets and unnecessary personal data must not be supplied. AI must not perform irreversible or major external actions without explicit authorised approval.
- **Future Review Date:** Review annually and after any material AI-related incident.

### DEC-021 — Use a pnpm workspace for JavaScript and TypeScript

- **Decision ID:** DEC-021
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Coding Standards, Architecture
- **Decision:** Manage the React application and future shared TypeScript packages in one pnpm workspace.
- **Context:** The repository needs one codebase for supported web devices and a controlled place for genuinely shared packages. Dependency versions must be reproducible without duplicating installation across packages.
- **Alternatives Considered:** npm workspaces; Yarn; pnpm; separate package-manager projects; a larger monorepo orchestration tool from the beginning.
- **Why this option was selected:** pnpm provides strict, space-efficient dependency management and native workspaces without adding a separate build-orchestration layer before it is needed.
- **Consequences:** Contributors need the approved Node.js LTS line and pnpm through Corepack. A committed lockfile becomes mandatory when installation is authorised. Advanced task caching is deferred until measured repository size justifies it.
- **Future Review Date:** Owner review of the engineering foundation or when workspace build times become material.

### DEC-022 — Use Python 3.13, uv, and a pyproject-based backend

- **Decision ID:** DEC-022
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Coding Standards, Architecture
- **Decision:** Target Python 3.13 and manage the FastAPI backend environment, dependency resolution, and lockfile with uv and `pyproject.toml`.
- **Context:** The backend needs a supported Python version, fast reproducible local setup, a standard project description, and one clear dependency workflow. The local system Python 3.9.6 is below the proposed project requirement and below current FastAPI support.
- **Alternatives Considered:** pip and `requirements.txt`; Poetry; PDM; uv with `pyproject.toml`; use the machine’s system Python.
- **Why this option was selected:** `pyproject.toml` is the standard Python project configuration, and uv provides Python management, dependency locking, environment creation, and command execution in one fast tool. Python 3.13 is a supported stable line without selecting the newest language line solely for novelty.
- **Consequences:** Developers must install uv or use an approved container workflow. `uv.lock` must be generated and committed after dependencies are approved. The backend cannot run on the current system Python without a separate project environment.
- **Future Review Date:** Owner review of the engineering foundation and before the first backend implementation.

### DEC-023 — Use React 19 with TypeScript, Vite, ESLint, Prettier, and Vitest

- **Decision ID:** DEC-023
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Architecture, Coding Standards, UX, UI
- **Decision:** Prepare the web application around React 19 and strict TypeScript, using Vite for development and builds, ESLint for code-quality rules, Prettier for formatting, and Vitest for unit and component tests.
- **Context:** The approved product direction requires a mobile-first responsive web application from one codebase. The engineering foundation needs a small, mainstream toolchain with fast feedback and strong static checks.
- **Alternatives Considered:** Next.js or another full-stack React framework; Create React App; a custom bundler; Vite with React; JavaScript without strict TypeScript; other test runners.
- **Why this option was selected:** The backend is a separate FastAPI application, so a client-focused Vite setup avoids an unnecessary second server framework. React has a mature ecosystem, strict TypeScript catches many mistakes early, and Vitest integrates with Vite. ESLint and Prettier give automated, consistent checks.
- **Consequences:** Routing, server-state management, styling, component tooling, accessibility testing, and browser end-to-end testing remain unselected until their concrete needs are approved. Dependency versions must be locked and reviewed before application work.
- **Future Review Date:** Owner review of the engineering foundation and before creating the first UI entry point.

### DEC-024 — Use FastAPI with strict Python quality tools

- **Decision ID:** DEC-024
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Architecture, Coding Standards, Testing
- **Decision:** Use FastAPI for the backend HTTP application, Uvicorn as its initial application server, Ruff for formatting and linting, mypy in strict mode for static type checking, and pytest with coverage support for tests.
- **Context:** The approved stack request names FastAPI. The backend foundation must provide consistent checks without implementing any route, schema, database model, or business feature.
- **Alternatives Considered:** Other Python web frameworks; separate formatter and multiple lint tools; Pyright instead of mypy; unittest instead of pytest; defer all quality tooling.
- **Why this option was selected:** These tools are well aligned with typed FastAPI projects, provide fast local feedback, and cover distinct quality needs with limited overlap. Strict checks establish expectations before code volume grows.
- **Consequences:** Initial strictness may require more explicit code, but reduces ambiguity. The coverage threshold remains zero until the first code and risk-based target are approved; critical behaviour will require meaningful tests regardless of percentage.
- **Future Review Date:** Before the first backend implementation and after the first completed backend milestone.

### DEC-025 — Use Docker Compose for local PostgreSQL only

- **Decision ID:** DEC-025
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Infrastructure, Database
- **Decision:** Use Docker Compose to provide an isolated PostgreSQL 17 service for local development, initially bound only to the developer’s loopback interface.
- **Context:** PostgreSQL is already accepted as the initial relational database. Developers need a repeatable local database without creating schemas or relying on a shared environment. The production hosting design is still unresolved.
- **Alternatives Considered:** Require a manually installed PostgreSQL server; use a shared remote development database; containerise every application immediately; use Docker Compose for local infrastructure only.
- **Why this option was selected:** A local container makes the database version and startup repeatable while keeping application execution flexible and avoiding production assumptions. Loopback binding limits accidental network exposure.
- **Consequences:** Docker is a proposed local prerequisite. The named volume preserves local data until deliberately removed. No table, migration, or seed data exists. The PostgreSQL major version and image update policy require approval before implementation.
- **Future Review Date:** Owner review of the engineering foundation and before creating the first database migration.

### DEC-026 — Use environment variables with committed examples and no committed secrets

- **Decision ID:** DEC-026
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Security, Infrastructure, Deployment
- **Decision:** Read environment-specific configuration from environment variables, commit only documented example values, and keep real local and deployed secrets out of version control.
- **Context:** Development, staging, and production require different database addresses, credentials, hosts, and operational settings. Secrets embedded in code or committed configuration create lasting exposure.
- **Alternatives Considered:** Hard-code configuration; commit a shared `.env`; use environment variables with ignored local files; require a production secret manager for local development as well.
- **Why this option was selected:** Environment variables are broadly supported by the selected tools and separate code from environment configuration. A safe `.env.example` explains required names without distributing credentials.
- **Consequences:** Local `.env` files are ignored. Production secrets must use an approved managed secret store; environment variables alone do not select that provider. Startup validation and secret-rotation procedures must be implemented later.
- **Future Review Date:** Before selecting production infrastructure.

### DEC-027 — Use GitHub Actions as the initial continuous-integration service

- **Decision ID:** DEC-027
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Infrastructure, Deployment, Testing
- **Decision:** Run repository validation, formatting, linting, type checks, tests, and builds through GitHub Actions with read-only repository permissions by default.
- **Context:** The repository requires automated, repeatable checks before merge. GitHub is the requested collaboration platform, and no independent CI service has been approved.
- **Alternatives Considered:** No hosted CI; another CI provider; self-hosted runners; GitHub Actions hosted runners.
- **Why this option was selected:** GitHub Actions integrates directly with pull requests and branch protection and can start with minimal infrastructure. Read-only default permissions reduce workflow risk.
- **Consequences:** Foundation validation runs immediately. Frontend and backend jobs remain gated until reviewed lockfiles exist, so CI cannot install unresolved dependencies. Production deployment is explicitly absent and needs a separate decision and approval.
- **Future Review Date:** Owner review of the engineering foundation and before enabling deployment workflows.

### DEC-028 — Keep testing close to applications with a cross-system test area

- **Decision ID:** DEC-028
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Testing, Coding Standards
- **Decision:** Place tests owned by one application beside that application, and reserve the root `tests/` directory for cross-application unit utilities, integration tests, and end-to-end journeys.
- **Context:** A monorepository needs clear test ownership. Putting every test in one distant folder makes changes harder to discover, while keeping all tests inside applications provides no natural home for browser-to-backend and infrastructure-boundary checks.
- **Alternatives Considered:** Put every test under root `tests/`; put every test inside application source trees; use application-local tests plus a deliberately small cross-system test area.
- **Why this option was selected:** Co-location supports maintainability and clear ownership, while the root test area supports critical workflows crossing component boundaries.
- **Consequences:** Test duplication and vague ownership must be avoided. The browser end-to-end tool, database test isolation method, and coverage gates still require approval.
- **Future Review Date:** Before the first feature test is written.

### DEC-029 — Keep the repository proprietary by default

- **Decision ID:** DEC-029
- **Date:** 2026-07-20
- **Status:** Proposed
- **Category:** Product, Security
- **Decision:** Use an all-rights-reserved proprietary repository notice until the owner approves another licence or distribution model.
- **Context:** The project is an internal commercial product, and no permission to open-source, distribute, or sublicense its materials has been granted. The requested repository foundation requires a `LICENSE` file.
- **Alternatives Considered:** Publish under a permissive open-source licence; use a copyleft licence; omit a licence; reserve all rights pending a business decision.
- **Why this option was selected:** Reserving rights avoids granting unintended public permissions and matches the project’s current internal status.
- **Consequences:** Outside use, copying, and distribution require written permission. The copyright owner’s exact legal name and final commercial licensing terms still need legal confirmation.
- **Future Review Date:** Owner review of the engineering foundation and before sharing the repository externally.

### DEC-030 — Give every Service Location a stable Digital Identity

- **Decision ID:** DEC-030
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Security, UX, Business Rules
- **Decision:** Every Service Location has one stable Digital Identity. NFC is the preferred initial way for authorised staff to identify and open that location’s current digital context, while manual identification by visible name or number remains available.
- **Context:** Staff working across beach, pool, and upper-table areas need to reach the correct Service Location quickly and reliably. A physical marker at the place of service can reduce searching and selection mistakes. However, Service Location identity must outlive any physical tag, and the tag must not become a portable copy of changing operational or financial information.
- **Alternatives Considered:** Manual selection only; store current location state on an NFC tag; make the physical NFC tag the identity of the Service Location; use a stable technology-neutral Digital Identity that NFC can resolve initially, with manual lookup and future identification methods available.
- **Why this option was selected:** A stable Digital Identity connects the physical location to the correct current information with minimal staff effort while preserving the central system as the source of truth. Keeping the business concept independent from NFC allows a damaged tag to be replaced and allows QR codes or other suitable methods to be supported later without creating a new Service Location.
- **Consequences:** The NFC tag may contain only a stable, non-sensitive identifier or secure application link that resolves to the Service Location. It must not contain the current Customer Group, Responsible Waiter, prices, Bill information, Order information, customer information, permissions, or other changing or sensitive business data. All current information is retrieved from the central system after identification. Replacing a physical tag does not create a new Service Location. Manual lookup by the same visible name or number must remain available. Identification never signs a person in, grants permission, bypasses business rules, or automatically creates a Customer Group, Bill, charge, Order, transfer, Payment, or any other operational or financial action.
- **Future Review Date:** After the first venue pilot and before approving another physical identification method.

### DEC-031 — Make Customer Group the primary operational entity

- **Decision ID:** DEC-031
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Architecture, Business Rules
- **Decision:** Customer Group is the primary operational entity. It owns its Service Location, Orders, optional Bill, Payments through that Bill, Responsible Waiter, and History. Visit is not part of the core operational model and may return only as an approved future concept.
- **Context:** Earlier documents used Customer Group and Visit for overlapping meanings. This made opening, occupancy, transfer, ordering, billing, responsibility, and completion ambiguous.
- **Alternatives Considered:** Keep both concepts as one-to-one core entities; make Visit primary; make Customer Group primary and defer Visit until it has a distinct future purpose.
- **Why this option was selected:** Staff already operate around the group being served. One primary entity removes duplication and makes responsibility and lifecycle language easier to understand.
- **Consequences:** A Service Location is occupied by an active Customer Group. Orders, responsibility, transfer, History, and any Bill are connected directly to that Customer Group. Core documents and events must not depend on Visit.
- **Future Review Date:** Before introducing reservations, customer profiles, or repeat-visit history.

### DEC-032 — Make Zones dynamic operational groupings

- **Decision ID:** DEC-032
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, UX, Business Rules
- **Decision:** A Zone is a dynamic operational grouping of an arbitrary collection of Service Locations. It is independent from physical layout and may be created, renamed, deleted, or reassigned by a Master user with the required Capability.
- **Context:** The earlier Domain Model described Zone as a permanent geographical subdivision inside an Area. Daily service may require staff to group locations differently for weekday, weekend, full-capacity, or event operation without changing the physical venue.
- **Alternatives Considered:** Permanent physical Zones; fixed waiter sections; dynamic operational Zones independent from Area and physical position.
- **Why this option was selected:** Dynamic Zones support daily coordination while preserving the enduring identity and physical Area of each Service Location.
- **Consequences:** A Zone belongs to one Venue but not to an Area. Service Locations may be reassigned at any time without changing identity or history. Deleting a Zone removes the grouping only and never deletes or relocates its Service Locations.
- **Future Review Date:** After the first operational pilot using Zones.

### DEC-033 — Create a Bill only when a financial obligation exists

- **Decision ID:** DEC-033
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Business Rules
- **Decision:** Opening a Customer Group does not automatically open a Bill. A Bill is created only when the group receives its first approved financial obligation.
- **Context:** A Customer Group may begin service before any charge exists. Treating every group opening as a financial event incorrectly combines service identity with billing.
- **Alternatives Considered:** Always create a zero-value Bill with the group; create the Bill on first Order only; create the Bill when any approved obligation first exists.
- **Why this option was selected:** The Bill then represents an actual financial obligation while the Customer Group can exist independently for seating and service responsibility.
- **Consequences:** The first obligation may be a sunbed charge, minimum consumption, first ordered item, reservation deposit, or another approved charge. A Customer Group may have no Bill. Once created, the Bill aggregates all approved obligations and Orders for that group.
- **Future Review Date:** Before adding deposits, minimum consumption, or no-charge service scenarios.

### DEC-034 — Apply the Beach Sunbed obligation when the waiter opens the group

- **Decision ID:** DEC-034
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Business Rules
- **Decision:** When the Responsible Waiter intentionally opens a Customer Group at a Beach Sunbed Service Location, the approved Beach Sunbed financial obligation arises immediately. This creates the Bill when the group does not already have one.
- **Context:** Beach Sunbed use creates a charge at the start of official service, but merely identifying the physical location must never create a financial event.
- **Alternatives Considered:** Charge on NFC identification; charge at first Order; charge at Bill closing; charge immediately after the Responsible Waiter officially opens the Customer Group.
- **Why this option was selected:** The intentional opening action clearly separates physical identification from the start of service and the financial obligation.
- **Consequences:** NFC and manual identification remain non-financial. The waiter must see and confirm the applicable approved charge through the opening flow. The charge and resulting Bill are created together as part of the official opening outcome.
- **Future Review Date:** Before approving waivers, minimum-consumption alternatives, or transfer between differently charged locations.

### DEC-035 — Only the Responsible Waiter opens a Customer Group

- **Decision ID:** DEC-035
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Business Rules, UX
- **Decision:** The Responsible Waiter is the only business role that officially opens a Customer Group and starts service. A Host may escort customers and organize seating; a Host or Cashier does not open the Customer Group.
- **Context:** Seating assistance and official service opening are different responsibilities. Combining them could create unclear ownership or unintended charges.
- **Alternatives Considered:** Allow Host, Cashier, or any authorized staff member to open; let the system open automatically on location identification; require the Responsible Waiter’s intentional opening action.
- **Why this option was selected:** The person accountable for service should intentionally accept the group and any immediate Beach Sunbed obligation.
- **Consequences:** A Host may identify or propose a Service Location but cannot start service. Capability-based authorization must preserve the waiter-only business rule rather than using a broad generic permission.
- **Future Review Date:** If a future Venue operates without waiter-led service.

### DEC-036 — Treat each submitted Order as one ordering round

- **Decision ID:** DEC-036
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Business Rules
- **Decision:** One Customer Group may have multiple Orders. Each submitted Order is one confirmed ordering round, and the group’s Bill aggregates the approved financial obligations from all Orders.
- **Context:** Hospitality customers commonly order several times while remaining at one Service Location or after transferring.
- **Alternatives Considered:** Keep one editable Order for the entire group; create a new Bill for each round; preserve each submitted round as a separate Order under one Customer Group and Bill.
- **Why this option was selected:** Separate rounds preserve preparation and ordering history while one Bill gives the customer and Cashier a complete running obligation.
- **Consequences:** Submitted Orders are not overwritten by later rounds. A later round creates new preparation work and Bill Lines while preserving earlier Orders.
- **Future Review Date:** Before introducing courses, scheduled Orders, or Bill splitting.

### DEC-037 — Define Zone Templates as a future capability

- **Decision ID:** DEC-037
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Business Rules, UX
- **Decision:** Zone Template is an approved future concept that describes a reusable starting arrangement of operational Zones. A Master user with the required Capability may apply a template before service starts, after which individual Service Locations may be reassigned manually.
- **Context:** Venues may organize daily service differently for Weekday, Weekend, Full Capacity, Private Event, or Wedding operation.
- **Alternatives Considered:** Rebuild all Zones manually every day; keep one permanent Zone arrangement; offer reusable templates while retaining manual reassignment.
- **Why this option was selected:** Templates can reduce setup effort without making Zones or Service Location identity permanent or inflexible.
- **Consequences:** Zone Templates are not part of the first version. Applying a template creates the day’s initial Zone structure; it does not change Areas, Service Location Digital Identities, historical groupings, Customer Groups, or financial records.
- **Future Review Date:** Before Zone Template implementation is approved.

### DEC-038 — Authorize actions through Capabilities, not Roles

- **Decision ID:** DEC-038
- **Date:** 2026-07-21
- **Status:** Accepted
- **Category:** Product, Security, Business Rules
- **Decision:** Roles group business responsibilities but do not directly authorize actions. A Capability is the explicit business authority to perform a defined action in an approved context.
- **Context:** Role names such as Waiter, Cashier, Manager, Host, or Master describe work but are too broad to safely determine every sensitive action.
- **Alternatives Considered:** Give all authority directly through Roles; use informal Manager exceptions; use explicit Capabilities independently from Role labels.
- **Why this option was selected:** Capability-based authorization makes authority clear, reviewable, and adaptable across different Venues without changing what a Role means.
- **Consequences:** Examples include Open Customer Group, Transfer Customer Group, Assign Waiter, Close Bill, Reopen Bill, Manage Zones, Manage Zone Templates, Manage Menus, Record Payments, and Refund Payments. A Staff Member must have the required Capability and satisfy the business rule. A Capability cannot make a Host or Cashier the official opener where DEC-035 requires the Responsible Waiter. This decision replaces generic Role-to-permission assumptions for business authorization; DEC-014 continues to require central enforcement, with Capability as the approved business term.
- **Future Review Date:** Before account and authorization implementation.

### DEC-039 — Require confirmed readiness before daily Venue opening

- **Decision ID:** DEC-039
- **Date:** 2026-07-25
- **Status:** Accepted
- **Category:** Product, Business Rules, UX, Reporting
- **Decision:** A Venue cannot open for guest service on a Business Date until every mandatory Operational Department has declared READY. The Host coordinates the opening process and, when holding the required Capability, intentionally opens the Venue after the readiness condition is satisfied. Opening creates the official operational start of the Business Date and a permanent Opening Report.
- **Context:** A safe and dependable opening requires coordinated readiness across teams such as Kitchen, Bar, Beach Operations, Cleaning, Maintenance, Cashier, and Reception where applicable. The Host needs one current view of readiness but should not be expected to personally verify work belonging to every department.
- **Alternatives Considered:** Open at a fixed time without readiness confirmation; make the Host personally inspect every department; allow guest service while some mandatory departments remain unready; require each department’s responsible person to declare status and allow opening only when all mandatory departments are READY.
- **Why this option was selected:** Department ownership keeps verification with the people closest to the work, while Host coordination provides one clear opening decision. The all-ready condition reduces avoidable guest-facing failures and creates a trustworthy start to the operating day.
- **Consequences:** Each mandatory Operational Department declares READY, NOT READY, or BLOCKED through its responsible person. NOT READY and BLOCKED require a reason. The Host sees all current declarations, delays, issues, and comments in one Opening Dashboard. OPEN VENUE is unavailable until all mandatory departments are READY and does not become authorized merely because a person holds the Host Role; the required Capability and business rules still apply. Before opening, guest arrivals, new Customer Groups, and Orders are not allowed. Opening starts the official operating day, enables those activities, starts operational timers, and begins collection of the day’s dashboard measures. The permanent Opening Report records the opening time, Host, department readiness, delays, blocking issues, and comments as part of daily operational history. This decision does not allow the Host to open a Customer Group; DEC-035 remains unchanged.
- **Future Review Date:** After the first live opening pilot and before applying the workflow to another Venue type.

## Rules for Maintaining This File

1. **Never delete a historical decision.** Rejected and superseded decisions remain part of the project’s history.
2. **Never reuse a Decision ID.** IDs increase sequentially and remain stable forever.
3. **Create a new entry when a decision changes.** Do not rewrite the old entry to make history appear different.
4. **Mark replaced decisions as Superseded.** Link the old and new Decision IDs in both entries whenever practical.
5. **Record significant decisions before implementation whenever possible.** If urgency prevents this, record the decision and reason promptly afterward.
6. **Record the reason, not only the result.** Context, realistic alternatives, trade-offs, and consequences are required.
7. **Use a Proposed entry for unresolved choices.** Change its status when authorised reviewers accept or reject it; preserve the proposal text.
8. **Name the real constraints.** Include business, user, security, cost, schedule, operational, and legal factors that materially shaped the choice.
9. **Link related decisions.** Mention relevant Decision IDs and project documents when they help explain dependencies or conflicts.
10. **Use exact dates.** Dates use the `YYYY-MM-DD` format.
11. **Use one or more recognised categories.** Add a category only when existing ones are genuinely insufficient.
12. **Set a future review trigger when assumptions may change.** A review date may be a calendar date or a clear event, such as onboarding the second venue.
13. **Do not record trivial implementation details.** Record choices that affect product behaviour, users, data, security, architecture, operation, cost, future options, or significant maintenance.
14. **Record every major product or architecture change.** This includes new modules, new external services, new kinds of sensitive data, important business-rule changes, and changes to the system’s source of truth.
15. **Record exceptions.** If an accepted principle is intentionally broken, document why, the scope, the risks, the approving person, and when the exception will be reviewed.
16. **Keep entries understandable to non-developers.** Use plain language and explain necessary technical terms.
17. **Require authorised human review for Accepted status.** AI agents may draft decisions but cannot grant themselves business authority.
18. **Keep this log consistent with the master blueprint.** If an accepted decision changes the blueprint, update the blueprint through an explicitly authorised separate change.
