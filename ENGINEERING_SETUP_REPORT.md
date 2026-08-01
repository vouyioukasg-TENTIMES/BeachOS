# Emerald Management System — Engineering Setup Report

## 1. Outcome

The repository now has a reviewable engineering foundation for a long-term React, FastAPI, PostgreSQL, Docker, and GitHub Actions project.

The workspace is initialised as a Git repository with `main` as its default branch. No commit or remote repository was created.

No application feature was implemented. There is no authentication, database table, migration, API route, application entry point, HTML page, React component, or user-interface screen. No package or dependency was installed, no lockfile was generated, no container was started, and no production infrastructure was created.

The six approved planning documents were read and moved unchanged from the repository root into `docs/`. This gives the repository one clear documentation home and satisfies the approved governance model.

## 2. Repository structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
├── apps/
│   ├── api/
│   └── web/
├── docs/
├── infrastructure/
│   ├── deployment/
│   └── docker/
├── packages/
│   ├── config/
│   └── shared/
├── scripts/
├── tests/
│   ├── e2e/
│   ├── integration/
│   └── unit/
├── .dockerignore
├── .editorconfig
├── .env.example
├── .gitignore
├── .prettierignore
├── .prettierrc.json
├── .tool-versions
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── ENGINEERING_SETUP_REPORT.md
├── LICENSE
├── README.md
├── SECURITY.md
├── package.json
└── pnpm-workspace.yaml
```

## 3. Folder explanations

### `.github/`

Contains collaboration and automated repository controls:

- `workflows/ci.yml` defines continuous-integration checks.
- `dependabot.yml` proposes weekly dependency-update pull requests for JavaScript, Python, Docker, and GitHub Actions.
- `PULL_REQUEST_TEMPLATE.md` requires outcome, scope, decisions, verification, risk, recovery, and AI-assistance information.
- `ISSUE_TEMPLATE/bug_report.yml` collects reproducible defects while warning against public security reports.
- `ISSUE_TEMPLATE/decision_proposal.yml` follows the project’s permanent decision format.

No deployment workflow exists because the production provider and release model are not approved.

### `apps/`

Holds independently runnable applications:

- `apps/web/` is prepared for one mobile-first React and TypeScript application. It contains only project and static-analysis configuration. It has no application entry point or visual output.
- `apps/api/` is prepared for the FastAPI backend. It contains only `pyproject.toml` and documentation. It has no Python package, route, database model, or business logic.

Keeping runnable applications here makes ownership clear and allows shared repository tooling without mixing frontend and backend implementation.

### `packages/`

Reserves space for carefully controlled shared work:

- `packages/config/` may later hold configuration proven to be shared.
- `packages/shared/` may later hold stable contracts or utilities with clear ownership.

Both are intentionally empty except for guidance. This prevents premature shared abstractions and cross-application coupling.

### `infrastructure/`

Separates operational definitions from product code:

- `infrastructure/docker/` contains the local PostgreSQL Compose definition and usage guidance.
- `infrastructure/deployment/` records the approval gate for future hosted infrastructure and contains no deployment resources.

### `scripts/`

Contains small repeatable engineering checks:

- `check-environment.sh` reports local availability and versions of Git, Node.js, Corepack, Python, uv, Docker, and Docker Compose. It does not install or change anything.
- `check-foundation.sh` verifies required folders and files and confirms that common application entry points and migration configuration have not appeared during this foundation-only phase.

### `tests/`

Provides homes for tests spanning application boundaries:

- `unit/` is reserved for repository-level utilities.
- `integration/` is reserved for real component and infrastructure boundaries.
- `e2e/` is reserved for a small number of critical browser-to-backend journeys.

Tests belonging only to the web or API application should stay beside that application. There are no test implementations because there is no application behaviour to test.

### `docs/`

Contains the permanent, approved project references:

- `MASTER_BLUEPRINT.md`
- `DECISIONS.md`
- `PRODUCT_VISION.md`
- `PRODUCT_REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `DEVELOPMENT_PLAN.md`
- `README.md`, which indexes the documents.

The original six documents were moved here without content changes. Engineering decisions DEC-021 through DEC-029 were added as **Proposed** entries to the decision log. Under the project’s governance rules, only an authorised human can accept them.

## 4. Root configurations and policies

### `README.md`

Explains the product, current foundation-only status, repository map, intended stack, prerequisites, validation commands, and governance entry points. It explicitly prevents application work before review.

### `CONTRIBUTING.md`

Defines the branch, review, decision, testing, security, commit, dependency, and AI-assisted contribution expectations. It turns the blueprint’s principles into a practical contribution workflow.

### `CODE_OF_CONDUCT.md`

