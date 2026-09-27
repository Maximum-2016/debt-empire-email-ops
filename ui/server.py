#!/usr/bin/env python3
"""
Debt Empire Email Ops UI — local server (stdlib only).
MGP wall. Default DRY_RUN=true. No real send unless keys exist AND DRY_RUN=false.
"""
from __future__ import annotations

import sys
sys.stdout.reconfigure(line_buffering=True)

import csv
import json
import os
import re
import smtplib
import ssl
import traceback
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
PACK = ROOT.parent
DELIVERY = PACK / "delivery"
CONTENT = PACK / "content"
DATA = ROOT / "data"
PUBLIC = ROOT / "public"
SEED = ROOT / "seed"

HOST = os.environ.get("EMAIL_UI_HOST", "127.0.0.1")
PORT = int(os.environ.get("EMAIL_UI_PORT", "8765"))
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() not in ("0", "false", "no")
PROVIDER = os.environ.get("EMAIL_PROVIDER", "mailgun").lower()

DATA.mkdir(parents=True, exist_ok=True)
for name in ("contacts.json", "enrollments.json", "suppressions.json", "send_log.json"):
    p = DATA / name
    if not p.exists():
        p.write_text("[]\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n")


def brand_registry():
    return load_json(DELIVERY / "brand-registry.json")


def sequences():
    return load_json(DELIVERY / "sequences.json")


def calendars_dir() -> Path:
    return DELIVERY / "calendars"


def load_brand_calendar(brand_id: str) -> dict | None:
    p = calendars_dir() / f"{brand_id}.json"
    if not p.exists():
        return None
    return load_json(p)


def list_brand_calendars() -> dict:
    idx = calendars_dir() / "index.json"
    if idx.exists():
        return load_json(idx)
    brands = []
    for p in sorted(calendars_dir().glob("*.json")):
        if p.stem == "index":
            continue
        cal = load_json(p)
        brands.append({
            "brand_id": cal.get("brand_id") or p.stem,
            "journey_id": cal.get("journey_id") or f"nurture-{p.stem}",
            "calendar_path": f"delivery/calendars/{p.stem}.json",
            "touch_count": len(cal.get("touches") or []),
        })
    return {"version": "1.0.0", "wall": "MGP", "brands": brands}


