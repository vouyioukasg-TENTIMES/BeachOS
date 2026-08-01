# Emerald Management System — Domain Model

## Purpose of this document

This document is the single source of truth for the business domain of Emerald Management System. It defines the people, places, commercial records, operational work, and business events that make up the product.

It is written for business owners, venue staff, product designers, developers, testers, and AI agents. Everyone working on the product should use the terms and meanings in this document consistently.

This document describes the business only. It does not prescribe databases, APIs, screens, software components, or other implementation details.

## How to use the model

- Use the exact names in this document in planning, design, training, testing, and business discussion.
- Do not use two different terms for the same business concept.
- Do not give one term several meanings.
- When a new concept is needed, define it here before building behaviour around it.
- When a business rule changes, review every affected entity, event, and glossary definition.
- Where this document marks a matter as requiring future approval, do not assume a rule.

## Domain boundaries

The initial domain covers venue operation from the start of a staff shift and the arrival of a customer group through order preparation, billing, payment, and departure. It also covers the business setup needed for those activities, such as venues, service locations, staff roles, menus, and payment methods.

Reservations, customer accounts, stock, purchasing, payroll, loyalty, accounting, and fiscal integrations are future domains unless separately approved.

---

## Organization

### Name

Organization

### Purpose

Represents the business group that owns, operates, or manages one or more venues in Emerald Management System.

### Business description

An Organization is the highest business boundary in the product. It may be a single independent operator with one venue or a hospitality group with several venues. Emerald Beach Club’s operating business is the first Organization.

The Organization provides common ownership and governance. It does not mean that every venue must use identical menus, prices, staff, or operating rules.

### Lifecycle

- An Organization is established before its first Venue is added.
- It may begin with one Venue and add more over time.
- Its business identity or operating details may change without creating a new Organization.
- It may become inactive only when it has no active venue operation requiring access.
- Historical activity remains associated with the Organization after it stops operating in the product.

### Business rules

- Every Venue belongs to exactly one Organization at a given time.
- An Organization must have a clear business identity and authorized owner or representative.
- One Organization must not view or control another Organization’s private operations without explicit authority.
- Deactivating an Organization must not erase its operational or financial history.
- Moving a Venue between Organizations is exceptional and requires an approved process that preserves historical meaning.

### Relationships

- Owns or operates one or more Venues.
- May define Roles, policies, reporting needs, and approved settings shared across its Venues.
- Is the business boundary for Staff Members who may work at one or more of its Venues.

### Examples

- A company operating only Emerald Beach Club.
- A hospitality group operating a beach club in Loutraki and a pool venue in another city.

### Future considerations

- Organization-wide menus, roles, reporting, and commercial agreements.
- Venue groups, franchises, or brands inside one Organization.
- Formal transfer of a Venue between Organizations.
- Central oversight with controlled local independence.

---

## Venue

### Name

Venue

### Purpose

Represents one physical hospitality operation where staff serve customers.

### Business description

A Venue is a distinct operating location, such as Emerald Beach Club in Loutraki. It has its own physical layout, operating timezone, service locations, staff assignments, menu availability, prices, shifts, and daily activity.

A Venue is not an Area within a larger property. It is the operating location whose work can be understood and managed as one business unit.

### Lifecycle

- A Venue is planned and configured before opening for service.
- It may be active, temporarily inactive, seasonal, or permanently closed.
- On each Business Date, its mandatory Operational Departments declare readiness before the Host may intentionally open it for guest service.
- Daily opening creates the official operational start of that Business Date and a permanent Opening Report.
- Its layout and operating details may change over time.
- Closing a Venue ends new operations but preserves all previous Customer Groups, Orders, Bills, Payments, and Activity Logs.

### Business rules

- Every Venue belongs to one Organization.
- A Venue must have one approved local timezone and business-day rule.
- A Venue must not conduct live service until its active layout and essential operating rules are approved.
- A Venue must not open for a Business Date until every mandatory Operational Department has declared READY.
- Before daily opening, guest arrivals, new Customer Groups, and Orders are forbidden.
- A Host coordinates daily opening but does not personally verify each Operational Department.
- The Host may open the Venue only when holding the required Capability and after every mandatory department is READY. The Host Role alone does not authorize the action.
- Daily Venue opening does not create a Customer Group, Bill, Financial Obligation, Order, or Payment.
- Every completed daily opening must preserve one permanent Opening Report as part of operational history.
- Venue-specific records must not be confused with records from another Venue.
- Historical records retain the Venue under which they occurred even if the Venue later changes name or ownership details.

### Relationships

- Belongs to an Organization.
- Contains Areas, Zones, and Service Locations.
- Contains Operational Departments and their daily readiness declarations.
- Hosts Customer Groups, Shifts, Orders, Tickets, Bills, Payments, and Activity Logs.
- Preserves an Opening Report for every completed daily opening.
- Makes Menus and Payment Methods available.
- Has Staff Members assigned or permitted to work there.

### Examples

- Emerald Beach Club, Loutraki.
- A second resort property operated by the same Organization.

### Future considerations

- Seasonal opening schedules.
- Multiple trading names within one property.
- Venue-level tax, language, currency, and fiscal rules.
- Cross-venue staff, menu, and reporting policies.

---

## Operational Department

### Name

Operational Department

### Purpose

Represents one recognized part of a Venue operation that owns a distinct area of opening readiness.

### Business description

An Operational Department groups related operating responsibility, such as Kitchen, Bar, Beach Operations, Cleaning, Maintenance, Cashier, or Reception. For daily Venue opening, each mandatory department has one responsible person who declares whether that department is READY, NOT READY, or BLOCKED.

The Host coordinates the combined opening process but does not replace the department’s responsible person or personally verify every department.

### Lifecycle

- An Operational Department is recognized and named as part of Venue operating setup.
- It is marked mandatory or optional for the relevant daily opening.
- Its responsible person declares a current readiness status before opening.
- A declaration may change as preparation continues, with important changes preserved in the Opening Report.
- The department continues its ordinary responsibilities after opening.
- It may be renamed, reorganized, made optional, or retired without rewriting earlier Opening Reports.

### Business rules

- Every Operational Department belongs to one Venue.
- Every mandatory department has one clearly responsible person for its current opening declaration.
- Its opening status is exactly one of READY, NOT READY, or BLOCKED.
- NOT READY and BLOCKED require a reason.
- A department’s responsible person verifies and declares that department’s readiness; the Host coordinates but does not assume that verification.
- Only the current declaration at the moment of opening determines whether the department satisfies the opening condition.
- Historical declarations relevant to a completed opening must not be silently deleted or rewritten.
- An optional department does not block opening unless it is made mandatory for that Business Date through an approved process.

### Relationships

- Belongs to a Venue.
- Has a responsible Staff Member for its opening declaration.
- Contributes readiness, reasons, delays, blocking issues, and comments to the Opening Report.
- Is visible to the Host during the opening workflow.

### Examples

- Kitchen.
- Bar.
- Beach Operations.
- Cleaning.
- Maintenance.
- Cashier.
- Reception, when applicable.

### Future considerations

- Different mandatory departments by Venue type, season, event, or Business Date.
- Approved substitute responsibility when the usual responsible person is absent.
- Department-specific readiness checklists.
- Organization-wide department standards with Venue-specific variations.

---

## Opening Report

### Name

Opening Report

### Purpose

Represents the permanent business record of one Venue’s completed opening for one Business Date.

### Business description

An Opening Report explains when the Venue officially opened, which Host performed the opening, and how every mandatory Operational Department declared readiness. It preserves delays, blocking issues, reasons, and comments so the business can understand the conditions under which service began.

The Opening Report is part of daily operational history. It is not merely a temporary dashboard view.

### Lifecycle

- Opening information accumulates while departments prepare and declare readiness.
- The Opening Report becomes official when the authorized Host opens the Venue.
- It remains available throughout and after the Business Date.
- Later comments or corrections require an approved, traceable process that preserves the original opening facts.
- The report remains part of history after the Business Date and after the Venue later changes or closes.

### Business rules

- A completed daily Venue opening creates exactly one official Opening Report for that opening.
- The report records the Venue, Business Date, opening time, Host, readiness of every mandatory department, delays, blocking issues, reasons, and comments.
- It must show that every mandatory department was READY at the time of opening.
- It must not claim that the Host personally verified each department.
- It must not be silently deleted or rewritten.
- The report does not itself create or authorize a Customer Group, Bill, Financial Obligation, Order, or Payment.
- Access to the report follows approved business responsibility and Capability rules.

