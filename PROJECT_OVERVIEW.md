# 📊 Agentic Fleet System - Complete Project Overview

## Project Summary

This is an **Agentic Fleet Predictive Maintenance & Risk Intelligence System** - an enterprise-grade prototype for managing vehicle fleets with AI-driven diagnostics, risk assessment, and maintenance recommendations. Now upgraded with **Gen-AI capabilities** including LLM-powered chatbot, RAG-based contextual responses, and AI-generated explanations.

---

## 🏗️ High-Level Architecture

```
CSV Data → MongoDB → ML Model → Agent Chain → APIs → React Dashboard
                                      ↓
                    Hybrid Intelligence Layer (ML + LLM Co-Reasoning + RAG)
```

The system follows a data pipeline:
1. **Data Ingestion**: CSV telemetry files are loaded into MongoDB
2. **ML Predictions**: Pre-trained scikit-learn model scores failure risk
3. **Agent Orchestration**: Master agent coordinates specialized agents for analysis
4. **Hybrid Intelligence**: ML predictions + LLM reasoning + RAG context for intelligent decisions
5. **API Layer**: FastAPI exposes data via RESTful endpoints with RBAC
6. **Frontend**: React/Vite dashboard visualizes fleet health and agent actions

**Intelligence Roles:**
- **ML**: Statistical prediction and pattern recognition
- **LLM**: Natural language reasoning, explanation generation, and decision synthesis
- **RAG**: Contextual knowledge retrieval from vehicle data history

**Design Tradeoff:**
- ML used for deterministic, low-latency predictions
- LLM used for reasoning, explanation, and decision synthesis
- Hybrid approach balances performance, cost, and interpretability

---

## 📁 Folder Structure

### Root Level
- `README.md` - Main documentation
- `EXECUTIVE_SUMMARY.md` - Feature completion status
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `QUICKSTART.md` - Quick start guide
- `data/ey_agent_dataset.csv` - Demo telemetry dataset
- `START.sh / START.bat` - Script to launch both backend and frontend

### `backend/` - FastAPI Application

```
backend/
├── main.py                 # FastAPI app initialization & bootstrap
├── dependencies.py         # Dependency injection (auth, DB, agents)
├── requirements.txt        # Python dependencies
│
├── agents/                 # 7 Specialized Agent Classes
│   ├── master_agent.py    # Orchestrates the agent chain
│   ├── prediction_agent.py # ML model inference
│   ├── diagnostics_agent.py # Analyzes telemetry anomalies
│   ├── risk_agent.py      # Scores overall risk
│   ├── scheduling_agent.py # Schedules maintenance
│   ├── recommendation_agent.py # Generates recommendations
│   ├── feedback_agent.py  # Captures operator feedback
│   └── rule_agent.py      # Applies rule-based logic
│
├── api/                   # API Route Handlers (9 modules)
│   ├── telemetry_api.py   # Vehicle data ingestion
│   ├── prediction_api.py  # ML predictions endpoint
│   ├── risk_api.py        # Risk assessment endpoint
│   ├── fleet_api.py       # Fleet overview & analytics
│   ├── feedback_api.py    # Collect operator feedback
│   ├── alerts_api.py      # Alert management
│   ├── agent_timeline_api.py # Agent action audit trail
│   ├── recommendation_api.py # Maintenance recommendations
│   └── assistant_api.py   # AI bot responses
│
├── database/              # MongoDB Connection
│   └── mongo_client.py    # MongoConnection class
│
├── ml/                    # Machine Learning Pipeline
│   ├── model_loader.py    # Load pre-trained joblib model
│   ├── predictor.py       # Prediction inference logic
│   ├── feature_mapper.py  # Map CSV columns to model features
│   └── train_model.py     # Model training script (optional)
│
├── routes/                # Additional Route Handlers
│   └── bot.py            # Chatbot endpoint
│
├── utils/                 # Utility Functions
│   ├── agent_logger.py    # Log agent actions to timeline
│   ├── explainability.py  # Generate explanations (ML + LLM)
│   ├── csv_validator.py   # Validate CSV data
│   ├── time_utils.py      # Timestamp handling
│   ├── llm_client.py      # OpenAI API wrapper
│   ├── embedding.py       # Text embeddings for RAG
│   ├── vector_store.py    # FAISS vector database
│   └── rag_pipeline.py    # RAG context retrieval
│
├── config.py              # Environment configuration
├── .env.example           # Environment variables template
```

