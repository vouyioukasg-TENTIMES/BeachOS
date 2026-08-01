# BeachOS Platform

BeachOS is an operational platform for beach clubs and similar hospitality venues. Emerald Beach Club in Loutraki, Greece, is the first client and learning partner.

The repository contains the approved product foundation and the runnable engineering bootstrap. It intentionally contains no business features, authentication, database schema, or product UI. The backend exposes only a health check, and the frontend shows only the Sprint 1 placeholder.

## Repository map

- `apps/` — independently runnable frontend and backend applications.
- `packages/` — code and configuration intended to be shared by applications.
- `infrastructure/` — local containers and future deployment definitions.
- `scripts/` — safe, repeatable engineering utilities.
- `tests/` — cross-application unit, integration, and end-to-end test areas.
- `docs/` — approved product, architecture, governance, and engineering documents.
- `.github/` — continuous integration and repository collaboration settings.

See [docs/README.md](docs/README.md) for the document index and [ENGINEERING_SETUP_REPORT.md](ENGINEERING_SETUP_REPORT.md) for the complete foundation review.

## Intended technology foundation

- React and TypeScript for the responsive web application.
- FastAPI and Python for the backend application.
- PostgreSQL for relational data.
- Docker Compose for reproducible local infrastructure.
- pnpm for the JavaScript workspace.
- uv for Python environments and dependency locking.
- GitHub Actions for automated checks.

## Current status

The repository is bootstrapped for Sprint 1. See [BOOTSTRAP.md](BOOTSTRAP.md) for installation, development, testing, and build commands.

## Local prerequisites

The proposed local environment requires:

- Git;
- Node.js 24 LTS with Corepack;
- Python 3.13;
- uv;
- Docker Engine or Docker Desktop with Docker Compose v2.

Run the environment check after installing the prerequisites:

```sh
./scripts/check-environment.sh
```

Install dependencies and validate the repository by following [BOOTSTRAP.md](BOOTSTRAP.md). The structural check is:

```sh
./scripts/check-foundation.sh
```

## Governance

Read these before contributing:

- [MASTER_BLUEPRINT.md](docs/MASTER_BLUEPRINT.md)
- [DECISIONS.md](docs/DECISIONS.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [SECURITY.md](SECURITY.md)

Application work must begin from an approved requirement, use a small reviewable change, include appropriate tests, and preserve the product’s financial and operational safety principles.

## Licence

This repository is currently proprietary and all rights are reserved. See [LICENSE](LICENSE). A different distribution model requires an explicit decision by the owner.
