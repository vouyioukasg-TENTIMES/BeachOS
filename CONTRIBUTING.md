# Contributing to Emerald Management System

Thank you for helping build Emerald Management System. Correctness, clarity, operational safety, and respect for staff take priority over delivery speed.

## Before starting

1. Read `docs/MASTER_BLUEPRINT.md`, `docs/DECISIONS.md`, and the relevant requirements.
2. Confirm that the work belongs to an approved phase and has clear acceptance conditions.
3. Search the decision log for related choices and unresolved proposals.
4. Create a new proposed decision before making a significant product or architecture change.
5. Never use production personal, payment, or customer data in development or tests.

## Change workflow

1. Work on a short-lived branch from the protected default branch.
2. Keep the change focused on one outcome.
3. Add or update tests and documentation with the behaviour they protect.
4. Run all applicable local checks.
5. Open a pull request using the repository template.
6. Obtain review from an authorised human. High-risk changes require explicit domain and security review.
7. Merge only after required automated checks pass and all review discussions are resolved.

Direct production changes and unreviewed changes to the protected default branch are not allowed.

## Commit guidance

- Write short, imperative commit subjects in English.
- Explain the reason for a non-obvious change in the commit body.
- Keep formatting-only work separate from behavioural work when practical.
- Reference a Decision ID when the commit implements or changes a recorded decision.

Example:

```text
Configure backend static analysis

Implements the tooling proposed in DEC-022.
```

## Quality requirements

- Follow the naming and coding standards in the master blueprint.
- Prefer clear, explicit solutions over clever shortcuts.
- Validate data at every system boundary.
- Never use floating-point values for money.
- Never silently rewrite operational or financial history.
- Keep secrets, credentials, and private data out of source control, tests, logs, screenshots, and AI prompts.
- Do not add a dependency without explaining its value, maintenance status, licence, and security effect.
- Treat accessibility, observability, recovery, and documentation as part of completion.

## Testing expectations

Use the smallest useful test level:

- unit tests for isolated rules and calculations;
- integration tests for database, transaction, and component boundaries;
- end-to-end tests for critical staff journeys;
- manual staff acceptance checks for real operational usability.

A defect affecting money, permissions, order delivery, transfers, or data integrity should receive a regression test whenever practical.

## AI-assisted contributions

AI assistance is allowed under `docs/MASTER_BLUEPRINT.md` and DEC-020. The contributor remains accountable for understanding and verifying every change. Disclose material AI assistance in the pull request, do not share secrets or unnecessary personal data, and do not accept generated dependencies or copied material without provenance and licence review.

## Security reports

Do not open a public issue for a suspected vulnerability. Follow `SECURITY.md`.

## Conduct

All contributors must follow `CODE_OF_CONDUCT.md`.
