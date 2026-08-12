# Enquiry Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the enquiry form on flowersbytavi.co.uk actually deliver enquiries, by replacing the never-connected Formspree placeholder with a self-hosted Vercel serverless API that screens submissions for bots and emails them on.

**Architecture:** Two repos. The public static site (`bouquets-by-tavi`, GitHub Pages) keeps its markup and posts JSON to a new **private** API repo deployed as its own Vercel project. The API is a single Express app (`server.js`) exported for `@vercel/node`, mirroring the existing Fresh & Clean backend so it is familiar to maintain. Requests pass five checks in a deliberate order — origin, honeypot, Turnstile, rate limit, validation — before nodemailer sends via Gmail. The cheap local checks run first so junk traffic never costs an outbound API call or email quota.

**Tech Stack:** Node 20+, Express 4, nodemailer 6, `@upstash/redis`, Cloudflare Turnstile, Vercel serverless, vanilla ES6 on the frontend.

## Global Constraints

- **Secrets never enter git.** Both repos must have `.env` git-ignored before any `.env` is created. The API repo carries a committed `.env.example` with placeholder values only. Never print a real secret value into a report, commit message, or terminal output that gets captured.
- **Environment variable names, exactly:** `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `MAIL_TO`, `TURNSTILE_SECRET`, `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`, `ALLOWED_ORIGINS`.
- **Field names sent by the frontend, exactly:** `intent`, `bouquet`, `budget`, `occasion`, `needed_by`, `fulfilment`, `name`, `email`, `message`, plus `turnstileToken` and the honeypot `website`. These match the existing form's `name` attributes — do not rename them.
- **`intent` values, exactly:** `Order from the collection` and `Design something custom`. These are matched verbatim in both repos.
- **Do NOT allowlist product names, occasions, budgets or fulfilment values** on the server. They are length-capped and sanitised only. Allowlisting would put the product catalogue in two repos, so a routine rename in `index.html` would silently reject real enquiries. Only `intent` is allowlisted, because it is structural.
- **Rate limits:** 10 submissions per IP per hour, 30 per IP per day.
- **Payload cap:** 16 KB. Field caps: `name` 100, `email` 254, `message` 5000, everything else 100 characters.
- **Strip CR and LF** from any value that reaches an email header (the subject line). This is a real bug in the Fresh & Clean original.
- **The site repo is PUBLIC and auto-deploys to flowersbytavi.co.uk on push to `main`.** Treat any push as instantly live. Do not push without explicit approval.
- **Local preview** of the site: `python3 -m http.server 8123` from the site repo root. Never port 8000 — another project owns it. This environment's browser has served STALE `js/main.js` through normal cache-bypass methods; always navigate with a cache-busted URL (`?cb=<timestamp>`) and confirm current code is running before trusting a result.

## Human prerequisites

Tasks 4, 6 and 7 cannot complete without these. They are the user's to create — do not attempt to sign up on their behalf.

| Needed | Where | Used by |
|---|---|---|
| Gmail account with 2FA + **app password** | Google Account → Security → App passwords | Task 4 |
| Cloudflare account + Turnstile site/secret keys | dash.cloudflare.com → Turnstile | Task 6 |
| Upstash account + Redis database (REST URL + token) | console.upstash.com | Task 7 |
| Vercel account | vercel.com | Task 9 |

If a credential is unavailable when a task needs it, report `BLOCKED` naming the missing credential rather than inventing a placeholder and marking the task done.

---

### Task 1: Scaffold the API repo with secrets protection first

**Files:**
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/.gitignore`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/.env.example`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/package.json`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/vercel.json`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/README.md`

**Interfaces:**
- Produces: the repo root every later task works in, and the exact env var names they read.

`.gitignore` is created in the FIRST commit, before any `.env` can exist. The Fresh & Clean repo has a real `.env` holding live credentials and no `.gitignore` at all — protected only by nobody having run `git add -A`. That is the mistake this ordering prevents.

- [ ] **Step 1: Create the directory and initialise git**

```bash
mkdir -p ~/Desktop/WebM8/flowers-by-tavi-api
cd ~/Desktop/WebM8/flowers-by-tavi-api
git init
```

- [ ] **Step 2: Write `.gitignore` BEFORE anything else**

Create `.gitignore`:
```
node_modules/
.env
.env.*
!.env.example
.vercel
.DS_Store
```

- [ ] **Step 3: Write `.env.example`**

Placeholder values only — never real credentials.
```
# Gmail account used to send. Requires 2FA and an app password.
GMAIL_USER=youraccount@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Where enquiries are delivered.
MAIL_TO=flowersbytavi@outlook.com

# Cloudflare Turnstile secret key (server-side verification).
TURNSTILE_SECRET=0x0000000000000000000000000000000000

# Upstash Redis REST credentials for rate limiting.
UPSTASH_REDIS_REST_URL=https://example.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx

# Comma-separated list of origins allowed to POST.
ALLOWED_ORIGINS=https://flowersbytavi.co.uk,https://www.flowersbytavi.co.uk,http://localhost:8123
```

- [ ] **Step 4: Write `package.json`**

