# Emerald Management System — Domain Consistency Review

> **Historical review status — superseded in part on 2026-07-21.** This report records the domain state before accepted decisions DEC-031 through DEC-038. Those decisions resolve Customer Group versus Visit, dynamic Zones, delayed Bill creation, Beach Sunbed opening charges, waiter-only Customer Group opening, multiple ordering rounds, future Zone Templates, and Capability-based authorization. Use `DOMAIN_MODEL.md` and `DECISIONS.md` for current rules. Findings and questions on those resolved subjects are retained here as review history, not as current open decisions.

## 1. Purpose

This report is the final business-domain consistency review before application implementation.

It compares every document currently in `docs/`, with particular attention to:

- `MASTER_BLUEPRINT.md`;
- `PRODUCT_REQUIREMENTS.md`;
- `ARCHITECTURE.md`;
- `DEVELOPMENT_PLAN.md`;
- `DECISIONS.md`;
- `DOMAIN_MODEL.md`.

`PRODUCT_VISION.md` and `README.md` were also reviewed.

The review looks for conflicting meanings, duplicated concepts, missing definitions, unresolved business rules, and gaps in important operating flows. It does not propose database structures, APIs, screens, or application implementation.

## 2. Overall assessment

The documents agree strongly on the product’s purpose and safety principles:

- one shared operational truth;
- reliable orders and financial records;
- one responsible waiter where waiter responsibility is required;
- separate Bar and Kitchen preparation work;
- several ordering rounds on one running Bill;
- complete and traceable movement of a party and Bill;
- controlled Payments and Bill closing;
- individual accountability for sensitive actions;
- one first Venue with a path to future multi-venue operation.

The domain is broad enough to support the intended product. However, it is not yet internally consistent enough to begin business-feature implementation. Several central concepts have different meanings across the approved documents, and some rules that control money or responsibility are still explicitly undecided.

The most important conflict is the introduction of **Visit** as a separate entity after earlier documents used **Customer Group** for both the party and the service visit. The second major conflict is that **Zone** now appears to contain the meaning previously given directly to a sunbed **Row**. Transfer boundaries and responsibility for upper tables also remain unresolved.

No document should be silently interpreted to resolve these conflicts. The owner should answer the critical questions in this report, after which the permanent documents and decision log should be aligned through a separately approved documentation change.

## 3. Source-of-truth conflict

`MASTER_BLUEPRINT.md` describes itself as the permanent product and architecture reference. `DOMAIN_MODEL.md` describes itself as the single source of truth for the business domain. These roles can coexist if their authority is made explicit:

- the Master Blueprint governs enduring product and engineering principles;
- the Domain Model governs business terms, entity meanings, lifecycles, relationships, and business events;
- the Decision Log governs why material choices were accepted or changed;
- requirements govern approved delivery scope and acceptance.

At present, no decision formally states this order of authority. Where the Blueprint and Domain Model disagree, a future contributor cannot know which wording wins merely from the existing documents.

This is critical because the documents already disagree about Customer Group, Visit, Activity Record versus Activity Log, and Row versus Zone.

---

# CRITICAL BEFORE IMPLEMENTATION

## C1. Customer Group and Visit currently overlap

### What the documents say

- `PRODUCT_REQUIREMENTS.md` says a Customer Group represents the people using one location **and their open Bill**. It opens, orders, moves, pays, and closes.
- `MASTER_BLUEPRINT.md` defines Customer Group as “the active service visit associated with one service location and one running bill.” It also says the Customer Group is the stable identity of the visit.
- DEC-011 allows one active Customer Group per Service Location.
- DEC-012 says the Customer Group, Bill, Orders, notes, Payment state, and waiter move during a transfer.
- `DOMAIN_MODEL.md` separates the concepts: Customer Group means the people served together, while Visit means the full service period and operational context. It places the location, waiter, Orders, and Bill on the Visit.

### Why this matters

Both models can work, but they are not the same model. If both entities remain, staff language, acceptance tests, responsibility changes, transfers, completion, and historical reporting must consistently follow Visit. If Visit is removed, Customer Group must carry the complete operational lifecycle described in the older documents.

Keeping two names for the same business identity would create unnecessary complexity and make statements such as “open the group,” “complete the visit,” and “move the group” ambiguous.

