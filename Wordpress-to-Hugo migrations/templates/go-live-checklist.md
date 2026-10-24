# Go-live checklist

Copy this checklist into the site project early. Keep private DNS/origin evidence in approved secure storage and put only its locator here.

## Before cutover

- [ ] Confirm owner gave a go/no-go for production cutover.
- [ ] Confirm latest successful Pages Production deployment uses the intended production branch and exact commit.
- [ ] Confirm Hugo build command, output directory, and deployed generator/runtime marker.
- [ ] Confirm beta has been reviewed and key routes work over HTTPS.
- [ ] Verify home, representative posts/pages, search, sitemap, RSS/Atom feeds, images, redirects, 404, comments, forms, and stats authentication where applicable.
- [ ] Verify canonical URLs, WordPress GUID/feed continuity where applicable, metadata, and indexing behavior.
- [ ] Inventory all old routes. Test each redirect at beta/preview; resolve every high-value legacy URL.
- [ ] Confirm no drafts or future-dated posts are exposed early.
- [ ] Keep WordPress operational and retain the original backup until acceptance.
- [ ] Capture current DNS records, origin, TLS, proxy state, redirect/Worker rules, and Pages domain assignments in private storage.
- [ ] Confirm authorized access to restore the previous site and validate the recovery path.

## Cutover

- [ ] Apply only the approved DNS/custom-domain changes.
- [ ] Keep mail-related DNS records unchanged.
- [ ] Confirm DNS resolution, Pages hostname association, and TLS certificate.
- [ ] Verify redirects and representative legacy paths from an external client.
- [ ] Record actual change time and propagation/observation window.

## After cutover

- [ ] Confirm active Production deployment ID, environment, branch, exact SHA, and status.
- [ ] Read the served Hugo generator marker from the production hostname.
- [ ] Verify key routes return expected content, not only HTTP 200.
- [ ] Check feeds parse and contain expected items; check representative legacy routes.
- [ ] Check search, comments, forms, stats Access policy, and collector.
- [ ] Check analytics/error logs without exposing secrets or personal data.
- [ ] Ask the owner to inspect the permanent site and accept it.
- [ ] Record outstanding issues and the decision to retire or retain WordPress.

## Recovery

- [ ] Stop further DNS/routing changes and record symptoms and time.
- [ ] If artifact output is faulty, roll Pages Production back to the last known-good production deployment.
- [ ] If DNS/TLS/origin is faulty, restore only the captured records and settings required to return to the old origin. Do not use an artifact rollback as a DNS recovery.
- [ ] Confirm DNS, HTTPS certificate, redirects, and representative WordPress routes reach the restored origin.
- [ ] Keep both origins and backups available while diagnosing.
- [ ] Prepare a reviewed source correction and deploy it through the normal PR path.
