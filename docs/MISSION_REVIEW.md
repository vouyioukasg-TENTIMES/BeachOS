# Mission and Values Review

## 1. Outcome

`MISSION_AND_VALUES.md` now defines the company’s reason for existing, official mission, long-term product vision, measures of success, core values, Product Promise, and Decision Test.

The document is strategic rather than promotional. It does not introduce requirements, implementation choices, delivery commitments, or new business behaviour.

No existing documentation, approved business decision, application code, API, database model, user interface, or implementation file was changed.

## 2. Summary of the mission

The official mission is:

> Enable every hospitality business owner to know, at any moment, that the digital view of the business faithfully reflects its real-world operation.

The mission centers the company on reducing uncertainty. It does not treat digitization as an end in itself. The product should make confirmed operational truth visible and understandable while being honest about pending, failed, or incomplete information.

The long-term vision is a Hospitality Operating System that coordinates live service rather than only recording sales. Operational work remains primary; financial and administrative functions support that work.

## 3. Summary of the values

The document defines ten values:

1. **Truth Over Assumptions** — rely on confirmed, explainable business facts.
2. **Simplicity Over Complexity** — use the smallest clear solution that safely works.
3. **Operations Before Administration** — protect live service from unnecessary administrative burden.
4. **Trust Through Transparency** — make important actions and state understandable without encouraging blame.
5. **Technology Should Reduce Stress** — reduce uncertainty, repeated checking, and avoidable coordination.
6. **Every Screen Must Save Time** — require a clear operational purpose for every screen.
7. **Every Workflow Should Feel Natural** — follow real hospitality work and official business language.
8. **Hospitality Before Software** — make technology serve people and service.
9. **Long-Term Thinking Over Short-Term Convenience** — preserve durable concepts, history, and adaptability.
10. **Design for Real People Under Real Pressure** — support interrupted, mobile, outdoor, and demanding work with safe recovery.

Success is defined through operational clarity, staff confidence, owner confidence, guest experience, fewer mistakes, better teamwork, and lower operational stress. Feature, report, and setting counts are explicitly rejected as primary measures of success.

## 4. Relationship with Product Philosophy

`MISSION_AND_VALUES.md` and `PRODUCT_PHILOSOPHY.md` are complementary:

- Mission and Values explains **why the company and product exist**, what future they pursue, and what outcomes matter.
- Product Philosophy explains **how product choices should be judged** during design and development.

The Mission’s focus on an accurate operational mirror aligns with Operations First, The Business Owns the Truth, Business Rules Must Be Explicit, Consistency Creates Confidence, and Hospitality Before Technology.

The values reinforce the Product Philosophy without replacing it. The Product Philosophy remains the detailed reference for product judgment, while Mission and Values provides the shared company purpose behind that judgment.

The two decision tests overlap intentionally. Both reject unnecessary complexity and require long-term operational value. Mission and Values adds explicit tests for operational awareness, uncertainty, teamwork, and guest experience.

## 5. Relationship with Domain Model

The Domain Model defines what the business means by concepts such as Customer Group, Service Location, Order, Bill, Payment, Capability, and Activity Log. Mission and Values does not redefine those concepts or change their rules.

The mission depends on the Domain Model because a digital view can reflect the real operation only when the business concepts have stable, agreed meanings. Clear domain language allows staff actions, owner understanding, operational history, and product behaviour to refer to the same reality.

The Product Promise is therefore conditional and precise:

- staff must use the system correctly;
- displayed facts must be confirmed;
- uncertainty must remain visible;
- the product must preserve approved business meaning;
- the digital view must not claim knowledge the operation has not provided.

This is consistent with the central system being the source of operational truth, but it does not make the system infallible or allow software state to override real-world evidence without investigation.

## 6. Recommendations for future strategic documents

The following documents may be useful after Product Owner approval:

1. **Strategic Principles for Growth** — criteria for entering new Venue types, markets, and countries without weakening the product’s operational focus.
2. **Customer Research Charter** — how the company observes staff, validates problems, handles feedback, and distinguishes one-Venue preferences from durable product needs.
3. **Product Quality Scorecard** — a small set of measures for operational clarity, confidence, mistakes, teamwork, guest experience, and stress.
4. **Trust and Transparency Charter** — principles for operational visibility, Activity Logs, Audit Trails, privacy, fair staff treatment, and owner access.
5. **Responsible Automation and AI Principles** — boundaries for assistance, prediction, human control, explainability, and decisions that must remain human.
6. **Multi-Venue Product Strategy** — principles for shared standards, local operating differences, data separation, and Organization-level oversight.
7. **Service Reliability Promise** — approved expectations for availability, confirmation, recovery, communication, and operational fallback.

These recommendations do not create commitments or approved scope. Any strategic document that introduces a material product or business decision should follow the Decision Log process and receive human approval.