### Assessment

Customer Group and Visit are necessary as separate concepts only if the business needs to distinguish:

- **who is being served together** from
- **the service occasion during which they are served**.

That distinction becomes valuable when a known or reserved party may return for another Visit, when one Visit may later contain more than one party or Bill, or when visit-level timing and history matter independently of the party.

For the initial anonymous, one-party, one-Bill operation, the distinction provides limited immediate business value. A Customer Group exists only for one Visit, has no independent identity before or after it, and is not a customer profile. Under those rules, the two entities behave almost one-to-one and are largely duplicative.

### Required resolution

Choose one of these business models before implementation:

1. **Simpler initial model:** Customer Group is the complete service occasion and party, as in the earlier documents. Do not use Visit as a separate entity yet.
2. **Separated long-term model:** Customer Group means only the party; Visit owns the operational lifecycle, location, responsible waiter, Orders, Bill, and completion. Update the older language and decisions to use Visit consistently.

The second model has a clearer long-term separation, but the owner must confirm that the extra concept is understandable and genuinely useful now.

## C2. The occupancy rule uses two different subjects

DEC-011 says one active Customer Group may occupy a Service Location. `DOMAIN_MODEL.md` says one active Visit may occupy it. This is a direct consequence of C1, but it affects a core safety rule.

There must be one unambiguous answer to: “What occupies a Service Location?” The same subject must be used for opening, transfer, availability, responsibility, and completion.

## C3. Customer Group Opened and Visit Opened duplicate one moment

`DOMAIN_MODEL.md` defines both events, but the initial relationship is one Customer Group to one Visit and both begin together. It does not explain whether one can occur without the other or which event staff mean by “open a group.”

If both concepts remain, the business must define the separate fact represented by each event. Otherwise, keep one opening event.

## C4. Row and Zone are not aligned

### What the documents say

- Requirements and development planning use **Row** directly for beach layout and sunbed charging.
- The Blueprint defines Row as a grouping used for position, display, and charging.
- `DOMAIN_MODEL.md` introduces **Zone** as the general subdivision of an Area and says a beach row may be a Zone.
- The Domain Glossary defines Sunbed Charge as a Bill Line whose rule “may consider the Zone.”

### Why this matters

It is unclear whether:

- Row remains its own domain concept;
- Row is one type of Zone;
- Zone replaces Row everywhere; or
- a Service Location can belong to both a Row and another Zone.

This affects venue mapping, sunbed charges, staff language, transfers, and reporting. A general Zone is useful for pool sides or upper-table sections, but it must not weaken the precise meaning of a chargeable beach Row.

### Required resolution

The recommended business wording is: **Zone is the general concept; Row is a named kind of Zone used where the Venue operates by rows.** The owner must confirm this and confirm whether every sunbed set belongs to exactly one charge-relevant Row Zone.

## C5. Allowed transfer destinations are inconsistent

### What the documents say

- The requirements describe moving an entire group from one sunbed set to another sunbed set.
- DEC-012 says the move is between locations but discusses sunbeds.
- The Domain Model defines Transfer between any two Service Locations.
- Service Location includes beach sunbed sets, pool sunbed sets, and upper tables.

### Why this matters

The Domain Model currently permits movement:

- between beach sunbeds;
- between pool sunbeds;
- from beach to pool;
- from pool to beach;
- from a sunbed to an upper table;
- from an upper table to a sunbed;
- between upper tables.

The earlier requirements authorize only sunbed-to-sunbed movement. The wider meaning may be correct, but it has not been approved. It also affects sunbed charges and waiter responsibility.

### Required resolution

Approve the allowed source and destination combinations. If some moves are not operationally meaningful, they must be forbidden explicitly.

## C6. The financial effect of transfer is unresolved

Every relevant planning document identifies this question but does not answer it: when a Customer Group moves to a differently priced Row or Zone, does the Bill:

- keep the original sunbed charge;
- replace it with the destination charge;
- add only the difference;
- apply a second charge; or
- require a Manager decision?

This is a critical money rule and must be decided before transfer or sunbed-charge work begins.

The rule must also cover movement between beach, pool, and upper-table location types if those transfers are allowed.

## C7. Responsible waiter scope is unresolved

### What the documents say

