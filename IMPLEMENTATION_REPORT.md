# Implementation Report — Parallel MVP Completion

## 1. Executive Summary

### Objective

Advance Billing, Payments, Customer Group Completion and Departure, and Venue
Closing in isolated parallel implementation branches.

### Status

Partially complete. Billing is implemented, verified, and merged. Three
capabilities are genuinely blocked by Product Owner decisions that the approved
repository explicitly forbids the team from assuming.

### Result

BeachOS now provides one authoritative, event-restored running Bill across the
Beach Sunbed opening obligation and all approved Order rounds. The operational
day advances through Bill Review. Payment, Completion/Departure, and Venue
Closing remain explicit gaps; no speculative business logic was introduced.

| Capability             | Branch                                | Outcome                                   |
| ---------------------- | ------------------------------------- | ----------------------------------------- |
| Billing                | `codex/billing`                       | Complete and merged (`7698620`)           |
| Payments               | `codex/payments`                      | Decision-blocked; report commit `a0b30fb` |
| Completion + Departure | `codex/customer-completion-departure` | Decision-blocked; report commit `f24b98d` |
| Venue Closing          | `codex/venue-closing`                 | Decision-blocked; clean baseline branch   |

## 2. Repository Tree

```text
apps/api/src/beachos_api/packs/beachos/billing/
├── __init__.py
├── application/
│   ├── __init__.py
│   └── service.py
├── domain/
│   ├── __init__.py
│   └── model.py
└── infrastructure/
    ├── __init__.py
    └── persistence.py
apps/api/tests/unit/packs/beachos/billing/test_billing.py
apps/web/src/
├── BillingWorkspace.tsx
├── billingApi.ts
└── billingApi.test.ts
docs/simulation/FIRST_OPERATIONAL_DAY.md
IMPLEMENTATION_REPORT.md
```

## 3. Files Created

- The Billing Domain, Application, and Infrastructure files shown above.
- `apps/api/tests/unit/packs/beachos/billing/test_billing.py`
- `apps/web/src/BillingWorkspace.tsx`
- `apps/web/src/billingApi.ts`
- `apps/web/src/billingApi.test.ts`

No source files were retained on the three blocked branches.

## 4. Files Modified

- `apps/api/src/beachos_api/api.py`
- `apps/api/src/beachos_api/composition.py`
- `apps/api/tests/integration/packs/beachos/ordering/test_ordering_vertical_slice.py`
- `apps/web/src/App.tsx`
- `docs/simulation/FIRST_OPERATIONAL_DAY.md`
- `IMPLEMENTATION_REPORT.md`

## 5. Commands Executed

```text
git baseline commit, branch creation, and isolated worktree creation
authoritative repository searches with rg, find, and sed
apply_patch for implementation, tests, simulation, and reports
ruff format and ruff check
mypy apps/api/src
pytest apps/api/tests/unit -q --no-cov
prettier --write
eslint . --max-warnings 0
tsc --build --pretty false
vitest run
vite build
git commits and Billing merge
```

No dependencies were installed.

## 6. Verification

| Check                               | Result                               |
| ----------------------------------- | ------------------------------------ |
| Backend formatting                  | Passed                               |
| Backend lint                        | Passed                               |
| Backend type checking               | Passed: 94 source files              |
| Backend unit tests                  | Passed                               |
| Frontend formatting and lint        | Passed                               |
| Frontend type checking              | Passed                               |
| Frontend tests                      | Passed                               |
| Frontend production build           | Passed                               |
| Billing PostgreSQL integration test | Added; execution unavailable locally |
| CI                                  | Not executed                         |

The blocked branches retain the compiling baseline and no speculative source
changes. Their blocker reports do not claim fresh build or test execution.

## 7. Test Results

- Backend unit tests: 134 passed, 0 failed, 0 skipped.
- Frontend tests: 34 passed, 0 failed, 0 skipped across 7 files.
- PostgreSQL Billing integration: collected with the existing Ordering vertical
  slice but not executed because no isolated PostgreSQL 17 server or
  `BEACHOS_TEST_DATABASE_URL` was available.

## 8. Known Issues

