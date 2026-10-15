# 🛒 Rappi AI Purchasing Agent

An autonomous purchasing validation engine built for the **Rappi India Engineering Evaluation**. The system ingests automated purchase recommendations, evaluates them against physical warehouse capacity, financial budget constraints, and supplier Minimum Order Quantities (MOQ), and autonomously determines whether to **ACCEPT**, **MODIFY**, or **REJECT** the purchase order with full audit logs.

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Business Logic & Guardrail Matrix](#-business-logic--guardrail-matrix)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Quick Start Guide](#-quick-start-guide)
- [Running Evaluation Tests](#-running-evaluation-tests)

---

## ✨ Key Features
- **Deterministic Guardrails**: Multi-layered constraint checks ensuring order quantities respect warehouse storage capacity, available budget, and supplier thresholds.
- **Autonomous Order Modification**: Automatically clamps requested quantities down to maximum available warehouse limits rather than outright rejection when capacity is constrained.
- **RESTful API**: Fast and lightweight API built using FastAPI with full CORS support.
- **Enterprise Dark-Mode Dashboard**: Interactive React frontend built with Vite, offering live investigation metrics, status badges, and execution audit logs.
- **Automated Test Harness**: Integrated unit test suite to validate decision rules against edge-case inventory scenarios.

---

## 🏗️ System Architecture

```
+--------------------------+          +---------------------------+
|  React Dashboard (Vite)  | -------> |  FastAPI Backend Engine   |
|  http://localhost:5173   |  POST    |   http://127.0.0.1:8000   |
+--------------------------+          +---------------------------+
                                                    |
                                                    v
                                      +---------------------------+
                                      | Dynamic Guardrail Engine  |
                                      |     (app/validator.py)    |
                                      +---------------------------+
                                                    |
                                    +---------------+---------------+
                                    |               |               |
                                    v               v               v
                             [Capacity Check]  [Budget Check]  [MOQ Check]
                                    |               |               |
                                    +---------------+---------------+
                                                    |
                                                    v
                                      +---------------------------+
                                      |  Action: Create PO Log    |
                                      +---------------------------+
```

---

## 📊 Business Logic & Guardrail Matrix

| Constraint Scenario | Input Quantity | Evaluation Rules | Decision Status | Executed Action |
| :--- | :--- | :--- | :--- | :--- |
| **Exceeds Storage Space** | `800 units` | Available Space = `350 units` | `MODIFIED` | PO generated automatically for `350 units`. |
| **Below Supplier MOQ** | `50 units` | Supplier MOQ = `100 units` | `REJECTED` | Order cancelled; rejection reason logged. |
| **Valid Order Within Limits** | `200 units` | Fits within storage & budget | `ACCEPTED` | PO generated for requested `200 units`. |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic
- **Frontend**: React 18, Vite, JavaScript (ES6+), CSS3 (Modern Dark Theme)
- **Testing**: Python `unittest` framework

---

## 📁 Repository Structure

```text
rappi-ai-agent/
├── backend/
│   ├── app/
│   │   ├── database.py       # Mock database state (Inventory, Suppliers, Budget)
│   │   ├── validator.py      # Core business rule validation engine
│   │   └── main.py           # FastAPI endpoints & CORS middleware configuration
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Interactive dashboard component
│   │   ├── App.css           # High-contrast enterprise styling
│   │   └── main.jsx          # React app entry point
│   ├── index.html            # Web entry point
│   └── package.json          # Frontend dependencies
├── .gitignore                # Git exclusion rules
├── evaluation_test.py        # Automated testing evaluation suite
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js (v18+) & npm

### 1. Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate virtual environment (Windows):
   ```bash
   venv\Scripts\activate
   ```

3. Install requirements (if needed) and run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   > The API server will run at `http://127.0.0.1:8000`

---

### 2. Frontend Setup (React + Vite)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```
   > Open `http://localhost:5173` in your browser to access the dashboard.

---

## 🧪 Running Evaluation Tests

To run the automated test suite verifying all business constraints and edge cases:

1. Open a terminal in the root directory (`rappi-ai-agent`).
2. Run:
   ```bash
   python evaluation_test.py
   ```

**Expected Output:**
```text
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```