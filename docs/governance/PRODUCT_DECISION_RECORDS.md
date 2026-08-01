# BeachOS Product Decision Record System

## Purpose

This document defines how BeachOS permanently records important Product Owner
decisions.

A Product Decision Record, or PDR, preserves:

- the product problem being decided;
- the approved business meaning or behavior;
- the alternatives considered;
- the reasoning and evidence;
- the expected consequences;
- the authority that approved it;
- its relationship to Capabilities, Domain concepts, architecture, and earlier
  decisions;
- its complete lifecycle when it is later deprecated or replaced.

This is Product Governance. It is not a technical Architecture Decision Record,
source code, a requirement by itself, or permission to implement an unresolved
Capability.

The system exists so a future Product Owner, operator, designer, developer,
tester, or AI agent can understand not only what BeachOS does, but why the
business chose that meaning.

## Relationship with the Existing Decision Log

`docs/DECISIONS.md` remains permanent historical authority for the decisions it
already contains. This PDR system does not renumber, rewrite, delete, or silently
replace those entries.

When the PDR system is adopted for active governance:

- existing `DEC-xxx` entries remain valid according to their recorded status;
- new product decisions should use the PDR structure defined here;
- architecture and technical decisions should use the ADR process;
- a new PDR that changes an existing `DEC-xxx` decision must cite it explicitly
  in `Supersedes`;
- migration of old decisions into new PDR files is optional and must never
  create two conflicting active authorities;
- a cross-reference may improve discoverability, but it must not alter
  historical wording.

# 1. Product Decisions and Architecture Decisions

## Product Decision

A Product Decision defines what BeachOS means, which operational outcome is
approved, which business rule applies, or which experience principle governs
the product.

Examples:

- Who intentionally opens a Customer Group?
- What does `READY` mean?
- Does a Bill open with the Customer Group or with the first Financial
  Obligation?
- Which official term names a business concept?
- Which human decision remains outside automation?
- Is a Capability approved for product design or implementation?
- Which behavior is no longer supported?

A Product Decision may create constraints that architecture must respect, but it
does not select a technical mechanism merely because one mechanism seems likely.

## Architecture Decision

An Architecture Decision defines how the software will satisfy approved product
meaning and quality constraints.

Examples:

- persistence strategy;
- transaction boundary;
- repository pattern;
- event publication mechanism;
- runtime topology;
- framework boundary;
- deployment or integration approach.

An ADR may recommend or select a technical option. It must not invent a business
rule, operational definition, Capability, or user authority.

## Why the distinction matters

| Product Decision Record                               | Architecture Decision Record                                        |
| ----------------------------------------------------- | ------------------------------------------------------------------- |
| Owns product and business meaning                     | Owns technical structure and trade-offs                             |
| Approved by the Product Owner                         | Approved through the engineering architecture authority             |
| Uses operational and business evidence                | Uses technical evidence and constraints                             |
| May be understood by a non-developer                  | May require technical expertise                                     |
| Constrains Domain, UX, requirements, and architecture | Must conform to approved Product Decisions                          |
| Cannot be approved by implementation alone            | Cannot change product meaning through technical convenience         |
| Remains valid across technology replacement           | May be superseded when technology or engineering constraints change |

## Boundary rule

When one proposal contains both product and technical decisions, record them
separately:

1. approve the Product Decision;
2. reference it from the ADR;
3. let the ADR choose how to satisfy it;
4. return to Product Governance if no responsible technical option can satisfy
   the approved meaning.

An ADR must never be used as evidence that the Product Owner approved a business
outcome. A PDR must never select hidden technical commitments without
architecture review.

# 2. Decisions Requiring Permanent Recording

A decision requires a PDR when changing it later would alter business meaning,
staff behavior, guest experience, financial truth, responsibility, product
scope, official language, or the interpretation of historical facts.

## New business rule

Record any rule that permits, requires, prevents, or causes an operational or
financial outcome.

Examples:

- one active Customer Group per Service Location;
- Bill creation at the first Financial Obligation;
- an authorization requirement for a sensitive action;
- a condition that blocks Venue Opening.

## New operational definition

Record the approved meaning of an operational condition, state, distinction, or
outcome.

Examples:

- `READY`, `NOT READY`, and `BLOCKED`;
- acknowledgement versus preparation start;
- ready versus completed;
- current Service Location versus submission location.