def generate_campaign_for_brand(brand_id: str) -> dict:
    """Import generate script from pack/scripts and run for one brand."""
    import importlib.util
    script = PACK / "scripts" / "generate_campaign_from_calendar.py"
    spec = importlib.util.spec_from_file_location("gen_cal_campaign", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.generate_campaign(brand_id, write_stubs=True)



def read_content(rel: str) -> str:
    path = PACK / rel
    if not path.exists():
        return f"(missing content: {rel})"
    return path.read_text()


def render_tokens(text: str, contact: dict, brand: dict) -> str:
    booking_map = brand_registry().get("booking_url_placeholders", {})
    booking = booking_map.get(brand.get("booking_url_key", "booking_default"), "https://BOOKING.example")
    repl = {
        "{{first_name}}": contact.get("first_name") or "there",
        "{{last_name}}": contact.get("last_name") or "",
        "{{business_name}}": contact.get("business_name") or "your business",
        "{{email}}": contact.get("email") or "",
        "{{booking_url}}": os.environ.get("BOOKING_URL", booking),
        "{{brand_url}}": brand.get("brand_url") or "https://example.com",
        "{{unsub_url}}": os.environ.get("UNSUB_URL", "https://UNSUB.example/u/TOKEN"),
        "{{postal_address}}": os.environ.get(
            "POSTAL_ADDRESS", "[Postal address placeholder — Anthony to supply]"
        ),
        "{{brand_disclaimer}}": f"[{brand.get('legal_disclaimer_key', 'settlement_non_law')} disclaimer — see BRAND_KIT.md]",
        "{{year}}": str(datetime.now().year),
        "{{person}}": "Team",
        "{{brand_name}}": brand.get("display_name") or "",
    }
    out = text
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def parse_email_md(md: str) -> dict:
    subject = preview = brand = ""
    m = re.search(r"\*\*Subject:\*\*\s*(.+)", md)
    if m:
        subject = m.group(1).strip()
    m = re.search(r"\*\*Preview:\*\*\s*(.+)", md)
    if m:
        preview = m.group(1).strip()
    m = re.search(r"\*\*From brand:\*\*\s*(.+)", md)
    if m:
        brand = m.group(1).strip()
    body = md
    if "## Body" in md:
        body = md.split("## Body", 1)[1]
        body = re.sub(r"^\s*\(plain / HTML-ish markdown\)\s*", "", body.lstrip())
    return {"subject": subject, "preview": preview, "brand_name": brand, "body": body.strip()}


def find_brand(brand_id: str) -> dict | None:
    for b in brand_registry()["brands"]:
        if b["id"] == brand_id:
            return b
    return None



def brand_cycle_cfg() -> dict:
    seq = sequences()
    if seq.get("brand_cycle"):
        return seq["brand_cycle"]
    path = DELIVERY / "brand-cycle.json"
    if path.exists():
        return load_json(path)
    return {"enabled": False, "order": [], "rules": {}}


def cycle_order() -> list:
    cfg = brand_cycle_cfg()
    order = list(cfg.get("order") or [])
    exclude = set((cfg.get("rules") or {}).get("exclude_brands") or cfg.get("exclude") or ["mda"])
    return [b for b in order if b not in exclude and b != "mda"]


def stop_sibling_nurtures(enrollments: list, email: str, keep_journey: str | None = None) -> list:
    """Mark other nurture-* enrollments stopped_converted for this email."""
    out = []
    for e in enrollments:
        if e.get("email", "").lower() != email.lower():
            out.append(e)
            continue
        j = e.get("journey") or ""
        if j.startswith("nurture-") and j != keep_journey and e.get("status") == "active":
            e = {**e, "status": "stopped_converted", "stopped_at": now_iso()}
        out.append(e)
    return out


def infer_brand_id(enrollment: dict) -> str | None:
    """Infer brand_id from nurture-<id> journey or explicit fields."""
    if enrollment.get("brand_id"):
        return enrollment["brand_id"]
    if enrollment.get("winning_brand"):
        return enrollment["winning_brand"]
    j = enrollment.get("journey") or ""
    if j.startswith("nurture-"):
        return j[len("nurture-"):] or None
    return None


def enrich_enrollment(e: dict) -> dict:
    out = dict(e)
    bid = infer_brand_id(out)
    if bid and not out.get("brand_id"):
        out["brand_id"] = bid
    return out


def contact_for_email(email: str) -> dict | None:
    email = (email or "").lower().strip()
    for c in load_json(DATA / "contacts.json"):
        if c.get("email", "").lower() == email:
            return c
    return None


def is_suppressed(email: str) -> bool:
    email = (email or "").lower().strip()
    for row in load_json(DATA / "suppressions.json"):
        if row.get("email", "").lower() == email:
            return True
    return False


def provider_ready() -> dict:
    if PROVIDER == "ses":
        ready = bool(os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY")) or bool(
            os.environ.get("AWS_PROFILE")
        )
        # Also allow explicit SES key flag
        ready = ready or bool(os.environ.get("SES_READY") == "1")
        return {"provider": "ses", "keys_present": ready, "dry_run": DRY_RUN}
    # mailgun default
    ready = bool(os.environ.get("MAILGUN_API_KEY") and os.environ.get("MAILGUN_DOMAIN"))
    return {"provider": "mailgun", "keys_present": ready, "dry_run": DRY_RUN}


def send_via_mailgun(from_email, from_name, to, subject, text) -> dict:
    domain = os.environ["MAILGUN_DOMAIN"]
    api_key = os.environ["MAILGUN_API_KEY"]
    base = os.environ.get("MAILGUN_BASE_URL", "https://api.mailgun.net")
    url = f"{base}/v3/{domain}/messages"
    boundary = "----DebtEmpireBoundary7a3"
    parts = []
    fields = {
        "from": f"{from_name} <{from_email}>",
        "to": to,
        "subject": subject,
        "text": text,
    }
    body_bytes = b""
    for k, v in fields.items():
        body_bytes += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    body_bytes += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body_bytes, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    import base64

    token = base64.b64encode(f"api:{api_key}".encode()).decode()
    req.add_header("Authorization", f"Basic {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode()
        return {"ok": True, "status": resp.status, "body": raw}


def send_via_ses(from_email, from_name, to, subject, text) -> dict:
    # Prefer boto3 if present; else fail clearly
    try:
        import boto3
    except ImportError:
        return {"ok": False, "error": "boto3 not installed; pip install boto3 for SES live sends"}
    client = boto3.client("ses", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    kwargs = {
        "Source": f"{from_name} <{from_email}>",
        "Destination": {"ToAddresses": [to]},
        "Message": {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Text": {"Data": text, "Charset": "UTF-8"}},
        },
    }
    cfg = os.environ.get("SES_CONFIGURATION_SET")
    if cfg:
        kwargs["ConfigurationSetName"] = cfg
    resp = client.send_email(**kwargs)
    return {"ok": True, "message_id": resp.get("MessageId")}


def attempt_send(payload: dict) -> dict:
    status = provider_ready()
    log = load_json(DATA / "send_log.json")
    entry = {
        "at": now_iso(),
        "to": payload["to"],
        "subject": payload["subject"],
        "brand_id": payload.get("brand_id"),
        "touch_id": payload.get("touch_id"),
        "dry_run": True,
        "provider": status["provider"],
        "result": None,
    }
    if DRY_RUN or not status["keys_present"]:
        entry["result"] = {
            "mode": "dry_run",
            "reason": "DRY_RUN=true" if DRY_RUN else "provider keys missing",
            "preview_from": payload.get("from_email"),
        }
        log.append(entry)
        save_json(DATA / "send_log.json", log)
        return {"sent": False, "dry_run": True, "detail": entry["result"], "log_entry": entry}

    # Live path
    entry["dry_run"] = False
    try:
        if status["provider"] == "ses":
            result = send_via_ses(
                payload["from_email"], payload["from_name"], payload["to"], payload["subject"], payload["text"]
            )
        else:
            result = send_via_mailgun(
                payload["from_email"], payload["from_name"], payload["to"], payload["subject"], payload["text"]
            )
        entry["result"] = result
        log.append(entry)
        save_json(DATA / "send_log.json", log)
        return {"sent": bool(result.get("ok")), "dry_run": False, "detail": result, "log_entry": entry}
    except Exception as e:
        entry["result"] = {"ok": False, "error": str(e), "trace": traceback.format_exc()[-500:]}
        log.append(entry)
        save_json(DATA / "send_log.json", log)
        return {"sent": False, "dry_run": False, "detail": entry["result"], "log_entry": entry}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[email-ui] {self.address_string()} {fmt % args}")

    def _json(self, code: int, obj):
        raw = json.dumps(obj, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n == 0:
            return {}
        return json.loads(self.rfile.read(n).decode())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/"):
            return self.api_get(path, parse_qs(parsed.query))
        if path == "/" or path == "":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self._json(404, {"error": "not found"})
            return
        try:
            body = self._read_json()
        except Exception:
            self._json(400, {"error": "invalid json"})
            return
        return self.api_post(parsed.path, body)

    def api_get(self, path, qs):
        if path == "/api/health":
            return self._json(200, {
                "ok": True,
                "wall": "MGP",
                "umbrella": "Debt Empire",
                "dry_run": DRY_RUN,
                "provider": provider_ready(),
                "time": now_iso(),
            })
        if path == "/api/brands":
            return self._json(200, brand_registry())
        if path == "/api/sequences":
            return self._json(200, sequences())
        if path.startswith("/api/sequences/"):
            jid = path.split("/")[-1]
            seq = sequences()["journeys"].get(jid)
            if not seq:
                return self._json(404, {"error": "unknown journey"})
            return self._json(200, {"id": jid, **seq})
        if path == "/api/contacts":
            return self._json(200, {"contacts": load_json(DATA / "contacts.json")})
        if path == "/api/enrollments":
            return self._json(200, {"enrollments": load_json(DATA / "enrollments.json")})
        if path == "/api/suppressions":
            return self._json(200, {"suppressions": load_json(DATA / "suppressions.json")})
        if path == "/api/send-log":
            return self._json(200, {"log": load_json(DATA / "send_log.json")})
        if path == "/api/brand-cycle":
            cfg = brand_cycle_cfg()
            order = cycle_order()
            journeys = {f"nurture-{b}": sequences()["journeys"].get(f"nurture-{b}") for b in order}
            return self._json(200, {
                "enabled": cfg.get("enabled", True),
                "order": order,
                "rules": cfg.get("rules") or {},
                "journeys_present": {k: bool(v) for k, v in journeys.items()},
                "conversion_exit": (cfg.get("rules") or {}).get("conversion_exit") or cfg.get("conversion_exit"),
            })
        if path == "/api/calendar":
            # Flatten nurture + side tracks for UI calendar
            seq = sequences()
            return self._json(200, {
                "source_of_truth": "delivery/calendars/<brandId>.json",
                "note": "Per-brand calendars generate nurture-<brand> campaigns. Default UI view is per-brand.",
                "journeys": {
                    k: {
                        "name": v["name"],
                        "brand_id": v.get("brand_id"),
                        "source_calendar": v.get("source_calendar") or (
                            f"delivery/calendars/{v['brand_id']}.json" if v.get("brand_id") else None
                        ),
                        "touches": [
                            {
                                **t,
                                "brand": find_brand(t["brand_id"]),
                            }
                            for t in v["touches"]
                        ],
                    }
                    for k, v in seq["journeys"].items()
                }
            })
        if path == "/api/calendars":
            return self._json(200, list_brand_calendars())
        if path.startswith("/api/calendars/"):
            brand_id = path.split("/")[-1].strip().lower()
            if brand_id == "mda":
                return self._json(400, {"error": "MDA is dead — no calendar"})
            cal = load_brand_calendar(brand_id)
            if not cal:
                return self._json(404, {"error": f"no calendar for {brand_id}"})
            brand = find_brand(brand_id)
            return self._json(200, {
                **cal,
                "brand": brand,
                "touches": [
                    {**t, "brand": brand}
                    for t in cal.get("touches") or []
                ],
            })
        if path == "/api/status":
            email = (qs.get("email") or [None])[0]
            return self.status({"email": email} if email else {})
        if path == "/api/atlas/email/health":
            return self._json(200, {
                "ok": True,
                "wall": "MGP",
                "umbrella": "Debt Empire",
                "arm": "email-marketing",
                "version": "2.0",
                "dry_run": DRY_RUN,
                "provider": provider_ready(),
                "time": now_iso(),
            })
        if path == "/api/atlas/email/status":
            email = (qs.get("email") or [None])[0]
            return self.status({"email": email} if email else {})
        return self._json(404, {"error": "unknown endpoint"})

    def api_post(self, path, body):
        if path == "/api/contacts/import":
            return self.contacts_import(body)
        if path == "/api/contacts/seed":
            return self.contacts_seed()
        if path == "/api/enroll":
            return self.enroll(body)
        if path == "/api/preview":
            return self.preview(body)
        if path == "/api/send-test":
            return self.send_test(body)
        if path == "/api/suppressions":
            return self.add_suppression(body)
        if path == "/api/suppressions/remove":
            return self.remove_suppression(body)
        if path == "/api/convert":
            return self.convert(body)
        if path == "/api/cycle/advance":
            return self.cycle_advance(body)
        if path == "/api/campaigns/generate":
            return self.campaigns_generate(body)
        if path == "/api/pause":
            return self.pause(body)
        if path == "/api/resume":
            return self.resume(body)
        if path == "/api/status":
            return self.status(body)
        # ATLAS Email arm aliases (same handlers)
        if path == "/api/atlas/email/enroll":
            return self.enroll(body)
        if path == "/api/atlas/email/pause":
            return self.pause(body)
        if path == "/api/atlas/email/resume":
            return self.resume(body)
        if path == "/api/atlas/email/convert":
            return self.convert(body)
        if path == "/api/atlas/email/cycle/advance":
            return self.cycle_advance(body)
        if path == "/api/atlas/email/status":
            return self.status(body)
        return self._json(404, {"error": "unknown endpoint"})



    def campaigns_generate(self, body):
        """Build/update nurture-<brand> journey + content stubs FROM delivery/calendars/<brand>.json.

        Body: { "brand_id": "mrd" } or { "all": true }
        No live sends. DRY_RUN is irrelevant here (metadata/stubs only).
        """
        if body.get("all"):
            import importlib.util
            script = PACK / "scripts" / "generate_campaign_from_calendar.py"
            spec = importlib.util.spec_from_file_location("gen_cal_campaign", script)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            try:
                result = mod.generate_all(write_stubs=True)
            except Exception as e:
                return self._json(400, {"error": str(e)})
            return self._json(200, result)
        brand_id = (body.get("brand_id") or body.get("brand") or "").strip().lower()
        if not brand_id:
            return self._json(400, {"error": "brand_id required (or all:true)"})
        if brand_id == "mda":
            return self._json(400, {"error": "MDA is dead — refuse generate"})
        try:
            result = generate_campaign_for_brand(brand_id)
        except FileNotFoundError as e:
            return self._json(404, {"error": str(e)})
        except ValueError as e:
            return self._json(400, {"error": str(e)})
        except Exception as e:
            return self._json(500, {"error": str(e)})
        return self._json(200, result)


    def pause(self, body):
        """Pause active enrollment(s) for an email. Optional journey filter."""
        email = (body.get("email") or "").lower().strip()
        journey = (body.get("journey") or "").strip() or None
        reason = body.get("reason")
        if not email:
            return self._json(400, {"error": "email required"})
        enrollments = load_json(DATA / "enrollments.json")
        paused = []
        for i, e in enumerate(enrollments):
            if e.get("email", "").lower() != email:
                continue
            if e.get("status") != "active":
                continue
            if journey and e.get("journey") != journey:
                continue
            updated = {
                **e,
                "status": "paused",
                "paused_at": now_iso(),
            }
            if reason is not None:
                updated["pause_reason"] = reason
            enrollments[i] = updated
            paused.append(enrich_enrollment(updated))
        if not paused:
            return self._json(404, {"error": "no active enrollment matching", "email": email, "journey": journey})
        save_json(DATA / "enrollments.json", enrollments)
        return self._json(200, {"ok": True, "email": email, "paused": paused, "count": len(paused)})

    def resume(self, body):
        """Resume paused enrollment(s). Will not resume terminal or suppressed."""
        email = (body.get("email") or "").lower().strip()
        journey = (body.get("journey") or "").strip() or None
        if not email:
            return self._json(400, {"error": "email required"})
        if is_suppressed(email):
            return self._json(403, {"error": "contact is suppressed — cannot resume"})
        terminal = {"stopped_converted", "converted", "rotated"}
        enrollments = load_json(DATA / "enrollments.json")
        resumed = []
        blocked = []
        for i, e in enumerate(enrollments):
            if e.get("email", "").lower() != email:
                continue
            if journey and e.get("journey") != journey:
                continue
            st = e.get("status")
            if st in terminal:
                blocked.append({"id": e.get("id"), "status": st, "reason": "terminal_status"})
                continue
            if st != "paused":
                continue
            updated = {**e, "status": "active", "resumed_at": now_iso()}
            updated.pop("pause_reason", None)
            # keep paused_at for history; clear live pause marker conceptually via status
            enrollments[i] = updated
            resumed.append(enrich_enrollment(updated))
        if not resumed:
            if blocked and journey:
                return self._json(400, {
                    "error": "cannot resume terminal enrollment",
                    "email": email,
                    "blocked": blocked,
                })
            return self._json(404, {"error": "no paused enrollment matching", "email": email, "journey": journey})
        save_json(DATA / "enrollments.json", enrollments)
        return self._json(200, {
            "ok": True,
            "email": email,
            "resumed": resumed,
            "count": len(resumed),
            "blocked": blocked or None,
        })

    def status(self, body):
        """ATLAS-facing status for one email."""
        email = (body.get("email") or "").lower().strip()
        if not email:
            return self._json(400, {"error": "email required"})
        suppressed = is_suppressed(email)
        contact = contact_for_email(email)
        enrollments = load_json(DATA / "enrollments.json")
        mine = [enrich_enrollment(e) for e in enrollments if e.get("email", "").lower() == email]
        active = [e for e in mine if e.get("status") == "active"]
        paused = [e for e in mine if e.get("status") == "paused"]
        history_statuses = {"converted", "rotated", "stopped_converted"}
        history = [e for e in mine if e.get("status") in history_statuses]

        order = cycle_order()
        converted = bool(contact and contact.get("converted"))
        winning = (contact or {}).get("winning_brand")
        current_brand = None
        for e in active:
            j = e.get("journey") or ""
            if j.startswith("nurture-"):
                current_brand = e.get("brand_id") or j[len("nurture-"):]
                break
            if j == "client-edu" and e.get("winning_brand"):
                current_brand = e.get("winning_brand")
        if current_brand is None:
            for e in paused:
                j = e.get("journey") or ""
                if j.startswith("nurture-"):
                    current_brand = e.get("brand_id") or j[len("nurture-"):]
                    break

        next_actions = []
        if not suppressed and not converted:
            next_actions.append("enroll")
        if active and not suppressed:
            next_actions.append("pause")
        if paused and not suppressed:
            next_actions.append("resume")
        if active and any(str(e.get("journey", "")).startswith("nurture-") for e in active) and not converted and not suppressed:
            next_actions.append("convert")
            next_actions.append("cycle_advance")
        # Always allow status re-check
        # (status itself is not listed — next_actions are mutation/ops actions that make sense)

        return self._json(200, {
            "email": email,
            "suppressed": suppressed,
            "contact": contact,
            "active": active,
            "paused": paused,
            "history": history,
            "brand_cycle": {
                "order": order,
                "current_brand": current_brand,
                "converted": converted,
                "winning_brand": winning,
            },
            "dry_run": DRY_RUN,
            "provider": PROVIDER,
            "next_actions": next_actions,
        })

    def convert(self, body):
        """Conversion exit: stop sibling brand nurtures; hand to client-edu for winning brand."""
        email = (body.get("email") or "").lower().strip()
        winning = (body.get("winning_brand") or body.get("brand_id") or "").strip()
        trigger = body.get("trigger") or "convert_flag"
        if trigger not in ("booked_call", "enrolled", "convert_flag"):
            return self._json(400, {"error": "trigger must be booked_call|enrolled|convert_flag"})
        if not email or not winning:
            return self._json(400, {"error": "email and winning_brand required"})
        if winning == "mda":
            return self._json(400, {"error": "MDA is dead — pick another brand"})
        enrollments = load_json(DATA / "enrollments.json")
        keep = f"nurture-{winning}"
        enrollments = stop_sibling_nurtures(enrollments, email, keep_journey=keep)
        # mark winning nurture converted
        for i, e in enumerate(enrollments):
            if e.get("email") == email and e.get("journey") == keep and e.get("status") == "active":
                enrollments[i] = {**e, "status": "converted", "converted_at": now_iso(), "convert_trigger": trigger}
        # enroll client-edu post-convert
        cohort = body.get("cohort") or f"post-convert-{winning}"
        ce_id = f"{cohort}:{email}:client-edu"
        enrollments = [e for e in enrollments if e.get("id") != ce_id]
        ce = {
            "id": ce_id,
            "cohort": cohort,
            "email": email,
            "journey": "client-edu",
            "enrolled_at": now_iso(),
            "start_day_offset": 0,
            "status": "active",
            "winning_brand": winning,
            "convert_trigger": trigger,
            "post_convert": True,
        }
        enrollments.append(ce)
        # stamp contact
        contacts = load_json(DATA / "contacts.json")
        for c in contacts:
            if c.get("email", "").lower() == email:
                c["converted"] = True
                c["winning_brand"] = winning
                c["convert_trigger"] = trigger
                c["converted_at"] = now_iso()
        save_json(DATA / "contacts.json", contacts)
        save_json(DATA / "enrollments.json", enrollments)
        return self._json(200, {
            "ok": True,
            "email": email,
            "winning_brand": winning,
            "trigger": trigger,
            "stopped_siblings": True,
            "next_journey": "client-edu",
            "enrollments": [e for e in enrollments if e.get("email") == email],
        })

    def cycle_advance(self, body):
        """Advance email to next brand in cycle (blocked if converted/suppressed)."""
        email = (body.get("email") or "").lower().strip()
        if not email:
            return self._json(400, {"error": "email required"})
        if is_suppressed(email):
            return self._json(400, {"error": "suppressed"})
        contacts = load_json(DATA / "contacts.json")
        contact = next((c for c in contacts if c.get("email", "").lower() == email), None)
        if contact and contact.get("converted"):
            return self._json(400, {"error": "already converted — cycle stopped", "winning_brand": contact.get("winning_brand")})
        order = cycle_order()
        enrollments = load_json(DATA / "enrollments.json")
        active = [e for e in enrollments if e.get("email") == email and e.get("status") == "active" and str(e.get("journey","")).startswith("nurture-")]
        idx = 0
        if active and active[-1].get("cycle_index") is not None:
            idx = int(active[-1]["cycle_index"]) + 1
        elif body.get("cycle_index") is not None:
            idx = int(body["cycle_index"])
        if idx >= len(order):
            return self._json(200, {"ok": True, "done": True, "message": "cycle order exhausted without conversion"})
        # stop current active nurtures (completed rotation, not conversion)
        for i, e in enumerate(enrollments):
            if e.get("email") == email and e.get("status") == "active" and str(e.get("journey","")).startswith("nurture-"):
                enrollments[i] = {**e, "status": "rotated", "rotated_at": now_iso()}
        save_json(DATA / "enrollments.json", enrollments)
        # enroll next via enroll()
        return self.enroll({
            "emails": [email],
            "journey": "brand-cycle",
            "cycle_index": idx,
            "cohort": body.get("cohort") or f"cycle-{order[idx]}",
            "start_day_offset": 0,
        })

    def contacts_seed(self):
        seed_csv = SEED / "fake-contacts.csv"
        if not seed_csv.exists():
            # copy from import-schema examples
            seed_csv.write_text((DELIVERY / "import-schema.csv").read_text())
        return self.contacts_import({"csv_text": seed_csv.read_text(), "replace": False})

    def contacts_import(self, body):
        csv_text = body.get("csv_text") or ""
        if not csv_text and body.get("rows"):
            rows = body["rows"]
        else:
            reader = csv.DictReader(csv_text.splitlines())
            rows = list(reader)
        contacts = load_json(DATA / "contacts.json")
        by_email = {c["email"].lower(): c for c in contacts if c.get("email")}
        added = updated = 0
        for row in rows:
            email = (row.get("email") or "").strip().lower()
            if not email:
                continue
            rec = {
                "email": email,
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "business_name": row.get("business_name", ""),
                "phone": row.get("phone", ""),
                "country": row.get("country", "US"),
                "consent_email": row.get("consent_email", ""),
                "consent_source": row.get("consent_source", ""),
                "consent_timestamp": row.get("consent_timestamp", ""),
                "segment": row.get("segment", "leads_open"),
                "journey": row.get("journey", "nurture"),
                "brand_affinity": row.get("brand_affinity", ""),
                "salesforce_id": row.get("salesforce_id", ""),
                "partner_id": row.get("partner_id", ""),
                "notes": row.get("notes", ""),
                "imported_at": now_iso(),
            }
            if email in by_email:
                by_email[email].update(rec)
                updated += 1
            else:
                by_email[email] = rec
                added += 1
        save_json(DATA / "contacts.json", list(by_email.values()))
        return self._json(200, {"ok": True, "added": added, "updated": updated, "total": len(by_email)})

    def enroll(self, body):
        emails = body.get("emails") or []
        journey = body.get("journey") or "nurture"
        cohort = body.get("cohort") or f"test-{datetime.now().strftime('%Y%m%d')}"
        cycle_index = body.get("cycle_index")
        if body.get("segment"):
            contacts = [c for c in load_json(DATA / "contacts.json") if c.get("segment") == body["segment"]]
            emails = [c["email"] for c in contacts]
        if not emails:
            return self._json(400, {"error": "emails or segment required"})

        # Meta journey: brand-cycle → enroll into nurture-<order[cycle_index]>
        cycle_meta = None
        if journey == "brand-cycle":
            order = cycle_order()
            if not order:
                return self._json(400, {"error": "brand cycle order empty"})
            idx = int(cycle_index if cycle_index is not None else 0) % len(order)
            brand_id = order[idx]
            journey = f"nurture-{brand_id}"
            cycle_meta = {"cycle_index": idx, "brand_id": brand_id, "order": order}

        seq = sequences()["journeys"].get(journey)
        if not seq:
            return self._json(400, {"error": f"unknown journey {journey}"})
        enrollments = load_json(DATA / "enrollments.json")
        created = []
        for email in emails:
            email_l = email.lower().strip()
            if is_suppressed(email_l):
                continue
            contact = next((c for c in load_json(DATA / "contacts.json") if c["email"].lower() == email_l), None)
            if not contact:
                continue
            # Anti-collision: if another nurture-* is active, do not double-enroll same day path
            # (demo: still allow replace of same journey id)
            rec = {
                "id": f"{cohort}:{email_l}:{journey}",
                "cohort": cohort,
                "email": email_l,
                "journey": journey,
                "enrolled_at": now_iso(),
                "start_day_offset": int(body.get("start_day_offset") or 0),
                "status": "active",
                "brand_id": seq.get("brand_id") or (seq.get("touches") or [{}])[0].get("brand_id"),
            }
            if cycle_meta:
                rec["cycle_index"] = cycle_meta["cycle_index"]
                rec["cycle_order"] = cycle_meta["order"]
                rec["cycle_member"] = True
            enrollments = [e for e in enrollments if e.get("id") != rec["id"]]
            enrollments.append(rec)
            created.append(rec)
        save_json(DATA / "enrollments.json", enrollments)
        return self._json(200, {
            "ok": True,
            "enrolled": created,
            "count": len(created),
            "cycle": cycle_meta,
            "note": "Mailgun-first · DRY_RUN default · no MDA · max one brand send/email/day",
        })


    def preview(self, body):
        journey = body.get("journey") or "nurture"
        touch_id = body.get("touch_id")
        day = body.get("day")
        email = (body.get("email") or "").lower().strip()
        seq = sequences()["journeys"].get(journey)
        if not seq:
            return self._json(400, {"error": "unknown journey"})
        touch = None
        if touch_id:
            touch = next((t for t in seq["touches"] if t["id"] == touch_id), None)
        elif day is not None:
            day = int(day)
            # nearest touch at or before day, else first on/after
            candidates = sorted(seq["touches"], key=lambda t: t["offset_days"])
            touch = next((t for t in candidates if t["offset_days"] == day), None)
            if not touch:
                before = [t for t in candidates if t["offset_days"] <= day]
                touch = before[-1] if before else candidates[0]
        else:
            touch = seq["touches"][0]
        if not touch:
            return self._json(404, {"error": "touch not found"})
        brand = find_brand(touch["brand_id"])
        contact = next((c for c in load_json(DATA / "contacts.json") if c["email"].lower() == email), None)
        if not contact:
            contact = {
                "email": email or "preview@example.com",
                "first_name": body.get("first_name") or "Alex",
                "business_name": body.get("business_name") or "Demo Merchant LLC",
            }
        raw = read_content(touch["content_path"])
        parsed = parse_email_md(raw)
        rendered_body = render_tokens(parsed["body"], contact, brand or {})
        rendered_subject = render_tokens(parsed["subject"] or touch["subject"], contact, brand or {})
        return self._json(200, {
            "journey": journey,
            "touch": touch,
            "brand": brand,
            "contact": contact,
            "day_offset": touch["offset_days"],
            "subject": rendered_subject,
            "preview_text": parsed["preview"],
            "from_email": (brand or {}).get("from_email"),
            "from_name": render_tokens((brand or {}).get("from_name_pattern") or "Debt Empire", contact, brand or {}),
            "body": rendered_body,
            "suppressed": is_suppressed(contact.get("email", "")),
            "provider": provider_ready(),
        })

    def send_test(self, body):
        """Gated test send. Requires confirm=true. Respects DRY_RUN + keys."""
        if not body.get("confirm"):
            return self._json(400, {"error": "confirm:true required"})
        to = (body.get("to") or body.get("email") or "").strip()
        if not to:
            return self._json(400, {"error": "to email required"})
        if is_suppressed(to):
            return self._json(403, {"error": "recipient is suppressed"})
        # Build preview first
        prev_body = {
            "journey": body.get("journey") or "nurture",
            "touch_id": body.get("touch_id"),
            "day": body.get("day"),
            "email": to,
            "first_name": body.get("first_name"),
            "business_name": body.get("business_name"),
        }
        # inline preview logic
        journey = prev_body["journey"]
        seq = sequences()["journeys"].get(journey)
        touch = None
        if prev_body.get("touch_id"):
            touch = next((t for t in seq["touches"] if t["id"] == prev_body["touch_id"]), None)
        else:
            touch = seq["touches"][0]
        brand = find_brand(touch["brand_id"])
        contact = next((c for c in load_json(DATA / "contacts.json") if c["email"].lower() == to.lower()), None) or {
            "email": to,
            "first_name": body.get("first_name") or "Anthony",
            "business_name": body.get("business_name") or "Debt Empire Test",
        }
        raw = read_content(touch["content_path"])
        parsed = parse_email_md(raw)
        subject = render_tokens(parsed["subject"] or touch["subject"], contact, brand)
        text = render_tokens(parsed["body"], contact, brand)
        # Prefix subject in dry-run clarity
        if DRY_RUN:
            subject = f"[DRY-RUN] {subject}"
        payload = {
            "to": to,
            "subject": subject,
            "text": text,
            "from_email": body.get("from_email") or brand.get("from_email"),
            "from_name": render_tokens(brand.get("from_name_pattern") or "Debt Empire", contact, brand),
            "brand_id": brand.get("id"),
            "touch_id": touch["id"],
        }
        # Optional override from-address for verified domain tests
        if os.environ.get("TEST_FROM_EMAIL"):
            payload["from_email"] = os.environ["TEST_FROM_EMAIL"]
            payload["from_name"] = os.environ.get("TEST_FROM_NAME", "Debt Empire Test")
        result = attempt_send(payload)
        return self._json(200, {
            "ok": True,
            "payload_meta": {
                "to": to,
                "subject": subject,
                "brand_id": payload["brand_id"],
                "touch_id": payload["touch_id"],
                "from_email": payload["from_email"],
            },
            **result,
        })

    def add_suppression(self, body):
        email = (body.get("email") or "").lower().strip()
        if not email:
            return self._json(400, {"error": "email required"})
        rows = load_json(DATA / "suppressions.json")
        if not any(r.get("email") == email for r in rows):
            rows.append({
                "email": email,
                "reason": body.get("reason") or "manual",
                "at": now_iso(),
            })
            save_json(DATA / "suppressions.json", rows)
        return self._json(200, {"ok": True, "suppressions": rows})

    def remove_suppression(self, body):
        email = (body.get("email") or "").lower().strip()
        rows = [r for r in load_json(DATA / "suppressions.json") if r.get("email") != email]
        save_json(DATA / "suppressions.json", rows)
        return self._json(200, {"ok": True, "suppressions": rows})


def main():
    # seed fake contacts file
    seed = SEED / "fake-contacts.csv"
    if not seed.exists():
        seed.write_text((DELIVERY / "import-schema.csv").read_text())
    print(f"Debt Empire Email UI · MGP wall")
    print(f"  http://{HOST}:{PORT}/")
    print(f"  DRY_RUN={DRY_RUN}  PROVIDER={PROVIDER}  keys={provider_ready()['keys_present']}")
    print(f"  Pack: {PACK}")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
