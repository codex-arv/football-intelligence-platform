# The 90ᵗʰ Minute 

*Intelligent Football Analytics & Insights for Premier League Matches*

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture & Workflow](#architecture--workflow)
4. [Tech Stack](#tech-stack)
5. [Datasets & Sources](#datasets--sources)
6. [Installation & Local Setup](#installation--local-setup)
7. [Docker & Containerized Deployment](#docker--containerized-deployment)
8. [CI/CD Pipelines](#cicd-pipelines)
9. [Frontend & Backend Integration](#frontend--backend-integration)
10. [API Endpoints](#api-endpoints)
11. [Future Enhancements](#future-enhancements)
12. [Credits & Acknowledgements](#credits--acknowledgements)
13. [Repository](#repository)

---

## Project Overview

**The 90th Minute** is a full-stack **Machine Learning platform** for Premier League match predictions and player performance analytics. It combines historical match data, player statistics, and fixture insights to deliver **accurate match outcome predictions**, **scoreline forecasts**, and **real-time player analytics**.

The platform demonstrates the complete ML lifecycle: data collection, preprocessing, model training, evaluation, online API inference, Docker-based containerized deployment, and automated CI/CD pipelines. Production-ready deployment is available on **Render** (backend) and **Vercel** (frontend), with scalable architecture.

---

## Features

* Predict match outcomes and scorelines using historical and live data
* Real-time player performance insights (FPL & match data)
* RESTful API for frontend integration or third-party applications
* Modular ML pipeline to extend to new leagues or datasets
* CI/CD-enabled Docker deployment for reproducibility
* Blended predictions: **XGBoost Classifier** for match outcomes and **Random Forest Regressor** for goals
* Dynamic weighting using team ELO and match context

---

## Architecture & Workflow

**Offline Training Pipeline:**

* Preprocess historical match and player data
* Feature engineering: differences, EWMA, venue modifiers, ELO adjustments
* Train ML models:

  * **XGBoost Classifier** for match outcome prediction
  * **Random Forest Regressor** for home/away goals
* Store trained models and artifacts for inference

**Online Prediction Pipeline:**

* FastAPI backend serves real-time predictions
* Loads models and datasets on startup
* Computes dynamic features for requested matches (EWMA, ELO, venue adjustments, SoS ratios)
* Blends classification and regression predictions with dynamic weighting
* Returns JSON with probabilities, predicted scoreline, winner, confidence levels, and blending weights
* Implements lazy loading to optimize cold-start performance on free-tier Render deployments

**Frontend Interaction:**

* React + Tailwind CSS dashboard
* Calls backend API for predictions, statistics, and club information
* Displays live probabilities and historical insights

---

## Tech Stack

* **Backend:** Python, FastAPI, Pandas, NumPy, Scikit-learn, XGBoost, Random Forest
* **Frontend:** React, HTML, Tailwind CSS
* **Data & ML:** Joblib, Numpy, Pandas, Scikit-learn
* **DevOps:** Docker, Render, Vercel, GitHub Actions (CI/CD)

---

## Datasets & Sources

* [**Football-Data**](https://www.football-data.co.uk) — Multi-decade historical match results and fixture statistics
* [**FPL Core Insights (GitHub)**](https://github.com/olbauday/FPL-Core-Insights) — Player metrics and match insights, including FPL API data

---

## Installation & Local Setup

```bash
git clone https://github.com/codex-arv/football-intelligence-platform.git
cd football-intelligence-platform
pip install -r requirements.txt
uvicorn api.main:app --reload --port 5005
```

**Local API docs:** [http://localhost:5005/docs](http://localhost:5005/docs)

**Note:** For production deployment, use the backend URL from Render.

---

## Docker & Containerized Deployment

Project is fully containerized with separate backend and frontend containers.

```bash
# Build backend container
docker build -t football-api .

# Run container
docker run -p 8000:8000 football-api
```

Containers include all dependencies, ML artifacts, and preprocessing logic.

---

## CI/CD Pipelines

* GitHub Actions triggers automatic builds and deployments on push
* Backend deployed to Render automatically
* Frontend deployed to Vercel automatically
* Ensures production-ready models and feature pipelines stay in sync with code

---

## Frontend & Backend Integration

**Frontend routes:**

* `/prediction` — Match Predictions
* `/knowclubs` — Club Information
* `/statistics` — Matches List & Stats
* `/workflow` — Prediction Pipeline Workflow
* `/contact` — Contact Form

**Backend responsibilities:**

* Dynamic feature calculation per match
* Classification + regression blending with ELO-based weights
* Error handling and CORS policies

---

## API Endpoints

* `GET /health` — Backend health check
* `GET /api/v1/teams` — List of all teams
* `POST /api/v1/predict` — Accepts `home_team` and `away_team`; returns winner, probabilities, scoreline, confidence, blending weights
* `GET /api/v1/stats/health` — Dataset readiness info
* `GET /api/v1/stats/matches` — Match list by season & gameweek
* `GET /api/v1/stats/match/basic` — Basic match statistics
* `GET /api/v1/stats/players` — Player statistics for a match
* `GET /api/v1/club?club=<club_name>` — Full club JSON

---

## Future Enhancements

* Integrate live bookmaker odds for more accurate predictions
* Graphical dashboards for team & player performance trends
* Expand to other leagues beyond Premier League
* Automated model retraining on new data
* Integrate RAG/LLM for club information retrieval

---

## Credits & Acknowledgements

* **Datasets:** Football-Data, FPL Core Insights (GitHub)
* **Project Inspiration:** End-to-end football analytics and predictive modeling
* **Frontend & DevOps:** React, Tailwind CSS, Docker, Render, Vercel

---

## Repository

GitHub: [https://github.com/codex-arv/football-intelligence-platform](https://github.com/codex-arv/football-intelligence-platform)

---

## Deployed Project Website

GitHub: [https://the90thminute.vercel.app](https://the90thminute.vercel.app)
