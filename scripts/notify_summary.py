"""
Formats the daily Telegram summary from the GitHub Actions run's own
job list (piped in as JSON on stdin — see .github/workflows/scrape.yml).

Kept as a real script rather than an inline `python -c '...'` in the
workflow YAML because the message text needs literal quotes/emoji that
are painful to nest correctly inside YAML's own quoting.
"""

import json
import sys

# Guards against a crash if this ever runs somewhere whose stdout isn't
# UTF-8 (the GitHub Actions Ubuntu runner this actually runs on doesn't
# hit this, but Windows' default console codepage can't encode emoji).
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def build_summary(jobs_json: dict) -> str:
    lines = []
    failed = 0
    for job in jobs_json["jobs"]:
        if job["name"] == "notify":
            continue
        module = job["name"].split("(")[-1].rstrip(")")
        ok = job["conclusion"] == "success"
        if not ok:
            failed += 1
        icon = "✅" if ok else "❌"
        lines.append(f"{icon} {module}")

    header = "✅ Daily scrape — all modules OK" if failed == 0 else f"⚠️ Daily scrape — {failed} module(s) failed"
    return header + "\n\n" + "\n".join(lines)


if __name__ == "__main__":
    print(build_summary(json.load(sys.stdin)))
