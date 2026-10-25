# WordPress-to-Hugo migration playbook

## Purpose and operating agreement

Guide one site from discovery through a production cutover. Work with the site owner at account boundaries, data decisions, and launch decisions. The agent should do the research, prepare reviewable changes, maintain checklists, and report evidence. The human signs into accounts and providers directly.

Use a separate GitHub repository for the public Hugo site and, where useful, a separate private repository for the stats application. The Hugo site starts as a new site on beta while the existing WordPress site remains online and serves the production hostname. Use isolated branches or worktrees for implementation. Preserve user changes and existing public URLs. Do not point production DNS to the new site during the beta milestones.

Before work, read the target repository's `AGENTS.md`, contribution guide, maintenance guide, and existing go-live notes. Establish a local and deployed baseline, including existing dirty files, build/runtime versions, the active host, and the latest deployment commit. Keep pre-existing failures distinct from regressions.

Maintain these artifacts from day one:

- A non-secret project profile based on [the template](templates/project-profile.md).
- A living go-live checklist based on [the template](templates/go-live-checklist.md).
- A migration inventory copied from [the CSV template](templates/content-inventory.csv): WordPress URL, content type, current status, intended Hugo URL, media dependencies, import status, review status, and exceptions. Keep the filled file private because it can contain unpublished titles and URLs; do not commit personal data.
- A decision log copied from [the template](templates/decision-log.md) for retired plugins, unavailable content, redirect choices, analytics, comments, newsletters, and other features.
- A cleanup batch tracker copied from [the template](templates/cleanup-batch-tracker.csv) to record each pass, PR, owner decision, merge, and verification.

By default, the cleanup scope is every migrated post and page intended to remain on the Hugo site. Build a complete item count from the content inventory. If the owner excludes an item, record that decision and its URL; do not silently skip it.

Do not invent credentials, resource IDs, or access. Verify current Cloudflare, GitHub, Hugo, and hosting-provider instructions from official documentation before relying on version-sensitive details.

## Milestone 1 — Accounts, delivery pipeline, beta site, and stats foundation

### Collaborate with the owner

Agree on:

- The GitHub account or organization that will own the site repository and who can approve and merge changes.
- The Cloudflare account and zone that will host the beta site.
- The beta hostname, in the form `beta.<domain>.<tld>`, and confirmation that it is safe to point that hostname to the new site.
- Whether the stats dashboard is wanted, which Cloudflare account/analytics source it will use, the D1 region or data choices when applicable, and which people need access.
- The stats login provider. Google sign-in through Cloudflare Access is one option; support another provider if the owner prefers it and current Cloudflare Access supports it.
- The local OS, the owner's comfort with Git/command-line tools/hosting, and preferred setup method for Git, a GitHub access method, Hugo, Node.js/npm, Python, and Wrangler when needed. Inspect prerequisites before setup, offer supported installation when possible, and guide the owner through official setup otherwise. Docker is optional and should be installed only if the selected architecture needs it.
- Whether to preserve the WordPress theme or redesign the site. By default, inspect the theme in the archive and plan to reproduce it. Explain the time/effort difference: faithful reproduction is a higher-effort Milestone 2 task; a redesign gets a modest visual baseline in Milestone 2 and collaborative theme selection/implementation in Milestone 3.

The human authenticates in browser/device flows and confirms the correct account. Never ask the human to paste a password, recovery code, OAuth client secret, PAT, API token, cookie, or private key into chat. Before installing anything, inspect the machine and provide a checklist of only the tools the selected design needs, marking each ready or missing. Offer supported installation flows when available; otherwise guide the owner through official installation instructions. Explain why each tool is needed and let the owner choose the pace.

### Build the site delivery path

1. Create the GitHub repository with the owner and intended visibility. Configure protected/default branch expectations and grant the minimum collaborators.
2. Scaffold a minimal Hugo site. Pin Hugo in a repository version file such as `.hugo-version`; have CI read that file instead of duplicating the version.
3. Add a pull-request workflow that checks out the repository, installs the pinned Hugo version, builds with warnings and path diagnostics treated as failures, and confirms a generated Hugo marker. Run it on pull requests and the production branch. If future content needs preview coverage, invoke the filtered wrapper in preview mode on PRs and use the normal production path on the production branch.
4. Connect the repository to the Cloudflare Pages project. Set its production branch, build wrapper command, output directory, and runtime version. Configure Preview and Production values separately and verify both use the intended Hugo release. A wrapper can use Pages branch context to include only normally published content plus explicit preview opt-ins on non-production branches, while Production uses Hugo's normal draft/future exclusions. For a private repository whose wrapper reads a PR field such as `Preview Date`, store a separate fine-grained GitHub token with pull-request read access in Pages Preview only.
5. Enable branch/PR previews. A preview must have a Pages-owned hostname and show the source branch and commit. Verify the preview deployment check is attached to the PR.
6. Add only the required `beta.<domain>.<tld>` custom hostname and DNS record. Confirm its DNS target, TLS status, and Pages association. Keep the apex and `www` production routing as-is.
7. Build and publish a hello-world page on beta. Verify the exact deployment branch, commit SHA, status, hostname, HTTPS certificate, generator marker, homepage, 404, sitemap, and feed. Inspect links and assets in a browser.