### `frontend/` - React/Vite Dashboard

```
frontend/
├── package.json           # Node dependencies
├── vite.config.js         # Vite build config
├── tailwind.config.js     # Tailwind CSS config
│
├── src/
│   ├── main.jsx          # App entry point
│   ├── App.jsx           # Route definitions
│   ├── index.css         # Global styles
│   │
│   ├── api/              # API Client Layer
│   │   ├── api.js        # Axios instance & general endpoints
│   │   └── bot.js        # Bot chat endpoint
│   │
│   ├── components/       # Reusable React Components
│   │   ├── Navbar.jsx    # Navigation (role-based filtering)
│   │   ├── BotWidget.jsx # Floating AI assistant
│   │   ├── Charts.jsx    # Recharts visualizations
│   │   ├── VehicleHealthBadge.jsx  # Health indicator with pulse
│   │   ├── PredictionExplanation.jsx # Model explanation panel
│   │   ├── MaintenanceRecommendations.jsx # Recommended actions
│   │   └── FloatingAssistant.jsx  # Chat panel UI
│   │
│   ├── context/          # React Context (Global State)
│   │   ├── AuthContext.jsx # User authentication state
│   │   └── UserContext.jsx # Current user & vehicle data
│   │
│   ├── layouts/          # Page Layout Templates
│   │   ├── AdminLayout.jsx # Admin-only pages wrapper
│   │   └── UserLayout.jsx  # User-only pages wrapper
│   │
│   └── pages/            # Full Page Components
│       ├── Login.jsx           # Mock login (role + vehicle ID)
│       ├── FleetDashboard.jsx  # Admin: Overall fleet KPIs
│       ├── VehicleAnalytics.jsx # User: Single vehicle deep dive
│       ├── RiskAnalytics.jsx   # Admin: Risk trends & events
│       ├── Alerts.jsx          # Admin: Alert management
│       ├── AgentTimeline.jsx   # Admin: Agent audit trail
│       └── BreakdownAssistance.jsx # User: Emergency assistance
```

### `models/` - ML Models
- Contains pre-trained `trained_model.pkl` (scikit-learn joblib format)
- 26-feature model for failure prediction
- Feature mapping handles missing values with median imputation

---

## 🎯 Core Functionality

### 1. Data Pipeline
- **CSV Ingestion**: Auto-loads `data/ey_agent_dataset.csv` on backend startup
- **MongoDB Collections**:
  - `vehicles` - Fleet metadata
  - `telemetry` - Raw sensor data (speed, RPM, temperature, etc.)
  - `predictions` - ML model outputs with probabilities & explanations
  - `risk_logs` - Risk scores & categorization
  - `maintenance_events` - Scheduled maintenance tasks
  - `agent_actions` - Audit trail of all agent decisions
  - `feedback` - Operator notes & status updates
  - `alerts` - System-generated alerts
  - `service_centers` - Demo emergency service locations

### 2. Agent Chain (MasterAgent Orchestration)

When telemetry arrives, `MasterAgent.process_telemetry()` executes:

1. **RuleAgent** → Applies rule-based logic (e.g., harsh acceleration alerts)
2. **PredictionAgent** → Runs ML model inference → Returns failure probability
3. **DiagnosticsAgent** → Analyzes anomalies in telemetry
4. **RiskAgent** → Combines prediction + diagnostics → Risk score (0-1)
5. **SchedulingAgent** → Plans maintenance based on risk
6. **LLM-powered Recommendation Agent** → Synthesizes ML predictions, telemetry, and historical data to generate context-aware maintenance strategies with reasoning and trade-off analysis
7. **FeedbackAgent** → Requests operator confirmation

