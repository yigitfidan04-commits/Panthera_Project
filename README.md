# 🏎️ Cupra Panthera VZ+ | Autonomous Engineering Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![Pandas](https://img.shields.io/badge/Data-Pandas-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

> An end-to-end digital engineering, financial, and physics simulator evaluating the mass-production feasibility of a high-performance EV coupe built on the VW MEB Evo architecture.

## 🎯 Executive Summary
Designed with an Industrial Engineering framework, this project bridges the gap between raw automotive physics and strict financial reality. The simulation validates a 340 HP (250 kW) AWD Sports Coupe against rigorous homologation standards (WLTP Range, Thermal Soaking, Aerodynamics) while strictly maintaining a competitive **€60k-€64k market target** and a 19-22% profit margin.

## 📊 Validated Engineering Specs
Through autonomous simulation, the Panthera VZ+ achieved the following production-ready metrics:
* **Battery & Range:** 79 kWh Net Capacity | **633 km WLTP Range** (using low-rolling-resistance EV tires).
* **Performance:** Dual-Motor AWD | 340 HP | **0-100 km/h in 4.18s**.
* **Aerodynamics:** Optimized Low-Slung Coupe Form | $C_d \le 0.24$.
* **Thermal Endurance:** Survived Alpine mountain pass simulations with **€0 additional hardware cost**, utilizing a Predictive BMS and GPS-triggered Pre-Conditioning.

---

## ⚙️ The Orchestrator (`main.py`)
This repository operates as an autonomous factory. Running the central orchestrator triggers a sequential, fail-safe pipeline of 7 distinct engineering departments:

1. **ETL & Data Architecture (`fabrika_kurulum.py`):** Extracts raw Excel constraints and BOMs, transforming them into a relational SQL Database (`Panthera_Factory.db`).
2. **Cost Engineering (`cost_engine.py`):** Audits per-part costs, tracking the upgrade premiums from the Base VZ to the High-Performance VZ+.
3. **Financial Engine (`finance_engine.py`):** Simulates dynamic MSRP targets ensuring targeted corporate margins.
4. **Dynamics Engine (`dynamics_engine.py`):** Calculates real-world kinetic acceleration strictly bounded by MEB Evo platform constraints.
5. **Aerodynamic Judge (`constraints_engine.py`):** Otonomously audits CAD physical parameters to minimize wind drag power loss at high speeds.
6. **Smart Thermal Engine (`thermal_engine.py`):** Simulates multi-phase real-world driving (Autobahn, City, Alpine Pass) to validate heat extraction and prevent Thermal Throttling.
7. **Range & Efficiency (`range_engine.py`):** Applies dynamic payload penalties to calculate true street-legal energy consumption (kWh/100km).

---

## 🚀 Installation & Usage

To run the Panthera Factory simulation on your local machine:

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/Panthera_Project.git](https://github.com/YOUR_USERNAME/Panthera_Project.git)
cd Panthera_Project

Install required dependencies:
pip install pandas
python main.py

📦 Panthera_Project
 ┣ 📜 main.py                  # Master Orchestrator (Run this)
 ┣ 📜 fabrika_kurulum.py       # ETL Engine
 ┣ 📜 cost_engine.py           # BOM & Cost Auditor
 ┣ 📜 finance_engine.py        # Profit Margin Simulator
 ┣ 📜 dynamics_engine.py       # Physics & Acceleration
 ┣ 📜 constraints_engine.py    # Aerodynamic Validator
 ┣ 📜 thermal_engine.py        # Predictive BMS Logic
 ┣ 📜 range_engine.py          # WLTP Range Calculator
 ┣ 📊 Master Spec.xlsx         # Raw Engineering Parameters
 ┗ 🗃️ Panthera_Factory.db      # Compiled SQLite Database
 Built and engineered by İbrahim Yiğit Fidan - Industrial Engineering, Middle East Technical University (METU).