- Requirements require one responsible waiter for each occupied sunbed set.
- They say upper tables should also have one “unless the owner decides otherwise.”
- The Blueprint says a responsible waiter is required “where the business rules require one.”
- The Domain Model repeats that conditional wording.

### Why this matters

The one-waiter rule cannot be tested until the business identifies which active Visits require it. It is also unclear whether the rule applies identically to beach sunbeds, pool sunbeds, and upper tables.

### Required resolution

The owner must define the Service Location types that require one Responsible Waiter and whether any Visit is allowed to be active temporarily without one.

## C8. Waiter handover is only partly defined

The domain supports `Responsible Waiter Changed` and `Shift Handover Completed`, and it forbids ending a waiter’s Shift while active Visits lack an approved Responsible Waiter. This is directionally correct.

However, the business has not decided:

- who may perform a handover;
- whether the receiving waiter must accept it;
- whether Visits move individually or as a group;
- what happens if the receiving waiter is not currently working;
- whether open Orders or ready Tickets require special acknowledgment;
- whether a Shift can end while a handover is incomplete.

At minimum, before implementation, the business must approve who can change responsibility and whether acceptance by the new waiter is required.

## C9. Staff Member, User, Role, and Permission are incomplete as a set

### What the documents say

- Requirements describe users, user accounts, login, and roles.
- The Blueprint defines User, Role, Permission, and Staff Session.
- DEC-014 relies on permissions.
- The Domain Model defines Staff Member and Role but omits User, Permission, and Staff Session from its entities and glossary.
- The Domain Model says Staff Members have authority but does not define the business distinction between a person and the account used to act.

### Boundary assessment

- **Staff Member** should mean the real individual recognized by the business.
- **User** should mean that person’s access identity, if the term is retained.
- **Role** should mean a named bundle of business responsibilities.
- **Permission** should mean authority to perform one particular sensitive or ordinary action.
- **Shift** should mean a period of work, not an account session and not a Role.

These concepts are not interchangeable.

### Required resolution

The business must decide whether User belongs in the business Domain Model or remains an access/security concept outside it. Either way, the relationship must be explicit. The rules already say shared accounts should be avoided and actions must be attributed to individuals, but the documents do not state whether every Staff Member has exactly one User identity, may have none, or may have more than one.

Permission also requires one agreed definition because sensitive authority is repeatedly described through it.

## C10. Shift may be premature or may be required for handovers

`DOMAIN_MODEL.md` treats Shift as a core entity. Earlier requirements explicitly exclude staff scheduling and do not require staff to start or end Shifts. The Development Plan does not introduce Shift management in the first operational phases.

A working-period Shift can be valuable without becoming a scheduling or payroll feature, especially for handovers and accountability. However, adding it to the core domain creates mandatory questions about starting work, ending work, overlapping shifts, and responsibility transfer.

The owner must decide whether Shift is:

- part of the first operational domain;
- retained as a defined future concept but not used initially; or
- unnecessary until scheduling or till reconciliation is introduced.

## C11. Ticket lifecycle and service completion are unclear

Requirements say Bar and Kitchen Staff may mark work “being prepared” or “ready.” The Domain Model adds acknowledged and completed states. It does not define whether “completed” means:

- preparation finished;
- the Ticket collected by a waiter;
- every item delivered to the Customer Group; or
- the preparation team has no more responsibility.

The Domain Model also says a Visit cannot complete while “outstanding operational work” exists, but Outstanding Work is defined broadly. Without a clear final preparation/service state, the business cannot know whether a paid Customer Group may leave while a Ticket remains ready or whether delivery tracking is required.

The initial status sequence and meaning of completion must be approved before Order and Ticket implementation.

## C12. Order cancellation and correction rules are not approved

All documents agree that submitted Orders and Order Items cannot be silently changed. They allow authorized cancellation or correction with Activity Logging. However, they do not decide:

- which Roles may cancel or correct;
- whether Bar or Kitchen acknowledgment changes what is allowed;
- whether prepared items can be cancelled financially;
- whether quantity can be partly cancelled;
- which reasons are mandatory;
- whether a Manager must approve some cases.

These decisions are necessary before cancellation or correction behaviour is built. If cancellation is deferred, the first release still needs an approved operational response to an incorrectly submitted item.

