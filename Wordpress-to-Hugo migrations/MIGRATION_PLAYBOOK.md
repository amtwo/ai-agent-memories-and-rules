# WordPress-to-Hugo migration playbook

## Purpose and operating agreement

Guide one site from discovery through a production cutover. Work with the site owner at account boundaries, data decisions, and launch decisions. The agent should do the research, prepare reviewable changes, maintain checklists, and report evidence. The human signs into accounts and providers directly.

Use a separate GitHub repository for the public Hugo site and, where useful, a separate private repository for the stats application. Use isolated branches or worktrees for implementation. Preserve user changes and existing public URLs. Do not point production DNS to the new site during the beta milestones.

Before work, read the target repository's `AGENTS.md`, contribution guide, maintenance guide, and existing go-live notes. Establish a local and deployed baseline, including existing dirty files, build/runtime versions, the active host, and the latest deployment commit. Keep pre-existing failures distinct from regressions.

Maintain these artifacts from day one:

- A non-secret project profile based on [the template](templates/project-profile.md).
- A living go-live checklist based on [the template](templates/go-live-checklist.md).
- A migration inventory: WordPress URL, content type, current status, intended Hugo URL, media dependencies, import status, review status, and exceptions. Do not put personal data into a public inventory.
- A decision log for retired plugins, unavailable content, redirect choices, analytics, comments, newsletters, and other features.

Do not invent credentials, resource IDs, or access. Verify current Cloudflare, GitHub, Hugo, and hosting-provider instructions from official documentation before relying on version-sensitive details.

## Milestone 1 — Accounts, delivery pipeline, beta site, and stats foundation

### Collaborate with the owner

Agree on:

- The GitHub account or organization that will own the site repository and who can approve and merge changes.
- The Cloudflare account and zone that will host the beta site.
- The beta hostname, in the form `beta.<domain>.<tld>`, and confirmation that it is safe to point that hostname to the new site.
- Whether the stats dashboard is wanted, which Cloudflare account/analytics source it will use, the D1 region or data choices when applicable, and which people need access.
- The stats login provider. Google sign-in through Cloudflare Access is one option; support another provider if the owner prefers it and current Cloudflare Access supports it.
- The local OS and preferred setup method for Git, GitHub CLI, Hugo, Node.js/npm, Python, and Wrangler. Install only tools needed by the selected architecture.

The human authenticates in browser/device flows and confirms the correct account. Never ask the human to paste a password, recovery code, OAuth client secret, PAT, API token, cookie, or private key into chat.

### Build the site delivery path

1. Create the GitHub repository with the owner and intended visibility. Configure protected/default branch expectations and grant the minimum collaborators.
2. Scaffold a minimal Hugo site. Pin Hugo in a repository version file such as `.hugo-version`; have CI read that file instead of duplicating the version.
3. Add a pull-request workflow that checks out the repository, installs the pinned Hugo version, builds with warnings and path diagnostics treated as failures, and confirms a generated Hugo marker. Run it on pull requests and the production branch.
4. Connect the repository to the Cloudflare Pages project. Set its production branch, Hugo build command, output directory, and runtime version. Configure Preview and Production environment values separately and verify both use the intended Hugo release.
5. Enable branch/PR previews. A preview must have a Pages-owned hostname and show the source branch and commit. Verify the preview deployment check is attached to the PR.
6. Add only the required `beta.<domain>.<tld>` custom hostname and DNS record. Confirm its DNS target, TLS status, and Pages association. Keep the apex and `www` production routing as-is.
7. Build and publish a hello-world page on beta. Verify the exact deployment branch, commit SHA, status, hostname, HTTPS certificate, generator marker, homepage, 404, sitemap, and feed. Inspect links and assets in a browser.

A green GitHub build is not proof that Cloudflare deployed the same commit. Record the Pages deployment ID, environment, branch, SHA, URL, and status.

### Build the stats foundation

Offer the stats app as a separate, optional service. Keep it operationally and logically separate from the public Hugo site. A common architecture is a Cloudflare Worker serving a dashboard and JSON API, with D1 for historical aggregates and a scheduled collector for ongoing Cloudflare analytics. Preserve metric names and sources as separate series; WordPress/Jetpack visitors and Cloudflare visits do not mean the same thing.