Each agent logs its reasoning to `agent_actions` collection → used by Agent Timeline page.

**LLM Integration Strategy:**
- LLM integration applied selectively (e.g., Recommendation Agent) where reasoning adds value
- Deterministic agents retained for reliability and performance-critical tasks

### 3. ML Prediction Model
- **Model Type**: scikit-learn trained model (26 features)
- **Features**: Engine RPM, vehicle speed, oil pressure, coolant temp, battery voltage, brake pressure, acceleration, harsh cornering, tire pressure, fuel consumption, distance traveled, etc.
- **Output**: Failure probability (0-1) + predicted event type
- **Robustness**: Missing values filled with median; numeric columns auto-detected

### 4. Role-Based UI Simulation
- **Admin** → Full dashboard, fleet analytics, agent audit trail
- **User** → Only allowed to view their assigned vehicle's details and breakdown assistance
- Enforced via the mock `AuthContext` (stored in `localStorage`) — frontend automatically scopes views for `user` role
- Backend enforces RBAC on key endpoints (for example: bot chat, breakdown assistance, telemetry/risk/predict) to prevent users from accessing other vehicles

### 5. Gen-AI Assistant (LLM + RAG)
- **LLM Integration**: OpenAI GPT-4o-mini powered chatbot with natural language understanding
- **RAG Pipeline**: FAISS vector store with sentence-transformers embeddings for contextual responses
- **Embeddings updated periodically** from new telemetry and risk logs
- **Top-k retrieval (3–5)** optimized for low-latency responses
- **Context Sources**: Telemetry summaries, predictions, risk logs embedded and retrieved
- **Response Flow**: Query → Embedding → Similarity Search → Context → LLM Generation
- **RBAC Enforced**: Users can only query their assigned vehicle data

### 6. AI-Generated Explanations
- **Dual Explanations**: Traditional ML feature impact + LLM human-readable summaries
- **LLM Explanations**: Converts technical ML outputs into natural language explanations
- **Recommendation Agent**: Optional LLM-based generation of maintenance recommendations

### 7. AI Decision Engine
- **Hybrid Intelligence**: Combines ML predictions with LLM reasoning for data-driven decisions with contextual reasoning
- **Evaluates possible maintenance actions with reasoning**: Analyzes maintenance approaches and trade-offs
- **Justified Actions**: Generates actionable decisions with detailed reasoning
- **Example Decision**: "Immediate service recommended due to high RPM + oil pressure anomaly correlation, risk of failure within 48 hours - prioritize brake inspection over general maintenance"

### 8. Breakdown Assistance (EY Core Feature)
- **Trigger**: Activates when risk > 0.8 OR prediction probability > 0.85
- **Functionality**:
  - Auto-opens modal with nearby service centers
  - Uses Haversine formula for distance calculation
  - Shows nearest center + highest-rated center
  - Call & Navigate buttons
  - Demo centers seeded in MongoDB

### 9. Intelligent Diagnostics (Gen-AI Use Case)
Users can ask natural language questions like:
**"Why is vehicle 102 high risk?"**

**System Response:**
- Retrieves relevant telemetry patterns, ML predictions, and risk assessments from vector store
- Runs LLM reasoning engine to synthesize cause-effect relationships
- Generates human-like explanation: *"Vehicle 102 shows elevated risk due to correlated anomalies: high RPM (3,200) combined with low oil pressure (28 PSI) over the last 48 hours, plus ML model predicting 78% brake failure probability. This suggests potential seal degradation in the brake system."*

## 🖥️ Frontend Pages

| Page | User Role | Purpose |
|------|-----------|---------|
| **Login** | All | Role selection + vehicle ID entry |
| **Fleet Dashboard** | Admin | KPIs: total vehicles, high-risk count, avg failure probability, risk distribution chart |
| **Vehicle Analytics** | User | Single vehicle: telemetry snapshot, prediction trend, risk trend, re-run prediction |
| **Risk Analytics** | Admin | Harsh events summary, risk timeline, high-risk vehicle cards |
| **Alerts** | Admin | Alert management & severity filtering |
| **Agent Timeline** | Admin | Tabular audit of all agent decisions with reasons |
| **Breakdown Assistance** | User | Emergency service center recommendations |

