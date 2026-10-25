#!/usr/bin/env python3
"""Build one SEO article in all 5 languages from a content JSON file.

Usage:
    python3 scripts/build_article.py content/<topic>.json          # write pages + update sitemap
    python3 scripts/build_article.py content/<topic>.json --check  # validate only, print stats

Content JSON schema (see content/README.md):
{
  "slugs":    {"en": "...", "de": "...", "tr": "...", "es": "...", "fr": "..."},
  "priority": "0.8",
  "langs": {
    "en": {
      "title": "<meta title, <=60 chars>",
      "description": "<meta description, 120-160 chars>",
      "headline": "<H1>",
      "subtitle": "<one-line summary shown under H1>",
      "read_time": "7 min read",
      "lede": "<2-3 sentence answer-first intro, plain text>",
      "body_html": "<h2>..</h2><p>..</p> ... (h2/h3/p/ul/ol/table/strong/a only)",
      "faq": [{"q": "...", "a": "..."}, ...],              # 4-6 items, plain text
      "sources": [{"label": "...", "url": "https://..."}], # verified medical/scientific refs
      "keep_reading": [{"href": "/...", "title": "..."}]   # 4-6 internal links, same language
    },
    "de": {...}, "tr": {...}, "es": {...}, "fr": {...}
  }
}
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://getpullupmaster.app"
LANGS = ["en", "de", "tr", "es", "fr"]
APP_STORE = "https://apps.apple.com/app/id6799707900"
PLAY = "https://play.google.com/store/apps/details?id=com.pullup.master"

# Per-language page chrome, copied verbatim from the existing hand-written articles.
L = {
    "en": {
        "og_locale": "en_US", "home": "/", "guide": "/first-pull-up/",
        "brand_aria": "PullUp Master home", "nav_aria": "Primary", "lang_aria": "Language", "menu_aria": "Menu",
        "nav": ["The climb", "How it adapts", "Apple Watch", "Pricing", "Guide"],
        "download": "Download", "eyebrow": "Guide",
        "faq_h": "Frequently asked questions", "sources_h": "Sources", "keep_h": "Keep reading",
        "cta_h": "Let the plan do the counting.",
        "cta_p": "PullUp Master runs this exact progression for you: it places you on the right block, guides every set with clips and a rest timer, and rewrites your next session from how the last one felt — with an estimate of how many weeks your first rep is away.",
        "cta_btn": "Get PullUp Master — 2 sessions free",
        "disclaimer": "PullUp Master is a training tool, not medical advice. Train within your ability.",
        "skip": "Skip to content",
        "f_tag": "An adaptive pull-up plan that starts at zero and rewrites itself after every session.",
        "f_product": "Product", "f_learn": "Learn", "f_legal": "Legal",
        "f_learn_links": [("/first-pull-up/", "First pull-up guide"), ("/pull-up-mistakes/", "Pull-up mistakes: 7 form errors that hold you back (and the fixes)"), ("/how-many-pull-ups-is-good/", "How many pull-ups is good? Rough standards by level"), ("/chin-up-vs-pull-up/", "Chin-up vs pull-up: what&#x27;s the difference and which should you do?"), ("/pull-up-muscles-worked/", "Pull-up muscles worked: what you&#x27;re really training"), ("/pull-up-workout-plan/", "Pull-up workout plan: a weekly routine to add reps"), ("/#faq", "FAQ"), ("/support/", "Support")],
        "f_legal_links": [("/privacy/", "Privacy"), ("/terms/", "Terms"), ("/delete-account/", "Delete account")],
        "f_rights": "All rights reserved.", "f_note": "Training tool, not medical advice.",
    },
    "de": {
        "og_locale": "de_DE", "home": "/de/", "guide": "/de/erster-klimmzug/",
        "brand_aria": "PullUp Master Startseite", "nav_aria": "Hauptnavigation", "lang_aria": "Sprache", "menu_aria": "Menü",
        "nav": ["Der Aufstieg", "So passt er sich an", "Apple Watch", "Preise", "Ratgeber"],
        "download": "Laden", "eyebrow": "Ratgeber",
        "faq_h": "Häufige Fragen", "sources_h": "Quellen", "keep_h": "Weiterlesen",
        "cta_h": "Lass den Plan mitzählen.",
        "cta_p": "PullUp Master führt genau diese Progression für dich durch: Die App setzt dich in den richtigen Block, begleitet jeden Satz mit Clips und Pausentimer und schreibt deine nächste Einheit danach neu, wie sich die letzte angefühlt hat — mit einer Schätzung, wie viele Wochen deine erste Wiederholung entfernt ist.",
        "cta_btn": "PullUp Master laden — 2 Einheiten gratis",
        "disclaimer": "PullUp Master ist ein Trainingstool, keine medizinische Beratung. Trainiere im Rahmen deiner Möglichkeiten.",
        "skip": "Zum Inhalt springen",
        "f_tag": "Ein adaptiver Klimmzug-Plan, der bei null startet und sich nach jeder Einheit neu schreibt.",
        "f_product": "Produkt", "f_learn": "Wissen", "f_legal": "Rechtliches",
        "f_learn_links": [("/de/erster-klimmzug/", "Ratgeber: erster Klimmzug"), ("/de/klimmzug-fehler/", "Klimmzug Fehler: Die 7 häufigsten und wie du sie behebst"), ("/de/wie-viele-klimmzuege-sind-gut/", "Wie viele Klimmzüge sind gut? Richtwerte nach Level"), ("/de/klimmzug-vs-chin-up/", "Klimmzug vs. Chin-up: Was ist der Unterschied?"), ("/de/klimmzug-muskeln/", "Klimmzug Muskeln: Welche Muskeln werden trainiert?"), ("/de/klimmzug-trainingsplan/", "Klimmzug Trainingsplan: So steigerst du deine Wiederholungen"), ("/de/#faq", "FAQ"), ("/support/", "Support")],
        "f_legal_links": [("/privacy/", "Datenschutz"), ("/terms/", "Nutzungsbedingungen"), ("/delete-account/", "Konto löschen")],
        "f_rights": "Alle Rechte vorbehalten.", "f_note": "Ein Trainingstool, keine medizinische Beratung.",
    },
    "tr": {
        "og_locale": "tr_TR", "home": "/tr/", "guide": "/tr/ilk-barfiks/",
        "brand_aria": "PullUp Master ana sayfa", "nav_aria": "Ana menü", "lang_aria": "Dil", "menu_aria": "Menü",
        "nav": ["Tırmanış", "Nasıl uyum sağlar", "Apple Watch", "Fiyatlar", "Rehber"],
        "download": "İndir", "eyebrow": "Rehber",
        "faq_h": "Sık sorulan sorular", "sources_h": "Kaynaklar", "keep_h": "Bunları da oku",
        "cta_h": "Saymayı plana bırak.",
        "cta_p": "PullUp Master bu ilerlemeyi senin için yürütür: seni doğru bloğa yerleştirir, her seti videolar ve dinlenme sayacıyla yönlendirir ve bir sonraki seansını öncekinin nasıl hissettirdiğine göre yeniden yazar — ilk tekrarına kaç hafta kaldığına dair tahminle birlikte.",
        "cta_btn": "PullUp Master'ı indir — 2 seans ücretsiz",
        "disclaimer": "PullUp Master bir antrenman aracıdır, tıbbi tavsiye değildir. Kendi sınırların içinde çalış.",
        "skip": "İçeriğe atla",
        "f_tag": "Sıfırdan başlayan ve her seanstan sonra kendini yeniden yazan adaptif barfiks planı.",
        "f_product": "Ürün", "f_learn": "Öğren", "f_legal": "Yasal",
        "f_learn_links": [("/tr/ilk-barfiks/", "İlk barfiks rehberi"), ("/tr/barfiks-hatalari/", "Barfiks hataları: en yaygın 7 form hatası ve nasıl düzeltilir"), ("/tr/kac-barfiks-iyi/", "Kaç barfiks iyi sayılır? Seviyelere göre rehber"), ("/tr/barfiks-vs-chin-up/", "Barfiks mi chin-up mı? Farkları ve hangisiyle başlamalı"), ("/tr/barfiks-hangi-kaslari-calistirir/", "Barfiks hangi kasları çalıştırır?"), ("/tr/barfiks-antrenman-programi/", "Barfiks antrenman programı: tekrar sayını artıran haftalık plan"), ("/tr/#faq", "FAQ"), ("/support/", "Destek")],
        "f_legal_links": [("/privacy/", "Gizlilik"), ("/terms/", "Kullanım koşulları"), ("/delete-account/", "Hesabı sil")],
        "f_rights": "Tüm hakları saklıdır.", "f_note": "Bir antrenman aracıdır, tıbbi tavsiye değildir.",
    },
    "es": {
        "og_locale": "es_ES", "home": "/es/", "guide": "/es/primera-dominada/",
        "brand_aria": "Inicio de PullUp Master", "nav_aria": "Principal", "lang_aria": "Idioma", "menu_aria": "Menú",
        "nav": ["La escalada", "Cómo se adapta", "Apple Watch", "Precios", "Guía"],
        "download": "Descargar", "eyebrow": "Guía",
        "faq_h": "Preguntas frecuentes", "sources_h": "Fuentes", "keep_h": "Sigue aprendiendo",
        "cta_h": "Deja que el plan lleve la cuenta.",
        "cta_p": "PullUp Master aplica esta misma progresión por ti: te coloca en el bloque correcto, guía cada serie con clips y temporizador de descanso y reescribe tu próxima sesión según cómo te sentiste en la anterior — con una estimación de cuántas semanas faltan para tu primera repetición.",
        "cta_btn": "Descarga PullUp Master — 2 sesiones gratis",
        "disclaimer": "PullUp Master es una herramienta de entrenamiento, no consejo médico. Entrena dentro de tus capacidades.",
        "skip": "Saltar al contenido",
        "f_tag": "Un plan de dominadas adaptativo que empieza desde cero y se reescribe después de cada sesión.",
        "f_product": "Producto", "f_learn": "Aprende", "f_legal": "Legal",
        "f_learn_links": [("/es/primera-dominada/", "Guía: tu primera dominada"), ("/es/errores-dominadas/", "Errores en las dominadas y cómo corregirlos"), ("/es/cuantas-dominadas-son-buenas/", "¿Cuántas dominadas son un buen número?"), ("/es/dominadas-vs-chin-up/", "Dominadas vs chin-ups: diferencias y cuál elegir"), ("/es/musculos-dominadas/", "¿Qué músculos trabajan las dominadas?"), ("/es/rutina-dominadas/", "Rutina de dominadas para ganar repeticiones"), ("/es/#faq", "FAQ"), ("/support/", "Soporte")],
        "f_legal_links": [("/privacy/", "Privacidad"), ("/terms/", "Términos"), ("/delete-account/", "Eliminar cuenta")],
        "f_rights": "Todos los derechos reservados.", "f_note": "Herramienta de entrenamiento, no consejo médico.",
    },
    "fr": {
        "og_locale": "fr_FR", "home": "/fr/", "guide": "/fr/premiere-traction/",
        "brand_aria": "Accueil PullUp Master", "nav_aria": "Principal", "lang_aria": "Langue", "menu_aria": "Menu",
        "nav": ["L'ascension", "Comment il s'adapte", "Apple Watch", "Tarifs", "Guide"],
        "download": "Télécharger", "eyebrow": "Guide",
        "faq_h": "Questions fréquentes", "sources_h": "Sources", "keep_h": "À lire aussi",
        "cta_h": "Laisse le plan compter pour toi.",
        "cta_p": "PullUp Master applique cette progression pour toi : il te place dans le bon bloc, guide chaque série avec des clips et un minuteur de repos, et réécrit ta prochaine séance selon ton ressenti sur la précédente — avec une estimation du nombre de semaines avant ta première répétition.",
        "cta_btn": "Télécharger PullUp Master — 2 séances offertes",
        "disclaimer": "PullUp Master est un outil d'entraînement, pas un avis médical. Entraîne-toi selon tes capacités.",
        "skip": "Aller au contenu",
        "f_tag": "Un plan de tractions adaptatif qui part de zéro et se réécrit après chaque séance.",
        "f_product": "Produit", "f_learn": "Apprendre", "f_legal": "Mentions",
        "f_learn_links": [("/fr/premiere-traction/", "Guide : ta première traction"), ("/fr/erreurs-tractions/", "Les erreurs aux tractions qui bloquent ta progression"), ("/fr/combien-de-tractions-est-bon/", "Combien de tractions est un bon niveau ?"), ("/fr/tractions-vs-chin-up/", "Tractions ou chin-up : lequel choisir ?"), ("/fr/muscles-tractions/", "Quels muscles travaillent aux tractions ?"), ("/fr/programme-tractions/", "Programme de tractions : un plan de la semaine pour progresser"), ("/fr/#faq", "FAQ"), ("/support/", "Assistance")],
        "f_legal_links": [("/privacy/", "Confidentialité"), ("/terms/", "Conditions"), ("/delete-account/", "Supprimer le compte")],
        "f_rights": "Tous droits réservés.", "f_note": "Outil d'entraînement, pas un avis médical.",
    },
}
LANG_NAMES = {"en": "English", "de": "Deutsch", "tr": "Türkçe", "es": "Español", "fr": "Français"}


def esc(s):
    return html.escape(s, quote=True).replace("&#x27;", "&#x27;")


def path_for(lang, slug):
    return f"/{slug}/" if lang == "en" else f"/{lang}/{slug}/"


def render(lang, data, slugs, today):
    t = L[lang]
    paths = {l: path_for(l, slugs[l]) for l in LANGS}
    url = SITE + paths[lang]

    hreflang = "\n".join(
        f'    <link rel="alternate" hreflang="{l}" href="{SITE}{paths[l]}" />' for l in LANGS
    ) + f'\n    <link rel="alternate" hreflang="x-default" href="{SITE}{paths["en"]}" />'

    lang_menu = "".join(
        f'<a href="{paths[l]}" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == lang else ""}><b>{l.upper()}</b> {LANG_NAMES[l]}</a>'
        for l in LANGS
    )

    article_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": data["headline"], "description": data["description"],
        "inLanguage": lang, "image": f"{SITE}/assets/img/og-image.png",
        "mainEntityOfPage": url, "datePublished": today, "dateModified": today,
        "author": {"@type": "Organization", "name": "PullUp Master"},
        "publisher": {"@type": "Organization", "name": "Qrodesk", "url": "https://qrodesk.com"},
    }
    if data.get("sources"):
        article_ld["citation"] = [{"@type": "CreativeWork", "name": s["label"], "url": s["url"]} for s in data["sources"]]
    faq_ld = {
        "@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
        "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in data["faq"]],
    }

    faq_html = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>'
        for i, f in enumerate(data["faq"])
    )
    sources_html = "".join(
        f'<li><a href="{esc(s["url"])}" rel="noopener nofollow" target="_blank">{esc(s["label"])}</a></li>' for s in data.get("sources", [])
    )
    keep_html = "".join(f'<li><a href="{esc(k["href"])}">{esc(k["title"])}</a></li>' for k in data["keep_reading"])
    f_learn = "\n".join(f'              <li><a href="{h}">{x}</a></li>' for h, x in t["f_learn_links"])
    f_legal = "\n".join(f'              <li><a href="{h}">{x}</a></li>' for h, x in t["f_legal_links"])
    nav = t["nav"]

    sources_block = ""
    if sources_html:
        sources_block = f"""
          <h2>{t["sources_h"]}</h2>
          <ol class="sources">{sources_html}</ol>
