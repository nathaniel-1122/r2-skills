#!/usr/bin/env python3
"""Log Nimble credits spent on a source-casting run to Cockpit's tracker.

Posts to Cockpit's /api/nimble-usage endpoint so the Admin "Nimble" card and the
Dashboard "API Spend" card stay current — without opening the app.

Reads two env vars:
  COCKPIT_URL        e.g. https://your-cockpit.vercel.app   (no trailing slash needed)
  NIMBLE_LOG_SECRET  the same secret set in Vercel's env (NIMBLE_LOG_SECRET)

Usage:
  python3 log_nimble_usage.py <credits> "<note>"
  python3 log_nimble_usage.py 120 "Munitions stockpile — 18 searches, 4 extracts"

Best-effort: prints a clear message and exits 0 even on failure, so it never
breaks the end of a casting run. The in-app "+ Log" form is the manual fallback.
"""
import json
import os
import sys
import urllib.request
import urllib.error


def main():
    if len(sys.argv) < 2:
        print("usage: log_nimble_usage.py <credits> [note]")
        return 0

    try:
        credits = float(sys.argv[1])
    except ValueError:
        print(f"⚠ Nimble log skipped — '{sys.argv[1]}' is not a number.")
        return 0
    if credits <= 0:
        print("⚠ Nimble log skipped — credits must be positive.")
        return 0

    note = sys.argv[2] if len(sys.argv) > 2 else ""

    base = (os.environ.get("COCKPIT_URL") or "").rstrip("/")
    secret = os.environ.get("NIMBLE_LOG_SECRET") or ""
    if not base or not secret:
        print("⚠ Nimble log skipped — set COCKPIT_URL and NIMBLE_LOG_SECRET in your "
              "shell env to enable auto-logging (or use the in-app '+ Log' form).")
        return 0

    payload = json.dumps({"credits": credits, "feature": "source-casting", "note": note}).encode()
    req = urllib.request.Request(
        base + "/api/nimble-usage",
        data=payload,
        method="POST",
        headers={
            "Authorization": "Bearer " + secret,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            json.loads(resp.read().decode() or "{}")
            print(f"✓ Logged {credits:g} Nimble credits to Cockpit"
                  + (f' ({note})' if note else "") + ".")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"⚠ Nimble log failed (HTTP {e.code}): {body[:200]}")
    except Exception as e:  # noqa: BLE001 — never break the run over telemetry
        print(f"⚠ Nimble log failed (network): {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
