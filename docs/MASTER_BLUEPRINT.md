# Emerald Management System — Master Blueprint

## 1. Purpose and authority

This document is the permanent product and architecture reference for Emerald Management System. It explains what the product should become, how important concepts are understood, and the rules that guide design and development over its lifetime.

Detailed requirement, architecture, and delivery documents may expand on this blueprint. If a future decision conflicts with it, the conflict must be discussed and this document must be deliberately updated. It should never change only because the current technology makes another approach easier.

The blueprint is a living document, but not a casual one. Material changes require a recorded reason, owner approval, and a review of their effect on operations, security, money, and existing data.

## 2. Vision

Emerald Management System will become the trusted operational centre for hospitality venues that combine service areas such as beaches, pools, bars, kitchens, and tables.

For staff, it should turn a busy venue into a clear shared picture: who is serving each customer group, what has been ordered, where each item must go, what is ready, what is owed, and what requires attention.

For owners, it should provide control and insight without forcing staff into slow or complicated processes. The system should begin with Emerald’s real operation in Loutraki and grow from proven needs rather than assumptions.

## 3. Product philosophy

### Operations first

The product exists to support a live hospitality shift. A feature is valuable when it makes work faster, safer, clearer, or more accountable.

### Simple outside, rigorous inside

Staff screens should feel direct and forgiving. Behind them, the system must apply strict rules to orders, locations, bills, transfers, and payments.

### One shared truth

All authorised devices should show the same operational state. The central system, not memory, paper notes, or a single device, is the official record.

### Earn complexity

Begin with the smallest complete solution. Add modules, integrations, and infrastructure only when real use, risk, or growth justifies them.

### Preserve trust

Money and history must remain understandable. Important records are corrected with traceable actions, never quietly rewritten.

## 4. Core principles

1. **Correctness before convenience.** A fast wrong bill or lost order is unacceptable.
2. **Clarity during pressure.** The interface must remain understandable in sunlight, noise, crowds, and weak connectivity.
3. **Explicit ownership.** Every active Customer Group has exactly one clearly Responsible Waiter at a time, and only that Responsible Waiter officially opens the group.
4. **Complete actions.** Important operations either succeed fully or leave the system unchanged.
5. **No false success.** The application confirms an order, transfer, or payment only after it is safely recorded.
6. **Least privilege.** Each person can perform only the actions needed for their work.
7. **Traceability.** Sensitive actions record who did what and when.
8. **Historical truth.** Later price, menu, or venue changes do not alter past bills.
9. **Device independence.** Core work must be usable on supported phones, tablets, and desktop computers.
10. **Inclusive communication.** Meaning must not depend on colour, technical language, or hidden gestures alone.
11. **Measured evolution.** Observed behaviour and reliable data guide priorities.
12. **Reversible delivery.** Changes should be small, testable, and safely deployable.
13. **Stable physical-to-digital identity.** Physical Service Locations have stable digital identities, while the central system remains the source of operational truth.
14. **Capability-based authority.** Roles describe business responsibility; explicit Capabilities authorize protected actions and never bypass business rules.

## 5. Domain model

The domain model defines the business language used in screens, discussions, data, and code. These terms should not be replaced by near-synonyms without a deliberate decision.

### Identity and access

- **User:** An individual staff member with a personal account.
- **Role:** A named set of business responsibilities, such as Waiter, Host, Bar Staff, Kitchen Staff, Cashier, Manager, or Master. A Role does not authorize an action.
- **Capability:** Explicit authority for a Staff Member to perform one defined action in an approved context. Capabilities are granted and reviewed separately from Roles.
- **Staff Session:** A user’s authenticated period of access on a device.

### Venue

- **Venue:** One operating business location using the system.
- **Area:** A major service section, such as Beach, Pool, or Upper Level.
- **Row:** A physical grouping used for position, display, and sunbed charging rules.
- **Service Location:** A place that can serve one active customer group, such as a Sunbed Set or Upper Table.
- **Zone:** A dynamic operational grouping of any selected Service Locations within one Venue, independent from Area and physical layout.
- **Zone Template:** A future reusable starting arrangement of Zones that an authorised Master user may apply before service begins.
- **Sunbed Set:** The business unit assigned to one customer group; it may contain one or more physical sunbeds.
- **Upper Table:** A service location in the upper-table area.
- **Location Status:** The operational state of a service location, such as Available, Occupied, or Unavailable.

Physical layout and commercial rules must remain separate. Moving a sunbed on a screen should not silently change pricing policy.

### Service

