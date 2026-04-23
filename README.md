# 💊 MediStock AI – Agentic Inventory Optimization for Pharmacies

## 📌 Overview

MediStock AI is an intelligent inventory management system designed for pharmacies to optimize stock levels, reduce expiry losses, and improve decision-making.

The system uses an **agentic approach** to analyze inventory data and generate actionable recommendations such as reorder alerts, expiry risk detection, and identification of slow-moving items.

---

## 🎯 Problem Statement

Pharmacies face challenges in managing inventory due to:

* Expiry-sensitive medicines leading to financial losses
* Stockouts of critical drugs affecting patient care
* Overstocking and slow-moving inventory
* Lack of intelligent, proactive decision support

---

## 🚀 Solution

MediStock AI processes inventory data and uses rule-based agents to:

* Detect low stock and suggest reorders
* Identify near-expiry medicines
* Flag dead stock (no sales for long duration)
* Generate human-readable explanations for decisions

---

## 🧠 Key Features

* 📉 Reorder Recommendation
* ⏳ Expiry Risk Detection
* 🐢 Dead Stock Identification
* 🧾 AI-based Decision Explanation
* 📊 Simple Dashboard (Streamlit)

---

## 🏗️ System Architecture

1. Data Ingestion (CSV / SQLite)
2. Data Processing (Derived metrics)
3. Agentic Decision Engine
4. Explanation Layer
5. Dashboard Output

---

## 📊 Dataset Structure

| Column          | Description       |
| --------------- | ----------------- |
| Item_ID         | Unique ID         |
| Item_Name       | Medicine name     |
| Stock_Quantity  | Current stock     |
| Min_Stock_Level | Reorder threshold |
| Expiry_Date     | Expiry date       |
| Last_Sold_Date  | Last sale date    |
| Monthly_Usage   | Average usage     |
| Cost_Per_Unit   | Cost price        |

---

## ⚙️ Tech Stack

* Python
* Pandas
* Streamlit
* Rule-based Agent System
* (Optional) LLM for explanations

---

## ▶️ How to Run

### 1. Clone Repository

```bash
git clone https://github.com/your-username/medistock-ai.git
cd medistock-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
streamlit run app.py
```

---

## 📈 KPI Metrics

* Inventory Holding Cost Reduction
* Expiry Loss Reduction
* Stockout Reduction
* Dead Stock Percentage
* Decision Efficiency

---

## 📊 Sample Output

* “Paracetamol: Stock below minimum → Reorder required”
* “Cough Syrup: Near expiry → Risk of loss”
* “Vitamin D: No sales → Dead stock”

---

## 🔮 Future Enhancements

* Machine Learning-based demand forecasting
* Automated email/alert system
* Supplier optimization
* Multi-industry support

---

## 👨‍💻 Author

Anand Yelloju

---

## ⚠️ Disclaimer

This project is for educational and demonstration purposes. It simulates inventory decisions based on sample data and rule-based logic.
