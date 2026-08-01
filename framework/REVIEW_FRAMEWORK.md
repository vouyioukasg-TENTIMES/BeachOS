# Beach Operations Framework — Consistency Review

## 1. Review Scope

This review compares the new Operational Framework direction with the complete existing repository, including:

- product, domain, governance, mission, philosophy, vision, requirements, architecture, planning, glossary, and historical review documents in `/docs`;
- repository governance and engineering reports;
- application, package, infrastructure, script, test, and GitHub foundation material;
- the new Framework introduction, principles, roadmap, and directory structure.

The review makes recommendations only. It does not modify or supersede existing documentation or approved business decisions.

## 2. Overall Consistency

The Operational Framework is strongly aligned with the project’s existing direction.

Existing documents already place hospitality operations before administration, treat the central system as a source of operational truth, preserve business concepts independently from technology, prioritize staff confidence and guest experience, require explicit business rules, and describe software as a quiet system that reduces uncertainty.

The new Framework makes a previously implicit distinction explicit:

- operational guidance defines how excellent work should be performed;
- software enables that guidance to be executed consistently and observed reliably.

This is an extension of scope rather than a contradiction. The most important governance need is now to define clear authority and links between Framework material and the existing product documents.

## 3. Duplicated Concepts

### Mission and Vision

`docs/MISSION_AND_VALUES.md`, `docs/PRODUCT_VISION.md`, `docs/MASTER_BLUEPRINT.md`, and the Framework introduction all discuss why the product exists and the long-term ambition to support hospitality operations.

The overlap is coherent but could become repetitive. The Framework should refer to the company Mission and Product Vision rather than restating them in every operational document. Framework Vision should focus on the desired future state of operations.

### Product Philosophy and Framework Philosophy

`docs/PRODUCT_PHILOSOPHY.md` defines how product choices should be evaluated. The new Framework principles define how operating practices should be evaluated.

Several principles intentionally overlap: Hospitality First, simplicity, trust, reduced stress, consistency, human judgment, long-term thinking, and operational value. They should remain two perspectives with a shared foundation:

- Product Philosophy governs product decisions.
- Framework Philosophy governs operational practice.

Copying the full principle text between both locations would create two sources that could drift.

### Roles

The Domain Model defines Staff Member, Role, Capability, Host, Cashier, and related business concepts. Requirements describe current responsibilities. The Framework’s `/03 Roles` area will also describe operational Roles.

This duplication is safe only if:

- the Domain Model defines what a Role means and how it relates to other business concepts;
- the Framework defines what good performance, collaboration, and handover look like for that Role;
- Capabilities continue to authorize protected actions;
- Role playbooks do not silently create authorization.

### Workflows

Requirements, Domain Events, development acceptance checks, and future Framework workflows may all describe sequences of work.

Their purposes should remain distinct:

- the Framework describes how the operation should work, including human activity outside software;
- Product Requirements describe what the product must support;
- Domain Events name meaningful completed business facts;
- the Development Plan describes when approved product support may be delivered;
- tests later verify the implemented behaviour.

### Operational Standards and Product Quality Requirements

Existing documents define product reliability, security, accessibility, performance, and usability principles. Framework standards will define observable standards for venue operation.

The two should be linked but not merged. A standard such as “every active Customer Group has clear responsibility” may have both an operational practice and a product control, but those are not the same document.

### Coaching, Activity Logs, and Audit Trails

Existing philosophy says accountability should support learning rather than punishment. The Framework adds Coaching Before Judging.

This is consistent, but Coaching material must not turn Activity Logs or Audit Trails into employee surveillance or simplistic performance scoring. Coaching practices should interpret evidence in context.

### Decision Guidance

The Product Philosophy, Mission and Values, Decision Log template, and `/08 Decision Engine` all involve decisions.

They should not become competing decision systems:

- Mission and Values states what outcomes matter.
- Product Philosophy filters product choices.
- Framework principles guide operational choices.
- the Decision Engine offers approved guidance for recurring operational situations.
- the Decision Log records material approved decisions and why they were made.

## 4. Conflicting or Unsettled Terminology

### Product Name

The repository uses both **Emerald Management System** and **Emerald Hospitality Operating System**.

The Project Glossary defines Hospitality Operating System as the official product category, but existing files and engineering package names still use Emerald Management System. It remains unclear whether Emerald Hospitality Operating System is a renamed product, a strategic description, or the umbrella product containing the Core Platform and Frameworks.

Recommendation: approve a naming architecture before changing existing titles, repository names, or package names.

### Beach Operations Framework

The new documents use **Beach Operations Framework** as requested. This term is not yet defined in the Project Glossary or Decision Log.

Recommendation: define whether this is the official name of the Phase 1 industry Framework and record its authority before wider documentation alignment.

### Operational Framework

The strategic decision refers to “the Operational Framework,” while the first industry-specific body is called the Beach Operations Framework.

Recommendation: use **Operational Framework** as the general category and **Beach Operations Framework** as the beach-club-specific instance, subject to Product Owner approval.

### Core Platform

The roadmap introduces **Core Platform** as the shared software foundation across industry Frameworks. Existing architecture describes one application and clear business areas but does not define Core Platform as an official concept.

Recommendation: define Core Platform strategically before using the term in architecture or implementation planning. Do not infer that a separate technical platform, service, or deployment is required.

### Responsible Service Staff and Responsible Waiter

The Project Glossary uses Responsible Service Staff as the venue-neutral concept. Existing accepted decisions and core documents use Responsible Waiter for the current approved opening and accountability rule.

Recommendation: resolve this terminology through Product Owner approval before authoring cross-industry Role standards. Preserve the accepted rule for Emerald Beach Club unless a new decision explicitly supersedes it.

### System

“The system advises” may mean the Framework, the software, or both.

Recommendation: Framework documents should name the actor precisely:

- **Framework guidance** advises through documented knowledge and standards.
- **Software guidance** presents approved advice in context.
- **Business rules** require or prohibit defined outcomes.
- **Humans** make decisions requiring judgment.

### Decision Engine

The directory name could be interpreted as an automated software component. In the Framework it means approved operational decision guidance.

Recommendation: define it in the Project Glossary before implementation discussion and avoid assuming automation, artificial intelligence, or autonomous authority.

### Activity Log and Audit Trail

The Project Glossary now distinguishes one Activity Log from a connected Audit Trail. Some historical review text retains older ambiguity.

Recommendation: use the current glossary in new Framework material and preserve historical reports as historical records.

## 5. Missing Links

### Repository and Documentation Indexes

The root `README.md` and `docs/README.md` do not mention `/framework`. This is expected because existing documentation was not modified in this task, but future readers may not discover the Framework.

### Governance

`CONTRIBUTING.md`, the pull-request template, and the decision proposal template do not yet require contributors to review relevant Framework material when changing an operational workflow.

### Decision Log

The strategic distinction between Operational Framework and software is not yet recorded in `docs/DECISIONS.md`. The Decision Log also has no explicit Framework or Operational Standards category.

### Project Glossary

The glossary does not yet define:

- Operational Framework;
- Beach Operations Framework;
- Core Platform;
- Workflow;
- Playbook;
- Coaching;
- Operational Standard;
- Decision Engine.

### Traceability

There is no agreed way to link:

- an operational principle to a workflow;
- a workflow to applicable Roles and Playbooks;
- a Framework rule to a Domain Model concept;
- an approved operational decision to a Decision ID;
- an operational workflow to Product Requirements and acceptance evidence;
- an Operational Standard to observed venue outcomes.

### Ownership and Approval

The repository does not define who owns each Framework area, who may approve an operational standard, how venue operators participate, or how often Framework material is reviewed.

