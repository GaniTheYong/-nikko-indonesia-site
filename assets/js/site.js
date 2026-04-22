const toggle = document.querySelector(".menu-toggle");
const nav = document.querySelector(".site-nav");
const navLinks = document.querySelectorAll(".site-nav a");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

const contactForm = document.querySelector("#contact-form");

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const name = String(formData.get("name") || "").trim();
    const email = String(formData.get("email") || "").trim();
    const phone = String(formData.get("phone") || "").trim();
    const message = String(formData.get("message") || "").trim();

    const subject = encodeURIComponent(`Website Inquiry from ${name || "Nikko Indonesia Contact Form"}`);
    const body = encodeURIComponent(
      [
        `Name / Nama: ${name}`,
        `E-mail / Surel: ${email}`,
        `Phone / Telepon: ${phone}`,
        "",
        "Message / Pertanyaan Maupun Komentar:",
        message,
      ].join("\n")
    );

    window.location.href = `mailto:admin@nikko-indonesia.co.id,yana@nikko-indonesia.co.id?subject=${subject}&body=${body}`;
  });
}