### Relationships

- Belongs to one Venue and Business Date.
- Records the Host who performed the opening.
- Contains the relevant readiness declarations of mandatory Operational Departments.
- Forms part of the Venue’s daily operational history.
- May be supported by related Activity Logs for sensitive changes or exceptions.

### Examples

- Emerald Beach Club opened at 09:03 after Kitchen, Bar, Beach Operations, Cleaning, Maintenance, and Cashier all declared READY.
- A delayed opening showing that Maintenance was BLOCKED by an ice machine failure before later declaring READY.

### Future considerations

- Opening comparison across Business Dates and Venues.
- Links to department-specific readiness checklists.
- Approved reopening or multiple operating-period rules if a Venue closes and opens again on one Business Date.
- Owner notifications for late opening or recurring blocking issues.

---

## Area

### Name

Area

### Purpose

Represents a major, recognizable part of a Venue used to organize service and navigation.

### Business description

An Area is a broad physical and operational section understood by staff, such as Beach, Pool, or Upper Level. It helps staff find locations, understand the venue, and focus on the part of the operation relevant to them.

An Area reflects physical layout. It remains independent from operational Zones, which may group Service Locations from several Areas.

### Lifecycle

- An Area is created as part of Venue setup.
- It may be renamed, reordered, temporarily unavailable, or retired as the Venue changes.
- Service Locations may be added, moved, or retired within it.
- Retiring an Area prevents new service there but does not alter historical Customer Groups or other activity.

### Business rules

- Every Area belongs to exactly one Venue.
- An Area name must be clear and distinct within its Venue.
- An Area cannot contain locations from another Venue.
- An Area with active Customer Groups cannot be retired until those groups are safely resolved or transferred.
- Renaming an Area must not change the meaning of past activity.

### Relationships

- Belongs to a Venue.
- Contains Service Locations as part of the physical Venue layout.
- Is independent from Zones, which group Service Locations for daily operations.
- May be relevant to Shift assignments and operational reporting.

### Examples

- Beach.
- Pool.
- Upper Level.

### Future considerations

- Area-specific opening hours.
- Staff sections or service teams.
- Temporary event Areas.
- Area-level preparation or delivery responsibilities.

---

## Zone

### Name

Zone

### Purpose

Represents a dynamic operational grouping of Service Locations used to organize daily work.

### Business description

A Zone is a flexible collection of Service Locations chosen for current operations. The locations do not need to be beside one another, in the same Area, or of the same physical type. A Zone may represent a waiter’s daily responsibility, an event operating group, or another approved service arrangement.

A Zone is independent from the Venue’s physical layout. Area describes physical location; Zone describes how Service Locations are grouped for operations at a particular time.

### Lifecycle

- An authorised Master user creates a Zone for a Venue.
- The Zone may be named, renamed, reordered, or deleted as operations change.
- Service Locations may be assigned or reassigned at any time by a Staff Member with the required Capability.
- Deleting a Zone ends only the operational grouping. It does not delete, retire, move, or rename any Service Location.
- Historical activity preserves the Zone context that applied at the relevant time.

### Business rules

- Every Zone belongs to exactly one Venue.
- A Zone does not belong to an Area and does not define geography, price, permanent ownership, or Service Location identity.
- A Zone may contain an arbitrary collection of Service Locations from different Areas within the same Venue.
- A Service Location may be reassigned without changing its visible identity, Digital Identity, physical Area, active Customer Group, Orders, Bill, Responsible Waiter, or history.
- Only a Staff Member with the Manage Zones Capability may create, rename, delete, or reassign a Zone.
- Deleting a Zone must not delete or otherwise alter its Service Locations or their history.
- A Zone must not contain a Service Location from another Venue.
- A Zone must not determine a financial charge unless a separate approved business decision explicitly establishes that rule. Physical Row-based charging remains independent from operational Zone membership.

### Relationships

- Belongs to a Venue.
- Groups zero or more Service Locations for current operations.
- May support Staff Member responsibility, daily coordination, or operational reporting.
- May be created initially from a future Zone Template.
- Is managed by a Master user or another Staff Member who holds the required Capability.

### Examples

- Waiter Maria’s service Zone containing selected Beach and Pool Service Locations.
- Weekend Zone A covering a larger collection than the weekday arrangement.
- Wedding Guest Zone containing selected upper tables and sunbed sets for event operations.

### Future considerations

- Whether a Service Location may belong to more than one active Zone at the same time. The initial assumption should remain one current operational Zone unless the owner approves overlapping purposes.
- Automatic Zone suggestions based on workload.
- Historical comparison of different daily Zone arrangements.
- Zone Templates for repeatable starting arrangements.

---

## Zone Template

### Name

Zone Template

### Purpose

Represents a reusable future plan for creating the initial operational Zone arrangement before service begins.

### Business description

A Zone Template describes a named starting pattern of Zones and Service Location assignments for a Venue. Examples include Weekday, Weekend, Full Capacity, Private Event, and Wedding.

It is a future capability, not part of the first version. A template supports preparation for the day but never replaces manual control of live Zones.

### Lifecycle

- A Master user with the Manage Zone Templates Capability prepares and approves a Zone Template.
- The template may be renamed, revised, copied, retired, or deleted when it is not needed for future use.
- Before service starts, an authorised Master user may apply it to create the initial operational Zones.
- After application, authorised staff may manually reassign individual Service Locations without changing the template itself.
- Retiring or changing a template does not rewrite Zones or history from earlier days.

### Business rules

- Every Zone Template belongs to exactly one Venue unless a future decision approves Organization-wide templates.
- Applying a Zone Template creates or arranges operational Zones; it does not change Areas or physical layout.
- It must not change a Service Location’s identity, Digital Identity, name, history, active Customer Group, Orders, Bill, or financial rules.
- Only a Staff Member with the Manage Zone Templates Capability may create, change, apply, retire, or delete a Zone Template.
- Applying a template must be an intentional action before service begins.
- Manual Zone reassignment remains available after a template is applied.

### Relationships

- Belongs to a Venue.
- Describes initial Zones and Service Location assignments.
- Is managed and applied by a Master user with the required Capability.
- Produces an operational starting arrangement without becoming the live Zone itself.

### Examples

- Weekday.
- Weekend.
- Full Capacity.
- Private Event.
- Wedding.

### Future considerations

- Organization-wide templates with Venue-specific adjustments.
- Scheduled recommendations based on events or expected capacity.
- Comparison between the starting template and later manual changes.
- Approval and version history for template changes.

---

## Service Location

### Name

Service Location

### Purpose

Represents one identifiable place where one active Customer Group can receive service and provides a stable Digital Identity through which staff can reach that place’s current digital context.

### Business description

A Service Location is the common business concept for a beach sunbed set, pool sunbed set, upper table, or another approved place of service. It has a stable identity that staff can recognize, such as “Beach A12” or “Upper Table 4.”

The Service Location represents the unit assigned to a Customer Group. A sunbed set may contain several physical pieces of furniture but remains one Service Location if it is served and billed as one unit.

Every Service Location also has one stable **Service Location Digital Identity**. Its purpose is to resolve the physical place to the same enduring business location so authorised staff can retrieve its current state from the central system. NFC is the preferred initial identification method. Manual lookup by the location’s visible name or number always remains available.

The physical NFC tag is not the Service Location and is not a separate core business entity. It is one replaceable way of presenting the Service Location Digital Identity.

### Lifecycle

- A Service Location is planned and made available within a Venue layout.
- It may be available, occupied, temporarily unavailable, or retired.
- It may be renamed or moved within the Venue while preserving its operational history.
- Its physical identification method may be added, replaced, disabled, or changed without creating a new Service Location or changing its history.
- It becomes occupied when an active Customer Group is officially opened at it or transferred to it.
- It becomes available after the Customer Group completes service or transfers, provided the location is not otherwise unavailable.

### Business rules