- **Customer Group:** The primary operational entity that owns its Service Location, Responsible Waiter, Orders, optional Bill, Payments through that Bill, and History.
- **Responsible Waiter:** The one staff member accountable for an active customer group at a given time.
- **Assignment History:** The record of changes to the responsible waiter.
- **Transfer:** One complete move of a customer group and all of its operational context from one Service Location to another.

The Customer Group remains the same when its location or Responsible Waiter changes. Visit is not a core operational entity and may be introduced later only if it gains a distinct approved business purpose.

### Menu and preparation

- **Menu Category:** A group used to organise menu items.
- **Menu Item:** A product available to order.
- **Price:** A dated commercial value for a menu item.
- **Preparation Destination:** The place responsible for fulfilling an item, normally Bar, Kitchen, or No Preparation.
- **Order:** One submitted round for a customer group.
- **Order Item:** A priced snapshot of a menu item, quantity, destination, and notes at submission time.
- **Preparation Ticket:** The destination-specific work created from an order.
- **Ticket Status:** The agreed preparation state, such as New, Preparing, or Ready.

An Order is one submitted ordering round. A Customer Group may have multiple Orders. An Order may create multiple preparation tickets and contributes approved obligations to the Customer Group’s Bill. If the first ordered item is the first financial obligation, submitting that Order creates the Bill.

### Billing

- **Bill:** The financial record created for one Customer Group only when its first approved financial obligation exists. A Customer Group may exist without a Bill.
- **Bill Entry:** One charge, discount, correction, or other amount contributing to the bill.
- **Sunbed Charge:** A bill entry calculated from the approved row rule at the agreed event.
- **Adjustment:** A traceable authorised change to an amount; it does not erase the original record.
- **Payment:** A recorded transfer of value against a bill using an approved payment method.
- **Balance:** Bill charges and adjustments minus valid payments.
- **Bill Closure:** The controlled end of a bill after its balance and business rules are satisfied.

Money is represented in exact minor units for its currency. Submitted order prices and applied charges are immutable snapshots.

Opening a Customer Group at a Beach Sunbed is an intentional action performed by the Responsible Waiter. It immediately creates the approved Beach Sunbed obligation and therefore the Bill. Identifying a Service Location by NFC or manual lookup never opens a Customer Group or creates a financial obligation.

### Governance

- **Activity Record:** An append-only account of a sensitive event, including actor, time, subject, and relevant before-and-after values.
- **Business Date:** The operating day to which a transaction belongs. Its boundary must be defined for shifts continuing after midnight.
- **Configuration:** Owner-approved business settings that may vary by venue without changing software.

### Essential relationships and invariants

- A Venue contains physical Areas, Rows, and Service Locations. Dynamic Zones group Service Locations independently from that physical layout.
- A service location has at most one active customer group.
- An active customer group has exactly one responsible waiter and may have no Bill until its first financial obligation exists.
- A customer group has many orders; an order has one or more order items.
- Order items produce tickets grouped by preparation destination.
- Once created, a bill has many bill entries and payments and aggregates approved obligations from all ordering rounds.
- A transfer changes location, not customer-group or bill identity.
- Role does not grant authority; the Staff Member must hold the required Capability and satisfy the applicable business rule.
- Closed financial history is retained and remains traceable.

## 6. UX principles

- Design around complete staff tasks, not database forms.
- Put the most common actions within easy thumb reach on mobile devices.
- Minimise taps, typing, scrolling, and repeated confirmation during normal order taking.
- Help staff reach the correct Service Location with the minimum practical number of interactions.
- Use physical context to open the relevant digital context directly when an approved identification method is available.
- Make Service Location identification fast and understandable in bright outdoor conditions.
- Treat NFC as the preferred initial identification method, not as the permanent business concept or the source of current location state.
- Never allow a failed, damaged, or unavailable NFC interaction to block service.
- Provide a visible manual fallback for critical location workflows so authorised staff can reach the same Service Location by its name or number.
- Make location, customer group, responsible waiter, bill state, and save state visible at the moment they matter.
- Use progressive disclosure: show normal choices first and exceptional tools only when needed.
- Prevent mistakes before showing error messages. Disable impossible choices and explain why.
- Preserve safe drafts where practical, but never imply that an unsent draft reached the bar or kitchen.
- Show immediate, plain-language feedback for saving, saved, failed, disconnected, and conflicting states.
- Provide a clear recovery path after errors; do not strand the user.
- Require stronger confirmation for destructive or financial actions, not routine actions.
- Keep patterns consistent between phone, tablet, and desktop while adapting layout to screen size.
- Test workflows with actual staff in realistic light, noise, connectivity, and time pressure.
- Design for Greek and English text expansion, even if launch begins in one language.
- Support keyboard use on desktop and accessible touch targets on handheld devices.