## New terminology

Record a new official business term, a material definition change, or the
replacement of an older term.

One business concept must retain one official name. A terminology PDR must state
whether historical documents keep their original language and which future
documents must use the new term.

## Capability approval

Record approval to:

- begin Product Capability design;
- accept the Capability’s business scope;
- permit implementation;
- expand a Capability with a new consequential outcome;
- withdraw or replace a Capability.

Capability approval must state what remains outside scope.

## Operational standard

Record an approved repeatable standard that the business expects people to
follow.

Examples:

- Venue Opening responsibilities;
- handover expectations;
- required operational review;
- approved completion conditions.

A common habit, historical pattern, recommendation, or current implementation
does not become a standard without approval.

## Hospitality principle

Record a new enduring principle or a material interpretation of an existing
principle when it will guide several Capabilities.

Examples:

- Hospitality First;
- coaching before judging;
- current facts over historical expectation;
- humans decide while the system advises.

## UX principle

Record an experience rule that materially affects user decisions or safety
across workflows.

Examples:

- uncertain consequential outcomes must never look successful;
- every critical workflow requires a visible fallback;
- physical context may identify digital context but cannot authorize action.

Routine layout choices do not require a PDR unless they change meaning,
authority, safety, or an approved cross-product principle.

## Business constraint

Record a non-negotiable limitation arising from operations, policy, contract,
market, privacy, legal review, safety, or product positioning.

The record must distinguish a permanent constraint from a temporary delivery
limit.

## Deprecated behavior

Record when approved behavior:

- must no longer be used for new operations;
- remains available only for historical understanding;
- is temporarily tolerated during an approved transition;
- is replaced by another behavior;
- is rejected as unsafe, misleading, or no longer aligned with the product.

Deprecation must state what happens to existing history and dependent
Capabilities.

## Other decisions requiring a PDR

Also record:

- Product authority boundaries;
- human-versus-system decision boundaries;
- financial correction, cancellation, reversal, refund, or closing rules;
- privacy and Operational Learning purposes;
- retention and intentional-forgetting policies;
- cross-Venue product behavior;
- metrics that will influence operational decisions;
- new sources of operational truth;
- material exceptions to an existing Product Decision;
- a decision not to support a requested behavior when that exclusion materially
  protects product scope or safety.

## Decisions that normally do not require a PDR

The following normally use another process:

- implementation details governed by an ADR;
- routine defect corrections that restore already-approved behavior;
- copyediting that does not change meaning;
- reversible visual polish that changes no behavior or principle;
- Sprint sequencing inside approved scope;
- test data;
- temporary development tooling;
- code organization that changes no architectural boundary;
- operational observations that have not been approved as rules or standards.

When uncertain, ask whether a reasonable future contributor could implement a
different business outcome without this decision. If yes, create a PDR.

# 3. Required Structure of a Product Decision Record

Every PDR must use the following structure. Optional fields may be marked `Not
applicable`; required fields must not be omitted.

## Identity

### Decision ID

Required. Use the next governed identifier in the form `PDR-XXX`.

The identifier is permanent and must never be reused, even if the record is
Rejected or created in error.

Examples and templates use `PDR-EX-XXX` so they cannot be mistaken for active
project authority.

### Title

Required. A short, specific statement of the decision subject.

Prefer:

> Responsible Service Staff intentionally opens the Customer Group

Avoid:

> Customer Group update

### Status

Required. One lifecycle status:

- Proposed;
- Approved;
- Deprecated;
- Replaced;
- Rejected.

### Date

Required. The date of the latest lifecycle decision, using `YYYY-MM-DD`.

The original proposal and approval dates should remain in Decision History.

### Author

Required. The person or accountable group that prepared the record.

Authorship does not imply approval.

### Approved by

Required for Approved, Deprecated, and Replaced records. Name the Product Owner
or formally delegated product authority.

Use `Not approved` for Proposed and Rejected records unless a Product Owner
approved the rejection.

## Classification and scope

### Decision Type

Required. Examples:

- Business Rule;
- Operational Definition;
- Terminology;
- Capability Approval;
- Operational Standard;
- Hospitality Principle;
- UX Principle;
- Business Constraint;
- Deprecated Behavior.

Use more than one only when separating the decisions would make the record
misleading. Technical choices must remain in ADRs.

### Scope

Required. Identify:

