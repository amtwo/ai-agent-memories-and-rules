# WordPress-to-Hugo migration kit

This folder packages a reusable, agent-neutral workflow for moving a WordPress site to Hugo on Cloudflare. It works as a human-readable runbook on its own and can also be loaded as context by Codex, Claude, Gemini, Grok, or another coding agent.

## Start here

1. Read [the migration playbook](MIGRATION_PLAYBOOK.md) and [security and access guide](SECURITY_AND_ACCESS.md).
2. Copy [the project profile](templates/project-profile.md) into the user's private project notes. Fill in non-secret choices and resource names; keep credentials in the provider vaults.
3. Run the four milestones in order. Do not advance while a milestone's exit conditions remain unmet.
4. Keep the [go-live checklist](templates/go-live-checklist.md) current from the first beta deployment.
5. After import, use the [Migration Cleanup and Polish skill](skills/Migration-Cleanup-and-Polish/SKILL.md) for the repair pass and Markdown conversion pass.
6. For an agent without skill discovery, provide [the agent-neutral entry prompt](adapters/AGENT-NEUTRAL-PROMPT.md) and this folder as context.

## Package layout

- `MIGRATION_PLAYBOOK.md`: the four milestones, decisions, exit criteria, and operating rules.
- `SECURITY_AND_ACCESS.md`: collaborative credential setup and secret-handling requirements.
- `skills/Migration-Cleanup-and-Polish/SKILL.md`: reusable two-pass content review with one PR per page or post.
- `templates/project-profile.md`: private, non-secret project facts and decisions.
- `templates/go-live-checklist.md`: cutover, verification, and recovery checklist.
- `adapters/AGENT-NEUTRAL-PROMPT.md`: short instructions for loading this package in different AI coding products.

## Agent portability

The canonical instructions are plain Markdown and do not require a vendor-specific plugin, tool schema, or agent runtime. If a product supports skills, load the cleanup skill and keep the playbook available as project context. If it supports repository instruction files, add only a short pointer to this folder. If neither is available, paste the entry prompt and relevant documents into the session.

Adapters should point to these canonical files instead of copying the entire workflow into multiple platform-specific files. Keep credentials and private WordPress exports out of this public package.
