---
type: rules
id: rules-field-authority
title: Field authority (which source wins)
status: active
owner: "{AI owner}"
sensitivity: team
created: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
updated: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
last_reviewed: "{YYYY-MM-DDTHH:MM+ZZ:ZZ}"
review_by: "{YYYY-MM-DD}"
confidence: high
source_kind: document
source_uri: "owner interview {YYYY-MM-DD}"
source_date: "{YYYY-MM-DD}"
---

# Field authority

When two sources disagree about a field, this table says which one the brain believes. The loser is still recorded with its source, in the Supersession register or side by side under `freshness_state: conflicted`. An agent never resolves a conflict by preference: it applies this table or asks the owner. Extend the table with this business's own systems.

| Field | Wins | Over | Note |
|---|---|---|---|
| Any contract term | The signed agreement in `91-Evidence` | Anything a platform, email or person describes | A platform's description is marketing, not the contract |
| Any rule the organisation follows | The active policy note in `02-Policies` | A chat message, an email, a habit seen in history | "We always" is evidence for a draft policy, never the policy |
| Who decided what | The decision note with `approval_evidence` | Meeting summaries, recollections | The transcript beats the summary; the summary beats memory |
| Live numbers (sales, stock, balances) | The system of record at answer time | Any report, note or snapshot about it | The brain records the snapshot with its date, never as current |
| Order or ticket facts | The order or help desk system | An email or message about it | |
| Whether a meeting happened | The recording or transcript | The calendar invite | An invite proves scheduling, not attendance |
| Whether an action is done | `completion_evidence` on the action note | A mention that it was done, or no complaint | Silence never closes an action |
| What was approved | The exact approved text, approver and date | Any later paraphrase | A paraphrase never widens an approval |
| A person's role and ownership | The roles note as set by the owner | A signature, an email title | |
