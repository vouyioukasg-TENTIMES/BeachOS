# Emerald Management System — Phased Development Plan

## 1. Purpose

This plan describes a careful path from requirements to live use. No application should be generated and no packages should be installed until the owner reviews and approves the planning documents.

Dates will be estimated after the open questions, team size, integrations, and first-version scope are agreed.

## Phase 0 — Owner review and discovery

### Work

- Review `PRODUCT_REQUIREMENTS.md` with the owner and key staff.
- Walk through a real shift from opening a sunbed to closing its bill.
- Map every beach sunbed set, pool sunbed set, upper table, and row.
- Confirm Staff Member Roles, explicit Capabilities, and sensitive business rules independently.
- Confirm row-charge, transfer, payment, tax, discount, correction, and closing rules.
- Confirm language, reporting, printing, fiscal, and card-terminal needs.
- Test Wi-Fi and internet coverage throughout the venue.
- Identify the phones, tablets, computers, browsers, kitchen displays, and bar displays to support.
- Decide which features belong in the first version and record later ideas separately.

### Result

- Approved requirements and architecture decisions.
- A confirmed first-version scope.
- A venue map and initial menu/pricing data.
- A list of integrations and legal/accounting requirements.

### Approval point

The owner approves the documents before any application setup or coding begins.

## Phase 1 — Experience design and technical foundation

### Work

- Create simple screen sketches for phone, tablet, bar, kitchen, cashier, and manager use.
- Test the sketches with actual staff and reduce unnecessary steps.
- Define the status words, colours, language, and touch-friendly controls.
- Select the exact technical tools and hosting approach.
- Set up the project, database structure, test environment, automated checks, security basics, and deployment process.
- Prepare safe sample data based on the venue layout and menu.

### Result

- Approved screen flow and visual direction.
- A working but non-production technical foundation.
- Documented setup and release instructions.

### Acceptance check

The owner and representative staff can understand and approve the proposed screens before full feature development.

## Phase 2 — Accounts, Roles, Capabilities, Zones, and Venue setup

### Work

- Build sign-in and sign-out.
- Build user, Role, and explicit Capability management without making Roles directly authorize actions.
- Build areas, rows, sunbed sets, upper tables, and location availability.
- Build dynamic operational Zones that can contain any Service Locations in one Venue, independently from physical Areas.
- Allow a Master user with the Manage Zones Capability to create, rename, delete, and reassign Zones without changing Service Location identity or history.
- Add one stable Digital Identity for every Service Location.
- Add NFC as the preferred initial way for signed-in, authorised staff to identify and open a Service Location’s current context.
- Keep manual identification by visible location name or number available for the same Service Locations.
- Build the responsive venue view.
- Assign and change exactly one Responsible Waiter per active Customer Group according to approved Capability and handover rules.
- Start the activity history for sensitive changes.

### Result

Staff can sign in, see the correct functions, identify Service Locations by NFC or manual lookup, view the venue, and manage responsibility safely.

### Acceptance check

Test Staff Members can perform only actions covered by their explicit Capabilities, changing a Role alone does not silently grant a Capability, and two active Customer Groups cannot occupy the same Service Location.

Zone acceptance checks:

- A Master user with Manage Zones can create, rename, and delete an operational Zone.
- A Staff Member without Manage Zones cannot change Zone structure or assignments.
- A Zone can contain an arbitrary selection of Service Locations from different Areas in the same Venue.
- A Service Location can be reassigned without changing its visible identity, Digital Identity, physical Area, active Customer Group, Orders, optional Bill, Responsible Waiter, or history.
- Deleting a Zone leaves every Service Location intact and does not change any financial rule.

NFC and location-identification acceptance checks:

- Tapping a location’s active NFC tag opens the correct Service Location and displays current information retrieved from the central system.
- An active tag cannot open the wrong Service Location and cannot resolve to more than one Service Location.
- An unauthorised or signed-out user cannot perform a protected action after identifying a location.
- Tapping NFC does not automatically create a Customer Group, Bill, charge, Order, transfer, Payment, or other business action; the Responsible Waiter still opens the Customer Group and confirms any resulting charge.
- Manual lookup by visible name or number reaches the same Service Location as its NFC identification.
- Missing, damaged, unavailable, unsupported, or replaced NFC does not stop normal operation through manual lookup and does not change the Service Location’s identity or history.
- Inspection confirms that the NFC tag contains no current Customer Group, Responsible Waiter, price, Bill, Order, customer, Capability, or other changing or sensitive business data.

## Phase 3 — Menu, order taking, bar, and kitchen

### Work

- Build menu categories, items, prices, and preparation destinations.
- Build quick mobile order entry, search, quantities, and notes.
- Build draft review and safe order submission.
- Preserve every submitted Order as one ordering round and allow multiple Orders under one Customer Group.
- Separate submitted items into bar and kitchen tickets.
- Build focused bar and kitchen screens with agreed statuses.
- Send live status updates to relevant staff screens.
- Add protection against duplicate submission and poor connections.

### Result

A waiter can safely send a mixed order, with drinks shown at the bar and food shown in the kitchen.

### Acceptance check

Staff complete realistic Orders, including several later rounds under one Customer Group, notes, repeat taps, slow connections, cancellations, and Capability checks. No earlier round is overwritten and no item is lost, duplicated, or sent to the wrong preparation area.

## Phase 4 — Customer Group opening, Bills, sunbed charges, and transfers

