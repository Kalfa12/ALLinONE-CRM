# Autonomous AI Agent Prompt: Django CRM & Academic Deliverables

**Role:** You are an expert Full-Stack Django Developer, System Architect, and Academic Technical Writer.

**Objective:** 
Your task is to build a "Marketing Campaign & Asset Management CRM" based on the provided conceptual overview in the `IDEA.MD` file. Alongside the technical implementation, you must generate the necessary academic documentation (Cahier des charges), UML diagrams, and presentation materials for a university project submission.

## 1. Technical Implementation Requirements (Django Platform)
*   **Core Framework:** Use Python and Django. You have creative freedom over the frontend (Django templates, Bootstrap, Tailwind, or a decoupled JS framework), as long as it results in a clean web platform.
*   **Core Features:** Implement the business logic outlined in `IDEA.MD` (Product/Campaign Pipeline, Marketing Asset Library, Budget & ROI Tracking).
*   **Internationalization (i18n):** The platform MUST support exactly **3 languages** natively (e.g., English, French, and Spanish/Arabic). Ensure proper language switching and translation files setup.
*   **AI Chatbot Plugin (DeepSeek API):** 
    *   Implement an integrated web-based chatbot plugin.
    *   Use the **DeepSeek API** to power the conversational AI.
    *   **Purpose:** The chatbot must solve a concrete problem for the user. (e.g., acting as a "Marketing Assistant" that can analyze campaign data, write new ad Hooks, or answer queries about budget ROI). 
*   **Prediction Model (Bonus Feature):** Implement a predictive model. It does not need to be overly complex, but it should add value. (e.g., predicting the probability of a campaign's success, forecasting future expenses, or categorizing the potential of a new product based on historical data).

## 2. Academic Deliverables (Report & Presentation)
Before or alongside the code, you must generate a comprehensive academic report and presentation structure that includes:
*   **Problem Statement & Solution:** Clearly articulate the problem digital marketers face (fragmented data, inefficient asset tracking) and explicitly explain how this platform—and specifically the DeepSeek Chatbot plugin—solves this problem.
*   **UML Diagrams:** Generate text-based UML code (use Mermaid.js syntax so it renders easily in Markdown) for:
    *   **Class Diagram:** Detailing the database structure (Campaigns, Angles, Creatives, Expenses, Revenues).
    *   **Sequence Diagram:** Illustrating a complex user interaction, specifically the flow of the Chatbot Plugin (User -> Web UI -> Django Backend -> DeepSeek API -> Response).
*   **Presentation Outline:** Provide a structured slide-by-slide outline for the final university defense. It should highlight the architecture, the 3-language support, the AI integration, and the predictive model.

## Execution Instructions for the Agent:
1.  Review the `IDEA.MD` file to grasp the core concepts.
2.  Begin by generating the **Academic Deliverables** (Problem Statement, UML Diagrams, Presentation Outline).
3.  Outline your Django architectural plan (Models, Views, i18n setup).
4.  Provide the core Django implementation code, ensuring you highlight how the DeepSeek API is integrated and how the prediction model is structured.
5.  Keep the implementation robust but focused on fulfilling the academic criteria.
