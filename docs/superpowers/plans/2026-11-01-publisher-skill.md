# Qumge publisher skill split and readiness plan

Goal: preserve the existing qumge consumer installation, add a self-contained qumge-publish skill in the same repository, and keep both using the existing hosted MCP.

Approved design: extract the current developer workflow rather than invent a second publishing backend. Add offline readiness and resumable reporting, reuse current managed-v2 templates and provider validation examples, and align MCP documentation.

- [x] Verify installer discovery with a root SKILL.md; document validated consumer and publisher install commands.
- [x] Write offline preflight acceptance cases first: valid managed v2, missing fields/private status, malformed JSON, credential leakage, multi-Cap selection, no network, and unchanged manifest/report-destination protection.
- [x] Implement self-contained publisher skill, local preflight/report helper and managed-v2 example. Keep detailed integration guidance progressive and preserve existing authorization; no generation, deployment or live publication during validation.
- [x] Narrow root qumge skill to consumers, retain a publisher handoff and legacy reference URLs, and declare both skills in marketplace metadata.
- [x] Sync MCP README, HTTP reference and both tool-drift checks to current live tools/schema, distinguishing native MCP from managed complete-result execution.
- [x] Validate bundled resources, actual installation into isolated temporary agent directories, scenarios, contract examples, tool drift and independent review. Release instruction: commit/push only the authorized repository changes, then remove clean worktrees immediately after integration and push.

Boundaries: no new repository or MCP service; no public Cap submission, real generation, production wallet changes or user-global skill installation. A local report is preflight evidence only, not deployment, platform approval or real-delivery proof.
