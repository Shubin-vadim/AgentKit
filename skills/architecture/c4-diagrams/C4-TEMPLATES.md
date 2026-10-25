# C4 Mermaid scaffolds

Copy the structure; replace names from `CONTEXT.md`.

## C1 — System context

```mermaid
flowchart TB
    user["👤 User<br/>role<br/>what they do"]

    system["🎯 SystemName<br/>one-line job"]

    ext["☁️ External system<br/>why we call it"]
    ops["📊 Observability<br/>errors, traces, cost"]

    user -- "HTTPS" --> system
    system -- "HTTPS" --> ext
    system -. "errors, traces" .-> ops
```

*Audience:* stakeholder — who uses the system and what it talks to externally.

Omit in-process libraries. Dash observability if the product continues when it is down.

## C2 — Containers

```mermaid
flowchart TB
    user["👤 User (browser)"]

    subgraph host["VPS · Docker Compose"]
        edge["🔀 Edge<br/>TLS, reverse-proxy"]
        spa["🖥️ Frontend · SPA"]
        api["⚙️ Backend · API"]
        worker["🔧 Worker"]
        db[("🗄️ Database")]
        queue[("⚡ Queue")]
        files[("📁 File store")]
    end

    ext["☁️ External API"]

    user -- "HTTPS" --> edge
    edge --> api
    api -- "serves SPA" --> spa
    api -- "SQL" --> db
    api -- "enqueue" --> queue
    queue --> worker
    worker --> ext
    worker --> db
```

*Audience:* developer/DevOps — what deploys, where data and the queue live.

## C3 — Components (one container)

Show the **hard boundary** the ADR locked (e.g. pure library vs web).

```mermaid
flowchart TB
    spa["🖥️ SPA"]

    subgraph app["web layer (HTTP + DB)"]
        routers["API routers"]
        services["Application services"]
        orm["ORM"]
    end

    subgraph worker["bridging layer"]
        task["job entry"]
    end

    subgraph core["pure library"]
        orch["orchestrator"]
        adapters["outbound adapters"]
    end

    db[("Database")]

    spa --> routers
    routers --> services
    services --> orm
    services -- "enqueue" --> task
    task --> orch
    orch --> adapters
    orm --> db
    task -- "persist results" --> orm
```

*Audience:* developer — how one container is decomposed and where the seam sits.

## Level 4 — ERD (not code)

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : "places"
    ORDER ||--o{ ORDER_LINE : "contains"

    CUSTOMER {
        uuid id PK
        string email UK
    }
    ORDER {
        uuid id PK
        uuid customer_id FK
        string status
    }
```

*Audience:* developer — persistence models are written from this schema.

## Sequence — key user path

Happy path only. Error branches belong in the API contract, not this figure.

```mermaid
sequenceDiagram
    actor U as User
    participant API as API
    participant Q as Worker
    participant S as DB + files

    U->>API: submit work
    API->>S: persist queued
    API-->>U: 202
    API->>Q: enqueue
    Q->>S: persist done
    U->>API: fetch result
```
