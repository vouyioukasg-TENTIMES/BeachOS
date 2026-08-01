# ADR-007 — Activity Log Strategy

## Status

Proposed recommendation. This ADR is not accepted.

## Context

Activity Logs preserve accountability for sensitive actions. They are distinct
from Domain Events, technical logs, and the wider Audit Trail. Approved principles
require an Activity Log for successful Venue opening and later sensitive actions,
including important financial and authority changes.

Activity Logs must support understanding and recovery without becoming employee
surveillance or allowing silent historical rewriting.

## Problem

The platform needs a consistent way to create, preserve, protect, and retrieve
Activity Logs while guaranteeing that a sensitive business outcome cannot succeed
without its required accountability record.

## Options

1. **Dedicated append-only Activity Log records in the primary database.** Stage
   the record in the same transaction as the sensitive business outcome.
2. **Reuse Domain Events as Activity Logs.** Treat every event as the accountability
   record.
3. **Use technical application logs.** Write structured log messages to the
   observability system.
4. **Write Activity Logs asynchronously after commit.** Allow the business outcome
   to commit first and add accountability later.
5. **Use an external audit service synchronously.** Require a remote system during
   each sensitive Command.

## Recommended Option

Use dedicated, append-only Activity Log records in PostgreSQL, staged through an
Application-owned port within the same transaction as the sensitive authoritative
outcome. Record the actor or approved origin, scope, time, affected subject,
official action, relevant prior and resulting facts, reason where required, and
request correlation.

Corrections add a linked record; they never rewrite the original. Access should be
explicit, least-privilege, and purpose-limited. Technical diagnostics remain in the
observability system. Domain Events remain separate business facts.

## Advantages

- Sensitive state and accountability commit or roll back together.
- Append-only history supports investigation and trust.
- Separation from Domain Events preserves clear business meaning.
- Separation from technical logs prevents retention and access policies from being
  conflated.
- Request correlation supports safe retry investigation.

## Disadvantages

- Every sensitive Command needs an explicit Activity Log contract.
- Append-only data grows continuously and needs an approved retention policy.
- Protecting useful prior/resulting facts without over-collecting personal data
  requires care.
- Read access needs dedicated authorization and query design.

## Risks

- Excessive logging could become surveillance.
- Sensitive personal or financial details could be exposed to broad readers.
- A generic unstructured payload could become impossible to govern.
- Retention may conflict with privacy or legal obligations.
- An adapter that commits the log separately could create silent divergence.

## Future Impact

Every new sensitive action must be classified during product and Domain review.
Feature Packs should use the shared Activity Log strategy while owning the
business-specific facts they contribute. Audit Trail views may later connect
Activity Logs, Domain Events, and preserved records, but must not rewrite or merge
their distinct meanings.