- Every Service Location belongs to one Venue and one Area; it may belong to one Zone.
- A Service Location may have at most one active Customer Group at a time.
- It must have a clear, unique staff-facing identity within its Venue.
- It must have one stable Service Location Digital Identity that continues to represent the same business location throughout changes to its physical identification method.
- Changing, removing, damaging, or replacing the physical NFC tag must not create a new Service Location or change the historical identity of the existing one.
- One active physical tag or other active identification marker must not resolve to more than one Service Location.
- A physical tag may contain only a stable, non-sensitive identifier or secure application link. It must not contain changing operational, financial, customer, permission, or other sensitive business information.
- Identifying a Service Location retrieves its current context from the central system; the physical tag is never the source of current operational truth.
- Identifying a Service Location does not sign in a Staff Member, grant authority, bypass permissions or business rules, or automatically perform any operational or financial action.
- NFC is the preferred initial identification method, but authorised staff must always be able to identify the same Service Location manually by its visible name or number.
- An unavailable or retired Service Location cannot receive a new Customer Group or transfer.
- A transfer destination must be available before the transfer begins.
- A Service Location cannot be moved to another Venue as part of an ordinary customer transfer.
- Retiring or renaming a Service Location must not erase or rewrite its past use.

### Relationships

- Belongs to a Venue and Area and may belong to a Zone.
- Hosts one active Customer Group at a particular time.
- Is associated with the Responsible Waiter through the active Customer Group.
- Appears on Orders, Kitchen Tickets, Bar Tickets, Bills, and Activity Logs as the service context.
- Is reached through its Service Location Digital Identity, using NFC initially or another approved identification method, and through manual lookup.

### Examples

- Beach Sunbed Set A12.
- Pool Sunbed Set P07.
- Upper Table U04.
- The NFC tag at Beach A12 and a manual search for “Beach A12” both resolve to the same Service Location and retrieve its current state.

### Future considerations

- Reservable, cleaning, maintenance, or blocked states.
- Composite locations that can be joined for a large group.
- Capacity and accessibility information.
- Seasonal layouts and reusable location templates.
- QR codes or other suitable identification methods that resolve the same stable Service Location Digital Identity.
- Operational management of physical markers if replacement, activation, deactivation, or tamper handling later becomes complex enough to require its own business lifecycle.

---

## Customer Group

### Name

Customer Group

### Purpose

Represents one party and its complete active service context, from official opening until service is completed.

### Business description

A Customer Group is the primary operational entity. It is a service concept, not a customer account, and the people do not need to be individually identified. It owns the current Service Location, Responsible Waiter, Orders, optional Bill, Payments through that Bill, and History.

The Customer Group remains the same operational entity if it moves to another Service Location, changes Responsible Waiter, places later ordering rounds, or receives its first financial obligation after opening.

### Lifecycle

- A Host may escort the party and organize seating without opening a Customer Group.
- The Responsible Waiter intentionally opens the Customer Group at an available Service Location and officially starts service.
- If the Service Location is a Beach Sunbed, opening immediately creates the approved Beach Sunbed financial obligation and therefore creates the Bill.
- At other Service Location types, the Customer Group may remain open without a Bill until the first approved financial obligation exists.
- It may place multiple Orders, with each submitted Order representing one ordering round.
- It may transfer to another available Service Location without changing identity.
- It may receive a different Responsible Waiter through an approved handover.
- It ends active service when the approved completion conditions are met or is cancelled under an approved exceptional rule.
- Its history remains available after departure.

### Business rules

- Only the Responsible Waiter may officially open a Customer Group. A Host or Cashier must not open it.
- Opening must be an intentional business action; identifying a Service Location by NFC or manual lookup does not open a Customer Group.
- An active Customer Group occupies exactly one Service Location at a time.
- An active Customer Group has exactly one Responsible Waiter at a time.
- A Customer Group may exist without a Bill.
- A Bill is created only when the first approved financial obligation exists.
- Opening at a Beach Sunbed immediately creates the approved Beach Sunbed obligation. NFC identification alone never creates that obligation.
- A Customer Group may have multiple Orders. Each submitted Order is a separate ordering round and must not overwrite an earlier Order.
- Once a Bill exists, it aggregates all approved obligations from every Order and other approved charges for that Customer Group.
- A Customer Group must not be duplicated merely because it changes Service Location.
- A Customer Group must not silently inherit another group’s Orders, Bill, or Payment.
- A completed Customer Group cannot receive new Orders or ordinary financial activity.
- Important lifecycle and responsibility changes must be preserved in its History and Activity Logs.
- Individual personal information must not be collected unless there is a defined and approved business need.
- Combining or splitting Customer Groups is forbidden in the initial domain unless a future rule explicitly allows it.

### Relationships

- Belongs to one Venue.
- Occupies one Service Location at a time and may transfer between approved locations.
- Has exactly one Responsible Waiter at a time while active.
- Owns zero or more Orders.
- May have one Bill after its first financial obligation exists.
- Owns Payments through its Bill.
- Has a permanent History represented by relevant Activity Logs and business records.
- May remain active across more than one Staff Shift.

### Examples

- Four guests officially opened by their Responsible Waiter at Beach Sunbed Set A12. The opening creates the applicable Beach Sunbed charge and Bill.
- A party officially opened at an approved Service Location whose opening creates no financial obligation, and therefore has no Bill yet.
- Six guests at Upper Table U04 who place three separate ordering rounds under the same Customer Group and Bill.

### Future considerations

- Group size and anonymous service preferences.
- Combining or splitting groups.
- Linking a group to a reservation or customer profile without making identity compulsory.
- Multiple Bills for one group, if bill splitting is approved.
- An optional future Visit concept only if reservations, known returning customers, or repeated service occasions create a clear meaning that is distinct from Customer Group. Visit is not part of the core operational domain.

---

## Staff Member

### Name

Staff Member

### Purpose

Represents an individual person who works for or is authorized to act within an Organization.

### Business description

A Staff Member is the person whose work and responsibility need to be recognized by the business. Examples include waiters, bar staff, kitchen staff, cashiers, and managers. A Staff Member is distinct from a Role: the person remains the same even when their responsibilities change.

### Lifecycle

- A Staff Member is added after their authority to work is confirmed.
- They may be assigned one or more Roles and one or more Venues.
- They may start and end Shifts and take responsibility for Customer Groups.
- Their assignments may change over time.
- They may become temporarily unavailable or inactive after leaving the business.
- Historical actions remain attributed to them after deactivation.

### Business rules

- Each Staff Member represents one individual; shared staff identities are forbidden.
- A Staff Member may act only within their Venue assignments and explicitly granted Capabilities.
- Deactivation prevents new work but must not erase or anonymize accountability unless required by an approved legal rule.
- Sensitive changes to Roles, Capabilities, or status must be authorized and logged.
- Only eligible Staff Members may become Responsible Waiters.
- Personal information must be limited to what the business genuinely needs.

### Relationships

- Belongs to or is authorized by an Organization.
- May work at one or more Venues.
- Holds one or more Roles.
- Participates in Shifts.
- Holds explicit Capabilities that authorize defined actions in an approved context.
- May be the Responsible Waiter for active Customer Groups.
- Creates Orders, updates Tickets, records Payments, or performs other activities only when the required Capability and business rules allow it.
- Is identified as the actor in Activity Logs.

### Examples

- Maria, working as a Waiter during the morning Shift.
- Nikos, holding both Cashier and Manager Roles.

### Future considerations

- Employment status, team, and preferred language.
- Staff scheduling and planned availability.
- Temporary or agency staff.
- Organization-wide staff working at several Venues.

---

## Role

### Name

Role

### Purpose

Represents a recognized set of business responsibilities given to Staff Members.

### Business description

A Role describes the kind of business responsibility a Staff Member holds, such as Waiter, Host, Bar Staff, Kitchen Staff, Cashier, Manager, or Master. A Role helps people understand expected work, but it does not by itself authorize an action.

### Lifecycle

- A Role is defined and approved by the Organization.
- It is assigned to eligible Staff Members.
- Its responsibilities may be reviewed and changed deliberately.
- A Role may be retired when no longer used, while past activity remains understandable.

### Business rules

- Role names and responsibilities must be clear and non-overlapping where practical.
- A Staff Member may hold more than one Role.
- Holding a Role never directly authorizes an action.
- Every protected business action requires the relevant Capability in addition to satisfaction of its business rules.
- Capabilities must be explicit rather than assumed from a broad title such as Manager or Master.
- A Capability cannot override a business rule that reserves an action for a particular responsibility. For example, only the Responsible Waiter officially opens a Customer Group even though Open Customer Group is a Capability.
- Changes to Role responsibility must be approved and logged independently from changes to Capabilities.
- Retiring a Role must not make past actions impossible to understand.

### Relationships

