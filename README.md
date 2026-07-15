# Data-Driven Soccer Recruitment System
### Identifying Undervalued Talent Through Machine Learning

**Author:** Md Rafiul Islam Rafi
**Course:** CISC 6080 Capstone Project in Data Science (Fordham University)
**Instructor:** Dr. Gary Weiss

---

## Overview

This project builds a data-driven soccer recruitment system that uses machine learning to
identify **undervalued players** whose on-field performance suggests they are worth
more than their current market value.

The system performs three main tasks:

1. **Player Market Value Prediction** — predict a player's market value from performance stats,
   age, position, league, and playing time (supervised regression).
2. **Undervalued Talent Identification** — compare each player's predicted value to their actual
   market value and rank the biggest positive gaps as potential bargains.
3. **Player Similarity Analysis** — group statistically similar players (K-Means + PCA) to find
   cheaper alternatives to a target or departing player.

---

## Data

The dataset combines two public sources for the 2025-26 season (top-5 European leagues):

| Source | Role | Provides |
|--------|------|----------|
| **FBref** (via Kaggle) | Features | Player performance stats: goals, assists, shots, minutes, tackles, interceptions, goalkeeping, etc. |
| **Transfermarkt** (via Kaggle) | Target + context | Market values, transfers, position, club, contract, height |

**Final dataset:** `soccer_recruitment_dataset.csv` — 2,839 players (2,514 with a market value), 71 columns.

The two sources were joined on a normalized player name + birth year (they share no common ID),
achieving an 88.6% match rate.

> **Note:** Following FBref's loss of its Opta data licence (January 2026), advanced metrics such
> as xG and progressive passing are unavailable for the current season; the project uses the
> available standard performance metrics.

---

## Repository Structure

```
.
├── README.md                          # this file
├── soccer_recruitment_dataset.csv     # final cleaned, analysis-ready dataset
├── data/                              # raw source files (git-ignored if large)
├── scripts/                           # data preparation code
│   ├── join_data.py                   # merges FBref stats with Transfermarkt values
│   ├── clean_data.py                  # removes redundant columns
│   └── rename_cols.py                 # renames columns to readable labels
└── docs/                              # proposal, report, and figures
```

---

## Methods & Tools

- **Language:** Python (pandas, scikit-learn, XGBoost, SHAP)
- **Models:** Linear Regression (baseline), Random Forest, XGBoost
- **Clustering:** K-Means with PCA
- **Explainability:** SHAP feature importance
- **Visualization:** Tableau dashboards
- **Storage:** PostgreSQL (planned)

## Project Pipeline

Data Sources → Collection & Integration → Cleaning & Feature Engineering → PostgreSQL Database → Exploratory Data Analysis → Machine Learning → Player Similarity Analysis → Model Explainability → Undervalued Talent Identification → Tableau Dashboards → Recommendation System

## Status

- [x] Proposal paper
- [x] Data collection (FBref + Transfermarkt)
- [x] Data integration / join
- [x] Data cleaning & formatting
- [x] Exploratory Data Analysis
- [ ] PostgreSQL Database
- [ ] Machine Learning (predict value)
- [ ] Undervalued talent identification
- [ ] Player Similarity Analysis
- [ ] Model Explainability (SHAP)
- [ ] Tableau Dashboards
- [ ] Final paper