- product or industry pack;
- Organization or Venue scope if limited;
- operational context;
- whether the decision is universal, configurable, or venue-specific.

Silence must not be interpreted as universal scope.

## Decision content

### Problem

Required. Explain:

- the operational or product question;
- why a decision is necessary;
- what is uncertain or conflicting;
- who or what is affected;
- why leaving it unresolved is risky.

Do not describe the preferred answer as if it were already decided.

### Decision

Required. State the approved meaning in direct, unambiguous business language.

The statement must be understandable independently of implementation.

For Proposed records, label the statement as the proposed decision.

### Alternatives Considered

Required. List realistic alternatives, including:

- retain current behavior;
- do nothing or leave unresolved, where relevant;
- materially different business meanings;
- narrower or broader scope.

Do not include obviously unacceptable alternatives merely to make the selected
option appear stronger.

### Reasoning

Required. Explain why the option was selected, including:

- operational evidence;
- product principles;
- guest and staff impact;
- owner confidence;
- trade-offs;
- uncertainty;
- why alternatives were not selected.

Repeated behavior, an existing screen, or existing source code is not sufficient
reasoning by itself.

### Consequences

Required. State:

- expected benefits;
- costs and limitations;
- risks;
- workflow changes;
- documentation affected;
- Capability impact;
- historical-data treatment;
- required follow-up decisions;
- what remains unresolved.

Consequences do not authorize unrelated scope.

## Relationships

### Related Capabilities

Required. List every Capability that:

- depends on this decision;
- creates the approved outcome;
- consumes the outcome;
- must be reviewed if the decision changes.

Use `None currently` when appropriate.

### Related Architecture

Required. Reference architecture documents and ADRs constrained by the Product
Decision.

Architecture relationships do not make technical recommendations part of the
PDR.

### Related Domain Concepts

Required. Use official Domain Model and Project Glossary terms.

If a concept is new, terminology and Domain updates remain required after
approval.

### Related Product Decisions

Required. List active or historical decisions that:

- support the decision;
- constrain it;
- may appear to conflict;
- must be interpreted together.

Use exact IDs.

### Supersedes

Required. List every Product Decision fully or partly replaced.

Use `None` when the decision is new.

Partial replacement must identify exactly which meaning is replaced.

### Superseded By

Required. Initially `None`.

When the record is replaced, update only its status, this field, and Decision
History. Preserve the original Problem, Decision, Alternatives, Reasoning, and
Consequences unchanged.

## Validation and governance

### Evidence and Validation

Required. State:

- evidence considered;
- owner, operator, guest, legal, privacy, financial, or technical review
  completed;
- how the decision’s intended outcome will be reviewed;
- which evidence remains missing.

Evidence informs Product Owner judgment; it does not approve the decision.

### Open Questions

Required. List unresolved matters explicitly.

An Approved PDR may contain open questions when they do not change the approved
meaning. If an open question would materially change the decision, the record
must remain Proposed or have narrower scope.

### Review Trigger

Required. Name a date or event that should cause review.

Examples:

- before the second Venue;
- after the pilot;
- before implementing Ready and Completed commands;
- when a legal requirement changes;
- no planned review unless evidence invalidates an assumption.

Review does not automatically change status.

### Decision History

Required. Append-only list containing:

- date;
- lifecycle action;
- actor or approving authority;
- short explanation;
- related replacement ID where applicable.

Do not rewrite earlier history.

# Product Decision Record Template

```markdown
# PDR-XXX — Title

- **Decision ID:** PDR-XXX
- **Title:** Title
- **Status:** Proposed / Approved / Deprecated / Replaced / Rejected
- **Date:** YYYY-MM-DD
- **Author:** Name or accountable group
- **Approved by:** Product Owner / delegated authority / Not approved
- **Decision Type:** Type
- **Scope:** Product, Venue, operational context, universality

## Problem

What product or operational question requires a permanent decision?

## Decision

What is proposed or approved?

## Alternatives Considered

- Alternative
- Alternative
- Do nothing or retain current behavior, where relevant

## Reasoning

Why was this option selected?

## Consequences

- Benefit
- Cost or risk
- Limitation
- Follow-up
- Remaining uncertainty

## Related Capabilities

- Capability

## Related Architecture

- Architecture document or ADR

## Related Domain Concepts

- Official Domain concept

## Related Product Decisions

- PDR-XXX or historical DEC-XXX

## Supersedes

None

## Superseded By

None

## Evidence and Validation

- Evidence considered
- Reviews completed
- Intended validation
- Missing evidence

## Open Questions

- Question or `None within the approved scope`

## Review Trigger

Date or event

## Decision History

- YYYY-MM-DD — Proposed by Author.
- YYYY-MM-DD — Approved by Product Owner.
```