1. Create a separate repository or clearly isolated app directory, D1 database, migration history, Worker, and deployment configuration. Keep the D1 identifier and non-secret analytics identifiers in the config; put credentials in Worker secrets.
2. Build a small dashboard/API and a health endpoint. Apply schema migrations before importing data.
3. Protect all Worker URLs and custom hostnames with Cloudflare Access. Configure the owner's chosen identity provider and a narrow allow policy. Google/Gmail accounts can be used without assuming Google Workspace. Test an allowed identity and a denied identity.
4. Keep the Cloudflare analytics collection credential read-only for the required analytics scope. Store it as a Worker secret. Configure the collector schedule and verify logs and D1 rows.
5. Deploy, test the custom stats hostname, authentication, health endpoint, collector, and D1 query. Export/backup the empty initial D1 before any destructive schema change.

**Milestone 1 exit:** A hello-world Hugo site works over HTTPS on beta; PR CI and exact Pages previews work; production DNS remains unchanged. If stats were selected, the protected dashboard, database schema, collector, and access policy work. The go-live checklist has ownership, DNS, recovery, and deployment facts filled in.

## Milestone 2 — Secure backup, import, and optional Jetpack history

### Find or obtain the source backup

Ask the owner to point to a local backup folder or archive. A useful migration backup normally includes a WordPress database export and the uploads/media directory. Preserve the original files unchanged and work from a copy.

If no local backup exists:

1. Inspect public DNS records with read-only lookups to identify nameservers, CDN/proxy clues, and likely hosting boundaries. DNS clues are not proof of the origin host; ask the owner to confirm the provider and account.
2. Ask whether the site is managed WordPress hosting or self-managed. For managed hosting, identify the exact provider from the human and consult its current official backup/export procedure. Guide the owner through their own authenticated dashboard or support process; do not request their login.
3. For self-managed WordPress, assume the owner can administer it. Ask them to create a database and uploads backup using their established process, then provide the resulting local path.
4. If a full backup cannot be obtained, discuss practical alternatives with the owner: host support export, WordPress export plus media fetch, or a scoped public-site crawl. Explain what each option loses. Get the owner's decision before scraping. Check applicable access terms, crawl limits, robots policy, copyright, and privacy obligations; keep the crawl rate low and identify unavailable content. A scrape is not equivalent to a database-plus-uploads backup.

Never upload the database or private media archive to a third-party AI service. Parse locally where possible. Treat the database, exports, comments, and logs as sensitive. Suppress personal fields and avoid copying private content into chat or PR descriptions.

### Inventory, convert, and reconcile

1. Inventory posts, pages, dates, slugs, statuses, categories, tags, canonical URLs, redirects, featured media, inline media, comments, and plugin/theme features.
2. Establish URL rules before importing. Preserve all valid public URLs unless the owner explicitly approves a change. Generate redirect candidates only from confirmed mappings.
3. Import from a copy into Hugo content and local media. Preserve titles, dates/time zones, excerpts/descriptions, authors, taxonomies, featured images, WordPress IDs where useful, and canonical routes.
4. Keep drafts and private posts out of production unless the owner asks to migrate them. Retain future dates; do not change publication dates to make content appear in previews.
5. Audit plugin behavior: forms, search, comments, short links, redirects, galleries, downloads, newsletters, social embeds, SEO metadata, schema, and event/calendar features. Classify each as migrate, replace, retire, or owner decision.
6. Check importer reports and reconcile counts. Flag missing media, unknown shortcodes, unsupported blocks, retired URLs, duplicate routes, and undecided features. Do not silently drop them.
7. Replace Jetpack stats with a standalone protected stats site only if the owner wants one. Explain the separate app, identity provider, D1 storage, and operating costs/limits before provisioning.

### Optional Jetpack/WordPress stats import

Ask explicitly whether the owner wants historical Jetpack stats imported. A WordPress database backup usually does not contain this history; access may require a separately authenticated WordPress.com/Jetpack API export.

If yes, help the owner authenticate through the provider's official browser/API flow. Request only the read permission needed. Keep tokens in a credential manager or provider-managed secret store, never in chat, exports, source files, logs, or shell history. Export the available daily metrics and native week/month/year aggregates; don't calculate longer-term unique visitors by summing daily uniques. Preserve actual returned dates, time zones, omissions, and unavailable reports.

