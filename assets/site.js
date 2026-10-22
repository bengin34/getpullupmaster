(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (header && toggle) {
    toggle.addEventListener("click", () => {
      const isOpen = header.getAttribute("data-open") === "true";
      header.setAttribute("data-open", String(!isOpen));
      toggle.setAttribute("aria-expanded", String(!isOpen));
    });
  }

  if (header && navLinks) {
    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        header.setAttribute("data-open", "false");
        if (toggle) {
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    });
  }

  document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = new Date().getFullYear();
  });
})();
