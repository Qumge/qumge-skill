# Resume from observed state

Keep a short local receipt outside public web roots. Record only non-secret facts: project
files changed; local manifest file fingerprint; chosen slug; deployment revision and public
manifest URL; actual draft/current/pending version; platform checks and the version tested;
real-delivery evidence if authorized; blockers and next action. Do not store private inputs,
keys or treat a receipt as permission. The preflight report supplies only its local subset.

| Last completed stage | Next observation before acting |
|---|---|
| Local preflight | Re-run on current bytes using a new report filename; inspect findings and not_checked. |
| Deployment | Verify the actual running revision, public manifest and authentication. |
| publish_cap response uncertain | Read list_caps and cap_status for the same slug before retrying or creating another Cap. |
| Draft exists | Compare its current contract/profile with the deployed manifest; update that draft within the approved scope. |
| Platform self-test passed | Check that the manifest/version still matches; distinguish fixture and real_delivery. |
| submit_cap response uncertain | Read cap_status/get_cap; do not report live from the submission attempt alone. |
| Cap already live | Read effective and pending contracts, price and operation docs; never overwrite history or assume a pending change is active. |

Changed local bytes invalidate that local report. Changed public contracts invalidate old
version-specific test evidence. The local raw-file SHA-256 is not the platform contract digest.
Ask only for missing pricing/publication/deployment scope, not approvals already given.

For a deliverable migration, inspect migrate_cap_contract's current tool schema and platform
guide; its prepare/test/activate/status flow is separate from an ordinary draft publish.
Candidate tests are non-generating fixtures, not paid delivery. Preserve price-notice rules,
current contracts on existing orders and any required new buyer confirmation. Metadata-only
repair_review is only for an already activated unchanged contract and is not a way to skip
migration validation. If another execution already finished the action, verify and stop.

A failed or unknown generation is never retried blindly. Respect the provider's actual
idempotency/recovery behavior and the platform job state. For 401, resolve authentication;
for 402, report balance/limit and top-up link without retrying; for 429, back off rather than
looping. Never call a billable operation merely to prove publication state.
