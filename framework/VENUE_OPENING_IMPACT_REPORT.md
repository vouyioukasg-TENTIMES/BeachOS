# Venue Opening Decision — Documentation Impact Report

## Decision Recorded

DEC-039 — Require confirmed readiness before daily Venue opening.

Status: Accepted.

Date: 2026-07-25.

## Documents Changed

### `docs/DECISIONS.md`

Changed to preserve the accepted decision, its context, alternatives, reasoning, consequences, and review trigger.

### `framework/04 Workflows/VENUE_OPENING_WORKFLOW.md`

Created to describe the complete technology-independent operating workflow, departmental responsibility, Host coordination, readiness states, opening sequence, forbidden outcomes, recovery boundary, and operational review.

### `docs/PRODUCT_REQUIREMENTS.md`

Changed only where daily Venue opening affects product behaviour. The requirements now cover department declarations, the Host’s Opening Dashboard, the all-ready gate, OPEN VENUE, activities forbidden before opening, effects after opening, and the permanent Opening Report.

### `docs/DOMAIN_MODEL.md`

Changed because DEC-039 introduces business concepts and invariants that the previous model did not contain:

- Operational Department;
- Department Readiness;
- daily Venue opening;
- Opening Report;
- the rule that guest arrivals, new Customer Groups, and Orders are forbidden before opening;
- the relationship between department verification and Host coordination.

The update is limited to the affected Venue lifecycle and rules, two new domain entities, two Domain Events, and glossary definitions.

## Documents Intentionally Unchanged

### `docs/ARCHITECTURE.md`

No technical structure or implementation approach was requested or approved.

### `docs/DEVELOPMENT_PLAN.md`

The decision establishes product and operational behaviour but does not assign it to a delivery phase in this task.

### `docs/MASTER_BLUEPRINT.md`

Existing principles remain compatible. No enduring architecture or product principle changed.

### `docs/PRODUCT_PHILOSOPHY.md`

The workflow follows Operations First, explicit rules, human responsibility, accountability without punishment, and operational continuity. No philosophy change was needed.

### `docs/MISSION_AND_VALUES.md`

The decision supports operational clarity and owner confidence without changing the Mission or Values.

### `docs/PRODUCT_VISION.md`

The long-term business vision remains valid.

### `docs/PROJECT_GLOSSARY.md`

The new terms should be considered in a future approved glossary-alignment task. They were not added here because the requested direct updates were the Decision Log, affected Framework material, Product Requirements, and the Domain Model only where required.

### Historical review and update reports

`docs/DOMAIN_REVIEW_REPORT.md`, `docs/NFC_DOCUMENTATION_UPDATE_REPORT.md`, `docs/PRODUCT_REVIEW_UPDATE_REPORT.md`, `docs/PRODUCT_PHILOSOPHY_REVIEW.md`, `docs/GLOSSARY_REVIEW.md`, and `docs/MISSION_REVIEW.md` remain unchanged as historical records.

### Repository and engineering files

Root policies, application configuration, infrastructure, scripts, tests, and GitHub files remain unchanged because this was a documentation-only business decision.

## Existing Decisions Preserved

- DEC-035 remains unchanged: the Responsible Waiter, not the Host, officially opens a Customer Group.
- DEC-038 remains unchanged: Roles describe responsibilities, while Capabilities authorize protected actions.
- Venue opening performs no Customer Group, Order, transfer, Billing, or Payment action.
- Department readiness verification remains with each department’s responsible person; the Host coordinates the complete opening.
