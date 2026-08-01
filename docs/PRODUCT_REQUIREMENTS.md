# Emerald Management System — Product Requirements

## 1. Purpose

Emerald Management System will be an internal application for a beach bar in Loutraki, Greece. It will help waiters, bar staff, kitchen staff, and cashiers manage seating, orders, bills, transfers, and payments from one shared system.

This document describes what the first useful version should do. It is a starting point for review, not a final contract.

## 2. Main goals

The system should:

- make order taking quick and clear on a mobile phone or tablet;
- send drinks and food to the correct preparation area;
- keep an accurate running bill for each customer group;
- show which waiter is responsible for each sunbed set;
- apply the correct sunbed charge based on its row;
- allow a complete group and bill to move to another sunbed;
- give the cashier a clear view of open and closed bills;
- work well on mobile phones, tablets, and desktop computers;
- reduce verbal mistakes and uncertainty between staff members.

## 3. Staff responsibilities and Capabilities

Roles describe business responsibilities but do not directly authorize actions. Protected actions require explicit Capabilities, and every business rule still applies. One person may hold more than one Role and may have only the Capabilities approved for their work and Venue.

### Waiter

- signs in with a personal account;
- sees the venue and assigned areas;
- becomes the Responsible Waiter and intentionally opens the Customer Group at a sunbed set or table when holding the Open Customer Group Capability;
- adds items to an order;
- sends orders to the bar and kitchen;
- views the running bill;
- requests or performs an allowed transfer when holding the required Capability;
- requests Payment or closes a Bill when holding the required Capability.

### Host

- escorts customers and helps organize seating;
- coordinates the daily Venue opening process;
- sees the current readiness declared by every mandatory Operational Department;
- may intentionally open the Venue only after every mandatory department is READY and when holding the required Capability;
- is not responsible for personally verifying every department’s work;
- may identify and propose a Service Location;
- does not officially open the Customer Group;
- does not create a Bill or charge by seating or identifying a location.

### Bar staff

- sees drink orders sent to the bar;
- sees the location, waiter, items, notes, and time;
- marks items or a whole ticket as being prepared or ready.

### Kitchen staff

- sees food orders sent to the kitchen;
- sees the location, waiter, items, notes, and time;
- marks items or a whole ticket as being prepared or ready.

### Cashier

- sees all open customer groups and bills;
- sees unpaid totals and their locations;
- records payments;
- closes bills;
- views transfers, corrections, cancellations, and relevant history.

### Manager / Administrator

- manages staff accounts and roles;
- manages venue locations and sunbed rows;
- manages menu items, prices, and whether an item goes to the bar or kitchen;
- manages sunbed charges;
- views reports and activity history;
- performs or approves sensitive corrections.

### Master

- oversees approved Venue configuration and operational setup;
- may manage dynamic Zones when holding the Manage Zones Capability;
- may later manage and apply Zone Templates when that future capability is approved;
- does not receive protected authority from the Role name alone.

Example Capabilities include Open Customer Group, Transfer Customer Group, Assign Waiter, Close Bill, Reopen Bill, Manage Zones, Manage Zone Templates, Manage Menus, Record Payments, and Refund Payments.

## 3A. Daily Venue opening

- The Venue must complete an intentional opening workflow for each Business Date before guest service begins.
- Each mandatory Operational Department has one responsible person for declaring its opening readiness.
- Initial department examples are Kitchen, Bar, Beach Operations, Cleaning, Maintenance, Cashier, and Reception where applicable.
- The Venue must be able to identify which departments are mandatory for its opening.
- Each mandatory department declares exactly one current opening status: READY, NOT READY, or BLOCKED.
- A NOT READY or BLOCKED declaration requires a clear reason.
- The responsible person may add a useful comment to any declaration.
- The Host sees the current status, responsible declaration, delays, blocking issues, reasons, and comments for every mandatory department in one Opening Dashboard.
- The Host coordinates the process but does not personally verify every department.
- OPEN VENUE is available only when every mandatory department is READY.
- The Host must hold the required Capability as well as satisfy the Host responsibility and all opening business rules. The Host Role alone does not authorize the action.
- Opening the Venue is an intentional action that creates the official operational start of the Business Date.
- Before the Venue is open, guest arrivals cannot begin, new Customer Groups cannot be created, and Orders cannot be submitted.
- After opening, guest arrivals become available, new Customer Groups and Orders are allowed under their existing rules, operational timers start, and the day’s dashboard measures begin.
- Venue opening does not itself create a Customer Group, Bill, Financial Obligation, Order, or Payment.
- The system preserves a permanent Opening Report containing the opening time, Host, readiness of every mandatory department, delays, blocking issues, reasons, and comments.
- The Opening Report forms part of the daily operational history and must not be silently deleted or rewritten.

