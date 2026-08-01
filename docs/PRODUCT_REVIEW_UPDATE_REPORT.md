# Emerald Management System — Product Architecture Review Update Report

## 1. Outcome

The approved Product Architecture Review decisions have been incorporated into the project documentation.

The current business model now consistently states that:

- Customer Group is the primary operational entity;
- Service Location Digital Identity remains stable and technology-neutral;
- Zones are dynamic operational groupings independent from physical layout;
- a Customer Group may exist without a Bill;
- a Bill is created only when the first approved financial obligation exists;
- opening a Customer Group at a Beach Sunbed immediately creates the approved obligation and Bill;
- NFC and manual location identification perform no operational or financial action;
- only the Responsible Waiter officially opens a Customer Group;
- each submitted Order is one ordering round and one Customer Group may have many Orders;
- Zone Templates are a future capability;
- Roles group responsibilities while explicit Capabilities authorize protected actions.

No application code, implementation file, dependency, API, database model, schema, migration, NFC integration, or user-interface screen was created or changed.

## 2. Files modified

### Required current-reference documents

#### `docs/DOMAIN_MODEL.md`

- Made Customer Group the owner of Service Location, Orders, optional Bill, Payments through that Bill, Responsible Waiter, and History.
- Removed Visit as a core entity, core relationship, lifecycle owner, and domain event.
- Retained Visit only as an optional future concept requiring a distinct approved purpose.
- Replaced geographical Zone meaning with dynamic operational grouping.
- Added Zone Template as a fully described future domain concept.
- Added Capability as a separate domain entity.
- Reworked Role so it never directly authorizes actions.
- Changed Bill creation to the first approved financial obligation.
- Added the immediate Beach Sunbed obligation at intentional Customer Group opening.
- Made every Order one ordering round under the Customer Group.
- Updated Service Location, Order, Ticket, Bill, Activity Log, Shift, events, relationships, examples, and glossary terms.
- Added or clarified Beach Sunbed, Capability, History, Host, Master User, Physical Row, Zone, and Zone Template glossary definitions.
- Verified that the existing Service Location Digital Identity and NFC rules remain unchanged in meaning.

#### `docs/DECISIONS.md`

Added eight Accepted decisions using the next available IDs:

- DEC-031 — Make Customer Group the primary operational entity.
- DEC-032 — Make Zones dynamic operational groupings.
- DEC-033 — Create a Bill only when a financial obligation exists.
- DEC-034 — Apply the Beach Sunbed obligation when the waiter opens the group.
- DEC-035 — Only the Responsible Waiter opens a Customer Group.
- DEC-036 — Treat each submitted Order as one ordering round.
- DEC-037 — Define Zone Templates as a future capability.
- DEC-038 — Authorize actions through Capabilities, not Roles.

DEC-030 remains the accepted Service Location Digital Identity decision and was verified for consistency. DEC-038 clarifies that DEC-014’s central enforcement rule now uses Capability as the approved business authorization term.

#### `docs/MASTER_BLUEPRINT.md`

- Added capability-based authority as a Core Principle.
- Updated identity and access definitions for Role and Capability.
- Defined dynamic Zone and future Zone Template.
- Replaced Visit-based Customer Group wording.
- Made Bill optional until the first obligation.
- Documented waiter-only opening and the immediate Beach Sunbed obligation.
- Preserved NFC as identification only.
- Updated essential relationships, security, testing, development, and AI-review terminology from generic Role permissions to Capabilities.
- Added Zone Templates to future operations.

#### `docs/PRODUCT_REQUIREMENTS.md`

- Added Host and Master responsibilities.
- Separated Roles from Capabilities.
- Added occupied-without-Bill as a valid state.
- Added dynamic Zone requirements and future Zone Template boundaries.
- Made Responsible Waiter mandatory for every active Customer Group.
- Reserved official Customer Group opening for the Responsible Waiter.
- Made Bill creation depend on the first approved financial obligation.
- Added immediate Beach Sunbed obligation and Bill creation at official opening.
- Preserved NFC and manual lookup as identification-only actions.
- Defined multiple Orders as separate ordering rounds aggregated by one Bill.
- Updated transfers, management functions, example flow, owner questions, and first-version acceptance wording.

