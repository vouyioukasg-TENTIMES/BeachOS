# Project Glossary Review

## 1. Outcome

`PROJECT_GLOSSARY.md` establishes the official vocabulary for the Emerald Hospitality Operating System. It defines business language without describing application implementation, databases, APIs, or user-interface design.

No existing documentation, approved business decision, application code, or implementation file was changed.

## 2. Number of concepts documented

The glossary documents **23 official concepts**:

1. Customer Group
2. Guest Token
3. Service Location
4. Service Location Digital Identity
5. Zone
6. Zone Template
7. Order
8. Order Round
9. Order Item
10. Bill
11. Financial Obligation
12. Payment
13. Responsible Service Staff
14. Host
15. Cashier
16. Manager
17. Capability
18. Activity Log
19. Audit Trail
20. Product Philosophy
21. Decision Log
22. Domain Model
23. Hospitality Operating System

Every concept includes its Official Name, Definition, Why it exists, Typical Examples, Common Terms That Should NOT Be Used, and Related Domain Concepts.

## 3. Terms that appear ambiguous

### Guest Token and Customer Group

Guest Token is now defined as the temporary operational identity used to recognize a Customer Group. Existing approved documents do not yet define whether every Customer Group must have one, when association begins, whether one group may receive replacements, or whether a Token can be reused after completion.

The glossary therefore defines the concept and technology-neutral boundary without inventing its lifecycle.

### Guest Token and Service Location Digital Identity

Both may currently use NFC, but they identify different subjects:

- Guest Token identifies a Customer Group temporarily.
- Service Location Digital Identity identifies one enduring Service Location.

Their physical markers, business purpose, lifetime, and permitted information must remain distinct. Neither identification alone authorizes or performs an action.

### Responsible Service Staff and Responsible Waiter

The new official cross-venue term is Responsible Service Staff. Existing accepted decisions and current domain documents use Responsible Waiter and reserve official Customer Group opening for that person at Emerald Beach Club.

The glossary preserves this rule by treating Responsible Waiter as the current venue-specific responsibility, not as the universal product term. Replacing the older term throughout existing authoritative documents would require explicit Product Owner approval and a consistency review; it was not performed in this task.

### Order and Order Round

Order is the business entity; Order Round explains its meaning within continuing service. Each submitted Order is exactly one Order Round. The terms should not be used as two different entities unless a future approved decision creates a real distinction.

### Activity Log and Audit Trail

An Activity Log records one sensitive or accountability-relevant event. An Audit Trail is the connected chronological account assembled from multiple relevant records and business facts. Audit Trail should not become a duplicate core entity unless a separately approved business need gives it its own lifecycle.

### Role and Capability

Role describes business responsibility. Capability authorizes one defined action. The terms remain related but are never interchangeable, and neither one overrides a business rule.

## 4. Terms requiring Product Owner decisions

1. Must every active Customer Group have a Guest Token, or is it optional by Venue or service type?
2. At what exact moment is a Guest Token associated with a Customer Group, and who may perform that action?
3. May Guest Token identification find an existing Customer Group only, or may it take part in a separately confirmed opening workflow?
4. What information may a Guest Token safely contain, and must current business state always remain only in the central system?
5. What happens when a Guest Token is lost, damaged, duplicated, returned, or replaced?
6. When may a physical NFC Guest Card be reused, and what verification is required before reuse?
7. May one Customer Group have more than one active Guest Token, and may one Guest Token ever identify more than one Customer Group?
8. Which Staff Members and Capabilities may issue, associate, replace, disable, and receive Guest Tokens?
9. Should the current accepted term Responsible Waiter be formally superseded by Responsible Service Staff across the Domain Model, Decision Log, requirements, events, and Capability names?
10. If terminology changes, does the approved rule remain that only the responsible service person intentionally opens the Customer Group at Emerald Beach Club?
11. Should “Order Round” remain explanatory vocabulary for Order, or become a separately governed business concept?
12. Who may view an Audit Trail, for which business purposes, and for how long?

Until these questions are approved, the glossary must not be interpreted as authorizing automatic Customer Group opening, charging, ordering, transfer, Payment, access, or any other operational or financial action.

## 5. Recommendations for future additions

After the relevant business rules are approved, consider adding:

- Staff Member, Role, Shift, and History;
- Venue, Organization, Area, and Physical Row;
- Menu, Menu Category, and Menu Item;
- Bar Ticket, Kitchen Ticket, and Preparation Ticket;
- Bill Line, Balance, Payment Method, Payment Attempt, correction, and reversal;
- Business Date, Domain Event, and Customer Group completion;
- NFC Guest Card as an explicitly replaceable physical form of Guest Token, if its operational lifecycle requires a formal business definition;
- terms for reservations, deposits, refunds, tips, fiscal documents, and other future modules only after those concepts are approved.

## 6. Recommendation

Use `PROJECT_GLOSSARY.md` as the vocabulary reference for all new work. Before aligning older authoritative documents, the Product Owner should first resolve the Guest Token lifecycle and approve how Responsible Service Staff relates to the existing Responsible Waiter decisions. Historical Decision Log entries should never be rewritten merely to modernize terminology.