## 4. Venue layout

The venue has three main location types:

- beach sunbeds;
- pool sunbeds;
- upper tables.

Each location needs a clear name or number. Sunbeds should be grouped into sets as they are used by customers. Each sunbed set should belong to an area and, where applicable, a row.

The system should show a simple venue view with clear statuses, for example:

- available;
- occupied without a bill;
- occupied with an open bill;
- waiting for preparation;
- ready items pending delivery;
- payment requested;
- unavailable or reserved, if this is included later.

The first version may use a clear list or grid. A detailed visual floor plan can be added later if needed.

## 4A. Service Location identification

- Every Service Location has one stable Digital Identity that remains with that business location throughout its history.
- An authorised, signed-in Staff Member may identify and open a Service Location’s current digital context by tapping the NFC tag attached to or associated with that location.
- After identification, the application displays the current state retrieved from the central system, subject to the Staff Member’s Capabilities and business rules.
- The NFC tag contains only a stable, non-sensitive identifier or secure application link that resolves to the Service Location. It contains no current Customer Group, Responsible Waiter, price, Bill, Order, customer, permission, or other changing or sensitive business information.
- Identification by NFC does not sign a user in, grant authority, or bypass Capabilities or business rules.
- Tapping NFC identifies and opens the Service Location only. It must not automatically create a Customer Group, Bill, sunbed charge, Order, transfer, Payment, or any other operational or financial action.
- The Responsible Waiter continues to open the Customer Group and confirm any resulting sunbed charge through the approved flow.
- Authorised staff can always reach the same Service Location manually through its visible name or number when NFC is unavailable, unsupported, damaged, or inconvenient.
- A missing, damaged, disabled, or replaced physical tag does not create a new Service Location and does not change the location’s historical identity.
- NFC is the preferred first-version identification method, but the Service Location Digital Identity remains independent from NFC so another approved method can resolve the same location in the future.

## 4B. Operational Zones

- A Zone is a dynamic operational grouping of any selected Service Locations within one Venue.
- A Zone is independent from the physical Area, Row, location type, visible identity, and Digital Identity of its Service Locations.
- A Zone may contain Service Locations from different Areas within the same Venue.
- A Master user holding the Manage Zones Capability may create, rename, delete, and reassign Zones.
- Service Locations may move between Zones at any time without changing their identity, physical Area, Customer Group, Orders, Bill, Responsible Waiter, or history.
- Deleting a Zone deletes only the operational grouping and never deletes or retires its Service Locations.
- Dynamic Zone membership does not create or change a financial charge. Beach Sunbed charges continue to follow approved physical Row rules.
- Zone Templates are a future capability, not a first-version requirement. A future Master user holding Manage Zone Templates may apply a Weekday, Weekend, Full Capacity, Private Event, Wedding, or other approved template before service starts, then reassign individual Service Locations manually.

## 5. Responsible waiter

- Every active Customer Group, whether at a beach sunbed, pool sunbed, or upper table, must have exactly one Responsible Waiter at a time.
- Only the Responsible Waiter officially opens the Customer Group and starts service. A Host and Cashier do not open it.
- The Responsible Waiter is recorded when the Customer Group is opened.
- The responsible waiter should remain visible to other authorised staff.
- A Staff Member holding the Assign Waiter Capability may change the Responsible Waiter under the approved handover rules.
- Any change should be saved in the activity history with the old waiter, new waiter, person making the change, and time.

## 6. Customer Groups, ordering rounds, and Bills

A Customer Group is the primary operational entity. It owns its Service Location, Orders, optional Bill, Payments through that Bill, Responsible Waiter, and History.