- PostgreSQL-backed Billing verification remains pending in the approved
  isolated PostgreSQL 17 environment.
- The Payments amount relationship is unresolved: partial, overpayment, and
  multiple-method behavior must not be assumed, while exact-full-only is also
  not an accepted invariant.
- Customer Group Completion and Departure lack approved conditions, authority,
  sequencing, no-Bill behavior, location release, evidence, and recovery rules.
- Venue Closing lacks an approved workflow, authority, readiness conditions,
  event, Closing Report, Business Date effects, and correction/reopening rules.

## 9. Technical Debt

- The temporary development identity remains in use.
- Bill corrections, reversals, closing, and reopening remain command-gated.
- Billing currently derives Balance from obligations only because confirmed
  Payment recording is not approved enough to implement.
- No workaround or hard-coded happy path was added for the blocked capabilities.

## Completed Work

- Created the four requested branches from one committed baseline.
- Implemented an event-restored Bill aggregate with structural validation.
- Added an explicit PostgreSQL adapter over the existing immutable financial
  event stream.
- Added `GET /billing/customer-groups/{customer_group_id}` and dependency wiring.
- Added a real-API Billing workspace with loading, no-Bill, failure, and
  explainable-line states.
- Added unit, integration-contract, and frontend tests.
- Removed the Billing gap from `FIRST_OPERATIONAL_DAY.md` only after the complete
  read path was executable.

## Deferred Work

- Payments until amount/method and success rules are approved.
- Customer Group Completion and Departure until lifecycle rules are approved.
- Venue Closing until its operational workflow and event are approved.

## Open Product Owner Questions

### Payments

1. Are partial Payments allowed?
2. Are overpayments allowed, and how is change or excess value handled?
3. May one Bill use multiple Payments or Payment Methods?
4. Which Payment Methods are approved for the MVP, and what confirms success for
   each one?
5. Who may record a Payment and which Capability authorizes it?
6. Which reference or evidence is mandatory for each Payment Method?
7. How must rejected and unknown outcomes be retained and recovered?
8. What Activity Log facts are mandatory?
9. What is the idempotency identity for an externally confirmed Payment?

### Customer Group Completion and Departure

1. What exact financial and operational conditions allow completion?
2. Who may complete the Customer Group and with which Capability?
3. Must its Bill already be closed, or are the actions one coordinated outcome?
4. Which outstanding Orders or Tickets block completion?
5. How does a no-Bill Customer Group complete?
6. Who confirms physical departure, and what event records it?
7. What is the exact sequence among departure, Bill closing, completion, and
   Service Location release?
8. When must a released location remain unavailable for cleaning or another
   reason?
9. What permanent evidence and Activity Log are required?
10. How is an unknown completion outcome safely recovered?

### Venue Closing

1. Who may close the Venue and which Capability authorizes it?
2. Which Customer Groups, Bills, Payments, Tickets, issues, and handovers must be
   resolved first?
3. Are overrides permitted, by whom, and with what recorded reason?
4. What is the official Venue Closing event and required event data?
5. What must the permanent Closing Report contain?
6. Which operations stop after closing, and how does closing affect the Business
   Date?
7. Can closing be corrected or reopened, and under what rules?

## Architecture Decisions

No new architecture theory was introduced. Billing reads financial events
already emitted atomically by Customer Group Opening and Ordering, avoiding a
duplicate financial source of truth. Blocked branches contain no invented event
models.

## Operational Coverage

The executable operational day now covers:

1. Department Readiness and Venue Opening.
2. Guest Arrival and intentional Customer Group Opening.
3. Ordering and separate Kitchen/Bar fulfilment through delivery.
4. Authoritative Bill Review, including opening and Order obligations.

The day currently stops at **Payment Requested**. Customer Group Transfer also
remains an earlier conditional gap when guests move locations. Payment,
Completion/Departure, and Venue Closing cannot be implemented safely until the
questions above are approved.

## 10. Next Recommended Task

Run a focused Product Owner decision session for **Payments**. It is the first
mandatory chronological blocker after Bill Review, and resolving its nine
questions enables the financial state needed by both Completion and Venue
Closing.
