# Future-dated posts and safe previews

This pattern previews scheduled content without changing its intended date or publishing it early. Adapt it to the site's Hugo version and the current Cloudflare Pages environment variables. Use one documented build wrapper for local, pull request, branch-preview, and production builds, with explicit rules for each environment.

## Required behavior

- Production branch: run an ordinary Hugo production build. Do not pass `--buildFuture` or `--buildDrafts`. Future-dated and draft content stays excluded.
- Pull request validation: run the wrapper in preview mode so opted-in content is included in the built output and checked by CI.
- Cloudflare Pages non-production branches: detect the Pages branch context and use a filtered staging copy of content. Include normally published content plus content the author explicitly opted into previewing. Invoke Hugo with draft/future support only against this filtered copy.
- Local review: expose an explicit preview option. Keep production build commands on the normal path.

## Per-post preview opt-in

A post can use a top-level boolean front matter field such as `preview: true` to include that item in non-production previews, even when it remains a draft or its publication date is in the future. Accept only an actual boolean, not the quoted string `"true"`. Do not change its date or set `draft: false` to make a preview work. The production build ignores this preview-only field and keeps Hugo's normal draft/date rules.

## Whole-site date simulation

Support an optional PR body field:

```text
Preview Date: YYYY-MM-DD
```

The wrapper reads this value only from the open PR associated with the Pages branch. It validates one strict calendar date, then asks Hugo which content is publishable through the cutoff using Hugo's clock setting. The staged content contains only pages published by that cutoff and pages explicitly opted into preview mode. Hugo may then build drafts and future pages from that staged directory without exposing every draft in the repository.

For example, a PR cutoff can show a non-draft post scheduled on or before the cutoff while excluding later posts and all unmarked drafts. Leave the field blank for an ordinary preview. Never set this value in production metadata or change the content's real date.

## Cloudflare and GitHub setup

1. Configure Pages with one build wrapper command used in both environments. The wrapper itself must use the normal production build on the production branch and preview filtering on non-production branches, based on verified Pages environment variables.
2. For a private GitHub repository, give the Pages **Preview** environment a fine-grained GitHub token restricted to that repository with read-only access to pull-request metadata. The wrapper needs this only to read the open PR body and its Preview Date. Do not configure that token in Production.
3. Ensure the GitHub Actions pull-request job invokes the wrapper with preview mode. Keep the ordinary push-to-production job on the normal build path.
4. Fail closed: a missing token, API error, multiple open PR matches, malformed date, or invalid preview metadata must fail clearly. It must not silently produce misleading content.
5. Clean the destination before a build so files from an earlier preview cannot survive after an opt-in or cutoff is removed.
6. Verify preview hostnames are treated as public unless access protection is active. Noindex can reduce discovery but does not restrict access. Do not include private WordPress content in a public preview.

## Local workflow and validation

Use the repository's wrapper, for example:

- Normal local server: `python scripts/hugo_build.py server`
- Preview server: `python scripts/hugo_build.py --preview server`
- Simulated future site date: `python scripts/hugo_build.py --preview-date YYYY-MM-DD server`

Follow the actual wrapper's help and repository documentation; command order can vary by implementation. A wrapper that stages a content snapshot may need a restart after edits.

Validate the wrapper's selection rules: opted-in future content appears in Preview; non-opted drafts and content later than the cutoff stay absent; removing the opt-in/cutoff removes the output on the next clean build; Production does not expose preview-only content. Check the affected page, home/archive listings, search index, feeds, sitemap, and any generated summaries for consistency.

## Implementation outline

A portable wrapper should:

1. Detect the production branch and explicit local preview flags.
2. Parse front matter safely and accept only top-level boolean `preview: true`.
3. Read at most one strict Preview Date from the matching open PR when running on a non-production Pages branch.
4. Ask Hugo for the normal published-content inventory at the cutoff.
5. Stage only that inventory plus explicit preview opt-ins in a temporary content directory.
6. Run Hugo with draft/future flags only against the staged directory.
7. Clean temporary content and the generated output, surface errors, and avoid printing the GitHub token.
8. Keep local preview and production paths explicit and test their boundaries.

The staging filter is the safety boundary. Passing `--buildDrafts --buildFuture` over the unfiltered production content directory is not an acceptable shortcut.