- The Responsible Waiter intentionally opens a Customer Group at an available Service Location and officially starts service.
- The system records the Service Location, Responsible Waiter, opening time, and status.
- A Host may escort the party and organize seating, but the Host does not open the Customer Group.
- A Cashier does not open the Customer Group.
- A Customer Group may exist without a Bill.
- A Bill is created only when the first approved financial obligation exists, such as a Beach Sunbed charge, minimum consumption, first ordered item, or future reservation deposit.
- Opening a Customer Group at a Beach Sunbed immediately creates the approved Beach Sunbed obligation and therefore creates the Bill.
- NFC or manual location identification alone never creates a Customer Group, Bill, charge, Order, or Payment.
- A Customer Group may contain multiple Orders. Every submitted Order is one separate ordering round.
- Once the Bill exists, it aggregates all approved Orders and other approved financial obligations for the Customer Group.
- The Bill shows ordered items, quantities, prices, sunbed charges, discounts or corrections if allowed, Payments, and the remaining total.
- A closed group cannot accept new orders unless a manager reopens it.
- The system must prevent two active groups from occupying the same location.

## 7. Menu and order taking

- Menu items are arranged in simple categories.
- Staff can search for an item and adjust its quantity.
- An item may have a note, such as “no ice” or “no onion.”
- Each item is configured to go to the bar, the kitchen, or neither if no preparation is needed.
- Prices used on a submitted order are saved with that order. Later menu price changes must not change an existing bill.
- Before sending, the waiter can review and change the draft order.
- After sending, changes and cancellations require the correct Capability and are recorded in the activity history.
- Adding a later round creates a new Order and new preparation work while contributing to the same Bill.

## 8. Bar and kitchen tickets

- When a waiter submits an order, the system automatically separates its items by preparation area.
- Drink items appear only on the bar screen.
- Food items appear only on the kitchen screen.
- Each ticket shows a unique number, location, responsible waiter, submission time, items, quantities, and notes.
- Bar and kitchen staff can update ticket status.
- Status updates should be visible to the waiter.
- A failure to send or save an order must be obvious. The waiter must not be shown a successful result unless the order was safely recorded.

## 9. Sunbed charges

- A sunbed charge is based on the configured row.
- The owner can set the charge for each row and the date from which a new price applies.
- When the Responsible Waiter officially opens a Customer Group at a Beach Sunbed, the applicable charge is shown and confirmed as part of the intentional opening action.
- The Beach Sunbed obligation arises immediately after official opening and creates the Bill when no Bill exists.
- Identifying the Beach Sunbed by NFC or manual lookup does not create the charge.
- The applied charge is saved on the bill so that a later price change does not alter it.
- The rules for complimentary sunbeds, minimum consumption, partial use, or manual waivers must be confirmed before implementation.
- Upper tables do not receive a sunbed charge unless the owner decides otherwise.

## 10. Moving a group to another sunbed

- A Staff Member holding Transfer Customer Group can transfer an entire active Customer Group from one sunbed set to another approved available sunbed set.
- The Service Location, Orders, optional Bill, Payments, Responsible Waiter, and History move with the Customer Group.
- The original sunbed becomes available and the new sunbed becomes occupied as one safe operation.
- The system must refuse the transfer if the destination is already occupied.
- The transfer is recorded with the old location, new location, Staff Member, and time.
- The system should show the new location on future preparation tickets. Tickets already sent should remain unchanged, with the transfer visible in history.
- Whether moving to a different row changes the sunbed charge must be confirmed by the owner before implementation.

Splitting a group or bill between locations is not part of the first version unless it is specifically approved later.

## 11. Cashier, payment, and closing

- The cashier can see all open bills, totals, responsible waiters, locations, and how long they have been open.
- The cashier can open a detailed bill and check every charge.
- The system records the payment method, amount, time, and user.
- Proposed payment methods are cash and card. Other methods can be added after confirmation.
- The system should support full payment. Split payments and partial payments require owner confirmation.
- A bill can close only when the remaining balance is zero, unless a manager uses a recorded exception.
- Closing a bill makes the location available again.
- Closed bills remain searchable and must not be silently deleted or changed.
- Receipt or fiscal-device integration is outside the first version unless required and specified separately.

## 12. Management functions

Staff Members with the required Capabilities should be able to maintain:

- user accounts, active status, Roles, and Capability grants;
- venue areas, locations, rows, and availability;
- dynamic Zones and Service Location assignments;
- menu categories, items, prices, and preparation destination;
- sunbed charges and the date each charge begins;
- Capability rules for transfers, cancellations, discounts, corrections, Payments, and reopening Bills.