#### `docs/DEVELOPMENT_PLAN.md`

- Replaced Role-permission work with separate Role and Capability work.
- Added dynamic Zone management and acceptance checks to Venue setup.
- Added explicit protection of Service Location identity during Zone reassignment.
- Added waiter-only Customer Group opening, optional Bill state, first-obligation Bill creation, and immediate Beach Sunbed charging to the billing phase.
- Added multi-round Order acceptance checks.
- Updated transfer scope to include the complete Customer Group and optional Bill.
- Added Zone Templates to later improvements only.

### Additional affected documentation aligned for consistency

#### `docs/ARCHITECTURE.md`

- Replaced Role-based permission language with Capability-based authorization.
- Added dynamic Zones, stable Service Location Digital Identity, Customer Group ownership, optional Bill creation, waiter-only opening, Beach Sunbed obligation, and ordering rounds to the architectural business boundaries and safety rules.

#### `docs/PRODUCT_VISION.md`

- Replaced cross-venue “permissions” wording with capability-based authorization.

#### `docs/DOMAIN_REVIEW_REPORT.md`

- Added a prominent historical-status notice explaining that DEC-031 through DEC-038 supersede the relevant earlier findings and questions.
- Preserved the report body as review history rather than rewriting the earlier analysis.

#### `docs/NFC_DOCUMENTATION_UPDATE_REPORT.md`

- Added a historical update note linking the later Customer Group, Zone, and Capability decisions.
- Clarified that the previously open Customer Group-versus-Visit and Zone findings are now resolved while the accepted NFC decision remains unchanged.

#### `docs/PRODUCT_REVIEW_UPDATE_REPORT.md`

- Created this documentation change report.

## 3. Decisions incorporated

### DEC-A — Customer Group is primary

Incorporated as DEC-031. Customer Group now owns the complete operational context. Visit is absent from the core model and may return only as a separately approved future concept.

### DEC-B — Stable Service Location Digital Identity

Verified against DEC-030, the Domain Model, Blueprint, Requirements, Development Plan, and NFC update report. No contradiction was found and no business meaning was changed.

### DEC-C — Dynamic Zones

Incorporated as DEC-032. Zone no longer represents geography. Area and Physical Row retain physical meaning; Zone may group arbitrary Service Locations within one Venue.

### DEC-D — Delayed Bill creation

Incorporated as DEC-033. Customer Group opening alone does not create a Bill. The first approved financial obligation does.

### DEC-E — Immediate Beach Sunbed obligation

Incorporated as DEC-034. The obligation arises when the Responsible Waiter intentionally opens the Customer Group at a Beach Sunbed. This first obligation creates the Bill. Location identification alone creates nothing.

### DEC-F — Responsible Waiter opens service

Incorporated as DEC-035. Host and Cashier may not officially open a Customer Group. Host may escort and organize seating.

### DEC-G — Multiple ordering rounds

Incorporated as DEC-036. Every submitted Order is one preserved ordering round. The Customer Group’s Bill aggregates all approved rounds after the Bill exists or is created by the first ordered item.

### DEC-H — Future Zone Templates

Incorporated as DEC-037. Templates may later create the initial daily Zone arrangement before service while preserving manual reassignment. They are explicitly outside the first version.

### DEC-I — Capability-based authorization

Incorporated as DEC-038. Roles communicate responsibilities; Capabilities explicitly authorize actions. Neither a Role nor a Capability bypasses business rules.

## 4. Contradictions removed

The refactor removed these contradictions:

1. **Customer Group versus Visit:** Customer Group is now the only core operational lifecycle owner.
2. **Occupancy owner:** An active Customer Group, not a Visit, occupies a Service Location.
3. **Opening events:** Customer Group Opened is the core event; Visit Opened was removed.
4. **History and transfer:** Orders, optional Bill, Payments, Responsible Waiter, and History remain with the Customer Group during transfer.
5. **Zone geography:** Zone no longer belongs to Area or defines physical position.
6. **Zone charging:** Dynamic Zone membership does not create or change Beach Sunbed charges; Physical Row remains independent.
7. **Zone deletion:** Deleting a Zone no longer risks deleting or relocating Service Locations.
8. **Bill at group opening:** Customer Group may exist without a Bill.
9. **Beach Sunbed exception:** Official opening at a Beach Sunbed creates the immediate obligation and therefore the Bill.
10. **NFC side effects:** NFC and manual lookup remain identification only and cannot start service or create money.
11. **Opening responsibility:** Responsible Waiter, not Host or Cashier, officially opens the Customer Group.
12. **Ordering rounds:** Later Orders no longer appear to edit one continuing Order; every round is separate and aggregates financially.
13. **Role authority:** Role no longer directly implies authority; Capability is explicit and independently reviewed.
14. **Waiter scope:** Every active Customer Group has exactly one Responsible Waiter, including groups at upper tables.
15. **Historical review reports:** Both earlier reports now clearly identify which findings were later resolved.

## 5. Remaining business questions

The approved review decisions are fully reflected. The following questions remain outside those decisions and should be answered before their affected features are implemented:

1. May one Service Location belong to more than one active Zone at the same time, or exactly one?
2. Who may grant and revoke each Capability, and which grants require a second approval?
3. What is the complete initial Capability catalog and the allowed scope of each Capability?
4. What exact handover process changes the Responsible Waiter, and must the receiving waiter accept?
5. Which transfer source and destination combinations are allowed among beach sunbeds, pool sunbeds, and upper tables?
6. What happens financially when a Customer Group transfers to a differently priced Physical Row?
7. What obligation arises if an existing Customer Group transfers into a Beach Sunbed after it was originally opened elsewhere?
8. Do Pool Sunbeds have an immediate opening charge, a different first-obligation rule, or no location charge?
9. When may the immediate Beach Sunbed obligation be waived, reduced, or replaced by minimum consumption?
10. What are the exact Bar and Kitchen Ticket states and what does Ticket completion mean?
11. Which Capabilities and approvals govern Order Item cancellation and correction?
12. Are partial Payments, split Payments, overpayment, cash change, tips, refunds, and Payment reversals required?
13. What exact conditions complete a Customer Group and release its Service Location after Bill closing?
14. May a Bill close with a non-zero Balance under any exception?
15. Does Shift belong in the first version, and what handover rule applies when a waiter’s Shift ends?
16. What is the Venue’s Business Date boundary?
17. Which reports, languages, devices, browsers, and connectivity standards are required for launch?
18. Which fiscal, receipt, card-terminal, accounting, privacy-retention, and legal rules apply?

## 6. Recommendations before implementation

1. Conduct one focused owner session on remaining questions 1–15 before building Customer Group, Zone, transfer, preparation, billing, Payment, or authorization behaviour.
2. Approve a complete Capability catalog with plain-language action definitions before account and authorization work.
3. Write acceptance examples for Customer Groups at Beach Sunbeds, Pool Sunbeds, and Upper Tables, including cases with no Bill and first-Order Bill creation.
4. Write transfer examples covering every allowed physical source and destination and the resulting charge.
5. Define Customer Group completion separately from Bill closing so Service Location release is unambiguous.
6. Keep Zone Templates outside first-version scope until dynamic manual Zones have been tested in real operation.
7. Run a short final consistency review after the remaining high-risk financial and lifecycle questions are approved.

## 7. Current readiness

The approved decisions remove the earlier structural ambiguity around Customer Group, Visit, Zone, Bill creation, opening responsibility, ordering rounds, and authorization.

The domain is now suitable for detailed workflow and acceptance-example design. Implementation of high-risk business features should still wait for the remaining transfer, charge, Ticket completion, Payment, Capability governance, and Customer Group completion rules listed above.

## 8. Stop point

The documentation refactor is complete. The project should stop here and wait for human review before any application implementation begins.
