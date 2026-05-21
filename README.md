# Marketing Campaign & Asset Management CRM

A Django web platform that consolidates the digital-marketing workflow:
product pipeline, marketing-asset library (angles, creatives, hooks),
budget & ROI tracking, an **AI Marketing Assistant** powered by the
**DeepSeek API**, and a **Random-Forest** model that predicts a new
product's potential.

The interface is fully translated into **English, French, Arabic** (Arabic
is rendered RTL).

## Stack

- Python 3.11+, Django 5
- Tailwind CSS (via CDN), HTMX, Alpine.js — no JS bundler needed
- SQLite (dev) / PostgreSQL (prod)
- scikit-learn for the predictor, joblib for serialization
- DeepSeek `deepseek-chat` for the assistant

## Quickstart

```bash
# 1. Create env + install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# then edit .env and set DEEPSEEK_API_KEY (optional — chatbot returns
# a friendly placeholder if absent)

# 3. Train the ML model (also generates synthetic seed data)
python ml/train.py

# 4. Migrate + create a superuser
python manage.py migrate
python manage.py createsuperuser

# 5. Compile translations (requires gettext installed locally)
python manage.py compilemessages

# 6. Run
python manage.py runserver
```

Open <http://localhost:8000>, log in, and use the language selector in
the top-right to switch between EN / FR / AR.

## Project layout

```
crm_project/         Django project (settings, urls, wsgi)
apps/
  core/              shared context processors
  pipeline/          Product + Campaign + Kanban
  assets/            Angle, Creative, Hook
  finance/           Expense, Revenue, ROI dashboard
  chatbot/           DeepSeek integration + chat widget backend
  prediction/        Form + inference for the ML categorizer
templates/           HTML templates (base.html is RTL-aware)
locale/{en,fr,ar}/   Translation catalogues
ml/                  train.py, seed_data.csv, model.pkl
docs/
  diagrams.md        Mermaid UML (use-case, class, sequence, deploy)
  presentation.md    Defense slide outline
  report/            LaTeX cahier des charges (compiles with pdflatex)
```


## DeepSeek chatbot — design note

The view at `POST /chat/` does **not** simply forward the user's message
to DeepSeek. It first calls
[`apps/chatbot/context.py::build_crm_context`](apps/chatbot/context.py)
to compute a compact factual snapshot of the user's CRM (top campaigns,
ROI, best angles, totals) and injects it into the **system prompt**. This
makes the assistant answer with grounded facts rather than hallucinated
generalities — that is the concrete user-problem the plugin solves.

## ML model — design note

[`ml/train.py`](ml/train.py) generates a synthetic but signal-bearing
dataset (latent score with noise → 3-class label), trains a
`RandomForestClassifier`, and dumps `(model, columns)` to
`ml/model.pkl`. Inference in
[`apps/prediction/services.py`](apps/prediction/services.py) caches the
load with `lru_cache` so the model is read from disk once per process.
Every prediction is logged to the `PredictionLog` table for future
re-training.

## Internationalization

All user-facing strings are wrapped with `gettext_lazy` (Python) or
`{% trans %}` (templates). To add or update translations:

```bash
python manage.py makemessages -l fr -l ar
# edit locale/{fr,ar}/LC_MESSAGES/django.po
python manage.py compilemessages
```

The base template flips `dir="rtl"` automatically when
`LANGUAGE_BIDI` is true (Arabic).
