# SK Vault Index — the map of Karthik's command center

> The map. Two jobs: tell SK about Karthik, and point SK to everything in the
> command center. Summaries and locations only — never full content. SK Command
> Deck loads this file as its "world" on startup; a file-reading agent reads it
> right after CLAUDE.md. Keep it lean — when you add something to SK, add one
> line here.

---

## Part 1 — About Karthik

Karthik Pandiyan — **Singapore**. Day job: lead safety coordinator at CES_SDC.
Building four income ventures in parallel with near-zero budget, aiming to go
full-time in **1–2 months**. Runs everything through SK by voice. Fast-moving,
technical, hands-on. Prefers short answers, clear next actions, and drafts he
can approve rather than open-ended questions.

*(Karthik — add anything else you want SK to know: working hours, how you like
to be spoken to, goals for the year.)*

---

## Part 2 — The map of the command center

### 🧠 The Deck itself
- **`jarvis.html`** — SK Command Deck. Voice interface, wake word, brain
  module (Gemini default / Claude optional), command pipeline. Loads this file
  and `CLAUDE.md` as its brain on startup.
- **`host_upload/dashboard.html`** — Mission Control: cross-venture status.
- **`host_upload/first100.html`** — first-100-customers / launch tracker.
- **`host_upload/manifest.json` + `sk-*.png`** — the installable PWA shell.

### 📦 Data sources (Supabase — load on demand)
- **`venture_notes`** (venture, title, content) — working knowledge base per
  venture. *SK's real memory store — pull from here first.*
- **`content_calendar`** — planned posts (date, time, platform, venture, hook,
  caption, status). Drives "what do I post today."
- **`projects`** — name, status, url, summary. Portfolio at a glance.
- **`todo`** / **`daily_brief`** — tasks SK captures by voice; the morning brief.
- **`msra_documents` / `msra_hazards`** — OneSafe's risk-assessment library
  (129 activities, 3,639 anonymized hazard rows).

### 🚀 Ventures
- **OneSafe / SafeFrame** — safety-document platform for Singapore
  construction. Live MSRA library, toolbox talks in 6 languages, PE-design
  guides. Upcoming: inspections, registers, permit-to-work, company logins.
  Revenue: subscriptions. App: `onesafe.html`.
- **Little Sprout** — new-parents guide app for Singapore, built with his wife:
  checklists, reminders, stage-by-stage guidance. Survey goal of 15 responses
  reached; next: analyze responses and build the app as a PWA. App:
  `little-sprout.html`.
- **SKAI** — dropshipping, learning phase; Page Pilot ready.
- **Studio** — paid video editing & marketing for a friend.
- **Coursiv** — AI course Karthik is working through.

### 🔌 Connected services
- **Google Workspace** — Gmail (unread triage), Calendar (today's agenda),
  Drive (search by voice).
- **LLM brain** — Gemini (default) or Claude (paid, for heavier writing).

---

## Part 4 — SK's playbooks (say the trigger, SK runs it)

When a request matches a trigger below, follow that playbook (full steps in
`SK Playbooks.md`). Load only the one that fits, then land the output where noted.

- **OneSafe** — "make a toolbox talk on <activity> in <languages>" (bilingual
  talk from the hazard library → `venture_notes`); "build an MSRA for
  <activity>" (risk assessment → `venture_notes` + review `todo`); "start an
  outreach sequence to SG construction firms" (cold email + 2 follow-ups →
  `content_calendar`).
- **Little Sprout** — "turn the survey into an insight brief" (synthesize the 15
  responses + feature list → `venture_notes`); "scope the MVP build spec" (PWA
  spec + data model → `venture_notes` + `projects`); "draft a week of Little
  Sprout posts" (7 SG-parent posts → `content_calendar`).
- **SKAI** — "find me a winning product" (SEA research + margins →
  `venture_notes`); "give me ad angles for <product>" (5 angles × 3 hooks →
  `content_calendar` + Page Pilot); "run the launch checklist for <product>"
  (CRO-graded checklist → `venture_notes` + `todo`).
- **Studio + content** — "plan this week's content across my ventures" (full
  week → `content_calendar`); "turn this idea into a content pack for <venture>"
  (multi-platform set → `content_calendar` + Canva brief); "ship the Studio
  delivery and invoice <client>" (handoff + invoice + follow-up).

## Part 3 — How to grow this

Every time Karthik teaches SK a new capability — how to draft a OneSafe MSRA,
how to write a Little Sprout post, how to research a SKAI product — write it as
a note in `venture_notes` (or a new vault note) and add **one line here** so SK
knows it exists. The map grows; SK gets smarter; nothing bloats.