# 4. Decision Lifecycle

## Proposed

### Meaning

The record describes a decision under review. It is not product authority and
must not be implemented as if approved.

### Allowed actions

- gather evidence;
- revise the proposal;
- consult operators and specialists;
- identify consequences;
- link affected Capabilities and Domain concepts;
- request Product Owner decision.

### Rules

- Every proposal must have one accountable Author.
- A proposal must identify the decision needed, not merely describe a problem.
- Competing proposals may coexist if each relationship is clear.
- Implementation may explore technical feasibility without committing business
  behavior.

## Approved

### Meaning

The Product Owner or delegated product authority has accepted the Decision for
the recorded scope.

### Effect

- Affected Product, Domain, UX, Capability, testing, and architecture work must
  align.
- The decision may authorize design or implementation only to the extent stated.
- Contradictory Proposed records do not override it.
- Existing implementation that conflicts with it must be treated as a gap, not
  as competing authority.

### Rules

- Approval date and approver are mandatory.
- Related documents should be aligned through separately scoped work.
- Approval must not be inferred from silence, implementation, or meeting
  attendance.

## Deprecated

### Meaning

The decision remains historical authority for earlier behavior, but the Product
Owner has decided it should not guide new use or expansion.

Deprecation may precede a replacement when transition or further decision is
required.

### Rules

- State why it is deprecated.
- State whether existing behavior remains temporarily valid.
- State what new work is forbidden.
- Preserve the original record and history.
- Reference a replacement if one exists.
- Do not use Deprecated when the decision was never Approved; use Rejected.

## Replaced

### Meaning

A new Approved PDR now governs all or a stated part of the old decision.

### Rules

- The new PDR must name the old PDR in `Supersedes`.
- The old PDR must name the new PDR in `Superseded By`.
- The old original content remains unchanged.
- Partial replacement must define which part remains active.
- Historical actions remain interpreted under the decision and standard that
  applied at their time.

## Rejected

### Meaning

The proposed decision was reviewed and not approved.

### Rules

- Preserve the proposal and rejection reasoning.
- State who rejected it and when.
- Rejection does not approve an alternative unless that alternative has its own
  Approved PDR.
- A materially changed future proposal receives a new Decision ID and references
  the rejected one.
- Do not delete rejected decisions; they prevent repeated unresolved debate and
  preserve context.

## Valid lifecycle transitions

```text
Proposed → Approved
Proposed → Rejected
Approved → Deprecated
Approved → Replaced
Deprecated → Replaced
```

Any correction of an administrative error must be visible in Decision History.
A material change always requires a new PDR.

# 5. Product Decision Rules

## No silent modification

No Product Decision may silently modify another Product Decision.

If two Approved PDRs appear inconsistent:

1. stop dependent implementation where the inconsistency affects outcome;
2. identify both decisions;
3. ask the Product Owner to clarify scope or approve a replacement;
4. record the resolution in a new PDR when business meaning changes;
5. preserve both historical records.

Document recency alone does not create authority.

## Replacement must be explicit

Every replacement must:

- receive a new Decision ID;
- be Approved before replacing active meaning;
- reference every decision it supersedes;
- explain why replacement is necessary;
- state consequences for current behavior and historical interpretation;
- update the replaced record’s status and relationship fields without rewriting
  its original content.

## Capability dependency

Every Capability must reference the Product Decisions it depends on.

At minimum, a Capability record should identify:

- decisions that define its purpose and scope;
- business rules it enforces;
- terminology it uses;
- human authority and Capability boundaries;
- operational standards it supports;
- UX principles affecting consequential actions;
- decisions that command-gate unresolved behavior;
- deprecated or replaced decisions relevant to historical behavior.

A Capability is not ready for implementation when a required Product Decision
is missing, Proposed, contradictory, or materially unclear.

## Product Decision before implementation

Record material Product Decisions before implementation whenever possible.

Urgent operational circumstances may require a temporary human response.
Temporary response does not become approved product behavior until recorded and
approved.

