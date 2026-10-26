(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");

  // Header turns solid once the page scrolls under it.
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }


  // Mobile: the header store buttons are hidden, so keep both store links pinned to the bottom.
  const bar = document.createElement("div");
  bar.className = "sticky-cta";
  const svg = (d) => '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="' + d + '"/></svg>';
  bar.innerHTML =
    '<a class="store-btn store-btn-sm" href="https://apps.apple.com/app/id6799707900" rel="noopener">' +
    svg("M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.77-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-2.99-.79-1.54.02-2.96.9-3.75 2.27-1.6 2.78-.41 6.9 1.15 9.15.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.24-.02 2.02-1.12 2.77-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.4-.92-2.41-3.66zM14.1 5.86c.63-.77 1.06-1.83.94-2.89-.91.04-2.01.61-2.66 1.37-.58.67-1.09 1.76-.96 2.79 1.02.08 2.05-.52 2.68-1.27z") + "<strong>App Store</strong></a>" +
    '<a class="store-btn store-btn-sm" href="https://play.google.com/store/apps/details?id=com.pullup.master" rel="noopener">' +
    svg("M3.6 2.3c-.3.3-.5.8-.5 1.4v16.6c0 .6.2 1.1.5 1.4l.1.1 9.3-9.3v-.2L3.7 2.2l-.1.1zm12.4 12.5-3.1-3.1v-.2L16 8.4l.1.1 3.7 2.1c1 .6 1 1.6 0 2.2l-3.7 2.1-.1-.1zm.1.1L12.9 11.7 3.6 21c.3.4.9.4 1.5.1l11-6.2zm0-6.2L5.1 2.5c-.6-.3-1.2-.3-1.5.1l9.3 9.2 3.2-3.2z") + "<strong>Google Play</strong></a>";
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
