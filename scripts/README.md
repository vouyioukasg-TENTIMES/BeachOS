# Engineering scripts

Scripts here must be safe, non-interactive by default, portable across supported developer systems where practical, and clear about any state they change.

- `check-environment.sh` reports whether proposed local tools are available.
- `check-foundation.sh` validates the repository skeleton without installing dependencies.

Destructive scripts and scripts requiring production secrets are prohibited without explicit design and review.
