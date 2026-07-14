# SK Playbooks — capabilities SK can run

This is SK's skill library. Each playbook is a task SK can carry out by voice,
distilled from Karthik's Cowork skills. When Karthik's request matches a
**Trigger**, SK follows that playbook's steps and lands the output where noted
(the Intel Feed, `venture_notes`, `content_calendar`, `todo`, etc.).

SK loads playbooks on demand: read the trigger list, pick the one that matches,
follow it. Don't dump every playbook into a reply — run the one that fits.

---

## OneSafe  _(on hold until end of month — run only if Karthik explicitly asks)_

### Generate a Toolbox Talk
**Trigger (say):** "SK, make me a toolbox talk on working at height in English and Tamil."
**SK does:** Pulls the relevant hazards from the MSRA library and drafts a ready-to-brief toolbox talk in the requested languages, saved for reuse.
**Steps:**
1. Match the spoken activity to rows in `msra_documents(activity)` and pull the linked `msra_hazards(hazard,injury)`.
2. Draft the talk: opening, top 5 hazards + control measures, injury consequences, and a 3-question sign-off check.
3. Produce English, then translate to the requested language(s) of the 6 supported (Tamil, Mandarin, Bengali, Malay, Burmese, English).
4. Save to `venture_notes(venture='OneSafe', title='TBT – <activity> – <langs>')`.
5. On request, "open Drive" to drop a formatted copy for site printing.
**Output:** Summary on the Intel Feed; full bilingual talk saved to `venture_notes`; optional copy to Drive.
**Draws on skills:** process-doc, risk-assessment, copywriting