### Work

- Allow only the Responsible Waiter with Open Customer Group to intentionally open a Customer Group. A Host or Cashier may not officially start service.
- Keep NFC and manual Service Location identification separate from Customer Group opening and all financial actions.
- Allow a Customer Group to exist without a Bill.
- Create the Bill only when the first approved financial obligation exists.
- When the Responsible Waiter opens a Customer Group at a Beach Sunbed, immediately create the approved Beach Sunbed obligation and therefore the Bill.
- Apply the approved row-based sunbed-charge rules.
- Aggregate approved financial obligations from every submitted ordering round into the same Customer Group Bill.
- Preserve the original item prices and charges on existing bills.
- Show clear bill details and totals.
- Transfer a complete Customer Group, including its Orders, optional Bill, Payments, Responsible Waiter, and History, to an available approved destination.
- Protect transfers from conflicts when multiple staff act at once.
- Record charge changes, corrections, responsible-waiter changes, and transfers in history.

### Result

Each active Customer Group has the correct financial state, including no Bill before its first obligation where allowed, and an authorised Staff Member with the required Capability can safely transfer the complete group.

### Acceptance check

Acceptance checks include:

- Identifying a Service Location does not create a Customer Group, Bill, charge, Order, transfer, or Payment.
- Only the Responsible Waiter can intentionally open the Customer Group; a Host and Cashier cannot.
- Opening at a Beach Sunbed immediately creates the approved obligation and Bill exactly once.
- An allowed Customer Group at another location can remain open without a Bill until its first approved obligation.
- The first ordered item creates the Bill when no earlier financial obligation exists.
- Several Orders remain separate ordering rounds while their approved obligations aggregate into the same Bill.
- Agreed examples for every physical Row and transfer case calculate correctly.
- Failed transfers leave both Service Locations, the Customer Group, its Orders, optional Bill, Responsible Waiter, and History unchanged.

## Phase 5 — Cashier, payments, closing, and reports

### Work

- Build the cashier overview of all open bills.
- Build payment recording with the approved methods and rules.
- Build balance checks and bill closing.
- Build authorised correction, reversal, and reopening flows if approved.
- Make closed bills searchable.
- Build the agreed daily, waiter, item, cancellation, transfer, and payment reports.
- Add export or printing only where it has been approved.

### Result

The cashier can see, settle, and close bills with a reliable activity history and basic reports.

### Acceptance check

All agreed payment examples balance exactly. Bills cannot close incorrectly, duplicate payments are prevented, and closed records remain traceable.

## Phase 6 — Full testing and venue pilot

### Work

- Test complete workflows on the selected phones, tablets, and desktop computers.
- Test with several users working at once.
- Test failures such as weak Wi-Fi, lost connection, repeated taps, and server errors.
- Check security, every explicit Capability, and the rule that Roles do not directly authorize actions.
- Check accessibility, outdoor readability, and touch-target sizes.
- Test monitoring, backups, and restoration.
- Train a small group of staff.
- Run a controlled pilot using real venue workflows.
- Record feedback, fix important problems, and repeat testing.

### Result

A release candidate proven in realistic conditions.

### Acceptance check

The acceptance conditions in `PRODUCT_REQUIREMENTS.md` pass, no critical issues remain, backup restoration succeeds, and the owner approves launch.

## Phase 7 — Launch and early support

### Work

- Load verified live users, venue data, menu items, prices, and row charges.
- Take a final backup and confirm support contacts and fallback procedures.
- Launch at a low-risk time agreed with the owner.
- Provide close support during the first live shifts.
- Watch errors, performance, order delivery, payment balancing, and staff feedback.
- Fix urgent issues and publish a short post-launch review.

### Result

The system is in live use with trained staff, monitored operation, and a clear support process.

### Acceptance check

The owner confirms that daily operations and totals are correct after the agreed stabilisation period.

## Phase 8 — Later improvements

Only prioritise these after real use provides evidence:

- reservations;
- stock and supplier management;
- customer loyalty;
- advanced floor plans;
- bill splitting;
- full offline operation;
- accounting, fiscal, receipt-printer, or card-terminal integrations not required at launch;
- deeper sales and staffing reports;
- customer-facing ordering.
- Zone Templates such as Weekday, Weekend, Full Capacity, Private Event, and Wedding, applied by a Master user before service with later manual reassignment.

Each later feature should receive its own requirements, design, estimate, and approval.

## Work principles for every phase

- Demonstrate small, complete pieces frequently to the owner and staff.
- Keep money, Payment, transfer, and Capability rules covered by automated tests.
- Use realistic but non-sensitive test data outside production.
- Keep a record of decisions and changes to scope.
- Do not hide errors from staff; show whether an action is saving, saved, or failed.
- Do not release a phase merely because it is coded; it must pass its acceptance check.
- Keep a tested recovery path before changing live data or software.

## Decisions that affect schedule and cost

The largest unknowns are:

- fiscal, receipt, card-terminal, and accounting integrations;
- full offline operation;
- split and partial payments;
- advanced visual venue mapping;
- bilingual content and menu management;
- amount and quality of initial venue and menu data;
- required reports and historical-data imports;
- availability of venue staff for testing and training.

These should be settled early. Estimates made before these decisions would be unreliable.

## Immediate next step

The owner should review all three planning documents, answer the open questions, and request any changes. Implementation begins only after explicit approval.
