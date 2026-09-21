document.getElementById("year").textContent = new Date().getFullYear();

// Mobile nav toggle
const navToggle = document.querySelector(".nav-toggle");
if (navToggle) {
  navToggle.addEventListener("click", () => {
    const isOpen = document.body.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  document.querySelectorAll(".mobile-nav a").forEach((link) => {
    link.addEventListener("click", () => {
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

// FAQ accordion
document.querySelectorAll(".faq-question").forEach((button) => {
  const answer = button.nextElementSibling;
  button.addEventListener("click", () => {
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    answer.style.maxHeight = isOpen ? "0px" : `${answer.scrollHeight}px`;
  });
});

// Waitlist forms
// NOTE: This is a front-end-only stub. Wire the fetch call below to your
// email service (e.g. a Mailchimp/ConvertKit/Beehiiv form endpoint, or your
// own API route) before launch.
function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function handleWaitlistSubmit(formId, noteId) {
  const form = document.getElementById(formId);
  const note = document.getElementById(noteId);
  if (!form || !note) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = form.querySelector('input[type="email"]');
    const email = input.value.trim();

    if (!isValidEmail(email)) {
      note.textContent = "Please enter a valid email address.";
      return;
    }

    // TODO: replace with a real request to your email service provider.
    note.textContent = "You're on the list — check your inbox for a confirmation soon.";
    form.reset();
  });
}

handleWaitlistSubmit("waitlist-form", "hero-form-note");
handleWaitlistSubmit("final-form", "final-form-note");
