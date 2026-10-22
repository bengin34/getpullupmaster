(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");

  // Header turns solid once the page scrolls under it.
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }


  // Mobile: the header Download button is hidden, so keep both store links pinned to the bottom.
  const storeLabels = { en: "Download", de: "Laden", es: "Descargar", fr: "Télécharger", tr: "İndir" };
  const pageLang = (document.documentElement.lang || "en").slice(0, 2);
  const bar = document.createElement("div");
  bar.className = "sticky-cta";
  bar.innerHTML =
    '<a class="btn btn-primary" href="https://apps.apple.com/app/id6799707900" rel="noopener">' +
    (storeLabels[pageLang] || storeLabels.en) + " · App Store</a>" +
    '<a class="btn btn-ghost" href="https://play.google.com/store/apps/details?id=com.pullup.master" rel="noopener">Google Play</a>';
  document.body.appendChild(bar);

  // Mobile menu.
  if (header && toggle) {
    const setOpen = (open) => {
      header.setAttribute("data-open", String(open));
      toggle.setAttribute("aria-expanded", String(open));
    };
    toggle.addEventListener("click", () => setOpen(header.getAttribute("data-open") !== "true"));
    header.querySelectorAll(".nav-links a").forEach((link) => link.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setOpen(false);
    });
  }

  // Reveal-on-scroll. Without IntersectionObserver everything just shows.
  const revealables = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    revealables.forEach((node) => observer.observe(node));
  } else {
    revealables.forEach((node) => node.classList.add("is-in"));
  }

  // "How did it feel?" demo — copy lives on the buttons so each locale ships its own.
  const board = document.querySelector("[data-feedback]");
  if (board) {
    const buttons = board.querySelectorAll("[data-rate]");
    const pain = board.querySelector("[data-pain]");
    const arrow = board.querySelector(".fb-result [data-arrow]");
    const result = board.querySelector("[data-result]");
    let rated = board.querySelector('[data-rate][aria-pressed="true"]');

    const render = () => {
      const source = pain && pain.getAttribute("aria-pressed") === "true" ? pain : rated;
      if (!source) return;
      arrow.textContent = source.dataset.arrow;
      result.innerHTML = source.dataset.msg;
    };

    buttons.forEach((button) =>
      button.addEventListener("click", () => {
        rated = button;
        buttons.forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
        render();
      })
    );
    if (pain) {
      pain.addEventListener("click", () => {
        pain.setAttribute("aria-pressed", String(pain.getAttribute("aria-pressed") !== "true"));
        render();
      });
    }
  }

  // Close the language menu on outside click.
  const lang = document.querySelector("details.lang");
  if (lang) {
    document.addEventListener("click", (event) => {
      if (lang.open && !lang.contains(event.target)) lang.open = false;
    });
  }

  // Screenshot gallery arrows.
  const track = document.querySelector("[data-gallery-track]");
  if (track) {
    document.querySelectorAll("[data-gallery]").forEach((button) =>
      button.addEventListener("click", () => {
        const step = track.clientWidth * 0.8 * Number(button.dataset.gallery);
        track.scrollBy({ left: step, behavior: "smooth" });
      })
    );
  }

  document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });
})();