## One decision per coherent meaning

Prefer one PDR for one coherent decision.

Split a record when:

- alternatives could be approved independently;
- different authorities are required;
- one part may be replaced without changing the rest;
- product and architecture decisions are mixed;
- scope differs by Venue or industry pack.

Do not split so finely that the business outcome becomes impossible to
understand.

## Historical integrity

- Never delete a PDR.
- Never reuse an ID.
- Never rewrite original reasoning after approval.
- Correct minor factual or formatting errors through Decision History.
- Replace material meaning through a new PDR.
- Keep rejected and replaced records searchable.
- Interpret historical actions under the rule applicable at that time.

## Terminology integrity

- Use official Project Glossary terms.
- A terminology change requires a PDR when it changes official business
  language.
- Historical Decision wording remains unchanged.
- The replacement decision defines language for future documents and UI.

## Scope integrity

- Every PDR must state whether it is universal, configurable, Venue-specific, or
  industry-pack-specific.
- A first-client decision does not silently become universal.
- A Platform abstraction does not make one Capability’s rule apply to another.
- A common habit does not become an approved standard.

## Traceability

Approved PDRs should be traceable to:

- requirements;
- Capabilities;
- Domain concepts and events;
- UX specifications;
- architecture and ADRs;
- tests and acceptance criteria;
- Operational Framework standards;
- implementation reports.

Traceability supports review. It does not permit those artifacts to alter the
PDR.

# 6. Governance

## Who may propose?

Any accountable contributor may propose a PDR, including:

- Product Owner;
- business owner;
- Venue operator or department lead;
- designer;
- developer or architect;
- tester or security specialist;
- customer support or implementation specialist;
- legal, privacy, financial, or compliance advisor;
- AI agent acting under human direction.

The proposer must:

- name the problem;
- use confirmed evidence where available;
- distinguish recommendation from approval;
- identify affected people and Capabilities;
- disclose uncertainty and conflicts;
- avoid presenting implementation as product authority.

An AI agent may draft or identify the need for a PDR. It may not approve,
deprecate, replace, or reject one.

## Who approves?

The Product Owner is the default approving authority for Product Decisions.

The Product Owner may delegate a defined category or scope to a named product
authority. Delegation must be explicit, recorded, limited, and revocable.

Additional approval or consultation may be mandatory when a decision affects:

- legal or regulatory obligations;
- privacy and retention;
- security;
- financial or fiscal behavior;
- staff safety;
- employment policy;
- contractual commitments;
- cross-Organization product standards.

Specialist approval does not replace Product Owner approval of product meaning.
The Product Owner must not approve a decision that requires specialist authority
without obtaining it.

## Who may deprecate or replace?

Only the Product Owner or the formally delegated authority for that exact scope
may deprecate or replace an Approved PDR.

The original Author, engineering team, operational team, or AI agent may propose
deprecation but cannot make it effective.

Deprecation or replacement must include:

- operational reason;
- affected Capabilities;
- transition impact;
- historical treatment;
- communication responsibility;
- Product Owner approval;
- any required specialist approval.

## Who may reject?

The Product Owner may reject a Product proposal.

A delegated authority may reject only within its recorded scope. A specialist
may block approval where their mandatory authority applies, but the PDR should
record whether it was Rejected or remains Proposed pending resolution.

## Governance roles

### Product Owner

- owns product meaning;
- approves, rejects, deprecates, and replaces PDRs;
- resolves scope and priority;
- ensures operational evidence is considered;
- protects the Mission, Product Philosophy, and Domain authority.

### Product Governance Steward

A named Product Governance Steward should:

- assign IDs;
- check required fields;
- verify references and lifecycle consistency;
- maintain the index;
- ensure replaced records are linked both ways;
- prevent administrative edits from changing meaning;
- identify decisions due for review.

The Steward does not approve product meaning unless also holding delegated
product authority.

### Domain Owner or Business Architect

- checks Domain terminology and boundaries;
- identifies affected concepts and invariants;
- explains contradictions;
- does not approve product meaning unless delegated.

### Capability Owner

- identifies dependencies;
- keeps Capability documentation aligned after approval;
- prevents implementation while required decisions remain unresolved;
- reports evidence and consequences.

### Architecture Authority

- evaluates technical feasibility and architectural consequences;
- creates or updates related ADRs after product approval;
- may raise safety, reliability, or feasibility objections;
- cannot redefine the Product Decision through architecture.

