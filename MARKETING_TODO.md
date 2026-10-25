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
| 2026-10-26 (planned) | Initial audit | Pending | Pending | TBD | 2026-11-02 |
