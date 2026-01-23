# The 90ᵗʰ Minute

*Real-Time Football Intelligence and Analytics Platform for Premier League*

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
13. [Repository & Live Demo](#repository--live-demo)

---

## Project Overview

**The 90ᵗʰ Minute** is an end-to-end Machine Learning and Full-Stack platform for Premier League match prediction, match analysis and player performance analytics.

The system combines historical match data, player-level statistics and contextual team strength metrics to generate:

- Match outcome probabilities
- Predicted scorelines
- Player performance insights for individual fixtures

This project demonstrates the **complete ML lifecycle in production** — from data consolidation and feature engineering to model training, API inference, containerized deployment and CI/CD automation.

---

## Features

- Blended ML predictions using **XGBoost (classification)** and **Random Forest (regression)**
- Dynamic feature engineering using **ELO ratings**, venue modifiers and rolling player statistics
- RESTful **FastAPI** backend for real-time inference
- **React + Tailwind CSS** dashboard for interactive visualization
- Modular data pipeline extendable to other leagues and datasets
- Dockerized backend for reproducible deployments
- Automated CI/CD pipelines for seamless production updates

---

## Architecture & Workflow

### Offline Training Pipeline

1. Consolidation of multi-season match, team and player datasets
2. Relational data merging and cleaning
3. Position-specific player feature engineering using rolling match windows
4. Contextual match feature creation (ELO differences, venue strength, possession, defensive metrics)
5. Model training:
   - **XGBoost Classifier** → Match outcome prediction
   - **Random Forest Regressor** → Home and away goal prediction
6. Model artifacts stored for online inference

---

### Online Prediction Pipeline

- FastAPI backend serves real-time predictions
- Loads trained models and processed datasets on startup
- Computes dynamic features per requested match (EWMA, ELO, venue adjustments, strength of schedule and many more)
- Blends classification and regression predictions with dynamic weighting
- Returns structured JSON with probabilities, predicted scoreline, winner, confidence and blending weights
- Lazy loading minimizes cold-start latency on Render free tier deployments

---

### Frontend Interaction

- React dashboard communicates with backend APIs
- Displays match predictions, club information and match statistics
- Visualizes probabilities and historical insights

---

## Tech Stack

**Backend**

- Python, FastAPI
- Pandas, NumPy
- Scikit-learn, XGBoost, Random Forest
- Joblib

**Frontend**

- React
- Tailwind CSS

**DevOps**

- Docker
- GitHub Actions (CI/CD)
- Render (backend hosting)
- Vercel (frontend hosting)

---

## Datasets & Sources

- [Football-Data](https://www.football-data.co.uk/): Historical match results and fixture statistics
- [FPL Core Insights (GitHub)](https://github.com/olbauday/FPL-Core-Insights): Player metrics and match insights derived from FPL and event data

---

## Installation & Local Setup

```bash
git clone https://github.com/codex-arv/real-time-premier-league-intelligence-platform.git
cd real-time-premier-league-intelligence-platform
pip install -r requirements.txt
uvicorn api.main:app --port 5005 --reload
```

**Local API Docs:**  
http://localhost:5005/docs

> For production usage, use the deployed Render backend URL.

---

## Docker & Containerized Deployment

The backend is fully containerized to guarantee reproducibility of the ML environment, dependencies and data artifacts.

```bash
# Build backend container
docker build -t football-api .

# Run container
docker run -p 8000:8000 football-api
```

The container bundles:
 * Trained model artifacts
 * Feature engineering pipelines
 * Historical datasets
 * All runtime dependencies

---

## CI/CD Pipelines

- GitHub Actions triggers on every push to the main branch
- Backend is automatically built and deployed to Render
- Frontend is automatically built and deployed to Vercel
- Ensures model artifacts, feature pipelines and API remain synchronized with code

---

## Frontend & Backend Integration

**Frontend Routes**

- `/prediction` — Match Predictions
- `/knowclubs` — Club Information
- `/statistics` — Match List and Player Statistics
- `/workflow` — Prediction Pipeline Workflow
- `/contact` — Contact Form

**Backend Responsibilities**

- Dynamic feature computation per fixture
- Classification and regression blending with ELO-based weights
- Dataset health checks and statistics endpoints
- CORS handling and robust error management

---

## API Endpoints

| Method | Endpoint | Description |
|-------|----------|-------------|
| GET | `/health` | Backend health check |
| GET | `/api/v1/teams` | List of teams |
| POST | `/api/v1/predict` | Match prediction |
| GET | `/api/v1/stats/health` | Dataset readiness information |
| GET | `/api/v1/stats/matches` | Match list by season and gameweek |
| GET | `/api/v1/stats/match/basic` | Basic match statistics |
| GET | `/api/v1/stats/players` | Player statistics for a match |
| GET | `/api/v1/club?club=<name>` | Club information JSON |

---

## Future Enhancements

- Integration of live bookmaker odds
- Visual dashboards for team and player performance trends
- Expansion to additional football leagues
- Automated model retraining with new season data
- RAG/LLM integration for intelligent club information retrieval

---

## Credits & Acknowledgements

- Football-Data for historical datasets
- FPL community data for player metrics
- React, Tailwind, Docker, Render and Vercel for infrastructure and deployment

---

## Repository & Live Demo

**GitHub Repository**  
https://github.com/codex-arv/real-time-premier-league-intelligence-platform

**Live Application**  
https://the90thminute.vercel.app