```json
{
  "name": "flowers-by-tavi-api",
  "version": "1.0.0",
  "private": true,
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "@upstash/redis": "^1.34.3",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.21.1",
    "nodemailer": "^6.9.16"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

- [ ] **Step 5: Write `vercel.json`**

```json
{
  "version": 2,
  "builds": [
    { "src": "server.js", "use": "@vercel/node" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/server.js" }
  ]
}
```

Note: unlike the Fresh & Clean `vercel.json`, no CORS headers are set here. They are handled in `server.js` against `ALLOWED_ORIGINS`, so there is one place to reason about, not two that can disagree.

- [ ] **Step 6: Write `README.md`**

```markdown
# Flowers by Tavi — Enquiry API

Serverless backend for the enquiry form on flowersbytavi.co.uk.
The site itself lives in the public `bouquets-by-tavi` repo; this repo is
private because it contains the anti-spam logic.

## Local development

    npm install
    cp .env.example .env    # then fill in real values
    npm start               # listens on http://localhost:3001

## Environment variables

See `.env.example`. All are required. In production they are set in the
Vercel project settings, never committed.

## Endpoints

- `GET  /api/health`   — returns `{ status: "ok" }`
- `POST /submit-form`  — accepts an enquiry, returns `{ success: true }`
```

- [ ] **Step 7: Install dependencies and commit**

```bash
npm install
git add .gitignore .env.example package.json package-lock.json vercel.json README.md
git commit -m "chore: scaffold enquiry API with secrets ignored from the first commit"
```

- [ ] **Step 8: Verify nothing sensitive is tracked**

```bash
git ls-files
```
Expected: exactly `.gitignore`, `.env.example`, `README.md`, `package-lock.json`, `package.json`, `vercel.json`. No `.env`, no `node_modules/`.

```bash
git check-ignore -q .env && echo "IGNORED"
```
Expected: `IGNORED`.

---

### Task 2: Validation and sanitisation module

**Files:**
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/lib/validate.js`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/test/validate.test.js`

**Interfaces:**
- Produces: `validateEnquiry(body)` returning `{ valid: boolean, errors: string[], clean: object }`. Task 5 consumes this.
- Produces: `stripHeader(value)` returning a string with CR/LF removed and trimmed. Task 5 uses it on the subject line.

This is pure logic with no I/O, so it gets real automated tests. Node 20 has a built-in test runner — no test framework to install.

- [ ] **Step 1: Write the failing tests**

Create `test/validate.test.js`:
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { validateEnquiry, stripHeader } = require("../lib/validate");

const COLLECTION = "Order from the collection";
const CUSTOM = "Design something custom";

function base(extra) {
  return Object.assign({ name: "Ada", email: "ada@example.com" }, extra);
}

test("accepts a valid collection enquiry", () => {
  const r = validateEnquiry(base({ intent: COLLECTION, bouquet: "Luxury Rose Box" }));
  assert.strictEqual(r.valid, true);
  assert.deepStrictEqual(r.errors, []);
  assert.strictEqual(r.clean.bouquet, "Luxury Rose Box");
});

test("accepts a valid custom enquiry", () => {
  const r = validateEnquiry(base({ intent: CUSTOM, message: "Pastel tones please" }));
  assert.strictEqual(r.valid, true);
});

test("rejects a missing name", () => {
  const r = validateEnquiry({ intent: CUSTOM, email: "a@b.co", message: "hi" });
  assert.strictEqual(r.valid, false);
  assert.ok(r.errors.includes("name"));
});

test("rejects a malformed email", () => {
  const r = validateEnquiry(base({ intent: CUSTOM, email: "not-an-email", message: "hi" }));
  assert.strictEqual(r.valid, false);
  assert.ok(r.errors.includes("email"));
});

test("rejects an unknown intent", () => {
  const r = validateEnquiry(base({ intent: "Something else" }));
  assert.strictEqual(r.valid, false);
  assert.ok(r.errors.includes("intent"));
});

test("requires bouquet only on the collection path", () => {
  const missing = validateEnquiry(base({ intent: COLLECTION }));
  assert.strictEqual(missing.valid, false);
  assert.ok(missing.errors.includes("bouquet"));

  const notRequired = validateEnquiry(base({ intent: CUSTOM, message: "hi" }));
  assert.strictEqual(notRequired.valid, true);
});

test("requires message only on the custom path", () => {
  const missing = validateEnquiry(base({ intent: CUSTOM }));
  assert.strictEqual(missing.valid, false);
  assert.ok(missing.errors.includes("message"));

  const notRequired = validateEnquiry(base({ intent: COLLECTION, bouquet: "Blush Basket" }));
  assert.strictEqual(notRequired.valid, true);
});

test("accepts any product name — the catalogue is not allowlisted", () => {
  const r = validateEnquiry(base({ intent: COLLECTION, bouquet: "A Product Renamed Yesterday" }));
  assert.strictEqual(r.valid, true);
});

test("rejects an over-long message", () => {
  const r = validateEnquiry(base({ intent: CUSTOM, message: "x".repeat(5001) }));
  assert.strictEqual(r.valid, false);
  assert.ok(r.errors.includes("message"));
});

test("drops unknown fields from clean output", () => {
  const r = validateEnquiry(base({ intent: CUSTOM, message: "hi", sneaky: "payload" }));
  assert.strictEqual(r.clean.sneaky, undefined);
});

test("stripHeader removes CR and LF", () => {
  assert.strictEqual(stripHeader("Ada\r\nBcc: victim@example.com"), "AdaBcc: victim@example.com");
  assert.strictEqual(stripHeader("  spaced  "), "spaced");
});

test("stripHeader tolerates non-strings", () => {
  assert.strictEqual(stripHeader(undefined), "");
  assert.strictEqual(stripHeader(null), "");
});
```

- [ ] **Step 2: Run the tests to confirm they fail**

```bash
node --test test/
```
Expected: FAIL — `Cannot find module '../lib/validate'`.

- [ ] **Step 3: Implement the module**

Create `lib/validate.js`:
```js
const COLLECTION = "Order from the collection";
const CUSTOM = "Design something custom";

const LIMITS = {
  name: 100,
  email: 254,
  message: 5000,
  bouquet: 100,
  budget: 100,
  occasion: 100,
  needed_by: 100,
  fulfilment: 100,
};

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Anything reaching an email header must not carry CR/LF, or a crafted name
// could inject extra headers (Bcc, etc.) into the outgoing message.
function stripHeader(value) {
  if (typeof value !== "string") return "";
  return value.replace(/[\r\n]/g, "").trim();
}

function asString(value) {
  return typeof value === "string" ? value.trim() : "";
}

function validateEnquiry(body) {
  const src = body && typeof body === "object" ? body : {};
  const errors = [];
  const clean = {};

  // Only known fields survive, so a crafted payload cannot add lines to the email.
  for (const field of Object.keys(LIMITS)) {
    const value = asString(src[field]);
    if (value.length > LIMITS[field]) errors.push(field);
    if (value) clean[field] = value;
  }

  const intent = asString(src.intent);
  if (intent !== COLLECTION && intent !== CUSTOM) {
    errors.push("intent");
  } else {
    clean.intent = intent;
  }

  if (!clean.name) errors.push("name");
  if (!clean.email || !EMAIL_RE.test(clean.email)) errors.push("email");

  // Required fields differ by path, mirroring what the form actually shows.
  if (intent === COLLECTION && !clean.bouquet) errors.push("bouquet");
  if (intent === CUSTOM && !clean.message) errors.push("message");

  return { valid: errors.length === 0, errors: [...new Set(errors)], clean };
}

module.exports = { validateEnquiry, stripHeader, COLLECTION, CUSTOM, LIMITS };
```

- [ ] **Step 4: Run the tests to confirm they pass**

```bash
node --test test/
```
Expected: PASS, 12 tests.

- [ ] **Step 5: Commit**

```bash
git add lib/validate.js test/validate.test.js
git commit -m "feat: add enquiry validation and header sanitisation"
```

---

### Task 3: Rate limiter module

**Files:**
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/lib/rate-limit.js`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/test/rate-limit.test.js`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `checkRateLimit(redis, ip)` returning `{ allowed: boolean, reason: string|null }`. Task 5 consumes this. `redis` is any object exposing `incr(key)` and `expire(key, seconds)`, which is the shape `@upstash/redis` provides — this keeps the module testable with a fake and free of network calls.

- [ ] **Step 1: Write the failing tests**

Create `test/rate-limit.test.js`:
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { checkRateLimit, HOURLY_MAX, DAILY_MAX } = require("../lib/rate-limit");

function fakeRedis(counts) {
  const store = Object.assign({}, counts);
  const expires = [];
  return {
    store,
    expires,
    async incr(key) {
      store[key] = (store[key] || 0) + 1;
      return store[key];
    },
    async expire(key, seconds) {
      expires.push([key, seconds]);
      return 1;
    },
  };
}

test("allows a first submission", async () => {
  const r = await checkRateLimit(fakeRedis({}), "1.2.3.4");
  assert.strictEqual(r.allowed, true);
  assert.strictEqual(r.reason, null);
});

test("blocks once the hourly limit is exceeded", async () => {
  const redis = fakeRedis({});
  for (let i = 0; i < HOURLY_MAX; i++) await checkRateLimit(redis, "1.2.3.4");
  const r = await checkRateLimit(redis, "1.2.3.4");
  assert.strictEqual(r.allowed, false);
  assert.strictEqual(r.reason, "hourly");
});

test("blocks once the daily limit is exceeded", async () => {
  const redis = fakeRedis({});
  // One real call first, so we learn the day key, then seed it past its max
  // without tripping the hourly limit.
  const r0 = await checkRateLimit(redis, "9.9.9.9");
  assert.strictEqual(r0.allowed, true);
  const dailyKey = Object.keys(redis.store).find((k) => k.includes(":day:"));
  redis.store[dailyKey] = DAILY_MAX;
  const r = await checkRateLimit(redis, "9.9.9.9");
  assert.strictEqual(r.allowed, false);
  assert.strictEqual(r.reason, "daily");
});

test("counts each IP separately", async () => {
  const redis = fakeRedis({});
  for (let i = 0; i < HOURLY_MAX; i++) await checkRateLimit(redis, "1.1.1.1");
  const other = await checkRateLimit(redis, "2.2.2.2");
  assert.strictEqual(other.allowed, true);
});

test("sets an expiry on first use of each window", async () => {
  const redis = fakeRedis({});
  await checkRateLimit(redis, "3.3.3.3");
  assert.strictEqual(redis.expires.length, 2);
});

test("fails open when redis throws", async () => {
  const broken = {
    async incr() { throw new Error("redis down"); },
    async expire() { throw new Error("redis down"); },
  };
  const r = await checkRateLimit(broken, "1.2.3.4");
  assert.strictEqual(r.allowed, true);
});
```

- [ ] **Step 2: Run the tests to confirm they fail**

```bash
node --test test/
```
Expected: FAIL — `Cannot find module '../lib/rate-limit'`.

- [ ] **Step 3: Implement the module**

Create `lib/rate-limit.js`:
```js
const HOURLY_MAX = 10;
const DAILY_MAX = 30;
const HOUR_SECONDS = 60 * 60;
const DAY_SECONDS = 24 * 60 * 60;

// Fixed windows keyed by clock hour/day. Simpler than a sliding window and
// entirely adequate here: the goal is stopping a flood from eating the daily
// send quota, not metering precisely.
function windowKeys(ip) {
  const now = new Date();
  const hour = `${now.getUTCFullYear()}-${now.getUTCMonth()}-${now.getUTCDate()}-${now.getUTCHours()}`;
  const day = `${now.getUTCFullYear()}-${now.getUTCMonth()}-${now.getUTCDate()}`;
  return {
    hourKey: `rl:${ip}:hour:${hour}`,
    dayKey: `rl:${ip}:day:${day}`,
  };
}

async function bump(redis, key, ttl) {
  const count = await redis.incr(key);
  if (count === 1) await redis.expire(key, ttl);
  return count;
}

async function checkRateLimit(redis, ip) {
  try {
    const { hourKey, dayKey } = windowKeys(ip);
    const hourCount = await bump(redis, hourKey, HOUR_SECONDS);
    const dayCount = await bump(redis, dayKey, DAY_SECONDS);
    if (hourCount > HOURLY_MAX) return { allowed: false, reason: "hourly" };
    if (dayCount > DAILY_MAX) return { allowed: false, reason: "daily" };
    return { allowed: true, reason: null };
  } catch {
    // Fail OPEN. If the rate-limit store is unreachable, a real customer
    // must still be able to send an enquiry — losing genuine business is a
    // worse outcome than briefly losing the limiter. Turnstile still applies.
    return { allowed: true, reason: null };
  }
}

module.exports = { checkRateLimit, HOURLY_MAX, DAILY_MAX };
```

- [ ] **Step 4: Run the tests to confirm they pass**

```bash
node --test test/
```
Expected: PASS, 18 tests total (12 from Task 2 plus 6 here).

- [ ] **Step 5: Commit**

```bash
git add lib/rate-limit.js test/rate-limit.test.js
git commit -m "feat: add per-IP rate limiting that fails open"
```

---

### Task 4: Mailer module

**Files:**
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/lib/mailer.js`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/test/mailer.test.js`

**Interfaces:**
- Consumes: `stripHeader` from `lib/validate.js` (Task 2).
- Produces: `buildMessage(clean)` returning `{ subject, text }`, and `sendEnquiry(transporter, clean)` returning a promise. Task 5 consumes both. `transporter` is any object with `sendMail(options)`, which is nodemailer's shape — so the message construction is testable without sending anything.

**Requires a Gmail app password** to send for real, but the tests here send nothing.

- [ ] **Step 1: Write the failing tests**

Create `test/mailer.test.js`:
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { buildMessage, sendEnquiry } = require("../lib/mailer");

const clean = {
  intent: "Order from the collection",
  name: "Ada Lovelace",
  email: "ada@example.com",
  bouquet: "Luxury Rose Box",
};

test("subject names the sender and the path", () => {
  const { subject } = buildMessage(clean);
  assert.ok(subject.includes("Ada Lovelace"));
  assert.ok(subject.includes("Order from the collection"));
});

test("subject cannot carry injected headers", () => {
  const { subject } = buildMessage(
    Object.assign({}, clean, { name: "Ada\r\nBcc: victim@example.com" })
  );
  assert.ok(!subject.includes("\n"));
  assert.ok(!subject.includes("\r"));
});

test("body includes every supplied field", () => {
  const { text } = buildMessage(clean);
  assert.ok(text.includes("Ada Lovelace"));
  assert.ok(text.includes("ada@example.com"));
  assert.ok(text.includes("Luxury Rose Box"));
});

test("body marks omitted optional fields rather than hiding them", () => {
  const { text } = buildMessage(clean);
  assert.ok(text.includes("—"));
});

test("sendEnquiry sets replyTo to the enquirer", async () => {
  let captured = null;
  const transporter = { async sendMail(opts) { captured = opts; return { messageId: "1" }; } };
  await sendEnquiry(transporter, clean, { from: "shop@gmail.com", to: "owner@outlook.com" });
  assert.strictEqual(captured.replyTo, "ada@example.com");
  assert.strictEqual(captured.to, "owner@outlook.com");
  assert.ok(captured.from.includes("shop@gmail.com"));
});

test("sendEnquiry propagates transport failure", async () => {
  const transporter = { async sendMail() { throw new Error("smtp refused"); } };
  await assert.rejects(
    () => sendEnquiry(transporter, clean, { from: "a@b.co", to: "c@d.co" }),
    /smtp refused/
  );
});
```

- [ ] **Step 2: Run the tests to confirm they fail**

```bash
node --test test/
```
Expected: FAIL — `Cannot find module '../lib/mailer'`.

- [ ] **Step 3: Implement the module**

Create `lib/mailer.js`:
```js
const { stripHeader } = require("./validate");

const LABELS = [
  ["intent", "Enquiry type"],
  ["bouquet", "Which piece"],
  ["budget", "Budget range"],
  ["occasion", "Occasion"],
  ["needed_by", "Needed by"],
  ["fulfilment", "Delivery or pickup"],
  ["name", "Name"],
  ["email", "Email"],
  ["message", "Message"],
];

function buildMessage(clean) {
  const subject = stripHeader(
    `New enquiry from ${clean.name || "someone"} — ${clean.intent || "unspecified"}`
  );

  // Every field is listed, with an em dash for the ones left blank, so it is
  // obvious at a glance what the customer chose to skip rather than leaving
  // the owner guessing whether a line is missing or was never asked.
  const lines = LABELS.map(([key, label]) => `${label}: ${clean[key] || "—"}`);
  lines.push("", `Received: ${new Date().toISOString()}`);

  return { subject, text: lines.join("\n") };
}

function sendEnquiry(transporter, clean, { from, to }) {
  const { subject, text } = buildMessage(clean);
  return transporter.sendMail({
    from: `"Flowers by Tavi" <${from}>`,
    to,
    replyTo: clean.email,
    subject,
    text,
  });
}

module.exports = { buildMessage, sendEnquiry };
```

- [ ] **Step 4: Run the tests to confirm they pass**

```bash
node --test test/
```
Expected: PASS, 24 tests total.

- [ ] **Step 5: Commit**

```bash
git add lib/mailer.js test/mailer.test.js
git commit -m "feat: build and send the enquiry email with header sanitisation"
```

---

### Task 5: The server

**Files:**
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/lib/turnstile.js`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/server.js`
- Create: `~/Desktop/WebM8/flowers-by-tavi-api/test/turnstile.test.js`

**Interfaces:**
- Consumes: `validateEnquiry`, `stripHeader` (Task 2); `checkRateLimit` (Task 3); `sendEnquiry` (Task 4).
- Produces: `POST /submit-form` and `GET /api/health`, and `verifyTurnstile(token, secret, ip, fetchImpl)` returning a boolean.

- [ ] **Step 1: Write the failing Turnstile tests**

Create `test/turnstile.test.js`:
```js
const { test } = require("node:test");
const assert = require("node:assert");
const { verifyTurnstile } = require("../lib/turnstile");

function fakeFetch(payload) {
  return async () => ({ json: async () => payload });
}

test("returns true when Cloudflare reports success", async () => {
  const ok = await verifyTurnstile("tok", "secret", "1.2.3.4", fakeFetch({ success: true }));
  assert.strictEqual(ok, true);
});

test("returns false when Cloudflare rejects the token", async () => {
  const ok = await verifyTurnstile("tok", "secret", "1.2.3.4", fakeFetch({ success: false }));
  assert.strictEqual(ok, false);
});

test("returns false when the token is missing", async () => {
  const ok = await verifyTurnstile("", "secret", "1.2.3.4", fakeFetch({ success: true }));
  assert.strictEqual(ok, false);
});

test("fails CLOSED when the verification call throws", async () => {
  const ok = await verifyTurnstile("tok", "secret", "1.2.3.4", async () => {
    throw new Error("network down");
  });
  assert.strictEqual(ok, false);
});
```

- [ ] **Step 2: Run to confirm failure**

```bash
node --test test/
```
Expected: FAIL — `Cannot find module '../lib/turnstile'`.

- [ ] **Step 3: Implement the Turnstile verifier**

Create `lib/turnstile.js`:
```js
const VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify";

async function verifyTurnstile(token, secret, ip, fetchImpl = fetch) {
  if (!token) return false;
  try {
    const body = new URLSearchParams({ secret, response: token });
    if (ip) body.append("remoteip", ip);
    const res = await fetchImpl(VERIFY_URL, { method: "POST", body });
    const data = await res.json();
    return data.success === true;
  } catch {
    // Fail CLOSED — the opposite of the rate limiter. If we cannot confirm a
    // human, reject. An unverifiable submission is exactly what a bot produces,
    // and the cost of a false rejection is one retry.
    return false;
  }
}

module.exports = { verifyTurnstile };
```

- [ ] **Step 4: Run to confirm the Turnstile tests pass**

```bash
node --test test/
```
Expected: PASS, 28 tests total.

- [ ] **Step 5: Write the server**

Create `server.js`:
```js
const express = require("express");
const cors = require("cors");
const nodemailer = require("nodemailer");
const { Redis } = require("@upstash/redis");
require("dotenv").config();

const { validateEnquiry } = require("./lib/validate");
const { checkRateLimit } = require("./lib/rate-limit");
const { sendEnquiry } = require("./lib/mailer");
const { verifyTurnstile } = require("./lib/turnstile");

const app = express();

const allowedOrigins = (process.env.ALLOWED_ORIGINS || "")
  .split(",")
  .map((o) => o.trim())
  .filter(Boolean);

app.use(
  cors({
    origin: allowedOrigins,
    methods: ["POST", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Accept"],
  })
);

// 16 KB cap: an enquiry is a few hundred bytes; anything larger is not a customer.
app.use(express.json({ limit: "16kb" }));

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_APP_PASSWORD,
  },
});

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

function clientIp(req) {
  const forwarded = req.headers["x-forwarded-for"];
  if (typeof forwarded === "string" && forwarded.length) {
    return forwarded.split(",")[0].trim();
  }
  return req.socket?.remoteAddress || "unknown";
}

app.get("/api/health", (req, res) => {
  res.json({ status: "ok" });
});

app.post("/submit-form", async (req, res) => {
  const { website, turnstileToken, ...fields } = req.body || {};
  const ip = clientIp(req);

  // 1. Honeypot — a hidden field no human ever fills in. Cheapest possible
  //    rejection, and deliberately vague so a bot learns nothing from it.
  if (website) {
    return res.status(400).json({ success: false, error: "Rejected" });
  }

  // 2. Turnstile — the real bot defence. Costs an outbound call, so it runs
  //    after the free check above.
  const human = await verifyTurnstile(turnstileToken, process.env.TURNSTILE_SECRET, ip);
  if (!human) {
    return res
      .status(403)
      .json({ success: false, error: "We couldn't verify that you're human. Please try again." });
  }

  // 3. Rate limit — costs a Redis round trip, so it runs after Turnstile.
  const limit = await checkRateLimit(redis, ip);
  if (!limit.allowed) {
    return res.status(429).json({
      success: false,
      error: "You've sent several enquiries recently. Please try again later, or email us directly.",
    });
  }

  // 4. Validate. Never trust the browser's own checks — they are trivially skipped.
  const { valid, errors, clean } = validateEnquiry(fields);
  if (!valid) {
    return res.status(400).json({ success: false, error: "Please check your details.", fields: errors });
  }

  try {
    await sendEnquiry(transporter, clean, {
      from: process.env.GMAIL_USER,
      to: process.env.MAIL_TO,
    });
    return res.json({ success: true });
  } catch (error) {
    console.error("Send failed:", error.message);
    return res.status(500).json({ success: false, error: "Something went wrong sending your enquiry." });
  }
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ success: false, error: "Something went wrong." });
});

if (require.main === module) {
  const PORT = process.env.PORT || 3001;
  app.listen(PORT, () => console.log(`Enquiry API listening on ${PORT}`));
}

module.exports = app;
```

- [ ] **Step 6: Verify the server starts and health responds**

Create a `.env` from `.env.example` with real values if available; if credentials are not yet available, put obvious dummies in — this step only checks the process boots and routes respond, and no email is sent.

```bash
node --check server.js
npm start &
sleep 2
curl -s http://localhost:3001/api/health
```
Expected: `{"status":"ok"}`.

```bash
curl -s -X POST http://localhost:3001/submit-form \
  -H "Content-Type: application/json" \
  -d '{"website":"bot","intent":"Design something custom","name":"x","email":"a@b.co","message":"hi"}'
```
Expected: `{"success":false,"error":"Rejected"}` with status 400 — the honeypot rejects before Turnstile is ever called, which is why this works without a real Turnstile secret.

Stop the server afterwards.

- [ ] **Step 7: Commit**

```bash
git add lib/turnstile.js test/turnstile.test.js server.js
git commit -m "feat: add the enquiry endpoint with layered request screening"
```

---

### Task 6: Add the Turnstile widget and honeypot to the site

**Files:**
- Modify: `~/Desktop/WebM8/Bouquets/index.html`
- Modify: `~/Desktop/WebM8/Bouquets/css/style.css`

**Interfaces:**
- Produces: a hidden `website` input and a `.cf-turnstile` container inside `#enquiry-form`. Task 8 reads the Turnstile token from the widget.

**Requires the Turnstile SITE key** (the public one — safe to commit; the secret key is not).

Work on a branch in the site repo, not `main`.

- [ ] **Step 1: Create a branch**

```bash
cd ~/Desktop/WebM8/Bouquets
git checkout -b enquiry-backend
```

- [ ] **Step 2: Load the Turnstile script**

In `index.html`, find:
```html
  <link rel="stylesheet" href="css/style.css">
</head>
```
Replace with:
```html
  <link rel="stylesheet" href="css/style.css">
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</head>
```

**Deliberately no `integrity="sha384-…"` on this tag, and this is not an oversight.**
Subresource Integrity is the right default for third-party scripts, but it assumes a
URL whose contents never change. `turnstile/v0/api.js` is a stable, unversioned URL
that Cloudflare updates in place. Pinning a hash to it means the browser refuses the
script the moment Cloudflare ships an update — and with no widget there is no token,
so every submission is rejected at the API with a verification failure. That breakage
would be silent, total, and would look like the form "just stopped working".

The exposure being accepted is a Cloudflare CDN compromise, against a script we are
already trusting to decide who is human. If Cloudflare ever publishes an SRI hash for
this endpoint, add it. Do not generate one from the current file contents.

- [ ] **Step 3: Add the honeypot and widget**

In `index.html`, find:
```html
          <button type="submit" class="btn">Submit</button>
          <p class="form-status" role="status" aria-live="polite" hidden></p>
```
Replace with:
```html
          <div class="honeypot-field" aria-hidden="true">
            <label for="website">Website</label>
            <input type="text" id="website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <div class="cf-turnstile" data-sitekey="REPLACE_WITH_TURNSTILE_SITE_KEY" data-theme="light"></div>
          <button type="submit" class="btn">Submit</button>
          <p class="form-status" role="status" aria-live="polite" hidden></p>
```

Replace `REPLACE_WITH_TURNSTILE_SITE_KEY` with the real site key from the Cloudflare dashboard. If it is not available, report BLOCKED — do not commit the placeholder.

⚠️ **Known risk at this insertion point — verify before moving on.** This markup sits
inside `#enquiry-details`, which `applyIntent()` hides with the `hidden` attribute on
page load, until the visitor picks an intent card. Turnstile auto-renders on script
load, and widgets that auto-render inside a `display:none` container can come back
zero-sized or fail to render at all. If that happens there is no token, and every
submission is rejected with a verification failure — a total, silent outage of the form.

So after Step 5's checks, explicitly confirm the widget is real: pick an intent card,
then evaluate in the page

```js
document.querySelector('[name="cf-turnstile-response"]')?.value.length > 0
```

Expected: `true` within a few seconds of the widget appearing.

If it is `false` or the element is missing, do NOT work around it by un-hiding the
container. Instead switch to explicit rendering: add `data-render="explicit"` to the
script URL query string, give the container an id, and call `turnstile.render()` from
`applyIntent()` the first time a path is chosen (guarding so it renders only once).
Report which route you took.

- [ ] **Step 4: Style the honeypot and widget**

In `css/style.css`, find the `.field-group > .field-label` rule and insert immediately after it:
```css
/* Hidden from people, visible to naive bots. Not display:none — some bots skip
   those. Kept out of the tab order and the accessibility tree instead. */
.honeypot-field {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.cf-turnstile { margin: 0 0 1.2rem; }
```

- [ ] **Step 5: Verify**

Serve on port 8123 and open with a cache-busted URL. Confirm:
- The Turnstile widget renders inside the form, above Submit, once a path is chosen.
- The honeypot input is invisible, and `document.getElementById("website").tabIndex` is `-1`.
- Tabbing from Email reaches the textarea and then Submit, never the honeypot.
- Zero console errors.

- [ ] **Step 6: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add Turnstile widget and honeypot to the enquiry form"
```

---

### Task 7: Point the frontend at the API

**Files:**
- Modify: `~/Desktop/WebM8/Bouquets/js/main.js`

**Interfaces:**
- Consumes: the honeypot and Turnstile widget from Task 6, and the `POST /submit-form` contract from Task 5.

- [ ] **Step 1: Replace the configuration block**

In `js/main.js`, find:
```js
// ── Configuration ────────────────────────────────────────────────
// Create a free form at https://formspree.io and paste its ID here.
const FORMSPREE_ID = "YOUR_FORM_ID";
const FALLBACK_EMAIL = "flowersbytavi@outlook.com";
```
Replace with:
```js
// ── Configuration ────────────────────────────────────────────────
const FALLBACK_EMAIL = "flowersbytavi@outlook.com";
const API_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:3001/submit-form"
    : "https://REPLACE_WITH_VERCEL_HOST/submit-form";
```

Replace `REPLACE_WITH_VERCEL_HOST` with the deployed Vercel hostname. If the API is not yet deployed, report BLOCKED — do not commit the placeholder.

- [ ] **Step 2: Replace the submit handler**

In `js/main.js`, find the whole block from `form.addEventListener("submit", async (event) => {` through its closing `});`, and replace with:
```js
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
```

Note the `turnstile.reset()` in `finally`: a Turnstile token is single-use, so without resetting, a visitor whose first attempt failed would be rejected on every retry with no way to recover.

- [ ] **Step 3: Confirm no Formspree references remain**

```bash
grep -n "FORMSPREE\|formspree" js/main.js index.html README.md
```
Expected: only `README.md` hits, which Task 9 rewrites.

- [ ] **Step 4: Verify against the local API**

Start the API (`npm start` in the API repo) and serve the site on 8123. With a cache-busted URL:
- Submit a valid collection enquiry. Because Turnstile's real widget requires the production domain, use Cloudflare's **test site key** `1x00000000000000000000AA` (always passes) and test secret `1x0000000000000000000000000000000AA` in the API `.env` for this check.
- Confirm the success panel appears and the API logs a send attempt.
- Submit with the honeypot filled via devtools (`document.getElementById("website").value = "bot"`). Confirm a rejection, and that the generic error shows.
- Confirm zero console errors throughout.

- [ ] **Step 5: Commit**

```bash
git add js/main.js
git commit -m "feat: submit enquiries to the self-hosted API"
```

---

### Task 8: Deploy the API to Vercel

**Files:**
- None modified — this is deployment and configuration.

**Requires:** a Vercel account, the Gmail app password, Turnstile secret key, and Upstash credentials.

- [ ] **Step 1: Push the API repo to a PRIVATE GitHub repo**

Create it as **private** — the repo contains the anti-spam logic. Confirm with:
```bash
gh repo view --json visibility
```
Expected: `{"visibility":"PRIVATE"}`. If it reports PUBLIC, stop and fix before continuing.

- [ ] **Step 2: Create the Vercel project and set environment variables**

Import the repo in Vercel, then add all seven variables from `.env.example` with real values, for the Production environment.

Set `ALLOWED_ORIGINS` to exactly:
```
https://flowersbytavi.co.uk,https://www.flowersbytavi.co.uk
```

- [ ] **Step 3: Deploy and verify health**

```bash
curl -s https://<your-vercel-host>/api/health
```
Expected: `{"status":"ok"}`.

- [ ] **Step 4: Verify the honeypot rejects in production**

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://<your-vercel-host>/submit-form \
  -H "Content-Type: application/json" \
  -d '{"website":"bot","name":"x","email":"a@b.co","intent":"Design something custom","message":"hi"}'
```
Expected: `400`.

- [ ] **Step 5: Verify a tokenless submission is rejected**

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://<your-vercel-host>/submit-form \
  -H "Content-Type: application/json" \
  -d '{"name":"x","email":"a@b.co","intent":"Design something custom","message":"hi"}'
```
Expected: `403` — proof that a direct `curl` bypassing the browser cannot submit, which is the gap CORS alone leaves open.

- [ ] **Step 6: Record the deployed hostname**

Report it — Task 7 Step 1 needs it, and if Task 7 was completed with a placeholder it must now be corrected and re-committed.

---

### Task 9: End-to-end verification and documentation

**Files:**
- Modify: `~/Desktop/WebM8/Bouquets/README.md`
- Modify: `~/Desktop/WebM8/Bouquets/AGENTS.md`

- [ ] **Step 1: Send a real enquiry end to end**

With the site served locally but `API_URL` pointed at the deployed Vercel host, submit one real enquiry on each path.

Confirm for each:
- The success panel appears.
- An email arrives at `flowersbytavi@outlook.com`.
- The subject names the sender and the path.
- Every field appears in the body, with `—` for the ones left blank.
- Hitting Reply addresses the customer, not the Gmail account.

- [ ] **Step 2: Verify the rate limiter**

Submit 11 enquiries in quick succession from the same machine. Expected: the 11th returns 429 and the friendly "try again later" message. Then confirm a fresh enquiry still succeeds the following hour, or by clearing the key in the Upstash console.

- [ ] **Step 3: Replace the README's Formspree section**

In `README.md`, find the section beginning:
```markdown
## Connect the enquiry form (one-time setup)
```
through the line ending:
```markdown
Until this is done, the form shows visitors a friendly "form not connected yet" message with the fallback email instead of sending.
```
Replace the whole section with:
```markdown
## How the enquiry form delivers

Enquiries are handled by our own API, not a third-party form service. The
server lives in the private `flowers-by-tavi-api` repo and runs on Vercel;
this site posts JSON to it. It screens each submission with a honeypot,
Cloudflare Turnstile, per-IP rate limiting and server-side validation, then
emails the enquiry to flowersbytavi@outlook.com with Reply-To set to the
customer.

To change where enquiries are delivered, update `MAIL_TO` in the API
project's Vercel environment variables — no code change needed here.

If the API host ever changes, update `API_URL` at the top of `js/main.js`.
```

- [ ] **Step 4: Add an AGENTS.md rule for the new coupling**

In `AGENTS.md`, find:
```markdown
- **Don't touch `FORMSPREE_ID` in `js/main.js`** unless explicitly given a real Formspree form ID to set — it's live production config, not a placeholder to guess at.
```
Replace with:
```markdown
- **Don't touch `API_URL` in `js/main.js`** unless explicitly given a real API host — it's live production config, not a placeholder to guess at. The enquiry backend lives in the separate private `flowers-by-tavi-api` repo; its secrets are Vercel environment variables and must never appear in this repo.
- **The Turnstile `data-sitekey` in `index.html` is public and safe to commit.** The matching SECRET key belongs only in the API's Vercel environment — if you ever see a Turnstile secret in this repo, that is a leak.
```

- [ ] **Step 5: Verify no secrets reached the site repo**

```bash
cd ~/Desktop/WebM8/Bouquets
grep -rni "app_password\|gmail_app\|turnstile_secret\|upstash" --include=*.html --include=*.js --include=*.css --include=*.md .
```
Expected: only the `AGENTS.md` line added above, which merely names them as things that must not appear.

```bash
git status --short
```
Confirm no `.env` is staged or untracked-and-unignored.

- [ ] **Step 6: Commit**

```bash
git add README.md AGENTS.md
git commit -m "docs: describe the self-hosted enquiry backend"
```

- [ ] **Step 7: Stop before merging**

Do NOT merge to `main` or push. Report the branch state and let the human decide — merging deploys to the live public site immediately, and this change alters how every enquiry is delivered.
