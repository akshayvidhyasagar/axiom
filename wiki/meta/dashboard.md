---
type: meta
title: "AXIOM Dashboard"
updated: 2026-05-05
---

# AXIOM Wiki Dashboard

## Recent Activity
```dataview
TABLE type, status, updated FROM "wiki" SORT updated DESC LIMIT 15
```

## Seed Pages (Need Development)
```dataview
LIST FROM "wiki" WHERE status = "seed" SORT updated ASC
```

## Phase Status
```dataview
TABLE status FROM "wiki/modules" SORT file.name ASC
```

## Open Gaps
```dataview
LIST FROM "wiki/gaps" WHERE type = "concept" SORT updated ASC
```
