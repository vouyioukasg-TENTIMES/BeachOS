# Emerald Hospitality Operating System — Project Glossary

## Purpose

This glossary is the authoritative language reference for the Emerald Hospitality Operating System. Product Owners, Designers, Developers, Testers, AI Agents, and venue stakeholders should use these official names whenever they mean the concepts defined here.

The glossary standardizes language; it does not create unapproved workflows, permissions, financial rules, or technical designs. The Domain Model remains the source of truth for business relationships and rules, and the Decision Log remains the source of truth for approved decisions and their reasons.

## Customer Group

- **Official Name:** Customer Group
- **Definition:** The primary operational entity representing one party receiving service together. It owns the party’s current Service Location, Orders, optional Bill, Payments through that Bill, responsible service relationship, and History from official opening through completion.
- **Why it exists:** Hospitality work needs one continuous business identity for the party, even when the party moves, orders several times, changes responsible staff, or has not yet incurred a Financial Obligation.
- **Typical Examples:** Four guests served at Beach Sunbed A12; a family served at Pool Sunbed P07; a party at Upper Table U04.
- **Common Terms That Should NOT Be Used:** Visit; table account; customer account; session; booking; party record.
- **Related Domain Concepts:** Guest Token; Service Location; Responsible Service Staff; Order; Bill; Payment; Activity Log.

## Guest Token

- **Official Name:** Guest Token
- **Definition:** The temporary operational identity used to recognize a Customer Group during service. The current physical implementation is an **NFC Guest Card**. Future implementations may include a wristband, Mobile Device, Hotel Room Card, QR, or another approved technology. Guest Token is the business concept; its technology is replaceable.
- **Why it exists:** A guest group may need a simple temporary way to be recognized across service interactions without requiring personal customer accounts or making one physical device permanent.
- **Typical Examples:** An NFC Guest Card issued for the duration of service; a future resort wristband associated with the active Customer Group; a future approved QR presented by the group.
- **Common Terms That Should NOT Be Used:** NFC card as the permanent business concept; customer ID; guest account; payment card; room key unless specifically referring to the physical technology; Service Location tag.
- **Related Domain Concepts:** Customer Group; NFC Guest Card; Service Location; Service Location Digital Identity; Bill; Payment. The rules for issuing, associating, replacing, and retiring Guest Tokens require Product Owner approval before implementation.

## Service Location

- **Official Name:** Service Location
- **Definition:** One identifiable place where one active Customer Group can receive service, such as a beach sunbed set, pool sunbed set, or upper table.
- **Why it exists:** Different physical service settings need one common business concept for occupancy, service responsibility, transfer, ordering context, and operational visibility.
- **Typical Examples:** Beach Sunbed A12; Pool Sunbed P07; Upper Table U04.
- **Common Terms That Should NOT Be Used:** Table when referring to all location types; seat; spot; station; NFC tag; sunbed number as the general concept.
- **Related Domain Concepts:** Venue; Area; Zone; Customer Group; Service Location Digital Identity; Physical Row.

## Service Location Digital Identity

- **Official Name:** Service Location Digital Identity
- **Definition:** The stable, technology-neutral identity that resolves to one enduring Service Location so its current state can be retrieved from the central system. It contains no changing operational, financial, customer, authorization, or other sensitive business information.
- **Why it exists:** Staff need to reach the correct digital context quickly while physical tags, devices, visible names, and identification technologies may be replaced over time.
- **Typical Examples:** An NFC tag containing a non-sensitive identifier or secure application link; a future QR resolving to the same Service Location; manual lookup by the location’s visible name or number.
- **Common Terms That Should NOT Be Used:** NFC identity; tag record; table code; Customer Group identity; Guest Token; automatic authorization.
- **Related Domain Concepts:** Service Location; NFC; manual location lookup; central source of truth. Identifying a Service Location never authorizes or performs a business action.

## Zone

- **Official Name:** Zone
- **Definition:** A temporary operational grouping of an arbitrary collection of Service Locations within one Venue. A Zone is not a geographical concept and does not change the physical location or identity of anything it groups.
- **Why it exists:** Venue leaders need to organize daily service responsibility and workload without changing the permanent venue layout.
- **Typical Examples:** Maria’s Service Zone; Weekend Zone A; Wedding Guest Zone.
- **Common Terms That Should NOT Be Used:** Area; geographical zone; section; physical row; permanent location group; pricing zone.
- **Related Domain Concepts:** Venue; Area; Service Location; Zone Template; Capability; Responsible Service Staff.

## Zone Template

