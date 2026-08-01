# Emerald Management System — Technical Architecture Proposal

## 1. Purpose

This document proposes how the system can be built. It uses simple language and avoids locking the project into a final technology choice before the requirements are approved.

The main recommendation is one responsive web application connected to one central server and database. Staff would open it in a browser on a phone, tablet, or desktop computer.

## 2. Proposed shape of the system

The system has four main parts:

1. **Staff web application** — screens for waiters, cashiers, managers, bar staff, and kitchen staff.
2. **Application server** — applies business rules, Capabilities, order routing, transfers, payments, and bill calculations.
3. **Central database** — safely stores users, venue locations, menu data, customer groups, orders, tickets, bills, payments, and history.
4. **Live update service** — quickly shows new orders and status changes on other devices without constant manual refreshing.

The bar and kitchen views are parts of the same application, with different responsibilities, explicit Capabilities, and simplified screens.

## 3. Why a responsive web application

- It can serve phones, tablets, and desktop computers from one codebase.
- Updates can be placed on the server without installing a new app on every device.
- It is suitable for an internal venue system.
- It keeps the first version simpler than building separate iPhone, Android, tablet, and desktop applications.

The application may later be made installable from the browser for a more app-like experience. Full offline operation should be treated as a separate decision.

## 4. Recommended technical approach

The exact tools will be selected only after document approval. A practical starting proposal is:

- a modern, well-supported web framework using TypeScript for the screens and server;
- a PostgreSQL relational database for accurate linked business records;
- secure browser sessions for login;
- server-sent events or WebSockets for live order and status updates;
- container-based deployment to keep development and production consistent;
- automated database backups and application monitoring.

Keeping the first version as one well-organised application is recommended. Separate small services would add operational complexity without a clear early benefit. The code can still be divided into clear business areas so parts can be separated later if scale requires it.

## 5. Main business areas

The application should be divided into these clear areas:

- **Accounts and Capabilities** — login, users, Roles, explicit Capabilities, and allowed actions. Roles do not directly authorize actions.
- **Venue** — physical Areas, Rows, sunbed sets, tables, stable Service Location Digital Identities, availability, dynamic Zones, and Responsible Waiter.
- **Menu and pricing** — categories, items, destinations, prices, and row charges.
- **Customer groups** — primary operational ownership of occupancy, opening, Responsible Waiter, Orders, optional Bill, Payments through that Bill, History, and transfer.
- **Orders** — draft orders, submitted items, notes, and later rounds.
- **Preparation** — separate bar and kitchen tickets and their statuses.
- **Billing** — running totals, charges, discounts, corrections, and balance.
- **Payments** — payment records and bill closing.
- **Reporting and history** — daily summaries and a record of sensitive actions.

Each area should have its rules enforced by the server. A user must not be able to bypass a rule by changing something in the browser.

## 6. Important information to store

The central database will need records similar to the following:

- users, roles, and user-role assignments;
- venue areas, rows, and locations;
- row-charge price history;
- menu categories, menu items, item prices, and preparation destinations;
- active and closed customer groups;
- location and responsible-waiter history;
- orders, order items, and item notes;
- preparation tickets and status history;
- bill entries, adjustments, and totals;
- payments and payment methods;
- activity-history entries.

Financial values should be stored as exact currency amounts, never as approximate decimal calculations. Important prices should be copied onto each order or bill entry when it is created so that later price changes do not rewrite history.

Records that affect money or accountability should normally be cancelled or corrected with a new history entry, not silently deleted.

## 7. Key safety rules

The database and server should jointly enforce these rules:

- one active customer group per location;
- exactly one responsible waiter per active customer group;
- only the Responsible Waiter intentionally opens a Customer Group; a Host or Cashier does not;
- a Customer Group may exist without a Bill;
- a Bill is created only when the first approved financial obligation exists;
- opening at a Beach Sunbed immediately creates the approved Beach Sunbed obligation, while NFC or manual identification creates nothing;
- each submitted Order is one ordering round, and one Customer Group may have many Orders aggregated by its Bill;
- dynamic Zones are independent from physical Areas and do not determine charges;
- an order submission creates the Bill Lines and any applicable preparation Tickets together;
- a transfer releases the old location and occupies the new one together;
- a destination cannot receive a transfer if it is occupied;
- a payment is never accidentally recorded twice;
- a bill cannot close with a remaining balance unless an authorised exception is recorded;
- closed financial records cannot be silently changed;
- menu or row-price changes do not alter existing bills.

“Together” means either the complete action succeeds or none of it does. This protects the system if two staff members act at the same time or a connection drops.

