# 🚗 Agentic Fleet Predictive Maintenance System

## Overview

This project is a **fleet risk intelligence and predictive maintenance platform** that combines:

- telemetry ingestion
- machine learning-based failure prediction
- rule-based diagnostics
- modular processing (agent-style architecture)
- full-stack visualization
- **Gen-AI capabilities** including LLM-powered chatbot, RAG-based contextual responses, and AI-generated explanations

It is designed as a **production-style prototype** demonstrating backend architecture, ML integration, decision workflows, and hybrid intelligence for fleet operations.

---

## 🏗️ Architecture


CSV / API Input
↓
MongoDB (Telemetry Storage)
↓
ML Prediction Layer
↓
Processing Pipeline (Agent Modules)
↓
Hybrid Intelligence Layer (ML + LLM Co-Reasoning + RAG)
↓
FastAPI Backend (RBAC APIs)
↓
React Dashboard


---

## ⚙️ Core Components

### 1. Data Pipeline

- CSV telemetry ingestion
- MongoDB collections:
  - `vehicles`
  - `telemetry`
  - `predictions`
  - `risk_logs`
  - `maintenance_events`
  - `alerts`
  - `agent_actions`
  - `feedback`

---

### 2. Processing Pipeline (Agent Modules)

The system uses modular processing units coordinated by a central orchestrator.

#### Execution Flow


Telemetry Input
↓
Rule Evaluation
↓
ML Prediction
↓
Diagnostics
↓
Risk Scoring
↓
Maintenance Scheduling
↓
LLM-powered Recommendations
↓
Feedback Logging


#### Modules

- **RuleAgent** → detects rule-based anomalies  
- **PredictionAgent** → ML inference (failure probability)  
- **DiagnosticsAgent** → analyzes telemetry patterns  
- **RiskAgent** → computes overall risk score  
- **SchedulingAgent** → generates maintenance plans  
- **RecommendationAgent** → suggests actions (with LLM reasoning)  
- **FeedbackAgent** → captures operator input  

> Note: This is a **hybrid intelligence pipeline** combining deterministic agents with LLM-powered reasoning for context-aware decisions.

---

### 3. Machine Learning

- Model: scikit-learn (joblib)
- Input: 26 telemetry features
- Output:
  - failure probability (0–1)
  - predicted event type

#### Features include:
- engine RPM
- coolant temperature
- oil pressure
- battery voltage
- vehicle speed
- braking behavior
- tire pressure
- fuel consumption

#### Data Handling
- Missing values → median imputation
- Automatic numeric feature detection

---

### 4. Gen-AI Capabilities

- **LLM Integration**: OpenAI GPT-4o-mini for natural language reasoning and explanation generation
- **RAG Pipeline**: FAISS vector store with sentence-transformers for contextual knowledge retrieval
- **AI Assistant**: Conversational chatbot with vehicle-specific context
- **Explainability**: Dual explanations - ML feature impact + LLM human-readable summaries
- **Intelligent Recommendations**: LLM-powered maintenance suggestions with reasoning and trade-off analysis

#### Intelligence Roles
- **ML**: Statistical prediction and pattern recognition
- **LLM**: Natural language reasoning, explanation generation, and decision synthesis
- **RAG**: Contextual knowledge retrieval from vehicle data history

---

### 5. API Layer (FastAPI)

#### Key Endpoints


POST /api/telemetry/ingest
GET /api/telemetry/latest/{vehicleId}
POST /api/predict
GET /api/predict/{vehicleId}
GET /api/risk/{vehicleId}
GET /api/fleet/overview
GET /api/fleet/top-risk
GET /api/fleet/agent-actions
POST /api/feedback
POST /api/bot/chat
GET /api/assist/breakdown/{vehicleId}
GET /api/alerts


#### Features
- dependency injection (FastAPI)
- modular routing
- basic RBAC enforcement

---

### 6. Frontend (React + Vite)

#### Pages

- Fleet Dashboard (admin)
- Vehicle Analytics (user)
- Risk Analytics
- Alerts Management
- Agent Timeline (audit logs)
- Breakdown Assistance

#### Features

- role-based UI filtering
- charts (Recharts)
- explainability panels
- assistant widget

---

### 7. Breakdown Assistance

Triggered when:


risk > 0.8 OR failure_probability > 0.85


Provides:
- nearest service center (Haversine distance)
- highest-rated center
- contact + navigation options

---

### 8. Audit & Explainability

All system actions are logged:


agent_actions collection


Each record includes:
- agent name
- decision
- reasoning
- timestamp

---

## 🧱 Technology Stack

| Layer | Technology |
|------|------------|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, Python |
| Database | MongoDB |
| ML | scikit-learn, Pandas |
| Gen-AI | OpenAI GPT-4o-mini, Sentence Transformers, FAISS Vector DB |
| Visualization | Recharts |
| Auth | Mock RBAC (localStorage + API checks) |

---

## 📁 Project Structure


backend/
agents/
api/
database/
ml/
utils/
scripts/

frontend/
src/
components/
pages/
context/
api/

models/
data/


---

## 🚀 Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB running locally
- OpenAI API key (for Gen-AI features)

---

### Backend

```bash
cd backend
cp .env.example .env  # Configure OpenAI API key
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access

http://localhost:5173
## 🧠 Design Principles

- modular architecture (SRP)
- separation of ML and API layers
- hybrid intelligence (ML + LLM + RAG)
- auditability of decisions
- explainable outputs
- scalable backend structure

## ⚠️ Current Limitations

- deterministic pipeline with selective LLM integration (no fully autonomous planning)
- no feedback loop / iterative reasoning
- no event-driven architecture
- no real-time streaming (Kafka, MQTT)
- basic RBAC (no JWT / OAuth)

## 🔮 Future Improvements

- planner + tool-based agent architecture
- event-driven ingestion (Kafka / Redis streams)
- real-time telemetry processing
- feedback loop for post-maintenance evaluation
- stronger authentication (JWT / OAuth)
- model retraining pipeline
- expanded LLM integration across all agents

## 🎯 Purpose

This project demonstrates:

- backend system design
- ML integration in production-style pipelines
- modular processing architecture
- hybrid intelligence (ML + LLM + RAG)
- full-stack engineering capability
- Gen-AI integration in enterprise applications

## 📌 Summary

A well-structured predictive maintenance system with:

- strong backend foundations
- integrated ML pipeline
- hybrid intelligence (ML + LLM + RAG)
- clear observability
- practical fleet use case

It provides a solid base for evolving into a fully autonomous agent system with advanced Gen-AI capabilities.