- Is defined by an Organization and may apply to one or more Venues.
- Is assigned to Staff Members.
- Groups and communicates business responsibilities.
- Is distinct from Capabilities, which authorize actions.
- Provides work context within Customer Groups, Orders, Tickets, Bills, Payments, Zones, and Shifts.

### Examples

- Waiter.
- Host.
- Bar Staff.
- Kitchen Staff.
- Cashier.
- Manager.
- Master.

### Future considerations

- Venue-specific Roles.
- Responsibility descriptions that vary by Venue without changing Capability meaning.
- Approval chains for especially sensitive responsibilities.
- Custom Roles for larger Organizations.

---

## Capability

### Name

Capability

### Purpose

Represents explicit business authority for a Staff Member to perform one defined action in an approved context.

### Business description

A Capability answers “May this Staff Member perform this action here?” A Role answers “What business responsibilities does this Staff Member have?” The two concepts are deliberately separate.

Capabilities make authority specific and reviewable. A Staff Member may hold a Role without every Capability commonly associated with that Role, and two Staff Members with the same Role may have different Capabilities when the business has approved that difference.

### Lifecycle

- The Organization defines a clear Capability for a protected business action.
- An authorised person grants it to an eligible Staff Member for an approved Organization, Venue, or operating context.
- It may be reviewed, limited, suspended, or revoked.
- Changes remain visible in the Activity Log.
- Retiring a Capability prevents new use but preserves the meaning of historical actions.

### Business rules

- Every protected action must identify the Capability it requires.
- A Role must not directly imply or automatically guarantee a Capability.
- Granting a Capability does not bypass the action’s business rules, required state, or accountability requirements.
- A Capability must have one clear action meaning and scope.
- Capability grants and revocations require authorized approval and Activity Logging.
- The Staff Member must hold the Capability at the time of the action.
- Open Customer Group does not allow a Host or Cashier to open service; the Staff Member must also be the Responsible Waiter under the approved opening rule.

### Relationships

- Is defined by an Organization.
- Is explicitly granted to Staff Members in an approved context.
- Is separate from Roles and Shifts.
- Authorizes actions affecting Customer Groups, Responsible Waiters, Orders, Bills, Payments, Zones, Zone Templates, Menus, and other protected business subjects.

### Examples

- Open Customer Group.
- Transfer Customer Group.
- Assign Waiter.
- Close Bill.
- Reopen Bill.
- Manage Zones.
- Manage Zone Templates.
- Manage Menus.
- Record Payments.
- Refund Payments.

### Future considerations

- Time-limited or Shift-limited Capability grants.
- Venue-specific Capability catalogs.
- Additional approval by another Staff Member for very sensitive actions.
- Emergency authority with mandatory reason and review.

---

## Menu

### Name

Menu

### Purpose

Represents an approved collection of items offered for ordering in a particular business context.

### Business description

A Menu brings together the categories and items that a Venue offers. A Venue may use one Menu throughout the day or different Menus for breakfast, drinks, events, seasons, or service areas.

A Menu defines availability and presentation of offerings. It does not rewrite the meaning or price of items already ordered.

### Lifecycle

- A Menu is prepared in draft form.
- It is reviewed and made active for an approved Venue, period, or context.
- It may be revised, scheduled, temporarily unavailable, or retired.
- Past Orders retain the item and price that applied when they were submitted.

### Business rules

- A Menu must belong to an Organization and be approved for each Venue where it is used.
- A Venue must not offer an unapproved or inactive Menu.
- A Menu must have a clear identity and availability period or rule.
- Changes must not alter submitted Order Items or closed Bills.
- Overlapping Menus must not make the same offering ambiguous to staff.
- Empty or incomplete Menus must not be activated for live use.

### Relationships

- Belongs to an Organization and is made available at one or more Venues.
- Contains Menu Categories.
- Makes Menu Items available in an ordered, understandable structure.
- Supplies the available choices from which Order Items originate.

### Examples

- Emerald Summer 2026 Menu.
- Pool Drinks Menu.
- Breakfast Menu active until noon.

### Future considerations

- Scheduled Menus by day, time, season, Area, or event.
- Organization-wide Menu templates with Venue variations.
- Multiple languages.
- Customer-facing versus staff-facing descriptions.

---

## Menu Category

### Name

Menu Category

### Purpose

Groups related Menu Items so staff and customers can find and understand them quickly.

### Business description

A Menu Category is a meaningful heading within a Menu, such as Coffees, Cocktails, Soft Drinks, Salads, or Main Dishes. It supports navigation and presentation rather than preparation routing or financial accounting unless a separate approved rule says otherwise.

### Lifecycle

- A Menu Category is created within a Menu.
- It may be named, described, ordered, hidden temporarily, or retired.
- Menu Items may be added, removed, or reordered within it.
- Retiring a category does not change past Orders.

### Business rules

- Every Menu Category belongs to a Menu.
- Its name must be clear and useful to the intended audience.
- A category must not be used to hide preparation destination or other item rules.
- A category with no available Menu Items should not be shown during live ordering.
- Changes must not alter the historical description of submitted Order Items.

### Relationships

- Belongs to one Menu.
- Contains Menu Items offered through that Menu.
- May influence ordering navigation and later approved reporting.

### Examples

- Coffees.
- Beers.
- Cocktails.
- Salads.
- Main Dishes.

### Future considerations

- Nested categories, only if real menus require them.
- Different category order by device, language, time, or service context.
- Reporting groups distinct from customer-facing categories.

---

## Menu Item

### Name

Menu Item

### Purpose

Represents one distinct product or service that can be selected for an Order.

### Business description

A Menu Item is an offering such as Espresso, Still Water, Club Sandwich, or Sunbed Package. It has a recognizable business identity, an approved selling price in a given context, and a preparation destination when preparation is required.

The current Menu Item describes what may be ordered now. An Order Item preserves what was actually ordered at that time.

### Lifecycle

- A Menu Item is defined and reviewed.
- It is offered through one or more Menus and Categories.
- Its price, description, availability, and preparation destination may change prospectively.
- It may be temporarily unavailable or retired.
- Retirement prevents new selection but preserves its identity in past Orders.

### Business rules

- A Menu Item must have one clear business identity.
- It must have an approved price before it can be ordered, including an explicit zero price when genuinely complimentary.
- It must have an approved preparation destination: Bar, Kitchen, or No Preparation in the initial domain.
- It cannot be ordered when unavailable in the applicable Menu and Venue context.
- Later changes must not rewrite submitted Order Items or Bills.
- Two items with materially different preparation or pricing meaning should not be disguised as one ambiguous item.

### Relationships

- Appears in one or more Menu Categories and Menus.
- Is selected to create an Order Item.
- Determines the initial preparation destination of that Order Item.
- May contribute to sales reporting after reporting rules are approved.

### Examples

- Espresso, prepared by the Bar.
- Club Sandwich, prepared by the Kitchen.
- Bottled Water, fulfilled by the Bar.
- A no-preparation approved charge item.

### Future considerations

- Sizes, options, additions, and ingredient choices.
- Allergens and dietary information.
- Time-limited availability and stock-related unavailability.
- Packages, promotions, minimum consumption, and bundled items.

---

## Order

### Name

Order

### Purpose

Represents one confirmed ordering round for an active Customer Group.

### Business description

An Order is the business commitment created when a Staff Member submits a reviewed collection of items. A Customer Group may place several Orders. Each submitted Order is one distinct ordering round, while the Customer Group’s Bill aggregates the approved financial obligations from all rounds.

A draft selection is not an Order. The business recognizes the Order only after submission is safely confirmed.

### Lifecycle

- Items are selected and reviewed as a draft outside the confirmed Order lifecycle.
- The Order is submitted once the Staff Member confirms it.
- Submission creates the relevant preparation work and Bill Lines as one complete business action.
- Order Items progress through preparation and service.
- An Order may be fully or partly corrected or cancelled only under approved rules.
- It remains part of the permanent Customer Group and Bill history.

### Business rules

- An Order belongs to one active Customer Group.
- An Order must contain at least one valid Order Item.
- It is not submitted until the business has safely accepted it; false success is forbidden.
- Repeated actions must not create duplicate Orders.
- Submitted Orders cannot be silently edited or deleted.
- Corrections and cancellations require authority, reason where required, and Activity Logging.
- Submission must not leave the Bill and preparation work disagreeing about what was ordered.
- A completed Customer Group cannot receive a new Order.