Treat beta and branch previews as public unless access protection is verified. Do not publish sensitive or private content there. Use noindex controls where appropriate, but do not treat noindex as access control. If the preview includes confidential material, protect the hostname with an authenticated access policy and test it before import.

A green GitHub build is not proof that Cloudflare deployed the same commit. Record the Pages deployment ID, environment, branch, SHA, URL, and status.

### Build the stats foundation

Offer the stats app as a separate, optional service. Keep it operationally and logically separate from the public Hugo site. A common architecture is a Cloudflare Worker serving a dashboard and JSON API, with D1 for historical aggregates and a scheduled collector for ongoing Cloudflare analytics. Preserve metric names and sources as separate series; WordPress/Jetpack visitors and Cloudflare visits do not mean the same thing.

1. Create a separate repository or clearly isolated app directory, D1 database, migration history, Worker, and deployment configuration. Keep the D1 identifier and non-secret analytics identifiers in the config; put credentials in Worker secrets.
2. Build a small dashboard/API and a health endpoint. Apply schema migrations before importing data.
3. Explain why the stats dashboard needs authentication: analytics may reveal sensitive traffic and behavior, so the dashboard and API should not be public. Ask the owner to choose an identity provider, offer common options such as Google, and verify current provider documentation and compatibility. Configure Cloudflare Access or the selected provider's supported auth service with a narrow allow policy. Test an allowed identity and a denied identity.
4. Keep the Cloudflare analytics collection credential read-only for the required analytics scope. Store it as a Worker secret. Configure the collector schedule and verify logs and D1 rows.
5. Deploy, test the custom stats hostname, authentication, health endpoint, collector, and D1 query. Export/backup the empty initial D1 before any destructive schema change.

**Milestone 1 exit:** A hello-world Hugo site using the LCARS theme works over HTTPS on beta; PR CI and exact Pages previews work; production DNS remains unchanged. If stats were selected, the protected dashboard, database schema, collector, and access policy work. The go-live checklist has ownership, DNS, recovery, and deployment facts filled in.

## Milestone 2 — Secure backup, import, and optional Jetpack history

### Find or obtain the source backup

Ask the owner to point to a local backup folder or archive. A useful migration backup normally includes a WordPress database export and the uploads/media directory. Preserve the original files unchanged and work from a copy.

If no local backup exists:

1. Inspect public DNS records with read-only lookups to identify nameservers, CDN/proxy clues, and likely hosting boundaries. DNS clues are not proof of the origin host; ask the owner to confirm the provider and account.
2. Ask whether the site is managed WordPress hosting or self-managed. For managed hosting, identify the exact provider from the human and consult its current official backup/export procedure. Guide the owner through their own authenticated dashboard or support process; do not request their login.
3. For self-managed WordPress, assume the owner can administer it. Ask them to create a database and uploads backup using their established process, then provide the resulting local path.
4. If a full backup cannot be obtained, discuss practical alternatives with the owner: host support export, WordPress export plus media fetch, or a scoped public-site crawl. Explain what each option loses. Get the owner's decision before scraping. Check applicable access terms, crawl limits, robots policy, copyright, and privacy obligations; keep the crawl rate low and identify unavailable content. A scrape is not equivalent to a database-plus-uploads backup.

Treat the database, exports, comments, and logs as sensitive. Never upload a raw backup or private media archive to an AI service. Before a remote coding agent reads post or page content, explain where processing occurs and get the owner's approval; without approval, keep processing local and share only redacted excerpts or aggregate reports. Suppress personal fields and avoid copying private content into chat or PR descriptions.

### Inventory, convert, and reconcile