Sets a concise professional standard for repository, meeting, and venue-testing collaboration. It includes reporting and conflict-of-interest expectations. A private contact still needs to be named before outside contributors join.

### `SECURITY.md`

Defines private vulnerability reporting, response steps, data-handling rules, dependency expectations, and future supported-version requirements. It intentionally does not publish a personal address. A dedicated security contact and response times are still required before production.

### `LICENSE`

Uses an all-rights-reserved proprietary notice because this is currently an internal commercial project and no open-source grant was authorised. The legal copyright owner and final licensing model need owner or legal confirmation.

### `.gitignore`

Excludes secrets, local environment files, dependency directories, virtual environments, build output, test reports, caches, editor files, logs, infrastructure state, and local database data. `.env.example` remains trackable.

### `.editorconfig`

Standardises UTF-8, LF line endings, final newlines, whitespace cleanup, and indentation across editors. Python uses four spaces; most configuration and web files use two.

### `.env.example`

Documents local PostgreSQL and future application environment-variable names with explicitly non-production values. `.env` and variant files are ignored. This file is a contract example, not a secret store and not an application configuration implementation.

### `.dockerignore`

Prevents secrets, repository metadata, dependencies, caches, results, logs, and local database data from being copied into future Docker build contexts.

### `.tool-versions`

Proposes Node.js 24.16.0 LTS and Python 3.13.14 for tools that understand the asdf-style file. The same major-version expectations appear in project metadata and CI.

### `package.json` and `pnpm-workspace.yaml`

Define a private pnpm workspace for the web application and future shared packages. The root scripts provide one entry point for formatting, linting, type checks, tests, and builds after lockfiles are approved. A workspace catalog keeps React and React DOM aligned.

No `pnpm-lock.yaml` exists because dependency resolution was not authorised. The frontend CI job remains gated until a reviewed lockfile is committed.

### Prettier configuration

`.prettierrc.json` establishes deterministic basic formatting and a 100-column preference. `.prettierignore` excludes generated output and lockfiles. Prettier is formatting-only; ESLint remains responsible for code-quality rules.

## 5. Frontend tool selection

### React 19

React matches the approved one-codebase, responsive web direction and provides a mature component ecosystem. The workspace proposes the current React 19.2 line. No React component or screen exists.

### TypeScript in strict mode

Strict TypeScript, unchecked-index protection, casing checks, and isolated modules are configured before code exists so unsafe defaults do not become established. The configuration uses the modern JSX transform required by React 19.

### Vite

Vite is proposed as the client development and build tool. A separate FastAPI backend already owns server behaviour, so a client-focused tool is simpler than introducing another full-stack server framework.

### ESLint and Prettier

ESLint is configured for JavaScript, type-aware TypeScript, React Hooks, and safe React refresh behaviour. Prettier handles formatting separately, limiting rule overlap.

### Vitest

Vitest is proposed for frontend unit and component tests because it shares Vite’s transformation model and supports fast feedback. No DOM-testing or accessibility-testing library has been selected yet.

## 6. Backend tool selection

### Python 3.13 and FastAPI

Python 3.13 is proposed as a stable supported runtime line. FastAPI is the requested backend framework and is constrained to one reviewed minor release line because versions below 1.0 may introduce breaking changes between minor versions.

### uv

uv is proposed to manage the project Python version, virtual environment, dependency resolution, lockfile, and tool execution through `pyproject.toml`. It avoids multiple overlapping setup tools and supports reproducible installs after `uv.lock` is approved.

### Uvicorn

Uvicorn is proposed as the initial ASGI application server used by FastAPI. Production process topology remains undecided because hosting and capacity requirements are not approved.

### Ruff, mypy, and pytest

- Ruff provides fast formatting, import ordering, security-oriented lint rules, and general Python checks.
- mypy is set to strict mode to make interface assumptions explicit.
- pytest provides readable tests; pytest-cov measures coverage.

The coverage failure threshold is deliberately zero during an empty foundation. A meaningful, risk-based threshold must be approved when the first code is introduced.

## 7. PostgreSQL and Docker

`infrastructure/docker/compose.yaml` proposes PostgreSQL 17 Alpine for local development. It:

- requires database name, user, and password through environment variables;
- publishes the port only on `127.0.0.1`;
- uses PostgreSQL’s readiness check;
- stores data in a named volume;
- places the service on an internal Docker network;
- creates no schema, table, migration, or seed data.

The application services are not yet containerised. Their entry points, build artefacts, non-root runtime users, health checks, and production process model cannot be defined honestly before application setup and deployment decisions are approved.

## 8. GitHub Actions and dependency maintenance

The continuous-integration workflow grants read-only repository access, cancels superseded runs on the same branch, and sets job time limits.

