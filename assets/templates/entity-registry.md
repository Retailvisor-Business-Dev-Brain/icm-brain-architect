---
type: rules
id: rules-entity-registry
title: Entity registry (one id, one spelling, one home per thing)
status: active
owner: "{AI owner}"
sensitivity: team
created: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
updated: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
last_reviewed: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
review_by: "{YYYY-MM-DD}"
confidence: high
source_kind: generated
source_uri: "owner interview and backfill"
source_date: "{YYYY-MM-DD}"
---

# Entity registry

Every person, product, supplier, customer segment, tool and channel the brain mentions has one row. The id is permanent and lowercase. The canonical path is the one home note. Aliases are every other spelling seen in sources; writes are corrected to the canonical spelling and aliases are kept so search still works. External ids (SKU, CRM id, account number) let an agent match a live record to the right note. An id you do not know is `unknown` with an owner to find it. Two entities with the same name get a disambiguation line.

| Id | Kind | Canonical name | Canonical path | Aliases | External ids | Disambiguation |
|---|---|---|---|---|---|---|