## C13. Payment rules and Bill closing are incomplete

The documents agree on exact Payments and forbid duplicate recording. They do not yet agree on or define:

- whether partial Payments are allowed;
- whether several Payment Methods may be used on one Bill;
- whether overpayment is allowed and how change is understood;
- whether tips are part of the Bill or separate;
- whether a failed card attempt is recorded as business history;
- who may reverse a Payment;
- whether a Manager may close a Bill with a non-zero Balance;
- the exact conditions beyond zero Balance that must be met before closing.

The requirement permitting a recorded Manager exception for a non-zero Balance conflicts with the Domain Model, which says such an exception is forbidden until separately approved. The owner must either approve the exception and its meaning or remove it from the expected first version.

## C14. Bill completion and Visit completion need one ordered rule

The Domain Model says:

- a Visit cannot complete while its Bill is open or unresolved;
- a Bill closes after approved conditions are met;
- a Visit completes after the Bill and outstanding operational work are resolved.

This sequence is sensible but not fully agreed elsewhere. The requirements say closing the Bill makes the location available, while the Domain Model makes availability depend on the Visit leaving or transferring. Those are different moments if a paid group remains seated or preparation work remains outstanding.

The business must decide whether:

- Bill Closed automatically completes the Visit and releases the Service Location;
- the Visit completes through a separate departure action; or
- the Service Location may remain occupied after payment for a controlled period.

This is a critical venue-occupancy rule.

## C15. The authority of Domain Model versus earlier terminology must be recorded

The Domain Model says it is the single source of truth, but accepted decisions and the Blueprint still use older meanings. A new business domain document does not automatically supersede accepted decisions under the project’s own decision rules.

After the owner answers the critical questions, a new accepted decision should state the domain authority and explicitly supersede or reinterpret affected decisions such as DEC-011 and DEC-012. Until that happens, future contributors face two approved meanings.

---

# IMPORTANT BUT CAN BE DECIDED LATER

These matters do not need to block the start of unrelated foundation or design work, but each must be decided before its affected feature is implemented.

## I1. Area and Zone boundary is sound after Row is resolved

The proposed boundary is useful:

- Area is a large staff-recognized part of a Venue.
- Zone is a meaningful subdivision inside an Area.
- Service Location is the actual unit assigned to a party.

Zone should not become an arbitrary tag used for every report or setting. A grouping without physical or operating meaning should use a different future concept.

Open later questions include whether a Service Location may exist directly in an Area without a Zone, whether every Area needs Zones, and how seasonal layout changes preserve historical names.

## I2. Order and Preparation Ticket boundary is valid

The documents correctly separate:

- **Order:** the Customer Group’s confirmed round of requested items;
- **Preparation Ticket:** destination-specific work created from that Order.

One Order may create a Bar Ticket, a Kitchen Ticket, both, or neither when all items require No Preparation. The Ticket must never become a second Order or create a second charge.

The remaining design question is whether Kitchen Ticket and Bar Ticket are genuinely separate business entities or two named types of one Preparation Ticket. Their purpose, lifecycle, rules, and relationships in `DOMAIN_MODEL.md` are nearly identical.

Using one Preparation Ticket concept with a Destination of Bar or Kitchen would remove duplication and allow future stations. Keeping separate terms may be easier for venue staff. This can be decided before preparation work is designed, provided the business meanings remain identical.

## I3. Bill and Bill Line boundary is clear

The distinction is necessary and well defined:

- Bill is the complete running financial obligation for a Visit.
- Bill Line is one explainable financial contribution.

Bill is not merely the total; it has an open-to-closed lifecycle. Bill Line is not a Payment. Original lines remain visible when corrected or reversed.

Later decisions are still needed for taxes, discounts, reversals, tips, service charges, and allocation of Payments, but the entity boundary itself is sound.

## I4. Activity Log and Activity Record use different names

The Blueprint uses **Activity Record**. Requirements and the new Domain Model use **Activity Log** or “activity history.” The meaning is effectively the same.

One term should be selected. `Activity Log` is already the full entity in the Domain Model, but “log” can sometimes sound like a technical system log rather than a protected business record. `Activity Record` is clearer for some business readers. This terminology decision can wait until activity-history design, but both terms should not remain permanent synonyms.

