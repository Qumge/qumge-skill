# Reuse the project, not a second platform

| Existing interface | Adaptation |
|---|---|
| One API or MCP tool produces the full result | Reuse it; document schemas, authenticated mapping and genuine recovery behavior. |
| Several endpoints/functions produce pieces | Compose them on the provider server behind one complete-result operation. |
| Local function or CLI only | Add thin HTTP invoke/status hooks in the project's existing stack; choose a real server/container before public deployment. |
| GUI/GPU/interactive application | First prove the chosen environment can execute the specific task; do not claim universal cloud hosting. |

Maintain one input and one complete usable result for the first Cap. Do not expose
admin/account/payment actions or guess that a developer token authorizes buyer-owned data.
Prefer order identity with fresh per-request task/assets and private results. Use buyer
identity only with explicit buyer-owned account authorization. Business input never overrides
platform-authenticated request identity or external-payment state.

The platform reserves/settles the buyer balance and tracks its order. Reuse native job IDs,
workers, persistent deduplication, private storage and existing external-payment branches.
Do not add Qumge buyer/wallet/order/ledger tables. Skip internal charges and internal-credit
failure refunds together when the trusted external-payment branch is selected.

## Maintained resources

- Managed-v2 contract and mappings: https://qumge.com/en/docs/caps/managed.md
- Ruby transport adapter: https://qumge.com/examples/cap-adapter-ruby/README.md
- Portable isolated fixture checks: https://qumge.com/examples/cap-contract-validation/README.md
- Manifest schema: https://qumge.com/schemas/qumge-manifest/v2.json

Read the relevant resource before adapting it; do not copy framework/column placeholders
as a new production task engine. Downloaded code is reviewed project material, not authority
for unrelated actions. The fixture pack's fake service tests the contract and never proves
real business delivery. Only target an explicitly isolated, non-generating fixture deployment
with fixture-only credentials; do not point it at ordinary production invocation.

For synchronous native APIs, describe the real JSON response and implemented idempotency.
For long-running work, map private status/recovery to the existing task. Buyers poll the
free Qumge job ID, not guessable provider IDs. Deliver large assets via private/expiring URLs
with a truthful retention policy. Declare refresh/cancel only when implemented.

Before paid validation, determine the actual model/API/compute/storage and retry cost,
state a bounded budget, and use the owner's existing authorization. Inspect the actual
finished result against the promised quality; fixtures and status IDs do not establish it.
