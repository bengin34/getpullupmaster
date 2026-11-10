# Security audit — getpullupmaster.app (MEN-214)

- Date: 2026-11-10. Commit reviewed: `354888f` (main), clean worktree.
- Mode: full audit workflow, `quick` profile, single agent, source-first, read-only. No site code executed, no live probing.
- Coverage: partial. Static site (HTML + 1 JS file + 1 GitHub Action + 4 helper scripts). No prior run exists.

## Result

| Severity | Count |
|---|---|
| critical / high / medium / low | 0 |
| needs_validation | 1 |
| rejected | 2 |

No confirmed findings, so no fixes in this PR.

## Checked, clean

- Secrets: no keys, tokens or credentials in tracked files. Only secret-like items are the IndexNow key (`0b41628e…txt`, `scripts/indexnow.sh`; public by design) and Bing site-auth file. Deleted-file history (`assets/site.js`, `styles.css`, `og-image.svg`) is old static assets, not secrets.
- Third-party scripts: none. Only first-party `/assets/js/site.js` plus inline JSON-LD. No iframes, no forms, no contact endpoint (support = mailto).
- External links: store and citation links only. 15 links use `rel="noopener"` without `noreferrer`, which is irrelevant (no sensitive referrer).
- Open redirects: none. `auth.html` navigates only to the fixed `pullupmaster://login` scheme with encoded values, sets `referrer=no-referrer`, `noindex`, and strips the token from the URL; robots.txt disallows it.
- Admin/preview routes: none in the repo.
- Supply chain: no package manifest, no dependencies. Workflow uses `actions/checkout@v4` (tag, not SHA pinned), no secrets, `push` trigger only.
- Hosting: GitHub Pages. Response headers (CSP, X-Frame-Options, HSTS beyond Pages default) cannot be set from the repo. Not reported: missing headers on a static, no-auth, no-form site have no demonstrated boundary result.

## Findings

- `auth-html-type-param-passthrough` — needs_validation. `auth.html:108` forwards `type` into the deep link without an allowlist. Page itself is safe; the app's handler must allowlist it. See `findings.json`.
- Rejected: `site-js-innerhtml-data-msg` (static authored attribute), `indexnow-workflow-expression-injection` (GitHub-generated SHA).

## Not covered

- Deployed headers and DNS/Pages settings (needs owner check).
- App-side deep-link handler and Supabase email templates (other repos).
- Generated article HTML inspected by sampling and grep, not line-by-line.