1. Inventory posts, pages, dates, slugs, statuses, categories, tags, canonical URLs, redirects, featured media, inline media, comments, and plugin/theme features. Start with the private CSV template. If the owner has a WordPress eXtended RSS (WXR) `.xml` or `.xml.gz` export, the optional [local metadata helper](tools/inventory_wxr.py) can produce a first-pass inventory: `python tools/inventory_wxr.py /private/path/export.xml.gz /private/path/content-inventory.csv`. It uses Python's standard library, reads the export locally, and omits post bodies, comment text, and author names/emails. Its output still contains potentially sensitive titles, URLs, and media paths: store it outside the repository or in a verified ignored private directory, never commit or upload it. It supports WXR metadata only; it does not inventory a database-plus-uploads backup, verify completeness, fetch media, or import content. Reconcile its rows against the full backup and inspect media separately.
2. Establish URL rules before importing. Preserve all valid public URLs unless the owner explicitly approves a change. Generate redirect candidates only from confirmed mappings.
3. Import from a copy into Hugo content and local media. Preserve titles, dates/time zones, excerpts/descriptions, authors, taxonomies, featured images, WordPress IDs where useful, and canonical routes.
4. Keep drafts and private posts out of production unless the owner asks to migrate them. Retain future dates; do not change publication dates to make content appear in previews.

By default, inspect the WordPress theme and assets in the archive and plan to reproduce the existing theme. If the owner wants to keep it, make faithful reproduction a substantial Milestone 2 work item, within technical and practical limits. If the owner wants a redesign, build only a modest visual baseline in Milestone 2 and defer detailed theme selection and implementation to a collaborative Milestone 3 effort. Record the choice and any licensing or asset constraints.
5. Audit plugin and theme behavior. For each feature, choose migrate, replace, retire, or owner decision. Select a comments provider early; recommend Giscus by default, or consult current Hugo documentation and provider documentation for alternatives that fit the owner's needs. By default, render historical comments as plain-text records immediately above the active comments embed, preserving useful date/author context while excluding spam and private commenter contact data. Assume direct import into the new comments provider is unavailable unless the owner asks for research; then investigate documented import options and decide with the owner. For newsletters and notifications, recommend RSS as the default. If the owner wants email notifications, use a third-party CRM designed for subscriber data and spam/privacy compliance; do not build a bespoke system that stores email addresses. Migrate existing subscriptions only with owner consent and verified subscriber permissions, and never send a test broadcast to real subscribers. Confirm search excludes drafts/future posts, forms have a chosen secure backend, embeds and media remain usable, SEO/canonical metadata is retained, legacy routes and feeds have a continuity plan, and custom post types/events are either migrated or explicitly retired.
6. Check importer reports and reconcile counts. Flag missing media, unknown shortcodes, unsupported blocks, retired URLs, duplicate routes, and undecided features. Do not silently drop them.
7. Replace Jetpack stats with a standalone protected stats site only if the owner wants one. Explain that authentication prevents potentially sensitive analytics from being exposed publicly; discuss the separate app, selected identity provider, D1 storage, and operating costs/limits before provisioning.

### Optional Jetpack/WordPress stats import

Ask explicitly whether the owner wants historical Jetpack stats imported. A WordPress database backup usually does not contain this history; access may require a separately authenticated WordPress.com/Jetpack API export.

If yes, help the owner authenticate through the provider's official browser/API flow. Request only the read permission needed. Keep tokens in a credential manager or provider-managed secret store, never in chat, exports, source files, logs, or shell history. Export the available daily metrics and native week/month/year aggregates; don't calculate longer-term unique visitors by summing daily uniques. Preserve actual returned dates, time zones, omissions, and unavailable reports.

Stage raw exports and generated SQL in a private ignored directory. Validate coverage, row counts, truncation, date gaps, and a sample against the source before writing to D1. Estimate writes and split imports to remain under the current D1 limits. Take a D1 backup before import. Use idempotent upserts where possible, and record exact imported date ranges. Keep Jetpack and Cloudflare series distinct and label non-equivalent metrics clearly.

If the owner declines, lacks access, or an endpoint is unavailable, record that choice or limitation. Do not imply stats were imported.

**Milestone 2 exit:** The content/media inventory reconciles to the source backup or documented fallback scope; imported site content renders on beta; public URLs and redirect mappings are accounted for; plugin and feature decisions are recorded. If requested, validated historical stats exist in D1 and can be viewed in the protected standalone dashboard.

## Milestone 3 — Repair, review, and launch readiness

Use [Migration Cleanup and Polish](skills/Migration-Cleanup-and-Polish/SKILL.md) Pass 1 only: repair broken or mangled output across every in-scope post and page. Ask the owner how many items to include in each batch and record the chosen size in the private [project profile](templates/project-profile.md) and [batch tracker](templates/cleanup-batch-tracker.csv) for both passes. Finish and verify Pass 1 before starting Milestone 4. Keep beta available throughout.