### Relationships

- Belongs to one Customer Group.
- Is submitted by a Staff Member.
- Contains one or more Order Items.
- Produces Kitchen Tickets, Bar Tickets, or no-preparation fulfillment as required.
- Creates or contributes Bill Lines to the Customer Group’s Bill. If the first ordered item is the first financial obligation, the Order causes the Bill to be created.
- Refers to the Service Location and Responsible Waiter context at submission time.

### Examples

- Two coffees and two waters ordered at 11:15.
- One club sandwich and one salad ordered as a later round at 13:30.

### Future considerations

- Courses, priority, scheduled preparation, and delivery confirmation.
- Customer-originated Orders.
- Transfer of unfulfilled work after a location move.
- Formal correction and cancellation reason lists.

---

## Order Item

### Name

Order Item

### Purpose

Represents one confirmed item, quantity, price, preparation destination, and instruction within an Order.

### Business description

An Order Item is the historical statement of what the Customer Group requested and the business accepted. It keeps the item description, agreed quantity, price, and preparation meaning that applied at submission, even if the Menu Item changes later.

### Lifecycle

- An Order Item begins as an unconfirmed selection in a draft.
- It becomes a confirmed Order Item when the Order is submitted.
- It may progress through preparation, readiness, and service.
- It may be corrected or cancelled only through an approved traceable action.
- It remains in the historical Order even when cancelled.

### Business rules

- Every Order Item belongs to one Order.
- It must identify what was ordered, in what quantity, at what agreed unit price, and where it must be prepared or fulfilled.
- Quantity must be meaningful and approved; zero or negative ordered quantity is forbidden.
- Price and preparation destination are preserved at submission.
- Notes must be relevant to service and must not be used to bypass a required Menu Item or pricing rule.
- A submitted Order Item must not be silently replaced by another item.
- Cancellation must not erase the original request.

### Relationships

- Belongs to an Order.
- Originates from a Menu Item.
- Is assigned to a Kitchen Ticket, Bar Ticket, or approved no-preparation path.
- Produces or supports a corresponding Bill Line.
- May be the subject of Activity Logs for corrections or cancellations.

### Examples

- Two Espressos at the agreed unit price, note “one without sugar,” sent to the Bar.
- One Club Sandwich, note “no onion,” sent to the Kitchen.

### Future considerations

- Item options, modifiers, courses, and shared items.
- Partial cancellation or partial fulfillment of a quantity.
- Allergen warnings and acknowledgment.
- Who delivered the item and when.

---

## Kitchen Ticket

### Name

Kitchen Ticket

### Purpose

Represents the Kitchen’s confirmed preparation work created from one Order.

### Business description

A Kitchen Ticket gives Kitchen Staff only the Order Items they are responsible for preparing. It keeps those items connected to the originating Order, Customer Group, Service Location context, and responsible service team.

It is an operational work record, not a separate customer Order or Bill.

### Lifecycle

- A Kitchen Ticket is created when a submitted Order contains one or more Kitchen-destination Order Items.
- It begins as new work.
- It may move through approved states such as acknowledged, preparing, ready, and completed.
- Problems, delays, or cancellations may be recorded under approved rules.
- It remains as operational history after completion.

### Business rules

- A Kitchen Ticket belongs to one Order.
- It contains only Kitchen-destination Order Items from that Order.
- It must not exist without at least one Kitchen item.
- Its creation must not be lost or separated from successful Order submission.
- It must not create a second charge; financial meaning comes from the Order and Bill.
- Status changes must follow the approved sequence and identify the responsible action where required.
- Moving the Customer Group does not rewrite the location originally shown at submission; the current location must remain discoverable for delivery.
- Completed or cancelled work must not be silently reopened or removed.

### Relationships

- Is created from one Order.
- Contains references to Kitchen-destination Order Items.
- Is handled by Kitchen Staff during Shifts.
- Refers to the Customer Group, Service Location context, and Responsible Waiter needed for service.
- Generates relevant Activity Logs when sensitive or exceptional changes occur.

### Examples

- Kitchen Ticket K-104 containing one Club Sandwich and one Salad from the same Order.
- No Kitchen Ticket is created for an Order containing only drinks.

### Future considerations

- Kitchen stations and preparation routing.
- Courses, preparation estimates, priority, and delayed items.
- Partial readiness and item-level progress.
- Printing or kitchen display integrations.

---

## Bar Ticket

### Name

Bar Ticket

### Purpose

Represents the Bar’s confirmed preparation or fulfillment work created from one Order.

### Business description

A Bar Ticket gives Bar Staff only the Order Items they are responsible for preparing or supplying. It remains connected to the originating Order, Customer Group, Service Location context, and responsible service team.

It is operational work, not a separate customer Order or Bill.

### Lifecycle

- A Bar Ticket is created when a submitted Order contains one or more Bar-destination Order Items.
- It begins as new work.
- It may move through approved states such as acknowledged, preparing, ready, and completed.
- Problems, delays, or cancellations may be recorded under approved rules.
- It remains as operational history after completion.

### Business rules

- A Bar Ticket belongs to one Order.
- It contains only Bar-destination Order Items from that Order.
- It must not exist without at least one Bar item.
- Its creation must not be lost or separated from successful Order submission.
- It must not create a second charge.
- Status changes must follow the approved sequence and identify the responsible action where required.
- Moving the Customer Group does not rewrite the submission location; the current delivery location must remain discoverable.
- Completed or cancelled work must not be silently reopened or removed.

### Relationships

- Is created from one Order.
- Contains references to Bar-destination Order Items.
- Is handled by Bar Staff during Shifts.
- Refers to the Customer Group, Service Location context, and Responsible Waiter needed for service.
- Generates relevant Activity Logs when sensitive or exceptional changes occur.

### Examples

- Bar Ticket B-205 containing two Espressos and two Waters.
- No Bar Ticket is created for an Order containing only Kitchen items.

### Future considerations

- Multiple bar stations and item routing.
- Cocktails versus immediate fulfillment.
- Partial readiness and item-level progress.
- Printing, bar display, or runner coordination.

---

## Bill

### Name

Bill

### Purpose

Represents the complete running financial obligation for a Customer Group after its first approved financial obligation exists.

### Business description

A Bill brings together every valid charge, adjustment, and Payment associated with a Customer Group. It allows staff and the Customer Group to understand what has been ordered, what other approved charges apply, what has been paid, and what remains due.

In the initial domain, a Customer Group may have no Bill until its first approved financial obligation exists. After creation, it has one Bill, which remains with the Customer Group when it changes Service Location.

### Lifecycle

- A Bill is created when the Customer Group receives its first approved financial obligation, not merely when the Customer Group opens.
- For a Customer Group opened at a Beach Sunbed, the immediate approved Beach Sunbed obligation creates the Bill as part of the official opening outcome.
- At other Service Location types, the first obligation may be a minimum consumption, first ordered item, reservation deposit, or another approved charge.
- Bill Lines are added through approved Orders, sunbed charges, and other approved business actions.
- Payments reduce the amount remaining due.
- Authorized corrections or adjustments may occur while preserving history.
- The Bill closes only when approved closing conditions are satisfied.
- A closed Bill remains permanent and searchable.
- Reopening is forbidden unless a future approved exception defines authority, reason, and audit requirements.

### Business rules

- A Bill belongs to one Customer Group in the initial product.
- A Bill must use one approved currency.
- Its total must be explainable through its Bill Lines and valid Payments.
- Money must be exact; approximate financial calculation is forbidden.
- Existing Bill Lines must not change because a Menu, price, Zone, or policy changes later.
- A Bill cannot close with an unresolved balance unless a separately approved, recorded exception allows it.
- A closed Bill cannot receive ordinary new Orders or Payments.
- A Bill must not be silently deleted, merged, split, or transferred away from its Customer Group.
- Corrections must preserve the original financial history.

### Relationships

- Belongs to a Customer Group and therefore its Venue.
- Contains Bill Lines.
- Receives Payments made through Payment Methods.
- Is affected by Orders and approved charges or adjustments.
- Is reviewed and closed by authorized Staff Members.
- Has sensitive changes represented in Activity Logs.

### Examples

- A running Bill containing four drinks, two meals, and the Beach Row 1 sunbed charge.
- A Bill fully paid by one card Payment and then closed.

### Future considerations

