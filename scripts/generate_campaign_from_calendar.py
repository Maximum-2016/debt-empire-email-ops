#!/usr/bin/env python3
"""Generate nurture-<brand> journey + content stubs FROM per-brand calendar.

Source of truth: delivery/calendars/<brandId>.json
Output: delivery/sequences.json journeys["nurture-<brandId>"]
        content stubs at each touch content_path (create if missing; never wipe existing)

No MDA. No live sends. Safe to re-run (idempotent on sequences; stubs only if absent).

CLI:
  python3 scripts/generate_campaign_from_calendar.py --brand mrd
  python3 scripts/generate_campaign_from_calendar.py --all
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
DELIVERY = PACK / "delivery"
CAL_DIR = DELIVERY / "calendars"
SEQ_PATH = DELIVERY / "sequences.json"
REG_PATH = DELIVERY / "brand-registry.json"

EXCLUDE = {"mda"}


def load_registry():
    return {b["id"]: b for b in json.loads(REG_PATH.read_text())["brands"]}


def list_calendar_brands() -> list[str]:
    index_path = CAL_DIR / "index.json"
    if index_path.exists():
        idx = json.loads(index_path.read_text())
        return [b["brand_id"] for b in idx.get("brands", []) if b["brand_id"] not in EXCLUDE]
    return sorted(
        p.stem for p in CAL_DIR.glob("*.json") if p.stem not in ("index",) and p.stem not in EXCLUDE
    )


def load_calendar(brand_id: str) -> dict:
    if brand_id in EXCLUDE:
        raise ValueError("MDA is dead — no calendar / campaign")
    path = CAL_DIR / f"{brand_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing calendar: delivery/calendars/{brand_id}.json")
    cal = json.loads(path.read_text())
    if cal.get("brand_id") != brand_id:
        raise ValueError(f"calendar brand_id mismatch: {cal.get('brand_id')} != {brand_id}")
    return cal


def stub_markdown(brand: dict, touch: dict) -> str:
    """Minimal content stub when file is missing — does not invent long copy."""
    bid = brand["id"]
    name = brand.get("display_name") or bid
    subject = touch.get("subject") or touch.get("id")
    month = touch.get("month") or "?"
    slot = touch.get("slot") or "touch"
    tid = touch.get("id") or "touch"
    return f"""# {tid}

**Subject:** {subject}
**Preview:** (stub — fill from calendar / brand voice)
**From brand:** {name}
**Journey:** nurture-{bid}
**Month:** {month} · slot `{slot}`
**CTA URL:** `{{{{booking_url}}}}?utm_source=email&utm_medium=nurture&utm_campaign=nb_{bid}&utm_content={tid}`
**Brand URL token:** `{{{{brand_url}}}}`

## Body (plain / HTML-ish markdown)

Hi {{{{first_name}}}},

This is a **content stub** generated from the brand sequence calendar
(`delivery/calendars/{bid}.json`). Replace with full copy before live sends.

Focus for {{{{business_name}}}}: *{subject}*

[{name}]({{{{brand_url}}}}) · [Book]({{{{booking_url}}}})

Reply STOP anytime.

— {name}

{{{{brand_disclaimer}}}}
{{{{postal_address}}}}
{{{{unsub_url}}}}
"""


def ensure_content_stub(brand: dict, touch: dict) -> bool:
    """Create stub file if missing. Returns True if created."""
    rel = touch["content_path"]
    path = PACK / rel
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stub_markdown(brand, touch))
    return True


def journey_from_calendar(cal: dict) -> dict:
    touches = []
    for t in cal["touches"]:
        touches.append({
            "id": t["id"],
            "offset_days": int(t["offset_days"]),
            "brand_id": t["brand_id"],
            "content_path": t["content_path"],
            "subject": t["subject"],
            "month": t.get("month"),
            "slot": t.get("slot"),
        })
    return {
        "name": cal.get("name") or f"{cal['brand_id']} nurture",
        "primary_goal": cal.get("primary_goal", "booked_discovery_enrollment_call"),
        "brand_id": cal["brand_id"],
        "cycle_member": cal.get("cycle_member", True),
        "cadence": cal.get("cadence") or {
            "kickoff": "every_other_day_d0_to_d12",
            "months_2_to_10": "2_per_month",
            "total_touches": len(touches),
        },
        "conversion_exit": cal.get("conversion_exit") or {
            "on": ["booked_call", "enrolled", "convert_flag"],
            "then": "stop_sibling_brand_journeys_hand_to_client_edu",
        },
        "source_calendar": f"delivery/calendars/{cal['brand_id']}.json",
        "touches": touches,
    }


def generate_campaign(brand_id: str, *, write_stubs: bool = True) -> dict:
    """Build/update nurture-<brand> from calendar. Returns result summary."""
    brand_id = brand_id.strip().lower()
    if brand_id in EXCLUDE:
        raise ValueError("MDA is dead — refuse generate")
    brands = load_registry()
    if brand_id not in brands:
        raise ValueError(f"unknown brand_id: {brand_id}")
    cal = load_calendar(brand_id)
    brand = brands[brand_id]
    jid = cal.get("journey_id") or f"nurture-{brand_id}"

    stubs_created = []
    if write_stubs:
        for t in cal["touches"]:
            if ensure_content_stub(brand, t):
                stubs_created.append(t["content_path"])

    journey = journey_from_calendar(cal)
    seq = json.loads(SEQ_PATH.read_text())
    seq.setdefault("journeys", {})
    seq["journeys"][jid] = journey
    # bump patch if version looks semver-ish
    ver = seq.get("version", "1.0.0")
    seq["version"] = ver  # keep; calendar is SoT
    SEQ_PATH.write_text(json.dumps(seq, indent=2) + "\n")

    return {
        "ok": True,
        "brand_id": brand_id,
        "journey_id": jid,
        "calendar_path": f"delivery/calendars/{brand_id}.json",
        "touch_count": len(journey["touches"]),
        "stubs_created": stubs_created,
        "stubs_created_count": len(stubs_created),
        "dry_run_note": "No live sends. Campaign metadata + stubs only.",
    }


def generate_all(*, write_stubs: bool = True) -> dict:
    results = []
    for bid in list_calendar_brands():
        results.append(generate_campaign(bid, write_stubs=write_stubs))
    return {
        "ok": True,
        "brand_count": len(results),
        "results": results,
        "dry_run_note": "No live sends. Campaigns generated from calendars only.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate nurture campaign from brand calendar")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--brand", help="brand_id e.g. mrd")
    g.add_argument("--all", action="store_true", help="all calendars in delivery/calendars/")
    ap.add_argument("--no-stubs", action="store_true", help="update journey only; skip content stubs")
    args = ap.parse_args(argv)
    write_stubs = not args.no_stubs
    if args.all:
        out = generate_all(write_stubs=write_stubs)
    else:
        out = generate_campaign(args.brand, write_stubs=write_stubs)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