## 8. Order routing and live updates

When a waiter sends an order:

1. The server checks the Staff Member, required Capability, location, group status, item prices, and business rules.
2. It saves the submitted order and bill entries.
3. It creates separate preparation tickets for bar and kitchen items.
4. It confirms success to the waiter only after the information is safely saved.
5. It sends a live notice to the relevant bar, kitchen, waiter, and cashier screens.

The database remains the official source of information. Live notices only tell screens that something changed. If a live connection is interrupted, a screen can reload the correct state from the server.

For the first version, database-backed preparation tickets should be enough. A separate message-queue system can be added later only if real usage shows a need.

## 9. Capabilities and activity history

Roles group business responsibilities but do not directly authorize actions. Protected actions require explicit Capabilities in an approved context. For example, two Staff Members with the same Role may hold different Capabilities, and a Capability never bypasses a business rule such as the requirement that only the Responsible Waiter opens a Customer Group.

The activity history should record at least:

- sign-in events and important failed access attempts;
- responsible-waiter changes;
- location transfers;
- submitted, cancelled, or corrected order items;
- discounts and manual price changes;
- payments, reversals, closing, and reopening;
- menu, Row-charge, Role, and Capability changes.

Each entry should include who acted, what changed, and when. For important changes it should include the previous and new values.

## 10. Security and privacy

- Use encrypted HTTPS connections.
- Store passwords using a modern one-way password method; never store readable passwords.
- Use short-lived, secure login sessions and allow managers to disable accounts promptly.
- Check explicit Capabilities and business rules for every protected action.
- Limit login attempts and record suspicious activity.
- Keep customer personal data to a minimum.
- Keep secrets outside the source code.
- Apply security updates regularly.
- Agree how long financial and activity records must be kept under applicable Greek and EU requirements.

A legal or accounting specialist should confirm fiscal, receipt, tax, and record-retention obligations. The software design alone is not legal advice.

## 11. Reliability, backups, and recovery

- The production database should have automated daily backups, with more frequent protection considered after usage is known.
- Backups should be encrypted and stored separately from the main server.
- A restore test must be completed before launch and repeated on a schedule.
- Errors, server health, storage use, and failed backups should be monitored.
- Important operations should carry a unique request identifier so an accidental repeat does not create duplicate orders or payments.
- The application should show clear connection and saving states to staff.

The owner should choose acceptable recovery targets. A starting discussion point is no more than one business day of data loss from a major disaster and restoration within several hours, but a busy venue may require stronger protection.

## 12. Connectivity approach

The proposed first version requires a connection to the central server. Before launch, the venue’s Wi-Fi coverage should be tested at the beach, pool, upper tables, bar, kitchen, and cashier position.

Recommended operational safeguards include:

- reliable business Wi-Fi with full venue coverage;
- a backup internet connection, such as mobile data;
- clear on-screen warning when a device is disconnected;
- no false “order sent” message while a save is unconfirmed.

A local venue server or full offline mode may be considered if connectivity testing shows that an online system is not dependable. That choice affects cost, maintenance, and data synchronisation and should not be added casually.

## 13. Environments and release process

Use separate environments:

- **Development** — where features are built.
- **Test / staging** — a safe copy for owner and staff testing with non-live data.
- **Production** — the real system used at the venue.

Changes should be checked automatically before release. Database changes should be versioned and reversible where practical. Production access should be limited and releases recorded.

## 14. Testing approach

Testing should cover:

- bill, tax, charge, and payment calculations;
- Capabilities independently from Roles;
- bar and kitchen routing;
- repeated taps and slow connections;
- two staff members changing the same group at once;
- complete and failed transfers;
- price changes without changes to old bills;
- phone, tablet, and desktop layouts;
- backup restoration;
- the full real-life workflow during a staff pilot.

Automated tests should protect important money and transfer rules. Manual testing with actual venue staff remains essential because speed and clarity cannot be judged from code alone.

## 15. Decisions still needed

Before the architecture is final, confirm:

- online hosting versus a local venue server;
- the quality of Wi-Fi and internet coverage;
- required Greek fiscal, receipt-printer, and card-terminal integrations;
- payment, tax, discount, and bill-splitting rules;
- required languages;
- expected number of staff devices and busiest order volume;
- required data retention and backup targets;
- whether the application must work when fully offline;
- which reports and exports accounting needs.

## 16. Architecture recommendation summary

Start with one responsive web application, one application server, and one PostgreSQL database. Use clear internal business areas, strict server-side rules, live screen updates, full activity history for sensitive actions, and tested backups. Confirm connectivity and fiscal requirements early because those findings may materially change the design.
