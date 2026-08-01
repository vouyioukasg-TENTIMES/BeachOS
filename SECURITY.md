# Security Policy

## Reporting a vulnerability

Do not report suspected vulnerabilities in a public issue, discussion, pull request, or chat channel.

Until a dedicated security address is approved, report the issue privately to the project owner or authorised security maintainer. A private reporting address and response owner must be configured before the repository is shared outside the founding team.

Include, when safe:

- the affected component and version or commit;
- steps to reproduce;
- likely impact;
- any temporary mitigation;
- whether the issue may already have been exposed publicly.

Do not access data that is not yours, disrupt venue operations, or attempt destructive proof of impact.

## Response process

The authorised maintainer will:

1. acknowledge the report and establish a private communication path;
2. assess severity and affected data or operations;
3. contain immediate risk where necessary;
4. prepare and verify a fix or mitigation;
5. coordinate release and communication;
6. record lessons and preventive actions after resolution.

Response-time commitments will be approved before production launch.

## Supported versions

No production application version exists yet. A supported-version table will be added before the first release. Once releases begin, security fixes will target supported production versions and the current development line according to an approved support policy.

## Security requirements

- Never commit secrets, private keys, credentials, production environment files, database dumps, or personal data.
- Store local secrets only in ignored environment files or an approved secret manager.
- Use synthetic or properly anonymised development and test data.
- Review new dependencies for necessity, maintenance, licence, and known vulnerabilities.
- Keep dependency lockfiles under version control once generated.
- Require automated security and dependency checks before production release.
- Limit production access and record sensitive administrative actions.
- Follow the security principles in `docs/MASTER_BLUEPRINT.md` and decisions in `docs/DECISIONS.md`.

## Disclosure

Public disclosure, customer notification, and regulatory reporting decisions belong to authorised project leadership with appropriate legal advice. They must consider Greek and EU obligations and the safety of affected people and businesses.