- Split Bills, deposits, refunds, tips, service charges, discounts, and credit.
- Formal tax and fiscal documents.
- Multiple currencies, only if future markets require them.
- Bill presentation and legally required receipt relationships.

---

## Bill Line

### Name

Bill Line

### Purpose

Represents one explainable financial contribution to a Bill.

### Business description

A Bill Line states why a Bill increased or decreased by a specific amount. It may represent an ordered item, a sunbed charge, a discount, a correction, or another approved financial reason.

A Bill Line preserves the description, quantity, unit value, and financial meaning that applied when it was created.

### Lifecycle

- A Bill Line is created by an approved business action.
- It remains active unless an authorized correction or reversal changes its financial effect.
- It is included in the running total and later in the closed Bill.
- It remains in history even when its effect is reversed.

### Business rules

- Every Bill Line belongs to one Bill.
- It must have one clear business reason and an exact amount in the Bill’s currency.
- An ordered-item Bill Line must remain traceable to its Order Item.
- A sunbed or other charge must identify the approved rule that justified it.
- A Bill Line cannot be silently edited or deleted after confirmation.
- Discounts, corrections, and reversals require appropriate authority and traceability.
- A descriptive note alone must not be used to introduce an unapproved charge.

### Relationships

- Belongs to a Bill.
- May originate from an Order Item.
- May represent a physical Row-related sunbed charge or another approved rule. Dynamic Zone membership alone does not create or change a charge.
- May be corrected or offset by another Bill Line.
- May be the subject of an Activity Log.

### Examples

- Two Espressos at €3.00 each.
- Beach Row 1 sunbed charge of €20.00.
- Authorized discount of €5.00 with an approved reason.
- Reversal of a cancelled Order Item while preserving the original line.

### Future considerations

- Taxes and tax categories.
- Packages, promotions, deposits, service charges, and tips.
- Allocation of a Payment to particular Bill Lines.
- Legally required fiscal classifications.

---

## Payment

### Name

Payment

### Purpose

Represents an accepted transfer of value toward a Bill.

### Business description

A Payment records that the business received an exact amount through an approved Payment Method for a particular Bill. It is a financial fact and must remain understandable independently of the Staff Member’s memory.

A payment request, attempted card transaction, or promise to pay is not a Payment until the business confirms it as received according to the method’s rules.

### Lifecycle

- A Payment is initiated against an open Bill.
- It is recorded only after the method-specific success condition is met.
- It reduces the Bill’s remaining balance.
- It may later be reversed or refunded only through an approved, traceable process.
- It remains part of financial history after the Bill closes.

### Business rules

- Every Payment belongs to one Bill.
- It must have an exact positive amount, currency, Payment Method, time, and responsible Staff Member or approved origin.
- A Payment must not be recorded twice because of a repeated action or uncertain response.
- An unsuccessful or abandoned attempt must not reduce the Bill balance.
- A Payment cannot silently move to another Bill.
- Reversal or refund must preserve the original Payment and require explicit authority.
- Whether overpayment, partial payment, or multiple methods are allowed requires approved rules; they must not be assumed.
- Recording a Payment does not by itself close the Bill unless all closing rules are satisfied.

### Relationships

- Applies to one Bill.
- Belongs to the Customer Group’s financial History through that Bill.
- Uses one Payment Method.
- Is recorded or confirmed by a Staff Member, or later by an approved external source.
- May occur during a Shift.
- Produces Activity Logs for recording, reversal, refund, or exceptional handling.

### Examples

- €75.00 received in cash against a €75.00 Bill.
- €120.00 confirmed by card against a €120.00 Bill.

### Future considerations

- Split and partial Payments.
- Tips, change given, refunds, deposits, and prepayments.
- Payment terminal references and reconciliation.
- Payment disputes and chargebacks.

---

## Payment Method

### Name

Payment Method

### Purpose

Represents an approved way by which a Venue may receive value.

### Business description

A Payment Method identifies the business form of payment, initially expected to include Cash and Card. It defines the meaning and confirmation expectations for Payments using that method.

Payment Method is not the individual Payment and not necessarily a specific external provider.

### Lifecycle

- A Payment Method is approved for an Organization or Venue.
- It is made available for use.
- Its operating rules may be revised prospectively.
- It may be temporarily unavailable or retired.
- Past Payments retain the method used at the time.

### Business rules

- A Payment Method must have a clear name and business meaning.
- Only active, approved methods may be used for new Payments.
- Retiring or renaming a method must not alter past Payments.
- Method-specific confirmation rules must be clear before use.
- Two methods with materially different reconciliation or legal meaning must not be combined under an ambiguous label.

### Relationships

- Is approved by an Organization and made available at one or more Venues.
- Is used by Payments.
- May be relevant to Shift reconciliation and reporting.
- May later connect to an external payment provider or device.

### Examples

- Cash.
- Card.
- A future approved room charge or digital wallet method.

### Future considerations

- Specific card providers or terminals.
- Digital wallets, vouchers, gift cards, or account credit.
- Venue-specific availability.
- Reconciliation and settlement rules.

---

## Activity Log

### Name

Activity Log

### Purpose

Provides a trustworthy business history of sensitive, exceptional, or accountability-relevant actions.

### Business description

An Activity Log explains who did what, when, in which Venue, and what important business context changed. It protects staff and the business by making significant actions understandable after the moment has passed.

It is not a general employee-surveillance record and should not collect activity simply because it can.

### Lifecycle

- An Activity Log is created when a defined business event requiring accountability occurs.
- It becomes part of the permanent or policy-controlled history.
- It may be reviewed by authorized people for support, reconciliation, disputes, security, or management.
- It is not edited to change the past.
- Retention or lawful removal follows an approved policy without falsifying remaining records.

### Business rules

- Every Activity Log must identify the event, time, Venue, actor or approved origin, affected business subject, and relevant change.
- Important previous and new values must be included when they explain the decision.
- Sensitive actions must not succeed without the required Activity Log.
- Activity Logs must not contain passwords, payment secrets, or unnecessary personal information.
- Staff may see Activity Logs only when their business responsibility requires it.
- Activity history must not be silently changed or deleted.
- Failure to perform an attempted action should be logged only when required for security or operational accountability.

### Relationships

- Belongs to an Organization and Venue context.
- Identifies a Staff Member or approved external origin as actor.
- May concern a Customer Group, Service Location, Order, Order Item, Ticket, Bill, Bill Line, Payment, Role, Capability, Zone, Shift, Menu, or other governed business subject.
- Records important Domain Events.

### Examples

- Responsible Waiter changed from Maria to Nikos at 15:10 by a Manager.
- Customer Group transferred from Beach A12 to Beach B05.
- Order Item cancelled with approved reason.
- Payment reversed by an authorized Cashier.

### Future considerations

- Retention periods by activity type.
- Owner-facing investigation and compliance views.
- External security or fiscal audit requirements.
- Anomaly detection without creating unfair staff surveillance.

---

## Shift

### Name

Shift

### Purpose

Represents a defined period during which a Staff Member is working in a particular Venue and business capacity.

### Business description

A Shift provides the working context for staff activity. It helps the business understand who was working, in which Venue, with which Role or responsibilities, and over what period.

A Shift is not the Venue’s business day and does not control the lifecycle of a Customer Group. A Customer Group may begin in one Shift and finish in another.

### Lifecycle

- A Shift may be planned in advance or opened when work begins, depending on future approval.
- It starts when the Staff Member begins approved work.
- Responsibilities or working Area may change through an authorized handover.
- It ends when the Staff Member stops that period of work.
- Corrections to start or end details require authority and an explanation.
- Shift history remains available after completion.

### Business rules

- A Shift belongs to one Staff Member and one Venue.
- It must have a clear start and, when completed, a clear end.
- A Staff Member must not act under a Role they do not hold for that Shift or Venue.
- Ending a waiter’s Shift must not leave active Customer Groups without an approved Responsible Waiter.
- Ending a Shift must not close Customer Groups, Bills, Tickets, or Payments automatically.
- Overlapping Shifts for the same Staff Member require an approved business reason.
- Shift corrections must be traceable.

### Relationships

- Belongs to a Staff Member and Venue.
- Uses one or more approved Roles or responsibilities.
- Provides context for Orders, Ticket work, Payments, Activity Logs, and Customer Group responsibility.
- May include responsibility for Areas or Zones.
- May hand active Customer Group responsibility to another Staff Member or Shift.

### Examples

