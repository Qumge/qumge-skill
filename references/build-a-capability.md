# Developer publishing moved to qumge-publish

This legacy reference URL is retained for existing installations. The developer workflow
now lives in the self-contained qumge-publish skill in the same repository:
https://github.com/Qumge/qumge-skill/tree/main/skills/qumge-publish

Install with `npx skills add Qumge/qumge-skill --full-depth --skill qumge-publish`.
The original qumge skill remains the consumer entry. Both connect to https://qumge.com/mcp.

Read its SKILL.md and references/adaptation.md for current managed manifest v2, native
job reuse, isolated fixtures and complete-result delivery. Do not reuse historical v1,
per-response, shared-user or usage-reporting examples as the default new-Cap integration.
The maintained schema is https://qumge.com/schemas/qumge-manifest/v2.json.