"""

    return f"""<!doctype html>
<html lang="{lang}" class="no-js">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>{esc(data["title"])}</title>
    <meta name="description" content="{esc(data["description"])}" />
    <link rel="canonical" href="{url}" />
{hreflang}
    <meta name="theme-color" content="#0a0b0d" />
    <meta name="apple-itunes-app" content="app-id=6799707900" />

    <meta property="og:type" content="article" />
    <meta property="og:site_name" content="PullUp Master" />
    <meta property="og:locale" content="{t["og_locale"]}" />
    <meta property="og:title" content="{esc(data["title"])}" />
    <meta property="og:description" content="{esc(data["description"])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE}/assets/img/og-image.png" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />

    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/icon-32.png" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <link rel="preload" href="/assets/fonts/barlow-condensed-800.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/assets/css/site.css" />
    <script>document.documentElement.classList.remove("no-js");</script>
    <script type="application/ld+json">
{json.dumps(article_ld, ensure_ascii=False, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(faq_ld, ensure_ascii=False, indent=2)}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#main">{t["skip"]}</a>

    <header class="site-header" data-open="false">
      <div class="wrap nav">
        <a class="brand" href="{t["home"]}" aria-label="{t["brand_aria"]}">
          <img src="/assets/img/icon-64.png" width="34" height="34" alt="" />
          <span>PullUp Master</span>
        </a>
        <nav id="site-nav" class="nav-links" aria-label="{t["nav_aria"]}">
          <a href="{t["home"]}#climb">{nav[0]}</a>
          <a href="{t["home"]}#adaptive">{nav[1]}</a>
          <a href="{t["home"]}#watch">{nav[2]}</a>
          <a href="{t["home"]}#pricing">{nav[3]}</a>
          <a href="{t["guide"]}">{nav[4]}</a>
        </nav>
        <div class="nav-cta">
          <details class="lang">
            <summary aria-label="{t["lang_aria"]}">{lang.upper()}</summary>
            <div class="lang-menu">{lang_menu}</div>
          </details>
          <a class="btn btn-primary btn-sm" href="{APP_STORE}" rel="noopener">{t["download"]}</a>
          <a class="btn btn-ghost btn-sm" href="{PLAY}" rel="noopener">Google Play</a>
          <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="{t["menu_aria"]}"><span></span></button>
        </div>
      </div>
    </header>

    <main id="main" class="page">
      <div class="wrap">
        <article class="page-card">
          <p class="eyebrow">{t["eyebrow"]}</p>
          <h1>{esc(data["headline"])}</h1>
          <div class="article-meta"><span>{esc(data["subtitle"])}</span><span>·</span><span>{esc(data["read_time"])}</span></div>

          <p class="lede" style="margin-top: 0">{esc(data["lede"])}</p>

          {data["body_html"].strip()}

          <h2>{t["faq_h"]}</h2>
          <div class="faq">{faq_html}</div>
{sources_block}
          <h2>{t["keep_h"]}</h2>
          <ul>{keep_html}</ul>

          <div class="inline-cta">
            <h2>{t["cta_h"]}</h2>
            <p>{t["cta_p"]}</p>
            <div class="cta-row" style="margin-top: 24px">
              <a class="btn btn-primary" href="{APP_STORE}" rel="noopener">{t["cta_btn"]}</a>
              <a class="btn btn-ghost play-alt" href="{PLAY}" rel="noopener">Google Play</a>
            </div>
          </div>

          <p class="muted" style="margin-top: 40px; font-size: 14px">{t["disclaimer"]}</p>
        </article>
      </div>
    </main>


    <footer class="footer">
      <div class="wrap">
        <div class="footer-grid">
          <div>
            <a class="brand" href="{t["home"]}"><img src="/assets/img/icon-64.png" width="34" height="34" alt="" loading="lazy" /><span>PullUp Master</span></a>
            <p class="tag">{t["f_tag"]}</p>
          </div>
          <div>
            <h4>{t["f_product"]}</h4>
            <ul>
              <li><a href="{t["home"]}#climb">{nav[0]}</a></li>
              <li><a href="{t["home"]}#watch">{nav[2]}</a></li>
              <li><a href="{t["home"]}#pricing">{nav[3]}</a></li>
              <li><a href="{APP_STORE}" rel="noopener">App Store</a></li>
              <li><a href="{PLAY}" rel="noopener">Google Play</a></li>
            </ul>
          </div>
          <div>
            <h4>{t["f_learn"]}</h4>
            <ul>
{f_learn}
            </ul>
          </div>
          <div>
            <h4>{t["f_legal"]}</h4>
            <ul>
{f_legal}
              <li><a href="https://qrodesk.com/impressum.html" rel="noopener">Impressum</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <span>© <span data-year>2026</span> Qrodesk. {t["f_rights"]}</span>
          <span>{t["f_note"]}</span>
        </div>
      </div>
    </footer>

    <script src="/assets/js/site.js" defer></script>
  </body>
</html>
"""


def validate(doc):
    errs, warns = [], []
    for l in LANGS:
        if l not in doc.get("slugs", {}):
            errs.append(f"slugs.{l} missing")
        elif not re.fullmatch(r"[a-z0-9-]+", doc["slugs"][l]):
            errs.append(f"slugs.{l} must be lowercase ascii + hyphens: {doc['slugs'][l]}")
        d = doc.get("langs", {}).get(l)
        if not d:
            errs.append(f"langs.{l} missing")
            continue
        for k in ["title", "description", "headline", "subtitle", "read_time", "lede", "body_html", "faq", "keep_reading", "sources"]:
            if k not in d:
                errs.append(f"{l}.{k} missing")
        if errs:
            continue
        if len(d["title"]) > 65:
            warns.append(f"{l}.title is {len(d['title'])} chars (aim <=60)")
        if not 100 <= len(d["description"]) <= 170:
            warns.append(f"{l}.description is {len(d['description'])} chars (aim 120-160)")
        if not 4 <= len(d["faq"]) <= 6:
            warns.append(f"{l}.faq has {len(d['faq'])} items (aim 4-6)")
        if len(d["sources"]) < 3:
            warns.append(f"{l}.sources has {len(d['sources'])} items (aim >=3)")
        if not 3 <= len(d["keep_reading"]) <= 6:
            warns.append(f"{l}.keep_reading has {len(d['keep_reading'])} items (aim 4-6)")
        words = len(re.sub(r"<[^>]+>", " ", d["body_html"]).split())
        if words < 900:
            warns.append(f"{l}.body_html has {words} words (aim 1100-1600)")
        bad_tags = set(re.findall(r"<(?!/?(?:h2|h3|p|ul|ol|li|table|thead|tbody|tr|th|td|strong|em|a|br|div|sup)\b)([a-zA-Z0-9]+)", d["body_html"]))
        if bad_tags:
            warns.append(f"{l}.body_html uses unexpected tags: {sorted(bad_tags)}")
        if "<h1" in d["body_html"]:
            errs.append(f"{l}.body_html must not contain <h1>")
        for k in d["keep_reading"]:
            href = k["href"]
            if href.startswith("/"):
                p = os.path.join(ROOT, href.strip("/"), "index.html")
                if not os.path.exists(p):
                    errs.append(f"{l}.keep_reading link target does not exist: {href}")
            if l != "en" and not href.startswith(f"/{l}/"):
                warns.append(f"{l}.keep_reading link is not in /{l}/: {href}")
            if l == "en" and re.match(r"/(de|tr|es|fr)/", href):
                warns.append(f"en.keep_reading link points to another language: {href}")
        for href in re.findall(r'href="(/[^"#]*)"', d["body_html"]):
            p = os.path.join(ROOT, href.strip("/"), "index.html")
            if not os.path.exists(p):
                errs.append(f"{l}.body_html internal link target does not exist: {href}")
        for s in d["sources"]:
            if not s["url"].startswith("https://"):
                errs.append(f"{l}.sources url must be https: {s['url']}")
        print(f"  {l}: {words} body words, {len(d['faq'])} FAQ, {len(d['sources'])} sources, {len(d['keep_reading'])} keep-reading")
    return errs, warns


def update_sitemap(urls, priority):
    p = os.path.join(ROOT, "sitemap.xml")
    xml = open(p, encoding="utf-8").read()
    added = []
    for u in urls:
        if f"<loc>{u}</loc>" in xml:
            continue
        xml = xml.replace("</urlset>", f"  <url><loc>{u}</loc><priority>{priority}</priority></url>\n</urlset>")
        added.append(u)
    open(p, "w", encoding="utf-8").write(xml)
    return added


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    src = sys.argv[1]
    check_only = "--check" in sys.argv
    doc = json.load(open(src, encoding="utf-8"))
    print(f"Validating {src}")
    errs, warns = validate(doc)
    for w in warns:
        print(f"  WARN {w}")
    for e in errs:
        print(f"  ERROR {e}")
    if errs:
        sys.exit(1)
    if check_only:
        print("OK (check only)")
        return
    today = datetime.date.today().isoformat()
    urls = []
    for l in LANGS:
        rel = path_for(l, doc["slugs"][l])
        out_dir = os.path.join(ROOT, rel.strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "index.html")
        open(out, "w", encoding="utf-8").write(render(l, doc["langs"][l], doc["slugs"], today))
        urls.append(SITE + rel)
        print(f"  wrote {os.path.relpath(out, ROOT)}")
    added = update_sitemap(urls, doc.get("priority", "0.8"))
    print(f"  sitemap: {len(added)} URL(s) added")
    print("URLS")
    for u in urls:
        print(u)


if __name__ == "__main__":
    main()