### Operational Representatives

- provide real workflow evidence;
- explain guest and staff impact;
- validate practicality;
- identify exceptional contexts;
- do not make universal product decisions unless delegated.

### Specialist Authorities

Legal, privacy, security, financial, safety, and other specialists approve or
block matters within their mandate.

## How disagreements are resolved

### Step 1 — State the disagreement

Write the exact competing meanings, affected scope, evidence, and consequences.
Do not reduce disagreement to personal preference.

### Step 2 — Identify decision authority

Determine whether the disagreement is:

- product meaning;
- Domain interpretation;
- UX consequence;
- architecture;
- legal, privacy, financial, safety, or security constraint;
- delivery sequencing.

Separate mixed questions.

### Step 3 — Gather relevant evidence

Use:

- confirmed operational facts;
- operator and guest evidence;
- approved Mission and principles;
- current Domain and Product Decisions;
- technical feasibility evidence;
- specialist constraints;
- explicit uncertainty.

Popularity, seniority outside the decision authority, existing code, and
historical habit do not decide product meaning.

### Step 4 — Seek the narrowest coherent decision

Prefer a decision with clear scope that resolves the necessary outcome without
inventing unrelated rules.

### Step 5 — Product Owner decision

The Product Owner approves, rejects, narrows, or postpones the proposal after
mandatory specialist constraints are satisfied.

When evidence remains insufficient, keep the record Proposed and state what must
be learned. Do not force artificial certainty.

### Step 6 — Preserve dissent and uncertainty

Record material objections, risks, and missing evidence in Reasoning,
Consequences, or Decision History.

Approval does not require pretending that every contributor agreed.

### Step 7 — Escalation

If the Product Owner and mandatory specialist authority cannot reach a safe
decision:

- implementation remains blocked for the affected outcome;
- escalate through the Organization’s named governance authority;
- preserve the conflict and attempted resolution;
- do not bypass it through architecture, UI, configuration, or manual data
  changes.

## Governance cadence

PDR review should occur:

- before Capability design when foundational meaning is missing;
- before implementation when behavior or authority is unresolved;
- when pilot evidence challenges an assumption;
- when an Operational Learning recommendation may become a standard;
- when terminology changes;
- before deprecating behavior;
- when architecture cannot responsibly satisfy approved meaning;
- at explicit Review Triggers.

Review should be proportional. Governance must protect clarity without turning
routine delivery into ceremony.

# Example Product Decision Records

The following are **format examples only**. Their IDs use `PDR-EX-xxx`, are not
part of the active PDR sequence, and do not replace existing approved
`DEC-xxx` decisions or authoritative documents.

# PDR-EX-001 — Operational Intelligence is an approved product framework

- **Decision ID:** PDR-EX-001
- **Title:** Operational Intelligence is an approved product framework
- **Status:** Approved
- **Date:** 2026-07-27
- **Author:** Product Governance example
- **Approved by:** Product Owner — illustrative
- **Decision Type:** Hospitality Principle, Operational Definition
- **Scope:** BeachOS product-wide; universal unless a later approved
  industry-specific decision narrows its application

## Problem

BeachOS needs one governed way to turn current business facts into readiness,
confidence, attention, advice, human decision, and outcome. Without it,
Capabilities may present inconsistent certainty, attention, or operational
language.

## Decision

Operational Intelligence is approved as the product-wide framework governing how
BeachOS reasons about current hospitality operations.

BeachOS begins with the human decision, uses confirmed facts, keeps readiness
separate from confidence, uses attention sparingly, makes advice explainable,
preserves uncertainty, and leaves consequential decisions with authorized
people.

Operational Intelligence does not own Domain truth or authorize actions.

## Alternatives Considered

- Let each Capability define its own reasoning style.
- Present raw facts without operational interpretation.
- Allow the product to make operational decisions automatically.
- Approve one product-wide Operational Intelligence Framework.

## Reasoning

One framework creates consistent confidence and conversation while protecting
Domain authority and human judgment. Raw data alone does not reduce uncertainty,
and automatic decision-making would conflict with the product principle that
the system advises and humans decide.

## Consequences

- Every Capability must identify its primary human decision.
- Recommendations must cite confirmed facts and uncertainty.
- Operational Intelligence may interpret but must not mutate Domain state.
- UX must distinguish facts, blockers, advice, and unknown outcomes.
- Capability-specific readiness and attention rules still require approval.

