# 💊 MediStock AI: Autonomous Pharmacy Inventory Orchestrator

MediStock AI is a state-of-the-art, multi-agent system designed to automate pharmacy inventory management. It leverages a coordinator-led architecture to handle everything from risk detection and reorder planning to automated supplier procurement and performance auditing.

## 🚀 Key Features

- **Autonomous Orchestration**: A central Coordinator Agent dynamically manages a suite of specialized agents (Intelligence, Reorder, Action, Selection).
- **Predictive Optimization**: Real-time stockout forecasting and adaptive safety buffer tuning based on historical performance.
- **Closed-Loop Procurement**: Automated Purchase Order generation and email dispatch to optimized suppliers.
- **Self-Improving System**: An evaluation layer that scores AI decisions and "learns" to minimize overstock and prevent stockouts.
- **FastAPI Backend**: A robust REST API layer for enterprise integration.

## 🏗️ Architecture

MediStock AI follows a **Phase-Based Agentic Workflow**:

1.  **Analysis Phase**: Intelligence agents identify risks (Expiry, Low Stock, Dead Stock).
2.  **Decision Phase**: Execution agents calculate reorder quantities and select the best supplier based on urgency vs. cost.
3.  **Execution Phase**: Action agents generate local POs and dispatch them via secure email.
4.  **Evaluation Phase**: A performance agent audits past outcomes to tune future decision logic.

## 🛠️ Tech Stack

- **Core**: Python 3.10+, Streamlit (UI), FastAPI (API)
- **Intelligence**: Groq (Llama 3.1) for explainable AI insights.
- **Database**: SQLite (audit logs, inventory, performance history).
- **Deployment**: Docker, Docker Compose, Cloud-ready entrypoints.

## 🏁 Quick Start

### 1. Prerequisites
- Python 3.10+
- A Groq API Key ([Get one here](https://console.groq.com/))

### 2. Installation
```bash
git clone https://github.com/your-repo/medistock-ai.git
cd medistock-ai
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

### 4. Run the Demo
Load realistic pharmacy data and launch the dashboard:
```bash
python scripts/load_demo_data.py
streamlit run app.py
```

## 🐳 Docker Deployment

Run the entire stack (UI + API) with a single command:
```bash
docker-compose up --build
```

## 📈 Monitoring & Learning
The system includes an **AI Accuracy** tracker in the dashboard sidebar. This metric reflects the system's ability to accurately predict usage and adjust safety margins autonomously.

---
*Built for Pharmacy Managers who want to focus on patients, not spreadsheets.*
