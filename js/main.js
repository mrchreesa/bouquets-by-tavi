// ── Configuration ────────────────────────────────────────────────
// Create a free form at https://formspree.io and paste its ID here.
const FORMSPREE_ID = "YOUR_FORM_ID";
const FALLBACK_EMAIL = "hello@bouquetsbytavi.com";

// ── Mobile navigation ────────────────────────────────────────────
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.getElementById("nav-menu");

navToggle.addEventListener("click", () => {
  const open = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!open));
  navMenu.classList.toggle("open", !open);
});

navMenu.addEventListener("click", (event) => {
  if (event.target.closest("a")) {
    navToggle.setAttribute("aria-expanded", "false");
    navMenu.classList.remove("open");
  }
});

// ── Pre-selection from bouquet cards and occasion tiles ──────────
const bouquetSelect = document.getElementById("bouquet");
const occasionSelect = document.getElementById("occasion");
const enquirySection = document.getElementById("enquiry");

function scrollToForm() {
  enquirySection.scrollIntoView({ behavior: "smooth" });
}

document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    bouquetSelect.value = button.dataset.bouquet;
    scrollToForm();
  });
});

document.querySelectorAll(".occasion-tile").forEach((tile) => {
  tile.addEventListener("click", () => {
    occasionSelect.value = tile.dataset.occasion;
    scrollToForm();
  });
});

// ── Enquiry form ─────────────────────────────────────────────────
const form = document.getElementById("enquiry-form");
const statusEl = form.querySelector(".form-status");
const successEl = document.getElementById("form-success");

function setFieldError(input, show) {
  const error = input.closest(".field").querySelector(".field-error");
  if (error) error.hidden = !show;
  input.setAttribute("aria-invalid", String(show));
}

function validate() {
  const email = form.elements.email;
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
  const checks = [
    [form.elements.name, form.elements.name.value.trim() !== ""],
    [email, emailOk],
    [form.elements.message, form.elements.message.value.trim() !== ""],
  ];
  let valid = true;
  for (const [input, ok] of checks) {
    setFieldError(input, !ok);
    if (!ok) valid = false;
  }
  return valid;
}

["name", "email", "message"].forEach((id) => {
  form.elements[id].addEventListener("input", () => setFieldError(form.elements[id], false));
});

function showStatus(text, isError) {
  statusEl.textContent = text;
  statusEl.hidden = false;
  statusEl.classList.toggle("error", isError);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.hidden = true;

  if (!validate()) {
    form.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  if (FORMSPREE_ID === "YOUR_FORM_ID") {
    showStatus(`The enquiry form isn't connected yet — please email us at ${FALLBACK_EMAIL}.`, true);
    return;
  }

  const submitButton = form.querySelector('[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = "Sending…";

  try {
    const response = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`Formspree responded ${response.status}`);
    form.hidden = true;
    successEl.hidden = false;
    successEl.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch {
    showStatus(`Something went wrong sending your enquiry — please try again, or email us at ${FALLBACK_EMAIL}.`, true);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Send Enquiry";
  }
});
