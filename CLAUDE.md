# getpullupmaster.app

Static marketing + SEO site for the PullUp Master app. Served by GitHub Pages from the repo root (CNAME = getpullupmaster.app). No build step for the site itself; pages are plain HTML using `/assets/css/site.css` and `/assets/js/site.js`.

## Languages and URL layout

- EN at `/<slug>/`, DE at `/de/<slug>/`, TR at `/tr/<slug>/`, ES at `/es/<slug>/`, FR at `/fr/<slug>/`.
- Every article exists in all 5 languages with cross-linked `hreflang` tags and a language menu. Never ship a page in one language only.
- Slugs are localized keywords (not translations of the EN slug), lowercase ASCII + hyphens.

## Adding a new article (the only supported way)

1. Write `content/<topic>.json` following `content/README.md` (all 5 languages in one file).
2. `python3 scripts/build_article.py content/<topic>.json --check` until it reports no ERROR.
3. `python3 scripts/build_article.py content/<topic>.json` writes the 5 `index.html` files and appends the URLs to `sitemap.xml`.
4. Add links to the new article in the "Keep reading" lists of 2-3 related existing articles per language (edit the `<ul>` after the keep-reading `<h2>`).
5. `python3 scripts/sitemap_lastmod.py` refreshes `<lastmod>` in `sitemap.xml` from git history (run it before committing).
6. Commit and push to `main`. The `IndexNow ping` GitHub Action then submits the changed pages to Bing/Yandex automatically. To ping by hand: `scripts/indexnow.sh --changed` or `scripts/indexnow.sh --all`.

Do not hand-write article HTML; regenerate from JSON so the chrome (header, footer, CTA, schema) stays identical across pages.

## Content rules

- Answer-first lede, then H2 sections phrased as questions where natural, FAQ block (also emitted as FAQPage schema), then a numbered Sources list.
- Anatomy and health claims must cite medical or peer-reviewed sources (StatPearls / NCBI Bookshelf, PubMed, PMC, journals, Physiopedia). Only include URLs that were verified to resolve.
- Tone: plain, second person, no hype. Every page ends with the "training tool, not medical advice" disclaimer (the generator adds it).
- Internal links only within the same language.

## Search engines

- Bing Webmaster Tools: site verified via `BingSiteAuth.xml`, sitemap submitted, IndexNow key file `0b41628e52eab36ebf653a9385beffc6.txt` at the root (public by design).
- Google: `sitemap.xml` is referenced from `robots.txt`.

## Marketing reviews

- Orchestration skill: `.agents/skills/marketing-workflow/SKILL.md` (symlinked into `.claude/skills/`). Cadence and run log live in `MARKETING_TODO.md`.
- Vendored upstream skills (coreyhaines31/marketingskills, MIT): `seo-audit`, `cro`, `copywriting` under `.agents/skills/`. They read `.agents/product-marketing.md` first; keep it current and never state its `[NEED: ...]` items as fact.
- Reviews propose only. No publishing, price changes, ad spend or tracking without explicit approval.
