# WordPress-to-Hugo migration kit

This folder packages a reusable, agent-neutral workflow for moving a WordPress site to Hugo on Cloudflare. It works as a human-readable runbook on its own and can also be loaded as context by a coding agent.

## Start here

1. Read [the migration playbook](MIGRATION_PLAYBOOK.md) and [security and access guide](SECURITY_AND_ACCESS.md).
2. Copy [the project profile](templates/project-profile.md) into the user's private project notes. Fill in non-secret choices and resource names; keep credentials in provider vaults.
3. Start with a plain-language introduction. Assume the owner is new to the migration, explain the milestones and what stays online, then adapt the pace and technical depth to their comfort level.
4. Inspect the available machine and report a checklist of required tools and access methods with `✅` and `⏹️`. Offer supported secure installation where possible; otherwise guide the owner through official setup.
5. Run the four milestones in order. Keep the [go-live checklist](templates/go-live-checklist.md) current from the first beta deployment.
6. After import, use the [Migration Cleanup and Polish skill](skills/Migration-Cleanup-and-Polish/SKILL.md) for the repair pass and Markdown conversion pass.
7. For an agent without skill discovery, provide [the agent-neutral entry prompt](adapters/AGENT-NEUTRAL-PROMPT.md) and this folder as context.

## Package layout

- `MIGRATION_PLAYBOOK.md`: the four milestones, decisions, exit criteria, and operating rules.
- `FUTURE_DATED_PREVIEWS.md`: filtered PR/local previews and scheduled production builds for future-dated content.
- `templates/BUILD_WRAPPER_CONTRACT.md`: site-specific build-wrapper behavior and validation contract.
- `SECURITY_AND_ACCESS.md`: collaborative credential setup and secret-handling requirements.
- `skills/Migration-Cleanup-and-Polish/SKILL.md`: reusable two-pass content review with one PR per page or post by default.
- `templates/project-profile.md`: private, non-secret project facts and decisions.
- `templates/go-live-checklist.md`: cutover, verification, deferred launch tasks, and recovery checklist.
- `adapters/AGENT-NEUTRAL-PROMPT.md`: onboarding and loading instructions for different AI coding products.

## Cleanup review workflow options

The default workflow stages a complete human-selected batch of Draft PRs, then adversarially reviews the batch before marking its PRs ready. Where the agent environment supports isolated subagents, the owner may choose an alternative: request an independent adversarial review as soon as each Draft PR is created. The primary agent still owns each change, incorporates review findings, verifies the exact preview, and stages the batch for human review. Either workflow keeps the same one-page-per-PR default and validation requirements.

## Agent portability

The canonical instructions are plain Markdown and do not require a vendor-specific plugin, tool schema, or agent runtime. If a product supports skills, load the cleanup skill and keep the playbook available as project context. If it supports repository instruction files, add only a short pointer to this folder. If neither is available, paste the entry prompt and relevant documents into the session.

Adapters should point to these canonical files instead of copying the entire workflow into multiple platform-specific files. Keep credentials and private WordPress exports out of this public package.
