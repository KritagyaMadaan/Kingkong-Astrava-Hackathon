# **Working project Demo / UI Preview**


https://github.com/user-attachments/assets/51cc60b9-e325-4f00-b497-8fc17d92ff90


# **Autonomous Predictive Bike Maintenance — Agentic AI System**

🏍️ Prevent Failures Before They Happen: 200–500 km Early

A next-generation agentic AI platform that predicts critical two-wheeler failures in advance, turning emergency breakdowns into planned, low-cost maintenance.

This system supports individual riders, workshops, fleets, and OEMs, running entirely as a scalable cloud service.


 # **The Problem (₹198B Lost Annually)**
India’s Two-Wheeler Crisis by the Numbers

124 million riders depend on 2-wheelers daily

₹198 billion annual productivity loss from breakdowns

1,000–2,000 preventable deaths/year linked to maintenance failures

Income loss for gig workers & delivery riders

High repair costs due to avoidable major failures

Roadside emergencies → unsafe + expensive + stressful

Breakdowns are predictable — but today, they are not predicted.


# **Proposed Solution: Agentic AI for Predictive Bike Maintenance**

An agentic AI system that predicts failures 200–500 km before they occur using telemetry, driving patterns, and historical data.

The system automatically:

Detects early-warning patterns

Predicts component failure risk

Estimates remaining life (ETA to failure)

Suggests required actions

Auto-books service appointments

Notifies rider + workshop

Reduces repair cost & eliminates surprise breakdowns


 # **How It Works**

1️⃣ Input Sources

Telematics / IoT sensor data (temperature, vibration, RPM, speed, GPS)

Rider behavior (routes, harsh braking, daily km)

Service history & warranty data

Environmental factors (dust, humidity, terrain)

2️⃣ Processing Pipeline

📥 Data Ingestion Layer

Streams data from IoT devices, telematics APIs, OBD, or mobile app

⚙️ Feature Engineering

Component stress analysis

Riding-pattern risk metrics

Time-series features

Environment-adjusted wear factors

🤖  ML Risk Scoring

XGBoost / LightGBM models

Anomaly detection for vibration, heat, noise

Failure-ETA prediction (remaining km before failure)

🧩  LLM + Agent Layer

LangChain-style agents for decision-making

LLM explanations: “Why this failure is likely”

Auto-service scheduling agent

Diagnostic reasoner: component-level root cause

📤  Output

Component-wise risk score

ETA to failure

Recommended action

Automatic notifications + booking

 # **Tech Stack**

Backend

Python

Flask / FastAPI

Overpass API

Leaflet API

REST APIs (JSON)

Machine Learning

Scikit-learn

XGBoost / LightGBM

Time-series forecasting

Anomaly detection models

LLM + Agent Layer

LangChain-style orchestration

RAG for service history retrieval

GPT-4-class / DeepSeek-chat-class reasoning models

Data & Infrastructure

PostgreSQL (structured data)

Redis (caching, queues)

Docker containers

Cloud deployment (scales automatically)

Integrations with:

Telematics/IoT APIs

Workshop CRM

Booking systems

WhatsApp/SMS alerts

Web dashboard


 # **Scalability**

The platform is designed using a microservices + event-driven architecture, enabling:

Start with a pilot of a few hundred vehicles

Seamlessly scale to millions of vehicles

Add compute nodes without changing core code

Independent services communicate via APIs

Zero downtime during updates

Predictive models retrain automatically as data grows

Scalability = more bikes, not more complexity.

# **Frontend UI**

![Adobe Express - Autonomous Predictive Maintainence Video (2)](https://github.com/user-attachments/assets/b911afc8-0795-4661-bb3e-e8273b54a854)

# **Working Backend**


<img width="1408" height="736" alt="Gemini_Generated_Image_ej8lraej8lraej8l (1)" src="https://github.com/user-attachments/assets/2ad92f37-d05d-40a8-9712-49d51ba8bbbb" />




 # **Local Setup**

1️⃣ Clone the Repository

git clone https://github.com/KritagyaMadaan/EY-Project.git
cd Claude-project

2️⃣ Create a .env File for Secrets / API Keys

Create a .env file in the project root. Example:

.env
OPENAI_API_KEY=your_openai_api_key_here

⚠️ Important: Ensure .env is listed in .gitignore, so you don’t accidentally commit sensitive keys.


3️⃣  Create virtual environment (optional but recommended)

python3 -m venv venv  
source venv/bin/activate

Install dependencies
pip install flask flask-cors langgraph langchain langchain-openai gTTS xgboost pandas numpy joblib


4️⃣ Start Backend API Server
Run  pyton app.py

Your backend will run at:
http://localhost:5000

5️⃣ Run Frontend 
Open okok.html directly in your browser

Double-click:
okok.html

# **API Key Setup (Important)**

The system uses external APIs such as LLMs, telematics providers, communication APIs (SMS/WhatsApp), or map services.
To protect user security and prevent accidental exposure, all API keys must be stored in a .env file.

📍 Where to store your API keys

Create a file in the project root:

.env


Add your keys inside:

OPENAI_API_KEY=your_openai_key_here


You can add as many keys as needed.

🛠️ How the backend loads environment variables
Python backend (FastAPI / Flask)

Environment variables are automatically loaded using:

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")


Or through frameworks that load them automatically.

🌐 How the frontend gets access (secure method)

⚠️ The frontend must NOT directly contain API keys.

Instead:

Frontend → calls your backend API

Backend → loads key from .env

Backend → makes the actual external API request

This keeps all API keys safe and prevents exposure in browser code.

📋 Provide a .env.example file

Include in your repo:

.env.example


Contents:

OPENAI_API_KEY=PUT_YOUR_KEY_HERE


Users copy it:

cp .env.example .env


Then fill in their values.
