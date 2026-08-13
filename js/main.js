// ── Configuration ────────────────────────────────────────────────
const FALLBACK_EMAIL = "flowersbytavi@outlook.com";
const API_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:3001/submit-form"
    : "https://flowers-by-tavi-api.vercel.app/submit-form";

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

// ── Hero CTA dropdown ─────────────────────────────────────────────
document.querySelectorAll(".hero-cta-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    link.closest(".hero-cta").removeAttribute("open");
  });
});

// ── Product photo carousels ──────────────────────────────────────
document.querySelectorAll(".card-carousel").forEach((carousel) => {
  const images = carousel.querySelectorAll(".carousel-track img");
  const dots = carousel.querySelectorAll(".carousel-dot");
  let activeIndex = 0;

  function show(nextIndex) {
    images[activeIndex].classList.remove("is-active");
    dots[activeIndex].classList.remove("is-active");
    activeIndex = (nextIndex + images.length) % images.length;
    images[activeIndex].classList.add("is-active");
    dots[activeIndex].classList.add("is-active");
  }

  carousel.querySelector(".carousel-prev").addEventListener("click", () => show(activeIndex - 1));
  carousel.querySelector(".carousel-next").addEventListener("click", () => show(activeIndex + 1));
  dots.forEach((dot, dotIndex) => dot.addEventListener("click", () => show(dotIndex)));
});

// ── Pre-selection from bouquet cards and occasion tiles ──────────
const bouquetSelect = document.getElementById("bouquet");
const occasionSelect = document.getElementById("occasion");
const enquirySection = document.getElementById("enquiry");

function scrollToForm() {
  enquirySection.scrollIntoView({ behavior: "smooth" });
}

// ── Enquiry intent paths ─────────────────────────────────────────
const COLLECTION = "Order from the collection";
const CUSTOM = "Design something custom";

const pathFieldsets = {
  [COLLECTION]: document.getElementById("path-collection"),
  [CUSTOM]: document.getElementById("path-custom"),
};
const enquiryDetails = document.getElementById("enquiry-details");
const messageField = document.getElementById("message");
const messageLabel = document.querySelector('label[for="message"]');

// The message field does double duty: an optional extras box when ordering a
// listed piece, and the required design brief when commissioning something new.
const MESSAGE_COPY = {
  [COLLECTION]: {
    label: 'Anything else <span class="optional">(optional)</span>',
    placeholder: "Size, colours, a note for the card…",
    required: false,
  },
  [CUSTOM]: {
    label: 'What you have in mind <span aria-hidden="true">*</span>',
    placeholder: "Colours, style, who it's for…",
    required: true,
  },
};

function selectedIntent() {
  return document.querySelector('input[name="intent"]:checked')?.value || "";
}

function applyIntent() {
  const intent = selectedIntent();
  for (const [value, fieldset] of Object.entries(pathFieldsets)) {
    const active = value === intent;
    fieldset.hidden = !active;
    // `disabled` keeps the inactive path out of FormData entirely, so a
    // submission never carries both paths' keys.
    fieldset.disabled = !active;
  }
  enquiryDetails.hidden = intent === "";

  // Switching paths changes which fields are required, so any error raised for the
  // previous path is now meaningless — and would otherwise sit stale under a
  // relabelled field, or reappear when the user switches back. Clear them all.
  document.querySelectorAll("#enquiry-form .field-error").forEach((error) => {
    error.hidden = true;
  });
  document.querySelectorAll('#enquiry-form [aria-invalid="true"]').forEach((field) => {
    field.setAttribute("aria-invalid", "false");
  });

  const copy = MESSAGE_COPY[intent];
  if (copy) {
    messageLabel.innerHTML = copy.label;
    messageField.placeholder = copy.placeholder;
    messageField.required = copy.required;
  }
}

document.querySelectorAll('input[name="intent"]').forEach((radio) => {
  radio.addEventListener("change", applyIntent);
});
applyIntent();

document.querySelectorAll(".enquire-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const collectionRadio = document.querySelector(
      `input[name="intent"][value="${COLLECTION}"]`
    );
    collectionRadio.checked = true;
    applyIntent();
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
const submitButton = form.querySelector('[type="submit"]');
const submitLabel = submitButton.textContent;

function setFieldError(input, show) {
  const error = input.closest(".field").querySelector(".field-error");
  if (error) error.hidden = !show;
  input.setAttribute("aria-invalid", String(show));
}

function validate() {
  const email = form.elements.email;
  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());
  const intent = selectedIntent();
  const checks = [
    [form.elements.name, form.elements.name.value.trim() !== ""],
    [email, emailOk],
  ];
  if (intent === COLLECTION) {
    checks.push([form.elements.bouquet, form.elements.bouquet.value !== ""]);
  }
  if (intent === CUSTOM) {
    checks.push([form.elements.message, form.elements.message.value.trim() !== ""]);
  }
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

bouquetSelect.addEventListener("change", () => setFieldError(bouquetSelect, false));

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

  const turnstileToken = form.querySelector('[name="cf-turnstile-response"]')?.value || "";
  if (!turnstileToken) {
    showStatus("Please complete the verification check above, then try again.", true);
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Sending…";

  const payload = Object.fromEntries(new FormData(form));
  payload.turnstileToken = turnstileToken;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json().catch(() => ({}));

    if (response.ok && data.success) {
      form.hidden = true;
      successEl.hidden = false;
      successEl.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }

    // Distinct messages: "try again later" and "we couldn't verify you" call for
    // different actions from the visitor than a generic failure does.
    if (response.status === 429 || response.status === 403) {
      showStatus(data.error || "Please try again in a little while.", true);
    } else if (response.status === 400 && Array.isArray(data.fields)) {
      data.fields.forEach((id) => {
        if (form.elements[id]) setFieldError(form.elements[id], true);
      });
      showStatus(data.error || "Please check your details.", true);
    } else {
      throw new Error(`API responded ${response.status}`);
    }
  } catch {
    showStatus(
      `Something went wrong sending your enquiry — please try again, or email us at ${FALLBACK_EMAIL}.`,
      true
    );
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = submitLabel;
    if (window.turnstile) window.turnstile.reset();
  }
});
