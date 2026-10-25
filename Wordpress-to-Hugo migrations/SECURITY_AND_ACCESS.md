# Collaborative access and secret handling

## Work together at account boundaries

The owner chooses accounts, installs or approves local tools, signs into providers, creates credentials, and selects the final access policy. The agent explains the permission needed, where to create it, and where to store it. Confirm the account name, resource, role, and scope without asking for secret values.

For GitHub, prefer the owner's browser/device authentication with GitHub CLI or the agent platform's native GitHub connection. Grant access only to the intended repositories and actions. Never ask for a password, recovery code, PAT, SSH private key, or browser cookie in chat.

For Cloudflare, have the owner sign in directly and create scoped API tokens only when an API integration requires them. Use read-only permissions for inventory and analytics reads. Use narrowly scoped Pages/Workers/D1 write access only for a task that needs it. Use a separate token for automation instead of reusing a personal global token. Prefer the Cloudflare dashboard or supported Wrangler login flow. Verify the selected account before any remote write.

Use separate credentials for agent-operated API calls and Cloudflare automation. Prefer the coding agent's native Cloudflare connection or an owner-authenticated secure integration for the agent; if a scoped token is required, place it in the platform's credential store or a protected process environment that is not exposed in prompts, tool output, or logs. Create a different least-privilege token for CI/Cloudflare automation and store it only in the provider's secret manager. The human should verify both credential names, scopes, owners, and rotation locations without showing either value to the agent.

For WordPress.com/Jetpack, use the provider's official OAuth or API-console browser flow with the minimum read scope needed for stats. Do not ask the owner to paste an application password or bearer token.

For stats authentication, the agent should ask which identity provider the owner wants. Configure it through Cloudflare Access or the chosen platform's supported auth service. Keep the allow-list narrow, and test both permitted and denied identities. Google/Gmail is an optional choice, not a default requirement.

## Secret rules

Secrets include passwords, PATs, API tokens, OAuth client secrets, private keys, cookies, recovery codes, database exports, and private D1 backups.

- Never include a secret in chat, prompts, source control, PR descriptions, issue comments, screenshots, telemetry, or ordinary logs.
- Never place secrets in a committed `.env`, `.dev.vars`, JSON, YAML, shell script, Hugo config, or test fixture.
- Never put a secret in a command argument or shell history. Use a secure prompt, browser flow, credential manager, CI secret store, or provider secret command.
- Do not print, echo, serialize, or inspect a secret value to verify it. Check only whether it exists or let the provider confirm successful storage.
- Keep local secret files ignored by Git and verify `git status` before committing. If a secret is accidentally exposed, revoke/rotate it immediately, remove it from current files/history as appropriate, and assess provider logs.
- Keep raw WordPress backups and stats exports in a private local folder or approved encrypted storage. Do not attach them to PRs or send them to an AI service.
- Use separate credentials for interactive human access, local development, CI, and production automation. Grant each only the resources and operations it needs; set expiry/rotation and review owners.

The agent may use an already configured credential only through its authorized provider integration or secure local credential mechanism. It must not reveal the value or forward it to another agent. If a tool asks the human for a secret in plain text, stop and choose a secure flow.

## GitHub CI and Cloudflare automation

A basic Hugo build usually needs no deployment token when Cloudflare Pages is connected to GitHub through its native integration. Prefer that model: GitHub Actions runs validation; Cloudflare Pages builds PR previews and production from Git events.

If a private-repository preview wrapper reads pull-request metadata (for example, an optional Preview Date field), create a separate fine-grained GitHub token limited to that repository with pull-request read access. Put it in Cloudflare Pages **Preview** secrets only. Do not put it in Production, GitHub Actions output, a command argument, or a source file. The wrapper must not print it and must fail clearly if it is missing or the metadata is invalid. See [the filtered future preview guide](FUTURE_DATED_PREVIEWS.md).

If custom automation is required, have the owner add the credential using GitHub's Actions Secrets UI or the platform's secure secret manager. Reference the secret by name in workflow code. Avoid printing shell environment or enabling verbose traces. Scope a Pages deployment token to the single account/project and the minimum Pages permissions available. Never commit it or paste it into a workflow file.

For a stats Worker, use Wrangler's authenticated login for development and deployment. Put runtime API credentials into Worker secrets using the current documented Wrangler command or Cloudflare dashboard. Keep public configuration (account/site identifiers, hostnames, non-secret names) separate from credentials.

When handing off across AI products, pass resource names and secret-variable names only. Each product/user should authenticate independently. Never transfer a token through prompts or conversation history.

## Safe local backup handling

Use a private working copy. Keep the original archive unchanged. Exclude database dumps, uploads, raw stats exports, generated SQL, local auth files, and Wrangler state from Git. Inspect archives before extraction, extract into a dedicated directory, and reject path traversal or unexpected executables. Avoid printing rows containing names, emails, IP addresses, comment bodies, or credentials. Use aggregate reports for progress and redact examples.

Before any remote database import or schema change, confirm account/database identity and make a recoverable backup. Validate generated SQL before execution. Record date ranges and row counts, never secret or personal values, in the project notes.
