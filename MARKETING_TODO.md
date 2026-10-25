# Marketing TODO — getpullupmaster

> Project: Pull Up Master acquisition website. Source: https://github.com/coreyhaines31/marketingskills
> Start: 2026-10-26. All tasks are manual agent-assisted reviews; this PR does **not** schedule automatic jobs or publish changes.

## Setup (once, before first audit)
- [x] Review upstream skills and license; install relevant skills in the repository using `npx skills add coreyhaines31/marketingskills` and select only applicable skills. Confirm actual installed skill identifiers using the upstream catalog; names below describe capabilities, not guaranteed package IDs. *(2026-10-25: MIT license reviewed; `seo-audit` 2.2.2, `cro` 2.0.3 (upstream merged page-cro into cro) and `copywriting` 2.3.1 vendored by hand from upstream commit e85f3cb into `.agents/skills/`.)*
- [x] Verify agent (Codex/Claude/Copilot) detects the installed SKILL.md files. Commit any vendored skill files only after reviewing upstream content. *(2026-10-25: `.claude/skills/*` symlinked to `.agents/skills/*` for Claude Code; `.agents/product-marketing.md` created with `[NEED: ...]` markers for owner input.)*
- [ ] Establish 28-day baseline: organic clicks, app-store outbound clicks. Record sources, dates and measurement definitions; never invent figures.
- [ ] Confirm analytics access, consent/privacy requirements and current business claims.

## Cadence and prompts
- [ ] **2026-10-26 (initial):** Run SEO/ASO and conversion baseline audit. Prompt: "Read .agents/skills/marketing-workflow/SKILL.md and this file. Inspect this repo, identify verified issues and opportunities for Pull Up Master acquisition website, cite exact paths and metrics, rank by impact/confidence/effort; propose changes only."
- [ ] **Every Monday (weekly):** Compare last 7 days vs prior 7 days for organic clicks, app-store outbound clicks. Prompt: "Run a weekly growth review; separate observed data from hypotheses; propose up to three measurable experiments."
- [ ] **First business day of each month:** Keyword/competitor and content opportunity review. Prompt: "Research search intent, competitor positioning and content gaps for pull-up progression topics; landing page CTA; output a prioritized backlog with evidence and no invented search volumes."
- [ ] **Before each release or landing-page launch:** Copy, store listing/metadata, onboarding, paywall or CTA QA as applicable. Prompt: "Audit the proposed release funnel and claims; identify accessibility, localization, privacy and conversion risks; propose A/B test variants."
- [ ] **Every 4 weeks:** Experiment retrospective: capture hypothesis, control/variant, start/end dates, sample size, guardrails, outcome and decision (ship/retest/stop).

## Project-specific first experiments
- [ ] Review pull-up progression topics; landing page CTA.
- [ ] Pick ONE high-intent search/store-listing opportunity and write a change proposal with target audience, target query, baseline and success metric.
- [ ] Pick ONE conversion bottleneck and draft an A/B test; do not deploy until reviewed.

## Done criteria
- [ ] Every finding links to repository paths or measured analytics.
- [ ] Every proposed change has owner, priority, due date, metric and rollback plan.
- [ ] No publishing, ad spend, pricing changes, medical claims or tracking changes without explicit approval.
- [ ] Record findings and next run date here after each session.

## Run log
| Date | Skill / workflow | Baseline and evidence | Decision | Owner | Next review |
|---|---|---|---|---|---|
| 2026-10-25 | Setup | Vendored seo-audit / cro / copywriting; wrote `.agents/product-marketing.md` from repo evidence; no analytics present on site | Setup done; audit still pending owner inputs (baseline, Search Console) | Owner | 2026-10-26 |
| 2026-10-25 | Initial audit (seo-audit + cro, code-only; no analytics exist) | 89 pages, all in sitemap, hreflang reciprocal + x-default, Article+FAQPage schema, 301/404/canonical OK, TTFB ~0.3s, LCP ~0.6s, CLS 0 (desktop). Store: App Store 1 rating, Google Play 100+ installs. See findings section below. | Proposals only; owner to confirm trial length and approve store-link attribution | Owner | 2026-11-02 |

## Initial audit findings (2026-10-25, proposals only)
| # | Finding | Evidence | Impact | Confidence | Effort |
|---|---|---|---|---|---|
| 1 | Trial-length claim mismatch: site says "3-day free trial" (all 5 langs, pricing cards), App Store 2.4.0 release notes say a free **week** of Pro | `index.html` pricing; apps.apple.com id6799707900 What's New | High (trust, refund risk) | High that they differ; owner must say which is right | Low |
| 2 | No analytics and no store-link attribution: every store link is the bare URL, so website-driven installs cannot be measured | `index.html`, `assets/js/site.js`, article CTAs | High (no baseline possible) | High | Low (App Store campaign `pt`/`ct` params + Play `referrer` need no on-site tracking; still needs approval) |
| 3 | Primary CTA below the fold on a 1440x778 laptop viewport: hero store buttons start at y=756, "2 sessions free" note at y=832 | measured in Chrome on `/` | Medium | High (one viewport measured) | Low-Medium |
| 4 | `first-pull-up` family (5 langs) predates the generator: no FAQ/FAQPage schema, descriptions 181-233 chars, DE/ES/FR titles 64-70 chars | audit script over `*/index.html` | Medium (highest-priority article) | High | Medium (migrate to `content/first-pull-up.json`) |
| 5 | Home page titles 62-70 chars (DE/ES/FR) and descriptions 215-255 chars on all 5 homes: truncated in SERPs | audit script | Medium | High | Low |
| 6 | No guide hub page: nav "Guide" goes to one article; 12 of 16 EN articles have 0 links from home; anatomy series has 4-5 inbound links each | link graph over `*/index.html` | Medium | High | Medium |
| 7 | Store subtitle "Calisthenics progress tracker" does not match site positioning "adaptive pull-up coach / first pull-up" | App Store listing vs `index.html` H1 | Medium (ASO + message match) | Medium | Low (store copy change) |
| 8 | Sitemap has no `lastmod`; legal pages lack hreflang (EN only, acceptable) | `sitemap.xml` | Low | High | Low |

**Backlog (priority order):** 1 → 2 → 4 → 5 → 3 → 6 → 7 → 8.

**Experiments (max 3, all need approval before deploy):**
1. **Attribution first:** add App Store campaign params and Play `referrer` per placement (hero / sticky / pricing / article CTA). Metric: installs by placement in App Store Connect + Play Console after 28 days. Guardrail: no on-site tracking, links must still resolve.
2. **Hero CTA above the fold** (after 1 is live): tighten hero spacing or move the store buttons above the lede on ≥1280px. Metric: hero-placement install share. Guardrail: LCP stays under 1s, CLS 0.
3. **first-pull-up rebuild via generator** with FAQ block and trimmed title/description. Metric: Search Console impressions/CTR for that URL family over 4 weeks vs prior 4 weeks (needs Search Console access). Guardrail: same sources, same claims, no new medical statements.

**Not verified / needs owner:** Search Console access, 28-day organic baseline, mobile viewport screenshot (browser window resize failed; CSS review shows the sticky store bar is fixed to the bottom under 900px with 72px body padding and safe-area inset, so no content overlap is expected; confirm on a real phone). Google Play shows no rating yet (listing has too few ratings to display one; 100+ installs, updated 2026-10-22).

