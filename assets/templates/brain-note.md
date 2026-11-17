---
type: {type from BRAIN-RULES}
id: {type-slug, lowercase, from the entity registry}
title: {Plain title}
status: draft
owner: {A human name}
sensitivity: team
created: {YYYY-MM-DDTHH:MM+ZZ:ZZ}
updated: {YYYY-MM-DDTHH:MM+ZZ:ZZ}
last_reviewed: {YYYY-MM-DDTHH:MM+ZZ:ZZ}
review_by: {YYYY-MM-DD}
confidence: medium
source_kind: {api | email | slack | whatsapp | call | document | session | person | mixed | generated}
source_uri: {evidence path, meeting note, or "owner interview YYYY-MM-DD"}
source_date: {YYYY-MM-DD}
freshness_state: current
supersedes: []
superseded_by: []
relates_to: []
aliases: []
---

# {Title}

{Current state (YYYY-MM-DD): two or three sentences, rewritten when the state moves.}

## {One topic}

Fact: {a claim.} (Source: {path or person}, {YYYY-MM-DD})

## Timeline

| Date | Event | Source |
|---|---|---|
| {YYYY-MM-DD} | {what happened} | {path} |

## Supersession register

| Date | Old claim | Current truth | Kind | Effective from | Source | Changed by |
|---|---|---|---|---|---|---|

## See also

- {link to related notes, one line each}
