# Migration Cleanup and Polish Skill

## Purpose

Review a migrated Hugo site in two complete passes: first repair broken or mangled content, then convert suitable verbose HTML to Markdown. Keep rendered output faithful and make each page reviewable on its own.

Use this after the WordPress import is on a beta/preview site. Read the repository's contributor and maintenance instructions first. The repository's policies and user instructions take precedence over this skill.

## Start

1. Establish the content inventory and rendered baseline. Record the commit, Hugo version, local build result, preview hostname, deployment branch/SHA, and pre-existing failures.
2. Ask the human how many posts/pages they want in each batch. Use that number as the cap for each round in both passes. Do not invent a default. The user may change the batch size later.
3. Confirm the in-scope posts/pages and the source of truth for each. Preserve URL, title, date, author, taxonomy, WordPress ID, media, attribution, and intended publication status unless the human requests a specific change.
4. Work in an isolated branch/worktree where available. Keep each PR scoped to one page or post.

Do not use issue labels, tags, or an IssueBot queue. Track work in a simple private checklist or PR list.

## Pass 1 — Repair broken or mangled HTML/Markdown

### Review and edit

Inspect one page/post at a time, comparing source, generated HTML, and browser rendering. Repair all confirmed broken items on that page in one PR. Possible defects include malformed or unclosed elements, lists rendered as literal text, missing/nested list items, broken links, bad image paths, captions attached to the wrong image, lost code formatting, shortcode residue, incorrect block boundaries, and layout overflow.

Do not "fix" valid but unusual source based on a regex or style preference. Confirm the failure in rendered output. Keep evidence and scope in the PR description.

### Stage a batch as Draft PRs

Work through pages in the human-selected batch size. For every page, open one Draft PR. This means a batch of 8 pages has up to 8 distinct Draft PRs, each repairing one page/post. Do not combine pages into one PR. Do not mark any PR ready while the batch is still being prepared.

Each PR should say:

- The one page/post and canonical URL.
- What was broken and how the rendered evidence established it.
- What source changed.
- What was checked locally and on the exact branch preview.
- Any unresolved uncertainty.

If one page has unrelated changes already present, preserve them and coordinate a clean scope rather than overwriting them.

### Adversarial review, readiness, and human review

After all Draft PRs in the batch are staged, review every PR adversarially. Inspect the complete diff and rendered before/after page. Challenge URL/date/metadata drift, accidental content changes, lost links/attributes, inaccessible markup, unclosed markup elsewhere on the page, overbroad edits, and regressions at narrow widths/themes. Resolve findings, rerun build checks, and confirm each PR's exact Preview deployment matches its head SHA.

Only after every PR in the batch has had this review and its Preview is valid, mark the reviewed PRs ready for review. The human reviews and merges them, or explicitly authorizes the agent to merge those PRs. Do not infer merge permission from permission to implement or open PRs.

After merge, verify each page at the deployed hostname and exact production commit. Check its canonical URL, critical text, links, images, layout, and intended status. Record the result. Do not start Pass 2 for an item until its Pass 1 PR is merged and verified.

## Pass 2 — Convert appropriate HTML to Markdown

Begin only after all Pass 1 items in scope have been repaired and verified. Reuse the same human-selected batch size and repeat the same steps: edit each item, one Draft PR per page/post; stage a complete batch; adversarially review every PR; mark valid PRs ready; wait for human review/merge or explicit merge authorization; verify every merged item on the deployed site.

Convert only syntax that Markdown can represent without losing the rendered meaning. Common candidates include paragraphs, headings, simple ordered/unordered/nested lists, emphasis, links, blockquotes, inline code, and fenced code blocks. Use the repository's actual Markdown parser and extensions when judging equivalence.

Retain raw HTML when Markdown cannot express essential behavior or presentation: meaningful classes/IDs, attributes, complex figures/captions, accessible labels, tables with special semantics, forms, custom embeds, inline styling, or structures that the parser changes. Do not remove an attribute just to make the source shorter.

## Per-page validation

For each item, capture or compare the before and after rendered HTML. Check:

- Text, headings, paragraphs, list nesting and numbering.
- Link destinations, labels, and meaningful attributes.
- Images, alternative text, captions, attribution, and download behavior.
- Code language, whitespace, escaping, and copyability.
- Quotes, tables, embeds, and accessibility semantics.
- Desktop and narrow-screen appearance; light/dark themes if provided.
- No unintended changes to URL, date, taxonomy, feeds, or indexing.

A successful static build only proves that the site built. Inspect the affected page's generated output and exact Cloudflare Preview. After merge, inspect its production rendering. Use screenshots when layout or visual behavior changed.

## Batch record and finish

Maintain a simple table with item, canonical URL, Pass 1 status/PR, Pass 1 verification, Pass 2 status/PR, and Pass 2 verification. At batch completion, report the items completed, open PRs, review findings, merge state, verified deployed URLs/SHAs, and blockers.

A pass is complete only when every in-scope page has a recorded outcome. Document exceptions and why they remain HTML or require owner input. Never mark a page complete based on source edits alone.
