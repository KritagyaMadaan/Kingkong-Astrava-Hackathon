import os
import random
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CORRECT CORS CONFIGURATION (Let the library do the work)
CORS(app, resources={r"/*": {"origins": "*"}})

# ============================
# CONFIGURATION
# ============================
OPENROUTER_API_KEY = "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"

llm = ChatOpenAI(
    model="deepseek/deepseek-chat",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

# ============================
# MACHINE LEARNING MODEL
# ============================
try:
    import pickle
    import numpy as np
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "xgb_failure_model.pkl")
    with open(MODEL_PATH, 'rb') as f:
        failure_model = pickle.load(f)
    print("✅ XGBoost Failure Model Loaded")
except Exception as e:
    print(f"⚠️ Model Loading Failed: {e}")
    failure_model = None

USERS = ["Kritagya", "Atul", "Piyush", "Shivam", "Rahul", "Vikram", "Sanjay", "Deepak", "Amit", "Karan", "Vishal", "Sumit"]
ISSUES_MAP = {
    0: "No Issue Detected",
    1: "Potential Component Failure"
}

def generate_mock_telemetry():
    """Generates realistic sensor data for the XGBoost model."""
    # Features: [air_temp, process_temp, rpm, torque, tool_wear]
    # Normal ranges for this dataset (approximate)
    is_failing = random.random() < 0.3  # 30% chance to generate 'risky' data
    
    if is_failing:
        return np.array([[
            random.uniform(300, 305), # Air temp
            random.uniform(310, 315), # Process temp
            random.uniform(2500, 2800), # High RPM
            random.uniform(50, 70),     # High Torque
            random.uniform(180, 240)    # High Tool Wear
        ]])
    else:
        return np.array([[
            random.uniform(295, 300), 
            random.uniform(305, 310), 
            random.uniform(1400, 1600), 
            random.uniform(30, 45), 
            random.uniform(0, 100)
        ]])

@app.route("/", methods=["GET"])
def home():
    return "✅ Backend Online"

@app.route("/api/start-journey", methods=["POST"])
def start_journey():
    print("--> 🚀 Prediction Request Received!")

    try:
        selected_user = random.choice(USERS)
        
        # 1. Model Prediction
        risk_level = "low"
        detected_issue = "Systems Nominal"
        probability = 0.0

        if failure_model:
            telemetry = generate_mock_telemetry()
            prediction = failure_model.predict(telemetry)[0]
            
            if hasattr(failure_model, 'predict_proba'):
                probs = failure_model.predict_proba(telemetry)[0]
                probability = float(probs[1]) # Probability of failure
            
            if prediction == 1 or probability > 0.5:
                risk_level = "critical" if probability > 0.8 else "warning"
                detected_issue = random.choice(["Engine Overheat", "Turbine Strain", "Mechanical Failure"])
            else:
                # If model says 0, we still occasionally return a minor warning for UI variety
                if random.random() < 0.1:
                    risk_level = "warning"
                    detected_issue = "Maintenance Due Soon"
        
        # 2. AI SCRIPT GENERATION
        print(f"--> Generating Script for {selected_user} ({risk_level})...")
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are a vehicle AI. User: {owner}. Status: {status}. Probability of Failure: {prob}%. "
                "Write a very short (1 sentence) alert. If status is critical, be very urgent."
            )
            chain = prompt | llm
            ai_response = chain.invoke({
                "owner": selected_user, 
                "status": detected_issue, 
                "prob": round(probability * 100, 1)
            })
            voice_script = ai_response.content
        except Exception as e:
            print(f"⚠️ AI Error: {e}")
            voice_script = f"Alert for {selected_user}. {detected_issue} detected."

        # 3. AUDIO GENERATION
        audio_dir = os.path.join(os.path.dirname(__file__), "audio")
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"voice_{uuid.uuid4()}.mp3"
        filepath = os.path.join(audio_dir, filename)
        tts = gTTS(text=voice_script, lang="en")
        tts.save(filepath)

        # 4. RESPONSE
        return jsonify({
            "success": True,
            "data": {
                "owner": selected_user,
                "vehicle": "Fleet-Unit-X",
                "issue": detected_issue,
                "risk": risk_level,
                "probability": probability,
                "voice_script": voice_script,
                "audio_url": f"{request.host_url}audio/{filename}"
            }
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "audio"), filename)

if __name__ == "__main__":
    # Using Port 5000 is fine now that headers are fixed
    print("🚀 Server starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