## I5. Manager and Administrator are not cleanly separated

Requirements combine “Manager / Administrator.” The Role examples use Manager only. Some described work is operational management; other work is system administration.

The owner should later decide whether:

- Manager includes both operational and configuration responsibility;
- Administrator is a separate Role; or
- authority is granted through specific Permissions regardless of Role name.

Sensitive authority should not be inferred from a broad title.

## I6. Sunbed Charge is a business concept but not a full entity

The Domain Model defines Sunbed Charge in the glossary and treats it as a kind of Bill Line. This is sufficient if the charge is simply a financial outcome of an approved rule.

What remains undefined is the charging policy itself:

- when it is applied;
- whether it is per set, sunbed, person, or Visit;
- which date and time select the price;
- whether it may be waived;
- whether minimum consumption replaces it;
- how complimentary use works.

These are business rules, not necessarily a reason to introduce another entity.

## I7. Menu availability and price context are broad

The Domain Model allows Menus by Venue, time, season, Area, or event, while the requirements need only straightforward categories and items initially. This is not a contradiction, but it risks introducing unapproved variability.

The first release should explicitly select the smallest required availability model. Organization-wide templates, timed Menus, and Area-specific Menus can remain future considerations.

## I8. No-Preparation Order Items need an operational meaning

The documents allow a Menu Item destination of No Preparation. It is unclear whether such an item:

- is considered fulfilled immediately on Order submission;
- requires a waiter action;
- represents a charge rather than a product; or
- should sometimes bypass Order entirely and become a direct Bill Line.

This can be decided when the first actual Menu and charge examples are reviewed.

## I9. Business Date is defined but not governed

The Domain Glossary defines Business Date, and the Blueprint notes shifts continuing after midnight. No document approves the Venue’s business-day boundary.

This can wait until reporting, end-of-day, and reconciliation work, but it must be set before those features or production transaction reporting begin.

## I10. Customer Group size and identity are optional but unclear

The Domain Model correctly avoids requiring personal customer information. It does not decide whether group size is recorded. Group size could affect capacity, reporting, or future charges, but collecting it adds staff work.

Do not assume group size or customer identity is required without a business purpose.

## I11. Upper tables and sunbed charges

Requirements say upper tables do not receive a sunbed charge unless the owner decides otherwise. The Domain Model permits generic approved charges but does not restate this default.

The initial rule should be confirmed before venue and billing acceptance examples are written.

## I12. Visit cancellation is undefined

The Domain Model says opening may be cancelled under an approved rule, but no document defines when a newly opened but unused Visit may be cancelled rather than completed. This can be decided before Visit correction flows are built.

## I13. Ticket cancellation and reopening are unclear

The Domain Model mentions Ticket problems and cancellations but defines no events for Ticket Cancelled or Ticket Reopened. It says completed work cannot be silently reopened, implying an authorized reopen might exist.

The initial product may avoid Ticket reopening if Order Item correction produces clear new work. This should be decided with real Bar and Kitchen workflows.

## I14. Shift and business-day reporting boundaries differ

The Domain Model correctly says a Shift is not a business day and a Visit may cross Shifts. Reports by waiter, Shift, and business day therefore answer different questions. The business should approve which dates and responsibility points apply to sales-by-waiter reporting before that report is implemented.

## I15. Proposed engineering decisions remain marked Proposed

The engineering foundation has now been approved by the owner, but DEC-021 through DEC-029 still have Status “Proposed.” This is a governance inconsistency rather than a business-domain defect.

It does not block domain design, but it should be resolved before contributors rely on the Decision Log as an accurate record of approved engineering choices.

---

# FUTURE PRODUCT CONSIDERATIONS

These are valid future questions but should not expand the initial domain without separate approval.

## F1. Multiple Customer Groups or Bills within one Visit

The Domain Model hints that a future Visit might include multiple groups or Bills. This should not be generalized now. It would materially change occupancy, ordering, transfer, and payment rules.

## F2. Returning customers and reservations

Separating Customer Group from Visit becomes more valuable if a known party or reservation can have several Visits. The current product intentionally avoids customer accounts and reservations.

## F3. Combining and splitting groups

Combining or splitting Customer Groups is forbidden initially. Future support would require explicit rules for Orders, Tickets, responsibility, locations, Bills, and Payments.