Zone Templates remain a future capability. When approved, a Master user with Manage Zone Templates may maintain and apply them before service starts.

Basic reports should include:

- open bills;
- daily closed bills and payments;
- sales by item and category;
- sales by waiter;
- cancelled or corrected items;
- location transfers;
- an end-of-day summary.

Exact report and tax requirements must be agreed before they are built.

## 13. Important quality requirements

### Ease of use

- Common waiter actions should need as few taps as practical.
- Buttons and text must be easy to use outdoors on a touch screen.
- Important statuses should use both words and colours, not colours alone.
- The first language should be agreed. Greek and English should be supported by the design even if only one is available at launch.

### Devices

- The application must fit modern mobile phones, tablets, and desktop computers.
- The same central information should be visible on all authorised devices.
- The first supported devices and browser versions will be agreed before testing.

### Reliability

- Money totals must be calculated consistently and stored accurately.
- Important actions must not be applied twice if a user taps again or the connection is slow.
- Several staff members must be able to work at the same time without overwriting each other’s work.
- Daily automated backups and a tested restore process are required before live use.

### Security and accountability

- Every staff member uses an individual account; shared accounts should be avoided.
- Users see only the functions allowed by their roles.
- Login and all sensitive traffic must be protected.
- Payments, transfers, cancellations, price changes, discounts, and bill reopening must be recorded.
- Personal information should be kept to the minimum needed for the business and handled according to applicable Greek and EU rules.

### Connectivity

The expected quality of internet and local Wi-Fi at the venue must be checked. The first version is proposed as an online system. Full offline order taking is not included until the owner confirms it is necessary, because safe offline billing and order delivery add significant complexity.

## 14. First-version boundaries

Unless added after review, the first version will not include:

- customer accounts or a customer-facing application;
- reservations;
- stock and supplier management;
- payroll or staff scheduling;
- loyalty programmes;
- online ordering;
- delivery orders;
- bill splitting by person or item;
- full offline operation;
- accounting, card-terminal, receipt-printer, or Greek fiscal-system integrations;
- advanced visual floor-plan editing.

## 15. Example successful flow

1. A Waiter signs in and identifies an available Beach Sunbed by NFC or manual lookup. Identification performs no business or financial action.
2. The Waiter becomes the Responsible Waiter and intentionally opens the Customer Group. The approved Beach Sunbed obligation arises immediately, creating the Bill and charge.
3. The Waiter adds drinks and food, reviews the first Order, and submits that ordering round.
4. Drinks appear at the bar and food appears in the kitchen.
5. The Customer Group orders again later; a new Order records the later round and its approved items join the same Bill.
6. If needed, a Staff Member with Transfer Customer Group transfers the complete group to an available approved sunbed set.
7. A Cashier with Record Payments views the complete running Bill and records Payment.
8. When the remaining Balance is zero, a Staff Member with Close Bill closes the Bill and the location becomes available under the approved completion rule.

## 16. Questions to settle with the owner

Before implementation, the owner should confirm:

1. What are the exact Venue Areas, location numbers, sunbed sets, and physical Rows?
2. Which Capabilities and additional approvals are required to change the Responsible Waiter?
3. Does a transfer to a differently priced physical Row keep the original charge, replace it, or add the difference?
4. Under which approved circumstances may the immediate Beach Sunbed charge be waived or changed?
5. Are reservations or unavailable locations needed at launch?
6. Which preparation statuses are useful in practice?
7. Which Capabilities and approvals govern cancellation, price correction, discounts, Bill reopening, or other exceptions?
8. Are partial and split Payments required? Which Payment Methods are used?
9. Is a printed Bill needed, and is integration with a receipt printer, card terminal, or Greek fiscal system required?
10. Is Greek, English, or both required at launch?
11. How reliable are the Venue’s internet connection and Wi-Fi?
12. Which reports are essential for daily operation and accounting?
13. Should tips be recorded in the system?

## 17. Acceptance of the first version

The first version will be ready for pilot use when agreed test users can complete the full flow above on the selected phones, tablets, and desktop computers; Customer Groups may correctly exist with or without Bills; Beach Sunbed opening creates the approved immediate obligation; later ordering rounds aggregate into the same Bill; Bar and Kitchen Tickets are routed correctly; totals and Row charges are correct; transfers are safe; Capabilities work independently from Roles; important actions are recorded; and backup restoration has been tested.
