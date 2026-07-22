# 🎢 Theme Park Ride Monitoring System — Fog & Edge Computing

A real-time theme park ride safety monitoring platform built on a distributed **Sensor → Edge → Fog → Cloud** architecture. Virtual ride sensors (speed, temperature, vibration, passenger load, brake status) stream data over **MQTT**, which is filtered and analysed at the **Edge**, aggregated and health-scored at the **Fog** layer, and finally stored and visualised on a **Django** dashboard deployed to **AWS EC2**.

---

## 📐 Architecture

```
 ┌────────────┐      MQTT       ┌────────────┐      MQTT       ┌────────────┐      REST API      ┌──────────────────┐
 │  Sensors   │ ───────────────▶│ Edge Node  │ ───────────────▶│ Fog Node   │ ──────────────────▶│  Cloud (Django)   │
 │ (Publisher)│  themepark/     │  (Rules +  │  themepark/     │(Aggregate +│  /api/alerts/       │  + Celery + Redis │
 │            │  sensors        │  Risk Score)│  fog           │ Ride Health│  /api/fog-health/    │  + SQLite + Nginx │
 └────────────┘                 └────────────┘                 └────────────┘                     └──────────────────┘
```

- **Sensors** (`sensors/`) — Simulated Speed, Temperature, Vibration, Passenger, and Brake sensors publish JSON readings to an MQTT broker every few seconds.
- **Edge Node** (`edge_node/`) — Subscribes to raw sensor data, applies threshold rules (`rules.py`), computes a risk score (`detector.py`), and forwards **alerts only** to the Fog layer/cloud — reducing unnecessary network traffic.
- **Fog Node** (`fog_node/`) — Subscribes to sensor data, maintains a rolling window average per sensor type (`aggregator.py`), computes an overall **Ride Health Score** (`ride_health.py`), and reports it to the cloud backend.
- **Cloud Backend** (`backend/`, `monitoring/`) — A Django + Django REST Framework application that:
  - Exposes `POST /api/alerts/` and `POST /api/fog-health/` endpoints (processed asynchronously via **Celery** + **Redis**).
  - Persists data in SQLite (`Ride`, `Sensor`, `SensorReading`, `FogData`, `Alert`, `FogHealth` models).
  - Serves a live dashboard with alert counts, severity breakdown, and ride health.
  - Provides **CSV** and **PDF** exports and a filterable **Reports** page with trend/severity charts.

---

## ✨ Features

- Real-time MQTT-based sensor ingestion
- Edge-layer rule-based anomaly detection & risk scoring
- Fog-layer data aggregation and ride health scoring
- Asynchronous alert persistence with Celery + Redis (with automatic retry/backoff)
- REST API built with Django REST Framework
- Web dashboard with live alerts, severity stats, and ride health
- CSV and PDF export of alert history
- Date-filterable analytics/reports page
- CI/CD pipeline (GitHub Actions) for automatic deployment to AWS EC2

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Sensors / Edge / Fog | Python, `paho-mqtt` |
| Message Broker | MQTT (e.g. Mosquitto) |
| Backend | Django 5.2, Django REST Framework |
| Async Task Queue | Celery, Redis |
| Database | SQLite |
| Reports | ReportLab (PDF), CSV |
| Deployment | AWS EC2, Gunicorn, Nginx, systemd |
| CI/CD | GitHub Actions |

---

## 📂 Project Structure

```
ThemeParkRideMonitoring/
├── backend/            # Django project (settings, urls, wsgi/asgi, celery app)
├── monitoring/         # Django app — models, views, serializers, tasks, dashboard
├── edge_node/           # Edge layer — MQTT subscriber, rules, risk detector, sender
├── fog_node/            # Fog layer — MQTT subscriber, aggregator, ride health, sender
├── sensors/             # Simulated ride sensors + MQTT publisher
├── templates/           # Dashboard HTML templates
├── static/              # CSS/JS for the dashboard
├── .github/workflows/   # GitHub Actions CI/CD (deploy to EC2)
├── requirements.txt
└── manage.py
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- Python 3.11+
- An MQTT broker (e.g. [Mosquitto](https://mosquitto.org/)) running locally
- Redis server running locally

### 1. Clone the repository
```bash
git clone https://github.com/ImaranMurshad/Fog_Egde_Computing_Project.git
cd Fog_Egde_Computing_Project
```

### 2. Create a virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run database migrations
```bash
python manage.py migrate
```

### 4. Start Redis and your MQTT broker
```bash
redis-server
mosquitto
```

### 5. Run the Django backend
```bash
python manage.py runserver
```

### 6. Start Celery (in a new terminal)
```bash
celery -A backend worker --loglevel=info
```

### 7. Start the Fog Node (in a new terminal)
```bash
cd fog_node
python mqtt_subscriber.py
```

### 8. Start the Edge Node (in a new terminal)
```bash
cd edge_node
python mqtt_subscriber.py
```

### 9. Start the Sensor Publisher (in a new terminal)
```bash
cd sensors
python sensor_manager.py
```

Visit **http://127.0.0.1:8000/** to view the live dashboard.

---

## ☁️ Deployment (AWS EC2)

This project is deployed on an **AWS EC2** instance with a static **Elastic IP**, so the address never changes across instance reboots.

**Production stack:** Gunicorn (WSGI server) → Nginx (reverse proxy) → systemd (process supervision), with Redis + Celery running as background services.

### One-time EC2 setup
```bash
# On the EC2 instance
sudo apt update && sudo apt install -y python3-venv python3-pip nginx redis-server

git clone https://github.com/ImaranMurshad/Fog_Egde_Computing_Project.git
cd Fog_Egde_Computing_Project

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py collectstatic --noinput
```

Configure **Gunicorn** and **Nginx** as systemd services / reverse proxy in front of the app, and point your Edge/Fog nodes' `DJANGO_API_URL` / `DJANGO_FOG_API_URL` (see `fog_node/config.py`) at your instance's **Elastic IP**.

### Continuous Deployment
Every push to `main` automatically redeploys via `.github/workflows/deploy.yml`, which:
1. SSHes into the EC2 instance
2. Pulls the latest code
3. Reinstalls dependencies
4. Runs migrations and `collectstatic`
5. Restarts `gunicorn` and `nginx`

Required GitHub Actions secrets:
| Secret | Description |
|---|---|
| `EC2_HOST` | Your EC2 instance's Elastic IP |
| `EC2_USER` | SSH username (e.g. `ubuntu`) |
| `EC2_SSH_KEY` | Private SSH key for the instance |
| `PROJECT_PATH` | Absolute path to the project on the EC2 instance |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Dashboard |
| `POST` | `/api/alerts/` | Submit an edge-layer alert |
| `POST` | `/api/fog-health/` | Submit a fog-layer ride health update |
| `GET` | `/export/csv/` | Download all alerts as CSV |
| `GET` | `/export/pdf/` | Download all alerts as PDF |
| `GET` | `/reports/` | Filterable analytics/reports page |

---

## 📄 License

This project was developed for academic purposes as part of a Fog and Edge Computing module.