- **Official Name:** Zone Template
- **Definition:** A future reusable plan for creating the initial operational Zone arrangement before service starts. Applying it creates a starting arrangement that authorized staff may later change manually.
- **Why it exists:** Venues may repeat useful operating patterns while still needing day-to-day control over live Zones.
- **Typical Examples:** Weekday; Weekend; Full Capacity; Private Event; Wedding.
- **Common Terms That Should NOT Be Used:** Floor plan; Area template; permanent Zone; seating map; pricing template.
- **Related Domain Concepts:** Zone; Service Location; Venue; Master Role; Manage Zone Templates Capability.

## Order

- **Official Name:** Order
- **Definition:** One safely submitted and confirmed ordering round for an active Customer Group. An Order contains one or more Order Items and becomes a business fact once submitted.
- **Why it exists:** Each confirmed request must remain distinct, understandable, and traceable while contributing to the Customer Group’s continuing service and Bill.
- **Typical Examples:** A first Order for coffees and water; a later Order for lunch; a final Order for desserts.
- **Common Terms That Should NOT Be Used:** Cart after submission; ticket; Bill; tab; request when referring to a confirmed Order.
- **Related Domain Concepts:** Order Round; Order Item; Customer Group; Bar Ticket; Kitchen Ticket; Bill.

## Order Round

- **Official Name:** Order Round
- **Definition:** The business meaning of one submitted Order within a Customer Group’s service. A new Order Round is created each time staff submit another confirmed collection of Order Items.
- **Why it exists:** A Customer Group often orders several times. Separate Orders preserve what was requested and when, while one Bill aggregates all approved Financial Obligations across those rounds.
- **Typical Examples:** Drinks on arrival; lunch ordered later; an additional round of drinks.
- **Common Terms That Should NOT Be Used:** Order version; Order update; batch; reopened Order; additions to the old Order.
- **Related Domain Concepts:** Order; Customer Group; Order Item; Bill; Financial Obligation.

## Order Item

- **Official Name:** Order Item
- **Definition:** One confirmed item, quantity, price, preparation destination, and any approved instruction within an Order.
- **Why it exists:** Each requested product or service must preserve its own commercial and preparation meaning even if the Menu later changes.
- **Typical Examples:** Two iced coffees with no sugar; one club sandwich without tomato; one bottled water requiring no preparation.
- **Common Terms That Should NOT Be Used:** Menu Item when referring to what was ordered; Bill Line; product row; ticket item as the general business term.
- **Related Domain Concepts:** Order; Menu Item; Bill Line; Bar Ticket; Kitchen Ticket; preparation destination.

## Bill

- **Official Name:** Bill
- **Definition:** The complete running financial obligation for one Customer Group, created only when that group receives its first approved Financial Obligation. A Customer Group may exist without a Bill.
- **Why it exists:** The business needs one clear account of what the Customer Group owes, why it is owed, what has been paid, and whether the financial relationship may close.
- **Typical Examples:** A Bill created by an immediate Beach Sunbed charge; a Bill first created when the group submits its first ordered item; a Bill containing several Order Rounds and later Payment.
- **Common Terms That Should NOT Be Used:** Order; receipt; invoice unless it legally is one; tab as the official term; Customer Group.
- **Related Domain Concepts:** Customer Group; Financial Obligation; Bill Line; Order; Payment; Balance.

## Financial Obligation

- **Official Name:** Financial Obligation
- **Definition:** An approved business reason why a Customer Group owes an exact amount. The first Financial Obligation creates the Bill when no Bill already exists.
- **Why it exists:** Service may begin before money is owed, and money may become owed for reasons other than an Order. The concept separates operational service from the moment a charge legitimately arises.
- **Typical Examples:** Beach Sunbed charge; minimum consumption; first ordered item; future reservation deposit.
- **Common Terms That Should NOT Be Used:** Bill when referring only to one reason for owing money; automatic fee; transaction; debit; charge event as the general term.
- **Related Domain Concepts:** Bill; Bill Line; Customer Group; Order Item; Sunbed Charge; Payment.

## Payment

- **Official Name:** Payment
- **Definition:** An exact amount of value confirmed as received against one Bill through an approved Payment Method.
- **Why it exists:** The business must distinguish money actually received from an attempt, promise, or selected method and must explain how the Bill’s Balance was reduced.
- **Typical Examples:** Cash accepted by an authorized Cashier; a confirmed card Payment; a future approved Payment through another method.
- **Common Terms That Should NOT Be Used:** Payment attempt; card authorization; settlement unless it has the approved business meaning; cash entry; Bill closure.
- **Related Domain Concepts:** Bill; Balance; Payment Method; Cashier; Capability; Activity Log.

## Responsible Service Staff