Stage raw exports and generated SQL in a private ignored directory. Validate coverage, row counts, truncation, date gaps, and a sample against the source before writing to D1. Estimate writes and split imports to remain under the current D1 limits. Take a D1 backup before import. Use idempotent upserts where possible, and record exact imported date ranges. Keep Jetpack and Cloudflare series distinct and label non-equivalent metrics clearly.

If the owner declines, lacks access, or an endpoint is unavailable, record that choice or limitation. Do not imply stats were imported.

**Milestone 2 exit:** The content/media inventory reconciles to the source backup or documented fallback scope; imported site content renders on beta; public URLs and redirect mappings are accounted for; plugin and feature decisions are recorded. If requested, validated historical stats exist in D1 and can be viewed in the protected standalone dashboard.

## Milestone 3 — Repair, review, and launch readiness

Use [Migration Cleanup and Polish](skills/Migration-Cleanup-and-Polish/SKILL.md). Ask the owner how many posts/pages belong in each batch. Complete its repair pass before its Markdown conversion pass. Keep beta available throughout.

Review pages in a browser at desktop and narrow sizes, with light and dark themes where available. Verify navigation, images, captions, code, embeds, downloads, search, forms, comments, feeds, canonical URLs, metadata, redirects, accessibility, and performance. Compare rendered behavior with the WordPress source where useful. A successful static build does not prove content equivalence.

Use a living go-live checklist from the first milestone. It should capture:

- Exact current and intended production branch, commit, Pages project, build settings, hostnames, and Hugo runtime.
- Pre-cutover DNS/origin records, proxy/TLS settings, Pages custom-domain setup, owner access, and private recovery record location.
- Content/route, redirect, feed, sitemap, image, comments, stats, and search verification.
- A cutover sequence, observation window, rollback decision, and recovery steps to restore the prior site.
- A post-cutover verification record showing actual DNS, certificate, deployment SHA, served marker, core routes, and changed output.

Never put DNS credentials, private origin passwords, tokens, or full zone exports in Git. Keep a private, access-controlled record with the previous origin and each changed record's name, type, target, TTL, and proxy state. Keep the old WordPress site and backup available until the owner accepts the new site.

**Milestone 3 exit:** the site is visually and functionally reviewed on beta; all known critical breakage is fixed; remaining exceptions have owner decisions; the go-live checklist is complete enough to execute and recover autonomously. The human makes the final production go/no-go decision.

## Milestone 4 — Final HTML and Markdown hygiene

After pages are repaired, run the skill's second pass over every post and page. Convert verbose HTML to Markdown only when Hugo's rendered output preserves meaning, links, attributes that matter, nesting, accessibility, and visual intent. Keep HTML for semantics/attributes Markdown cannot represent reliably, custom components, forms, embeds, and complex figures. Do not combine a repair and a syntax cleanup in one PR.

Complete the final content inventory and route/redirect audit. Run the project's documented lint/build and inspect affected generated output. Update maintenance documentation for each new recurring integration, generated artifact, migration tool, or deploy setting.

**Milestone 4 exit:** every in-scope page has a recorded result for both passes; unresolved exceptions are explicit; all PRs are merged and verified; the full site passes local and CI builds; the owner-approved go-live checklist has current evidence.

## Future-dated content and previews

Preserve each post's intended `date` and draft status. Hugo normally excludes future-dated content from ordinary production builds. For local review, use the project's Hugo version and an explicit future-content preview option such as `hugo server --buildDrafts --buildFuture`; confirm the exact flags with the installed Hugo help. Keep production build commands free of the future-content flag. For a Cloudflare branch preview, confirm whether the current Pages configuration can use a Preview-specific command. If not, use a documented preview-only branch build rule or local preview. Never make a future post appear by changing its date, and verify it remains absent from production until its intended date.

## General merge, deployment, and recovery rules

- Pull requests are the review unit. Keep changes scoped and reproducible.
- Do not merge on the owner's behalf unless the owner explicitly authorizes that PR's merge. A general request to build the migration does not waive review.
- Before calling a deploy complete, verify the intended provider, environment, branch, exact commit SHA, deployment status, hostname, TLS, served runtime marker, and changed output.
- For a failed release, prefer the provider's artifact rollback for immediate recovery, then make a reviewed source correction. DNS/origin failures require the captured routing recovery procedure; a deployment rollback does not restore DNS.
- Repeat required health checks at the end and compare against the recorded baseline. Report blocked or unverified checks plainly.
