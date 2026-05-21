# UML Diagrams — Marketing Campaign & Asset Management CRM

All diagrams are written in [Mermaid](https://mermaid.js.org/) syntax. They render
natively on GitHub, GitLab, VS Code, and most Markdown viewers. They can also be
exported to PNG/SVG (via `mmdc`, the Mermaid CLI) for inclusion in the LaTeX
report.

---

## 1. Use-Case Diagram

Captures the main actors of the platform and the business actions they can
perform. The DeepSeek **Marketing Assistant** chatbot is treated as a first-class
use case because it is a key differentiator of the project.

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart LR
    subgraph Actors
        MM([Marketing Manager])
        AN([Data Analyst])
        AD([Administrator])
    end

    subgraph "Marketing CRM"
        UC1((Manage Product Pipeline))
        UC2((Manage Campaigns))
        UC3((Manage Angles & Hooks))
        UC4((Upload & Tag Creatives))
        UC5((Log Expenses & Revenues))
        UC6((View ROI Dashboard))
        UC7((Chat with Marketing Assistant))
        UC8((Predict Product Potential))
        UC9((Manage Users & Permissions))
        UC10((Switch UI Language EN / FR / AR))
    end

    MM --> UC1
    MM --> UC2
    MM --> UC3
    MM --> UC4
    MM --> UC5
    MM --> UC7
    MM --> UC8
    MM --> UC10

    AN --> UC6
    AN --> UC7
    AN --> UC8
    AN --> UC10

    AD --> UC9
    AD --> UC10
```

---

## 2. Class Diagram (Domain Model)

Describes the persistent data model behind the CRM. Each class becomes a Django
model in the corresponding app (`pipeline`, `assets`, `finance`, `chatbot`,
`prediction`).

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +string role
    }

    class Product {
        +int id
        +string name
        +string description
        +Status status  %% Planning | Active | Evaluated
        +float score
        +text notes
        +datetime created_at
    }

    class Campaign {
        +int id
        +string name
        +date start_date
        +date end_date
        +decimal budget
        +Status status
        +calculate_roi() float
    }

    class Angle {
        +int id
        +string name
        +Category category   %% Problem-Solution | Benefit | Offer
        +float success_rate
    }

    class Creative {
        +int id
        +string title
        +file file
        +MediaType type      %% Image | Video
        +bool is_winner
    }

    class Hook {
        +int id
        +text text
        +Platform platform   %% Social | Search | Display
        +Trigger trigger_type %% Curiosity | Pain | Demo
        +float performance_score
    }

    class Expense {
        +int id
        +decimal amount
        +Category category   %% Ads | Production | Tools
        +date date
    }

    class Revenue {
        +int id
        +decimal amount
        +date date
        +string source
    }

    class ChatSession {
        +int id
        +datetime started_at
    }

    class ChatMessage {
        +int id
        +Role role           %% user | assistant | system
        +text content
        +datetime created_at
    }

    class PredictionLog {
        +int id
        +json input_features
        +string predicted_class %% Low | Medium | High
        +float confidence
        +datetime created_at
    }

    User "1" --> "*" Product : owns
    User "1" --> "*" ChatSession : starts
    Product "1" --> "*" Campaign : has
    Campaign "1" --> "*" Creative : contains
    Campaign "1" --> "*" Expense : incurs
    Campaign "1" --> "*" Revenue : generates
    Angle "1" --> "*" Creative : inspires
    Angle "1" --> "*" Hook : drives
    ChatSession "1" --> "*" ChatMessage : contains
    User "1" --> "*" PredictionLog : runs
```

---

## 3. Sequence Diagram — DeepSeek Chatbot Flow

This diagram traces the full lifecycle of a single user message through the
chatbot plugin. It demonstrates how the Django backend enriches the prompt with
**live CRM context** (top campaigns, recent ROI, best angle) before forwarding
it to the DeepSeek API.

```mermaid
sequenceDiagram
    autonumber
    actor U as User (Marketer)
    participant UI as Browser (Alpine.js widget)
    participant V as Django View<br/>/chat/
    participant CTX as CRM Context Builder
    participant DB as PostgreSQL
    participant DS as DeepSeek API
    participant H as ChatMessage History

    U->>UI: Types question<br/>"Which angle performs best?"
    UI->>V: POST /chat/ {message, session_id}
    V->>H: Save user message
    V->>CTX: build_context(user)
    CTX->>DB: SELECT top campaigns, ROI, angles
    DB-->>CTX: aggregated stats
    CTX-->>V: system_prompt + facts
    V->>DS: POST /v1/chat/completions<br/>{model: deepseek-chat, messages}
    DS-->>V: streamed completion
    V->>H: Save assistant message
    V-->>UI: text/event-stream chunks
    UI-->>U: Renders reply progressively
```

---

## 4. Sequence Diagram — Product Potential Prediction

Shows how the ML bonus feature is invoked (either directly via a form, or
indirectly by the chatbot when asked "Should I launch this product?").

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant UI as Browser
    participant V as Django View<br/>/predict/
    participant S as prediction.services
    participant M as RandomForest model.pkl
    participant DB as PostgreSQL

    U->>UI: Submit product features
    UI->>V: POST /predict/
    V->>S: predict_potential(features)
    S->>M: model.predict_proba(X)
    M-->>S: [P(Low), P(Med), P(High)]
    S-->>V: (class, confidence)
    V->>DB: INSERT PredictionLog
    V-->>UI: render result page
    UI-->>U: "High potential — confidence 0.87"
```

---

## 5. Deployment / Component Diagram

Production-style topology. For the academic demo we run everything on
`localhost`, but the report describes the target deployment.

```mermaid
flowchart LR
    subgraph Client
        B[Browser<br/>HTMX + Alpine.js + Tailwind]
    end

    subgraph "Application Server"
        N[Nginx<br/>reverse proxy + static]
        G[Gunicorn]
        D[Django 5.x<br/>crm_project]
        ML[(model.pkl<br/>RandomForest)]
    end

    subgraph "Data Layer"
        PG[(PostgreSQL)]
        FS[(Media files<br/>Creatives)]
    end

    subgraph "External Services"
        DS[DeepSeek API<br/>api.deepseek.com]
    end

    B <--> N
    N <--> G
    G <--> D
    D <--> PG
    D <--> FS
    D <--> ML
    D <--> DS
```

---

## 6. Activity Diagram — Campaign Lifecycle

Shows the Kanban-style flow of a product through the pipeline, used to motivate
the `Status` enum on the `Product` model.

```mermaid
stateDiagram-v2
    [*] --> Planning
    Planning --> Active : campaign launched
    Active --> Evaluated : test ended
    Evaluated --> Active : re-test with new angle
    Evaluated --> [*] : discontinued
```
