#!/usr/bin/env python3
"""Mechanical checks for a brain (a workspace with _System/BRAIN-RULES.md). Read-only: it reports, never edits.

    python -I _tools/brain_check.py [BRAIN_DIR] [--exec] [--today YYYY-MM-DD]

BRAIN_DIR defaults to the current folder. By default the brain is treated as the TEAM brain, so any
note with sensitivity: exec, any link into an exec path, and any exec-word hit is reported. Pass
--exec when checking the restricted brain itself (those three checks are skipped).

Errors (exit 1): missing or disallowed frontmatter fields, owner blank or "AI", blank source_uri,
credential or card patterns, exec notes in a team brain, _CONTEXT.md past 100 lines, notes past 500 KB.
Warnings (exit 0): review_by passed, notes past 100 KB or 1,000 lines, em or en dashes, exec-word hits
(a hit forces a read, it never decides), links into exec paths.
Links that do not resolve are links.py's job. Skipped: evidence, archive, logs, inboxes, templates,
_index.md, README.md, the setup pack, and dot folders. The exec-word watch also skips _System/. Standard library only.
"""
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REQUIRED = ["type", "id", "title", "status", "owner", "sensitivity", "created", "updated",
            "last_reviewed", "review_by", "confidence", "source_kind", "source_uri",
            "source_date", "freshness_state"]
ALLOWED = {
    "type": "context rules reference company person product supplier customer channel policy decision routine action sop meeting project incident review inbox log evidence hub".split(),
    "status": "draft active historical deprecated superseded archived open waiting blocked done cancelled proposed accepted".split(),
    "sensitivity": ["team", "exec"],
    "confidence": ["high", "medium", "low"],
    "source_kind": "api email slack whatsapp call document session person mixed generated".split(),
    "freshness_state": ["current", "stale", "unavailable", "conflicted", "unverified"],
}
SKIP_DIRS = {"plugins", "91-Evidence", "99-Archive", "90-Logs", "00-Inbox", "Setup-Pack", "_templates", "_tools", "node_modules"}
SKIP_FILES = {"_index.md", "readme.md", "agents.md", "claude.md", "gemini.md"}
EXEC_WORDS = ("cash", "overdue", "hmrc", "irs", "arrears", "solicitor", "dispute", "claim", "breach",
              "redundancy", "disciplinary", "salary", "payroll", "commission", "margin", "cashflow",
              "forecast", "bank account", "resignation", "investor", "acquisition", "equity", "funding", "nda")
EXEC_WORD_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in EXEC_WORDS) + r")\b", re.I)
CREDENTIALS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("API key or token", re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16})\b")),
    ("password assignment", re.compile(r"\b(password|passwd|secret|api[_ -]?key|token)\s*[:=]\s*[^\s<>{}\[\]|]{6,}", re.I)),
    ("card number", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("IBAN", re.compile(r"\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]{4}){3,7}(?:[ ]?[A-Z0-9]{1,3})?\b")),
]
LINK_RE = re.compile(r"\]\(([^)#\s]+)")


def split(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return "", text


def fields(front):
    out = {}
    for line in front.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            v = re.split(r"\s+#", m.group(2), maxsplit=1)[0].strip().strip("\"'")
            out[m.group(1)] = v
    return out


def luhn(digits):
    s, alt = 0, False
    for d in reversed(digits):
        n = int(d)
        if alt:
            n *= 2
            n -= 9 if n > 9 else 0
        s += n
        alt = not alt
    return s % 10 == 0


def is_placeholder(v):
    return v.startswith("{") or v.startswith("[")


def notes(root):
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        parts = rel.parts
        if any(x in SKIP_DIRS or x.startswith(".") for x in parts[:-1]):
            continue
        name = parts[-1]
        if name.lower() in SKIP_FILES or name.endswith("-TEMPLATE.md") or name.lower() == "context.md":
            continue
        yield p, rel


def main(argv):
    exec_brain = "--exec" in argv
    today = date.today()
    if "--today" in argv:
        i = argv.index("--today")
        try:
            today = date.fromisoformat(argv[i + 1])
        except (IndexError, ValueError):
            print("--today needs YYYY-MM-DD")
            return 2
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0] if args else ".").resolve()
    if not (root / "_System" / "BRAIN-RULES.md").exists():
        print(f"not a brain: {root / '_System' / 'BRAIN-RULES.md'} does not exist")
        return 2

    errors, warns = [], []
    checked = 0
    for p, rel in notes(root):
        text = p.read_text(encoding="utf-8", errors="replace")
        front, body = split(text)
        f = fields(front)
        r = str(rel)
        checked += 1
        lines = text.count("\n") + 1
        size = len(text.encode("utf-8"))

        if not front:
            errors.append(f"{r}: no frontmatter")
        else:
            for k in REQUIRED:
                if not f.get(k):
                    errors.append(f"{r}: missing or blank {k}")
            for k, allowed in ALLOWED.items():
                v = f.get(k, "")
                if v and not is_placeholder(v) and v not in allowed:
                    errors.append(f"{r}: {k}: '{v}' is not an allowed value")
            if f.get("owner", "").strip().lower() in ("ai", "claude", "chatgpt", "assistant"):
                errors.append(f"{r}: owner must be a human name, not '{f['owner']}'")
            rb = f.get("review_by", "")
            if rb and not is_placeholder(rb):
                try:
                    d = date.fromisoformat(rb[:10])
                    if d < today:
                        warns.append(f"{r}: review_by {rb[:10]} has passed (check it, then set freshness_state if two periods over)")
                except ValueError:
                    errors.append(f"{r}: review_by '{rb}' is not YYYY-MM-DD")
            if not exec_brain and f.get("sensitivity") == "exec":
                errors.append(f"{r}: sensitivity: exec in a team brain (move to the restricted brain)")

        if r == "_CONTEXT.md" and lines > 100:
            errors.append(f"{r}: {lines} lines, limit 100")
        if size > 500_000 or lines > 5000:
            errors.append(f"{r}: {size // 1000} KB / {lines} lines, split or roll now")
        elif size > 100_000 or lines > 1000:
            warns.append(f"{r}: {size // 1000} KB / {lines} lines, flag for split")

        if "—" in text or "–" in text:
            warns.append(f"{r}: em or en dash (use plain punctuation)")

        for label, rx in CREDENTIALS:
            for m in rx.finditer(text):
                if label == "card number" and not luhn(re.sub(r"\D", "", m.group(0))):
                    continue
                if label == "card number" and not (13 <= len(re.sub(r"\D", "", m.group(0))) <= 19):
                    continue
                errors.append(f"{r}: possible {label} (rotate if real, remove, clean git history)")
                break

        if not exec_brain and rel.parts[0] != "_System":
            for m in LINK_RE.finditer(body):
                tgt = m.group(1)
                if re.search(r"(^|/)(exec|exec-brain)(/|$)", tgt):
                    warns.append(f"{r}: link into an exec path ({tgt})")
            hits = sorted({w.lower() for w in EXEC_WORD_RE.findall(body)})
            if hits:
                warns.append(f"{r}: exec-word watch hit ({', '.join(hits)}): read it, then keep, reword or move")

    print(f"brain_check: {checked} notes in {root}")
    for w in warns:
        print("warn  ", w)
    for e in errors:
        print("ERROR ", e)
    print(f"{len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