Review pages in a browser at desktop and narrow sizes, with light and dark themes where available. If the owner chose a redesign, work with them in this milestone to select and implement the site's visual direction, then review representative templates before continuing through the content repair batches. Verify navigation, images, captions, code, embeds, downloads, search, forms, comments, feeds, canonical URLs, metadata, redirects, accessibility, and performance. Compare rendered behavior with the WordPress source where useful. A successful static build does not prove content equivalence.

Use a living go-live checklist from the first milestone. It should capture:

- Exact current and intended production branch, commit, Pages project, build settings, hostnames, and Hugo runtime.
- Pre-cutover DNS/origin records, proxy/TLS settings, Pages custom-domain setup, owner access, and private recovery record location.
- Content/route, redirect, feed, sitemap, image, comments, stats, and search verification.
- Tangible deferred work that could affect launch readiness, with an owner, status, and resolution or explicit acceptance. Track deferrals here throughout all milestones; omit trivial tasks that do not affect launch readiness.
- A cutover sequence, observation window, rollback decision, and recovery steps to restore the prior site.
- A post-cutover verification record showing actual DNS, certificate, deployment SHA, served marker, core routes, and changed output.

Never put DNS credentials, private origin passwords, tokens, or full zone exports in Git. Keep a private, access-controlled record with the previous origin and each changed record's name, type, target, TTL, and proxy state. Keep the old WordPress site and backup available until the owner accepts the new site.

**Milestone 3 exit:** every in-scope page has completed the repair pass and is verified on beta; the site's content and functionality are ready for production cutover; remaining exceptions and recovery steps are recorded. After this exit, the owner may choose to cut over before or after Milestone 4. The owner makes the final production go/no-go decision.

## Milestone 4 — Final HTML and Markdown hygiene

After Milestone 3's repairs are merged and verified, run the skill's Pass 2 over every in-scope post and page, using the same human-selected batch size and recording per-item evidence in the [batch tracker](templates/cleanup-batch-tracker.csv). The owner may choose to complete this pass before or after production DNS cutover; Markdown cleanup should preserve the user-visible content and behavior. If cutover happens first, continue through the normal PR/preview/deployment path and verify each merged page on Production. Convert verbose HTML to Markdown only when Hugo's rendered output preserves meaning, links, attributes that matter, nesting, accessibility, and visual intent. Keep HTML for semantics/attributes Markdown cannot represent reliably, custom components, forms, embeds, and complex figures. Do not combine a repair and a syntax cleanup in one PR.

Complete the final content inventory and route/redirect audit. Run the project's documented lint/build and inspect affected generated output. Update maintenance documentation for each new recurring integration, generated artifact, migration tool, or deploy setting. If Production is not live yet, the owner may now approve the DNS cutover using the go-live checklist; if it is already live, verify each content-only deployment at the production hostname.

**Milestone 4 exit:** every in-scope page has a recorded result for both passes; unresolved exceptions are explicit; all PRs are merged and verified; the full site passes local and CI builds; the go-live checklist has current evidence. If the owner has not cut over, the site is ready for their final go/no-go decision; if it is live, the owner reviews and accepts the updated site.

## Future-dated content and previews

Use a filtered preview build so opted-in future content can be reviewed without changing its real date or exposing all drafts. The recommended pattern uses one Hugo build wrapper: Production runs ordinary Hugo; pull request validation requests preview mode; non-production Pages branches filter content using Pages branch context. A top-level boolean `preview: true` opts an individual page into review. An optional `Preview Date: YYYY-MM-DD` field in the open PR body simulates the site through a strict date cutoff. The wrapper stages only normally published-by-cutoff content plus explicit opt-ins before using Hugo's draft/future flags. See [the detailed future preview guide](FUTURE_DATED_PREVIEWS.md).

For private GitHub repositories, the Pages Preview build may need a fine-grained, repository-scoped read-only pull-request token to read that field. Store it in the Preview environment only; Production does not need it. Keep public-preview privacy controls in place. Never change a post's publication date to make it appear, and verify the content is absent from Production until intended.

## General merge, deployment, and recovery rules

- Pull requests are the review unit. Keep changes scoped and reproducible.
- Do not merge on the owner's behalf unless the owner explicitly authorizes that PR's merge. A general request to build the migration does not waive review.
- Before calling a deploy complete, verify the intended provider, environment, branch, exact commit SHA, deployment status, hostname, TLS, served runtime marker, and changed output.
- For a failed release, prefer the provider's artifact rollback for immediate recovery, then make a reviewed source correction. DNS/origin failures require the captured routing recovery procedure; a deployment rollback does not restore DNS.
- Repeat required health checks at the end and compare against the recorded baseline. Report blocked or unverified checks plainly.