## Related Capabilities

- Venue Opening
- Host Workspace
- Guest Arrival
- Ordering
- Kitchen Operations
- All future operational Capabilities

## Related Architecture

- `docs/architecture/PLATFORM_STRATEGY.md`
- `docs/engineering/ARCHITECTURE.md`

## Related Domain Concepts

- Operational Readiness
- Attention
- Capability
- Domain Event
- Staff Member
- Venue

## Related Product Decisions

- Historical `DEC-007` — central system is the source of truth
- Historical `DEC-016` — human approval before major implementation phases
- Historical `DEC-038` — Capability-based authorization

## Supersedes

None

## Superseded By

None

## Evidence and Validation

- Based on Mission, Product Philosophy, Operational Framework, Host review, and
  approved operational workflows.
- Validate through every Capability review and real operator feedback.
- Capability-specific evidence remains necessary.

## Open Questions

- Which future capability-specific recommendations require separate Product
  Decisions?
- Which operational standards may provide approved advice?

## Review Trigger

Before approving any capability that performs or recommends a consequential
action automatically.

## Decision History

- 2026-07-27 — Example record written to demonstrate the PDR format.
- 2026-07-27 — Shown as Approved for illustration only; no active authority
  created.

# PDR-EX-002 — Operational Learning is an approved product framework

- **Decision ID:** PDR-EX-002
- **Title:** Operational Learning is an approved product framework
- **Status:** Approved
- **Date:** 2026-07-27
- **Author:** Product Governance example
- **Approved by:** Product Owner — illustrative
- **Decision Type:** Hospitality Principle, Operational Definition
- **Scope:** BeachOS product-wide; recommendations remain subject to approved
  retention, privacy, comparison, and capability rules

## Problem

BeachOS needs to help hospitality businesses improve over time without
introducing hidden scoring, prediction, surveillance, or automatic policy
changes.

## Decision

Operational Learning is approved as the product-wide framework for using
confirmed historical facts to support explainable human learning and operational
improvement.

Historical knowledge may inform current decisions but must never override
current confirmed facts. Repetition does not create a business rule. Human
approval creates operational standards.

## Alternatives Considered

- Retain history only for lookup with no learning use.
- Let each Capability define historical pattern logic independently.
- Use opaque scores or predictions.
- Approve one explainable, fact-based Operational Learning Framework.

## Reasoning

The business benefits from preserving and applying operational experience, but
trust requires clear evidence, privacy restraint, current-fact priority, and
human review. A shared framework prevents patterns from becoming hidden
judgments.

## Consequences

- Source facts, interpretations, recommendations, decisions, and outcomes remain
  distinct.
- Every recommendation must explain scope, evidence, comparability, uncertainty,
  and human authority.
- Intentional forgetting must not rewrite permanent Domain or financial history.
- No capability may use historical recommendations until its retention,
  privacy, and comparison rules are approved.
- No scoring, ranking, or prediction is authorized.

## Related Capabilities

- Venue Opening
- Guest Arrival
- Ordering
- Kitchen Operations
- Future Billing
- Future Payments
- Future Reporting

## Related Architecture

- `docs/architecture/PLATFORM_STRATEGY.md`
- Future Reporting and Audit Platform decisions

## Related Domain Concepts

- Domain Event
- Activity Log
- Opening Report
- Business Date
- Venue
- Staff Member

## Related Product Decisions

- PDR-EX-001 — example Operational Intelligence approval
- Historical `DEC-009` — never silently lose or rewrite financial data
- Historical `DEC-010` — audit every sensitive action

## Supersedes

None

## Superseded By

None

## Evidence and Validation

- Based on confirmed-history requirements, coaching principles, operational KPI
  cautions, and Operational Intelligence.
- Requires later validation with Venue operators before capability-specific
  recommendations.
- Retention, privacy, and recurrence definitions remain unapproved.

## Open Questions

- What information may be retained for each learning purpose?
- What makes situations comparable in each Capability?
- Who may accept a recommendation as an operational standard?

## Review Trigger

Before the first Capability presents a historical pattern or operational habit
recommendation.

## Decision History

- 2026-07-27 — Example record written to demonstrate the PDR format.
- 2026-07-27 — Shown as Approved for illustration only; no active authority
  created.