---

## ⚡ API Endpoints

```
POST   /api/telemetry/ingest        - Upload CSV or JSON telemetry
GET    /api/telemetry/latest/{id}   - Latest sensor data for vehicle
POST   /api/predict                 - Run ML model on telemetry
GET    /api/predict/{vehicleId}     - Latest prediction for vehicle
GET    /api/risk/{vehicleId}        - Risk assessment
GET    /api/fleet/overview          - Fleet KPIs
GET    /api/fleet/top-risk          - Top risky vehicles
GET    /api/fleet/agent-actions     - Agent audit trail
POST   /api/feedback                - Submit operator feedback
POST   /api/bot/chat                - LLM-powered conversational AI with RAG context
GET    /api/assist/breakdown/{id}   - Service centers for breakdown
GET    /api/alerts                  - Get system alerts
```

---

## 🚀 Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 18, Vite, Tailwind CSS, Recharts, Framer Motion, Axios |
| **Backend** | FastAPI, Python 3.10+, Uvicorn |
| **Database** | MongoDB (local or cloud) |
| **ML** | scikit-learn, Joblib, Pandas |
| **Gen-AI** | OpenAI GPT-4o-mini, Sentence Transformers, FAISS Vector DB |
| **Auth** | Mock localStorage headers (not JWT, no real auth) |

---

## 🎓 Key Design Patterns

1. **Dependency Injection** - FastAPI `Depends()` for DB, agents, auth
2. **Agent Pattern** - Each agent handles specific responsibility (SRP)
3. **RAG Architecture** - Retrieval-Augmented Generation for contextual AI responses
4. **Vector Search** - FAISS-based similarity search for relevant context retrieval
5. **LLM Integration** - Clean API wrapper pattern for external AI services
6. **Audit Trail** - Every decision logged to `agent_actions`
7. **Frontend Role Filtering** - UI-level role simulation coupled with backend RBAC on key endpoints
8. **Explainability** - All predictions include reasoning (ML + LLM)
9. **Resilience** - Missing data handled with median imputation
10. **Modular AI** - Pluggable LLM providers and embedding models

---

## 🔧 Getting Started

**Prerequisites**: Python 3.10+, Node 18+, MongoDB running locally

```bash
# Configure environment
cd backend && cp .env.example .env
# Edit .env with your OpenAI API key

# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend && npm install
npm run dev
```

Access at `http://localhost:5173` (frontend proxies API to backend)

---

## ✨ Key Features

✅ **Multi-Agent System** - 7 specialized agents working in coordination  
✅ **ML-Powered Predictions** - Scikit-learn model with 26-feature inference  
✅ **Gen-AI Assistant** - LLM-powered chatbot with RAG contextual responses  
✅ **Vector Search RAG** - FAISS-based retrieval of relevant vehicle data  
✅ **AI Explanations** - Dual ML + LLM explainability for predictions  
✅ **LLM Recommendations** - Optional AI-generated maintenance suggestions  
✅ **Explainability** - Every prediction includes reasoning  
✅ **Role-Based UI** - Frontend role simulation with backend RBAC on key endpoints (users scoped to assigned vehicle)  
✅ **Real-Time Monitoring** - API-driven vehicle telemetry & risk scoring (near-real-time)  
✅ **Emergency Assistance** - Automatic breakdown detection & service center routing  
✅ **Audit Trail** - Complete agent action logging  
✅ **Responsive UI** - Mobile-friendly React/Tailwind dashboard  
✅ **Production-Ready** - Enterprise-grade error handling & patterns  

---

This is a **production-ready prototype** with complete feature implementation, RBAC, explainability, and **Gen-AI capabilities** including LLM chatbot and RAG! 🎉
