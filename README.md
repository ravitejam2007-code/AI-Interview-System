# AI Interview Preparation System

An end-to-end AI-powered platform designed to help job seekers master their interview skills. The system parses resumes (PDF format), extracts technical skills, calculates ATS compatibility scores, generates personalized mock interview questions, and tracks communication analytics.

---

## 📂 Repository Structure

```txt
AI-Interview-System/
│
├── backend/                # Flask REST API & service-oriented logic
│   ├── app.py              # Main Flask application entry point
│   ├── config.py           # Application environment configuration loader
│   ├── requirements.txt    # Backend Python dependencies
│   ├── .env.example        # Reference environment variables
│   │
│   ├── src/
│   │   ├── routes/         # API routes partitioned under v1
│   │   │   └── v1/         # Version 1 blueprints (auth, resume, interview, ats)
│   │   │
│   │   ├── models/         # User, Resume, and Interview logical schemas
│   │   ├── services/       # Core domain services (resume parser, ats checker, question generator)
│   │   ├── utils/          # Static utility helpers (pdf reader, text cleaner)
│   │   └── database/       # Database managers and session initializers
│   │
│   ├── uploads/            # Temporary directory for candidate uploads (ignored)
│   └── tests/              # Pytest backend test suite
│
├── frontend/               # React (Vite SPA) client interface
│   ├── index.html          # SPA entry shell
│   ├── package.json        # Frontend Node dependencies & build scripts
│   ├── vite.config.js      # Vite dev-server config with local reverse proxy & @ src alias
│   ├── .env.example        # Reference frontend environment parameters
│   │
│   └── src/
│       ├── main.jsx        # SPA DOM renderer
│       ├── App.jsx         # App router layout
│       ├── components/     # Reusable standalone elements (Navbar, etc.)
│       ├── pages/          # Full-view components (Home, Upload, Interview, Feedback)
│       └── services/       # API clients (unified Axios wrapper mapped to versioned routes)
│
├── ml_models/              # Stores serialized binary weights and model dumps (git-ignored)
│   └── README.md
│
├── datasets/               # CSV datasets for model training & evaluation
│   └── README.md
│
├── docs/                   # Visual system architectures & screenshots
│   └── README_assets.md
│
├── tests/                  # Unified E2E test suites
│   └── backend/            # Pytest test suite for service endpoints
│
├── package.json            # Workspace orchestrator for one-command execution
└── .gitignore              # Repository file filters
```

---

## ✨ Features

- **Advanced Resume Parsing**: Extracts plain text, skills, education history, and employment context using robust pattern recognition.
- **ATS Optimizer**: Matches keywords, checks missing skills, evaluates formatting thresholds, and computes an overall compatibility score.
- **Interactive Mock Interview**: Conducts an interactive tech interview using speech-to-text transcription and browser text-to-speech feedback.
- **Service-Oriented Design**: Clean division of roles between backend modules (services, utilities, database layer) and React client pages.
- **V1 API Versioning**: Blueprints versioned under `/api/v1/...` for easy scalability and backwards compatibility.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- **Node.js (v20+)**
- **Python (v3.11+)**

### 2. Quick-Start (Unified Development)
Initialize all workspaces and boot up both the Flask backend and React frontend simultaneously with a single terminal command:
```bash
# Install root and frontend packages
npm install

# Start both servers in concurrent mode
npm run dev
```

### 3. Manual Startup

#### Flask Backend Setup
```bash
cd backend
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Start backend server (runs on port 5000)
flask run
```

#### React Frontend Setup
```bash
cd frontend
# Install packages
npm install

# Boot dev server (runs on port 5173 with proxy mapped to port 5000)
npm run dev
```

---

## 🔌 API Documentation

| Method | Path | Description |
|---|---|---|
| **POST** | `/api/v1/resume/upload` | Upload PDF resume to parse skills, education, and experience. |
| **POST** | `/api/v1/interview/generate-questions` | Generate 5 personalized technical questions based on resume context. |
| **POST** | `/api/v1/interview/emotion` | Mock telemetry for tracking user's facial expression metadata. |
| **POST** | `/api/v1/ats/ats-score` | Compute detailed keyword alignment and missing skills checklist. |
| **GET** | `/api/v1/ats/results` | Fetch complete mock interview result metrics and insights. |
