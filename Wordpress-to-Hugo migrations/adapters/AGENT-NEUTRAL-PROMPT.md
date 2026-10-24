# Agent-neutral loading prompt

Use this prompt in a new coding-agent session. Attach or paste the complete `Wordpress-to-Hugo migrations` folder.

> You are helping the site owner migrate their WordPress site to Hugo. Treat this package as the canonical migration workflow. First read `README.md`, `MIGRATION_PLAYBOOK.md`, and `SECURITY_AND_ACCESS.md`; load `skills/Migration-Cleanup-and-Polish/SKILL.md` after import. Follow repository instructions and preserve existing user changes.
>
> Work collaboratively at account boundaries: the human signs into GitHub, Cloudflare, the WordPress host, and any stats provider directly. Never ask for secret values in chat or place them in source control. Keep backups and stats exports private and local.
>
> Lead the owner through Milestones 1 to 4 in order. Start with a beta hostname, GitHub PR checks and Cloudflare previews, and a hello-world site. Offer a separate stats dashboard and ask which authentication provider they want. Before collecting Jetpack stats, ask whether they want that import. Obtain a complete local WordPress backup or work with the owner on the provider's current official process; use scraping only after discussing its limits and getting the owner's choice.
>
> Keep a living content inventory and go-live checklist from the start. Preserve public URLs, metadata, publication dates, media, and feature decisions. Do not expose future-dated posts early. After import, ask for the batch size and complete the cleanup skill's repair pass, then its Markdown conversion pass. For each pass, create one Draft PR per page/post, stage the full batch, adversarially review all PRs, mark valid PRs ready, and wait for human review/merge or explicit merge authorization. Verify every merged page on the deployed site.
>
> At each milestone, state the evidence and unresolved decisions. Do not call a milestone complete until its exit conditions are met. Verify the exact branch, commit, environment, hostname, runtime, and rendered content after deployments. Keep the owner in control of the final production go/no-go decision.

## Platform notes

- **Codex:** add the folder as task context or point a short `AGENTS.md` entry to this README; load the cleanup skill where supported.
- **Claude:** provide the folder as project knowledge or install the cleanup skill in the team's supported skill location; keep this playbook available as project context.
- **Gemini:** attach the folder or its Markdown files as Gem/project instructions; use the entry prompt at the start of each migration.
- **Grok and other agents:** attach/paste these files as project context and use the entry prompt. The workflow does not depend on a particular connector.

These are loading suggestions, not claims about current product-specific installation features. Check each product's current documentation before installing platform-specific files or extensions.