### Versioning and Applicability

The Framework does not yet define:

- whether a document is draft, approved, or retired;
- which industry and Venue types it applies to;
- whether a rule is universal, industry-specific, or Venue-specific;
- how historical Framework guidance is preserved when practice changes;
- how a Venue records an approved local variation.

### Evidence and Learning

Existing product documents value real staff testing, but there is no Framework-specific evidence standard for promoting an observed practice into a recommended workflow or Operational Standard.

## 6. Recommendations

1. Record the new strategic distinction between Operational Framework and software as an Accepted decision before implementation work relies on it.
2. Approve a clear naming architecture for the company, product, Hospitality Operating System, Core Platform, and industry Frameworks.
3. Add the Framework to root and documentation indexes after this structure is approved.
4. Extend the Project Glossary with the missing Framework terms before the folders receive substantial content.
5. Define an authority map showing which source governs mission, vocabulary, business meaning, decisions, operational practice, product behaviour, architecture, and delivery.
6. Create a lightweight standard header for future Framework documents: purpose, scope, applicability, status, owner, related concepts, related Decision IDs, evidence, and review date.
7. Keep Framework Roles focused on responsibility, conduct, collaboration, and outcomes; keep Capabilities as the source of action authority.
8. Keep Framework workflows useful without software and link product requirements to them only when software support is approved.
9. Separate normal workflows, exception Playbooks, coaching guidance, and Operational Standards so they do not become four descriptions of the same content.
10. Define the Decision Engine as explainable operational guidance before considering any software or AI support.
11. Establish a human approval and field-validation process involving experienced operators.
12. Preserve historical Framework versions or decision history rather than silently rewriting important operating guidance.
13. Review privacy and fairness before using operational data for coaching, standards, or staff evaluation.
14. Add Framework checks to future product proposals: identify the supported operational outcome and confirm that software does not redefine the practice.
15. Delay cross-industry abstraction until common concepts are proven in real Beach Club operation.

## 7. Short Integration Proposal

The Framework should integrate with existing documentation through references and traceability, not repeated content.

Use the following authority boundaries:

| Source | Governs |
|---|---|
| `docs/MISSION_AND_VALUES.md` | Why the company and product exist |
| `docs/PRODUCT_PHILOSOPHY.md` | How product choices are evaluated |
| `docs/PROJECT_GLOSSARY.md` | Official business vocabulary |
| `docs/DOMAIN_MODEL.md` | Business concepts, relationships, lifecycles, rules, and events |
| `docs/DECISIONS.md` | Approved material decisions and their reasoning |
| `/framework` | How excellent hospitality operations should be performed |
| `docs/PRODUCT_REQUIREMENTS.md` | What the software must support |
| `docs/ARCHITECTURE.md` | How approved software responsibilities are structured |
| `docs/DEVELOPMENT_PLAN.md` | How approved product support is phased |

For each future software feature:

1. link to the operational outcome or Framework workflow it supports;
2. use official Glossary and Domain Model language;
3. cite any material Decision IDs;
4. state which part of the workflow remains human;
5. define what the software advises, enforces, confirms, or records;
6. test both operational usefulness and product correctness.

For each future Framework document:

1. link to existing Domain Concepts rather than redefining them;
2. cite approved decisions rather than restating their full history;
3. describe the complete operation, including work outside software;
4. state whether guidance is a principle, recommendation, required standard, or approved business rule;
5. identify the affected Roles and measurable operational outcome.

This approach keeps the Operational Framework usable without software, keeps software accountable to real operations, and gives each important idea one authoritative home.

## 8. Review Conclusion

The Framework direction is consistent with the project’s mission, Product Philosophy, Domain Model, and emphasis on operational truth.

The structure is ready for strategic review. Before substantial Framework content or implementation begins, the Product Owner should approve the authority boundaries, naming architecture, governance model, and missing glossary terms identified above.
