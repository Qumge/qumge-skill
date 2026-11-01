# Consumer/publisher split verification

Scope: same two existing public repositories, same hosted MCP. Keep root skill name qumge;
add self-contained skills/qumge-publish. No platform code/runtime or Cap listing is created.

## Baseline and resulting behavior

- Independent baseline found existing developer instructions, but no bundled offline local
  readiness checker or resumable JSON report. The only prior script queried live tool metadata.
- Actual skills@1.7.4 default discovery found the root qumge entry. With --full-depth it found
  qumge and qumge-publish. A root SKILL.md short-circuits default discovery; installation docs
  explicitly account for this behavior rather than promising an unsupported name-only install.
- Actual isolated project copy installations succeeded for original default consumer and explicit
  full-depth publisher (Codex target, project scope only). Publisher resources ran standalone.
  The consumer root copy can contain nested repository resources; compatibility means preserving
  the root entry/name/command, not promising consumer-only package bytes.
- Independent forward test used a synthetic CLI-only project with example-domain URLs, no login,
  no approved price/publication and an offline-only request. The agent inspected code/manifest,
  ran the installed skill's checker, wrote/re-read its report, returned blocked and identified
  deployment/real URL gaps. It did not log in, network, deploy, invoke the CLI or publish.

## Checks

- 13 Python-standard-library tests pass. Cover strict JSON/duplicate/nonfinite values, extreme
  integer prices, credential redaction, malformed types, async private status, multiple-Cap
  selection, stable/changed file fingerprints, no network and non-overwriting report writes.
- Package check verifies both declared entry points, self-contained relative resources and the
  synchronized v2 template retained at the legacy reference path. Example-domain placeholders
  deliberately block local readiness rather than pretending to be a deployed provider.
- Official Skill Creator quick_validate.py passed for root qumge and qumge-publish. Its PyYAML
  dependency was installed in a temporary validation venv, not the user's global Python.
- Example manifest plus input/output examples pass the platform's current JSON Schema validator.
- Both repositories' live metadata-only tool checks pass: all 22 tools match, including migration.
- Independent code/package review found an oversized-integer diagnostic failure. A focused red
  regression reproduced it; range-before-float conversion fixed it. Reviewer reran all 13 tests,
  package and diff checks, then approved integration with no remaining material findings.

## Boundaries

The checker is offline local readiness, not full JSON Schema/business validation. It reads no
credential store, invokes no provider code and performs no platform mutation. Its raw local file
fingerprint is not a platform accepted contract digest. Deployment, authentication, owner scope,
platform checks and real delivery remain explicitly not_checked. Failed/partial/queued results
are not complete delivery. No new Cap, paid generation, user-global skill installation, payout
or wallet change occurred in this verification.

Before public release: integrate into main and push, then repeat remote installation from GitHub
using the documented command. Remove clean worktrees immediately after merge and push, preserving
branches. GitHub publication/installability is separate from publishing a developer's Cap.
