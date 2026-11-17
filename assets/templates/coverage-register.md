---
type: rules
id: rules-coverage-register
title: Coverage register (which sources feed this brain)
status: active
owner: "{AI owner}"
sensitivity: team
created: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
updated: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
last_reviewed: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
review_by: "{YYYY-MM-DD}"
confidence: high
source_kind: session
source_uri: "discovery {YYYY-MM-DD}"
source_date: "{YYYY-MM-DD}"
---

# Coverage register

A brain that looks complete but is missing a source is worse than one that says what it cannot see. List every source in use, connected or not. A gap is a visible gap, never proof nothing happened. A row marked not connected, excluded or unverified is never reported as current. A source past its allowed lag makes dependent facts stale. A busy source that returns nothing is a possible broken connection, listed in the nightly summary, not a quiet day. The nightly review updates "last read" and "date reached". For private sources, the full cursor lives in the restricted brain's register; this one carries only the date reached.

| Source | Kind | Owner | Connected | Cadence | Last read | Date reached | Allowed lag | Notes |
|---|---|---|---|---|---|---|---|---|