The foundation job runs now and uses no installed project dependencies. Frontend and backend jobs are defined but execute only after their respective lockfiles exist. Once enabled, they use locked installs and run formatting, linting, type checks, tests, and builds.

Dependabot is configured to propose grouped or bounded weekly updates. Automated update pull requests still require tests and human review; they are not automatically merged.

No CI secret, cloud credential, deployment permission, self-hosted runner, or production action is configured.

## 9. Environment variables and local development

The local model is:

1. approved runtimes are installed by the developer;
2. `.env.example` is copied to ignored `.env` and its local password is changed;
3. Docker Compose provides PostgreSQL;
4. pnpm and uv create isolated dependency environments only after lockfiles are approved;
5. frontend and backend applications run as developer processes during early implementation.

This provides fast iteration and simple debugging while keeping the database reproducible. A fully containerised developer experience can be added if onboarding evidence shows it provides enough value.

The current machine check found Git 2.50.1 and Python 3.9.6. Node.js, Corepack, uv, and Docker were not available. No attempt was made to install or upgrade them.

## 10. Decisions documented

The following proposed decisions were added to `docs/DECISIONS.md`:

- DEC-021 — pnpm workspace;
- DEC-022 — Python 3.13, uv, and `pyproject.toml`;
- DEC-023 — React and frontend quality toolchain;
- DEC-024 — FastAPI and backend quality toolchain;
- DEC-025 — local PostgreSQL through Docker Compose;
- DEC-026 — environment-variable configuration and secret exclusion;
- DEC-027 — GitHub Actions continuous integration;
- DEC-028 — application-local and cross-system test placement;
- DEC-029 — proprietary licence by default.

The entries include alternatives, reasons, consequences, and review triggers. They remain Proposed until an authorised human changes their status.

## 11. Validation performed

The foundation was validated without package installation:

- required top-level directories and policy files exist;
- all six approved planning documents exist under `docs/`;
- no common frontend or backend application entry point exists;
- no migration configuration or database schema exists;
- JSON and YAML files were syntax-checked using available system tools;
- shell scripts were syntax-checked and the foundation check was executed;
- file and directory inventories were inspected;
- dependency directories, lockfiles, application build output, and containers were not created.

The backend TOML configuration could not be parser-checked because neither Python 3.11+ nor another TOML parser is available locally, and installing one is outside this task. Full frontend, backend, Compose, and GitHub Actions execution also cannot be verified locally because the required tools are not installed and dependency installation is outside this task.

## 12. Items requiring approval

### Engineering decisions

The owner should accept, reject, or revise DEC-021 through DEC-029. In particular, confirm:

- Node.js 24 LTS, Python 3.13, pnpm, and uv;
- React 19, Vite, TypeScript, ESLint, Prettier, and Vitest;
- the FastAPI minor line, Uvicorn, Ruff, mypy, and pytest;
- PostgreSQL 17 for local development;
- GitHub Actions and Dependabot;
- the proprietary licensing approach and legal copyright owner.

### Repository administration

- Confirm the GitHub organisation, repository visibility, and whether the local `main` default branch should remain.
- Create the remote repository and first reviewed commit.
- Name code owners and required reviewers.
- Configure branch protection, required checks, signed-commit policy if desired, and merge strategy.
- Configure a private security-reporting address and conduct-report contact.

### Dependency resolution

- Review every declared dependency and version.
- Authorise dependency resolution and installation.
- Generate and review `pnpm-lock.yaml` and `apps/api/uv.lock`.
- Run licence, vulnerability, formatting, linting, type, test, and build checks.
- Enable the currently gated frontend and backend CI jobs through committed lockfiles.

### Application and testing choices

- Approve source and module layouts before creating entry points.
- Select routing, server-state management, styling, component, form, localisation, and accessibility-testing tools only when required.
- Select browser end-to-end tooling and database-test isolation.
- Set coverage and supported browser/device policies.

### Infrastructure and operations

- Confirm PostgreSQL major-version policy.
- Select hosting provider, region, deployment format, network, DNS, TLS, secret manager, monitoring, logging, and alerting.
- Approve availability, recovery-time, recovery-point, backup-retention, and restore-test targets.
- Confirm development, staging, and production ownership and access controls.
- Complete venue connectivity testing.

### Business and legal questions still open in approved documents

The engineering foundation does not resolve fiscal, receipt, payment-terminal, accounting, data-retention, privacy, reporting, language, or offline-operation decisions. Those require owner and appropriate professional review before relevant implementation.

## 13. Stop point

The engineering environment is ready for review and stops at the authorised boundary. The next action should be human review of this report and proposed decisions. No application code, dependency installation, database design, API, authentication, or UI work should begin until explicitly approved.