- **Official Name:** Responsible Service Staff
- **Definition:** The one eligible Staff Member accountable for coordinating service for an active Customer Group at a given time. The person may hold different operational Roles in different Venues. At Emerald Beach Club, the currently approved opening responsibility belongs to the Responsible Waiter; the venue-neutral business concept is Responsible Service Staff.
- **Why it exists:** Accountability belongs to one person at a time, but a long-term multi-venue product must not assume that every Venue names or organizes that responsibility as “Waiter.”
- **Typical Examples:** A Waiter responsible for a beach Customer Group; a server responsible for a pool cabana; another approved service Role performing the same responsibility at a future Venue.
- **Common Terms That Should NOT Be Used:** Responsible Waiter as the universal cross-venue term; owner of the customer; assigned user; table owner; Host or Cashier when those Roles do not hold the responsibility.
- **Related Domain Concepts:** Staff Member; Customer Group; Role; Capability; Host; Manager; Shift. Existing waiter-only opening rules remain in force until any separate approved decision changes them.

## Host

- **Official Name:** Host
- **Definition:** A Staff Member Role focused on welcoming guests, organizing seating, and escorting parties to Service Locations. Under current approved rules, a Host does not officially open a Customer Group.
- **Why it exists:** Arrival and seating coordination are distinct responsibilities from formally starting and owning service.
- **Typical Examples:** Greeting a party; finding an available Service Location; escorting guests to their sunbeds.
- **Common Terms That Should NOT Be Used:** Responsible Service Staff; Customer Group opener; receptionist when the business means Host; Cashier.
- **Related Domain Concepts:** Customer Group; Service Location; Responsible Service Staff; Role; Capability.

## Cashier

- **Official Name:** Cashier
- **Definition:** A Staff Member Role focused on financial visibility and approved payment and bill-closing work. A Cashier’s Role does not itself authorize an action; the required Capability is also necessary.
- **Why it exists:** Venues need clear financial responsibility and a reliable view of open Bills and Payments without confusing that responsibility with live service ownership.
- **Typical Examples:** Reviewing an open Bill; recording a confirmed Payment when authorized; closing a fully settled Bill when authorized.
- **Common Terms That Should NOT Be Used:** Responsible Service Staff; accountant; payment terminal; Bill owner; Customer Group opener.
- **Related Domain Concepts:** Bill; Payment; Payment Method; Capability; Activity Log; Customer Group.

## Manager

- **Official Name:** Manager
- **Definition:** A Staff Member Role with oversight responsibilities for venue operations, exceptions, people, and approved controls. The Role describes responsibility but grants no action automatically.
- **Why it exists:** Live operations require accountable oversight and escalation without giving every person unrestricted authority.
- **Typical Examples:** Reviewing an exception; overseeing a handover; investigating a transfer; acting through an explicitly granted Capability.
- **Common Terms That Should NOT Be Used:** Administrator; superuser; all-access user; Master User when the approved business responsibility is Manager; automatic approver.
- **Related Domain Concepts:** Staff Member; Role; Capability; Activity Log; Audit Trail; Venue.

## Capability

- **Official Name:** Capability
- **Definition:** Explicit business authority for a Staff Member to perform one defined action in an approved context. Roles describe responsibilities; Capabilities authorize actions.
- **Why it exists:** People with similar Roles may need different authority, and a Role title alone must never silently grant sensitive access.
- **Typical Examples:** Open Customer Group; Transfer Customer Group; Assign Waiter; Close Bill; Manage Zones; Record Payments.
- **Common Terms That Should NOT Be Used:** Role permission; access level; privilege; rights as a vague collective term; job title authorization.
- **Related Domain Concepts:** Staff Member; Role; Customer Group; Manager; Activity Log. A Capability never bypasses a business rule.

## Activity Log

- **Official Name:** Activity Log
- **Definition:** A trustworthy business record of one sensitive, exceptional, or accountability-relevant event, including who acted, what happened, when it happened, and the business context needed to understand it.
- **Why it exists:** Important actions must remain explainable so the business can resolve mistakes and disputes, protect staff, and improve operations without silently rewriting history.
- **Typical Examples:** One Responsible Service Staff handover; one Customer Group transfer; one Payment reversal; one Capability change.
- **Common Terms That Should NOT Be Used:** Technical log; system log; surveillance record; Activity Record; audit log when referring to one official Activity Log entry.
- **Related Domain Concepts:** Audit Trail; Domain Event; Staff Member; Customer Group; Payment; Capability.

## Audit Trail

- **Official Name:** Audit Trail
- **Definition:** The connected, chronological account of relevant business facts used to understand the history of a subject or process. It may bring together multiple Activity Logs and the preserved history of Orders, Bills, Payments, transfers, and other business events.
- **Why it exists:** One Activity Log explains one accountable event; an Audit Trail explains the wider sequence of what happened over time.
- **Typical Examples:** The full sequence of a Customer Group transfer and later handover; the history of a Bill from creation through correction, Payment, and closure; the sequence of Capability grants and revocations for a Staff Member.
- **Common Terms That Should NOT Be Used:** Activity Log when referring to the complete connected history; technical trace; surveillance history; change list.
- **Related Domain Concepts:** Activity Log; History; Domain Event; Customer Group; Bill; Payment; Staff Member.

