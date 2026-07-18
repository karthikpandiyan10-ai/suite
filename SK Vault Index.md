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

**Current focus (July):** **One Journey** launch is the priority. The four
ventures are **One Journey, OneSafe, OneFlat, Barber Den** (SKAI kept but not
featured). **OneSafe is parked** until end of month / after One Journey
launches — don't push MSRA work unless asked. **OneFlat** is new and still in
scoping — don't build it yet, help define the offer when asked.

**One Journey — v1 focus (zero to 100), from `One Journey — Action Plan.md`:**
1) define & draft the founding offer; 2) tighten the `first100.html` waitlist
page for signups; 3) set the target (first 100 this month) + main channel; then
build the MVP core, write the S$6 well-being ebook, a week of SG-parent content,
pick a launch date. **The survey is done — parked for v2; don't re-analyze it
now.** The one metric this month: **first 100 One Journey signups.** When Karthik
asks what to do for One Journey, pull from this.

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

### 🚀 The four ventures (current priority order)
- **One Journey** — new-parents guide app for Singapore, built with his wife
  (formerly "Little Sprout"): checklists, reminders, stage-by-stage guidance,
  plus a S$6 well-being ebook. Survey of 15 responses reached. **FLAGSHIP —
  launches Sat 1 Aug, on autopilot via the 8:30am brief** (site already live
  with real Stripe payments). Waitlist + app: `first100.html` (now captures
  signups → Supabase `signups`). Supabase venture key is `sprout` — match it.
- **OneSafe** — safety-document platform for SG construction. MSRA library
  (129 activities, 3,639 hazard rows), toolbox talks in 6 languages, PE-design
  guides; subscriptions. App: `onesafe.html`. Venture key `safeframe`/`onesafe`.
  **ON HOLD until end of month — don't open MSRA work unless asked.**
- **OneFlat** — **new** property idea (Karthik's words: "three words so far").
  **Un-scoped** — nothing built, no offer defined, just the working name.
  Needs one scoping session with SK first. Don't state specifics as decided.
  Venture key `oneflat`. Part of the "One" brand family.
- **Barber Den** — paid video editing & marketing for a friend (renamed from
  "Studio"). Fastest cash, per job. Venture key still `studio` (display renamed).

Also in SK, not featured:
- **SKAI** — faceless TikTok dropshipping; Page Pilot ready. Learning phase —
  raise only when Karthik asks. Venture key `skai`.
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
- **One Journey** — "turn the survey into an insight brief" (synthesize the 15
  responses + feature list → `venture_notes`); "scope the MVP build spec" (PWA
  spec + data model → `venture_notes` + `projects`); "draft a week of One
  Journey posts" (7 SG-parent posts → `content_calendar`).
- **SKAI** — "find me a winning product" (SEA research + margins →
  `venture_notes`); "give me ad angles for <product>" (5 angles × 3 hooks →
  `content_calendar` + Page Pilot); "run the launch checklist for <product>"
  (CRO-graded checklist → `venture_notes` + `todo`).
- **Studio + content** — "plan this week's content across my ventures" (full
  week → `content_calendar`); "turn this idea into a content pack for <venture>"
  (multi-platform set → `content_calendar` + Canva brief); "ship the Studio
  delivery and invoice <client>" (handoff + invoice + follow-up).

## Part 5 — Work (day job: HSE / WSH safety) — full map in `SK Work Knowledge.md`

Karthik is a **Workplace Safety & Health Coordinator** in Singapore
construction (employers: CES / CES_SDC / GRC Group; main project: **CCKWW —
Choa Chu Kang Waterworks reconstruction**). His work files live in
`Jarvis/Work` (~1,346 files). SK knows the shape of it and can find/build from
it:

- **Training decks** (~130) — confined space, firewatchman, manual handling,
  lifting, crane/excavator/MEWP/forklift, work-at-height, heat stress, LOTO/RWA,
  electrical, first aid. In `Work/Karthik/`.
- **Incident & near-miss reports**, **toolbox/TBM programs**, **monthly HSSE
  scoring audits** (No.17–20), **MSRA / method statements / SWPs** (`Work/Sankar
  MSRA/`, `Work/DX/`), **duty rosters**, **inspection checklists**, **machinery
  & lifting-gear** compliance, **worker permits/certs**, **619 WSH posters**.
- **Career/degree** — WSHO professional review, HSE degree, resume.

When Karthik asks about his safety work, use this map: find the right file, draft
toolbox talks/MSRAs/reports from existing ones, check cert/calibration expiries,
pull the latest audit. Full index + paths in `SK Work Knowledge.md`.

**🔒 Private — never touch:** Karthik's sensitive personal-legal/financial files
(divorce filings, salary/CPF/credit) have been moved OUT of Work into
`Jarvis/_PRIVATE - keep off AI - move me off Jarvis/`. Never read, surface, index,
or include them in any answer or output.

## Part 3 — How to grow this

Every time Karthik teaches SK a new capability — how to draft a OneSafe MSRA,
how to write a Little Sprout post, how to research a SKAI product — write it as
a note in `venture_notes` (or a new vault note) and add **one line here** so SK
knows it exists. The map grows; SK gets smarter; nothing bloats.
