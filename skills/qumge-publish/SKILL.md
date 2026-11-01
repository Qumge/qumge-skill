---
name: qumge-publish
description: Use when a developer wants to turn an existing project, API, MCP tool, CLI or internal workflow into a paid Qumge capability, prepare or resume its publishing process, update its contract, or manage their published Caps and earnings. For buying or using capabilities, use the qumge skill instead.
license: MIT
metadata:
  author: Qumge
  version: 0.1.0
---

# Publish an existing workflow on Qumge


Work in the developer's project using its existing coding, test and deployment tools.
The hosted Qumge MCP at https://qumge.com/mcp handles registration, checks, publication
and settlement; it does not read local code or deploy it. This skill adds a reusable
publishing workflow, not a new runtime, wallet, hosted CLI service or permission to publish.

## Language

Use the user's requested language for explanations, questions and human-readable reports.
If no language is specified, follow the language of their latest request, including Simplified
Chinese or English. Keep tool names, commands, identifiers, JSON keys and protocol values
unchanged. Preserve machine-readable report schemas; explain their findings in the user's
language. These English instructions are the single maintained execution specification.

## Start with the outcome

Read the project before asking the owner to fill in details you can determine locally.
Identify one clear input, a complete usable result, its completion criteria and limits.
Reuse an existing API/MCP operation if it supplies that whole outcome. Compose partial
steps privately on the provider server; do not sell the internal status or helper steps.
If no interface exists, add thin authenticated HTTPS invoke/status hooks around native
functions and jobs. A local CLI still needs a chosen server/container to run on; do not
promise an always-on service from a laptop or invent a deployment URL.

Use current managed manifest v2 and prefer `identity: order`. Read
[adaptation.md](references/adaptation.md) for interface selection and native-task reuse.
It links the maintained Ruby adapter and isolated contract-validation pack; use them
when appropriate rather than building a second order/queue system.

## Resolve only missing decisions

Reuse the owner's approved outcome, price, deployment target and publication scope.
Ask only for missing initial pricing, a changed price, unclear scope or indispensable
access. A price copied from a template is not approval. Implementation/deployment
permission alone is not permission to publish or run a paid real generation.

Keep provider credentials in the private connection, never public JSON or reports.
Use the owner's Qumge login/key for platform tools; provider authentication is a separate
credential. See [platform-access.md](references/platform-access.md) only when connecting
or authenticating, or when MCP tools are unavailable. Do not repeat login each session.

## Prepare a reproducible local preflight

1. Inspect existing functions, jobs, API/MCP routes and deployment configuration. Choose
   the least-change reliable path and keep account/admin/payment tools private.
2. Create the project's `qumge.json`. Start from
   [qumge.example.json](references/qumge.example.json), replacing example-domain URLs,
   example names and suggested pricing with the actual approved contract. Supply real
   HTTPS icon/connection URLs, schemas, examples, truthful idempotency, and async status
   mappings when needed. Read https://qumge.com/en/docs/caps/managed.md for full requirements.
3. Run the bundled checker from this installed skill directory, passing the manifest's
   absolute project path. Run it before any platform mutation; it makes no network call:

   ```bash
   python3 scripts/preflight.py /absolute/project/qumge.json \
     --slug your-cap-slug --report /absolute/project/.qumge/preflight-01.json
   ```

   The checker needs Python 3.10+, no third-party packages. It reads only the manifest
   and creates the explicitly requested report. Use a new report filename for each run;
   existing files are never overwritten. Without `--report`, JSON is printed to stdout.
   It never reads credential files, invokes the CLI, deploys, publishes or generates work.
4. Fix `findings` and rerun. Exit `0` means its named local checks passed, `1` means
   blocked local checks/JSON, and `2` means usage or report-writing failure. The script
   deliberately does not implement full JSON Schema or platform/business validation;
   all of those remain in `not_checked`. Do not turn this result into "ready/live/paid".

The report's `manifest_file_sha256` fingerprints raw local file bytes. It is not the
platform's accepted contract digest. Save reports outside public web roots; do not commit
owner credentials, private inputs or the owner's authorization details into public files.

## Adapt, deploy, register and verify

- Implement only the missing provider-side interface/composition. Reuse native jobs,
  durable atomic request-ID deduplication, workers and private assets. `native`
  idempotency is a claim about implemented behavior; the example truthfully declares
  `none` until you implement recovery. Account-bound operations need explicit buyer
  authorization; a shared service token never authorizes access to all users' data.
- Test full output, failure, partial completion, concurrent duplicate submissions and
  request/result isolation on the project side. Acceptance/job IDs are not completion.
  Use isolated non-generating fixtures first; real paid tests need an approved budget.
- Deploy using the project's normal tools within the existing scope. Confirm the
  running version, authentication and reachable HTTPS manifest. Qumge does not host this
  provider automatically. If deployment/access is missing, report it and preserve the
  completed local artifacts instead of inventing a service URL.
- Read `list_caps`/`cap_status` when resuming. Use `become_developer` only if needed.
  `publish_cap(manifest_url:, slug:)` creates or updates the draft. Inspect the current
  tool schema through `tools/list`; do not hand-build a legacy price book by default.
- Call `test_cap`. Record connection, fixture and real_delivery separately. Native
  OPTIONS/tools-list evidence is reachability, not generation; a fixture must finish
  successfully and match the output schema. A valid schema is not business-quality proof.
- When required checks pass, use existing owner publication authorization and call
  `submit_cap`. If publication/price approval is missing, present the concrete tested
  draft and ask only for the missing decision. Read back the effective version and
  `cap_status` after submission. Do not mark future pending changes as already active.

## Resume and manage existing Caps

Read [resume.md](references/resume.md) after an interruption, on an uncertain publish
response, or when updating an existing capability. Reconcile state before repeating a
mutation. Never use a saved local report as platform approval or a previous test of a
changed manifest. Review deliverable changes and owner scope; do not bypass the platform's
price notice or contract confirmation rules.

`delist_cap` stops new calls immediately while preserving the public page. `relist_cap`
retests a changed service address. Use these only when requested/authorized. Domain
verification releases frozen earnings; it is not required merely to list a Cap.
Use `get_earnings` and `request_payout` for developer income within the owner's scope;
only Cap income is withdrawable, not topped-up spending money.

Return a concise handoff: files changed, local preflight, deployment version/URL, Cap
slug and draft/live/pending state, tested version and evidence scope, real delivery and
actual charges if any, remaining blockers and the next action. Never print a key.