## F4. Joining and splitting Service Locations

Large parties may eventually use several sunbed sets or tables. The current one-Visit-per-location rule does not support a group occupying several locations at once. This is a separate future capability, not an exception to add casually.

## F5. Reservations, cleaning, maintenance, and capacity

Service Location states beyond Available, Occupied, Unavailable, and Retired may become useful. They should be based on observed venue needs.

## F6. Multiple preparation stations

Future Venues may have more than one Bar or Kitchen station. The preparation domain should remain capable of adding destinations or stations, but the initial business vocabulary should stay simple.

## F7. Stock, recipes, allergens, and modifiers

These concepts are intentionally outside the current domain. Item options and allergen information may become important sooner than full stock management and should receive separate domain review.

## F8. Fiscal documents and external payments

Receipt, tax, payment-terminal, accounting, refund, chargeback, and settlement concepts require professional and integration-specific review. A Bill is not automatically a legal receipt or fiscal document.

## F9. Multi-venue administration

Organization and Venue provide the correct starting boundary. Future questions include shared staff, shared Menus, Venue-specific prices, organization reporting, Venue transfers, and access across Venues.

## F10. Offline operation

Full offline operation remains outside the initial product. It does not change the business domain facts, but it raises difficult questions about when an Order or Payment becomes accepted. Those questions require a separate decision if offline work is later approved.

## F11. Customer-facing ordering and loyalty

Customer identity, customer-originated Orders, loyalty, deposits, and self-payment should not be added to the current terms until their business ownership and privacy rules are approved.

## F12. Staff scheduling, payroll, and performance

Shift is currently defined as an operating context, not a scheduling or payroll record. Future staff-management modules must not silently expand it or turn Activity Logs into generalized employee surveillance.

---

# BOUNDARY REVIEW SUMMARY

## Customer Group and Visit

**Current result:** Not resolved. The earlier model treats Customer Group as party plus service occasion. The new Domain Model separates party from service occasion.

**Recommendation:** Either use Customer Group alone for the first version or fully commit to Visit as the operational owner and revise all older terms. Do not implement both while they remain one-to-one and ambiguously opened together.

## Area and Zone

**Current result:** Conceptually useful, but Row is unresolved.

**Recommendation:** Area is the broad Venue section. Zone is its meaningful subdivision. Confirm Row as a specific kind of Zone and use one charge-relevant Zone for each sunbed set.

## Order and Preparation Ticket

**Current result:** Necessary and correctly separate.

**Recommendation:** Order remains the confirmed customer round. Preparation Ticket remains destination-specific work. Decide later whether Bar Ticket and Kitchen Ticket are separate entities or named types of Preparation Ticket.

## Bill and Bill Line

**Current result:** Necessary, clear, and consistent.

**Recommendation:** Keep both. A Bill owns the financial lifecycle and total obligation; Bill Lines explain each financial contribution. Preserve original lines through corrections and reversals.

## Staff Member, User, Role, and Shift

**Current result:** Staff Member, Role, and Shift have useful separate meanings, but User and Permission are missing from the Domain Model.

**Recommendation:** Keep Staff Member as the person, Role as a responsibility bundle, and Shift as a working period only if Shifts are required initially. Define User as the access identity or explicitly place it outside the business domain. Define Permission consistently before account and authorization work.

---

# CAPABILITY CHECK

## Movement between sunbeds and upper tables

**Supported in concept:** Yes. Transfer preserves the Visit, Customer Group, Bill, Orders, notes, Payment state, and responsibility while changing Service Location.

**Gap:** The allowed location-type combinations and financial effects are not approved. Earlier requirements authorize only sunbed-to-sunbed transfer, while the Domain Model permits any Service Location.

## One responsible waiter at a time

**Supported in concept:** Yes. The Domain Model allows exactly one Responsible Waiter at a time where responsibility is required and preserves changes in Activity Logs.

**Gap:** The Venue/location types requiring a waiter and whether a temporary unassigned state is allowed are not decided.

## Waiter handovers

**Supported in concept:** Yes. Responsible Waiter Changed and Shift Handover Completed cover the business facts.

**Gap:** Authority, acceptance, bulk handover, and incomplete-handover rules remain open.