- Maria works as a Waiter at Emerald Beach Club from 09:00 to 17:00.
- Nikos works as Cashier and Manager from 15:00 to closing.

### Future considerations

- Planned schedules, breaks, attendance, and overtime.
- Team or Area assignments.
- Till opening, cash float, and end-of-Shift reconciliation.
- Formal handover between Shifts.

---

# DOMAIN EVENTS

## Purpose of domain events

A Domain Event is a business fact stating that something meaningful has happened. Event names use the past tense because the event describes a completed fact, not an intention or a button press.

Domain Events help owners, staff, designers, developers, testers, and AI agents discuss lifecycle changes consistently. Not every small action is a Domain Event. An event should matter to operations, money, accountability, or another business process.

Every event has:

- an agreed event name;
- the time it occurred;
- the Organization and Venue context;
- the business subject affected;
- the Staff Member or approved origin responsible, where relevant;
- the business facts needed to understand the outcome.

Events do not replace the entities described above. They describe meaningful changes involving those entities.

## Organization and venue events

### Organization Established

An Organization has been approved to operate within Emerald Management System.

### Organization Deactivated

An Organization has stopped new operation in the product while its history remains preserved.

### Venue Established

A Venue has been added under an Organization and is ready for setup.

### Venue Activated

A configured Venue has been approved for live operation.

### Department Readiness Declared

The responsible person for an Operational Department has declared READY, NOT READY, or BLOCKED for the current Venue opening. NOT READY and BLOCKED include a reason.

### Venue Opened for Business Date

An authorized Host has intentionally opened the Venue after every mandatory Operational Department declared READY. This creates the official operational start of the Business Date and its permanent Opening Report.

### Venue Deactivated

A Venue has stopped accepting new live activity while historical records remain.

### Area Established

A major operational section has been added to a Venue.

### Zone Created

An authorised Master user has created a dynamic operational grouping for a Venue.

### Zone Renamed

An authorised Staff Member has changed a Zone’s operational name without changing any Service Location identity.

### Service Location Reassigned to Zone

An authorised Staff Member has moved a Service Location into a different operational Zone without changing its physical Area, Digital Identity, active Customer Group, or history.

### Zone Deleted

An authorised Staff Member has removed an operational grouping without deleting or changing the Service Locations it contained.

### Zone Template Applied

An authorised Master user has applied a future Zone Template before service to create the initial operational Zone arrangement. This event is not part of the first version.

### Service Location Made Available

A Service Location has become eligible to receive a Customer Group or transfer.

### Service Location Made Unavailable

A Service Location has been intentionally blocked from receiving a new Customer Group or transfer.

## Staff and shift events

### Staff Member Added

An individual has been recognized as an authorized Staff Member of the Organization.

### Staff Member Deactivated

A Staff Member has lost authority to perform new work while historical actions remain attributed to them.

### Role Assigned

A Staff Member has been given an approved Role for an Organization or Venue context.

### Role Removed

A Staff Member’s named business responsibility has ended without changing past actions or silently changing separately granted Capabilities.

### Capability Granted

A Staff Member has received explicit authority to perform one defined action in an approved context.

### Capability Revoked

A Staff Member’s explicit authority to perform one defined action has ended without changing past actions.

### Shift Started

A Staff Member has begun an approved period of work at a Venue.

### Shift Ended

A Staff Member has completed an approved period of work at a Venue.

### Shift Handover Completed

Operational responsibility has been deliberately passed from one Staff Member or Shift to another.

## Customer Group and service events

### Customer Group Opened

A Responsible Waiter has intentionally started official service for a party at an available Service Location. If the location is a Beach Sunbed, the approved immediate financial obligation is created as part of this outcome.

### Responsible Waiter Assigned

An eligible Staff Member has accepted responsibility for an active Customer Group.

### Responsible Waiter Changed

Responsibility for an active Customer Group has moved from one eligible Staff Member to another through an authorized action.

### Transfer Started

An authorized move of an active Customer Group to an available destination Service Location has begun but is not yet a completed business fact.

This event is optional for business history. It must never imply that the Customer Group has moved before completion.

### Transfer Completed

The complete Customer Group, including its Orders, optional Bill, Payments, Responsible Waiter, and History, has moved from the previous Service Location to the destination as one successful action.

### Transfer Rejected

A requested transfer did not occur because a business rule was not satisfied. Both locations and the Customer Group remain unchanged.

### Customer Group Completed

The Customer Group’s service has ended after any Bill and all outstanding operational work satisfied the approved completion rules. A Customer Group that never received a financial obligation may complete without ever having a Bill.

## Menu events

### Menu Activated

A reviewed Menu has become available in an approved Venue and context.

### Menu Retired

A Menu has stopped accepting new selections while historical Orders remain unchanged.

### Menu Item Made Available

A Menu Item has become selectable in an approved Menu context.

### Menu Item Made Unavailable

A Menu Item has stopped being selectable for new Orders without changing past Order Items.

### Menu Item Price Changed

A new approved selling price has taken effect prospectively. Existing Order Items and Bill Lines remain unchanged.

## Order and preparation events

### Order Submitted

A reviewed round of Order Items has been safely accepted as one Order for an active Customer Group. The business may now rely on it for preparation and billing.

### Order Submission Rejected

A proposed Order was not accepted because a business rule failed. It must not be treated as sent, billed, or ready for preparation.

### Order Item Cancelled

An authorized cancellation has removed the financial and fulfillment effect of a submitted Order Item while preserving its history.

### Order Item Corrected

An authorized correction has addressed an error without silently rewriting the original Order Item.

### Kitchen Ticket Created

A submitted Order containing Kitchen items has produced confirmed work for the Kitchen.

### Bar Ticket Created

A submitted Order containing Bar items has produced confirmed work for the Bar.

### Kitchen Ticket Acknowledged

Kitchen Staff have recognized the Ticket as active work.

### Bar Ticket Acknowledged

Bar Staff have recognized the Ticket as active work.

### Kitchen Ticket Ready

The Kitchen has marked the approved Ticket work as ready for the next service step.

### Bar Ticket Ready

The Bar has marked the approved Ticket work as ready for the next service step.

### Kitchen Ticket Completed

The Kitchen’s responsibility for the Ticket has been completed under the approved workflow.

### Bar Ticket Completed

The Bar’s responsibility for the Ticket has been completed under the approved workflow.

## Billing and payment events

### Bill Created

A Bill has been created because a Customer Group received its first approved financial obligation. Customer Group opening alone creates no Bill unless opening at a Beach Sunbed creates the immediate approved Beach Sunbed obligation.

### Bill Line Added

An approved Order, charge, discount, correction, or other financial reason has contributed a new explainable line to the Bill.

### Bill Line Reversed

An authorized action has offset a previous Bill Line while preserving the original financial fact.

### Payment Recorded

The business has confirmed receipt of an exact amount against a Bill through an approved Payment Method.

### Payment Rejected

A payment attempt was not accepted and did not reduce the Bill balance.

### Payment Reversed

An authorized action has reversed a previously recorded Payment while preserving its history.

### Bill Fully Paid

Valid Payments have reduced the Bill’s remaining balance to zero. This fact does not bypass any other closing requirement.

### Bill Closed

An authorized Staff Member has confirmed that the Bill satisfies all approved closing conditions. It no longer accepts ordinary financial or ordering activity.

### Bill Reopened

A closed Bill has returned to an active state through a separately approved exceptional rule. This event is forbidden until such a rule is accepted.

## Accountability events

### Activity Logged

A required Activity Log has been created for a sensitive or accountability-relevant business event.

`Activity Logged` does not replace the more specific event. For example, a transfer may produce both `Transfer Completed` and `Activity Logged` because the first describes the operational fact and the second confirms that the required accountability record exists.

---

# DOMAIN GLOSSARY

## Agreed terms

### Active

Currently permitted to participate in new business activity. Active does not mean that an entity is busy or occupied.

### Activity Log

The trustworthy business history of a sensitive, exceptional, or accountability-relevant event, including who acted, what happened, and when.

### Adjustment

An authorized financial change that adds to or reduces a Bill while preserving the original financial history.

### Area

A major recognizable physical section of a Venue, such as Beach, Pool, or Upper Level.

### Available

Eligible to be selected for a new business action. For a Service Location, available means it can receive a Customer Group or transfer.

### Balance

The exact amount still due on a Bill after valid charges, adjustments, and Payments are considered.

