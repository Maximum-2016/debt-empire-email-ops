#!/usr/bin/env python3
"""Generate per-brand 10-month nurture journeys + brand cycle config.

Cadence (Anthony 2026-09-27):
  Kickoff weeks 1–2: every other day → D0,D2,D4,D6,D8,D10,D12 (7 emails)
  Months 2–10: 2 emails/month (calmer)
  Total: 25 emails/brand

Cycle: contact rotates brands until conversion; on convert stop all other
brand sequences; winning brand → client-edu (or post-convert).

No MDA. No FM. No live sends in this script.
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
CONTENT = PACK / "content" / "nurture-by-brand"
DELIVERY = PACK / "delivery"
REGISTRY = json.loads((DELIVERY / "brand-registry.json").read_text())

# Explicit brand order — exclude mda (dead). Registry order with sensible cycle.
CYCLE_ORDER = [
    "mrd", "abr", "bdn", "ccc", "slc", "aab", "spa", "bds",
    "mcb", "lrl", "dag", "fintrilo", "lsp", "icd",
]

BRANDS = {b["id"]: b for b in REGISTRY["brands"] if b["id"] != "mda"}
assert all(bid in BRANDS for bid in CYCLE_ORDER), "cycle brand missing from registry"
assert "mda" not in CYCLE_ORDER

# Month themes (shared arc; brand voice colors the copy)
MONTH_THEMES = {
    1: ("Orient — name the pressure", "kickoff"),
    2: ("MCA mechanics without hype", "mechanics"),
    3: ("Cash-flow triage", "triage"),
    4: ("Creditor behavior & communication", "escalation"),
    5: ("Settlement / options literacy", "literacy"),
    6: ("Scenarios & composites", "scenarios"),
    7: ("Risk, guaranty & legal awareness", "risk"),
    8: ("Readiness & fit", "readiness"),
    9: ("Trust, alternatives, second look", "trust"),
    10: ("Commit invitation & wrap", "commit"),
}

# Kickoff slot angles (7) + monthly pair angles
KICKOFF_SLOTS = [
    (0, "welcome", "Welcome — let's get oriented"),
    (2, "pain", "Name the daily pressure"),
    (4, "stack", "What stacking feels like in the bank"),
    (6, "cost", "True cost without fake stats"),
    (8, "options", "Options map (teaser)"),
    (10, "mistakes", "Moves that make pressure worse"),
    (12, "soft_cta", "A calm next step when you're ready"),
]

# Months 2–10: (month, day_offset_from_enroll, slug, subject_seed)
# Base month start ≈ (month-1)*30; two touches ~day +5 and +18 within month
def month_offsets():
    out = []
    for m in range(2, 11):
        base = (m - 1) * 30
        out.append((m, base + 5, "a", None))
        out.append((m, base + 18, "b", None))
    return out

SIGN_OFF = {
    "dag": "DAG Law Client Education",
    "bds": "Business Debt Solutions",
    "bdn": "The Ninjas",
    "lsp": "Level Set Partners",
    "fintrilo": "Fintrilo",
    "mrd": "Relief Desk",
    "ccc": "Clarity Team",
    "spa": "Settlement Path Advisors",
    "lrl": "The Lab",
    "aab": "Alternatives Brief",
    "abr": "Breath Room",
    "icd": "ISO Care Desk",
    "mcb": "Crisis Brief",
    "slc": "Stack Literacy",
}

CTA_PHRASE = {
    "dag": "Schedule a consultation",
    "bds": "Book a discovery call",
    "bdn": "Talk to a specialist",
    "lsp": "Connect on next steps",
    "fintrilo": "Connect with a Liaison Officer",
    "mrd": "Book a pressure-map call",
    "ccc": "Run your clarity session",
    "spa": "Book a path review",
    "lrl": "Book a lab walkthrough",
    "aab": "Book an alternatives brief",
    "abr": "Book breath-room time",
    "icd": "Book a partner sync",
    "mcb": "Book a crisis brief",
    "slc": "Book a literacy session",
}

VOICE_OPENERS = {
    "dag": "This note is educational, not legal advice for your specific facts.",
    "bds": "We'll stay practical — cash, ACH, and fit — no courtroom theater.",
    "bdn": "Straight talk. Here's how this actually works.",
    "lsp": "Partner-facing note — alignment over noise.",
    "fintrilo": "One picture: funding, processing, and optimization in the same conversation.",
    "mrd": "Let's sort what is urgent vs what is merely loud.",
    "ccc": "Clarity first — frameworks and questions, not slogans.",
    "spa": "Think path and checkpoint, not countdown clock.",
    "lrl": "Scenario thinking before you lock a plan.",
    "aab": "Questions before capital — never a push to stack another advance.",
    "abr": "Drafts, retries, mid-week balance — grounded, low drama.",
    "icd": "ISO/broker hygiene: spot distress early, hand off clean.",
    "mcb": "Acute triage energy — calm, short, tripwire-aware.",
    "slc": "Definitions and whiteboard questions on stacking mechanics.",
}

# Per-brand angle libraries keyed by slot kind
BRAND_ANGLE = {
    "dag": {
        "welcome": ("A measured introduction from DAG Law", "Formal orientation for owners facing collection pressure."),
        "pain": ("When pressure becomes a legal question", "Notices, suits, and account freezes change the conversation."),
        "stack": ("Stacked obligations — informational overview", "Multiple pulls often collide with personal guaranty exposure."),
        "cost": ("Cost is not only the factor rate", "Litigation risk and PG exposure are part of the real picture."),
        "options": ("Counsel vs. non-counsel paths", "Know when educational brands stop and a law firm begins."),
        "mistakes": ("Panic replies that can hurt your position", "What not to put in writing under pressure."),
        "soft_cta": ("Consultation when the facts warrant it", "No hype — a conversation if legal risk is in play."),
        "mechanics": ("MCA contracts — what counsel often reviews", "UCC, confession clauses, and venue language at a high level."),
        "triage": ("Urgent legal events vs. loud collection noise", "Suits, levies, freezes — route to counsel."),
        "escalation": ("How escalation often appears in the file", "Demand letters, UCC filings, suit threats — informational."),
        "literacy": ("Settlement talk vs. legal strategy", "Settlement companies are not law firms; know the difference."),
        "scenarios": ("Composite: owner with PG + active suit risk", "Illustrative only — not your case, not a promise."),
        "risk": ("Personal guaranty — informational overview", "PG is where business stress becomes personal risk."),
        "readiness": ("What to bring to a consultation", "Documents and timeline — not a sales script."),
        "trust": ("Burned by aggressive collectors?", "Trust rebuild starts with accurate process education."),
        "commit": ("If legal pressure is active, talk to counsel", "Schedule a consultation — engagement is separate."),
    },
    "bds": {
        "welcome": ("Welcome from Business Debt Solutions", "Settlement and cash-flow restructuring — not a law firm."),
        "pain": ("Daily ACH is eating the week", "Name the pulls before you invent a desperate fix."),
        "stack": ("Stacked advances, one bank account", "Why mid-week balances feel like fiction."),
        "cost": ("Sketching true cost (illustrative)", "No fake stats — your statements are the source of truth."),
        "options": ("Discovery exists when you're ready", "Soft intro to how a settlement conversation works."),
        "mistakes": ("Don't ghost funders in a panic", "Communication hygiene beats radio silence."),
        "soft_cta": ("A discovery call — only when you're ready", "See if settlement is a fit. No guarantee of outcome."),
        "mechanics": ("Factor rate in merchant English", "What you repay vs. what hit the account."),
        "triage": ("Stabilize core ops first", "Payroll and rent before vanity vendors."),
        "escalation": ("When funders turn up the heat", "Patterns merchants report — education, not legal advice."),
        "literacy": ("What settlement is — and isn't", "No outcome promised. Fit questions matter."),
        "scenarios": ("Composite: multi-advance retail stack", "Illustrative walkthrough only."),
        "risk": ("If a suit shows up, pause and get counsel", "BDS is not a law firm — we route legal tripwires."),
        "readiness": ("Fit questions before enrollment", "Five questions we actually care about."),
        "trust": ("If you've been burned before", "Second-look discovery without countdown spam."),
        "commit": ("Enrollment-oriented discovery", "Book when the cash pain is real — urgency from ACH, not fake scarcity."),
    },
    "bdn": {
        "welcome": ("Ninja brief: you're not crazy", "Daily ACH chaos has a vocabulary. We'll teach it."),
        "pain": ("The mid-week balance lie", "Why Friday looks fine and Wednesday doesn't."),
        "stack": ("What “stacked” actually means", "Multiple advances, overlapping holds, one operating account."),
        "cost": ("Paying twice — the feeling vs. the math", "Education only. Illustrative, not a promise."),
        "options": ("Read this before you stack again", "Soft: understand mechanics → then talk to a specialist."),
        "mistakes": ("Broker culture traps", "Renewals and add-ons that sound helpful."),
        "soft_cta": ("Curious? Talk to a specialist", "Training energy, not a hard close."),
        "mechanics": ("Factor rate in plain English", "The ninjas' favorite whiteboard."),
        "triage": ("Urgent vs loud — a merchant drill", "Sort the fire from the smoke."),
        "escalation": ("How escalation often shows up", "Education on patterns — not legal advice."),
        "literacy": ("Settlement literacy without the pitch", "Definitions first."),
        "scenarios": ("Composite: broker-stacked retail", "Story-shaped education."),
        "risk": ("When education ends and counsel begins", "Suits/UCC → DAG territory."),
        "readiness": ("Myths that delay good decisions", "Kill the folklore."),
        "trust": ("Second look without the shame", "You're allowed to relearn this."),
        "commit": ("Ready for a human conversation?", "Specialist booking — still no fake scarcity."),
    },
    "lsp": {
        "welcome": ("Level Set — partner orientation", "Alignment for referral and ISO-adjacent partners."),
        "pain": ("When your merchant's ACH stress hits you", "Partner lens on merchant pressure."),
        "stack": ("Stack signals partners should spot", "Early flags before relationships burn."),
        "cost": ("True cost talk for partner desks", "Help merchants see math without selling fear."),
        "options": ("Referral paths that stay clean", "Connect / share / align — not consumer spam."),
        "mistakes": ("Handoffs that damage trust", "What not to promise on a warm transfer."),
        "soft_cta": ("Connect on next steps", "Book a partner sync."),
        "mechanics": ("MCA mechanics partners must explain fairly", "Education shared with merchant-facing brands."),
        "triage": ("Partner triage checklist", "When to pause funding talk and open relief talk."),
        "escalation": ("Escalation signals in partner pipelines", "Protect the relationship."),
        "literacy": ("Settlement vs funding — partner script hygiene", "Don't blur law and non-law."),
        "scenarios": ("Composite: ISO caught between funder and merchant", "Illustrative."),
        "risk": ("Legal tripwires — stop and route", "Partners are not counsel."),
        "readiness": ("Align before you enroll a referral", "Fit questions for partner desks."),
        "trust": ("Repairing a burned referral", "Trust rebuild playbook."),
        "commit": ("Partner sync + merchant handoff", "Connect when both sides are ready."),
    },
    "fintrilo": {
        "welcome": ("One picture beats three vendors", "Funding + processing + optimization under one liaison."),
        "pain": ("Fragmented vendors, fragmented cash", "Why separate shops miss the whole."),
        "stack": ("Processing float vs. advance pulls", "How Clover/payments talk meets MCA stress."),
        "cost": ("Cost of sprawl", "Multiple fees, multiple stories — one ledger reality."),
        "options": ("Liaison Officer conversation", "Listen, analyze, guide — not a single SKU pitch."),
        "mistakes": ("Buying another tool instead of a plan", "Anti-vendor-sprawl note."),
        "soft_cta": ("Connect with a Liaison Officer", "Discuss funding + payments when ready."),
        "mechanics": ("Funding options without fog", "Approvals/rates not guaranteed — education first."),
        "triage": ("Stabilize payments rails while cash is tight", "Processing hygiene under pressure."),
        "escalation": ("When capital talk must pause for legal", "Fintrilo is not a law firm."),
        "literacy": ("Optimization vs. settlement lanes", "Know which conversation you're in."),
        "scenarios": ("Composite: retail needing Clover + capital clarity", "Illustrative."),
        "risk": ("Debt-relief interest ≠ legal advice", "Route suits to counsel."),
        "readiness": ("What a liaison session covers", "Agenda without scarcity."),
        "trust": ("If prior funders overpromised", "Rebuild with clear terms talk."),
        "commit": ("Explore funding + payments fit", "Book the liaison conversation."),
    },
    "mrd": {
        "welcome": ("Welcome — let's name the pressure", "Calm triage desk for daily ACH overwhelm."),
        "pain": ("Urgent vs loud", "Sort the pulls that threaten payroll from the noise."),
        "stack": ("How many advances are pulling?", "Pressure-map question #1."),
        "cost": ("30-day cash if nothing changes", "A question, not a fake statistic."),
        "options": ("Pressure-map call exists", "Soft CTA — map before you move."),
        "mistakes": ("Desperate moves that backfire", "Stacking again, ghosting, panic transfers."),
        "soft_cta": ("Book a pressure-map call", "When you want a calm walkthrough."),
        "mechanics": ("Reading the ACH calendar", "Where drafts land in the week."),
        "triage": ("Pressure-map checklist", "MRD's core tool."),
        "escalation": ("When calm triage isn't enough", "Crisis → MCB; legal → DAG."),
        "literacy": ("Relief vs. settlement language", "We map; enrollment is a later conversation."),
        "scenarios": ("Composite: restaurant with three daily drafts", "Illustrative."),
        "risk": ("If the bank account freezes", "Pause soft help — get appropriate help."),
        "readiness": ("What we cover on a relief review", "Checklist energy."),
        "trust": ("Still getting hit daily?", "Re-open the map without shame."),
        "commit": ("Relief review → discovery handoff", "Book when the picture is clear enough."),
    },
    "ccc": {
        "welcome": ("Clarity before commitment", "Diagnostic education for stacked MCA math."),
        "pain": ("Why your mid-week balance lies", "Whiteboard the week."),
        "stack": ("Stacking on a spreadsheet", "Lines, dates, pulls — see it."),
        "cost": ("True cost sketch (illustrative)", "Your numbers only — no invented benchmarks."),
        "options": ("Clarity session teaser", "Frameworks over slogans."),
        "mistakes": ("Optimizing the wrong line item", "Cutting the wrong cost while ACH rages."),
        "soft_cta": ("Run your clarity session", "See the cash-flow picture."),
        "mechanics": ("Holdbacks and effective cost", "Plain diagnostic language."),
        "triage": ("Weekly cash picture under hardship", "What to track for 14 days."),
        "escalation": ("When numbers say escalate", "Data → human decision."),
        "literacy": ("Refinance vs settle — questions to ask", "Education, not advice."),
        "scenarios": ("Composite: clarity sheet for a multi-advance shop", "Illustrative."),
        "risk": ("Numbers can't replace counsel", "Legal events → DAG."),
        "readiness": ("Clarity → fit questions", "Hand off cleanly to settlement conversation."),
        "trust": ("If prior “audits” were sales pitches", "Our session is diagnostic."),
        "commit": ("Clarity session + options review", "Book when you want the picture."),
    },
    "spa": {
        "welcome": ("Path, not panic", "Settlement Path Advisors — stages and tradeoffs."),
        "pain": ("Pressure without a map", "Name stages before you sprint."),
        "stack": ("Stacked path checkpoints", "Where each advance sits on the path."),
        "cost": ("Tradeoffs on the path", "Time, cash, and creditor behavior — no guarantees."),
        "options": ("Options map teaser", "Path review when ready."),
        "mistakes": ("Skipping checkpoints", "Jumping to enrollment without fit."),
        "soft_cta": ("Book a path review", "Steady guide CTA."),
        "mechanics": ("How settlement paths are often sequenced", "Education — outcomes vary."),
        "triage": ("Path vs. crisis fork", "If on fire, triage first."),
        "escalation": ("Path checkpoints under creditor heat", "Adjust without drama."),
        "literacy": ("What settlement is — and isn't", "SPA core literacy."),
        "scenarios": ("Composite: path review for a service business", "Illustrative."),
        "risk": ("Legal fork on the path", "We are not a law firm."),
        "readiness": ("Readiness checklist", "Before enrollment talk."),
        "trust": ("Burned before? Trust rebuild", "Second-look path review."),
        "commit": ("Enrollment-adjacent path review", "Book when checkpoints clear."),
    },
    "lrl": {
        "welcome": ("Lab open — experiment before you lock", "Scenario A vs B thinking."),
        "pain": ("Ledger under ACH stress", "See obligations as experiments, not fate."),
        "stack": ("Stacking as a lab problem", "Variables: pull day, amount, cash buffer."),
        "cost": ("Scenario cost without fake stats", "Illustrative worksheets only."),
        "options": ("Reset session teaser", "Walk through scenarios."),
        "mistakes": ("Locking a plan on day-one emotion", "Lab first."),
        "soft_cta": ("Book a lab walkthrough", "Curious, structured CTA."),
        "mechanics": ("Modeling factor cost in scenarios", "Workshop tone."),
        "triage": ("Scenario A status quo vs B structured path", "LRL signature."),
        "escalation": ("When the lab says pause for counsel", "Tripwire routing."),
        "literacy": ("Settlement as a ledger redesign", "Education."),
        "scenarios": ("Composite: multi-advance restaurant lab", "Illustrative."),
        "risk": ("PG risk in the model", "Flag — don't practice law."),
        "readiness": ("Which scenario are you ready to test?", "Soft commit."),
        "trust": ("Prior plans that ignored the ledger", "Rebuild with scenarios."),
        "commit": ("Lab walkthrough → human decision", "Book the session."),
    },
    "aab": {
        "welcome": ("Before you take another advance", "Alternatives Brief — questions, not lending."),
        "pain": ("Quick capital fog", "Hard-money offers love urgency. We love checklists."),
        "stack": ("Why “one more” feels rational", "And why it often isn't."),
        "cost": ("Cost of the next advance (illustrative)", "Your term sheet, your math."),
        "options": ("Fund vs wait vs other path", "Map without a product push."),
        "mistakes": ("Signing under NSF panic", "Slow the pen."),
        "soft_cta": ("Book an alternatives brief", "Skeptical-but-fair educator CTA."),
        "mechanics": ("Reading a hard-money offer", "Questions to ask aloud."),
        "triage": ("Is this a capital problem or an ACH problem?", "Diagnostic fork."),
        "escalation": ("When another advance won't fix escalation", "Stop digging."),
        "literacy": ("Refinance vs stack vs settle — question set", "Education only."),
        "scenarios": ("Composite: owner offered a “save” refinance", "Illustrative."),
        "risk": ("Contracts that quietly add PG heat", "Flag for counsel if needed."),
        "readiness": ("Decision checklist before any new capital", "AAB core."),
        "trust": ("If the last broker oversold ease", "Brief without the fog."),
        "commit": ("Alternatives brief → options handoff", "Book the brief."),
    },
    "abr": {
        "welcome": ("Breath room for the ACH week", "Drafts, retries, mid-week balance — grounded help."),
        "pain": ("NSF spiral language", "Name retries without panic."),
        "stack": ("Overlapping draft windows", "Why the calendar feels stacked."),
        "cost": ("What drafts do to operating cash", "No fake averages — your bank history."),
        "options": ("Draft-pressure review", "Soft CTA."),
        "mistakes": ("Moving money in ways that trigger more retries", "Hygiene notes."),
        "soft_cta": ("Book breath-room time", "Request a draft-pressure review."),
        "mechanics": ("ACH timing 101 for merchants", "Practical, low drama."),
        "triage": ("This week's draft map", "Breath Room tool."),
        "escalation": ("When drafts become legal events", "Route out of soft lane."),
        "literacy": ("Breath room vs settlement talk", "Sequence the conversations."),
        "scenarios": ("Composite: NSF week in a service business", "Illustrative."),
        "risk": ("Frozen account? Stop DIY", "Get the right help."),
        "readiness": ("What we cover in breath-room time", "Agenda."),
        "trust": ("Still getting hit?", "Re-open without shame."),
        "commit": ("Breath-room → discovery handoff", "Book when ready."),
    },
    "icd": {
        "welcome": ("ISO Care Desk — handoff hygiene", "Spot merchant distress early; hand off clean."),
        "pain": ("When your funded merchant starts drowning", "Partner ops lens."),
        "stack": ("Stack signals on the ISO desk", "Flags before relationships burn."),
        "cost": ("Cost of a messy handoff", "Reputation > one more fund."),
        "options": ("Handoff brief request", "Partner sync CTA."),
        "mistakes": ("Promising settlement outcomes as an ISO", "Don't."),
        "soft_cta": ("Book a partner sync", "Reciprocal-value framing."),
        "mechanics": ("What to explain fairly about MCA cost", "Script-aware education."),
        "triage": ("Distress checklist for ISOs", "When to pause selling."),
        "escalation": ("Escalation without burning the funder", "Careful ops."),
        "literacy": ("Settlement lane vs funding lane", "Keep walls clear."),
        "scenarios": ("Composite: ISO between funder and stressed merchant", "Illustrative."),
        "risk": ("Legal tripwires — you are not counsel", "Route."),
        "readiness": ("Clean referral packet", "What good handoffs include."),
        "trust": ("Repairing partner trust after a bad transfer", "Playbook."),
        "commit": ("Partner sync + care handoff", "Book the sync."),
    },
    "mcb": {
        "welcome": ("Crisis Brief — this week’s fire", "Urgent-calm triage for 72-hour pressure."),
        "pain": ("Urgent vs loud in a crisis window", "Short paragraphs. Clear sorts."),
        "stack": ("Stacked drafts in a crisis week", "What to stop doing today."),
        "cost": ("Cost of waiting 72 more hours", "A question — not a fake stat."),
        "options": ("Crisis brief booking", "Human review soon."),
        "mistakes": ("Panic communications", "What not to send while hot."),
        "soft_cta": ("Book a crisis brief", "Schedule triage."),
        "mechanics": ("Crisis ≠ mechanics class", "Only what you need this week."),
        "triage": ("72-hour plan", "MCB signature."),
        "escalation": ("Legal tripwire → DAG", "We pause soft skins."),
        "literacy": ("After the fire: literacy later", "Stabilize first."),
        "scenarios": ("Composite: owner with suit threat this week", "Illustrative — may need counsel."),
        "risk": ("Account freeze / levy language", "Stop. Route to counsel."),
        "readiness": ("What triage needs from you", "Docs in 24 hours."),
        "trust": ("If last “help” vanished in a crisis", "We're here for the brief."),
        "commit": ("Crisis brief → next stable step", "Book triage now if on fire."),
    },
    "slc": {
        "welcome": ("Stack Literacy — class is open", "Definitions before decisions."),
        "pain": ("The “paying twice” feeling", "Name it precisely."),
        "stack": ("Stacking mechanics literacy", "Teacher energy."),
        "cost": ("Literacy on effective cost", "Illustrative worksheets — your numbers."),
        "options": ("Literacy session teaser", "Then options review."),
        "mistakes": ("Renewal language that hides a stack", "Read aloud."),
        "soft_cta": ("Book a literacy session", "Teacher CTA."),
        "mechanics": ("Holds, splits, and stack entries", "Whiteboard."),
        "triage": ("Literacy under cash stress", "Learn while stabilizing."),
        "escalation": ("When literacy isn't enough", "Hand off."),
        "literacy": ("Settlement words merchants confuse", "Glossary session."),
        "scenarios": ("Composite: stack literacy for a multi-advance shop", "Illustrative."),
        "risk": ("Contract words that imply PG heat", "Flag for counsel."),
        "readiness": ("Literacy → options review", "Clean handoff."),
        "trust": ("If education was just a sales funnel before", "This is literacy-first."),
        "commit": ("Literacy + options review", "Book the session."),
    },
}

PREVIEW = {
    "welcome": "Orientation without hype.",
    "pain": "Name it so you can manage it.",
    "stack": "Overlapping pulls, one account.",
    "cost": "Illustrative thinking — your numbers matter.",
    "options": "A map beats a panic move.",
    "mistakes": "Avoid the usual traps.",
    "soft_cta": "A calm next step when ready.",
    "mechanics": "Plain-English mechanics.",
    "triage": "Urgent vs loud.",
    "escalation": "How heat often shows up.",
    "literacy": "Definitions before commitment.",
    "scenarios": "Illustrative composite only.",
    "risk": "Know the tripwires.",
    "readiness": "Fit before enrollment talk.",
    "trust": "Second looks welcome.",
    "commit": "Book when the pain is real.",
}

MONTH_KIND = {
    2: ("mechanics", "triage"),
    3: ("triage", "soft_cta"),
    4: ("escalation", "options"),
    5: ("literacy", "readiness"),
    6: ("scenarios", "literacy"),
    7: ("risk", "mistakes"),
    8: ("readiness", "soft_cta"),
    9: ("trust", "options"),
    10: ("commit", "trust"),
}


def body_for(brand_id: str, kind: str, subject: str, preview: str, month: int, seq: int) -> str:
    b = BRANDS[brand_id]
    name = b["display_name"]
    angle = BRAND_ANGLE[brand_id][kind]
    sign = SIGN_OFF[brand_id]
    cta = CTA_PHRASE[brand_id]
    opener = VOICE_OPENERS[brand_id]
    theme, _ = MONTH_THEMES[month]
    utm_campaign = f"nb_{brand_id}_m{month:02d}"
    utm_content = f"{brand_id}_m{month:02d}_e{seq:02d}"

    # Audience framing
    if brand_id in ("lsp", "icd"):
        audience = "If you work with merchants carrying MCA / daily-ACH stress"
        biz = "your book of merchants"
    else:
        audience = "If {{business_name}} is dealing with MCA / daily-ACH pressure"
        biz = "{{business_name}}"

    bullets = {
        "welcome": [
            f"Who **{name}** is (and is not).",
            "What this 10-month education arc will cover.",
            "How to reply STOP anytime — no drama.",
        ],
        "pain": [
            "How many advances are pulling right now?",
            "Which pull threatens payroll vs. which is merely loud?",
            "What happens to cash if nothing changes for 30 days?",
        ],
        "stack": [
            "List each advance and pull cadence.",
            "Note overlapping draft windows.",
            "Flag any personal guaranty you remember signing.",
        ],
        "cost": [
            "Use your statements — not internet “averages.”",
            "Separate fee fog from cash leaving the account.",
            "Illustrative sketches only; not a promise of results.",
        ],
        "options": [
            "Stabilize communications.",
            "Map options (education).",
            "Talk to a human when ready — no fake scarcity.",
        ],
        "mistakes": [
            "Don't sign new capital under pure NSF panic.",
            "Don't ghost every funder at once without a plan.",
            "Don't treat educational brands as your attorney.",
        ],
        "soft_cta": [
            f"CTA style here: {cta}.",
            "Browse {{brand_url}} on your own time.",
            "Legal events (suit, levy, freeze) → pause and get counsel.",
        ],
        "mechanics": [
            "Factor / hold language in plain English.",
            "What “stacked” changes about effective cost.",
            "Questions to bring to a specialist — not DIY legal conclusions.",
        ],
        "triage": [
            "Protect payroll and critical vendors first.",
            "Write the ACH calendar for 14 days.",
            "Separate crisis-this-week from structural stack problems.",
        ],
        "escalation": [
            "Demand tone shifts and collection patterns (education).",
            "What not to put in angry emails.",
            "Tripwire: suit / UCC / freeze → law-firm lane (DAG), not DIY.",
        ],
        "literacy": [
            "Settlement / restructuring words without guarantees.",
            "Fit questions before any enrollment talk.",
            "Law firm vs. non-law brand — keep the wall clear.",
        ],
        "scenarios": [
            "Composite only — not your file, not a promise.",
            "What good questions look like in that story.",
            "Where a human review changes the path.",
        ],
        "risk": [
            "Personal guaranty and account pressure — high-level overview.",
            "Educational brands do not represent you in court.",
            "If legal process is active, speak with counsel.",
        ],
        "readiness": [
            "Documents worth gathering.",
            "What “fit” means before enrollment conversations.",
            "No outcome guarantees — ever.",
        ],
        "trust": [
            "It's normal to have been burned by hype before.",
            "Second looks are allowed.",
            "We won't use countdown-timer spam.",
        ],
        "commit": [
            f"When cash pain is real, {cta.lower()}.",
            "Urgency comes from your ACH reality — not invented scarcity.",
            "On conversion we stop other brand drips for this email.",
        ],
    }[kind]

    bullet_md = "\n".join(f"{i}. {t}" for i, t in enumerate(bullets, 1))

    return textwrap.dedent(f"""\
    # nurture-{brand_id}-m{month:02d}-e{seq:02d}

    **Subject:** {subject}
    **Preview:** {preview}
    **From brand:** {name}
    **Journey:** nurture-{brand_id}
    **Month:** {month} — {theme}
    **CTA URL:** `{{{{booking_url}}}}?utm_source=email&utm_medium=nurture&utm_campaign={utm_campaign}&utm_content={utm_content}`
    **Brand URL token:** `{{{{brand_url}}}}`

    ## Body (plain / HTML-ish markdown)

    Hi {{{{first_name}}}},

    {opener}

    {audience}, this note from **{name}** focuses on: *{angle[0]}*.

    {angle[1]}

    **For {biz} this week:**
    {bullet_md}

    No fake stats. No FM-lane hype. Wall: MGP / Debt Empire skins only.

    [{cta}]({{{{booking_url}}}}) · {{{{brand_url}}}}

    — {sign}
    ---
    {{{{brand_disclaimer}}}}

    {{{{postal_address}}}}

    Prefer not to hear from us? [Unsubscribe]({{{{unsub_url}}}}) or reply STOP.
    """)


def build_touches_for_brand(brand_id: str):
    """Return (touches list for sequences.json, files written)."""
    touches = []
    files = []
    brand_dir = CONTENT / brand_id
    brand_dir.mkdir(parents=True, exist_ok=True)

    # Month 1 kickoff
    for seq, (offset, kind, _default_subj) in enumerate(KICKOFF_SLOTS, 1):
        subj, _ = BRAND_ANGLE[brand_id][kind]
        preview = PREVIEW[kind]
        month = 1
        rel = f"content/nurture-by-brand/{brand_id}/month-01/e{seq:02d}-{kind}.md"
        path = PACK / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        md = body_for(brand_id, kind, subj, preview, month, seq)
        path.write_text(md)
        files.append(rel)
        touches.append({
            "id": f"nurture_{brand_id}_m01_e{seq:02d}",
            "offset_days": offset,
            "brand_id": brand_id,
            "content_path": rel,
            "subject": subj,
            "month": 1,
            "slot": kind,
        })

    # Months 2–10
    seq_counter = 1
    for m in range(2, 11):
        kinds = MONTH_KIND[m]
        base = (m - 1) * 30
        day_pair = (base + 5, base + 18)
        month_dir = CONTENT / brand_id / f"month-{m:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        for i, kind in enumerate(kinds):
            seq_counter += 1
            # local month email index 1..2
            local = i + 1
            offset = day_pair[i]
            subj, _ = BRAND_ANGLE[brand_id][kind]
            # differentiate month subjects slightly
            theme_name, _ = MONTH_THEMES[m]
            subject = f"{subj}" if m < 10 else subj
            if m == 10 and kind == "commit":
                subject = BRAND_ANGLE[brand_id]["commit"][0]
            preview = PREVIEW[kind]
            # global sequence number across journey for filename clarity
            global_seq = 7 + (m - 2) * 2 + local
            rel = f"content/nurture-by-brand/{brand_id}/month-{m:02d}/e{local:02d}-{kind}.md"
            path = PACK / rel
            md = body_for(brand_id, kind, subject, preview, m, global_seq)
            path.write_text(md)
            files.append(rel)
            touches.append({
                "id": f"nurture_{brand_id}_m{m:02d}_e{local:02d}",
                "offset_days": offset,
                "brand_id": brand_id,
                "content_path": rel,
                "subject": subject,
                "month": m,
                "slot": kind,
            })

    return touches, files


def write_brand_calendars(seq: dict, order: list[str]) -> None:
    """Persist per-brand calendars as source of truth (campaigns are generated FROM these)."""
    cal_dir = DELIVERY / "calendars"
    cal_dir.mkdir(parents=True, exist_ok=True)
    index = {
        "version": "1.0.0",
        "wall": "MGP",
        "description": "Per-brand sequence calendars are the source of truth. Campaigns (nurture-<brand>) are GENERATED from these files.",
        "generate_endpoint": "POST /api/campaigns/generate",
        "brands": [],
    }
    brands_map = {}
    for brand_id in order:
        jid = f"nurture-{brand_id}"
        j = seq["journeys"][jid]
        cal = {
            "version": "1.0.0",
            "wall": "MGP",
            "brand_id": brand_id,
            "journey_id": jid,
            "name": j["name"],
            "primary_goal": j.get("primary_goal", "booked_discovery_enrollment_call"),
            "cycle_member": j.get("cycle_member", True),
            "cadence": j.get("cadence"),
            "conversion_exit": j.get("conversion_exit"),
            "touches": [
                {
                    "id": t["id"],
                    "offset_days": t["offset_days"],
                    "brand_id": t["brand_id"],
                    "content_path": t["content_path"],
                    "subject": t["subject"],
                    "month": t.get("month"),
                    "slot": t.get("slot"),
                }
                for t in j["touches"]
            ],
        }
        (cal_dir / f"{brand_id}.json").write_text(json.dumps(cal, indent=2) + "\n")
        brands_map[brand_id] = f"delivery/calendars/{brand_id}.json"
        index["brands"].append({
            "brand_id": brand_id,
            "journey_id": jid,
            "calendar_path": f"delivery/calendars/{brand_id}.json",
            "touch_count": len(cal["touches"]),
            "offsets": [t["offset_days"] for t in cal["touches"]],
        })
    (cal_dir / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    (DELIVERY / "brand-calendars.json").write_text(json.dumps({
        "version": "1.0.0",
        "wall": "MGP",
        "source_of_truth": "delivery/calendars/<brandId>.json",
        "note": "Campaigns are generated FROM per-brand calendars. Edit calendar then run scripts/generate_campaign_from_calendar.py or POST /api/campaigns/generate.",
        "brands": brands_map,
        "index": "delivery/calendars/index.json",
    }, indent=2) + "\n")



def main():
    seq_path = DELIVERY / "sequences.json"
    seq = json.loads(seq_path.read_text())
    seq["version"] = "1.3.0"
    seq.setdefault("journeys", {})

    # Brand cycle + conversion exit policy
    seq["brand_cycle"] = {
        "enabled": True,
        "order": CYCLE_ORDER,
        "description": (
            "Contacts cycle through per-brand nurture journeys until conversion. "
            "Kickoff on each brand: D0/D2/D4/D6/D8/D10/D12, then months 2–10 at 2 touches/month. "
            "On conversion (booked_call | enrolled | convert_flag): stop ALL other brand sequences "
            "for that email; keep only post-convert track for the winning brand (client-edu handoff)."
        ),
        "rules": {
            "max_one_send_per_email_per_calendar_day": True,
            "cooldown_days_between_brand_switch": 3,
            "switch_after": "journey_complete_or_kickoff_plus_idle",
            "kickoff_complete_offsets": [0, 2, 4, 6, 8, 10, 12],
            "idle_days_after_last_touch_to_rotate": 14,
            "exclude_brands": ["mda"],
            "conversion_exit": {
                "triggers": ["booked_call", "enrolled", "convert_flag"],
                "action": "stop_all_other_brand_journeys",
                "winning_brand_next": "client-edu",
                "suppress_parallel_nurture": True,
            },
            "suppression": {
                "global_unsub_stops_all_brands": True,
                "same_day_multi_brand_forbidden": True,
            },
        },
    }

    total_emails = 0
    per_brand = {}
    for brand_id in CYCLE_ORDER:
        touches, files = build_touches_for_brand(brand_id)
        jid = f"nurture-{brand_id}"
        b = BRANDS[brand_id]
        seq["journeys"][jid] = {
            "name": f"{b['display_name']} — 10-month nurture",
            "primary_goal": "booked_discovery_enrollment_call",
            "brand_id": brand_id,
            "cycle_member": True,
            "cadence": {
                "kickoff": "every_other_day_d0_to_d12",
                "months_2_to_10": "2_per_month",
                "total_touches": len(touches),
            },
            "conversion_exit": {
                "on": ["booked_call", "enrolled", "convert_flag"],
                "then": "stop_sibling_brand_journeys_hand_to_client_edu",
            },
            "source_calendar": f"delivery/calendars/{brand_id}.json",
            "touches": touches,
        }
        per_brand[brand_id] = len(touches)
        total_emails += len(touches)
        print(f"  {brand_id}: {len(touches)} emails, {len(files)} files")

    # Keep shared multi-brand nurture intact
    assert "nurture" in seq["journeys"]

    seq_path.write_text(json.dumps(seq, indent=2) + "\n")

    write_brand_calendars(seq, CYCLE_ORDER)

    # brand-cycle.json companion for UI/ops
    cycle_doc = {
        "version": "1.0.0",
        "wall": "MGP",
        "order": CYCLE_ORDER,
        "exclude": ["mda"],
        "per_brand_emails": per_brand,
        "total_emails": total_emails,
        "brand_count": len(CYCLE_ORDER),
        "conversion_exit": seq["brand_cycle"]["rules"]["conversion_exit"],
        "cadence": {
            "kickoff_offsets_days": [0, 2, 4, 6, 8, 10, 12],
            "months_2_10": "2 emails/month (~day +5 and +18 within each 30-day month block)",
            "emails_per_brand": 25,
        },
    }
    (DELIVERY / "brand-cycle.json").write_text(json.dumps(cycle_doc, indent=2) + "\n")

    # CALENDAR-BY-BRAND.md
    lines = [
        "# Calendar by Brand — Per-Brand 10-Month Nurture",
        "",
        "**Wall:** MGP · **No MDA** · **No FM** · **DRY_RUN default / no live sends from this pack alone**",
        "",
        "## Cadence (all brands)",
        "",
        "| Phase | Timing | Emails |",
        "|-------|--------|--------|",
        "| Kickoff (Month 1, weeks 1–2) | Every other day: D0, D2, D4, D6, D8, D10, D12 | 7 |",
        "| Months 2–10 | ~2 / month (month_base+5, month_base+18) | 18 |",
        "| **Total per brand** | ~10 months | **25** |",
        "",
        "## Brand cycle (until conversion)",
        "",
        "Contacts are **not** locked to one brand forever. They cycle:",
        "",
        " → ".join(CYCLE_ORDER),
        "",
        "### Conversion exit",
        "",
        "On `booked_call` / `enrolled` / `convert_flag` for email E:",
        "1. Stop **all** other `nurture-<brand>` enrollments for E.",
        "2. Keep / start **client-edu** (or post-convert) for the **winning** brand only.",
        "3. Honor global unsubscribe across every brand.",
        "",
        "### Anti-collision",
        "",
        "- Max **one send per email per calendar day** (no two brands same day).",
        "- **3-day cooldown** when rotating to the next brand journey.",
        "- Rotate after journey complete, or after kickoff + 14 idle days (ops configurable).",
        "",
        f"**Brand count:** {len(CYCLE_ORDER)} · **Emails/brand:** 25 · **Total generated:** {total_emails}",
        "",
        "---",
        "",
    ]
    for brand_id in CYCLE_ORDER:
        b = BRANDS[brand_id]
        j = seq["journeys"][f"nurture-{brand_id}"]
        lines.append(f"## {b['display_name']} (`nurture-{brand_id}`)")
        lines.append("")
        lines.append(f"Voice: `{b.get('voice')}` · Disclaimer: `{b.get('legal_disclaimer_key')}` · From: `{b.get('from_email')}`")
        lines.append("")
        lines.append("| # | Day | Month | Slot | Subject | Path |")
        lines.append("|---|-----|-------|------|---------|------|")
        for i, t in enumerate(j["touches"], 1):
            lines.append(
                f"| {i} | D{t['offset_days']} | {t['month']} | {t['slot']} | {t['subject']} | `{t['content_path']}` |"
            )
        lines.append("")
    cal_path = PACK / "CALENDAR-BY-BRAND.md"
    cal_path.write_text("\n".join(lines) + "\n")

    summary = {
        "brand_count": len(CYCLE_ORDER),
        "emails_per_brand": 25,
        "total_emails": total_emails,
        "cycle_order": CYCLE_ORDER,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
