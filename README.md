# 🚀 Predictive Incident Management System

![CI Pipeline](https://github.com/your-username/your-repo-name/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

A cloud-native, machine-learning-powered simulation that shifts incident management from **reactive** (waiting for a crash) to **proactive** (predicting the crash before it happens). 

This system monitors a deliberately vulnerable FastAPI application, collects real-time telemetry, uses Linear Regression to forecast memory exhaustion, and automatically fires proactive alerts to Slack *before* the system hits its Out-Of-Memory (OOM) limits.

---

## 🏗️ Architecture & How It Works

The system consists of four main components working together:

1. **The Vulnerable App (`app.py`)**: A FastAPI service with a `/leak` endpoint that intentionally allocates 10MB of memory per request, simulating a severe memory leak. It also exposes a `/metrics` endpoint for containerized telemetry.
2. **The Telemetry Collector (`collector.py`)**: A background daemon that polls the application's memory usage every 2 seconds and logs it to a shared CSV file (or metrics buffer).
3. **The Predictive Engine (`predictor.py`)**: A machine learning script using `scikit-learn`. It reads the telemetry window, fits a Linear Regression trend line, and projects resource consumption 20 seconds into the future.
4. **The Alerting System**: If the predictive model forecasts that memory will breach the critical threshold (e.g., 80MB) within the projection window, it triggers an automated HTTP POST to a **Slack Incoming Webhook**.

---

## ✨ Features

- 📈 **Real-time Telemetry**: Continuous memory footprint monitoring.
- 🤖 **Machine Learning Forecasting**: Uses Linear Regression to predict future states based on current degradation trends.
- 🐳 **Fully Containerized**: Ready for Docker and Docker Compose with strict resource limits to simulate real-world OOM constraints.
- 💬 **Slack Integration**: Automated, formatted proactive alerts sent directly to your DevOps/SRE channels.
- 🔄 **CI/CD Automated**: GitHub Actions pipeline for code linting and automated Docker image building/pushing to GHCR.

---

## 📋 Prerequisites

To run this project, you will need:
- **Python 3.11+** (for local execution)
- **Docker & Docker Compose** (for containerized execution)
- **cURL** (for the load generator)
- A **Slack Workspace** with an Incoming Webhook configured.

### 🔑 Setting up your Slack Webhook
1. Go to [Slack API: Incoming Webhooks](https://api.slack.com/messaging/webhooks).
2. Create a new app (or use an existing one) and activate Incoming Webhooks.
3. Add a new webhook to your desired channel (e.g., `#devops-alerts`).
4. Copy the Webhook URL.
5. Create a `.env` file in the root of the project and add:
   ```env
   SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
