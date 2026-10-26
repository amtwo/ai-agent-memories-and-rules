# AM2.co Owner Hub: client bootstrap brief

This brief gives an independent agent stable product, API, security, and data context for building an AM2.co owner client. It is intentionally platform-neutral. Choose the native UI, navigation, component architecture, and platform-specific interaction model for the target platform; the existing web dashboard is not a visual specification.

## Product scope

AM2.co Owner Hub is a private owner-facing home for site operations. The first client surfaces are **Stats** (Cloudflare current-day traffic and real-user performance, historical traffic and rankings, and clearly separated sources) and **Site Health** (Cloudflare Pages production metadata plus read-only live HTTP and Hugo generator checks).

The first native implementation is in [amtwo/am2-co-stats/android](https://github.com/amtwo/am2-co-stats/tree/main/android). Android is the first client; iOS can consume the same JSON contracts. Additional owner tools may be added as independent modules. The public website and analytics collector remain separate systems.

## Source repository pointers

Canonical implementation and operations live in [amtwo/am2-co-stats](https://github.com/amtwo/am2-co-stats):

The corresponding native Android/API implementation is under review in [amtwo/am2-co-stats PR #11](https://github.com/amtwo/am2-co-stats/pull/11).

- Worker routes, response types, Cloudflare GraphQL queries, and Pages checks: [src/index.js](https://github.com/amtwo/am2-co-stats/blob/main/src/index.js)
- D1 schema and historical metric tables: [migrations/](https://github.com/amtwo/am2-co-stats/tree/main/migrations)
- Android reference client and widget: [android/](https://github.com/amtwo/am2-co-stats/tree/main/android)
- API, credential, and Access runbook: [MAINTENANCE.md](https://github.com/amtwo/am2-co-stats/blob/main/MAINTENANCE.md)
- Product and source distinctions: [README.md](https://github.com/amtwo/am2-co-stats/blob/main/README.md)

The Android tree is a source example, not a design mandate for another platform. Read the Worker response shape before interpreting a metric. Keep API field changes additive where practical and update this brief.

## Owner API and access boundary

The API origin is https://stats.am2.co and is protected by Cloudflare Access. Native clients must use the existing Access application, identity provider, and owner allow-list; this is not a public analytics API and there is no separate AM2 account/password system.

The intended native flow is Cloudflare Access Managed OAuth with an external system browser, public-client dynamic registration, Authorization Code + PKCE (S256), and the RFC 8707 resource indicator set to https://stats.am2.co/. Access policies are re-evaluated when refresh credentials are used. Store refresh credentials only in platform secure credential storage. Never embed Cloudflare API tokens, service tokens, Access allow-list entries, or a client secret in a distributed app.

The existing Access administrator must enable Managed OAuth and dynamic client registration on the self-hosted app, allow an appropriate loopback redirect, and preserve the current Google identity provider and policy. The Android reference currently registers http://127.0.0.1:8400/callback; a different client can use a suitable redirect supported by its platform and Access configuration. App/operator configuration is a deployment prerequisite, not something a mobile binary can enable itself.

All app and widget data requests are read-only GET calls. Clients must not call POST /api/collect; the existing hourly Worker Cron performs collection. Do not silently invoke collection to fill gaps.

## API contracts

### GET /api/current

Fetches Cloudflare Web Analytics GraphQL data on demand at app refresh. It does not use D1 and does not write or alter the hourly complete-day history. The response is a **partial current UTC day**, not a complete day or guaranteed second-by-second feed.

Representative success response (illustrative values only; no site records):

    {
      "source": "cloudflare_web_analytics",
      "day": "YYYY-MM-DD",
      "complete": false,
      "retrievedAt": "ISO-8601 UTC timestamp",
      "window": { "start": "UTC day start", "end": "retrieval time" },
      "sampling": { "sampled": true, "sampleInterval": 10,
        "note": "Cloudflare Web Analytics may be adaptively sampled and can arrive with delay." },
      "traffic": { "pageviews": 120, "visits": 87 },
      "performance": [
        { "dataset": "performance", "sampleCount": 50, "sampleInterval": 10,
          "averages": { "pageLoadTime": 1230000 }, "p75": { "pageLoadTimeP75": 2000000 } }
      ],
      "webVitals": [
        { "dataset": "web_vitals", "sampleCount": 40, "sampleInterval": 10,
          "averages": { "largestContentfulPaint": 1800000, "cumulativeLayoutShift": 0.03 },
          "p75": { "largestContentfulPaintP75": 2200000 } }
      ],
      "topPaths": [
        { "path": "/", "pageviews": 90, "visits": 60, "sampleInterval": 10 }
      ]
    }

Sampling.sampled can be null when Cloudflare has no sample interval to report. Empty datasets are valid and should render as unavailable/empty, not as an observed zero-quality measurement. Provider/query failures return HTTP 502 with an error and retrieval time.

Traffic values are Cloudflare Web Analytics RUM page-load event counts and visit totals. Performance and Core Web Vitals are real-user measurements. Existing timing query values are in microseconds; divide by 1,000 for display in milliseconds. CLS is a unitless score and must not be converted. sampleCount is the observation count returned by the aggregate query, not all site users.

Cloudflare adaptive sampling and reporting delay apply. These data are not instant operational monitoring. Show the source, UTC day/window, retrieval time, and reported sample interval or an unknown-sampling state.

### GET /api/data

Reads the established D1 history. Call with ?days=30 (1–36,500 days), or an inclusive ?from=YYYY-MM-DD&to=YYYY-MM-DD range. Dates are UTC calendar dates. This route includes distinct source rows; do not combine unlike visitor definitions into one series.

The metrics array rows look like:

    { "day": "YYYY-MM-DD", "source": "cloudflare", "metric": "visits", "value": 87, "sampleInterval": 1 }

Sources:

- cloudflare: daily pageviews and visits. The hourly collector refreshes recent complete UTC days. A sample interval of 1 means unsampled at that reported resolution; larger values indicate sampling. Historical availability and resolution depend on Cloudflare retention and imports.
- jetpack: WordPress-era historical pageviews and visitors. Jetpack visitors and Cloudflare visits are different measures and must be labeled separately. Do not add daily unique counts to claim a deduplicated range-wide audience.

Other fields include from, to, rangeDays, periodMetrics, lastCollection, siteStats, topPosts, lowPosts, breakdowns, cloudflarePages, cloudflareLowPages, cloudflareBreakdowns, and cloudflarePerformance. Top posts and engagement/discovery fields originate from historical Jetpack imports; Cloudflare path and RUM details are Cloudflare sourced. Results may be empty because of date coverage, provider retention, missing imports, or no observations. Preserve source labels in chart legends, cards, exports, and accessibility descriptions.

The mobile widget should use complete-day rows only, with the default window ending yesterday in UTC. Supported first-client periods are the latest complete UTC day, trailing 7 complete UTC days, and trailing 30 complete UTC days. Display inclusive covered dates, source, and cache/update time. Keep offline cached values visibly dated; do not relabel a stale cache as live.

### GET /api/site-status

Combines the Cloudflare Pages project am2-co API response with live HTTPS checks of am2.co and www.am2.co. A representative successful response:

    {
      "retrievedAt": "ISO-8601 UTC timestamp",
      "deployment": {
        "ok": true, "project": "am2-co", "productionBranch": "main",
        "branch": "main", "commit": "full commit SHA", "status": "success",
        "environment": "production", "url": "Pages deployment URL",
        "domains": ["am2.co", "www.am2.co"]
      },
      "hosts": [
        { "host": "am2.co", "ok": true, "url": "https://am2.co/",
          "httpStatus": 200, "hugoVersion": "0.168.0", "error": null }
      ],
      "ok": true
    }

Treat individual source failures as failures. The route returns HTTP 502 when a required deployment or host check is unavailable/unhealthy and includes partial results to identify the failing check. The Hugo version comes from the served generator meta marker. Project domains are current Pages project domains; host checks validate the two configured production hosts.

## Freshness and presentation rules

- Use Cloudflare for current traffic and real-user performance; use D1 for retained historical trends, rankings, and source-specific detail.
- Keep partial-day current data visibly distinct from complete-day history, including during UTC rollover.
- Keep Cloudflare visits separate from Jetpack visitors; never chart or total them as one metric.
- Display Cloudflare sampling interval where available and indicate when sampling status is unknown. Interval 1 is an unsampled reported bucket, not a promise of a census outside Cloudflare's documented scope.
- Show retrieval/capture freshness. An API timestamp is when the Worker retrieved the current snapshot, not proof every event was generated then.
- Empty results, stale/offline cache, missing source history, and endpoint errors are separate UI states; don't turn them into a healthy zero or lose date/source context.
- Site Health checks deployment metadata and current route markers; it is a lightweight snapshot, not an alerting/SLO service.

## Security and privacy boundaries

- Analytics token and separate Cloudflare Pages: Read API token are Worker secrets only. Neither is a mobile credential.
- Cloudflare Access bearer/refresh tokens belong only in OS secure storage and should be erased on sign-out. Do not log OAuth codes, tokens, or callback URLs containing codes.
- Do not copy owner email addresses, Access policy members, exported Jetpack records, page/post analytics records, or production secrets into this public brief or another app repo.
- Request only APIs/date ranges needed for the feature; avoid sending analytics data to third parties.
- Keep client permissions and API behavior read-only. Any future write or operational action needs separate design and explicit authorization.

## Validation checklist

Use non-production test doubles or an explicitly authenticated, read-only owner session. Never trigger production collection as an app test.

- Check current-day UTC boundaries, partial-day labeling, empty observations, sample interval 1, sampled interval >1, unknown sampling, and Cloudflare failures.
- Confirm history can render independently of current-snapshot failure, and Jetpack/Cloudflare rows and page/post rankings retain their source.
- Exercise Site Health API failure, Pages deployment failure/partial metadata, host HTTP failure, missing Hugo marker, and hostname redirects.
- Exercise Access denied/allow, browser cancellation/denial, PKCE state mismatch, successful code exchange, expired/revoked refresh, policy revocation on refresh, and sign-out/revocation.
- For each widget period, verify UTC covered dates, cached offline output, stale-cache indication, and recovery after reconnection.

This brief describes API and owner-data constraints, not a visual design. Independent iOS/Android designers can choose native patterns within these boundaries.