# PDR-EX-003 — Responsible Waiter intentionally opens the Customer Group

- **Decision ID:** PDR-EX-003
- **Title:** Responsible Waiter intentionally opens the Customer Group
- **Status:** Approved
- **Date:** 2026-07-27
- **Author:** Product Governance example
- **Approved by:** Product Owner — illustrative
- **Decision Type:** Business Rule, Operational Standard
- **Scope:** Current BeachOS Customer Group opening workflow; venue-specific
  terminology remains subject to the approved glossary and any later terminology
  replacement

## Problem

Guest seating and official service beginning require clear responsibility.
Allowing the Host, Cashier, or an automatic identification interaction to open
the Customer Group would make service ownership and immediate financial
consequences ambiguous.

## Decision

The Responsible Waiter intentionally opens the Customer Group while holding the
required Open Customer Group Capability.

The Host may escort guests and coordinate seating but does not officially open
the Customer Group. NFC or manual Service Location identification opens only the
location’s digital context and never creates a Customer Group, Bill, charge,
Order, transfer, or Payment.

## Alternatives Considered

- The Host opens the Customer Group during seating.
- The Cashier opens the Customer Group.
- NFC identification automatically opens the Customer Group.
- Any Staff Member at the Service Location opens it.
- The Responsible Waiter accepts responsibility and intentionally opens it.

## Reasoning

The Responsible Waiter owns active service responsibility and is best placed to
confirm the party, Service Location, authority, and immediate opening
consequences. Intentional opening prevents physical identification or seating
coordination from silently creating operational or financial state.

## Consequences

- One eligible Responsible Waiter must accept responsibility before opening.
- The actor requires the Open Customer Group Capability; Role alone is
  insufficient.
- Guest Arrival must include a clear Host-to-Responsible-Waiter handoff.
- Opening at a Beach Sunbed produces the separately approved immediate Financial
  Obligation.
- Customer Group opening must remain safely recorded before success is shown.
- Responsible Service Staff terminology may require a future replacement
  decision; this example preserves the currently accepted decision language.

## Related Capabilities

- Guest Arrival
- Customer Group Opening
- Host Workspace
- Waiter Operations
- Ordering

## Related Architecture

- Authentication boundary
- Capability authorization boundary
- Guest Operations Platform strategy

## Related Domain Concepts

- Customer Group
- Responsible Waiter
- Staff Member
- Capability
- Service Location
- Financial Obligation

## Related Product Decisions

- Historical `DEC-011` — one active Customer Group per Service Location
- Historical `DEC-030` — Service Location Digital Identity
- Historical `DEC-034` — Beach Sunbed opening creates the immediate obligation
- Historical `DEC-035` — Responsible Waiter opens the Customer Group
- Historical `DEC-038` — Capability-based authorization

## Supersedes

None

## Superseded By

None

## Evidence and Validation

- Based on the approved Guest Arrival workflow, Customer Group lifecycle,
  Product Requirements, and Decision Log.
- Validate with Responsible Waiters and Hosts during workflow acceptance.
- Universal replacement of the term Responsible Waiter remains unresolved.

## Open Questions

- Should the official universal term become Responsible Service Staff?
- How are responsibility acceptance and handover formally confirmed?
- Which operational roles may hold Open Customer Group at future Venue types?

## Review Trigger

Before introducing a Venue type where the responsible service role is not called
Waiter, or before implementing production Customer Group opening.

## Decision History

- 2026-07-27 — Example record written from historical `DEC-035`.
- 2026-07-27 — Shown as Approved for illustration only; no replacement or new
  active authority created.

# Adoption Rules

Before this PDR system becomes the active process, the Product Owner should
approve:

- the PDR identifier sequence;
- the Product Governance Steward;
- the location and index of individual records;
- delegated approval scopes, if any;
- required specialist reviews;
- whether future PDRs are one file per record or maintained in an append-only
  collection;
- the transition policy for new decisions currently recorded in
  `DECISIONS.md`.

Until then, this document defines the proposed governance system, while
`DECISIONS.md` remains the active historical Decision Log.

# Final Principle

Product Decisions must make business meaning more durable, not more bureaucratic.

BeachOS should record the decisions that future people must understand, preserve
their reasoning and disagreement honestly, and make every later change explicit.

No contributor, implementation, architecture, document, or AI agent may silently
change what the Product Owner decided.