## Product Philosophy

- **Official Name:** Product Philosophy
- **Definition:** The enduring principles used to judge whether a product choice supports hospitality operations, simplicity, trust, consistency, and long-term quality.
- **Why it exists:** Requirements and technology change, but teams need a stable way to evaluate trade-offs and avoid decisions that conflict with the product’s character.
- **Typical Examples:** Operations First; Simplicity Wins; Human Mistakes Are Normal; Quality Over Quantity.
- **Common Terms That Should NOT Be Used:** Requirements; roadmap; architecture; marketing vision; feature policy.
- **Related Domain Concepts:** Decision Log; Domain Model; Product Vision; Product Requirements; Master Blueprint.

## Decision Log

- **Official Name:** Decision Log
- **Definition:** The permanent historical record of important product, business, design, architecture, security, and technical decisions, including what was decided and why.
- **Why it exists:** Future teams must understand the reasoning and consequences behind a decision rather than seeing only its final outcome.
- **Typical Examples:** The decision that Customer Group is primary; the decision that Zones are dynamic; the decision that Capabilities authorize actions.
- **Common Terms That Should NOT Be Used:** Changelog; meeting notes; issue list; requirements; current-state summary.
- **Related Domain Concepts:** Product Philosophy; Domain Model; Product Owner approval; Decision ID.

## Domain Model

- **Official Name:** Domain Model
- **Definition:** The single source of truth for the business concepts, lifecycles, rules, relationships, and meaningful events that make up the Emerald hospitality domain.
- **Why it exists:** Owners, staff, Designers, Developers, Testers, and AI Agents need one shared understanding of the business before they design or evaluate product behaviour.
- **Typical Examples:** The agreed meanings of Customer Group, Service Location, Order, Bill, Payment, Zone, and Capability.
- **Common Terms That Should NOT Be Used:** Data model; database model; schema; architecture; entity list when referring to the complete business model.
- **Related Domain Concepts:** Project Glossary; Decision Log; Domain Event; Business Rule; Product Philosophy.

## Hospitality Operating System

- **Official Name:** Hospitality Operating System
- **Definition:** A product that coordinates the connected day-to-day work of hospitality across locations, staff responsibility, service, Orders, preparation, Bills, Payments, and operational history.
- **Why it exists:** Emerald is intentionally broader than a Point of Sale. A Point of Sale describes the financial moment of sale, while the Hospitality Operating System supports the complete operational journey before, during, and after that moment.
- **Typical Examples:** Coordinating a Customer Group from opening through several Order Rounds, preparation, transfer, Payment, and completion; supporting staff responsibility and live venue organization across Service Locations.
- **Common Terms That Should NOT Be Used:** Point of Sale or POS as the name for the whole product; cash register; ordering app; restaurant till; payment system.
- **Related Domain Concepts:** Customer Group; Service Location; Responsible Service Staff; Order; Bill; Payment; Activity Log; Product Philosophy.

## Vocabulary Rules

1. **One concept = one official name.** Do not create a second name for an existing concept.
2. **Avoid synonyms in documentation.** Use ordinary descriptive language only when it cannot be mistaken for another business concept.
3. **Use official terminology everywhere.** Documentation, user interfaces, APIs, tests, training material, support material, and project conversations should use the official vocabulary.
4. **Preserve capitalization for defined concepts.** Capitalization signals that a word refers to the agreed business meaning.
5. **Do not turn technology into business vocabulary.** NFC, QR, cards, devices, frameworks, and storage choices may implement a concept but do not replace its official business name.
6. **Do not invent business meaning to solve a technical problem.** Business terminology always takes precedence over technical terminology.
7. **Check the Domain Model for rules.** A glossary definition gives consistent language; it does not replace lifecycle, relationship, or business-rule definitions.
8. **Check the Decision Log for authority and reasoning.** A glossary term must not silently change an accepted decision.
9. **Product Owner approval is required for change.** Adding, renaming, merging, splitting, or materially redefining an official term requires Product Owner approval and any necessary Decision Log entry.
10. **Resolve conflicts deliberately.** When existing material uses a conflicting term, do not silently rewrite history. Record the conflict, obtain approval, and align current references through a controlled documentation update.
11. **Prefer business language.** When a technical and business term compete, use the business term in product discussion and explain the technical term only where genuinely necessary.
12. **Review new features against the glossary.** A proposed feature must use existing official concepts or obtain approval for any genuinely new business concept before implementation.