## 7. UI philosophy

The interface should feel calm, operational, and easy to scan. Decoration must never compete with the next required action.

- Use a small, consistent design system for colour, type, spacing, controls, states, and feedback.
- Use strong contrast and readable type suitable for outdoor use.
- Use colour as reinforcement only; pair it with labels, icons, shape, or position.
- Prefer familiar words such as “Send order,” “Move group,” and “Record payment.”
- Keep primary actions visually clear and limit competing primary buttons.
- Show currency, date, time, and quantities consistently according to approved Greek locale rules.
- Separate live operational state from historical or management information.
- Keep bar and kitchen displays glanceable, with oldest and urgent work evident.
- Do not show technical identifiers or errors to staff when a human description is possible.
- Avoid dense dashboards whose numbers do not lead to action.
- Use animation sparingly and never make it necessary to understand state.

Accessibility is part of quality, not a later visual adjustment. Aim for recognised web accessibility guidance appropriate to an internal business application.

## 8. Security principles

- Give every person an individual account; avoid shared identities.
- Authenticate every protected request and authorise the action on the server.
- Apply least privilege through explicit Capabilities, reviewed independently from Role definitions.
- Protect all traffic with current encryption and store passwords only with an approved one-way method.
- Keep credentials, keys, and connection details outside source code and logs.
- Record access failures and sensitive business actions without logging passwords, payment secrets, or unnecessary personal data.
- Minimise personal data and define retention and deletion policies with professional legal and accounting advice.
- Protect against common web risks through secure defaults, input validation, output encoding, safe database access, and dependency review.
- Use secure sessions, timeouts appropriate to venue work, account disabling, and a safe recovery process.
- Separate development, testing, and production access and data.
- Encrypt backups, restrict access, and test restoration.
- Maintain an incident response process covering containment, communication, recovery, and learning.
- Treat fiscal, payment-terminal, accounting, and external integrations as separate trust boundaries.

Security controls must be proportional, usable, and reviewed regularly. Staff should not be pushed toward insecure workarounds by impractical rules.

## 9. Performance and reliability principles

- Define performance from the user’s view: screen response, confirmed save, live update delay, and recovery time.
- Common navigation and local interactions should feel immediate on supported devices.
- Normal read actions should generally complete within one second on a healthy venue connection; important writes should acknowledge promptly and show progress when they cannot.
- New preparation tickets and important status changes should normally appear on connected screens within a few seconds.
- Never trade financial correctness or confirmed durability for superficial speed.
- Measure before optimising. Use production-safe monitoring to find real bottlenecks.
- Design database access, indexes, pagination, and payload sizes for predictable growth.
- Cache only information that can safely be stale, and define how it is refreshed.
- Make order submission, transfer, and payment operations safe to retry.
- Use timeouts, bounded retries, and clear failure states for external services.
- Avoid single-device state that would be lost or invisible to other staff.
- Set measurable availability, recovery-time, and recovery-point objectives before launch and revise them with business growth.
- Test concurrency and peak-shift behaviour, not only single-user speed.

## 10. Naming conventions

### Product and business language

- Use **Emerald Management System** as the full product name and **Emerald** only when the context is unambiguous.
- Use the exact domain terms defined in this blueprint in requirements, interface labels, code, and data.
- Prefer one clear name over abbreviations. Do not use “table” to mean every service location or “customer” to mean a customer group.
- Names should describe business meaning, not current screen position or technical implementation.

### Code and data

- Use English for code, technical documentation, database names, APIs, logs, and commits.
- Use `PascalCase` for types and user-interface components.
- Use `camelCase` for variables, functions, and application fields.
- Use `snake_case` for database tables and columns.
- Use plural nouns for collections and database tables; use singular nouns for domain types.
- Use clear boolean names beginning with `is`, `has`, `can`, or `should`.
- Include units in ambiguous names, such as `timeoutMs` or `amountCents`.
- Use stable, non-meaningful identifiers for records. Human-readable numbers may exist separately.
- Name timestamps by event, such as `submittedAt` or `closedAt`, and store them in UTC. Display them in the venue’s timezone.
- Name state values with approved domain language and avoid vague states such as `done` when `ready` or `closed` is meant.
- APIs and events should describe outcomes or business actions, not screen buttons.
- Avoid unexplained acronyms, generic names such as `data`, and misleading legacy names.

### Files and documents

