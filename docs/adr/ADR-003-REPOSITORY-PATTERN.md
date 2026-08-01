# ADR-003 — Repository Pattern

## Status

Proposed recommendation. This ADR is not accepted.

## Context

The approved Clean Architecture direction places repository ports in the
Application Layer and their implementations in Infrastructure. The Venue Opening
Application Layer already depends on a narrow `VenueRepository` interface rather
than a database session or persistence model.

BeachOS will contain multiple Feature Packs and Industry Packs. Repository
boundaries must prevent one module from treating another module’s storage as a
public interface.

## Problem

The project needs a repository convention that supports aggregate consistency and
testability without becoming generic database abstraction or hiding uncontrolled
cross-module access.

## Options

1. **Aggregate-specific repositories owned by Application.** Define only the load
   and save operations required by approved use cases.
2. **Generic CRUD repository.** Use one reusable interface for create, read, update,
   delete, filtering, and pagination across all models.
3. **Direct persistence-session access from Application services.** Let use cases
   construct queries and save records directly.
4. **Repositories owned by Infrastructure.** Let database adapters define the
   interface consumed by inner layers.

## Recommended Option

Use aggregate-specific repository interfaces owned by the Application Layer.
Repositories load and stage complete aggregates within a unit of work. Their method
names use business context and do not expose tables, query builders, persistence
models, or database sessions.

Use separate query ports and read models when a use case needs reporting or
presentation data that does not require aggregate behavior. Do not expand Command
repositories into generic read APIs.

## Advantages

- Dependency direction remains inward.
- Tests can replace repositories with focused fakes.
- Aggregate boundaries and ownership stay visible.
- Infrastructure libraries can change without altering use cases.
- Separate Command and query needs avoid loading aggregates for every report.

## Disadvantages

- Several modules will define small, purpose-specific interfaces.
- Mapping and adapter code may appear repetitive.
- Repository boundaries require judgment when a use case touches several
  aggregates.
- Developers cannot use arbitrary database queries directly from Application code.

## Risks

- A generic base repository may become a disguised database API.
- Repository methods may grow around screen needs rather than business intentions.
- Cross-module joins may bypass Feature Pack ownership.
- Partial saves may violate aggregate consistency.
- Query ports may accidentally acquire Command behavior.

## Future Impact

Each Feature Pack will own its Application repository ports and Infrastructure
adapters. Cross-feature work should use public Application contracts, approved
read models, or explicit orchestration rather than another module’s private
repository. Shared repository abstractions should be introduced only after several
proven identical requirements.
