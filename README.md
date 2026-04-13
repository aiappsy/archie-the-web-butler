# Archie – The Web Butler 🧐🎩

**Archie** is an **AI Content Reconstruction System (AICRS)** designed to transform chaotic, legacy website data into structured, modern, and CMS-ready digital assets. Built for agencies who dread the manual grunt work of migrating legacy sites, Archie automates the "unsexy" parts of digital reconstruction.

---

## 🚀 Key Features

### 1. The Autonomous Audit Engine
- **Deep-Crawl Ingestion**: Uses Playwright to map legacy site structures, handling broken HTML and JavaScript-heavy legacy frameworks.
- **Pain Quantification**: Identifies 404s, duplicate headers, and thin content to help agencies justify migration costs to their clients.
- **Investor-Grade Reports**: Generates high-contrast PDF audit reports that highlight legacy technical debt vs. modern potential.

### 2. Semantic De-structuring (The Moat)
- **AI Component Mapping**: Leverages Cloud LLMs (Gemini 1.5 Pro) to analyze legacy HTML and reconstruct it into "Clean Component Skeletons" (Heros, Features, Testimonials).
- **Narrative Synthesis**: Extracts core brand values while filtering out decades of SEO fluff and outdated boilerplate.

### 3. The Canva Marketing Suite
- **Media Bridge**: Automatically optimizes legacy images to WebP and pushes them directly to Canva via the Connect Assets API.
- **Design Autofill**: Programmatically populates Canva Brand Templates with reconstructed site content for instant marketing collateral generation.

### 4. Last-Mile Export
- **Webflow CMS Connector**: One-click export of AI components directly into Webflow CMS Collections.
- **Human-in-the-Loop**: A premium workspace for agencies to Review, Edit, or Reject AI-synthesized sections before they go live.

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Next.js 15 (App Router), Tailwind CSS, Glassmorphism UI |
| **Backend** | Python (FastAPI), Playwright (Crawl Service) |
| **Intelligence** | Gemini 1.5 Pro (via Google Generative AI API) |
| **Database** | Firebase Firestore (Real-time NoSQL) |
| **Integrations** | Canva Connect API, Webflow Data API v2 |

---

## 📦 Project Structure

```text
archie-web-butler/
├── frontend/             # Next.js Dashboard UI
│   ├── src/app/          # Premium Dashboard & Workspace views
│   └── globals.css       # Custom Design System
├── backend/              # FastAPI Intelligence Engine
│   ├── crawler.py        # Asynchronous crawler logic
│   ├── parser.py         # AI Semantic mapping + Firestore
│   ├── canva_bridge.py   # Canva Connect API integration
│   ├── report_generator.py # PDF reporting engine
│   └── main.py           # API Coordination layer
└── docs/                 # Strategic specifications & white paper
```

---

## 🚦 Getting Started

### Backend Setup
1. From the **project root**, create and activate a virtual environment:
   ```bash
   python -m venv backend/venv
   # macOS / Linux
   source backend/venv/bin/activate
   # Windows
   backend\venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```
4. Copy the sample env file and fill in your credentials:
   ```bash
   cp backend/.env.example backend/.env
   ```
   | Variable | Description |
   | :--- | :--- |
   | `GOOGLE_API_KEY` | Gemini API key from Google AI Studio |
   | `GOOGLE_APPLICATION_CREDENTIALS` | Path to Firebase service-account JSON (or use GCP ADC) |
   | `CANVA_ACCESS_TOKEN` | Canva Connect API access token |
   | `WEBFLOW_API_TOKEN` | Webflow Data API v2 token |
   | `ALLOWED_ORIGINS` | Comma-separated frontend origins for CORS (default: `http://localhost:3000`) |

5. Start the engine from the **project root**:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dashboard:
   ```bash
   npm run dev
   ```

---

## 📜 Final Verdict
Archie isn't just a website builder; it’s an **Agency OS for Content Sovereignty**. By parsing latent value from the chaotic web, Archie transforms static folders of HTML into high-ticket, CMS-ready digital assets.

---
*Created by Advanced Agentic Coding Assistants for the Aiappsy Ecosystem.*
