# 🛒 Rappi AI Purchasing Agent

An autonomous purchasing validation engine built with **FastAPI** and **React (Vite)** to validate restocking recommendations against warehouse capacity limits, supplier Minimum Order Quantities (MOQ), and available budget guardrails.

---

## 🌟 Key Features

- **Autonomous Decision Engine**: Evaluates inventory recommendations against live operational constraints (`ACCEPTED`, `MODIFIED`, `REJECTED`).
- **Dynamic Capacity & MOQ Validation**: Automatically adjusts batch sizes when orders exceed remaining storage or caps.
- **Audit Logging**: Generates transparent, human-readable execution reasons alongside automated Purchase Orders (PO).
- **Interactive Dashboard**: Modern dark-mode React UI with live status badges, metric breakdown cards, and JSON response viewer.
- **Automated Test Suite**: Complete unit test coverage for validation rules and edge cases.

---

## 🏗️ Architecture & Core Components
rappi-ai-agent/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI Application & REST Endpoints
│   │   ├── validator.py       # Core Business Logic & Rule Engine
│   │   └── database.py        # In-Memory Database & PO Management
│   └── requirements.txt       # Backend Dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main Dashboard Component
│   │   └── App.css            # Dark Theme Enterprise Styling
│   └── package.json           # Frontend Dependencies
├── evaluation_test.py         # Automated Test Suite
└── README.md                  # Documentation
---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**

---

### Step 1: Backend Setup (FastAPI)

1. Navigate to the `backend` directory:
   ```bash
   cd backend
2. Activate virtual environment: 
   ```bash
   venv\Scripts\activate
3.venv\Scripts\activate
  ```bash
    pip install -r requirements.txt

  