- Product governance documents use uppercase descriptive Markdown filenames.
- Source-file conventions should be chosen once with the technology stack and enforced automatically.
- Database changes and architectural decisions use dated or sequential identifiers and meaningful titles.

## 11. Development rules

1. Begin work from an approved requirement with clear acceptance conditions.
2. Keep changes small enough to review, test, deploy, and reverse safely.
3. Put business rules in the central domain or application layer, not only in screens.
4. Make the database enforce essential uniqueness and relationship rules where possible.
5. Treat money, Capabilities, transfers, order submission, and closing as high-risk areas requiring explicit design review.
6. Do not silently delete or rewrite operational and financial history.
7. Do not introduce a dependency, service, or framework without a specific benefit, maintenance check, and security review.
8. Keep business decisions configurable only when real variation exists; avoid a settings system for every detail.
9. Use versioned database changes and preserve compatibility during safe releases.
10. Never use production customer or payment data in development or automated tests.
11. Review every change by another person or an explicitly approved review process before production.
12. Automated checks must pass before merging or release; exceptions require a recorded reason and owner of the follow-up.
13. Update relevant requirements, decisions, runbooks, and user guidance in the same change as behaviour.
14. Remove obsolete paths and feature flags after a safe transition; do not accumulate permanent temporary code.
15. Observe features after release and define rollback or mitigation before risky deployment.
16. Build integrations behind clear boundaries so failure does not corrupt the core bill or order record.
17. Prefer simple, boring, well-supported solutions over novelty.

## 12. Coding standards

- Use the language’s strict type and validation options.
- Keep functions and modules focused on one business responsibility.
- Prefer explicit data flow and descriptive names over clever shortcuts.
- Validate all information at system boundaries, even if the interface already validated it.
- Represent expected business failures as clear outcomes; reserve unexpected exceptions for genuine faults.
- Do not use floating-point arithmetic for money.
- Use database transactions for actions that must succeed together.
- Make important commands idempotent so safe retries cannot duplicate results.
- Keep time, timezone, currency, and locale handling explicit.
- Use structured, searchable logs with request and activity identifiers; never expose protected data.
- Write comments for reasons, business rules, and non-obvious trade-offs—not to repeat the code.
- Avoid premature generalisation, hidden global state, large multipurpose modules, and circular dependencies.
- Keep external providers behind adapters with documented failure behaviour.
- Enforce formatting, static analysis, tests, and dependency checks automatically.
- Track important architectural choices in short decision records.
- Consider code complete only when it is readable, tested, observable, documented where needed, and safe to operate.

Exact formatter, linter, coverage, and file-layout rules will be selected with the approved technology stack and added without weakening these standards.

## 13. Testing philosophy

Testing is evidence that the product protects real operations. It is not a target number or a final phase.

- Start each feature with business examples and acceptance conditions.
- Use many fast unit tests for calculations, state transitions, and Capability rules.
- Use integration tests for database constraints, transactions, live updates, and external boundaries.
- Use a smaller set of end-to-end tests for critical staff journeys.
- Test contracts for fiscal, payment, accounting, printing, and other integrations.
- Test migrations against realistic data shape and volume before production.
- Test accessibility and responsive behaviour on agreed devices and browsers.
- Test concurrent edits, repeated taps, slow requests, disconnections, retries, and partial external failure.
- Test every money rule with boundaries, refunds or reversals where supported, and historical price changes.
- Test that forbidden actions remain forbidden for each role.
- Verify backup restoration, not merely backup creation.
- Use staff acceptance sessions and venue pilots to test usability under real conditions.
- Turn production defects into regression tests where practical.
- Keep tests deterministic, independent, readable, and based on controlled data.

High coverage in critical rules matters more than uniform coverage. No percentage can replace tests of the risks that could lose an order, corrupt a bill, expose data, or stop a shift.

## 14. Future modules

Future modules are options, not current commitments. Each requires discovery, business value, risk assessment, and explicit approval.

### Operations

- reservations and advance deposits;
- advanced venue maps and seasonal layouts;
- Zone Templates such as Weekday, Weekend, Full Capacity, Private Event, and Wedding;
- waiter sections, shifts, and handovers;
- queues, runners, and delivery confirmation;
- multi-course timing and preparation coordination;
- controlled offline operation for unreliable connectivity.

### Commerce

- bill splitting and partial payments;
- tips and service charges;
- discounts, promotions, packages, and minimum consumption;
- customer loyalty and profiles;
- customer-facing QR ordering and payment;
- gift cards and prepaid credit.

### Back office

