---
name: marketing-workflow
description: Coordinate evidence-based SEO, ASO and conversion reviews for getpullupmaster using the vendored seo-audit, cro and copywriting skills and MARKETING_TODO.md. Use for a marketing audit, weekly growth review, release marketing QA, keyword/content plan, or a pricing/conversion experiment on the Pull Up Master acquisition website.
---

# Marketing workflow for getpullupmaster

This is a local orchestration skill. The upstream skills it depends on are vendored from https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines).

## Installed skills (vendored 2026-10-25, upstream commit e85f3cb)

| Capability | Upstream skill | Version | Path |
|---|---|---|---|
| SEO audit (technical, on-page, international/hreflang) | `seo-audit` | 2.2.2 | `.agents/skills/seo-audit/` |
| Page conversion review (upstream merged `page-cro` + `form-cro` into `cro`) | `cro` | 2.0.3 | `.agents/skills/cro/` |
| Marketing copy, CTA and headline alternatives | `copywriting` | 2.3.1 | `.agents/skills/copywriting/` |

Canonical copies live in `.agents/skills/` (shared by Codex, Copilot and other agents). `.claude/skills/<name>` are relative symlinks to them so Claude Code discovers the same files. To update: re-clone upstream, review the diff of `skills/<name>/`, copy `SKILL.md` + `references/` over, and bump this table. Do not install with `npx skills add` from inside an agent session without `-a claude-code`; it otherwise writes only to `.agents/skills/`.

All three upstream skills read `.agents/product-marketing.md` first. Keep that file current; anything marked `[NEED: ...]` there is unverified and must not be stated as fact.

## When to use
When asked for a marketing audit, weekly growth review, release marketing QA, keyword/content plan, pricing or conversion experiment for the **Pull Up Master acquisition website**.

## Procedure
1. Read `MARKETING_TODO.md`; check cadence and run log. Read `.agents/product-marketing.md` and `CLAUDE.md` (site structure, content rules).
2. Load the relevant vendored SKILL.md: `seo-audit` for crawl/index/on-page/hreflang, `cro` for landing page and store-link CTAs, `copywriting` for copy alternatives. Verify the file exists before claiming the skill is applied.
3. Inspect project code, metadata, landing pages and instrumentation; request missing analytics instead of fabricating data. The site currently has no analytics or click tracking.
4. Focus on: pull-up progression topics; landing page CTA (App Store / Google Play outbound clicks).
5. Output an evidence table (finding, evidence/path, impact, confidence, effort), a prioritized backlog and at most 3 testable experiments with guardrails.
6. Do not modify production, publish content, alter prices, spend on ads or add tracking without approval. Article changes go through `content/<topic>.json` + `scripts/build_article.py`, never hand-edited HTML. Update TODO checkboxes/run log only after completing a run.