## Several order rounds on one Bill

**Supported:** Yes. Each submitted round is a new Order for the same active service occasion, and all valid Bill Lines contribute to one Bill in the initial domain.

**Gap:** The service occasion must be named consistently as Customer Group or Visit.

## Bar and Kitchen preparation

**Supported:** Yes. One mixed Order may create separate destination-specific work while remaining one Order and one Bill.

**Gap:** Exact status meanings, final completion, cancellation, partial readiness, and delivery responsibility are not approved.

## Payment and Bill closing

**Supported in concept:** Yes. Payment is distinct from Payment Attempt and Bill, and Bill closing is controlled.

**Gap:** Partial/split Payments, overpayment, change, tips, reversal authority, non-zero closing exceptions, and the relationship between Bill closing, Visit completion, and location release remain open.

## Future multi-venue operation

**Supported:** Yes. Organization, Venue, venue ownership, data boundaries, and future shared configuration provide a sound business foundation.

**Gap:** Cross-Venue staff, Menus, Roles, reporting, and ownership-transfer policies can wait until expansion beyond the first Venue.

---

# OPEN BUSINESS DECISIONS FOR THE OWNER

The following questions collect every unresolved business choice found in the documents. Questions 1–22 should be answered before implementation of affected core features. Later questions may be answered before their related phase or future module.

## Critical questions

1. Should **Customer Group** mean both the party and its complete service occasion, or should **Visit** be kept as a separate concept for the service occasion?
2. If both Customer Group and Visit remain, what can happen to one without the other, and why does the business need both in the first version?
3. What exactly occupies a Service Location: the Customer Group or the Visit?
4. Should there be one opening event or two separate events called Customer Group Opened and Visit Opened?
5. Which document has final authority when business terms conflict: the Domain Model, Master Blueprint, Decision Log, or Product Requirements?
6. Is a beach **Row** one specific kind of **Zone**?
7. Must every beach sunbed set belong to exactly one charge-relevant Row Zone?
8. Can a Service Location exist in an Area without belonging to any Zone?
9. Which transfers are allowed: beach-to-beach, pool-to-pool, beach-to-pool, pool-to-beach, sunbed-to-upper-table, upper-table-to-sunbed, and upper-table-to-upper-table?
10. When a group moves to a differently priced Row or Zone, does it keep the original charge, use the new charge, pay the difference, receive a second charge, or require a Manager decision?
11. What happens to a sunbed charge when a group moves from a sunbed to an upper table or from an upper table to a sunbed?
12. Which Service Location types must always have one Responsible Waiter: beach sunbeds, pool sunbeds, upper tables, or all of them?
13. May an active service occasion ever be temporarily without a Responsible Waiter?
14. Who may change the Responsible Waiter?
15. Must the new waiter accept a handover before it becomes effective?
16. When a waiter ends a Shift, are all active assignments handed over together or one at a time?
17. Does the first version need Staff Shifts as a business concept, or can waiter handover work without formal Shift start and end?
18. What is the business difference between a Staff Member and a User account?
19. Does every Staff Member have one User account, can some have no account, and is more than one account ever allowed?
20. What does **Permission** mean, and which sensitive actions need their own explicit Permission?
21. Is Administrator a separate Role from Manager?
22. What are the exact initial Bar and Kitchen Ticket states, in their allowed order?
23. Does Ticket Completed mean preparation finished, collected by a waiter, delivered to the customer, or simply no longer the preparation team’s responsibility?
24. Can a Visit complete while a Bar or Kitchen Ticket is still new, preparing, or ready?
25. Who may cancel a submitted Order Item?
26. Who may correct a submitted Order Item?
27. Can an item be cancelled after the Bar or Kitchen has started or completed it?
28. Are partial item cancellation and quantity correction required?
29. Which cancellation or correction reasons must be recorded, and when is Manager approval required?
30. Are partial Payments allowed in the first version?
31. May one Bill be paid with more than one Payment Method?
32. Is overpayment allowed, and if cash change is given, what amount is recorded as the Payment?
33. Are tips recorded, and if so, are they part of the Bill or separate from it?
34. Who may reverse or refund a Payment?
35. May a Manager close a Bill with a non-zero Balance? If yes, in which exact situations and how is the remaining amount explained?
36. Besides a zero Balance, what must be true before a Bill can close?
37. Does closing the Bill automatically complete the service occasion and make the Service Location available?
38. If a group pays but remains seated, does its Service Location stay occupied, and how does staff later complete the service occasion?