### Draft or Expand an MSRA
**Trigger (say):** "SK, build an MSRA for confined space entry from the hazard library."
**SK does:** Assembles a Method Statement Risk Assessment for the named activity from the live hazard library, ready for WSH review.
**Steps:**
1. Look up the activity in `msra_documents(activity)`; if new, flag it as a library addition.
2. Pull all `msra_hazards(hazard,injury)` rows tied to that activity as the risk base.
3. Draft method-statement steps, then a risk table (hazard, who's harmed, existing controls, risk rating, additional controls, residual rating), aligned to SG WSH norms.
4. Add `todo(text='Review MSRA – <activity>', done=false)` for Karthik's sign-off.
5. Save the draft to `venture_notes(venture='OneSafe', title='MSRA draft – <activity>')`.
**Output:** MSRA draft in `venture_notes`, review row in `todo`, risk-rating summary on the Intel Feed.
**Draws on skills:** risk-assessment, compliance-tracking, process-doc

### Subscriber Sales Outreach + Follow-Up
**Trigger (say):** "SK, start an outreach sequence to SG construction firms for OneSafe."
**SK does:** Drafts a cold email plus a 2-step follow-up to WSH officers and safety coordinators, and schedules the touches so Karthik just hits send.
**Steps:**
1. Draft a lead-magnet-led cold email (free sample MSRA or a 6-language toolbox talk), positioned on subscription value.
2. Write follow-up 1 (day 3, proof/objection) and follow-up 2 (day 7, deadline/close).
3. Save all three to `venture_notes(venture='OneSafe', title='Outreach seq – <segment>')`.
4. Log each touch to `content_calendar(venture='OneSafe', platform='Email', hook=<subject>, caption=<email>, status='planned', post_date=<send date>)`.
5. "Open Calendar" to block a send-and-reply slot; add `todo(text='Send OneSafe outreach batch')`.
**Output:** 3 email drafts in `venture_notes`, 3 planned `content_calendar` rows, a Calendar block, a `todo`, subject lines on the Intel Feed.
**Draws on skills:** cold-email, product-marketing, copywriting, pricing

---

## One Journey

### Survey Insight Brief
**Trigger (say):** "SK, turn the One Journey survey into an insight brief."
**SK does:** Pulls the 15 survey responses and produces a synthesized insight brief plus a prioritized feature list, so Karthik knows what to build first.
**Steps:**
1. "Open One Journey survey" to load the responses (or the linked Drive sheet); read all 15.
2. Cluster into themes: top pain points, most-wanted features, stage coverage (expecting / newborn / toddler), pricing signals.
3. Rank features by frequency × pain into a Must / Should / Later list.
4. Write the brief to `venture_notes(venture='One Journey', title='Survey Insight Brief')`; log 3–5 open questions.
5. Drop the top 3 next actions into `todo`.
**Output:** Insight brief + prioritized features in `venture_notes`, actions in `todo`, read back by voice.
**Draws on skills:** synthesize-research, customer-research, product-management

### PWA MVP Build Spec
**Trigger (say):** "SK, scope the One Journey MVP build spec."
**SK does:** Turns the prioritized features into a tight, buildable PWA spec scoped for a near-zero-budget solo build on Supabase.
**Steps:**
1. Read the Survey Insight Brief and feature list from `venture_notes`.
2. Define the MVP cut: core screens (checklists, reminders, stage guidance), Must-haves only, and an explicit "not in v1" list.
3. Draft the Supabase data model (stages, checklist_items, reminders, user_progress); note auth + PWA install/offline needs.
4. Write the spec to `venture_notes(title='MVP Build Spec v1')`; create/update the `projects` row (One Journey, status='building').
5. Break the build into phased `todo` items (schema, checklist UI, reminders, stage content, deploy).
**Output:** Build-ready spec in `venture_notes`, updated `projects` entry, phased `todo`, voice summary.
**Draws on skills:** write-spec, roadmap-update, product-management, small-business

### Launch-Week Social Content
**Trigger (say):** "SK, draft a week of One Journey social posts for SG parents."
**SK does:** Generates 7 days of on-brand posts (hooks + captions) for Singapore new/expecting parents and schedules them.
**Steps:**
1. Pull audience pain points and language from the Survey Insight Brief in `venture_notes`.
2. Draft 7 posts across a mix (relatable pain, quick tip, checklist teaser, behind-the-build, waitlist CTA) with SG angles (baby bonus, hospital bag, confinement).
3. Write each as a scroll-stopping hook + caption with a soft waitlist/lead-magnet CTA.
4. Insert 7 rows into `content_calendar(venture='One Journey', ..., status='draft')` across the next week.
5. Add a `todo` to review and approve before they go live.
**Output:** 7 draft posts in `content_calendar`, approval task in `todo`, read back by voice.
**Draws on skills:** content-strategy, social, launch, lead-magnets

---

## SKAI

### Winning Product Research
**Trigger (say):** "SK, find me a winning product for SKAI."
**SK does:** Researches trending SEA-market products against dropshipping criteria and returns a shortlist with a go/no-go call on each.
**Steps:**
1. Open Shopee, Lazada, AliExpress, TikTok, Amazon; note price bands, review counts, sell-through signals.
2. Score each candidate: problem-solving/wow factor, not in local malls, light/cheap to ship to SG/SEA, 3×+ target margin, low return risk.
3. Price-check top candidates for supplier-vs-market spread; margin-analyzer for landed cost, ad cost, net margin per unit.
4. Scan competitors already running it (ad libraries, listings) for saturation and angle gaps.
5. Write the top 3 to `venture_notes(venture='SKAI', title='Product Research <date>')`; one-line summary to `daily_brief`.
**Output:** Ranked 3-product shortlist with margin math and a go/test/skip verdict in `venture_notes`, surfaced in the daily brief.
**Draws on skills:** price-check, margin-analyzer, competitors

### Ad Angle & Hook Generator
**Trigger (say):** "SK, give me ad angles for the <product>."
**SK does:** Generates distinct ad-creative angles with scroll-stopping hooks and captions, ready to shoot or brief into Page Pilot.
**Steps:**
1. Read the product's row in `venture_notes(venture='SKAI')` for offer, price, audience.
2. Produce 5 angles (pain-relief, before/after, curiosity, social-proof, price-anchor), each with 3 hook variations for the first 3 seconds of TikTok/Reels.
3. Write matching primary-copy captions and a CTA per angle.
4. Open Page Pilot (pagepilot.ai) to spin the winning angle into a landing page / ad set.
5. Schedule top angles into `content_calendar(venture='SKAI', platform='TikTok', ..., status='draft')`.
**Output:** 5 angles × 3 hooks + captions/CTAs, dropped as draft `content_calendar` rows, ready for Page Pilot.
**Draws on skills:** ad-creative, copywriting, product-marketing, offers

### Store & Landing-Page Launch Checklist
**Trigger (say):** "SK, run the launch checklist for <product>."
**SK does:** Grades the store/offer/landing page against a CRO checklist and flags what to fix before spending on ads.
**Steps:**
1. Pull the product and angle from `venture_notes(venture='SKAI')`; confirm the offer (bundle, price, guarantee, urgency).
2. Open Page Pilot and audit the page: above-fold hook, hero image, benefit bullets, social proof, sticky CTA, trust badges, mobile speed, one clear action.
3. Verify offer math with margin-analyzer so the discount/free-shipping still clears target net margin at expected ad cost.
4. Check 2–3 competitor pages for missing trust/objection-handling to close.
5. Log the pass/fail checklist to `venture_notes(title='Launch Checklist <product>')`; a `todo` per open fix; set the go-live `content_calendar` row to 'ready' once all pass.
**Output:** Graded checklist with prioritized fixes in `venture_notes`, one `todo` per fix, go-live flag in `content_calendar`.
**Draws on skills:** cro, offers, margin-analyzer, competitors

---

## Studio + content engine

### Weekly Cross-Venture Content Calendar
**Trigger (say):** "SK, plan this week's content across all my ventures."
**SK does:** Drafts a full week of platform-ready posts for OneSafe, One Journey, and SKAI and writes them into `content_calendar` as a ready-to-review schedule.
**Steps:**
1. Pull recent context from `venture_notes` (per venture) and check `content_calendar` for what already ran, so hooks don't repeat.
2. Plan a balanced week: assign each post a `venture`, `platform`, `post_date`, `post_time` (best-time slots).
3. Write a copywriting-grade `hook` + `caption` per slot, tuned to each venture's audience.
4. Insert every post into `content_calendar` with `status='draft'`.
5. Read the week back by voice; flip approved rows to `status='scheduled'`.
**Output:** 7–10 draft rows across all three ventures; one-line summary to `daily_brief`.
**Draws on skills:** content-strategy, social, copywriting

### One Idea to Multi-Platform Pack
**Trigger (say):** "SK, turn this idea into a content pack for <venture>."
**SK does:** Takes one idea, clip, or asset and spins it into a full multi-platform set, then files it into the calendar.
**Steps:**
1. Capture the raw idea/asset into `venture_notes(venture, title, content)` as the source.
2. Fan it into platform variants: a video hook + shot list, a carousel outline, short text posts.
3. Draft ad-creative-strength hooks and captions for each, in the venture's voice.
4. For visuals, prep a Canva/Figma brief (dimensions, headline, layout) so Karthik can "open Canva" and drop it in.
5. Write each variant into `content_calendar` (one row per platform, `status='draft'`); log the asset link in `projects.url` if tied to a build.
**Output:** 4–6 platform-specific posts from one idea as `content_calendar` drafts + a Canva/Figma brief, traceable to the source note.
**Draws on skills:** repurposing, video, ad-creative, copywriting, canva/figma

### Studio Client Delivery + Invoice
**Trigger (say):** "SK, ship the Studio delivery and invoice <client>."
**SK does:** Packages the finished deliverable, logs the Studio job as done, and chases payment.
**Steps:**
1. Confirm the deliverable is ready (open Drive/Canva for the final export link); update the Studio `projects` row (status='delivered', url=asset link, summary).
2. Draft the client handoff message: what's delivered, where to view, next steps.
3. Build invoice line items (scope, rate, total, due date); open Gmail to send.
4. Add `todo(text='Follow up on <client> invoice')`; set a Calendar reminder for the due date.
5. On the reminder, draft a polite payment nudge; flip the `todo` to done once paid and note it in `daily_brief`.
**Output:** Updated Studio `projects` row, handoff + invoice ready in Gmail, tracked `todo` + Calendar reminder, automated follow-up.
**Draws on skills:** invoice-chase, copywriting, video
