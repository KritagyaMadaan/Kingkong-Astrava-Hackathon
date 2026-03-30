# **Working project Demo / UI Preview**

<p align="center">
  <a href="https://youtu.be/NpFsPlzFudA">
    <img src="https://img.youtube.com/vi/NpFsPlzFudA/maxresdefault.jpg" width="700">
  </a>
</p>

## Calling Feature

https://github.com/user-attachments/assets/48602007-43ad-48bc-b2e1-eef05b3c3ae7


# **Autonomous Predictive Maintenance for Vehicles — Agentic AI System**

🏍️ Prevent Failures Before They Happen: 200–500 km Early

A next-generation agentic AI platform that predicts critical vehicles failures in advance, turning emergency breakdowns into planned, low-cost maintenance.

This system supports individual riders, workshops, fleets, and OEMs, running entirely as a scalable cloud service.


 # **The Problem (₹198B Lost Annually)**
₹198 billion annual productivity loss from breakdowns

1,000–2,000 preventable deaths/year linked to maintenance failures

Income loss for gig workers & delivery riders

High repair costs due to avoidable major failures

Roadside emergencies → unsafe + expensive + stressful

Breakdowns are predictable — but today, they are not predicted.


# **Proposed Solution: Agentic AI Autonomous Predictive Maintenance for Vehicles**

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

AI4I 2020 Predictive Maintenance Dataset (temperature, vibration, RPM, speed, GPS)

2️⃣ Processing Pipeline

📥 Data Ingestion Layer

Streams data from IoT devices, telematics APIs, OBD, or mobile app

⚙️ Feature Engineering

Component stress analysis

Riding-pattern risk metrics

Time-series features

Environment-adjusted wear factors

🤖  ML Risk Scoring

uses trained XGBoost models

Anomaly detection for vibration, heat, noise

Failure-ETA prediction (remaining km before failure)

🧩  LLM + Agent Layer

LangChain-style agents for decision-making

LLM explanations: “Why this failure is likely”

Auto-service scheduling agent

Diagnostic reasoner: component-level root cause

📤  Output

Nearest Mechanic



Recommended action

Automatic notifications + booking

## ✨ Features 
### 🗺️ Interactive Map 
Displays the user's current live location 

Shows nearby mechanicson the map

Helps users quickly locate the closest repair service 

### 🔧 Nearest Mechanic Finder 
Detects mechanics based on the user’s location 

Displays mechanic information such as:

     Name 
     Contact details 
     Distance from the user 
     Location on the map 
     
### 🚘 Vehicle Information 
Stores and displays important vehicle details such as: 

     Vehicle model 
     Engine information 
     Usage data 
     Performance metrics
     
### 📍 Location Tracking 

Tracks the real-time location of the vehicle 

Helps users easily identify their position and nearby services 

### 🤖 Vehicle Failure Prediction 

Uses a **machine learning model** to analyze vehicle data 

Predicts possible **vehicle component failures** 

Helps users take preventive maintenance actions 

### 📅 Maintenance Scheduler

Integrated calendar system for vehicle service scheduling

Automatically schedules a maintenance appointment when a critical issue is detected

Users can manually add maintenance appointments

Helps maintain a regular vehicle service history

### 📞 Automated Calling Feature

The system can automatically call mechanics using AI agents.

Workflow:

     AI detects a vehicle issue

     Finds nearby mechanic

     Calls the mechanic automatically

     Books an appointment

     Sends confirmation to the driver

This removes the need for manual phone calls during emergencies.


### 🎙️ AI Voice Assistant

The platform includes an AI-powered voice assistant that helps drivers understand and resolve vehicle issues in real time.

Instead of checking dashboards or reading error logs, drivers can simply talk to the assistant.

How it Works

    The system detects a vehicle issue using predictive maintenance AI.

    The voice assistant informs the driver about the problem.

    The assistant suggests possible solutions.


## 🧠 Dataset Used
### AI4I 2020 Predictive Maintenance Dataset

This project uses the AI4I 2020 Predictive Maintenance Dataset, a well-known dataset used for machine learning research in predictive maintenance.

The dataset contains simulated manufacturing machine data such as:

    Air temperature
    Process temperature
    Rotational speed
    Torque
    Tool wear
    Failure indicators

These parameters are used to train the XGBoost predictive model that identifies possible failure conditions.

 # **Tech Stack**

Python

OpenRouter (LLM Gateway)

Deepseek Chat (LLM Model)

Google Text-to-Speech (gTTS)

Leaflet.js (Maps)  

CartoDB (Map Tiles) 

OpenStreetMap Nominatim (Geocoding) 

Overpass API (POI Data)

MacroDroid (Mobile Automation)

Flask (Web Framework)  

Flask-CORS (API Middleware)

LangChain (LLM Orchestration)

LangChain-OpenAI (LLM Integration)
   
Three.js r128 (3D Graphics) 

Web Audio API (Audio)

Speech Synthesis API (TTS Fallback)  


 # **Scalability**

The platform is designed using a microservices + event-driven architecture, enabling:

Start with a pilot of a few hundred vehicles

Seamlessly scale to millions of vehicles

Add compute nodes without changing core code

Independent services communicate via APIs

Zero downtime during updates

Predictive models retrain automatically as data grows

Scalability = more bikes, not more complexity.

 # **Local Setup**

1️⃣ Clone the Repository

git clone https://github.com/KritagyaMadaan/Kingkong-Astrava-Hackathon.git
cd Kingkong-Astrava-Hackathon

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
Open fleet (2).html directly in your browser

Double-click:
fleet (2).html

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

Contributor: Piyush Singh
