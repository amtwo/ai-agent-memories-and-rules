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

## Loading this package in any agent

- If the product supports reusable skills, install the cleanup skill using that product's documented skill mechanism.
- If it supports project or repository instructions, point a short instruction file to this folder's README and keep the playbook available as project context.
- If it supports file attachments, attach the folder or its Markdown files and use the entry prompt above.
- If it supports only a plain chat, paste the entry prompt and provide the playbook, security guide, and cleanup skill as context.

Keep the canonical workflow in these Markdown files. Do not create platform-specific copies unless the owner needs them, and verify current product instructions before configuring an integration.