### Bar Ticket

The Bar’s confirmed preparation or fulfillment work created from the Bar-destination items of one Order.

### Bill

The complete running financial obligation created for a Customer Group when its first approved financial obligation exists.

### Bill Closure

The authorized action that ends ordinary financial activity on a Bill after all approved conditions are satisfied.

### Bill Line

One explainable financial contribution to a Bill, such as an ordered item, sunbed charge, discount, correction, or reversal.

### Business Date

The Venue operating day to which activity belongs. Its boundary may differ from midnight and requires Venue approval.

### Department Readiness

The current declared opening condition of an Operational Department: READY, NOT READY, or BLOCKED. NOT READY and BLOCKED require a reason.

### Beach Sunbed

A sunbed-set Service Location in the physical Beach Area. Officially opening its Customer Group creates the approved immediate Beach Sunbed financial obligation.

### Category

In the phrase Menu Category, a meaningful group that helps people find related Menu Items. It does not automatically define preparation or accounting treatment.

### Closed Bill

A Bill whose approved closing conditions have been confirmed and which no longer accepts ordinary Orders, lines, or Payments.

### Capability

Explicit business authority for a Staff Member to perform one defined action in an approved context. A Capability is separate from Role and never bypasses business rules.

### Completed Customer Group

A Customer Group whose service, operational work, and any Bill have met the approved completion conditions.

### Correction

An authorized action that addresses an error while preserving what originally happened.

### Customer

A person receiving hospitality service. The initial product does not require an individual customer identity or account.

### Customer Group

The primary operational entity representing one party and its Service Location, Orders, optional Bill, Payments, Responsible Waiter, and History from official opening through completion.

### Destination

The approved preparation or fulfillment responsibility for an Order Item. Initial destinations are Bar, Kitchen, and No Preparation.

### Domain Entity

A person, place, thing, record, or concept with a distinct business identity and lifecycle in the Emerald domain.

### Domain Event

A meaningful business fact stating that something has happened.

### Draft Order

An unconfirmed selection of proposed items. It is not an Order and has not been sent, billed, or committed to preparation.

### History

The preserved operational and financial story of a Customer Group, including its Service Locations over time, Responsible Waiter changes, Orders, optional Bill, Payments, and relevant Activity Logs.

### Host

A Staff Member responsibility that coordinates daily Venue opening and may open the Venue after every mandatory Operational Department is READY when holding the required Capability. The Host does not personally verify every department and does not officially open a Customer Group.

### Inactive

Not permitted to participate in new business activity while historical meaning remains preserved.

### Kitchen Ticket

The Kitchen’s confirmed preparation work created from the Kitchen-destination items of one Order.

### Menu

An approved collection of offerings available in a particular Venue, period, or service context.

### Menu Category

A meaningful heading used to organize related Menu Items within a Menu.

### Menu Item

One distinct product or service that may be selected for an Order under approved availability and pricing rules.

### Master User

A Staff Member holding the Master Role for business responsibility. The Role alone grants no authority; the Staff Member must hold the required Capability, such as Manage Zones or the future Manage Zone Templates.

### No Preparation

The destination for an approved Order Item that requires no Bar or Kitchen preparation work.

### Occupied

The state of a Service Location currently assigned to an active Customer Group.

### Order

One safely submitted and confirmed ordering round of requested Order Items for an active Customer Group.

### Order Item

One confirmed item, quantity, price, preparation destination, and instruction within an Order.

### Opening Report

The permanent daily operational record of a completed Venue opening, including opening time, Host, department readiness, delays, blocking issues, reasons, and comments.

### Operational Department

One recognized part of a Venue operation that owns a distinct area of opening readiness and has a responsible person declare its status.

### Organization

The highest business boundary in Emerald Management System, owning or operating one or more Venues.

### Outstanding Work

Confirmed service, preparation, financial, or accountability activity that has not yet reached its approved completion state.

### Payment

An exact amount of value confirmed as received against one Bill through an approved Payment Method.

### Payment Attempt

An effort to make a Payment that has not yet been confirmed as received. It does not reduce the Bill balance.

### Payment Method

An approved business form through which a Venue may receive value, such as Cash or Card.

### Preparation Ticket

The general term for destination-specific preparation work. In the initial domain, the concrete preparation tickets are Kitchen Ticket and Bar Ticket.

### Price

The exact approved monetary value of an offering in a defined business context. A submitted Order Item preserves the price that applied to it.

### Physical Row

A stable physical grouping of Beach Sunbed Service Locations used for position, display, and approved charging rules. It is independent from dynamic operational Zones.

### Responsible Waiter

The one eligible Staff Member accountable for coordinating service for an active Customer Group at a given time. The Responsible Waiter intentionally opens the Customer Group.

### Retired

No longer available for new use but preserved in historical records.

### Role

An approved set of business responsibilities assigned to a Staff Member. A Role does not itself authorize actions; Capabilities do.

### Service Location

One identifiable place, such as a sunbed set or upper table, where one active Customer Group can receive service.

### Service Location Digital Identity

The stable, technology-neutral identity that resolves to one enduring Service Location and allows its current state to be retrieved from the central system. NFC is the preferred initial identification method, while manual lookup remains available. The Digital Identity contains no changing operational, financial, customer, permission, or other sensitive business data and does not authorize or perform an action.

### Shift

A defined period during which one Staff Member works at one Venue in an approved business capacity.

### Staff Member

One individual person authorized to work for an Organization or Venue.

### Submission

The point at which a reviewed draft becomes a confirmed Order that the business may rely upon for preparation and billing.

### Sunbed Charge

An approved Bill Line applied for sunbed service according to the applicable physical Row and charging rule. Dynamic operational Zone membership does not itself determine the charge.

### Sunbed Set

A Service Location made up of the physical sunbeds treated as one unit for assignment and service. A Beach Sunbed creates its approved financial obligation when the Responsible Waiter officially opens the Customer Group.

### Transfer

The complete, authorized movement of an active Customer Group, including its Orders, optional Bill, Payments, Responsible Waiter, and History, from one Service Location to another available Service Location.

### Unavailable

Temporarily or permanently not eligible for a new business action. An unavailable Service Location cannot receive a Customer Group or transfer.

### Venue

One physical hospitality operation where staff serve customers under an Organization.

### Zone

A dynamic operational grouping of an arbitrary collection of Service Locations within one Venue. A Zone is independent from Area, physical layout, Service Location identity, and financial charging rules.

### Zone Template

A future reusable plan that an authorised Master user may apply before service to create the initial operational Zone arrangement for a Venue.

## Terms that must not be confused

- **Organization and Venue:** The Organization is the operating business boundary; the Venue is one physical hospitality operation.
- **Area and Zone:** Area describes a permanent physical section of a Venue. Zone is a dynamic operational grouping that may contain Service Locations from several Areas.
- **Service Location and physical furniture:** A Service Location is the unit assigned and served. It may contain several physical sunbeds.
- **Customer and Customer Group:** A Customer is one person; a Customer Group is the party served together. The product does not require individual customer identities initially.
- **Customer Group and future Visit:** Customer Group is the complete primary operational entity. Visit is not a core concept and may be introduced later only if it gains a distinct approved purpose.
- **Customer Group and Shift:** A Customer Group follows the party’s service lifecycle; a Shift follows a Staff Member’s working period. A Customer Group may continue across Shifts.
- **Role, Capability, and Staff Member:** A Staff Member is a person. A Role groups responsibilities. A Capability explicitly authorizes one defined action.
- **Menu Item and Order Item:** A Menu Item is the current offering; an Order Item is the preserved fact of what was ordered.
- **Order and Ticket:** An Order is the Customer Group’s confirmed round; a Ticket is destination-specific preparation work created from it.
- **Order and Bill:** An Order describes requested goods or services; the Bill describes the financial obligation created by approved Orders and other charges.
- **Bill and Payment:** A Bill is what is owed; a Payment is value confirmed as received against it.
- **Payment Attempt and Payment:** An attempt is not financial receipt. Only a confirmed Payment reduces the Balance.
- **Cancellation and deletion:** Cancellation preserves the original business fact and removes or offsets its effect. Deletion would erase history and is forbidden for confirmed operational and financial facts.
- **Correction and rewriting:** A correction creates an explainable change. Rewriting would conceal the original fact and is forbidden.
- **Available and active:** Available means eligible for selection; active means currently permitted to participate in new business activity.