## Important questions for later phases

39. Should Kitchen Ticket and Bar Ticket remain separate domain entities, or should they be two types of one Preparation Ticket?
40. Should the permanent business term be Activity Log or Activity Record?
41. When exactly is the sunbed charge applied: when service opens, when the group first occupies a sunbed, at a particular time, or at Bill closing?
42. Is a sunbed charge calculated per Service Location, physical sunbed, person, or Visit?
43. Can a sunbed charge be waived or discounted, and who may approve that?
44. Are complimentary sunbeds, minimum consumption, or partial-day charges required?
45. Do upper tables ever receive a sunbed or location charge?
46. Which Menus are needed initially: one Venue Menu, separate food and drink Menus, time-based Menus, or Area-specific Menus?
47. What does a No-Preparation Order Item mean operationally, and when is it considered fulfilled?
48. What time marks the end of the Venue’s Business Date for reporting and end-of-day work?
49. Should the number of people in a Customer Group be recorded?
50. When may an accidentally opened service occasion be cancelled instead of completed?
51. Can a completed or cancelled Ticket ever be reopened, and by whom?
52. For sales-by-waiter reporting, does credit belong to the waiter who opened the service occasion, submitted each Order, was responsible at closing, or share responsibility by time?
53. Which preparation statuses should waiters see, and which require their action?
54. Which Payment Methods are available at launch besides Cash and Card, if any?
55. Should failed Payment attempts appear in the business Activity Log, or only successful Payments and reversals?
56. How long should closed Bills, Payments, and Activity Logs be kept?
57. Which exact reports are essential for the first daily operation and accounting handoff?
58. Is the launch language Greek, English, or both?
59. Which phones, tablets, computers, and browsers must be supported at launch?
60. What Wi-Fi and backup-connectivity standard is acceptable before live use?

## Future product questions

61. May one Customer Group occupy more than one Service Location at the same time in the future?
62. May several Customer Groups share one Service Location in the future?
63. Will combining or splitting Customer Groups be needed?
64. Will one service occasion ever have several Bills?
65. Will reservations or named customer profiles be connected to future Visits?
66. Will Service Locations need capacity, reservation, cleaning, maintenance, or accessibility states?
67. Will the Venue need several Bar or Kitchen stations with different routing rules?
68. Will item sizes, additions, removals, allergen warnings, or courses be needed?
69. Which receipt printer, card terminal, fiscal, tax, or accounting connections will eventually be required?
70. Will staff work across several Venues under one Organization?
71. Will Menus, prices, and Roles be shared across Venues or managed separately?
72. Will full offline operation ever be required, and what business event should count as acceptance while disconnected?
73. Will customer-facing ordering, loyalty, deposits, gift cards, or prepaid credit be needed?
74. Will Shift grow into scheduling, attendance, cash-till reconciliation, or payroll, or remain only an operational working period?

---

# RECOMMENDATION

## Domain status: Not ready for implementation

The domain has a strong foundation and supports all intended operational capabilities in concept. Bill and Bill Line are clearly separated, Order and preparation work are correctly distinguished, multi-venue growth has a sound boundary, and the safety principles are consistent.

Application-feature implementation should not begin yet because the following central rules are unresolved:

- whether Customer Group and Visit are one concept or two;
- what occupies a Service Location;
- how Row relates to Zone;
- which location transfers are allowed and how they affect charges;
- where Responsible Waiter is mandatory and how handover works;
- how Staff Member, User, Role, Permission, and Shift relate;
- the Ticket lifecycle and meaning of completion;
- cancellation and correction authority;
- Payment, Bill closing, Visit completion, and location-release rules.

These are not minor wording issues. They determine operational responsibility, financial outcomes, and the lifecycle of the product’s central records.

The recommended next step is a focused owner review of questions 1–38. After the answers are approved, create new decision-log entries and align the Domain Model, Blueprint, requirements, and affected accepted decisions. Then perform a short confirmation review. If those changes resolve the critical findings without introducing new conflicts, the domain can become ready for implementation.
