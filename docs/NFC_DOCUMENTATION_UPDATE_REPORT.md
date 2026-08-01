# Emerald Management System — NFC Documentation Update Report

> **Historical update note — 2026-07-21.** The Customer Group versus Visit and Zone findings described as unresolved in this report were later resolved by DEC-031 and DEC-032. Capability terminology was established by DEC-038. The NFC decision itself remains unchanged and accepted as DEC-030.

## 1. Outcome

The approved Service Location Digital Identity decision has been added to the project documentation.

The enduring business concept is **Service Location Digital Identity**. NFC is documented as the preferred initial staff identification method, not as the Service Location itself and not as the source of current operational information.

No NFC integration, application code, API, database model, migration, or user interface was created.

## 2. Files changed

### `docs/DECISIONS.md`

Changed section:

- Added accepted decision **DEC-030 — Give every Service Location a stable Digital Identity** before the decision-log maintenance rules.

The decision records that:

- every Service Location has one stable Digital Identity;
- NFC is the preferred initial staff interaction;
- the tag contains no changing operational, financial, customer, permission, or other sensitive information;
- the central system remains the source of truth;
- manual lookup remains available;
- QR codes or other suitable methods may resolve the same identity later;
- identification does not bypass authentication, permission, or business rules;
- identification performs no automatic operational or financial action.

### `docs/DOMAIN_MODEL.md`

Changed sections:

- `Service Location` — Purpose.
- `Service Location` — Business description.
- `Service Location` — Lifecycle.
- `Service Location` — Business rules.
- `Service Location` — Relationships.
- `Service Location` — Examples.
- `Service Location` — Future considerations.
- `DOMAIN GLOSSARY` — added `Service Location Digital Identity`.

The physical NFC tag remains an identification method rather than a separate core domain entity. The documentation leaves open the possibility of defining a physical-marker lifecycle later only if real replacement, activation, deactivation, or tamper-management needs justify it.

### `docs/MASTER_BLUEPRINT.md`

Changed sections:

- `Core principles` — added the stable physical-to-digital identity principle.
- `UX principles` — added direct physical-to-digital context, minimal interaction, bright outdoor use, NFC failure recovery, and visible manual fallback principles.

### `docs/PRODUCT_REQUIREMENTS.md`

Changed section:

- Added `4A. Service Location identification` after Venue layout.

The first-version requirements preserve the rule that the Responsible Waiter opens the Customer Group and confirms any resulting sunbed charge. NFC identifies and opens only the Service Location context.

### `docs/DEVELOPMENT_PLAN.md`

Changed section:

- `Phase 2 — Accounts, roles, and venue setup` — Work, Result, and Acceptance check.

NFC identification is now planned for the Venue foundation phase, with acceptance checks for correct identity, permission enforcement, manual equivalence, failure recovery, historical continuity, no automatic action, and absence of sensitive tag data.

### `docs/NFC_DOCUMENTATION_UPDATE_REPORT.md`

Created this report to record the documentation-only change.

## 3. New decision ID

**DEC-030** — Give every Service Location a stable Digital Identity.

Status: **Accepted**  
Date: **2026-07-21**

## 4. Contradictions discovered

No direct contradiction was found with the central-system source-of-truth, authentication, permission, responsible-waiter, Customer Group opening, charging, or manual venue-selection rules.

The approved NFC decision strengthens existing principles rather than replacing them:

- DEC-007 already makes the central system the operational and financial source of truth.
- DEC-014 already requires permissions and business rules to be enforced independently of the interface.
- Product requirements already require the waiter to sign in and open the Customer Group.
- The venue view already provides the basis for manual location selection.

One terminology gap was found and resolved in the changed documents: Service Location previously had a “stable identity” and visible name, but **Service Location Digital Identity** was not explicitly defined. The new decision and glossary entry now distinguish the enduring business identity from the replaceable NFC tag.

At the time of this NFC update, the earlier domain consistency findings were unresolved and intentionally unchanged. Customer Group versus Visit, dynamic Zone meaning, and Capability terminology were subsequently resolved by DEC-031, DEC-032, and DEC-038. Transfer charging, Ticket completion, and several Payment rules remain open.

## 5. Questions still requiring owner approval

The product behaviour approved in DEC-030 is clear. The following operational choices are still needed before NFC implementation, but they do not change the domain decision:

1. Which staff devices and operating environments must support NFC at launch?
2. Should the tag present an opaque identifier or a secure application link as the preferred first-version format?
3. Who may issue, associate, replace, disable, and verify physical NFC tags?
4. What visible marking should help staff confirm the physical tag belongs to the expected Service Location?
5. What staff procedure should apply when a tag appears damaged, missing, moved, duplicated, or tampered with?
6. Should an old tag stop resolving immediately when it is replaced, or is a short controlled replacement period allowed?
7. Should NFC identification be available only inside the signed-in staff application, or may an unsigned user reach a sign-in prompt without seeing location state?
8. Which manual search details are sufficient at launch: visible name, number, Area, Zone, or a combination?
9. Who is responsible for checking all physical tags before a live season or Venue layout change?
10. What evidence must the pilot provide before NFC becomes the preferred daily workflow rather than an optional shortcut?

These questions concern operating policy and later implementation design. None permits sensitive or changing business information to be stored on a tag, removes manual fallback, or allows identification to perform an automatic business action.

## 6. Stop point

The documentation update is complete. The project should wait for human review of DEC-030, the changed sections, and the remaining owner questions before any NFC or application implementation begins.