- stock, recipes, wastage, purchasing, and suppliers;
- staff scheduling and performance insights;
- accounting exports and reconciliation;
- fiscal devices, receipt printers, and payment terminals;
- advanced reporting, forecasting, and anomaly detection.

### Platform growth

- multi-venue organisations;
- central menu and pricing with venue overrides;
- franchise or group-level reporting and governance;
- documented external API, webhooks, and approved integration marketplace;
- modular language and country-specific fiscal support.

## 15. AI collaboration guidelines

AI may assist with discovery, design, documentation, implementation, testing, review, and support. It does not replace product ownership, professional legal or accounting advice, security accountability, or human approval for production decisions.

### Required behaviour

- Give AI the approved requirements, relevant files, constraints, and acceptance conditions before asking for changes.
- Ask AI to inspect existing work before proposing or editing anything.
- Keep AI tasks narrow, reviewable, and reversible.
- Require AI to state assumptions, uncertainty, files changed, and verification performed.
- Require human review for domain rules, Capabilities, security, money, data migration, infrastructure, and releases.
- Run normal automated checks on AI-produced work; AI claims are not evidence that tests passed.
- Never provide production secrets, passwords, payment details, or unnecessary personal data to an AI system.
- Use anonymised or synthetic examples whenever possible.
- Verify licenses, provenance, and security before accepting generated dependencies, assets, or copied material.
- Record material AI-assisted architectural decisions through the same process as human proposals.
- Reject changes that are unexplained, overly broad, or inconsistent with the domain language.
- Do not allow AI to deploy, delete production data, change access, or perform irreversible external actions without explicit authorised human approval.

### Collaboration prompt standard

A useful task request should state:

- the business outcome;
- the files and systems in scope;
- what must not change;
- relevant domain rules;
- acceptance checks;
- whether implementation is authorised;
- the expected form of the response.

### Review standard

The reviewer remains responsible for understanding the change. If a reviewer cannot explain why AI-generated code is correct and safe, the change is not ready.

## 16. Long-term scalability

Scalability means more than handling traffic. Emerald must be able to grow in data, users, venues, features, integrations, and team size without losing clarity or reliability.

### Application growth

- Begin with a modular single application whose business areas have clear ownership and boundaries.
- Keep domain logic independent from presentation and external providers.
- Use internal contracts and events deliberately, not as a reason to create early distributed services.
- Separate a module into its own service only when measured load, reliability isolation, deployment independence, or team ownership clearly requires it.

### Data growth

- Give core records stable identifiers and explicit venue ownership from the start.
- Plan indexes, pagination, archiving, and reporting around growing transaction history.
- Keep financial and activity records durable while applying approved retention to unnecessary data.
- Evolve database structures through tested, versioned, backward-compatible steps where practical.
- Separate heavy reporting workloads from live operations when measurement shows contention.

### Venue and regional growth

- Model venue timezone, currency, language, tax, preparation destinations, and business-date rules explicitly.
- Isolate each venue’s operational data and enforce access boundaries.
- Allow organisation-wide standards with controlled venue-specific configuration.
- Keep country-specific fiscal behaviour outside the universal order and bill core.

### Traffic and availability growth

- Keep application instances replaceable and avoid relying on local memory for official state.
- Scale common read and live-update paths only from measured demand.
- Introduce queues, replicas, caching, or service separation when the simpler design no longer meets agreed targets.
- Protect the system with capacity testing, rate limits, back-pressure, monitoring, and graceful degradation.
- Ensure a non-critical reporting or external integration failure cannot stop core order taking and billing.

### Organisational growth

- Maintain clear module ownership, domain language, decision records, onboarding material, and operational runbooks.
- Keep interfaces documented and compatibility expectations explicit.
- Automate build, test, security, deployment, observability, and recovery checks as the team grows.

### Scalability rule

Do not pay today for imagined scale, but do not close tomorrow’s path. Prefer designs that are simple now and have known, testable evolution points.

## 17. Governance and evolution

This blueprint should be reviewed:

- before the first implementation begins;
- before adding a major module or external integration;
- before changing core domain or financial rules;
- before expanding to another venue or country;
- after a serious operational or security incident;
- at least once each year during active product development.

Every material amendment should record the date, decision owner, reason, and affected sections. Minor wording clarifications may be made without changing intent, but domain definitions and principles require explicit review.

## 18. Definition of enduring success

Emerald succeeds when staff trust it during the busiest shift, owners trust its records after the shift, customers receive faster and more accurate service, and the product can evolve without sacrificing correctness, clarity, security, or accountability.
