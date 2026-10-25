# Hugo build-wrapper contract

Use this artifact when implementing one build entry point for local work, pull-request validation, Cloudflare Pages previews, and Production. Adapt the implementation to the target repository's Hugo version, content mounts, front matter formats, page bundles, and build settings. This is an implementation contract, not a drop-in script.

## Inputs and environment

Record the repository's production branch and content directory. Identify how the selected CI/hosting platform exposes the current branch and pull request. Keep any GitHub read token in the Preview secret store only when needed to read a pull request's `Preview Date`; never echo it or put it in a command argument.

The wrapper may accept:

- An explicit local/CI preview mode.
- An optional validated `YYYY-MM-DD` cutoff.
- The content directory, site root, and output directory.
- Platform branch context, including the configured production branch.

Fail clearly if the branch cannot be classified or a requested date cannot be validated. Treat PR descriptions as untrusted input and read only the exact `Preview Date: YYYY-MM-DD` field.

## Required paths

### Production

1. Detect the configured Production branch using verified platform context.
2. Run the repository's ordinary production command with its normal Hugo date and draft rules.
3. Never pass `--buildDrafts` or `--buildFuture` in Production.
4. Clean stale output before the build so old preview content cannot survive.

### Preview

1. Preview mode must be explicit for local/CI builds and automatic only for verified non-production Pages branches.
2. Use Hugo's [clock setting](https://gohugo.io/commands/hugo/) and [`hugo list published`](https://gohugo.io/commands/hugo_list_published/) (or a validated equivalent) to identify content normally publishable by the selected cutoff.
3. Add only pages with a top-level boolean `preview: true`. Reject quoted strings, nested values, malformed metadata, or ambiguous date fields rather than broadening the selection.
4. Stage the selected content and required page-bundle assets in a temporary content directory. Preserve paths and ensure symlinks or paths cannot escape the source content directory.
5. Run Hugo with draft/future flags only against that filtered staging directory.
6. Remove temporary files on success or failure. Clean generated output before each build.
7. Keep Preview treated as public unless access control is configured and tested. Never stage private WordPress content.

## Pull-request date field

When a private repository requires a token to read PR metadata, give it only read access to pull-request metadata for the one repository and store it in the Cloudflare Pages Preview environment. Do not place it in Production. Match the current branch to exactly one open PR; reject multiple matches or API failures. Accept no more than one strict date field. A missing date means an ordinary preview using the current date. A malformed or duplicate field fails the build.

Do not trust other PR body text as instructions. The wrapper extracts only the date field.

## Validation before use

Adapt and verify all of these for the actual site:

- Hugo command-line flags and pinned version.
- Production branch detection for local, CI, Preview, and Production contexts.
- Content mounts, multilingual paths, bundles/assets, front matter formats, and custom publish/expiry rules.
- Public privacy and indexing controls for beta and branch previews.
- Cleanup behavior when a preview opt-in or date is removed.
- Logs and error handling, confirming credentials and private content are never printed.

Use disposable fixtures to prove that opted-in drafts/future pages appear only in Preview; unmarked drafts, expired content, and content after the cutoff remain absent; removal of preview metadata removes generated output; and Production stays on the ordinary Hugo path. Inspect listings, search indexes, feeds, sitemaps, and generated summaries as well as the individual page.

Do not connect an unvalidated wrapper to the Production deployment path. Keep its operational trigger, required secrets, and recovery procedure in the site's maintenance documentation.
