# Article content files

One JSON file per topic, all five languages inside. Build with `python3 scripts/build_article.py content/<topic>.json`.

```json
{
  "slugs": { "en": "rotator-cuff-pull-ups", "de": "rotatorenmanschette-klimmzug", "tr": "rotator-manset-barfiks", "es": "manguito-rotador-dominadas", "fr": "coiffe-des-rotateurs-tractions" },
  "priority": "0.8",
  "langs": {
    "en": {
      "title": "Rotator Cuff and Pull-Ups: Anatomy, Role, Injury Prevention",
      "description": "120-160 chars, contains the main keyword, written as a promise of what the page answers.",
      "headline": "H1 of the page",
      "subtitle": "One short line shown under the H1",
      "read_time": "7 min read",
      "lede": "2-3 sentence plain-text answer to the search intent. Shown as the opening paragraph.",
      "body_html": "<h2>...</h2><p>...</p><ul><li>...</li></ul><div class=\"table-scroll\"><table>...</table></div>",
      "faq": [ { "q": "Question?", "a": "Plain-text answer, 1-3 sentences." } ],
      "sources": [ { "label": "Author/Org. Title. Journal/Site, year.", "url": "https://..." } ],
      "keep_reading": [ { "href": "/first-pull-up/", "title": "How to do your first pull-up" } ]
    },
    "de": { "...same keys..." }, "tr": {}, "es": {}, "fr": {}
  }
}
```

Rules enforced or warned by `--check`:

- Allowed tags in `body_html`: h2, h3, p, ul, ol, li, table/thead/tbody/tr/th/td (wrap tables in `<div class="table-scroll">`), strong, em, a, br, sup. No h1, no inline styles, no images.
- 1100-1600 body words per language, 4-6 FAQ items, at least 3 sources, 4-6 keep-reading links.
- Every internal link must point to an existing page in the same language.
- Cite sources inline with `<sup>[n]</sup>` matching the order of the `sources` list.
- Translations are adaptive, not literal: native phrasing, local keyword in title/H1/slug, same facts and the same sources.
