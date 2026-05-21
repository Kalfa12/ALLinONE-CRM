# Presentation Outline — University Defense

**Project:** Marketing Campaign & Asset Management CRM
**Stack:** Django 5 · Tailwind · HTMX · DeepSeek API · scikit-learn
**Languages:** English · Français · العربية (RTL)

The defense is built around a 15-slide deck. Each slide below is annotated with
the **goal**, the **key message** to convey, and **what to show on screen**.

---

## Slide 1 — Title
- **Goal:** establish identity.
- **Show:** project title, student name, supervisor, university, academic year, the three flag emojis 🇬🇧 🇫🇷 🇸🇦 to hint at the i18n angle.
- **Say:** one-sentence pitch — *"A unified CRM that replaces marketing spreadsheets with a multilingual, AI-assisted command center."*

## Slide 2 — Problem Statement
- **Goal:** convince the jury the problem is real.
- **Key pain points:**
  1. Fragmented data — campaigns in Trello, expenses in Excel, creatives on Drive.
  2. Manual ROI computation — slow, error-prone.
  3. No reuse of marketing knowledge — winning angles & hooks get lost.
  4. No decision support — junior teams launch products blindly.
- **Show:** a "spaghetti diagram" of disconnected tools.

## Slide 3 — Proposed Solution
- **Goal:** position the CRM as the single source of truth.
- **Show:** one-slide architecture summary (Pipeline · Assets · Finance · AI · Prediction).
- **Stress:** the **DeepSeek chatbot** is what makes this CRM *active* rather than passive — it answers business questions on top of live data.

## Slide 4 — Functional Scope (from `IDEA.MD`)
- Product & Campaign Pipeline (Kanban: Planning → Active → Evaluated).
- Marketing Asset Library (Angles, Creatives, Hooks).
- Budget & ROI Tracking.
- AI Marketing Assistant (DeepSeek).
- Product Potential Categorizer (ML).

## Slide 5 — Architecture
- **Show:** the *Deployment / Component diagram* from `docs/diagrams.md` §5.
- **Highlight:** Django backend, PostgreSQL, model.pkl loaded once, DeepSeek as the only external dependency, static-served Tailwind.

## Slide 6 — Domain Model (Class Diagram)
- **Show:** the Mermaid class diagram from §2 of `docs/diagrams.md` (exported PNG).
- **Walk through:** Product 1—* Campaign 1—* (Creative, Expense, Revenue); Angle reused across Creatives and Hooks.

## Slide 7 — Internationalization (i18n)
- **Goal:** prove the 3-language requirement is real, not cosmetic.
- **Show:** three side-by-side screenshots of the dashboard in EN / FR / AR.
- **Emphasize:** Arabic is rendered **RTL** via `dir="rtl"` driven by Django's `LANGUAGE_BIDI`. All strings live in `locale/{en,fr,ar}/LC_MESSAGES/django.po`.

## Slide 8 — DeepSeek Chatbot — Sequence Flow
- **Show:** the sequence diagram from §3 of `docs/diagrams.md`.
- **Key insight:** the backend **enriches the prompt with live CRM facts** (top campaigns, ROI, best angles) so answers are grounded in the user's own data, not generic LLM trivia.

## Slide 9 — DeepSeek Integration — Code Highlight
- **Show:** ~15 lines of `apps/chatbot/services.py::ask_deepseek()`.
- **Talk about:** model `deepseek-chat`, streaming, system-prompt injection, message history persistence in `ChatMessage`.

## Slide 10 — Predictive Model
- **Goal:** demonstrate the ML bonus.
- **Show:** training pipeline (`ml/train.py`) → `RandomForestClassifier` → `model.pkl`.
- **Demo:** submit a new product on `/predict/` → returns `High potential — 0.87 confidence`.
- **Mention:** confusion matrix and feature-importance plot live in the report.

## Slide 11 — Live Demo (3 minutes)
1. Switch language to French → all labels update.
2. Switch to Arabic → layout flips RTL.
3. Drag a product card from *Planning* to *Active* on the Kanban board.
4. Log an expense and a revenue → ROI dashboard updates.
5. Open the chatbot widget → ask *"Quelle est l'angle le plus performant ce mois-ci ?"* → DeepSeek answers in French using live data.
6. Hit `/predict/` → categorize a new product.

## Slide 12 — Tech Stack & Quality
- Django 5 · Tailwind 3 · HTMX · Alpine.js · scikit-learn · pandas · joblib.
- Tests: model unit tests, ROI calculation tests, chatbot service mock test.
- Coverage report screenshot.

## Slide 13 — Challenges & Lessons Learned
- RTL CSS quirks with Tailwind's `space-x-*` utilities → solved with logical properties.
- Streaming responses from DeepSeek through Django without WebSockets → used `StreamingHttpResponse` + Server-Sent Events.
- Building a small but realistic synthetic dataset for the categorizer.

## Slide 14 — Future Work
- Real-time collaboration (Django Channels).
- OAuth (Google / Meta) for direct ad-platform sync.
- Replace synthetic ML data with real campaign history; retrain periodically.
- Mobile-first redesign.

## Slide 15 — Conclusion & Q&A
- Recap: a focused, multilingual, AI-augmented CRM that solves a concrete marketing-ops problem.
- Invite questions.

---

## Speaker Tips

- **Always demo in all three languages.** Switching languages mid-demo is the single most memorable moment for the jury.
- **Open the chatbot in front of the jury.** A live LLM response in French/Arabic on the marketer's own data is the "wow" moment.
- **Show the class diagram on a separate monitor** while answering data-model questions — saves time.
- **Have `pdflatex docs/report/main.tex` already compiled** so the PDF cahier des charges can be opened on demand.
- Keep a **fallback recording** of the demo in case the network blocks the DeepSeek API call from the lecture room.
